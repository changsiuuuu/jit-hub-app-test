from .database import SessionLocal
from .models import Tourist


def seed_tourist():
    db = SessionLocal()
    try:
        if db.query(Tourist).count() > 0:
            return

        records = [
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
            Tourist(name="설악산 국립공원", region_code="32", region_name="강원", category="자연",
                    address="강원 속초시 설악산로 833", latitude=38.1195, longitude=128.4654,
                    admission_fee=0, admission_info="무료 (케이블카 별도)",
                    peak_season="10월(단풍), 1~2월(설경)", off_season="장마철(7월)",
                    open_hours="일출~일몰 (코스별 상이)",
                    image_url="https://upload.wikimedia.org/wikipedia/commons/thumb/9/95/Seoraksan_01.jpg/1280px-Seoraksan_01.jpg",
                    description="대한민국의 대표 산악 국립공원으로 울산바위, 공룡능선 등이 유명합니다."),
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
        print(f"[Seed] 관광지 데이터 {len(records)}건 삽입 완료", flush=True)
    finally:
        db.close()
