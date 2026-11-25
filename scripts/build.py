from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter as L
import json
exec(open("news_a.py").read()); exec(open("news_b.py").read())
M=json.load(open("metrics.json"))
rows=[r.split(",") for r in open("rows.txt").read().strip().split(";")]
H=["순서","종목","시장","시가총액(억)","외국인 7/30~8/31(억)","외국인 9월(억)","외국인 10/1~10/18(억)","외국인 최근 10/19~11/24(억)","외국인 누적(억)","누적÷시총(%)","7/29 대비(%)","최근 4주(%)","전종목 상승률 순위","코드","판정","RSI","MACD","이격도(20일, %)","20일선 상하","50일선 상하","최근 1주(%)","최근 2주(%)","4주간 호재·악재 (10/27~11/24)"]
D=[]
for r in rows:
    f=[float(x) for x in r[4:8]]; cum=sum(f); mc=int(r[3])
    D.append((cum/mc*100,r,f,cum))
D.sort(key=lambda x:-x[0])
wb=Workbook(); ws=wb.active; ws.title="외국인 4구간 연속 순매수"; ws.append(H)
for i,(ra,r,f,cum) in enumerate(D,1):
    c=r[0]; n=r[1]; m=M[c]
    ws.append([i,n,{"피":"코스피","닥":"코스닥"}[r[2]],int(r[3]),*f,round(cum,1),round(ra,2),float(r[8]),float(r[9]),int(r[10]),c,m["v"],m["rsi"],m["macd"],m["gap"],m["ma20"],m["ma50"],m["r1"],m["r2"],N.get(n) or C[c]])
last=len(D)+1
thin=Side(style="thin",color="DDDDDD")
for row in ws.iter_rows(min_row=1,max_row=last):
    for c in row:
        c.font=Font(name="Arial",size=10,bold=(c.row==1)); c.border=Border(bottom=thin)
        c.alignment=Alignment(vertical=("center" if c.column!=23 or c.row==1 else "top"),wrap_text=(c.row==1 or c.column==23),horizontal="center" if c.row==1 else None)
        if c.row==1: c.fill=PatternFill("solid",fgColor="F3F3F3")
for r in range(2,last+1):
    ws.cell(r,4).number_format="#,##0"
    for c in (5,6,7,8,9,11,12,21,22): ws.cell(r,c).number_format="#,##0.0"
    ws.cell(r,10).number_format="0.00"; ws.cell(r,13).number_format="#,##0"; ws.cell(r,14).number_format="@"
W=[6,18,8,12,14,12,14,16,12,11,11,11,12,9,10,7,13,11,10,10,10,10,90]
for i,w in enumerate(W,1): ws.column_dimensions[L(i)].width=w
ws.row_dimensions[1].height=48; ws.auto_filter.ref=f"A1:W{last}"; ws.freeze_panes="C2"
fills={"지속":"C6EFCE","지속·과열":"FFD8A8","둔화":"FFF2B3","횡보":"E0E0E0","꺾임":"F8C9C9"}
for r in range(2,last+1): ws.cell(r,15).fill=PatternFill("solid",fgColor=fills[ws.cell(r,15).value])
ws2=wb.create_sheet("요약·기준")
info=[["항목","내용"],
["조건","코스피·코스닥, 2026-11-24 시가총액 1,000억 원 이상, 외국인 순매수가 4개 구간 모두 플러스 (58개 종목). 시총 대비 비중 기준은 적용하지 않음."],
["4개 구간","7/30~8/31, 9/1~9/30, 10/1~10/18, 10/19~11/24 (KRX 투자자별 순매수상위종목, 순매수대금). 앞의 세 구간은 11/13판과 같고 마지막 구간만 11/24까지 연장함."],
["정렬","누적 순매수 ÷ 시가총액(%) 큰 순. 기관 순매수 컬럼은 이번 갱신에서 수집하지 않아 뺐음"],
["7/29 대비 / 최근 4주(%)","KRX 전종목 등락률(수정주가). 7/29 종가→11/24 종가, 10/27 종가→11/24 종가"],
["전종목 상승률 순위","코스피·코스닥 전체 종목 중 7/29 대비 상승률 순위"],
["판정·지표 기준","종가 기준 11/24, 일봉(야후파이낸스) 계산. RSI 14일, MACD 12-26-9(히스토그램 부호로 골든/데드와 경과일), 이격도=종가÷20일 이동평균, 20일선·50일선 위/아래는 종가 위치, 화살표는 이동평균의 5일 전 대비 방향. 판정: 20일선 아래=꺾임 / 20일선 위+선 상승+MACD 골든=지속(RSI 70 이상이면 과열 표시) / 그 외 20일선 위=둔화 / 최근 4주 변동 0%=횡보. 1주·2주 수익률은 11/17·11/10 종가 대비. 참고: KRX 등락률 조회는 시작일 전일 종가를 기준가로 쓰므로 시작일을 하루 늦춰 조회해 기준을 맞춤."],
["호재·악재 컬럼","10/27~11/24 종목별 뉴스 요약. 출처: 마이데일리바이트(mydailybyte.com) 종목뉴스 페이지의 호재/악재/중립 라벨과 요약을 바탕으로 정리. 게시 시점이 'N주 전' 식 상대 표기라 날짜가 부정확하며 경계 기사는 '구간 경계'로 표시. '확인 못함'은 해당 페이지에 기간 내 뉴스가 없다는 뜻이지 이슈가 없었다는 뜻이 아님. 우선주(LG전자우, 삼성전기우, 한화3우B)는 보통주 뉴스로 대체하거나 확인 못함. 자동 분류 라벨이라 해석이 틀릴 수 있어 원문 확인 필요."],
["주의","외국인 순매수 금액이 아주 작은 구간도 '플러스'로 셌습니다. 순매수 지속이 주가 상승을 보장하지 않으며 투자 자문이 아닙니다. 판단은 본인 책임입니다."],
["출처","KRX 정보데이터시스템, 야후파이낸스, 마이데일리바이트"]]
for r in info: ws2.append(r)
for row in ws2.iter_rows():
    for c in row:
        c.font=Font(name="Arial",size=10,bold=(c.row==1 or c.column==1)); c.alignment=Alignment(wrap_text=True,vertical="top")
ws2.column_dimensions["A"].width=22; ws2.column_dimensions["B"].width=110
wb.save("외국인_4구간_연속순매수_58종목_1124.xlsx")
old=set("""파마리서치 키다리스튜디오 글로벌텍스프리 빙그레 한국알콜 고스트스튜디오 지어소프트 대한항공 삼성전기우 CJ 제주항공 HL만도 GS건설 KG스틸 대양전기공업 현대해상 제룡전기 에스티팜 세아제강 SK이노베이션 한화3우B 에이피알 티엑스알로보틱스 오로라 케어젠 흥아해운 한국가스공사 케이씨 현대힘스 동아제약 제이브이엠 HMM 나이스정보통신 성우하이텍 한국공항 롯데손해보험 데브시스터즈 HJ중공업 넥써쓰 HDC 잇츠한불 세방 수산세보틱스 아모레퍼시픽홀딩스 KCC 노루페인트 케이알엠 옵투스제약 한라IMS SK바이오사이언스 CJ프레시웨이 서연이화 SJG세종 대원산업 케이프 동부건설 DKME 태광산업 서희건설 이연제약 동서 이엘씨 에코아이 미원화학 제일파마홀딩스 탑런토탈솔루션""".split())
new={r[1] for r in rows}
print("신규",sorted(new-old)); print("제외",sorted(old-new))
print(ws.max_row, [ (ws.cell(i,2).value,ws.cell(i,15).value) for i in range(2,6)])
