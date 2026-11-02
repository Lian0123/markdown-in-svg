#!/usr/bin/env python3
"""Build localized HTML and examples. Requires markdown and lxml. No network."""
from pathlib import Path
from hashlib import sha256
import re
import markdown
from lxml import etree as ET

BASE=Path(__file__).resolve().parents[1]
# Retain the previously verified stylesheet, shared across language editions.
existing=(BASE/'MISVG-0.1.zh-Hant.html').read_text(encoding='utf-8')
CSS=re.search(r'<style>(.*?)</style>',existing,re.S).group(1)
CSS=CSS.replace('"PingFang TC","Noto Sans CJK TC",sans-serif','"PingFang TC","Hiragino Sans","Noto Sans CJK TC",sans-serif')
LANGS={
'en': {'title':'Document Interchange Specification','notice':'Independent specification draft; not approved by IEEE or IETF.','example':'Open SVG example','source':'Markdown source'},
'zh-Hant': {'title':'文件交換規範','notice':'獨立技術規範草案，未經 IEEE／IETF 核准。','example':'開啟 SVG 範例','source':'Markdown 原稿'},
'ja': {'title':'文書交換仕様','notice':'独立した仕様草案。IEEE／IETF による承認は受けていません。','example':'SVG の例','source':'Markdown 原文'},
}
for lang,cfg in LANGS.items():
    md=(BASE/f'MISVG-0.1.{lang}.md').read_text(encoding='utf-8')
    body=markdown.markdown(md,extensions=['tables','fenced_code','toc'],output_format='html5')
    nav=' · '.join(f'<a href="MISVG-0.1.{code}.html" lang="{code}" hreflang="{code}"'+(' aria-current="page"' if code==lang else '')+f'>{label}</a>' for code,label in [('en','English (default)'),('zh-Hant','繁體中文'),('ja','日本語')])
    html=f'''<!doctype html><html lang="{lang}"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>MISVG 0.1 — {cfg['title']}</title>
<style>{CSS}</style></head><body><main>
<nav aria-label="Language" class="notice">{nav}<br>MISVG-SPEC-0001 · Draft 02 · 2026-11-02<br>{cfg['notice']} <a href="examples/order-flow.{lang}.misvg.svg">{cfg['example']}</a> · <a href="MISVG-0.1.{lang}.md">{cfg['source']}</a></nav>
{body}</main></body></html>\n'''
    (BASE/f'MISVG-0.1.{lang}.html').write_text(html,encoding='utf-8')
    if lang=='en':
        (BASE/'index.html').write_text(html,encoding='utf-8')
        (BASE/'MISVG-0.1.md').write_text(md,encoding='utf-8')

S='http://www.w3.org/2000/svg'; M='https://example.org/ns/markdown-in-svg/0.1'
ns={'s':S,'m':M}
DATA={
'en': {'source':'# Order workflow\n\n1. The customer completes payment.\n2. The warehouse confirms successful payment, then arranges shipment.\n\nRule: Do not ship if payment has not succeeded.\n',
       'heading':'Order workflow','desc':'The customer completes payment. The warehouse confirms successful payment before arranging shipment. Do not ship if payment has not succeeded.',
       'payment':['Customer completes','payment.'],'shipping':['Warehouse confirms','successful payment, then','arranges shipment.'],
       'rule':'Rule: Do not ship if payment has not succeeded.','uuid':'urn:uuid:7eab91ae-9b9f-444b-a10f-88f57787c613'},
'ja': {'source':'# 注文フロー\n\n1. 顧客が支払いを完了する。\n2. 倉庫が支払い成功を確認してから出荷を手配する。\n\n規則：支払いが成功していない場合は出荷しない。\n',
       'heading':'注文フロー','desc':'顧客が支払いを完了し、倉庫が支払い成功を確認してから出荷を手配する。支払いが成功していない場合は出荷しない。',
       'payment':['顧客が支払いを','完了する。'],'shipping':['倉庫が支払い成功を確認','してから出荷を手配する。'],
       'rule':'規則：支払いが成功していない場合は出荷しない。','uuid':'urn:uuid:583a71bd-f207-4479-99b3-f2ca6c29d831'}
}
raw=(BASE/'examples/order-flow.misvg.svg').read_bytes()
(BASE/'examples/order-flow.zh-Hant.misvg.svg').write_bytes(raw)
(BASE/'examples/order-flow.zh-Hant.md').write_bytes((BASE/'examples/order-flow.md').read_bytes())
for lang,cfg in DATA.items():
    root=ET.fromstring(raw,ET.XMLParser(strip_cdata=False))
    root.find('s:title',ns).text=cfg['heading']; root.find('s:desc',ns).text=cfg['desc']
    root.find('.//m:source',ns).text=ET.CDATA(cfg['source'])
    root.find('.//m:presentation',ns).set('source-digest','sha256:'+sha256(cfg['source'].encode()).hexdigest())
    root.find('.//m:document',ns).set('doc-id',cfg['uuid'])
    root.find('.//s:g',ns).set('font-family','Hiragino Sans, PingFang TC, Noto Sans CJK JP, sans-serif')
    root.xpath('//*[@id="heading"]')[0].text=cfg['heading']
    for ident,x,ys in [('payment',66,[266,302]),('shipping',536,[265,292,319] if lang=='en' else [270,309])]:
        node=root.xpath(f'//*[@id="{ident}"]/s:text',namespaces=ns)[-1]
        node.clear();node.set('x',str(x));node.set('y',str(ys[0]));node.set('font-size','21' if lang=='en' else '23');node.set('font-weight','bold')
        for text,y in zip(cfg[ident],ys):
            ET.SubElement(node,f'{{{S}}}tspan',x=str(x),y=str(y)).text=text
    rule=root.xpath('//*[@id="rule"]/s:text',namespaces=ns)[0]
    rule.text=cfg['rule'];rule.set('font-size','22' if lang=='en' else '21')
    (BASE/f'examples/order-flow.{lang}.misvg.svg').write_bytes(ET.tostring(root,xml_declaration=True,encoding='UTF-8',pretty_print=True))
    (BASE/f'examples/order-flow.{lang}.md').write_text(cfg['source'],encoding='utf-8')
print('Built 3 complete language editions, English entry points, and 3 localized examples.')
