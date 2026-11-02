#!/usr/bin/env python3
"""Check translation structure and artifacts; not semantic equivalence proof."""
from pathlib import Path
import json
import re
from lxml import etree as ET
from check_package import check_metadata_and_binding

BASE=Path(__file__).resolve().parents[1]
LANGS=['en','zh-Hant','ja']
REQUIREMENTS=['MUST NOT','MUST','SHALL NOT','SHALL','SHOULD NOT','SHOULD','MAY']
texts={l:(BASE/f'MISVG-0.1.{l}.md').read_text(encoding='utf-8') for l in LANGS}
results=[]
def check(name,condition):
    if not condition: raise AssertionError(name)
    results.append({'case':name,'result':'pass'})
def clauses(s):
    pieces=re.split(r'(?m)^###? (\d+(?:\.\d+)?)\.? ',s)
    return {pieces[i]:pieces[i+1] for i in range(1,len(pieces),2)}
def tokens(s):
    s=s.split('## 1.')[1]
    s=re.split(r'(?m)^## (?:Annex A|附錄 A|附属書 A)',s)[0]
    return set(re.findall(r'(?<!`)`([^`\n]+)`(?!`)',s))
ref=clauses(texts['en'])
for lang,s in texts.items():
    c=clauses(s)
    check(lang+'-numbered-clause-parity',list(c)==list(ref))
    check(lang+'-six-annexes',len(re.findall(r'(?m)^## (?:Annex|附錄|附属書) [A-F]',s))==6)
    check(lang+'-all-30-test-ids',re.findall(r'(?m)^\| (T\d\d) \|',s)==[f'T{i:02}' for i in range(1,31)])
    check(lang+'-technical-token-parity',tokens(s)==tokens(texts['en']))
    # Requirement levels match by clause; this does not prove translations equivalent.
    for key,body in c.items():
        for word in REQUIREMENTS:
            pattern=r'\b'+word+r'\b'
            check(lang+'-requirements-'+key+'-'+word,len(re.findall(pattern,body))==len(re.findall(pattern,ref[key])))
    check(lang+'-normative-reference-links',set(re.findall(r'https://[^)\s]+',s))==set(re.findall(r'https://[^)\s]+',texts['en'])))
    html=ET.HTML((BASE/f'MISVG-0.1.{lang}.html').read_bytes())
    check(lang+'-html-lang',html.get('lang')==lang)
    links=html.xpath('//nav/a/@href')
    check(lang+'-language-navigation',all(f'MISVG-0.1.{l}.html' in links for l in LANGS))
    check(lang+'-localized-example-link',f'examples/order-flow.{lang}.misvg.svg' in links)
    for href in html.xpath('//a/@href'):
        if not re.match(r'^(?:https?:|#)',href):
            check(lang+'-local-link-'+href,(BASE/href).exists())
    sample=BASE/f'examples/order-flow.{lang}.misvg.svg'
    check(lang+'-example-exact-extraction',check_metadata_and_binding(sample.read_bytes())==(BASE/f'examples/order-flow.{lang}.md').read_text(encoding='utf-8'))
check('default-html-is-english',(BASE/'index.html').read_bytes()==(BASE/'MISVG-0.1.en.html').read_bytes())
check('default-markdown-is-english',(BASE/'MISVG-0.1.md').read_bytes()==(BASE/'MISVG-0.1.en.md').read_bytes())
check('default-readme-links-english','Default and authoritative language: English' in (BASE/'README.md').read_text())
report={'specification':'MISVG-SPEC-0001 0.1.1 / Draft 02','default_language':'en','authoritative_language':'en','languages':LANGS,'scope':'Structural/token/requirement-level alignment and artifact checks; not a proof of translation equivalence or full MISVG conformance','passed':len(results),'failed':0,'cases':results}
(BASE/'tests/localization-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
# Validate the explicit publication defaults and edition paths as well.
manifest=json.loads((BASE/'languages.json').read_text(encoding='utf-8'))
check('manifest-default-fallback-authority',all(manifest[k]=='en' for k in ['defaultLanguage','fallbackLanguage','authoritativeLanguage']))
check('manifest-editions',set(manifest['editions'])==set(LANGS))
for lang,edition in manifest['editions'].items():
    for field in ['markdown','html','readme','example']:
        check('manifest-'+lang+'-'+field,(BASE/edition[field]).is_file())
report['passed']=len(results)
(BASE/'tests/localization-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:report[k] for k in ['passed','failed','default_language','languages']}))
