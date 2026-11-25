import json,datetime,statistics as st
rows=[r.split(",") for r in open('rows.txt').read().strip().split(";")]
def ema(v,n):
    k=2/(n+1);e=[v[0]]
    for x in v[1:]: e.append(x*k+e[-1]*(1-k))
    return e
def rsi(c,n=14):
    g=[max(c[i]-c[i-1],0) for i in range(1,len(c))];l=[max(c[i-1]-c[i],0) for i in range(1,len(c))]
    ag=sum(g[:n])/n;al=sum(l[:n])/n
    for i in range(n,len(g)):
        ag=(ag*(n-1)+g[i])/n;al=(al*(n-1)+l[i])/n
    return 100 if al==0 else 100-100/(1+ag/al)
D=datetime.date;out={}
for r in rows:
    code=r[0];krx7=float(r[8]);krx4=float(r[9])
    d=json.load(open(f'data/{code}.json'))['data'];q=d['indicators']['quote'][0]
    rs=[(datetime.datetime.fromtimestamp(t,datetime.timezone(datetime.timedelta(hours=9))).date(),q['close'][i]) for i,t in enumerate(d['timestamp']) if q['close'][i] is not None]
    dt=[x[0] for x in rs];c=[x[1] for x in rs];n=len(c);last=c[-1]
    def ret(day): i=max(k for k in range(n) if dt[k]<=day); return (last/c[i]-1)*100
    r1=ret(D(2026,11,17));r2=ret(D(2026,11,10));r4=ret(D(2026,10,27));r7=ret(D(2026,7,29))
    ma20=sum(c[-20:])/20;ma50=sum(c[-50:])/50
    sl20='↗' if ma20>sum(c[-25:-5])/20 else '↘';sl50='↗' if ma50>sum(c[-55:-5])/50 else '↘'
    e12=ema(c,12);e26=ema(c,26);m=[a-b for a,b in zip(e12,e26)];sg=ema(m,9);h=[a-b for a,b in zip(m,sg)]
    cross=None
    for k in range(n-1,0,-1):
        if (h[k]>0)!=(h[k-1]>0): cross=(n-1-k,'골든' if h[k]>0 else '데드');break
    R=rsi(c);above=last>ma20
    w=c[-20:];mm=sum(w)/20;sd=st.pstdev(w);pb=(last-(mm-2*sd))/(4*sd)*100
    if abs(krx4)<0.05: v="횡보"
    elif not above: v="꺾임"
    elif sl20=='↗' and h[-1]>0: v="지속·과열" if R>=70 else "지속"
    else: v="둔화"
    out[code]=dict(v=v,rsi=round(R),macd=(f"{cross[1]} ({'오늘' if cross[0]==0 else str(cross[0])+'일째'})" if cross else "-"),gap=round(last/ma20*100),
      ma20=("위 " if above else "아래 ")+sl20,ma50=("위 " if last>ma50 else "아래 ")+sl50,pb=round(pb),r1=round(r1,1),r2=round(r2,1),last=dt[-1].isoformat(),lastpx=round(last),krxpx=float(r[11]),c7=round(r7-krx7,1),c4=round(r4-krx4,1))
json.dump(out,open('metrics.json','w'),ensure_ascii=False)
print(set(v['last'] for v in out.values()))
print([(k,v['lastpx'],v['krxpx'],v['c7'],v['c4']) for k,v in out.items() if abs(v['c7'])>3 or abs(v['c4'])>3 or abs(v['lastpx']/v['krxpx']-1)>0.01])
from collections import Counter;print(Counter(v['v'] for v in out.values()))
