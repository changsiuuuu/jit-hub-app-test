from datetime import date, timedelta
import random
from .database import SessionLocal
from .models import Weather, TrafficRoute, Tourist

REGION_MAP = {
    "11": "서울", "21": "부산", "22": "대구",
    "23": "인천", "24": "광주", "25": "대전",
    "39": "제주",
}
CONDITIONS = ["맑음", "구름많음", "흐림", "비", "눈"]


# ── 날씨 시드 ──────────────────────────────────────────────
def seed_weather():
    db = SessionLocal()
    try:
        if db.query(Weather).count() > 0:
            return
        records = []
        start = date(2025, 1, 1)
        end = date(2026, 12, 31)
        current = start
        while current <= end:
            month = current.month
            if month in [12, 1, 2]:
                temp_max = random.uniform(-5, 7)
                temp_min = random.uniform(-12, 0)
                condition = random.choices(CONDITIONS, weights=[20, 25, 30, 10, 15])[0]
            elif month in [3, 4, 5]:
                temp_max = random.uniform(12, 22)
                temp_min = random.uniform(4, 14)
                condition = random.choices(CONDITIONS, weights=[40, 30, 20, 8, 2])[0]
            elif month in [6, 7, 8]:
                temp_max = random.uniform(28, 36)
                temp_min = random.uniform(22, 28)
                condition = random.choices(CONDITIONS, weights=[20, 20, 20, 35, 5])[0]
            else:
                temp_max = random.uniform(15, 25)
                temp_min = random.uniform(7, 17)
                condition = random.choices(CONDITIONS, weights=[45, 30, 15, 8, 2])[0]
            for code, name in REGION_MAP.items():
                offset = {"21": 2, "39": 3, "22": 1}.get(code, 0)
                records.append(Weather(
                    region_code=code, region_name=name, date=current,
                    temp_max=round(temp_max + offset, 1),
                    temp_min=round(temp_min + offset, 1),
                    humidity=round(random.uniform(40, 90), 1),
                    precipitation=round(random.uniform(0, 30), 1) if condition in ["비", "눈"] else 0.0,
                    condition=condition,
                ))
            current += timedelta(days=1)
        db.bulk_save_objects(records)
        db.commit()
        print(f"[Seed] 날씨 데이터 {len(records)}건 삽입 완료")
    finally:
        db.close()


# ── 교통 시드 ──────────────────────────────────────────────
def seed_traffic():
    db = SessionLocal()
    try:
        if db.query(TrafficRoute).count() > 0:
            return

        CONGESTION = ["낮음", "보통", "높음"]
        records = [
            # 서울 지하철
            TrafficRoute(region_code="11", region_name="서울", type="subway", route_name="1호선", start_stop="소요산", end_stop="인천", congestion=random.choice(CONGESTION), interval_min=3),
            TrafficRoute(region_code="11", region_name="서울", type="subway", route_name="2호선", start_stop="시청", end_stop="시청(순환)", congestion=random.choice(CONGESTION), interval_min=2),
            TrafficRoute(region_code="11", region_name="서울", type="subway", route_name="3호선", start_stop="대화", end_stop="오금", congestion=random.choice(CONGESTION), interval_min=4),
            TrafficRoute(region_code="11", region_name="서울", type="subway", route_name="4호선", start_stop="당고개", end_stop="오이도", congestion=random.choice(CONGESTION), interval_min=4),
            TrafficRoute(region_code="11", region_name="서울", type="subway", route_name="5호선", start_stop="방화", end_stop="마천", congestion=random.choice(CONGESTION), interval_min=5),
            # 서울 버스
            TrafficRoute(region_code="11", region_name="서울", type="bus", route_name="101번", start_stop="도봉산역", end_stop="서울역", congestion=random.choice(CONGESTION), interval_min=8),
            TrafficRoute(region_code="11", region_name="서울", type="bus", route_name="143번", start_stop="수유역", end_stop="광화문", congestion=random.choice(CONGESTION), interval_min=6),
            TrafficRoute(region_code="11", region_name="서울", type="bus", route_name="N37번(심야)", start_stop="강남역", end_stop="노원역", congestion="낮음", interval_min=30),
            # 부산 지하철
            TrafficRoute(region_code="21", region_name="부산", type="subway", route_name="1호선", start_stop="노포", end_stop="신평", congestion=random.choice(CONGESTION), interval_min=4),
            TrafficRoute(region_code="21", region_name="부산", type="subway", route_name="2호선", start_stop="장산", end_stop="양산", congestion=random.choice(CONGESTION), interval_min=4),
            # 부산 버스
            TrafficRoute(region_code="21", region_name="부산", type="bus", route_name="51번", start_stop="해운대역", end_stop="부산역", congestion=random.choice(CONGESTION), interval_min=10),
            TrafficRoute(region_code="21", region_name="부산", type="bus", route_name="1003번", start_stop="기장군청", end_stop="서면", congestion=random.choice(CONGESTION), interval_min=15),
            # 대구 지하철
            TrafficRoute(region_code="22", region_name="대구", type="subway", route_name="1호선", start_stop="설화명곡", end_stop="안심", congestion=random.choice(CONGESTION), interval_min=5),
            TrafficRoute(region_code="22", region_name="대구", type="subway", route_name="2호선", start_stop="문양", end_stop="영남대", congestion=random.choice(CONGESTION), interval_min=5),
            # 대구 버스
            TrafficRoute(region_code="22", region_name="대구", type="bus", route_name="급행1번", start_stop="북구청", end_stop="수성구청", congestion=random.choice(CONGESTION), interval_min=12),
            # 인천 지하철
            TrafficRoute(region_code="23", region_name="인천", type="subway", route_name="1호선", start_stop="계양", end_stop="국제업무지구", congestion=random.choice(CONGESTION), interval_min=6),
            TrafficRoute(region_code="23", region_name="인천", type="subway", route_name="2호선", start_stop="검단오류", end_stop="운연", congestion=random.choice(CONGESTION), interval_min=6),
            # 인천 버스
            TrafficRoute(region_code="23", region_name="인천", type="bus", route_name="9번", start_stop="인천공항", end_stop="부평역", congestion=random.choice(CONGESTION), interval_min=20),
            # 제주 버스
            TrafficRoute(region_code="39", region_name="제주", type="bus", route_name="급행100번", start_stop="제주공항", end_stop="서귀포", congestion=random.choice(CONGESTION), interval_min=30),
            TrafficRoute(region_code="39", region_name="제주", type="bus", route_name="201번", start_stop="제주시청", end_stop="함덕", congestion=random.choice(CONGESTION), interval_min=20),
        ]
        db.bulk_save_objects(records)
        db.commit()
        print(f"[Seed] 교통 데이터 {len(records)}건 삽입 완료")
    finally:
        db.close()


# ── 관광지 시드 ─────────────────────────────────────────────
def seed_tourist():
    db = SessionLocal()
    try:
        if db.query(Tourist).count() > 0:
            return

        records = [
            # 서울
            Tourist(name="경복궁", region_code="11", region_name="서울", category="역사",
                    address="서울 종로구 사직로 161", latitude=37.5796, longitude=126.9770,
                    admission_fee=3000, admission_info="성인 3,000원 / 청소년 1,500원 / 어린이 1,500원",
                    peak_season="4월~5월, 9월~10월", off_season="12월~2월",
                    open_hours="09:00~18:00 (화요일 휴무)",
                    image_url="https://upload.wikimedia.org/wikipedia/commons/thumb/1/13/Gyeongbokgung.jpg/1280px-Gyeongbokgung.jpg",
                    description="조선 왕조의 법궁으로, 서울 도심에 위치한 대표 궁궐입니다."),
            Tourist(name="남산서울타워", region_code="11", region_name="서울", category="문화",
                    address="서울 용산구 남산공원길 105", latitude=37.5512, longitude=126.9882,
                    admission_fee=21000, admission_info="성인 21,000원 / 어린이 14,000원",
                    peak_season="연중 (야경 명소)", off_season="없음",
                    open_hours="10:00~23:00 (연중무휴)",
                    image_url="https://upload.wikimedia.org/wikipedia/commons/thumb/4/46/N_Seoul_Tower_2019.jpg/800px-N_Seoul_Tower_2019.jpg",
                    description="서울 남산에 위치한 전망대로, 서울 야경을 한눈에 볼 수 있습니다."),
            Tourist(name="북촌한옥마을", region_code="11", region_name="서울", category="문화",
                    address="서울 종로구 계동길 37", latitude=37.5826, longitude=126.9830,
                    admission_fee=0, admission_info="무료",
                    peak_season="3월~5월, 9월~11월", off_season="1월~2월",
                    open_hours="상시 개방",
                    image_url="https://upload.wikimedia.org/wikipedia/commons/thumb/8/8e/Bukchon_Hanok_Village.jpg/1280px-Bukchon_Hanok_Village.jpg",
                    description="600년 역사의 한옥촌으로 전통 건축물과 골목을 체험할 수 있습니다."),
            # 부산
            Tourist(name="해운대해수욕장", region_code="21", region_name="부산", category="자연",
                    address="부산 해운대구 해운대해변로 264", latitude=35.1586, longitude=129.1603,
                    admission_fee=0, admission_info="무료",
                    peak_season="7월~8월", off_season="11월~3월",
                    open_hours="상시 개방 (수영: 7~8월 09:00~18:00)",
                    image_url="https://upload.wikimedia.org/wikipedia/commons/thumb/d/d5/Haeundae_Beach.jpg/1280px-Haeundae_Beach.jpg",
                    description="대한민국 대표 해수욕장으로, 여름 시즌 수백만 명이 방문하는 명소입니다."),
            Tourist(name="감천문화마을", region_code="21", region_name="부산", category="문화",
                    address="부산 사하구 감내2로 203", latitude=35.0976, longitude=129.0107,
                    admission_fee=0, admission_info="무료 (일부 시설 유료)",
                    peak_season="봄·가을", off_season="여름(더위), 겨울",
                    open_hours="09:00~18:00",
                    image_url="https://upload.wikimedia.org/wikipedia/commons/thumb/e/e9/Gamcheon_Culture_Village.jpg/1280px-Gamcheon_Culture_Village.jpg",
                    description="알록달록한 집들이 계단식으로 펼쳐진 부산의 마추픽추로 불리는 마을입니다."),
            # 제주
            Tourist(name="한라산 국립공원", region_code="39", region_name="제주", category="자연",
                    address="제주 서귀포시 토평동 산15-1", latitude=33.3617, longitude=126.5292,
                    admission_fee=0, admission_info="무료",
                    peak_season="10월~11월(단풍), 1월~2월(설경)", off_season="장마철(6~7월)",
                    open_hours="일출 후 1시간 ~ 입산 통제 시간 (코스별 상이)",
                    image_url="https://upload.wikimedia.org/wikipedia/commons/thumb/9/9e/Hallasan_National_Park.jpg/1280px-Hallasan_National_Park.jpg",
                    description="대한민국 최고봉(1,950m)으로 사계절 다양한 자연경관을 자랑합니다."),
            Tourist(name="성산일출봉", region_code="39", region_name="제주", category="자연",
                    address="제주 서귀포시 성산읍 일출로 284-12", latitude=33.4580, longitude=126.9425,
                    admission_fee=2000, admission_info="성인 2,000원 / 청소년 1,000원 / 어린이 1,000원",
                    peak_season="1월 1일(일출), 4~5월, 9~10월", off_season="여름 장마철",
                    open_hours="07:00~20:00 (계절별 상이)",
                    image_url="https://upload.wikimedia.org/wikipedia/commons/thumb/1/15/Sunrise_Peak%2C_Jeju.jpg/1280px-Sunrise_Peak%2C_Jeju.jpg",
                    description="유네스코 세계자연유산으로 등재된 제주의 대표 화산체입니다."),
            Tourist(name="천지연폭포", region_code="39", region_name="제주", category="자연",
                    address="제주 서귀포시 천지동 667-7", latitude=33.2475, longitude=126.5617,
                    admission_fee=2000, admission_info="성인 2,000원 / 청소년 1,100원 / 어린이 600원",
                    peak_season="봄·여름(수량 풍부)", off_season="건기(가뭄 시)",
                    open_hours="09:00~22:00 (연중무휴)",
                    image_url="https://upload.wikimedia.org/wikipedia/commons/thumb/5/5b/Cheonjiyeon_falls.jpg/800px-Cheonjiyeon_falls.jpg",
                    description="천상의 연못에서 떨어지는 폭포라는 뜻으로, 높이 22m의 제주 명폭입니다."),
            # 강원
            Tourist(name="설악산 국립공원", region_code="32", region_name="강원", category="자연",
                    address="강원 속초시 설악산로 833", latitude=38.1195, longitude=128.4654,
                    admission_fee=0, admission_info="무료 (케이블카 별도)",
                    peak_season="10월(단풍), 1~2월(설경)", off_season="장마철(7월)",
                    open_hours="일출~일몰 (코스별 상이)",
                    image_url="https://upload.wikimedia.org/wikipedia/commons/thumb/9/95/Seoraksan_01.jpg/1280px-Seoraksan_01.jpg",
                    description="대한민국의 대표 산악 국립공원으로 울산바위, 공룡능선 등이 유명합니다."),
            # 경북
            Tourist(name="불국사", region_code="37", region_name="경북", category="역사",
                    address="경북 경주시 불국로 385", latitude=35.7897, longitude=129.3317,
                    admission_fee=5000, admission_info="성인 5,000원 / 청소년 3,500원 / 어린이 2,500원",
                    peak_season="봄(벚꽃), 가을(단풍)", off_season="겨울",
                    open_hours="07:00~18:00 (계절별 상이)",
                    image_url="https://upload.wikimedia.org/wikipedia/commons/thumb/4/41/Bulguksa_2014.jpg/1280px-Bulguksa_2014.jpg",
                    description="유네스코 세계문화유산으로 신라 불교 문화의 정수를 보여주는 사찰입니다."),
        ]
        db.bulk_save_objects(records)
        db.commit()
        print(f"[Seed] 관광지 데이터 {len(records)}건 삽입 완료")
    finally:
        db.close()


def run_all():
    seed_weather()
    seed_traffic()
    seed_tourist()
