#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SACRA - Standalone Version
Eine einzelne ausführbare Datei!

"""

import math, sys, argparse
from datetime import datetime, timedelta
from decimal import Decimal, getcontext

# Hexagramm-Datenbank (gekürzt für Kompaktheit)
HEX_DB = [
    {"n": 1, "name": "Das Schöpferische", "j": "Das Schöpferische wirkt erhabenes Gelingen"},
    {"n": 2, "name": "Das Empfangende", "j": "Das Empfangende wirkt erhabenes Gelingen"},
    {"n": 3, "name": "Die Anfangsschwierigkeit", "j": "Die Anfangsschwierigkeit wirkt erhabenes Gelingen"},
    {"n": 4, "name": "Die Jugendtorheit", "j": "Jugendtorheit hat Gelingen"},
    {"n": 5, "name": "Das Warten", "j": "Das Warten. Wenn du wahrhaftig bist, so hast du Licht und Gelingen"},
    {"n": 6, "name": "Der Streit", "j": "Der Streit: Du bist wahrhaftig und wirst gehemmt"},
    {"n": 7, "name": "Das Heer", "j": "Das Heer braucht Beharrlichkeit"},
    {"n": 8, "name": "Das Zusammenhalten", "j": "Zusammenhalten bringt Heil"},
    {"n": 9, "name": "Des Kleinen Zähmungskraft", "j": "Des Kleinen Zähmungskraft hat Gelingen"},
    {"n": 10, "name": "Das Auftreten", "j": "Auftreten. Auf den Schwanz des Tigers treten"},
    {"n": 11, "name": "Der Friede", "j": "Der Friede. Das Kleine geht, das Große kommt. Heil!"},
    {"n": 12, "name": "Die Stockung", "j": "Stockung durch schlechte Menschen"},
    {"n": 13, "name": "Gemeinschaft mit Menschen", "j": "Gemeinschaft mit Menschen im Freien: Gelingen"},
    {"n": 14, "name": "Der Besitz von Großem", "j": "Der Besitz von Großem: erhabenes Gelingen"},
    {"n": 15, "name": "Die Bescheidenheit", "j": "Bescheidenheit schafft Gelingen"},
    {"n": 16, "name": "Die Begeisterung", "j": "Die Begeisterung. Fördernd ist es"},
    {"n": 17, "name": "Die Nachfolge", "j": "Die Nachfolge wirkt erhabenes Gelingen"},
    {"n": 18, "name": "Die Arbeit am Verdorbenen", "j": "Die Arbeit am Verdorbenen hat erhabenes Gelingen"},
    {"n": 19, "name": "Die Annäherung", "j": "Die Annäherung hat erhabenes Gelingen"},
    {"n": 20, "name": "Die Betrachtung", "j": "Die Betrachtung. Die Abwaschung ist vollzogen"},
    {"n": 21, "name": "Das Durchbeißen", "j": "Das Durchbeißen hat Gelingen"},
    {"n": 22, "name": "Die Anmut", "j": "Die Anmut hat Gelingen"},
    {"n": 23, "name": "Die Zersplitterung", "j": "Zersplitterung. Nicht fördernd ist es"},
    {"n": 24, "name": "Die Wiederkehr", "j": "Die Wiederkehr. Gelingen"},
    {"n": 25, "name": "Die Unschuld", "j": "Die Unschuld. Erhabenes Gelingen"},
    {"n": 26, "name": "Des Großen Zähmungskraft", "j": "Des Großen Zähmungskraft. Beharrlichkeit fördernd"},
    {"n": 27, "name": "Die Ernährung", "j": "Die Ernährung. Beharrlichkeit bringt Heil"},
    {"n": 28, "name": "Des Großen Übergewicht", "j": "Des Großen Übergewicht. Der Firstbalken biegt sich durch"},
    {"n": 29, "name": "Das Abgründige", "j": "Das Abgründige, wiederholt"},
    {"n": 30, "name": "Das Haftende", "j": "Das Haftende. Beharrlichkeit ist fördernd"},
    {"n": 31, "name": "Die Einwirkung", "j": "Die Einwirkung. Gelingen"},
    {"n": 32, "name": "Die Dauer", "j": "Die Dauer. Gelingen. Kein Makel"},
    {"n": 33, "name": "Der Rückzug", "j": "Der Rückzug. Gelingen"},
    {"n": 34, "name": "Des Großen Macht", "j": "Des Großen Macht. Beharrlichkeit ist fördernd"},
    {"n": 35, "name": "Der Fortschritt", "j": "Der Fortschritt. Der mächtige Fürst"},
    {"n": 36, "name": "Die Verfinsterung des Lichts", "j": "Die Verfinsterung des Lichts"},
    {"n": 37, "name": "Die Sippe", "j": "Die Sippe. Beharrlichkeit der Frau ist fördernd"},
    {"n": 38, "name": "Der Gegensatz", "j": "Der Gegensatz. In kleinen Dingen Gelingen"},
    {"n": 39, "name": "Das Hemmnis", "j": "Das Hemmnis. Fördernd ist der Südwesten"},
    {"n": 40, "name": "Die Befreiung", "j": "Die Befreiung. Fördernd ist der Südwesten"},
    {"n": 41, "name": "Die Minderung", "j": "Die Minderung mit Wahrhaftigkeit bringt erhabenes Heil"},
    {"n": 42, "name": "Die Mehrung", "j": "Die Mehrung. Fördernd ist es, etwas zu unternehmen"},
    {"n": 43, "name": "Der Durchbruch", "j": "Der Durchbruch. Man muss die Sache am Hof des Königs wahrhaftig kundtun"},
    {"n": 44, "name": "Das Entgegenkommen", "j": "Das Entgegenkommen. Das Weib ist mächtig"},
    {"n": 45, "name": "Die Sammlung", "j": "Die Sammlung. Gelingen"},
    {"n": 46, "name": "Das Empordringen", "j": "Das Empordringen hat erhabenes Gelingen"},
    {"n": 47, "name": "Die Bedrängnis", "j": "Die Bedrängnis. Gelingen. Beharrlichkeit"},
    {"n": 48, "name": "Der Brunnen", "j": "Der Brunnen. Man kann die Stadt wechseln"},
    {"n": 49, "name": "Die Umwälzung", "j": "Die Umwälzung. An deinem eigenen Tage wirst du geglaubt"},
    {"n": 50, "name": "Der Tiegel", "j": "Der Tiegel. Erhabenes Heil. Gelingen"},
    {"n": 51, "name": "Das Erregende", "j": "Das Erregende bringt Gelingen"},
    {"n": 52, "name": "Das Stillehalten", "j": "Stillehalten seines Rückens"},
    {"n": 53, "name": "Die Entwicklung", "j": "Die Entwicklung. Das Mädchen wird verheiratet. Heil!"},
    {"n": 54, "name": "Das heiratende Mädchen", "j": "Das heiratende Mädchen. Unternehmungen bringen Unheil"},
    {"n": 55, "name": "Die Fülle", "j": "Die Fülle hat Gelingen"},
    {"n": 56, "name": "Der Wanderer", "j": "Der Wanderer. Gelingen im Kleinen"},
    {"n": 57, "name": "Das Sanfte", "j": "Das Sanfte. Gelingen im Kleinen"},
    {"n": 58, "name": "Das Heitere", "j": "Das Heitere. Gelingen"},
    {"n": 59, "name": "Die Auflösung", "j": "Die Auflösung. Gelingen"},
    {"n": 60, "name": "Die Beschränkung", "j": "Beschränkung. Gelingen"},
    {"n": 61, "name": "Innere Wahrheit", "j": "Innere Wahrheit. Schweine und Fische. Heil!"},
    {"n": 62, "name": "Des Kleinen Übergewicht", "j": "Des Kleinen Übergewicht. Gelingen"},
    {"n": 63, "name": "Nach der Vollendung", "j": "Gelingen im Kleinen. Fördernd ist Beharrlichkeit"},
    {"n": 64, "name": "Vor der Vollendung", "j": "Vor der Vollendung. Gelingen"}
]

TRIG = {0:"☷",1:"☶",2:"☵",3:"☴",4:"☳",5:"☲",6:"☱",7:"☰"}
TRIG_N = ["Erde","Berg","Wasser","Wind","Donner","Feuer","See","Himmel"]
TZ_T = ["Imix","Ik","Akbal","Kan","Chicchan","Cimi","Manik","Lamat","Muluc","Oc","Chuen","Eb","Ben","Ix","Men","Cib","Caban","Etznab","Cauac","Ahau"]
HB_M = ["Pop","Wo","Sip","Sotz","Sek","Xul","Yaxkin","Mol","Chen","Yax","Sak","Keh","Mak","Kankin","Muan","Pax","Kayab","Kumku","Wayeb"]

def pi_calc(d=16):
    getcontext().prec=max(d+50,100)
    C=426880*Decimal(10005).sqrt()
    K,M,X,L,S=Decimal(6),Decimal(1),Decimal(1),Decimal(13591409),Decimal(13591409)
    for i in range(1,10):
        M=M*(K**3-16*K)/((i)**3);K+=12;L+=545140134;X*=-262537412640768000;S+=Decimal(M*L)/X
    p=str(C/S);return p.split('.')[1][:d] if '.' in p else "0"*d

def fib(n):
    if n<=0:return []
    if n==1:return [0]
    s=[0,1]
    while len(s)<n:s.append(s[-1]+s[-2])
    return s

def jd(d):
    a=(14-d.month)//12;y=d.year+4800-a;m=d.month+12*a-3
    return d.day+(153*m+2)//5+365*y+y//4-y//100+y//400-32045

def maya(d):
    j=jd(d);t=int(j-584283)
    tn=((t+4)%13);tn=13 if tn==0 else tn
    tt=TZ_T[(t+19)%20];hp=(t+348)%365
    hm=HB_M[hp//20 if hp<360 else 18];ht=hp%20 if hp<360 else hp-360
    vt=t%584;vp="Morgenstern" if vt<236 else "Obere Konjunktion" if vt<326 else "Abendstern" if vt<576 else "Untere Konjunktion"
    return {'tz_n':tn,'tz_t':tt,'tz_p':(t%260)+1,'hb_t':ht,'hb_m':hm,'vp':vp}

def hex_calc(d):
    tu=(d.year%100+d.month+d.day+d.hour)%8
    ra=math.degrees(math.atan2(math.sin(math.radians((d.timetuple().tm_yday-80)*360/365.25))*math.cos(math.radians(23.44)),math.cos(math.radians((d.timetuple().tm_yday-80)*360/365.25))))%360
    to=(int(ra*12/360)+int((0+90)/30))%8
    hv=(tu<<3)|to;hn=hv+1;hd=next((h for h in HEX_DB if h['n']==hn),{})
    y=bin(hv).count('1');return {'hn':hn,'hv':hv,'name':hd.get('name','?'),'j':hd.get('j',''),'tu':tu,'to':to,'y':y,'yi':6-y}

def qual(h):
    j=h['j'].lower()
    p=sum(10 for w in ['gelingen','heil','fördernd'] if w in j)
    n=sum(10 for w in ['unheil','gefahr','makel'] if w in j)
    b=(6-abs(h['y']-h['yi']))*10;s=min(100,max(0,p+b-n))
    return {'s':s,'st':'GÜNSTIG' if s>=70 else 'NEUTRAL' if s>=50 else 'HERAUSFORDERND' if s>=30 else 'SCHWIERIG'}

def sacra(d=None):
    if d is None:d=datetime.now()
    m=maya(d);tp=m['tz_p']-1
    pd=pi_calc(260);pz=int(pd[min(tp,len(pd)-1)])
    fs=fib(min(tp+1,93));fr=fs[tp] if tp<len(fs) else 0
    h=hex_calc(d);iq=qual(h)
    pe=(pz/9.0)*100;he=((h['tu']+h['to'])/14.0)*100
    fm=math.log(fr+1)/math.log(1.618) if fr>0 else 0
    e=((pe+he)/2.0)*(1+fm/10.0)
    r=((pz+h['hv']+tp)%9)+1;ss=min(100,r*10+e*0.3)
    sq='EXZELLENT' if ss>=80 else 'SEHR GUT' if ss>=65 else 'GUT' if ss>=50 else 'MODERAT' if ss>=35 else 'TRANSFORMATIV'
    return {'d':d,'sig':f"P{pz}-H{h['hv']:02X}-T{tp:03d}",'ss':ss,'sq':sq,'iq':iq,'h':h,'pz':pz,'fr':fr,'tp':tp,'m':m,'e':e}

def show(s,k=False):
    print(f"\n{'═'*80}\nSACRA - {s['d'].strftime('%d.%m.%Y %H:%M:%S')}\n{'═'*80}")
    print(f"🔐 {s['sig']}")
    print(f"\n✨ SACRA: {s['sq']} ({s['ss']:.1f}/100)")
    print(f"🔯 I-GING: {s['iq']['st']} ({s['iq']['s']:.1f}/100)")
    print(f"\n🔄 HEXAGRAMM {s['h']['hn']}: {s['h']['name']}")
    print(f"   {TRIG[s['h']['to']]} {TRIG_N[s['h']['to']]} / {TRIG[s['h']['tu']]} {TRIG_N[s['h']['tu']]}")
    print(f"   Balance: {'●'*(6-abs(s['h']['y']-s['h']['yi']))}{'○'*abs(s['h']['y']-s['h']['yi'])}")
    print(f"   {s['h']['j']}")
    if not k:
        print(f"\n🌀 PI: {s['pz']} | Fib: {s['fr']:,} | Pos: {s['tp']}/260")
        print(f"📅 MAYA: {s['m']['tz_n']} {s['m']['tz_t']} | {s['m']['hb_t']} {s['m']['hb_m']} | {s['m']['vp']}")
        print(f"⚡ ENERGIE: {s['e']:.1f}/100")
    print(f"{'═'*80}\n")

def week():
    print(f"\n{'═'*80}\nWOCHEN-ÜBERSICHT\n{'═'*80}\n")
    print(f"{'Tag':<12}|{'Datum':<12}|{'SACRA':<10}|{'I-Ging':<10}|{'Hex'}")
    print('─'*80)
    for i in range(7):
        d=datetime.now()+timedelta(days=i)
        s=sacra(d)
        print(f"{'→' if i==0 else ' '} {d.strftime('%a'):<9}|{d.strftime('%d.%m.'):<12}|{s['ss']:3.0f}/100   |{s['iq']['s']:3.0f}/100   |{s['h']['name'][:20]}")
    print('─'*80+'\n')

def optimal(t=30):
    print(f"\n{'═'*80}\nOPTIMALE MOMENTE ({t} Tage)\n{'═'*80}\n")
    r=[]
    for i in range(t):
        s=sacra(datetime.now()+timedelta(days=i))
        if s['ss']>=70 and s['iq']['s']>=60:r.append(s)
    r.sort(key=lambda x:(x['ss']+x['iq']['s'])/2,reverse=True)
    for i,s in enumerate(r[:5],1):
        print(f"{i}. {s['d'].strftime('%d.%m.%Y %A')}")
        print(f"   SACRA: {s['ss']:.0f} | I-Ging: {s['iq']['s']:.0f} | {s['h']['name']}\n")
    if not r:print("Keine optimalen Momente gefunden.\n")
    print('─'*80+'\n')

if __name__=="__main__":
    p=argparse.ArgumentParser(description="SACRA Standalone")
    p.add_argument('-d','--datum',help='YYYY-MM-DD')
    p.add_argument('-w','--woche',action='store_true',help='Woche')
    p.add_argument('-o','--optimal',action='store_true',help='Optimal')
    p.add_argument('-k','--kompakt',action='store_true',help='Kompakt')
    p.add_argument('--tage',type=int,default=30,help='Tage für -o')
    a=p.parse_args()
    
    if a.woche:week()
    elif a.optimal:optimal(a.tage)
    else:
        d=datetime.strptime(a.datum,'%Y-%m-%d') if a.datum else None
        show(sacra(d),a.kompakt)
