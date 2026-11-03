#!/usr/bin/env python3
"""Checks web/content/<lang>.json against content/en.json: the same keys and list lengths, nothing empty, the fixed fields, and texts
that look untranslated (identical to the English and longer than a few words). usage: python3 check_content.py <lang> [<lang> …]"""
import json, os, sys, re
D = os.path.dirname(os.path.abspath(__file__))
FIX = {'cs': ('CZ', 'cs-CZ', 'Čeština'), 'sk': ('SK', 'sk-SK', 'Slovenčina'), 'de': ('DE', 'de-DE', 'Deutsch'), 'es': ('ES', 'es-ES', 'Español'),
       'da': ('DK', 'da-DK', 'Dansk'), 'sv': ('SE', 'sv-SE', 'Svenska'), 'fr': ('FR', 'fr-FR', 'Français'), 'it': ('IT', 'it-IT', 'Italiano'),
       'nl': ('NL', 'nl-NL', 'Nederlands'), 'pt': ('PT', 'pt-PT', 'Português'), 'pl': ('PL', 'pl-PL', 'Polski'), 'ro': ('RO', 'ro-RO', 'Română'),
       'hu': ('HU', 'hu-HU', 'Magyar'), 'nb': ('NO', 'nb-NO', 'Norsk')}
KEEP = re.compile(r'^(SELYVO( Market| Core)?|MailChat|[A-Z]{2,4}-[\d-]+|.*@.*)$')
def walk(e, o, p, out):
    if isinstance(e, dict):
        if not isinstance(o, dict): out.append('TYPE ' + p); return
        for k in e:
            if k not in o: out.append('MISSING ' + p + '.' + k)
            else: walk(e[k], o[k], p + '.' + k, out)
        for k in o:
            if k not in e: out.append('EXTRA ' + p + '.' + k)
    elif isinstance(e, list):
        if not isinstance(o, list) or len(o) != len(e): out.append('LIST LENGTH %s (%s vs %s)' % (p, len(e), len(o) if isinstance(o, list) else type(o).__name__)); return
        for i, (x, y) in enumerate(zip(e, o)): walk(x, y, '%s[%d]' % (p, i), out)
    elif isinstance(e, str):
        if not isinstance(o, str): out.append('TYPE ' + p)
        elif e and not o.strip(): out.append('EMPTY ' + p)
        elif o == e and len(e.split()) > 3 and not KEEP.match(e) and p not in ('.lang', '.cc', '.hreflang', '.name'): out.append('SAME AS EN ' + p)
en = json.load(open(os.path.join(D, 'content', 'en.json'), encoding='utf-8'))
for l in sys.argv[1:]:
    f = os.path.join(D, 'content', l + '.json')
    try: o = json.load(open(f, encoding='utf-8'))
    except Exception as e: print(l, 'BAD', e); continue
    out = []
    walk(en, o, '', out)
    cc, hl, nm = FIX[l]
    for k, v in (('lang', l), ('cc', cc), ('hreflang', hl), ('name', nm)):
        if o.get(k) != v: out.append('FIELD %s should be %r' % (k, v))
    t = [(k, len(v['title']), len(v['description'])) for k, v in o['pages'].items()]
    long = [k for k, a, b in t if a > 75 or b > 175]
    if long: out.append('LONG title/description: ' + ', '.join('%s (%d/%d)' % x for x in t if x[0] in long))
    print(l, 'OK' if not out else '\n  '.join([str(len(out)) + ' issue(s):'] + out[:40]))
