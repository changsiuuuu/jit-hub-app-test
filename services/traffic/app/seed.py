import random
from .database import SessionLocal
from .models import TrafficRoute


def seed_traffic():
    db = SessionLocal()
    try:
        if db.query(TrafficRoute).count() > 0:
            return

        CONGESTION = ["낮음", "보통", "높음"]
        records = [
            TrafficRoute(region_code="11", region_name="서울", type="subway", route_name="1호선", start_stop="소요산", end_stop="인천", congestion=random.choice(CONGESTION), interval_min=3),
            TrafficRoute(region_code="11", region_name="서울", type="subway", route_name="2호선", start_stop="시청", end_stop="시청(순환)", congestion=random.choice(CONGESTION), interval_min=2),
            TrafficRoute(region_code="11", region_name="서울", type="subway", route_name="3호선", start_stop="대화", end_stop="오금", congestion=random.choice(CONGESTION), interval_min=4),
            TrafficRoute(region_code="11", region_name="서울", type="subway", route_name="4호선", start_stop="당고개", end_stop="오이도", congestion=random.choice(CONGESTION), interval_min=4),
            TrafficRoute(region_code="11", region_name="서울", type="subway", route_name="5호선", start_stop="방화", end_stop="마천", congestion=random.choice(CONGESTION), interval_min=5),
            TrafficRoute(region_code="11", region_name="서울", type="bus", route_name="101번", start_stop="도봉산역", end_stop="서울역", congestion=random.choice(CONGESTION), interval_min=8),
            TrafficRoute(region_code="11", region_name="서울", type="bus", route_name="143번", start_stop="수유역", end_stop="광화문", congestion=random.choice(CONGESTION), interval_min=6),
            TrafficRoute(region_code="11", region_name="서울", type="bus", route_name="N37번(심야)", start_stop="강남역", end_stop="노원역", congestion="낮음", interval_min=30),
            TrafficRoute(region_code="21", region_name="부산", type="subway", route_name="1호선", start_stop="노포", end_stop="신평", congestion=random.choice(CONGESTION), interval_min=4),
            TrafficRoute(region_code="21", region_name="부산", type="subway", route_name="2호선", start_stop="장산", end_stop="양산", congestion=random.choice(CONGESTION), interval_min=4),
            TrafficRoute(region_code="21", region_name="부산", type="bus", route_name="51번", start_stop="해운대역", end_stop="부산역", congestion=random.choice(CONGESTION), interval_min=10),
            TrafficRoute(region_code="21", region_name="부산", type="bus", route_name="1003번", start_stop="기장군청", end_stop="서면", congestion=random.choice(CONGESTION), interval_min=15),
            TrafficRoute(region_code="22", region_name="대구", type="subway", route_name="1호선", start_stop="설화명곡", end_stop="안심", congestion=random.choice(CONGESTION), interval_min=5),
            TrafficRoute(region_code="22", region_name="대구", type="subway", route_name="2호선", start_stop="문양", end_stop="영남대", congestion=random.choice(CONGESTION), interval_min=5),
            TrafficRoute(region_code="22", region_name="대구", type="bus", route_name="급행1번", start_stop="북구청", end_stop="수성구청", congestion=random.choice(CONGESTION), interval_min=12),
            TrafficRoute(region_code="23", region_name="인천", type="subway", route_name="1호선", start_stop="계양", end_stop="국제업무지구", congestion=random.choice(CONGESTION), interval_min=6),
            TrafficRoute(region_code="23", region_name="인천", type="subway", route_name="2호선", start_stop="검단오류", end_stop="운연", congestion=random.choice(CONGESTION), interval_min=6),
            TrafficRoute(region_code="23", region_name="인천", type="bus", route_name="9번", start_stop="인천공항", end_stop="부평역", congestion=random.choice(CONGESTION), interval_min=20),
            TrafficRoute(region_code="39", region_name="제주", type="bus", route_name="급행100번", start_stop="제주공항", end_stop="서귀포", congestion=random.choice(CONGESTION), interval_min=30),
            TrafficRoute(region_code="39", region_name="제주", type="bus", route_name="201번", start_stop="제주시청", end_stop="함덕", congestion=random.choice(CONGESTION), interval_min=20),
        ]
        db.bulk_save_objects(records)
        db.commit()
        print(f"[Seed] 교통 데이터 {len(records)}건 삽입 완료", flush=True)
    finally:
        db.close()
