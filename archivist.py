import os
import sys
import json
import shutil
import datetime

# Windows 콘솔 한글/유니코드 인코딩 안전화
if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

LEDGER_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "asset_ledger.json")
ARCHIVE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "archive", "deprecated_assets")

def load_ledger() -> dict:
    if os.path.exists(LEDGER_PATH):
        try:
            with open(LEDGER_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"  ⚠️ 원장 로드 실패: {e}")
    return {}

def save_ledger(ledger: dict):
    with open(LEDGER_PATH, "w", encoding="utf-8") as f:
        json.dump(ledger, f, ensure_ascii=False, indent=2)

def deprecate_and_isolate_asset(filename: str, reason: str = "도면 개정(Revision) 및 폐기"):
    """
    [코키퍼 2대 책무] 구자료 폐기 기록 및 현장 작업장 격리 보관
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    src_file = os.path.join(base_dir, filename)
    
    os.makedirs(ARCHIVE_DIR, exist_ok=True)
    
    ledger = load_ledger()
    deprecated_list = ledger.setdefault("deprecated_assets", [])
    
    # 장부에 폐기 기록
    if filename not in deprecated_list:
        deprecated_list.append(filename)
    
    history = ledger.setdefault("revision_history", [])
    history.append({
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "action": "DEPRECATE_AND_ISOLATE",
        "file": filename,
        "reason": reason
    })
    
    save_ledger(ledger)
    
    # 실제 파일이 현장에 존재할 경우 아카이브로 격리 이동
    if os.path.exists(src_file):
        dst_file = os.path.join(ARCHIVE_DIR, filename)
        shutil.move(src_file, dst_file)
        print(f"📦 [코키퍼 격리 조치 완료] '{filename}' 현장 퇴출 ➡️ 'archive/deprecated_assets/' 보관 완료!")
    else:
        print(f"📝 [코키퍼 장부 등재] '{filename}' 폐기 자산으로 안전하게 장부 기록 완료!")

def verify_asset_approved(filepath: str) -> bool:
    """
    [코키퍼 1대 책무] 현장에 배포/사용되는 자료가 사장님 승인 최신 자료인지 검증
    """
    if not filepath:
        return False
    base_name = os.path.basename(filepath)
    ledger = load_ledger()
    deprecated_list = ledger.get("deprecated_assets", [])
    
    if base_name in deprecated_list:
        print(f"🚨 [코키퍼 배포 차단] '{base_name}'은(는) 폐기된 구자료입니다! 사용 불가.")
        return False
        
    return True

if __name__ == "__main__":
    print("📦 [코키퍼 - 자산/형상 관리 지킴이] 시스템 점검 가동...")
    print(f"  * 관리 원장: {LEDGER_PATH}")
    print(f"  * 격리 보관소: {ARCHIVE_DIR}")
    print("  * 2대 핵심 책무(최신 승인자료 배포 / 구자료 폐기 및 격리보관) 정상 가동 중!")
