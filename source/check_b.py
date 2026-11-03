#!/usr/bin/env python3
"""Checks web/content-b/<lang>.json (the words added for the second round of direction A, 3 Nov: Simple · Compliant · Performing, the process, Good to know) against content-b/en.json: the same keys and list
lengths, nothing empty, texts that look untranslated, the fixed names kept, and no 'provider'.
usage: python3 check_a.py <lang> [<lang> …]"""
import json, os, sys, re
D = os.path.dirname(os.path.abspath(__file__))
KEEP = re.compile(r'^(SELYVO( Market| Core)?|MailChat|Revolut Business|Stripe|[A-Z]{2,4}-[\d-]+|.*@.*)$')
MUST = ['SELYVO', 'invoice@market.selyvo.com', 'ISDOC', 'Revolut Business', 'Stripe', 'MailChat', 'API']
def walk(e, o, p, out):
    if isinstance(e, dict):
        if not isinstance(o, dict): out.append('TYPE ' + p); return
        for k in e:
            if k not in o: out.append('MISSING ' + p + '.' + k)
            else: walk(e[k], o[k], p + '.' + k, out)
        for k in o:
            if k not in e: out.append('EXTRA ' + p + '.' + k)
    elif isinstance(e, list):
        if not isinstance(o, list) or len(o) != len(e): out.append('LIST LENGTH %s' % p); return
        for i, (x, y) in enumerate(zip(e, o)): walk(x, y, '%s[%d]' % (p, i), out)
    elif isinstance(e, str):
        if not isinstance(o, str): out.append('TYPE ' + p); return
        if e and not o.strip(): out.append('EMPTY ' + p)
        elif o == e and len(e.split()) > 2 and not KEEP.match(e): out.append('SAME AS EN ' + p)
        for m in MUST:
            if m in e and m not in o: out.append('LOST %r in %s' % (m, p))
        if re.search(r'[Pp]rovider|[Pp]oskytovate[lľ]|Anbieter|Dienstleister|proveedor de servicios|[Pp]restador|fournisseur de services|[Pp]restataire|[Pp]restatore|fornitore di servizi|tjänsteleverantör|szolgáltató|dostawca usług|[Aa]anbieder|[Uu]dbyder', o): out.append('PROVIDER? ' + p + ': ' + o[:80])
en = json.load(open(os.path.join(D, 'content-b', 'en.json'), encoding='utf-8'))
for l in sys.argv[1:]:
    f = os.path.join(D, 'content-b', l + '.json')
    try: o = json.load(open(f, encoding='utf-8'))
    except Exception as ex: print(l, 'BAD', ex); continue
    out = []; walk(en, o, '', out)
    print(l, 'OK' if not out else '\n  '.join([str(len(out)) + ' issue(s):'] + out[:40]))
