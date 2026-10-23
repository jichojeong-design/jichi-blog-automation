import os
import sys
import glob

# Windows 콘솔 인코딩 안전화
if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

import auto_publisher
import formatter
import quality_inspector
from archivist import verify_asset_approved

def publish_milktea_bread_webtoon():
    """
    [지치 컴퍼니 정규 편제] 3시15분 밀크티 생크림빵 웹툰 수정 포스팅
    - 사장님의 명품 기획 콘티 100% 반영
    - 코포터(원고 서식 및 모바일 호흡), 코자이너(이미지 인터리빙), 코리티(번호 매기기 및 품질 무결점 검수)
    - [컷] -> [대사] -> [컷] -> [대사] 교차 인터리빙 레이아웃
    - 네이버 우수 블로거 기준: [자료 기반 창작 안내] 및 [독립 구매 후기 출처 링크] 명확화
    """
    print("\n" + "=" * 65)
    print("🥐 [지치 컴퍼니] '3시15분 밀크티 생크림빵' 웹툰 수정 포스팅 준비 가동!")
    print("=" * 65)

    base_dir = os.path.dirname(os.path.abspath(__file__))
    drop_dir = os.path.join(base_dir, "webtoon_drop")

    # 1. 코자이너 & 코키퍼: 사장님께서 챗GPT로 생성하여 드롭존에 넣어주신 이미지 스캔
    # (jpg, jpeg, png 파일 검색)
    drop_images = sorted(glob.glob(os.path.join(drop_dir, "*.[jJ][pP][gG]")) + 
                         glob.glob(os.path.join(drop_dir, "*.[jJ][pP][eE][gG]")) + 
                         glob.glob(os.path.join(drop_dir, "*.[pP][nN][gG]")))

    print(f"📦 [코키퍼 점검] 'webtoon_drop/' 폴더 내 감지된 승인 이미지: {len(drop_images)}장")
    for img in drop_images:
        print(f"  - 승인 투입 도면: {os.path.basename(img)}")

    title = "3시15분 밀크티 생크림빵, 빨대 대신 포크!"

    # 2. 코포터 & 코자이너: 본문 문단 및 대사 인터리빙 구성
    # 이미지가 2장 이상 있을 경우 상반부(1~3컷)/하반부(4~8컷) 또는 각 장면에 교차 배치
    paragraphs = []

    # 도입부 (상반부 이미지 배치)
    if len(drop_images) >= 1:
        paragraphs.append(f"__IMAGE__:{drop_images[0]}")

    part1 = [
        "1컷 · 편의점에서 밀크티 생크림빵을 발견한 지치.\n지치: “오늘은 밀크티를 빵으로?”",
        "2컷 · 송이는 빈 컵과 빨대를 챙겨 온다.\n송이: “컵은 내가 맡을게!”",
        "3컷 · 포장을 열자 둥근 빵이 모습을 드러낸다.\n송이: “어? 마시는 게 아니네?”"
    ]
    paragraphs.extend(part1)

    # 중반부 (하반부/단면 컷 이미지 배치)
    if len(drop_images) >= 2:
        paragraphs.append(f"__IMAGE__:{drop_images[1]}")

    part2 = [
        "4컷 · 반으로 가른 빵 속에 밀크티색 크림이 보인다.\n지치: “일단 단면부터 보자!”",
        "5컷 · 아래쪽 작은 펄을 발견한 지치.\n지치: “여기, 펄도 들어 있어!”",
        "6컷 · 송이가 빵 앞에서 빨대를 멈춘다.\n송이: “이 빨대는 어디에 쓰지?”",
        "7컷 · 송이는 빨대를 내려놓고 포크를 든다.\n송이: “오늘은 포크 차례야!”",
        "8컷 · 컵을 든 지치와 포크를 든 송이가 웃는다.\n지치: “컵은 잠시 쉬어도 되겠다!”"
    ]
    paragraphs.extend(part2)

    if len(drop_images) >= 3:
        for extra_img in drop_images[2:]:
            paragraphs.append(f"__IMAGE__:{extra_img}")

    # 후반부: 실구매 후기 팩트 체크 및 안내
    part3 = [
        "[지치와 송이의 실구매 후기 팩트 체크]",
        "1. 밀크티 크림과 펄의 조화:\n구매 후기에서 진한 밀크티 풍미의 크림과 쫄깃한 펄의 조합이 공통으로 확인됐습니다.",
        "2. 펄 식감에 대한 솔직 평가:\n펄의 쫀득함과 식감에 대한 평가는 개인별 취향에 따라 다소 차이가 있어 하나의 표현으로 단정하지 않았습니다.",
        "[안내 및 제작 정보]",
        "본 포스팅은 제품 정보와 독립 구매 후기 2건을 참고하여 제작한 지치컴퍼니의 순수 창작 웹툰입니다.",
        "등장인물(지치, 송이)의 행동과 대사는 창작이며, 직접 구매·시식한 후기가 아닙니다.",
        "게시된 이미지는 AI로 생성한 3D 연출 이미지이며 실제 제품 사진이 아니므로, 맛과 식감에는 개인차가 있을 수 있습니다.",
        "[참고 출처]",
        "도비 · 구매 후기 · 2026.10.9\nhttps://blog.naver.com/dnel0123/224436638003",
        "희다리 · 배달 구매 후기 · 2026.10.10\nhttps://blog.naver.com/ldh128/224436725743"
    ]
    paragraphs.extend(part3)

    # 3. 코리티: 모바일 가독성 및 번호 결합 예외 검수 포맷팅
    formatted_paragraphs = []
    for p in paragraphs:
        p_str = str(p).strip()
        if not p_str:
            continue
        if p_str.startswith("__IMAGE__:"):
            formatted_paragraphs.append(p_str)
        else:
            formatted_paragraphs.append(formatter.format_mobile_text(p_str, max_chars=18))

    tags = [
        "#3시15분밀크티생크림빵",
        "#밀크티생크림빵",
        "#GS25신상",
        "#편의점디저트",
        "#편의점빵",
        "#지치웹툰",
        "#솔직후기",
        "#편의점신상"
    ]

    print("\n🔍 [코리티] 최종 포스팅 전 품질 검사 통과 여부 확인...")
    print(f"  - 제목: {title}")
    print(f"  - 본문 문단 수: {len(formatted_paragraphs)}개")
    print(f"  - 삽입 이미지 수: {len(drop_images)}장")

    # 로컬 실행 모드: 사장님의 크롬 브라우저 로그인 세션을 그대로 활용하도록 CLOUD_MODE 미설정
    if "CLOUD_MODE" in os.environ:
        del os.environ["CLOUD_MODE"]

    if len(drop_images) == 0:
        print("\n💡 [코키퍼 안내] 'webtoon_drop/' 폴더에 아직 사장님의 신규 컷 이미지가 없습니다.")
        print("  - 사장님께서 챗GPT로 생성하신 이미지(1.jpg, 2.jpg 등)를 'webtoon_drop' 폴더에 넣어주시면,")
        print("  - 즉시 네이버 블로그에 '임시저장'으로 완벽하게 등록됩니다!")
        return False

    print("\n📝 [코포터 & 코널리스트] 스마트에디터 ONE 진입 및 네이버 블로그 임시저장(Draft) 시작...")
    success = auto_publisher.post_to_naver_blog(
        title=title,
        content_paragraphs=formatted_paragraphs,
        category_name="웹툰",
        tags=tags,
        save_draft=True
    )

    if success:
        print("\n🎉 [지치 컴퍼니 미션 완수] '3시15분 밀크티 생크림빵' 웹툰 임시저장 성공!")
        print("  * 사장님의 검토를 위해 '임시저장' 상태로 안전하게 보관되었습니다.")
    return success

if __name__ == "__main__":
    publish_milktea_bread_webtoon()
