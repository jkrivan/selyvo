#!/usr/bin/env python3
"""selyvo.com (3 Nov 2026 — Jiri, 11:17: "Perfect, produce the website"; 13:28: "Perfect, prepare the final website" — all light): every section light, white and light SELYVO teal in turn, the footer dark,
the four functions first, the market's processes played as you scroll, the films on the pages they belong to — in 15 languages.

  python3 build_site_e.py zip        → site-zip/  every page a full HTML document; the videos expected in videos/ (for the developers)
  python3 build_site_e.py artifact   → site-art/  the same pages for the mockup: the English home page without its skeleton, the
                                                  videos from the mockup's asset store (videos-art.json)

It runs the site's generator (build_site.py: languages, URLs, hreflang, sitemap, JSON-LD, the words of every earlier round) and then
the mixed design's templates (mixed/tpl_d.py, then mixed/tpl_e.py) with its styles and script (mixed/site.css, mixed/site.js).
The words: every earlier round's (content/, content-a/, content-b/), the mixed design's English (mixed/words/*.en.json) and its
translations (content-e/<lang>.json — the words new or changed in this design; content-e/need-paths.json lists them all, so that a
language never shows an older translation of a sentence the English has changed). Where a translation is missing, English is shown
and the build says so."""
import os, sys, json, shutil, glob, re, copy
W = os.path.dirname(os.path.abspath(__file__)); M = os.path.join(W, 'mixed')
mode = sys.argv[1] if len(sys.argv) > 1 else 'zip'
src = open(os.path.join(W, 'build_site.py'), encoding='utf-8').read()
SCHEME = os.environ.get('SCHEME', 'light')                 # the site is light since 3 Nov 13:28 (Jiri: "Perfect, prepare the final website"); SCHEME=mixed gives the mostly-white one with a few dark sections
if os.environ.get('OUT_DIR'):
    src = src.replace("OUT = os.path.join(D, 'site-zip' if MODE == 'zip' else 'site-art')", "OUT = %r" % os.environ['OUT_DIR'], 1)
sys.argv = ['build_site.py', mode]
ns = {'__name__': 'mixed', '__file__': os.path.join(W, 'build_site.py')}
exec(compile(src, os.path.join(W, 'build_site.py'), 'exec'), ns)
C = ns['CONTENT']; WARN = ns['WARN']
if os.environ.get('VIDEO_MAP'):                           # another mockup's own copies of the films (its asset store)
    ns['ART_VIDEOS'].clear(); ns['ART_VIDEOS'].update(json.load(open(os.environ['VIDEO_MAP'])))

# ---- the words
EN = C['en']
for f in ('content-c.en.json', 'content-d.en.json', 'content-films.en.json'):
    EN = ns['addkeys'](EN, json.load(open(os.path.join(M, 'words', f), encoding='utf-8')))
NEED = json.load(open(os.path.join(W, 'content-e', 'need-paths.json'), encoding='utf-8'))
def get(o, path):
    for k in path.split('.'): o = o[k]
    return o
def put(o, path, v):
    ks = path.split('.')
    for k in ks[:-1]: o = o.setdefault(k, {})
    o[ks[-1]] = v
def overlay(a, b, p=''):
    """b's words over a, all the way down (lists of the same length item by item; what b leaves out — screens, addresses — stays a's)."""
    if isinstance(a, dict) and isinstance(b, dict): return {k: overlay(a[k], b[k], p + '.' + k) if k in b else a[k] for k in a}
    if isinstance(a, list) and isinstance(b, list):
        if len(a) != len(b): WARN.append('content-e: list length differs at %s' % p); return a
        return [overlay(x, y, '%s[%d]' % (p, i)) for i, (x, y) in enumerate(zip(a, b))]
    if isinstance(a, str) and isinstance(b, str): return b
    if isinstance(a, (int, float)) and isinstance(b, (int, float)): return a        # numbers are the English ones
    return a
MISSING_E = []
for l in ns['BUILT']:
    if l == 'en': continue
    base = ns['deep'](EN, C[l])                          # every earlier round's translations, on the whole of the English
    for p in NEED:                                        # new or changed in this design: from the English first …
        try: put(base, p, copy.deepcopy(get(EN, p)))
        except (KeyError, TypeError): pass
    f = os.path.join(W, 'content-e', l + '.json')        # … then its translation
    if os.path.exists(f): base = overlay(base, json.load(open(f, encoding='utf-8')))
    else: MISSING_E.append(l)
    if l in ns['ONE_LETTER']: base = ns['nbsp_after_one_letter'](base, ns['ONE_LETTER'][l])
    C[l] = base
C['en'] = EN; ns['EN'] = EN
if mode == 'zip':                                         # every word each language's pages show, in one file (for the developers)
    os.makedirs(os.path.join(W, 'words'), exist_ok=True)
    for l in ns['BUILT']: json.dump(C[l], open(os.path.join(W, 'words', l + '.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
ns['CD'] = ns['DD'] = ns['ED'] = M; ns['TONE_SCHEME'] = SCHEME

# ---- the templates
exec(compile(open(os.path.join(M, 'tpl_d.py'), encoding='utf-8').read(), os.path.join(M, 'tpl_d.py'), 'exec'), ns)
exec(compile(open(os.path.join(M, 'tpl_e.py'), encoding='utf-8').read(), os.path.join(M, 'tpl_e.py'), 'exec'), ns)
ns['build']()

# ---- the design's styles, script, screens, the films' posters and stills
OUT = ns['OUT']; A = os.path.join(OUT, 'assets')
shutil.copy(os.path.join(M, 'site.css'), os.path.join(A, 'site.css')); shutil.copy(os.path.join(M, 'site.js'), os.path.join(A, 'site.js'))
if SCHEME == 'light':
    open(os.path.join(A, 'site.css'), 'a', encoding='utf-8').write(open(os.path.join(M, 'site-light.css'), encoding='utf-8').read())
if mode == 'artifact' and os.environ.get('ART_TITLE'):    # another mockup's own name (e.g. ART_TITLE="SELYVO Website Light")
    ix = os.path.join(OUT, 'index.html'); h = open(ix, encoding='utf-8').read()
    open(ix, 'w', encoding='utf-8').write(h.replace('<title>SELYVO Website</title>', '<title>%s</title>' % os.environ['ART_TITLE'], 1))
m = os.path.join(A, 'shots', 'master'); os.makedirs(m, exist_ok=True)
for f in glob.glob(os.path.join(M, 'shots', '*.webp')): shutil.copy(f, m)
for sub in ('posters', 'thumbs'):
    o = os.path.join(OUT, 'videos', sub); os.makedirs(o, exist_ok=True)
    for f in glob.glob(os.path.join(W, 'videos', sub, '*.jpg')): shutil.copy(f, o)

# ---- only what the pages use: every file under assets/shots and videos that no page, style or share picture names goes
used = set()
REF = re.compile(r'(?:src|href|poster|content)="([^"#?]+)')
for dp, _, fs in os.walk(OUT):
    for f in fs:
        if not f.endswith('.html'): continue
        h = open(os.path.join(dp, f), encoding='utf-8').read()
        refs = REF.findall(h) + re.findall(r'&quot;p&quot;:&quot;([^&]+)&quot;', h)
        for r in refs:
            if r.startswith(ns['BASE']): used.add(os.path.normpath(os.path.join(OUT, r[len(ns['BASE']):])))
            elif not re.match(r'^(https?:|mailto:|/_blob/|data:)', r): used.add(os.path.normpath(os.path.join(dp, r)))
gone = 0
for top in (os.path.join(A, 'shots'), os.path.join(OUT, 'videos')):
    for dp, _, fs in os.walk(top):
        for f in fs:
            p = os.path.normpath(os.path.join(dp, f))
            if p not in used: os.remove(p); gone += 1
for dp, ds, fs in sorted(os.walk(A), reverse=True):
    if not os.listdir(dp): os.rmdir(dp)
print('mixed design built:', OUT, '·', len(ns['BUILT']), 'languages ·', gone, 'unused files left out')
if MISSING_E: print('  ! the mixed design\'s words (content-e) not yet in:', ' '.join(MISSING_E), '— English shown there')
for w in sorted(set(WARN)): print('  !', w)
