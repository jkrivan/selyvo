#!/usr/bin/env python3
"""Checks web/content-e/<lang>.json (the words of the mixed site, 3 Nov 2026) against content-e/en.json: the same keys and list
lengths, the same numbers, nothing empty, texts that look untranslated, the fixed names kept, no 'provider', and the short labels short.
usage: python3 check_e.py <lang> [<lang> …]"""
import json, os, sys, re
D = os.path.dirname(os.path.abspath(__file__))
KEEP = re.compile(r'^(SELYVO( Market| Core)?|MailChat|Revolut Business|Stripe|[A-Z]{2,4}-[\d-]+|.*@.*)$')
MUST = ['SELYVO', 'invoice@market.selyvo.com', 'ISDOC', 'Revolut Business', 'Revolut', 'Stripe', 'MailChat', 'API', 'VIES', 'ARES']
SHORT = re.compile(r'^\.common\.(c\.nav|c\.fn|d\.local|d\.learn|d\.how|d\.watch|d\.stepWord|e\.(eyebrow|nowPlaying|guideWord|tourWord|fromWord|watch|localVideo))|^\.common\.c\.steps\.\w+\[\d+\]\[0\]|^\.pages\.index\.c\.processShort|^\.common\.e\.guides\.\w+\.chapters')
LIMIT = {'.common.c.nav': 18, '.common.d.local': 16, '.common.e.guides': 30, '.pages.index.c.processShort': 13, '.common.c.steps': 14}
def walk(e, o, p, out, warn):
    if isinstance(e, dict):
        if not isinstance(o, dict): out.append('TYPE ' + p); return
        for k in e:
            if k not in o: out.append('MISSING ' + p + '.' + k)
            else: walk(e[k], o[k], p + '.' + k, out, warn)
        for k in o:
            if k not in e: out.append('EXTRA ' + p + '.' + k)
    elif isinstance(e, list):
        if not isinstance(o, list) or len(o) != len(e): out.append('LIST LENGTH %s' % p); return
        for i, (x, y) in enumerate(zip(e, o)): walk(x, y, '%s[%d]' % (p, i), out, warn)
    elif isinstance(e, (int, float)):
        if o != e: out.append('NUMBER CHANGED %s: %r → %r' % (p, e, o))
    elif isinstance(e, str):
        if not isinstance(o, str): out.append('TYPE ' + p); return
        if e and not o.strip(): out.append('EMPTY ' + p)
        elif o == e and len(e.split()) > 2 and not KEEP.match(e): out.append('SAME AS EN ' + p)
        for m in MUST:
            if re.search(r'\b%s\b' % re.escape(m), e) and m not in o: out.append('LOST %r in %s' % (m, p))
        if re.search(r'[Pp]rovider|[Pp]oskytovate[lľ]|Anbieter|Dienstleister|proveedor de servicios|[Pp]restador|fournisseur de services|[Pp]restataire|[Pp]restatore|fornitore di servizi|tjänsteleverantör|szolgáltató|dostawca usług|[Aa]anbieder|[Uu]dbyder|[Ll]everandør av tjenester', o): out.append('PROVIDER? ' + p + ': ' + o[:80])
        if '  ' in o or o != o.strip(): out.append('SPACES ' + p)
        if SHORT.search(p):
            lim = next((v for k, v in LIMIT.items() if p.startswith(k)), None)
            if lim and len(o) > lim: warn.append('LONG %s (%d > %d): %s' % (p, len(o), lim, o))
            elif len(o) > max(8, 1.6 * len(e)): warn.append('LONG %s (%d vs EN %d): %s' % (p, len(o), len(e), o))
en = json.load(open(os.path.join(D, 'content-e', 'en.json'), encoding='utf-8'))
for l in sys.argv[1:]:
    f = os.path.join(D, 'content-e', l + '.json')
    try: o = json.load(open(f, encoding='utf-8'))
    except Exception as ex: print(l, 'BAD', ex); continue
    out, warn = [], []; walk(en, o, '', out, warn)
    print(l, ('OK' if not out else '\n  '.join([str(len(out)) + ' issue(s):'] + out[:60])) + (('\n  note — long labels (shorten where you can):\n    ' + '\n    '.join(warn[:30])) if warn else ''))
