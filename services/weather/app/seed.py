from datetime import date, timedelta
import random
from .database import SessionLocal
from .models import Weather

REGION_MAP = {
    "11": "서울", "21": "부산", "22": "대구",
    "23": "인천", "24": "광주", "25": "대전",
    "39": "제주",
}
CONDITIONS = ["맑음", "구름많음", "흐림", "비", "눈"]


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
        print(f"[Seed] 날씨 데이터 {len(records)}건 삽입 완료", flush=True)
    finally:
        db.close()
