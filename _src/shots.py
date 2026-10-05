"""python shots.py 1440|390 -> zrzuty wszystkich podstron (full page)"""
import sys, os
from playwright.sync_api import sync_playwright
w=int(sys.argv[1]);h=900 if w>800 else 844
OUT=os.path.join(os.path.dirname(os.path.abspath(__file__)),'sh')
P=['','naprawy/','zgloszenie/?czesc=bateria','odbior/','kontakt/']
with sync_playwright() as p:
    b=p.chromium.launch(executable_path=r"C:\Program Files\Google\Chrome\Application\chrome.exe")
    ctx=b.new_context(viewport={'width':w,'height':h},is_mobile=w<800,has_touch=w<800,timezone_id='Europe/Warsaw')
    pg=ctx.new_page();errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e)));pg.on('console',lambda m:errs.append(m.text) if m.type=='error' else None)
    for path in P:
        pg.goto('http://127.0.0.1:8124/serwis-hulajnog-kutno/'+path+('&' if '?' in path else '?')+'team=1',wait_until='networkidle')
        pg.wait_for_timeout(1800)
        n=(path.split('?')[0].strip('/') or 'home')
        if n=='home':
            if w>900: pg.click('.co[data-part=hamulce] text')
            else: pg.click('.parts-list button[data-part=hamulce]')
        if n=='odbior':
            pg.evaluate("document.querySelector('#mapa').scrollIntoView()");pg.wait_for_timeout(1500)
            pg.fill('#miasto','Żychlin');pg.wait_for_timeout(1500);pg.evaluate("scrollTo(0,0)")
        pg.wait_for_timeout(400)
        pg.screenshot(path=f'{OUT}/{w}_{n}.png',full_page=True)
    print('ERR',errs)
