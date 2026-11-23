from pathlib import Path
import argparse,json
from playwright.sync_api import sync_playwright,TimeoutError
ROOT=Path(__file__).resolve().parents[1];p=argparse.ArgumentParser();p.add_argument('--url',default='http://127.0.0.1:8186/');p.add_argument('--report',default='navigation.json');a=p.parse_args();result={}
with sync_playwright() as tool:
 b=tool.chromium.launch(executable_path='/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge',headless=True,ignore_default_args=['--disable-back-forward-cache']);page=b.new_page()
 page.goto(a.url+'python/?lang=en',wait_until='networkidle');page.wait_for_function('!document.querySelector("#run").disabled',timeout=60000);page.locator('#code').fill('print("before-navigation")');page.locator('#run').click();page.wait_for_function('document.querySelector("#output").textContent.includes("before-navigation")');page.wait_for_function('!document.querySelector("#run").disabled')
 page.evaluate('window.__courseProbe=1;window.addEventListener("pageshow",e=>window.__persisted=e.persisted)');page.locator('#back').click();page.wait_for_url(a.url+'?lang=en');page.evaluate('history.back()');page.wait_for_function('location.pathname.endsWith("/python/")&&window.__courseProbe===1',timeout=15000);result['used_real_bfcache']=page.evaluate('window.__courseProbe===1&&window.__persisted===true');page.wait_for_function('!document.querySelector("#run").disabled',timeout=60000);result['editor_retained']=page.locator('#code').input_value()=='print("before-navigation")';page.locator('#code').fill('print("after-navigation")');page.locator('#run').click()
 try:page.wait_for_function('document.querySelector("#output").textContent.includes("after-navigation")',timeout=3000);result['next_execution_works']=True
 except TimeoutError:result['next_execution_works']=False
 b.close()
result['status']='passed' if all(result.values()) else 'failed';(ROOT/'docs/qa'/a.report).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2));assert result['status']=='passed'
