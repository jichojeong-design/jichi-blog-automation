import os
import sys
import subprocess
import base64
import requests
from dotenv import load_dotenv

if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass


def sync_env_to_github_secrets(repo: str = "jichojeong-design/jichi-blog-automation") -> bool:
    """
    로컬 .env의 최신 네이버 세션 쿠키(NAVER_NID_AUT, NAVER_NID_SES) 및 API 키를
    GitHub Actions Repository Secrets에 자동 암호화 업로드하여 로컬-클라우드 불일치를 원천 차단합니다.
    """
    if os.environ.get("GITHUB_ACTIONS") == "true":
        return True

    load_dotenv(override=True)
    try:
        from nacl import encoding, public
    except ImportError:
        return False

    try:
        proc = subprocess.run(
            ["git", "credential", "fill"],
            input="protocol=https\nhost=github.com\n\n",
            capture_output=True,
            text=True,
            timeout=5
        )
        token = None
        for line in proc.stdout.splitlines():
            if line.startswith("password="):
                token = line.split("=", 1)[1].strip()
        if not token:
            return False

        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json"
        }
        pk_resp = requests.get(
            f"https://api.github.com/repos/{repo}/actions/secrets/public-key",
            headers=headers,
            timeout=10
        )
        if pk_resp.status_code != 200:
            return False

        pk_data = pk_resp.json()
        key_id = pk_data["key_id"]
        pub_key = public.PublicKey(pk_data["key"].encode("utf-8"), encoding.Base64Encoder())
        sealed_box = public.SealedBox(pub_key)

        secret_keys = ["NAVER_NID_AUT", "NAVER_NID_SES", "GEMINI_API_KEY", "NAVER_ID"]
        synced = 0
        for s_name in secret_keys:
            val = (os.environ.get(s_name) or "").strip().strip('"').strip("'")
            if not val:
                continue
            encrypted = base64.b64encode(sealed_box.encrypt(val.encode("utf-8"))).decode("utf-8")
            put_resp = requests.put(
                f"https://api.github.com/repos/{repo}/actions/secrets/{s_name}",
                headers=headers,
                json={"encrypted_value": encrypted, "key_id": key_id},
                timeout=10
            )
            if put_resp.status_code in (201, 204):
                synced += 1

        if synced > 0:
            print(f"  🔐 [코부장 보안동기화] 로컬 .env -> GitHub Actions Secrets ({synced}종) 자동 동기화 완료!")
        return synced > 0
    except Exception as e:
        print(f"  ⚠️ GitHub Secrets 자동 동기화 생략: {e}")
        return False


if __name__ == "__main__":
    sync_env_to_github_secrets()
