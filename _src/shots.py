"""python shots.py 1440 [klik] -> pełne zrzuty strony"""
import sys, os
from playwright.sync_api import sync_playwright
w=int(sys.argv[1]);h=900 if w>800 else 844
OUT=os.path.join(os.path.dirname(os.path.abspath(__file__)),'sh')
with sync_playwright() as p:
    b=p.chromium.launch(executable_path=r"C:\Program Files\Google\Chrome\Application\chrome.exe")
    ctx=b.new_context(viewport={'width':w,'height':h},device_scale_factor=1,is_mobile=w<800,has_touch=w<800,timezone_id='Europe/Warsaw')
    pg=ctx.new_page();errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e)));pg.on('console',lambda m:errs.append(m.text) if m.type=='error' else None)
    pg.goto('http://127.0.0.1:8124/serwis-hulajnog-kutno/?team=1',wait_until='networkidle')
    pg.wait_for_timeout(2500)
    pg.screenshot(path=f'{OUT}/{w}_hero.png')
    if w>900: pg.click('.co[data-part=bateria] text')
    else: pg.click('.parts-list button[data-part=bateria]')
    pg.wait_for_timeout(500);pg.screenshot(path=f'{OUT}/{w}_part.png')
    pg.fill('#miasto','Żychlin');pg.wait_for_timeout(300)
    pg.evaluate("document.querySelector('#odbior').scrollIntoView()");pg.wait_for_timeout(500)
    pg.screenshot(path=f'{OUT}/{w}_odbior.png')
    pg.check('input[value="Bateria szybko pada / nie ładuje"]',force=True)
    pg.check('input[value="Proszę o odbiór"]',force=True)
    pg.fill('[name=adres]','Krośniewice, ul. Polna 3');pg.fill('[name=tel]','600 100 200');pg.fill('[name=imie]','Adam')
    pg.click('#form button[type=submit]');pg.wait_for_timeout(600)
    pg.evaluate("document.querySelector('#zgloszenie').scrollIntoView()")
    pg.screenshot(path=f'{OUT}/{w}_full.png',full_page=True)
    print('ERR',errs)
