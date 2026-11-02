#!/usr/bin/env python3
"""Package checks, not a complete MISVG validator. Requires Python 3 + lxml.

Checks the provided metadata, source bindings and a basic element screen.
Does NOT validate the full static-profile attribute/value grammar, CommonMark
rendering, content fidelity, visual output, resource limits or editor transactions.
"""
from pathlib import Path
from hashlib import sha256
import copy
import json
import re
from lxml import etree as ET

BASE = Path(__file__).resolve().parents[1]
M = 'https://example.org/ns/markdown-in-svg/0.1'
S = 'http://www.w3.org/2000/svg'
X = 'http://www.w3.org/XML/1998/namespace'
NS = {'m': M, 's': S}
ID = re.compile(r'[A-Za-z][A-Za-z0-9._-]{0,63}')
schema = ET.XMLSchema(ET.parse(str(BASE / 'schema/misvg-metadata-0.1.xsd')))


def digest(s):
    return 'sha256:' + sha256(s.encode('utf-8')).hexdigest()


def lines(s):
    return 0 if not s else len(s.split('\n')) - int(s.endswith('\n'))


def require(condition, code):
    if not condition:
        raise ValueError(code)


def check_metadata_and_binding(data):
    """Partial check only; successful return is NOT full conformance."""
    parser = ET.XMLParser(resolve_entities=False, load_dtd=False,
                          no_network=True, remove_comments=False,
                          strip_cdata=False, huge_tree=False)
    try:
        data.decode('utf-8-sig')
        root = ET.fromstring(data, parser)
    except (UnicodeError, ET.XMLSyntaxError):
        raise ValueError('E_XML') from None
    require(not root.getroottree().docinfo.doctype, 'E_XML')
    require(not root.getroottree().xpath('//processing-instruction()'), 'E_XML')
    require(root.tag == f'{{{S}}}svg', 'E_STRUCTURE')
    children = [n for n in root if isinstance(n.tag, str)]
    require([n.tag for n in children] == [f'{{{S}}}{n}' for n in ['title','desc','metadata','g']], 'E_STRUCTURE')
    metadata = children[2]
    docs = [n for n in metadata if isinstance(n.tag, str)]
    require(len(docs) == 1 and docs[0].tag == f'{{{M}}}document', 'E_STRUCTURE')
    doc = docs[0]
    require(doc.get('version') == '0.1' and doc.get('profile') == 'static', 'E_UNSUPPORTED')
    sources = doc.findall(f'{{{M}}}source')
    require(len(sources) == 1, 'E_STRUCTURE')
    source = sources[0]
    require(source.get('dialect') == 'commonmark-0.31.2', 'E_UNSUPPORTED')
    require(len(source) == 0, 'E_SOURCE')
    require(source.get(f'{{{X}}}space') == 'preserve', 'E_SOURCE')
    require(set(source.attrib) == {'media-type','dialect',f'{{{X}}}space'}, 'E_STRUCTURE')
    require(schema.validate(doc), 'E_STRUCTURE')
    require(re.fullmatch(r'[1-9][0-9]*', doc.get('revision')) is not None, 'E_STRUCTURE')
    text = source.text or ''
    require('\r' not in text, 'E_SOURCE')
    presentation = doc.find(f'{{{M}}}presentation')
    require(presentation.get('source-digest') == digest(text), 'E_DIGEST_MISMATCH')
    view = children[3]
    require(view.get('id') == presentation.get('root-ref'), 'E_REFERENCE')
    ids = {}
    allowed_elements = {'g','text','tspan','rect','circle','ellipse','line','polyline','polygon','path'}
    for n in view.iter():
        if not isinstance(n.tag, str):
            continue
        q = ET.QName(n)
        require(q.namespace == S and q.localname in allowed_elements, 'E_PROFILE')
        require(not any(ET.QName(a).localname.lower().startswith('on') or ET.QName(a).localname in {'href','style'} for a in n.attrib), 'E_PROFILE')
        if 'id' in n.attrib:
            ident = n.get('id')
            require(ID.fullmatch(ident) is not None and ident not in ids, 'E_REFERENCE')
            ids[ident] = n
    require(presentation.get('root-ref') in ids, 'E_REFERENCE')
    seen = set()
    for bind in doc.findall(f'{{{M}}}bindings/{{{M}}}bind'):
        target = bind.get('target')
        require(target in ids and target not in seen, 'E_REFERENCE')
        seen.add(target)
        require(all(re.fullmatch(r'[1-9][0-9]*', bind.get(k)) for k in ('start-line','end-line')), 'E_REFERENCE')
        require(1 <= int(bind.get('start-line')) <= int(bind.get('end-line')) <= lines(text), 'E_REFERENCE')
    return text


def main():
    raw = (BASE/'examples/order-flow.misvg.svg').read_bytes()
    root = ET.fromstring(raw)
    results = []

    def record(name, test):
        test()
        results.append({'case': name, 'result': 'pass'})

    def same(a, b):
        assert a == b, (a, b)

    def mutation(name, mutate, expected=None):
        tree = copy.deepcopy(root)
        mutate(tree)
        candidate = ET.tostring(tree, encoding='utf-8')
        if expected:
            try:
                check_metadata_and_binding(candidate)
            except ValueError as exc:
                same(str(exc), expected)
            else:
                raise AssertionError(f'{name}: expected {expected}')
        else:
            check_metadata_and_binding(candidate)
        results.append({'case': name, 'result': 'pass', 'expected_error': expected})

    src = lambda t: t.find('.//m:source', NS)
    pres = lambda t: t.find('.//m:presentation', NS)
    bind = lambda t: t.find('.//m:bind', NS)
    doc = lambda t: t.find('.//m:document', NS)
    def set_source(t, value):
        src(t).text = value
        pres(t).set('source-digest', digest(value))
        b = t.find('.//m:bindings', NS)
        if b is not None:
            b.getparent().remove(b)

    record('sample-extraction-exact', lambda: same(check_metadata_and_binding(raw), (BASE/'examples/order-flow.md').read_text(encoding='utf-8')))
    record('namespace-prefix-independent', lambda: same(check_metadata_and_binding(raw.replace(b'xmlns:m=', b'xmlns:doc=').replace(b'<m:', b'<doc:').replace(b'</m:', b'</doc:')), check_metadata_and_binding(raw)))
    record('xml-crlf-normalization', lambda: same(check_metadata_and_binding(raw.replace(b'\n', b'\r\n')), check_metadata_and_binding(raw)))
    record('file-bom-accepted', lambda: same(check_metadata_and_binding(b'\xef\xbb\xbf'+raw), check_metadata_and_binding(raw)))
    vectors = json.loads((BASE/'tests/hash-vectors.json').read_text(encoding='utf-8'))
    for v in vectors:
        def vector_test(v=v):
            same(v['source'].encode('utf-8').hex(), v['utf8_hex'])
            same(digest(v['source']), v['digest'])
            same(lines(v['source']), v['line_count'])
            tree = copy.deepcopy(root)
            set_source(tree, v['source'])
            escaped = ET.tostring(tree, encoding='utf-8')
            src(tree).text = ET.CDATA(v['source'])
            cdata = ET.tostring(tree, encoding='utf-8')
            same(check_metadata_and_binding(escaped), v['source'])
            same(check_metadata_and_binding(cdata), v['source'])
        record('vector-'+v['id'], vector_test)
    record('known-sha256-abc', lambda: same(digest('abc'), 'sha256:ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad'))
    record('known-sha256-empty', lambda: same(digest(''), 'sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'))
    mutation('stale-source-digest', lambda t: setattr(src(t), 'text', 'changed'), 'E_DIGEST_MISMATCH')
    mutation('decoded-cr-rejected', lambda t: set_source(t, 'a\rb'), 'E_SOURCE')
    mutation('duplicate-source', lambda t: doc(t).insert(1, copy.deepcopy(src(t))), 'E_STRUCTURE')
    mutation('unknown-core-attribute', lambda t: doc(t).set('typo', '1'), 'E_STRUCTURE')
    mutation('source-child-rejected', lambda t: src(t).append(ET.Element('bad')), 'E_SOURCE')
    mutation('source-comment-rejected', lambda t: src(t).append(ET.Comment('bad')), 'E_SOURCE')
    mutation('unknown-version', lambda t: doc(t).set('version','0.2'), 'E_UNSUPPORTED')
    mutation('unknown-profile', lambda t: doc(t).set('profile','html'), 'E_UNSUPPORTED')
    mutation('unknown-dialect', lambda t: src(t).set('dialect','gfm'), 'E_UNSUPPORTED')
    mutation('bad-root-ref', lambda t: pres(t).set('root-ref','missing'), 'E_REFERENCE')
    mutation('bad-target', lambda t: bind(t).set('target','missing'), 'E_REFERENCE')
    mutation('out-of-range-line', lambda t: bind(t).set('end-line','1000'), 'E_REFERENCE')
    mutation('duplicate-id', lambda t: t.find('.//s:text',NS).set('id','view'), 'E_REFERENCE')
    mutation('script-screen', lambda t: t.find('s:g',NS).append(ET.Element(f'{{{S}}}script')), 'E_PROFILE')
    mutation('event-screen', lambda t: t.find('s:g',NS).set('onclick','alert(1)'), 'E_PROFILE')
    mutation('foreignobject-screen', lambda t: t.find('s:g',NS).append(ET.Element(f'{{{S}}}foreignObject')), 'E_PROFILE')
    mutation('view-tamper-not-detectable-by-source-digest', lambda t: setattr(t.find('.//s:text',NS), 'text', 'altered view'))
    for name, candidate in [
        ('doctype-rejected', raw.replace(b'<svg ', b'<!DOCTYPE svg [<!ENTITY ext SYSTEM "file:///MISVG-NO-SUCH-FILE">]><svg ', 1)),
        ('pi-rejected', raw.replace(b'<svg ', b'<?misvg processing?><svg ', 1)),
    ]:
        def rejected(candidate=candidate):
            try:
                check_metadata_and_binding(candidate)
            except ValueError as exc:
                same(str(exc), 'E_XML')
            else:
                raise AssertionError('expected E_XML')
        record(name, rejected)

    report = {
        'specification': 'MISVG-SPEC-0001 Draft 02',
        'scope': 'Package consistency and partial metadata/source-binding tests; NOT complete conformance',
        'passed': len(results), 'failed': 0, 'cases': results,
        'sample_checks': {'metadata_xsd': 'pass', 'source_extraction': 'pass', 'source_digest': 'pass',
                          'ids_and_line_bindings': 'pass', 'basic_element_screen': 'pass'},
        'full_conformance_dimensions': {'structure': 'not-checked', 'source-binding': 'pass',
                                      'static-profile': 'not-checked', 'content-fidelity': 'not-checked',
                                      'visual-review': 'not-checked'},
        'not_covered': ['Full SVG attribute/value grammar', 'Complete CommonMark rendering',
                        'General resource limits', 'Unknown extension edit behavior',
                        'Editor atomicity and conflict tests', 'Independent cross-renderer interoperability'],
    }
    (BASE/'tests/verification-report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({'passed': len(results), 'failed': 0, 'scope': report['scope']}, ensure_ascii=False))


if __name__ == '__main__':
    main()
