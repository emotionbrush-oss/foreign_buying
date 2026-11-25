# foreign_buying

시총 1,000억 원 이상 코스피·코스닥 종목 중 외국인 순매수가 4개 구간 모두 플러스인 종목 목록.
GitHub Pages(`/docs`)로 표를 보여준다. 엑셀식 헤더 필터·정렬 지원.

## 구조
- `docs/index.html` 화면 (정적 페이지)
- `docs/data/latest.json` 최신 스냅샷, `docs/data/YYYY-MM-DD.json` 날짜별 스냅샷, `docs/data/index.json` 날짜 목록
- `scripts/` 수집 후 계산·빌드 스크립트 (rows.txt, metrics.py, news_*.py, build.py)

## 갱신 방식 (반자동)
KRX 데이터는 로그인이 필요해 무인 자동화가 안 된다. 모바일에서 Claude 대화에 "업데이트"를 요청하면
PC의 로그인된 Chrome으로 KRX 데이터를 받고, 지표·뉴스를 갱신해 `docs/data/`에 새 스냅샷을 커밋한다.
권장 시각: 영업일 21:00 KST 이후 (KRX 애프터마켓 종료 후).

## 주의
투자 자문이 아니다. 뉴스는 자동 분류 라벨 요약이라 부정확할 수 있다.
