#!/usr/bin/env python3
"""The new SELYVO website (selyvo.com), built from content/<lang>.json — 9 pages in each language whose content exists.

  python3 build_site.py zip        → site-zip/  every page a full HTML document; the videos from videos/ (for the developers)
  python3 build_site.py artifact   → site-art/  the same pages, the English home page without its skeleton (the Artifact tool adds
                                               it), the contact form ending on the thank-you page, the videos from videos-art.json

English stays at the root with the old site's URLs; every other language is in /<country code>/ (cz, sk, de, es, dk, se, fr, it, nl,
pt, pl, ro, hu, no) — the codes shown on the site are COUNTRY codes; hreflang and lang keep the language codes (cs-CZ, da-DK, nb-NO…).
Screenshots: the app's seven languages (en cs sk de es da sv) show the app in their language where shots-raw/<lang>/ has the picture,
the other languages show the English app. Videos: <name>-<CC>.mp4 from videos/, the English one where a language's is not made yet."""
import json, os, sys, re, html, shutil, subprocess, glob

D = os.path.dirname(os.path.abspath(__file__))
MODE = sys.argv[1] if len(sys.argv) > 1 else 'zip'
OUT = os.path.join(D, 'site-zip' if MODE == 'zip' else 'site-art')
BASE = 'https://selyvo.com/'
TODAY = '2026-11-03'
LANGS = [('en', 'GB', 'en-GB', 'English', 'en_GB'), ('cs', 'CZ', 'cs-CZ', 'Čeština', 'cs_CZ'), ('sk', 'SK', 'sk-SK', 'Slovenčina', 'sk_SK'),
         ('de', 'DE', 'de-DE', 'Deutsch', 'de_DE'), ('es', 'ES', 'es-ES', 'Español', 'es_ES'), ('da', 'DK', 'da-DK', 'Dansk', 'da_DK'),
         ('sv', 'SE', 'sv-SE', 'Svenska', 'sv_SE'), ('fr', 'FR', 'fr-FR', 'Français', 'fr_FR'), ('it', 'IT', 'it-IT', 'Italiano', 'it_IT'),
         ('nl', 'NL', 'nl-NL', 'Nederlands', 'nl_NL'), ('pt', 'PT', 'pt-PT', 'Português', 'pt_PT'), ('pl', 'PL', 'pl-PL', 'Polski', 'pl_PL'),
         ('ro', 'RO', 'ro-RO', 'Română', 'ro_RO'), ('hu', 'HU', 'hu-HU', 'Magyar', 'hu_HU'), ('nb', 'NO', 'nb-NO', 'Norsk', 'nb_NO')]
LANG = {l[0]: l for l in LANGS}
APP_LANGS = ('en', 'cs', 'sk', 'de', 'es', 'da', 'sv')
PAGES = ['index', 'spend-control', 'revenue-acceleration', 'inventory-control', 'finance-administration', 'operational-scale',
         'compliance-by-design', 'operating-layer', 'thank-you']
AREA = {'buy': 'spend-control', 'sell': 'revenue-acceleration', 'orders': 'inventory-control', 'invoices': 'finance-administration',
        'projects': 'operational-scale', 'trust': 'compliance-by-design', 'core': 'operating-layer'}
PAGE_AREA = {v: k for k, v in AREA.items()}
NAV = ['buy', 'sell', 'orders', 'invoices', 'projects', 'trust', 'core']
SHOT = {'index': 'purchases', 'spend-control': 'compare', 'revenue-acceleration': 'sales', 'inventory-control': 'order',
        'finance-administration': 'invoice', 'operational-scale': 'projects', 'compliance-by-design': 'register', 'operating-layer': 'core-suppliers'}
CORE_SHOTS = ['core-suppliers', 'core-questionnaires', 'core-shop', 'core-process']
CORE_LABEL = {'core-suppliers': 'SELYVO Core › Suppliers', 'core-questionnaires': 'SELYVO Core › Questionnaires',
              'core-shop': 'SELYVO Core › Request & shop', 'core-process': 'SELYVO Core › Processes'}
VIDEOS = ['overview', 'joining', 'buying', 'freelancer']
VNAME = {'tour': 'SELYVO-market-tour', 'overview': 'SELYVO-overview', 'joining': 'SELYVO-joining-from-an-invitation', 'buying': 'SELYVO-buying-guide', 'freelancer': 'SELYVO-freelancer-guide'}
ICON_OF = {'buy': 'buy', 'sell': 'sell', 'orders': 'orders', 'invoices': 'invoices', 'projects': 'projects', 'trust': 'trust', 'core': 'core'}
WARN = []

# ------------------------------------------------------------------------------------------------ icons (24 × 24, stroked)
ICONS = {
  'buy': '<circle cx="9" cy="20" r="1.4"/><circle cx="18" cy="20" r="1.4"/><path d="M2.5 3.5h3l2.4 11.2a1.5 1.5 0 0 0 1.5 1.2h8.4a1.5 1.5 0 0 0 1.5-1.1L21 7.5H6.4"/>',
  'sell': '<path d="M3 12.2V4.5A1.5 1.5 0 0 1 4.5 3h7.7l8.8 8.8a1.5 1.5 0 0 1 0 2.1l-7.1 7.1a1.5 1.5 0 0 1-2.1 0z"/><circle cx="8" cy="8" r="1.6"/>',
  'orders': '<path d="M21 8.2 12 3 3 8.2v7.6L12 21l9-5.2z"/><path d="M3 8.2 12 13.4l9-5.2M12 13.4V21"/>',
  'invoices': '<path d="M6 2.8h12a1 1 0 0 1 1 1V21l-3-1.8-2.5 1.8L12 19.2 10.5 21 8 19.2 5 21V3.8a1 1 0 0 1 1-1z"/><path d="M9 8h6M9 12h6M9 16h3"/>',
  'projects': '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3.2 2"/>',
  'trust': '<path d="M12 3 4.5 6v5.5c0 4.4 3.1 8.2 7.5 9.5 4.4-1.3 7.5-5.1 7.5-9.5V6z"/><path d="m8.8 12 2.2 2.2 4.4-4.5"/>',
  'core': '<path d="m12 3 9 5-9 5-9-5z"/><path d="m3 13 9 5 9-5"/>',
  'register': '<path d="M4 21V5.5A1.5 1.5 0 0 1 5.5 4h7A1.5 1.5 0 0 1 14 5.5V21M14 10h4.5a1.5 1.5 0 0 1 1.5 1.5V21M2.5 21h19"/><path d="M7.5 8h3M7.5 12h3M7.5 16h3"/>',
  'check': '<circle cx="10.5" cy="10.5" r="6.5"/><path d="m20 20-4.8-4.8M8 10.6l1.8 1.8 3.3-3.4"/>',
  'qualify': '<path d="M9 3.5h6v3H9z"/><path d="M15 5h2.5A1.5 1.5 0 0 1 19 6.5v13a1.5 1.5 0 0 1-1.5 1.5h-11A1.5 1.5 0 0 1 5 19.5v-13A1.5 1.5 0 0 1 6.5 5H9"/><path d="m9 13.5 2 2 4-4.5"/>',
  'review': '<path d="m12 3.5 2.6 5.3 5.8.8-4.2 4.1 1 5.8L12 16.8l-5.2 2.7 1-5.8-4.2-4.1 5.8-.8z"/>',
  'file': '<path d="M14 3H6.5A1.5 1.5 0 0 0 5 4.5v15A1.5 1.5 0 0 0 6.5 21h11a1.5 1.5 0 0 0 1.5-1.5V8z"/><path d="M14 3v5h5M8.5 13h7M8.5 17h5"/>',
  'mail': '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3.5 6.5 8.5 6.5 8.5-6.5"/>',
  'negotiate': '<path d="M20.5 12a8.5 8.5 0 0 1-12.4 7.6L3.5 21l1.4-4.6A8.5 8.5 0 1 1 20.5 12z"/><path d="M8.5 11h7M8.5 14.5h4"/>',
  'model': '<rect x="6" y="6" width="12" height="12" rx="2"/><path d="M9.5 2.5V6M14.5 2.5V6M9.5 18v3.5M14.5 18v3.5M2.5 9.5H6M2.5 14.5H6M18 9.5h3.5M18 14.5h3.5"/><rect x="9.5" y="9.5" width="5" height="5" rx=".8"/>',
  'buyer': '<rect x="3" y="7" width="18" height="13" rx="2"/><path d="M9 7V5.5A1.5 1.5 0 0 1 10.5 4h3A1.5 1.5 0 0 1 15 5.5V7M3 12.5h18"/>',
  'supplier': '<path d="M2.5 6.5h11v10h-11zM13.5 10h4l3.5 3.5v3h-7.5"/><circle cx="6.5" cy="18" r="1.8"/><circle cx="17" cy="18" r="1.8"/>',
  'freelancer': '<circle cx="12" cy="8" r="4"/><path d="M4.5 20.5c.8-3.7 3.9-6 7.5-6s6.7 2.3 7.5 6"/>',
  'globe': '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.4 2.5 3.6 5.5 3.6 9s-1.2 6.5-3.6 9c-2.4-2.5-3.6-5.5-3.6-9S9.6 5.5 12 3z"/>',
  'arrow': '<path d="M5 12h14M13 6l6 6-6 6"/>',
  'chev': '<path d="m6 9 6 6 6-6"/>',
  'right': '<path d="m9 6 6 6-6 6"/>',
  'plus': '<path d="M12 5v14M5 12h14"/>',
  'ok': '<circle cx="12" cy="12" r="9"/><path d="m8 12.3 2.7 2.7L16 9.7"/>',
  'info': '<circle cx="12" cy="12" r="9"/><path d="M12 11v5.5M12 7.6v.4"/>',
  'lock': '<rect x="5" y="10.5" width="14" height="10" rx="2"/><path d="M8 10.5V7.5a4 4 0 0 1 8 0v3"/>',
  'menu': '<path d="M4 7h16M4 12h16M4 17h16"/>',
  'sparkle': '<path d="M12 3.5 13.8 9a2 2 0 0 0 1.2 1.2l5.5 1.8-5.5 1.8a2 2 0 0 0-1.2 1.2L12 20.5 10.2 15A2 2 0 0 0 9 13.8L3.5 12 9 10.2A2 2 0 0 0 10.2 9z"/>',
  'signin': '<path d="M14 4h4.5A1.5 1.5 0 0 1 20 5.5v13a1.5 1.5 0 0 1-1.5 1.5H14M10 16.5 14.5 12 10 7.5M14.5 12H4"/>',
  'tick': '<path d="M5 12.5l4.5 4.5L19 7.5"/>',
  'x': '<path d="M6.5 6.5l11 11M17.5 6.5l-11 11"/>',
  'back': '<path d="M9 14 4 9l5-5"/><path d="M4 9h10.5a5.5 5.5 0 0 1 0 11H11"/>',
  'db': '<ellipse cx="12" cy="5.5" rx="7.5" ry="2.8"/><path d="M4.5 5.5v6.5c0 1.5 3.4 2.8 7.5 2.8s7.5-1.3 7.5-2.8V5.5M4.5 12v6.5c0 1.5 3.4 2.8 7.5 2.8s7.5-1.3 7.5-2.8V12"/>',
  'partners': '<path d="M3 21V9.5L9 6v15M9 21V3.5l12 4V21M3 21h18"/><path d="M12.5 10h1.5M12.5 13.5h1.5M12.5 17h1.5M16.5 10H18M16.5 13.5H18M16.5 17H18"/>',
  'key': '<circle cx="8" cy="15" r="4.5"/><path d="m11.3 11.7 8.2-8.2M17 6l2.5 2.5M14.5 8.5l2 2"/>',
  'log': '<path d="M8.5 6H20M8.5 12H20M8.5 18H20"/><circle cx="4.5" cy="6" r=".9"/><circle cx="4.5" cy="12" r=".9"/><circle cx="4.5" cy="18" r=".9"/>',
  'updown': '<path d="M8.5 20V4M8.5 4 5 7.5M8.5 4 12 7.5M15.5 4v16M15.5 20 12 16.5M15.5 20l3.5-3.5"/>',
  'bulb': '<path d="M9.5 18h5M10.5 21h3"/><path d="M12 3a6 6 0 0 0-3.7 10.7c.8.7 1.2 1.5 1.2 2.4v.4h5v-.4c0-.9.4-1.7 1.2-2.4A6 6 0 0 0 12 3z"/>',
  'trend': '<path d="m3 17 6-6 4 4 8-8"/><path d="M15 7h6v6"/>',
  'route': '<circle cx="6" cy="18" r="2.2"/><circle cx="18" cy="6" r="2.2"/><path d="M8.2 18H15a3 3 0 0 0 0-6H9a3 3 0 0 1 0-6h6.8"/>',
  'users': '<circle cx="9" cy="8" r="3.5"/><path d="M2.5 20c.6-3.3 3.3-5.5 6.5-5.5s5.9 2.2 6.5 5.5"/><path d="M16 4.6a3.5 3.5 0 0 1 0 6.8M18.5 14.8c1.6.8 2.7 2.4 3 5.2"/>',
}
def svg(name, cls=''):
    if name == 'play':
        return '<svg%s viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M8 5.5v13l10.5-6.5z"/></svg>' % (' class="%s"' % cls if cls else '')
    return ('<svg%s viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">%s</svg>'
            % (' class="%s"' % cls if cls else '', ICONS[name]))

# ------------------------------------------------------------------------------------------------ text helpers
def e(s): return html.escape(str(s), quote=True)
REF = re.compile(r'\b((?:REQ|ORD|FV|OFR|NF-PO)-[\d-]*\d|invoice@market\.selyvo\.com)')
def t(s):
    """A text for the page: escaped, references set in the mono face."""
    return REF.sub(lambda m: '<code>%s</code>' % m.group(1), e(s))
def eur(lang, v):
    s = '{:,.2f}'.format(v); ip, dp = s.split('.'); g = ip.split(',')
    if lang == 'en': return '€' + s
    ip2 = ('.' if lang in ('de', 'es', 'it', 'ro', 'da', 'nl') else ' ').join(g)
    return ('€ ' + ip2 + ',' + dp) if lang == 'nl' else (ip2 + ',' + dp + ' €')
def deep(a, b):
    """b over a: every key of a, b's value where b has one."""
    if isinstance(a, dict) and isinstance(b, dict): return {k: deep(a[k], b[k]) if k in b else a[k] for k in a}
    if isinstance(a, list) and isinstance(b, list) and len(a) == len(b): return [deep(x, y) for x, y in zip(a, b)]
    return b if type(b) == type(a) else a

def addkeys(a, b):
    """b's keys added into a (b wins), all the way down: the new design's words next to the old ones."""
    if not (isinstance(a, dict) and isinstance(b, dict)): return b
    out = dict(a)
    for k, v in b.items(): out[k] = addkeys(a[k], v) if k in a else v
    return out
def content_a(l):
    f = os.path.join(D, 'content-a', l + '.json')
    return json.load(open(f, encoding='utf-8')) if os.path.exists(f) else {}
def content_b(l):
    """Round 2 of direction A (3 Nov 2026): Simple · Compliant · Performing, the process by its screens, Good to know."""
    f = os.path.join(D, 'content-b', l + '.json')
    return json.load(open(f, encoding='utf-8')) if os.path.exists(f) else {}
EN = addkeys(addkeys(json.load(open(os.path.join(D, 'content', 'en.json'), encoding='utf-8')), content_a('en')), content_b('en'))
CONTENT = {'en': EN}
MISSING_A = []; MISSING_B = []
SKIP = set(x for x in os.environ.get('SKIP', '').split(',') if x)      # languages whose words are still being written
for l, *_ in LANGS[1:]:
    f = os.path.join(D, 'content', l + '.json')
    if os.path.exists(f) and l not in SKIP:
        if not content_a(l): MISSING_A.append(l)
        if not content_b(l): MISSING_B.append(l)
        CONTENT[l] = deep(EN, addkeys(addkeys(json.load(open(f, encoding='utf-8')), content_a(l)), content_b(l)))
# Czech, Slovak and Polish typography: a one-letter word (preposition or conjunction) never ends a line — a no-break space after it
ONE_LETTER = {'cs': 'aikosuvzAIKOSUVZ', 'sk': 'aikosuvzAIKOSUVZ', 'pl': 'aiouwzAIOUWZ'}
def nbsp_after_one_letter(o, letters):
    if isinstance(o, dict): return {k: nbsp_after_one_letter(v, letters) for k, v in o.items()}
    if isinstance(o, list): return [nbsp_after_one_letter(v, letters) for v in o]
    if isinstance(o, str): return re.sub(r'(?<![\w\u00a0-])([' + letters + r'])\s+(?=\S)', '\\1\u00a0', o)
    return o
for l, letters in ONE_LETTER.items():
    if l in CONTENT: CONTENT[l] = nbsp_after_one_letter(CONTENT[l], letters)
BUILT = [l for l, *_ in LANGS if l in CONTENT]

def folder(l): return '' if l == 'en' else LANG[l][1].lower() + '/'
def up(l): return '' if l == 'en' else '../'
def link(frm, to, page): return up(frm) + folder(to) + page + '.html'
def url(l, page): return BASE + folder(l) + ('' if page == 'index' else page + '.html')
def asset(l, p): return up(l) + 'assets/' + p

# ------------------------------------------------------------------------------------------------ media: screenshots, posters, videos
SHOTS_OUT = os.path.join(OUT, 'assets', 'shots')
def prepare_media():
    from PIL import Image
    made = 0
    for src in sorted(glob.glob(os.path.join(D, 'shots-raw', '*', '*.png'))):
        lang = os.path.basename(os.path.dirname(src)); name = os.path.basename(src)[:-4]
        dst = os.path.join(SHOTS_OUT, lang, name + '.webp')
        if not os.path.exists(dst) or os.path.getmtime(dst) < os.path.getmtime(src):
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            im = Image.open(src).convert('RGB')
            if im.width > 1800: im = im.resize((1800, round(im.height * 1800 / im.width)), Image.LANCZOS)
            im.save(dst, 'WEBP', quality=82, method=6); made += 1
            if lang in ('en', 'core'):          # the share picture (og:image), from the English app
                og = os.path.join(SHOTS_OUT, lang, name + '.jpg'); w = 1200
                im.resize((w, round(im.height * w / im.width)), Image.LANCZOS).save(og, 'JPEG', quality=82, optimize=True, progressive=True)
    return made
SHOT_SIZE = {}
def shot_file(l, name):
    """The picture for this language: its own (the app's languages), else the English one."""
    from PIL import Image
    for lang in ([l] if l in APP_LANGS else []) + ['en', 'core']:
        p = os.path.join(SHOTS_OUT, lang, name + '.webp')
        if os.path.exists(p):
            if p not in SHOT_SIZE: SHOT_SIZE[p] = Image.open(p).size
            return lang + '/' + name + '.webp', SHOT_SIZE[p]
    WARN.append('no screenshot %s for %s' % (name, l)); return 'en/' + name + '.webp', (1792, 864)
def shot_url(l, name):
    if name in CORE_LABEL: return CORE_LABEL[name]
    for lang in ([l] if l in APP_LANGS else []) + ['en']:
        f = os.path.join(D, 'shots-raw', lang, 'urls.json')
        if os.path.exists(f):
            u = json.load(open(f)).get(name)
            if u is not None: return 'market.selyvo.com/' + (u or '')
    return 'market.selyvo.com/'

VIDEO_DIR = os.path.join(D, 'videos')
ART_VIDEOS = json.load(open(os.path.join(D, 'videos-art.json'))) if os.path.exists(os.path.join(D, 'videos-art.json')) else {}
DUR = {}
def video_of(l, key):
    """(file name, seconds, poster path) — the language's own video, else the English one."""
    for cc in ([LANG[l][1]] if l != 'en' else []) + ['GB']:
        f = '%s-%s.mp4' % (VNAME[key], cc)
        p = os.path.join(VIDEO_DIR, f)
        if os.path.exists(p) and (MODE != 'artifact' or f in ART_VIDEOS):     # the artifact: only videos already in its asset store
            if cc != LANG[l][1] and key != 'tour': WARN.append('video %s: %s shows the English one' % (key, l))   # the tour: English on every page, on purpose
            if f not in DUR:
                DUR[f] = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', p], capture_output=True, text=True).stdout.strip() or 0)
                poster = os.path.join(VIDEO_DIR, 'posters', f[:-4] + '.jpg')
                if not os.path.exists(poster) or os.path.getmtime(poster) < os.path.getmtime(p):
                    os.makedirs(os.path.dirname(poster), exist_ok=True)
                    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-ss', '2.4', '-i', p, '-frames:v', '1', '-vf', 'scale=1280:-2', '-q:v', '4', poster], check=True)
            return f, DUR[f]
    WARN.append('video %s missing entirely' % key); return '%s-GB.mp4' % VNAME[key], 0
def mmss(s): s = int(round(s)); return '%d:%02d' % (s // 60, s % 60)
def iso_dur(s): s = int(round(s)); return 'PT%dM%dS' % (s // 60, s % 60)
def video_src(l, f):
    if MODE == 'artifact' and f in ART_VIDEOS: return ART_VIDEOS[f]
    if MODE == 'artifact': WARN.append('artifact: %s not in the asset store yet' % f)
    return up(l) + 'videos/' + f

# The page templates of direction A (2 Nov 2026) — spliced into build_site.py between "the parts of a page" and "def render".
# A strong promise on navy, the product as it is, the SELYVO palette; the same content files, and the words of content-a/<lang>.json.

def head(l, page, C, P, image):
    lang, cc, hl, name, loc = LANG[l]
    alts = ''.join('<link rel="alternate" hreflang="%s" href="%s">' % (LANG[x][2], url(x, page)) for x in BUILT)
    alts += '<link rel="alternate" hreflang="x-default" href="%s">' % url('en', page)
    ogalt = ''.join('<meta property="og:locale:alternate" content="%s">' % LANG[x][4] for x in BUILT if x != l)
    robots = '<meta name="robots" content="noindex, follow">' if page == 'thank-you' else ''
    canon = '' if page == 'thank-you' else '<link rel="canonical" href="%s">%s' % (url(l, page), alts)
    return ('<title>%s</title>\n<meta name="description" content="%s">\n%s%s\n'
            '<meta property="og:type" content="website"><meta property="og:site_name" content="SELYVO"><meta property="og:title" content="%s">'
            '<meta property="og:description" content="%s"><meta property="og:url" content="%s"><meta property="og:image" content="%s">'
            '<meta property="og:image:width" content="1200"><meta property="og:image:height" content="579"><meta property="og:locale" content="%s">%s'
            '<meta name="twitter:card" content="summary_large_image">\n'
            '<meta name="theme-color" content="#071C3C"><meta name="format-detection" content="telephone=no">\n'
            '<link rel="icon" href="%sfavicon.svg" type="image/svg+xml"><link rel="icon" href="%sfavicon.ico" sizes="any"><link rel="apple-touch-icon" href="%s">\n'
            '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
            '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@500;600&amp;family=Plus+Jakarta+Sans:wght@400;500;600;700;800&amp;display=swap">\n'
            '<link rel="stylesheet" href="%s">\n<script>document.documentElement.classList.add(\'js\')</script>\n'
            % (e(P['title']), e(P['description']), robots, canon, e(P['title']), e(P['description']), url(l, page), BASE + 'assets/shots/' + image,
               loc, ogalt, up(l), up(l), asset(l, 'apple-touch-icon.png'), asset(l, 'site.css')))

def lang_links(l, page, cls):
    return ''.join('<a href="%s" hreflang="%s" lang="%s"%s><span class="cc">%s</span>%s</a>'
                   % (link(l, x, page), LANG[x][2], LANG[x][2], ' aria-current="true"' if x == l else '', LANG[x][1], e(LANG[x][3])) for x in BUILT)

MARKET = ['buy', 'sell', 'orders', 'invoices', 'projects']
def home_link(l, page, anchor):
    return '#' + anchor if page == 'index' else link(l, l, 'index') + '#' + anchor
def featured(l):
    """The video a language's pages lead with: the new tour in English, each language's own overview elsewhere."""
    return 'tour' if l == 'en' else 'overview'

def announce(l, page, C):
    a = C['common']['a']; k = featured(l)
    title = a['tour']['title'] if k == 'tour' else C['common']['videos'][k]['title']
    new = '<span class="announce__new">%s</span>' % e(a['new']) if k == 'tour' else ''
    return ('<div class="announce"><div class="wrap">%s<span>%s: %s</span><a href="%s">%s%s</a></div></div>\n'
            % (new, e(a['videoGuide']), e(title), home_link(l, page, 'videos'), e(a['watchIt']), svg('arrow')))

def header(l, page, C):
    c = C['common']; n = c['nav']; a = c['a']; idx = C['pages']['index']['areas']
    dd = ''.join('<a href="%s"%s><span class="ico">%s</span><span><strong>%s</strong><small>%s</small></span></a>'
                 % (link(l, l, AREA[k]), ' aria-current="page"' if AREA[k] == page else '', svg(ICON_OF[k]), e(c['areas'][k]), t(idx[k])) for k in MARKET)
    cur = lambda p: ' aria-current="page"' if p == page else ''
    nav = ('<details class="dd"><summary>%s%s</summary><div class="dd__panel">%s</div></details>'
           '<a href="%s"%s>%s</a><a href="%s">%s</a><a href="%s"%s>%s</a>'
           % (e(a['product']), svg('chev'), dd, link(l, l, 'compliance-by-design'), cur('compliance-by-design'), e(n['trust']),
              home_link(l, page, 'videos'), e(c['b']['navTour']), link(l, l, 'operating-layer'), cur('operating-layer'), e(n['core'])))
    mnav = ('<a href="%s"%s>%s %s</a>' % (link(l, l, 'index'), cur('index'), e(n['home']), svg('right'))
            + ''.join('<a href="%s"%s>%s %s</a>' % (link(l, l, AREA[k]), cur(AREA[k]), e(c['areas'][k]), svg('right')) for k in NAV)
            + '<a href="%s">%s %s</a>' % (home_link(l, page, 'videos'), e(c['b']['navTour']), svg('right')))
    join = home_link(l, page, 'join') if page != 'index' else '#join'
    return (
      '<a class="skip" href="#main">%s</a>\n%s<header class="top"><div class="wrap top__in">'
      '<a class="brand" href="%s" aria-label="SELYVO Market — %s"><img src="%s" alt="SELYVO" width="203" height="24"><span class="brand__tag">MARKET</span></a>'
      '<nav class="nav" aria-label="%s">%s</nav>'
      '<div class="tools">'
      '<details class="lang"><summary aria-label="%s: %s">%s<span class="cc">%s</span>%s</summary><div class="lang__menu">%s</div></details>'
      '<a class="signin" href="https://market.selyvo.com/">%s</a>'
      '<a class="btn btn--primary btn--sm" href="%s">%s</a>'
      '<details class="menu"><summary>%s<span>%s</span></summary><div class="menu__panel"><nav aria-label="%s">%s</nav>'
      '<div class="menu__cta"><a class="btn btn--primary btn--lg" href="%s">%s %s</a><a class="btn btn--line btn--lg" href="https://market.selyvo.com/">%s %s</a></div>'
      '<div class="menu__langs" aria-label="%s">%s</div></div></details>'
      '</div></div></header>\n'
      % (e(c['skip']), announce(l, page, C), link(l, l, 'index'), e(n['home']), asset(l, 'selyvo-white.png'), e(n['menu']), nav,
         e(n['language']), e(LANG[l][3]), svg('globe'), LANG[l][1], svg('chev', 'chev'), lang_links(l, page, ''),
         e(n['signIn']), join, e(a['getInvited']),
         svg('menu'), e(n['menu']), e(n['menu']), mnav, join, e(a['getInvited']), svg('arrow'), svg('signin'), e(n['signIn']), e(n['language']), lang_links(l, page, '')))

def footer(l, page, C):
    c = C['common']; f = c['footer']; n = c['nav']
    market = ''.join('<li><a href="%s">%s</a></li>' % (link(l, l, AREA[k]), e(c['areas'][k])) for k in MARKET)
    comp = ('<li><a href="%s">%s</a></li><li><a href="%s">%s</a></li><li><a href="%s">%s</a></li><li><a href="%s">%s</a></li><li><a href="%s">%s</a></li>'
            '<li><a href="https://market.selyvo.com/">%s</a></li>'
            % (link(l, l, 'compliance-by-design'), e(c['areas']['trust']), link(l, l, 'operating-layer'), e(c['areas']['core']),
               home_link(l, page, 'videos'), e(c['b']['navTour']), home_link(l, page, 'join'), e(n['join']), home_link(l, page, 'contact'), e(f['contact']), e(n['signIn'])))
    return ('<footer class="foot"><div class="wrap"><div class="foot__grid">'
            '<div class="foot__brand"><img src="%s" alt="SELYVO" width="203" height="24" loading="lazy"><p>%s</p></div>'
            '<div><h4>%s</h4><ul>%s</ul></div><div><h4>%s</h4><ul>%s</ul></div>'
            '<div><h4>%s</h4><div class="foot__langs">%s</div></div></div>'
            '<div class="foot__bottom"><span>%s</span><span>%s</span></div></div></footer>\n'
            % (asset(l, 'selyvo-white.png'), e(f['about']), e(f['market']), market, e(f['company']), comp, e(f['languages']), lang_links(l, page, ''),
               e(f['rights']), e(c['a']['illustrative'])))

def shot(l, name, caption, eager=False, cls='', alt=None):
    src, (w, h) = shot_file(l, name)
    return ('<figure class="%s"><div class="frame"><div class="frame__bar"><i></i><i></i><i></i><span class="frame__url">%s</span></div>'
            '<img src="%s" alt="%s" width="%d" height="%d"%s></div>%s</figure>'
            % (cls, e(shot_url(l, name)), asset(l, 'shots/' + src), e(alt if alt is not None else caption), w, h,
               ' fetchpriority="high"' if eager else ' loading="lazy" decoding="async"', '<figcaption>%s</figcaption>' % t(caption) if caption else ''))

def points(items, coming_at=None, coming=''):
    return '<ul class="points">%s</ul>' % ''.join('<li>%s<span>%s%s</span></li>' % (svg('ok'), t(x), (' <span class="badge">%s</span>' % e(coming)) if i == coming_at else '')
                                                  for i, x in enumerate(items))

def faq(C, items, title=None, cls=''):
    c = C['common']
    lst = ''.join('<details><summary>%s%s</summary><p>%s</p></details>' % (e(q), svg('plus'), t(a)) for q, a in items)
    return ('<section class="sec%s" id="faq"><div class="wrap faq"><div class="sec__head"><h2 class="h2">%s</h2></div>'
            '<div class="faq__list">%s</div></div></section>\n' % (cls, e(title or c['faqTitle']), lst))

def check_card(C):
    k = C['common']['a']['check']['card']
    return ('<div class="check" aria-hidden="true"><div class="check__head"><b>%s</b><span class="check__tag">AI</span></div><ul>'
            '<li class="ok">%s<span>%s</span></li><li class="ok">%s<span>%s</span></li><li class="bad">%s<span>%s</span></li></ul>'
            '<div class="check__ret">%s<span>%s</span></div></div>'
            % (e(k['title']), svg('tick'), e(k['ok1']), svg('tick'), e(k['ok2']), svg('x'), t(k['bad']), svg('back'), e(k['returned'])))

def connect_diagram(l, C):
    k = C['common']['a']['connect']
    arrow = svg('updown')
    return ('<div class="connect"><div class="connect__node"><span class="ico">%s</span><b>%s</b></div>'
            '<div class="connect__link">%s<span>%s</span></div>'
            '<div class="connect__node connect__node--market"><img src="%s" alt="SELYVO" width="170" height="20" loading="lazy"><small>MARKET</small></div>'
            '<div class="connect__link">%s<span>%s</span></div>'
            '<div class="connect__node"><span class="ico">%s</span><b>%s</b></div>'
            '<div class="connect__foot"><span>%s%s</span><span>%s%s</span></div></div>'
            % (svg('db'), e(k['yours']), arrow, e(k['carries']), asset(l, 'selyvo-white.png'), arrow, e(k['invoices']), svg('partners'), e(k['partners']),
               svg('key'), e(k['api']), svg('log'), e(k['log'])))

def row(copy, media, flip=False, rid=''):
    return '<div class="row%s"%s><div class="row__copy">%s</div><div class="row__media">%s</div></div>' % (' row--flip' if flip else '', ' id="%s"' % rid if rid else '', copy, media)

def row_copy(x, more_href=None, more=None, coming=''):
    pts = points(x['points'], coming_at=x.get('_coming'), coming=coming)
    m = '<a class="more" href="%s">%s %s</a>' % (more_href, e(more), svg('arrow')) if more_href else ''
    return '<span class="eyebrow">%s</span><h2 class="h2">%s</h2><p class="lede">%s</p>%s%s' % (e(x['eyebrow']), e(x['title']), t(x['text']), pts, m)

def video_player(l, key, C, pid):
    v = C['common']['a']['tour'] if key == 'tour' else C['common']['videos'][key]
    f, secs = video_of(l, key)
    poster = up(l) + 'videos/posters/' + f[:-4] + '.jpg'
    return ('<div class="vplayer"><video id="%s" controls preload="none" playsinline poster="%s" aria-label="%s"><source src="%s" type="video/mp4"></video></div>'
            % (pid, poster, e(v['title']), video_src(l, f)), v, secs)

def videos_section(l, C, cls=' sec--canvas'):
    c = C['common']; vt = c['videos']; k0 = featured(l)
    player, v0, s0 = video_player(l, k0, C, 'vmain')
    others = (['overview'] if k0 == 'tour' else []) + ['joining', 'buying', 'freelancer']
    items = []
    for i, k in enumerate([k0] + others):
        v = c['a']['tour'] if k == 'tour' else vt[k]
        f, secs = video_of(l, k)
        items.append('<li><button type="button" data-player="vmain" data-src="%s" data-poster="%s" data-title="%s" data-text="%s" data-dur="%s" aria-pressed="%s">'
                     '<span class="play">%s</span><span><strong>%s</strong><small>%s</small></span><span class="dur">%s</span></button></li>'
                     % (e(video_src(l, f)), e(up(l) + 'videos/posters/' + f[:-4] + '.jpg'), e(v['title']), e(v['text']), mmss(secs),
                        'true' if i == 0 else 'false', svg('play'), e(v['title']), e(v['text']), mmss(secs)))
    note = ('<p class="vid-note">%s<span>%s</span></p>' % (svg('info'), e(vt['enScreens']))) if l not in APP_LANGS else ''
    body = ('<section class="sec%s" id="videos"><div class="wrap vids"><div><div class="vplay">%s</div>'
            '<div class="vnow"><h3 id="vmain-title">%s</h3><span class="dur" id="vmain-dur">%s</span></div><p class="text" id="vmain-text">%s</p></div>'
            '<div><div class="sec__head sec__head--left" style="margin-bottom:0"><span class="eyebrow">%s</span><h2 class="h2">%s</h2><p class="lede">%s</p></div>'
            '<ul class="vlist">%s</ul>%s</div></div></section>\n'
            % (cls, player, e(v0['title']), mmss(s0), t(v0['text']), e(vt['eyebrow']), e(vt['title']), t(vt['lede']), ''.join(items), note))
    return body, [k0] + others

def invite_contact(l, page, C, cls=' sec--canvas'):
    c = C['common']; k = c['contact']; iv = C['pages']['index']['a']['invite']
    topics = ''.join('<option>%s</option>' % e(x) for x in k['topics'])
    netlify = ' data-netlify="true" netlify-honeypot="bot-field"' if MODE == 'zip' else ''
    joining = (link(l, l, 'compliance-by-design') + '#video') if page != 'compliance-by-design' else '#video'
    return (
      '<section class="sec%s" id="join"><div class="wrap" style="display:flex;flex-direction:column;gap:clamp(56px,7vw,88px)">'
      '<div class="invite"><div><h2 class="h2">%s</h2><p>%s</p><div class="ctas"><a class="btn btn--primary btn--lg" href="%s">%s%s</a>'
      '<a class="btn btn--line btn--lg" href="#contact">%s</a></div></div>'
      '<div class="mail" aria-hidden="true"><div class="mail__from"><span class="mail__av">FS</span><span><b>Form Studio s.r.o.</b><small>%s</small></span></div>'
      '<p>%s</p><span class="mail__btn">%s</span><small class="mail__valid">%s</small></div></div>'
      '<div class="contact" id="contact"><div class="contact__copy"><span class="eyebrow">%s</span><h2 class="h2">%s</h2><p class="lede">%s</p></div>'
      '<form class="form" name="selyvo-contact" method="POST" action="thank-you.html" data-thanks="thank-you.html" accept-charset="UTF-8" novalidate%s>'
      '<input type="hidden" name="form-name" value="selyvo-contact"><input type="hidden" name="language" value="%s"><input type="hidden" name="page" value="%s">'
      '<p hidden><label>Bot <input name="bot-field" tabindex="-1" autocomplete="off"></label></p>'
      '<div class="form__row"><label>%s<input id="cf-first-name" name="first-name" autocomplete="given-name" required></label><label>%s<input id="cf-last-name" name="last-name" autocomplete="family-name" required></label></div>'
      '<div class="form__row"><label>%s<input id="cf-email" name="email" type="email" inputmode="email" autocomplete="email" spellcheck="false" required></label>'
      '<label>%s<input id="cf-company" name="company" autocomplete="organization"></label></div>'
      '<div class="form__row"><label>%s<input id="cf-country" name="country" autocomplete="country-name"></label><label>%s<select id="cf-topic" name="topic">%s</select></label></div>'
      '<label>%s<textarea id="cf-message" name="message" rows="5" required></textarea></label>'
      '<p class="form__err" role="alert" hidden>%s</p>'
      '<div class="form__foot"><button class="btn btn--teal" type="submit">%s %s</button><small>%s</small></div></form></div>'
      '</div></section>\n'
      % (cls, e(iv['title']), t(iv['text']), joining, svg('play'), e(iv['cta']), e(c['join']['write']),
         e(iv['mockWho']), t(iv['mockText']), e(iv['mockButton']), e(iv['mockValid']),
         e(k['eyebrow']), e(k['title']), t(k['lede']), netlify, LANG[l][2], page,
         e(k['firstName']), e(k['lastName']), e(k['email']), e(k['company']), e(k['country']), e(k['topic']), topics, e(k['message']),
         e(k['required']), e(k['send']), svg('arrow'), e(k['note'])))

def area_card(l, k, C, text=None, label=None):
    c = C['common']; idx = C['pages']['index']['areas']
    return ('<a class="card" href="%s"><span class="ico">%s</span><h3 class="h3">%s</h3><p class="text">%s</p><span class="more">%s %s</span></a>'
            % (link(l, l, AREA[k]), svg(ICON_OF[k]), e(c['areas'][k] if label is None else label[0]), t(text if text is not None else idx[k]),
               e(c['readMore'] if label is None else label[1]), svg('arrow')))

def jsonld(*items):
    g = [x for x in items if x]
    return '<script type="application/ld+json">%s</script>\n' % json.dumps({'@context': 'https://schema.org', '@graph': g}, ensure_ascii=False).replace('</', '<\\/')
def ld_faq(items): return {'@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in items]}
def ld_video(l, key, C):
    v = C['common']['a']['tour'] if key == 'tour' else C['common']['videos'][key]; f, secs = video_of(l, key)
    return {'@type': 'VideoObject', 'name': v['title'], 'description': v['text'], 'thumbnailUrl': BASE + 'videos/posters/' + f[:-4] + '.jpg',
            'contentUrl': BASE + 'videos/' + f, 'uploadDate': TODAY, 'duration': iso_dur(secs), 'inLanguage': LANG[l][2]}
def ld_crumbs(l, page, C):
    return {'@type': 'BreadcrumbList', 'itemListElement': [{'@type': 'ListItem', 'position': 1, 'name': C['common']['nav']['home'], 'item': url(l, 'index')},
            {'@type': 'ListItem', 'position': 2, 'name': C['common']['areas'][PAGE_AREA[page]], 'item': url(l, page)}]}

# ------------------------------------------------------------------------------------------------ the pages
def home_faq(P):
    items = [list(x) for x in P['faq']]
    for i, (q, a) in enumerate(P['faq']):
        if i == 3: items[i] = list(P['a']['faqAccounting'])
    return items

def page_index(l, C):
    P = C['pages']['index']; A = P['a']; c = C['common']; ca = c['a']
    ticks = ''.join('<li>%s%s</li>' % (svg('tick'), e(x)) for x in A['ticks'])
    floats = ('<div class="float float--l" aria-hidden="true"><div class="float__head"><span class="float__ok">%s</span><span class="float__title">%s</span>'
              '<span class="float__time">10:42</span></div><div class="float__who">Holzwerk Brandt GmbH · <code>REQ-2026-0164</code></div>'
              '<div class="float__row"><span class="float__amt">%s</span><span class="float__note">%s</span></div></div>'
              '<div class="float float--r" aria-hidden="true"><div class="float__head" style="justify-content:space-between"><span class="float__ref">INV-2026-0094</span>'
              '<span class="status status--ok">%s</span></div><div class="float__title" style="margin-top:8px">Nordvik A/S · %s</div>'
              '<div class="float__row"><span class="float__amt">%s</span><span class="float__who" style="margin:0">Revolut Business</span></div></div>'
              % (svg('tick'), e(A['offer']['title']), eur(l, 8469.60), e(A['offer']['note']), e(A['paid']['status']), e(A['paid']['country']), eur(l, 10360.00)))
    hero = ('<div class="band">%s<section class="hero"><div class="wrap"><p class="pill"><i></i>%s</p><h1>%s <span class="hl">%s</span></h1><p class="lede">%s</p>'
            '<div class="ctas"><a class="btn btn--primary btn--lg" href="#join">%s %s</a><a class="btn btn--line btn--lg" href="#videos">%s%s</a></div>'
            '<ul class="ticks">%s</ul><div class="hero__media">%s%s</div></div></section></div>\n'
            % ('{HEADER}', e(A['pill']), e(A['title1']), e(A['title2']), t(A['lede']), e(A['cta']), svg('arrow'), svg('play'), e(A['cta2']), ticks,
               shot(l, 'purchases', '', True, alt=A['shotAlt']), floats))
    facts = ''.join('<div class="fact"><b>%s</b><p>%s</p></div>' % (e(a.replace(' ', '\u00a0', 1)), t(b)) for a, b in A['facts'])   # the numeral stays with its noun
    pr = A['promise']
    cards = ''.join(area_card(l, k, C, text=pr['items'][i][1], label=(pr['items'][i][0], pr['items'][i][2])) for i, k in enumerate(['sell', 'buy', 'invoices']))
    R = A['rows']; buy = dict(R['buy']); buy['_coming'] = 2
    rows = (row(row_copy(R['sell'], link(l, l, 'revenue-acceleration'), c['readMore']), shot(l, 'sales', '', alt=R['sell']['title']))
            + row(row_copy(buy, link(l, l, 'spend-control'), c['readMore'], c['coming']), shot(l, 'compare', '', alt=R['buy']['title']), flip=True)
            + row(row_copy(R['invoices'], link(l, l, 'finance-administration'), c['readMore']), shot(l, 'invoice', '', alt=R['invoices']['title']) + check_card(C))
            + row(row_copy(ca['connect'], link(l, l, 'finance-administration') + '#connect', c['readMore']), connect_diagram(l, C), flip=True, rid='connect'))
    tr = A['trust']
    tsteps = ''.join('<div class="tstep"><div class="tstep__n"><span>%02d</span><span class="ico">%s</span></div><h3>%s</h3><p>%s</p></div>' % (i + 1, svg(ic), e(a), t(b))
                     for i, (ic, (a, b)) in enumerate(zip(['register', 'check', 'qualify', 'review'], P['trust'])))
    ai = P['ai']
    ai_items = ''.join('<div class="ai__item"><span class="ico">%s</span><div><h3>%s%s</h3><p>%s</p></div></div>'
                       % (svg(ic), e(a), (' <span class="badge">%s</span>' % e(c['coming'])) if flag == 'coming' else '', t(b))
                       for ic, (a, b, flag) in zip(['file', 'mail', 'negotiate', 'model'], ai['items']))
    demo = ('<div class="ai__demo"><div class="ai__card" aria-hidden="true"><span class="ai__btn">%s<span>%s</span></span>'
            '<div class="ai__found"><span class="ico">%s</span><span><b>%s</b><small>%s</small></span></div></div><p class="ai__cap">%s</p></div>'
            % (svg('sparkle'), e(A['ai']['button']), svg('users'), e(A['ai']['found']), e(A['ai']['foundText']), e(A['ai']['caption'])))
    vids, vkeys = videos_section(l, C)
    items = home_faq(P)
    body = (hero
      + '<main id="main">\n<section class="facts lift"><div class="wrap"><div class="facts__grid">%s</div></div></section>\n' % facts
      + ('<section class="sec sec--canvas" id="areas"><div class="wrap"><div class="sec__head"><span class="eyebrow">%s</span><h2 class="h2">%s</h2><p class="lede">%s</p></div>'
         '<div class="cards3">%s</div></div></section>\n' % (e(pr['eyebrow']), e(pr['title']), t(pr['lede']), cards))
      + '<section class="sec" id="features"><div class="wrap rows">%s</div></section>\n' % rows
      + ('<section class="sec sec--navy" id="trust"><div class="wrap"><div class="trust__top"><div class="sec__head sec__head--left" style="margin:0">'
         '<span class="eyebrow">%s</span><h2 class="h2">%s</h2></div><p class="lede">%s</p></div><div class="trust__grid">%s</div></div></section>\n'
         % (e(tr['eyebrow']), e(tr['title']), t(tr['lede']), tsteps))
      + ('<section class="sec" id="ai"><div class="wrap ai"><div><div class="sec__head sec__head--left" style="margin-bottom:8px"><span class="eyebrow">%s</span>'
         '<h2 class="h2">%s</h2><p class="lede">%s</p></div><div class="ai__list">%s</div></div>%s</div></section>\n'
         % (e(ai['eyebrow']), e(ai['title']), t(ai['lede']), ai_items, demo))
      + vids + faq(C, items) + invite_contact(l, 'index', C) + '</main>\n')
    ld = jsonld({'@type': 'Organization', '@id': BASE + '#org', 'name': 'SELYVO', 'url': BASE, 'logo': BASE + 'assets/selyvo-dark.png'},
                {'@type': 'WebSite', '@id': BASE + '#site', 'name': 'SELYVO Market', 'url': BASE, 'inLanguage': LANG[l][2], 'publisher': {'@id': BASE + '#org'}},
                ld_faq(items), *[ld_video(l, k, C) for k in vkeys])
    return P, 'purchases', body, ld

def page_topic(l, page, C):
    P = C['pages'][page]; c = C['common']; ca = c['a']; h = P['hero']; core = page == 'operating-layer'
    area = c['areas'][PAGE_AREA[page]]
    eyebrow = '' if h['eyebrow'].strip().lower() == area.strip().lower() else '<span class="eyebrow">%s</span>' % e(h['eyebrow'])
    cta2 = ('<a class="btn btn--line btn--lg" href="#video">%s%s</a>' % (svg('play'), e(c['videos']['watchVideo']))) if P.get('video') else \
           ('<a class="btn btn--line btn--lg" href="#contact">%s</a>' % e(c['join']['write']))
    hero = ('<div class="band">{HEADER}<section class="phero"><div class="wrap"><div class="phero__copy">'
            '<nav class="crumbs" aria-label="%s"><a href="%s">%s</a>%s<span aria-current="page">%s</span></nav>%s<h1>%s</h1><p class="lede">%s</p>'
            '<div class="ctas"><a class="btn btn--primary btn--lg" href="#join">%s %s</a>%s</div></div>%s</div></section></div>\n'
            % (e(c['nav']['home']), link(l, l, 'index'), e(c['nav']['home']), svg('right'), e(area), eyebrow, e(h['title']), t(h['lede']),
               e(ca['getInvited']), svg('arrow'), cta2, shot(l, SHOT[page], h['shot'], True, cls='phero__media')))
    feats = ''.join('<div class="feat"><span class="feat__n">%02d</span><h3>%s</h3><p class="text">%s</p></div>' % (i + 1, e(a), t(b)) for i, (a, b) in enumerate(P['features']['items']))
    body = hero + '<main id="main">\n'
    body += ('<section class="sec sec--lift"><div class="wrap"><div class="sec__head sec__head--left"><span class="eyebrow">%s</span><h2 class="h2">%s</h2></div>'
             '<div class="features">%s</div></div></section>\n' % (e(area), e(P['features']['title']), feats))
    if core:
        gal = ''.join(shot(l, n, cap) for n, cap in zip(CORE_SHOTS, P['shots']))
        body += '<section class="sec sec--canvas" id="screens"><div class="wrap"><div class="gallery">%s</div></div></section>\n' % gal
    if page == 'finance-administration':
        k = ca['check']
        steps = ''.join('<li><span class="flow__n">%02d</span><h3>%s</h3><p>%s</p></li>' % (i + 1, e(a), t(b)) for i, (a, b) in enumerate(k['steps']))
        body += ('<section class="sec sec--navy" id="check"><div class="wrap"><div class="split"><div><span class="eyebrow">%s</span><h2 class="h2" style="color:#FFFFFF">%s</h2>'
                 '<p class="lede">%s</p></div><div style="display:flex;justify-content:center">%s</div></div><ol class="flow flow--navy" style="margin-top:48px">%s</ol></div></section>\n'
                 % (e(k['eyebrow']), e(k['title']), t(k['text']), check_card(C).replace('class="check"', 'class="check" style="width:min(380px,100%)"'), steps))
        x = ca['connect']
        body += ('<section class="sec" id="connect"><div class="wrap">%s</div></section>\n'
                 % row(row_copy(x), connect_diagram(l, C), flip=True))
    if page == 'operational-scale':
        x = P['a']['project']
        tiles = ''.join('<div class="budget__tile"><small>%s</small><b>%s</b></div>' % (e(a), eur(l, v)) for a, v in
                        [(lbl, val) for lbl, val in zip(_budget_labels(C), [28500.00, 15940.00, 14250.00])])
        ms = ''.join('<li><span>%s</span><span class="status status--%s">%s</span></li>' % (e(a), kind, e(b)) for a, b, kind in _milestones(C))
        card = ('<div class="budget" aria-hidden="true"><div class="budget__tiles">%s</div><div class="budget__bar"><i style="width:56%%;background:var(--teal-d)"></i>'
                '<i style="width:22%%;background:#7FC6D4"></i></div><ul class="budget__ms">%s</ul></div>' % (tiles, ms))
        body += '<section class="sec sec--canvas" id="project"><div class="wrap">%s</div></section>\n' % row(row_copy(x), card)
    flow = ''.join('<li><span class="flow__n">%02d</span><h3>%s</h3><p>%s</p></li>' % (i + 1, e(a), t(b)) for i, (a, b) in enumerate(P['flow']['steps']))
    hi = ''
    if P.get('highlight') and page != 'operational-scale':      # the projects page: its 'coming next' budget is now the section above
        x = P['highlight']
        hi = ('<div class="highlight"><span class="ico">%s</span><div><h3>%s%s</h3><p>%s</p></div></div>'
              % (svg('sparkle'), e(x['title']), (' <span class="badge">%s</span>' % e(c['coming'])) if x.get('badge') == 'coming' else '', t(x['text'])))
    flow_bg = ' sec--canvas' if page != 'operational-scale' else ''
    body += ('<section class="sec%s"><div class="wrap"><div class="sec__head sec__head--left"><h2 class="h2">%s</h2></div><ol class="flow">%s</ol>%s</div></section>\n'
             % (flow_bg, e(P['flow']['title']), flow, hi))
    vld = None
    if P.get('video'):
        k = P['video']; v = c['videos'][k]
        note = ('<p class="vid-note">%s<span>%s</span></p>' % (svg('info'), e(c['videos']['enScreens']))) if l not in APP_LANGS else ''
        player, v0, secs = video_player(l, k, C, 'vpage')
        body += ('<section class="sec" id="video"><div class="wrap vblock"><div class="vblock__copy"><span class="eyebrow">%s · <span class="mono">%s</span></span><h2 class="h2">%s</h2>'
                 '<p class="lede">%s</p><div class="ctas"><a class="btn btn--ghost" href="%s#videos">%s %s</a></div>%s</div>%s</div></section>\n'
                 % (e(c['videos']['eyebrow']), mmss(secs), e(v['title']), t(v['text']), link(l, l, 'index'), e(c['videos']['more']), svg('arrow'), note, player))
        vld = ld_video(l, k, C)
    items = [list(x) for x in P['faq']]
    if page == 'finance-administration': items.append(list(P['a']['faqAdd']))
    body += faq(C, items, cls=' sec--canvas')
    rel = ''.join(area_card(l, k, C) for k in P['related'])
    body += ('<section class="sec"><div class="wrap"><div class="sec__head sec__head--left"><h2 class="h2">%s</h2></div><div class="cards3">%s</div></div></section>\n'
             % (e(c['related']), rel))
    body += invite_contact(l, page, C) + '</main>\n'
    ld = jsonld(ld_crumbs(l, page, C), ld_faq(items), vld)
    return P, SHOT[page], body, ld

def _budget_labels(C):
    a = C['pages']['operational-scale']['a']['project']
    return a['tiles']

def _milestones(C):
    a = C['pages']['operational-scale']['a']['project']
    return [(n, st, kind) for (n, st), kind in zip(a['milestones'], ['ok', 'wait', 'plan'])]

def page_thanks(l, C):
    P = C['pages']['thank-you']; h = P['hero']; k = P['links']; home = link(l, l, 'index')
    body = ('<div class="band">{HEADER}</div><main id="main"><section class="sec"><div class="wrap"><div class="thanks"><span class="ico">%s</span><span class="eyebrow">%s</span><h1>%s</h1>'
            '<p class="lede">%s</p><div class="ctas"><a class="btn btn--primary" href="%s#videos">%s%s</a><a class="btn btn--ghost" href="%s#join">%s</a>'
            '<a class="btn btn--ghost" href="%s">%s</a></div></div></div></section></main>\n'
            % (svg('ok'), e(h['eyebrow']), e(h['title']), t(h['lede']), home, svg('play'), e(k['videos']), home, e(k['join']), home, e(k['home'])))
    return P, 'purchases', body, ''


# ═══════════ round 2 of direction A (3 Nov 2026): Simple · Compliant · Performing, the process by its screens, Good to know, the tour only ═══════════
# Jiri, 3 Nov 00:47: "Make the key message clearly introduced: Simple, Compliant, Performing … much more selling the market as the best place for
# business. Use just the 5 minutes video … apply more … the great idea of 'Good to know' … explain 1 process in detail (by screens)".
# These definitions come after the first round's and take their place.

TOUR_CHAPTERS = [0, 17, 39, 94, 133, 167, 183, 219, 240, 265, 312, 333]      # seconds: the tour's scenes (tourvid/scenes/timeline.json)
PAGE_CHAPTER = {'spend-control': 4, 'revenue-acceleration': 3, 'inventory-control': 5, 'finance-administration': 6, 'operational-scale': 7,
                'compliance-by-design': 1, 'operating-layer': 10}
PROCESS = ['1-request', '2-suppliers', '3-offers', '4-order', '5-received', '6-checked', '7-paid']
PROCESS_URL = ['market.selyvo.com/#/new-request', 'market.selyvo.com/#/new-request', 'market.selyvo.com/#/requests/REQ-2026-0398',
               'market.selyvo.com/#/orders', 'market.selyvo.com/#/orders/ORD-2026-0612', 'market.selyvo.com/#/invoices/received/FV-2026-0042',
               'market.selyvo.com/#/invoices/to-pay']
PILLAR_ICON = {'simple': 'route', 'compliant': 'trust', 'performing': 'trend'}

def featured(l): return 'tour'

def announce(l, page, C):
    a = C['common']['a']
    return ('<div class="announce"><div class="wrap"><span class="announce__new">%s</span><span>%s: %s</span><a href="%s">%s%s</a></div></div>\n'
            % (e(a['new']), e(a['videoGuide']), e(a['tour']['title']), home_link(l, page, 'videos'), e(a['watchIt']), svg('arrow')))

def gtk_box(C, items, cls='gtk'):
    b = C['common']['b']
    items = [items] if isinstance(items, str) else items
    return ('<aside class="%s"><span class="gtk__label">%s%s</span><ul>%s</ul></aside>'
            % (cls, svg('bulb'), e(b['gtk']), ''.join('<li>%s</li>' % t(x) for x in items)))

def tour_player(l, C, pid, start=0):
    f, secs = video_of(l, 'tour')
    poster = up(l) + 'videos/posters/' + f[:-4] + '.jpg'
    return ('<div class="vplayer"><video id="%s" controls preload="none" playsinline poster="%s" aria-label="%s"%s><source src="%s" type="video/mp4"></video></div>'
            % (pid, poster, e(C['common']['a']['tour']['title']), ' data-start="%d"' % start if start else '', video_src(l, f) + ('#t=%d' % start if start else '')), secs)

def videos_section(l, C, cls=' sec--canvas'):
    c = C['common']; b = c['b']; V = C['pages']['index']['b']['video']
    player, secs = tour_player(l, C, 'vmain')
    chap = ''.join('<li><button type="button" data-player="vmain" data-t="%d"><span class="t">%s</span><span>%s</span></button></li>'
                   % (s, mmss(s), e(n)) for s, n in zip(TOUR_CHAPTERS, b['chapters']))
    note = ('<p class="vid-note">%s<span>%s</span></p>' % (svg('info'), e(b['tourNote']))) if l != 'en' else ''
    body = ('<section class="sec%s" id="videos"><div class="wrap"><div class="sec__head"><span class="eyebrow">%s · <span class="mono">%s</span></span><h2 class="h2">%s</h2><p class="lede">%s</p></div>'
            '<div class="vids vids--tour"><div class="vwrap">%s%s</div><div><span class="eyebrow">%s</span><ol class="chap">%s</ol></div></div></div></section>\n'
            % (cls, e(V['eyebrow']), mmss(secs), e(V['title']), t(V['lede']), player, note, e(b['chaptersLabel']), chap))
    return body, ['tour']

def ld_video(l, key, C):
    v = C['common']['a']['tour']; f, secs = video_of(l, 'tour'); b = C['common']['b']
    ends = TOUR_CHAPTERS[1:] + [int(secs)]
    parts = [{'@type': 'Clip', 'name': n, 'startOffset': s, 'endOffset': en, 'url': url(l, 'index') + '#videos'} for s, en, n in zip(TOUR_CHAPTERS, ends, b['chapters'])]
    return {'@type': 'VideoObject', 'name': v['title'], 'description': v['text'], 'thumbnailUrl': BASE + 'videos/posters/' + f[:-4] + '.jpg',
            'contentUrl': BASE + 'videos/' + f, 'uploadDate': TODAY, 'duration': iso_dur(secs), 'inLanguage': 'en-GB', 'hasPart': parts}

def process_section(l, C):
    P = C['pages']['index']['b']['process']; b = C['common']['b']
    tabs, panels = '', ''
    for i, (name, st) in enumerate(zip(PROCESS, P['steps'])):
        on = i == 0
        tabs += ('<li role="presentation"><button type="button" role="tab" id="proc-t%d" aria-controls="proc-p%d" aria-selected="%s"%s><span class="proc__n">%d</span>'
                 '<span><strong>%s</strong><small>%s</small></span></button></li>'
                 % (i + 1, i + 1, 'true' if on else 'false', '' if on else ' tabindex="-1"', i + 1, e(st['title']), t(st['text'])))
        img = ('<figure class="frame"><div class="frame__bar"><i></i><i></i><i></i><span class="frame__url">%s</span></div>'
               '<img src="%s" alt="%s" width="1800" height="1100"%s></figure>'
               % (PROCESS_URL[i], asset(l, 'shots/process/%s.webp' % name), e(st['alt']), ' loading="lazy" decoding="async"' if i else ''))
        nxt = ('<button type="button" class="btn btn--ghost btn--sm proc__next" data-next="%d">%s %s</button>' % (i + 2, e(b['next']), svg('arrow'))) if i < len(PROCESS) - 1 else ''
        panels += ('<div class="proc__panel%s" id="proc-p%d" role="tabpanel" aria-labelledby="proc-t%d"><div class="proc__txt"><h3><span class="mono" style="color:var(--teal-d)">%d · </span>%s</h3><p>%s</p></div>%s'
                   '<div class="proc__foot">%s%s</div></div>'
                   % (' on' if on else '', i + 1, i + 1, i + 1, e(st['title']), t(st['text']), img, gtk_box(C, st['gtk']), nxt))
    note = ('<p class="vid-note proc__note">%s<span>%s</span></p>' % (svg('info'), e(b['screensNote']))) if l != 'en' else ''
    return ('<section class="sec sec--canvas" id="how"><div class="wrap"><div class="sec__head"><span class="eyebrow">%s</span><h2 class="h2">%s</h2><p class="lede">%s</p></div>'
            '<div class="proc"><ol class="proc__steps" role="tablist" aria-label="%s">%s</ol><div class="proc__panels">%s</div></div>%s</div></section>\n'
            % (e(P['eyebrow']), e(P['title']), t(P['lede']), e(P['title']), tabs, panels, note))

def pillars_section(l, C):
    P = C['pages']['index']['b']['pillars']; b = C['common']['b']
    cards = ''
    for k in ('simple', 'compliant', 'performing'):
        x = P[k]
        cards += ('<article class="pil__card pil__card--%s"><div class="pil__top"><span class="ico">%s</span><span class="pil__word">%s</span></div>'
                  '<h3 class="pil__lead">%s</h3><p class="text">%s</p>%s%s</article>'
                  % (k, svg(PILLAR_ICON[k]), e(b[k]), e(x['lead']), t(x['text']), points(x['points']), gtk_box(C, x['gtk'])))
    return ('<section class="sec" id="promises"><div class="wrap"><div class="sec__head"><span class="eyebrow">%s</span><h2 class="h2">%s</h2><p class="lede">%s</p></div>'
            '<div class="pil">%s</div></div></section>\n' % (e(P['eyebrow']), e(P['title']), t(P['lede']), cards))

def compare_section(l, C):
    P = C['pages']['index']['b']['compare']; pr = C['pages']['index']['a']['promise']
    head = '<div class="cmp__row cmp__head" aria-hidden="true"><div></div><div>%s</div><div>%s</div></div>' % (e(P['without']), e(P['with']))
    rows = ''.join('<div class="cmp__row"><div>%s</div><div>%s<span><span class="sr">%s: </span>%s</span></div><div>%s<span><span class="sr">%s: </span>%s</span></div></div>'
                   % (e(a), svg('x'), e(P['without']), t(b_), svg('ok'), e(P['with']), t(c_)) for a, b_, c_ in P['rows'])
    links = ''.join('<a href="%s"><span>%s<small>%s</small></span>%s</a>' % (link(l, l, AREA[k]), e(pr['items'][i][0]), e(pr['items'][i][2]), svg('arrow'))
                    for i, k in enumerate(['sell', 'buy', 'invoices']))
    return ('<section class="sec" id="compare"><div class="wrap"><div class="sec__head"><span class="eyebrow">%s</span><h2 class="h2">%s</h2><p class="lede">%s</p></div>'
            '<div class="cmp">%s%s</div><div class="cmp__links">%s</div></div></section>\n'
            % (e(P['eyebrow']), e(P['title']), t(P['lede']), head, rows, links))

def gtk_band(l, C):
    G = C['pages']['index']['b']['gtk']; b = C['common']['b']
    return ('<section class="sec sec--navy gtkband" id="good-to-know"><div class="wrap"><div class="gtkband__head"><span class="gtk__label">%s%s</span><h2 class="h2">%s</h2>'
            '<p class="lede">%s</p></div><ul class="gtkband__list">%s</ul></div></section>\n'
            % (svg('bulb'), e(b['gtk']), e(G['title']), t(G['lede']), ''.join('<li>%s</li>' % t(x) for x in G['items'])))

def budget_card(l, C):
    tiles = ''.join('<div class="budget__tile"><small>%s</small><b>%s</b></div>' % (e(a), eur(l, v)) for a, v in zip(_budget_labels(C), [28500.00, 15940.00, 14250.00]))
    ms = ''.join('<li><span>%s</span><span class="status status--%s">%s</span></li>' % (e(a), kind, e(b_)) for a, b_, kind in _milestones(C))
    return ('<div class="budget" aria-hidden="true"><div class="budget__tiles">%s</div><div class="budget__bar"><i style="width:56%%;background:var(--teal-d)"></i>'
            '<i style="width:22%%;background:#7FC6D4"></i></div><ul class="budget__ms">%s</ul></div>' % (tiles, ms))

def page_index(l, C):
    P = C['pages']['index']; A = P['a']; B = P['b']; c = C['common']; ca = c['a']
    ticks = ''.join('<li>%s%s</li>' % (svg('tick'), e(x)) for x in A['ticks'])
    floats = ('<div class="float float--l" aria-hidden="true"><div class="float__head"><span class="float__ok">%s</span><span class="float__title">%s</span>'
              '<span class="float__time">10:42</span></div><div class="float__who">Holzwerk Brandt GmbH · <code>REQ-2026-0164</code></div>'
              '<div class="float__row"><span class="float__amt">%s</span><span class="float__note">%s</span></div></div>'
              '<div class="float float--r" aria-hidden="true"><div class="float__head" style="justify-content:space-between"><span class="float__ref">INV-2026-0094</span>'
              '<span class="status status--ok">%s</span></div><div class="float__title" style="margin-top:8px">Nordvik A/S · %s</div>'
              '<div class="float__row"><span class="float__amt">%s</span><span class="float__who" style="margin:0">Revolut Business</span></div></div>'
              % (svg('tick'), e(A['offer']['title']), eur(l, 8469.60), e(A['offer']['note']), e(A['paid']['status']), e(A['paid']['country']), eur(l, 10360.00)))
    w1, w2, w3 = B['title']
    hero = ('<div class="band">{HEADER}<section class="hero"><div class="wrap"><p class="pill"><i></i>%s</p>'
            '<h1 class="slogan"><span>%s</span> <span>%s</span> <span class="hl">%s</span></h1><p class="lede">%s</p>'
            '<div class="ctas"><a class="btn btn--primary btn--lg" href="#join">%s %s</a><a class="btn btn--line btn--lg" href="#videos">%s%s</a></div>'
            '<ul class="ticks">%s</ul><div class="hero__media">%s%s</div></div></section></div>\n'
            % (e(B['pill']), e(w1), e(w2), e(w3), t(B['lede']), e(A['cta']), svg('arrow'), svg('play'), e(B['cta2']), ticks,
               shot(l, 'purchases', '', True, alt=A['shotAlt']), floats))
    facts = list(A['facts']); facts[2] = B['factLang']
    facts = ''.join('<div class="fact"><b>%s</b><p>%s</p></div>' % (e(a.replace(' ', ' ', 1)), t(b_)) for a, b_ in facts)
    R = A['rows']; proj = C['pages']['operational-scale']['a']['project']
    rows = (row(row_copy(R['sell'], link(l, l, 'revenue-acceleration'), c['readMore']), shot(l, 'sales', '', alt=R['sell']['title']))
            + row(row_copy(ca['connect'], link(l, l, 'finance-administration') + '#connect', c['readMore']), connect_diagram(l, C), flip=True, rid='connect')
            + row(row_copy(proj, link(l, l, 'operational-scale') + '#project', c['readMore']), budget_card(l, C)))
    vids, vkeys = videos_section(l, C)
    items = home_faq(P)
    body = (hero
      + '<main id="main">\n<section class="facts lift"><div class="wrap"><div class="facts__grid">%s</div></div></section>\n' % facts
      + pillars_section(l, C) + process_section(l, C) + compare_section(l, C)
      + '<section class="sec sec--canvas" id="features"><div class="wrap rows">%s</div></section>\n' % rows
      + gtk_band(l, C) + vids + faq(C, items) + invite_contact(l, 'index', C) + '</main>\n')
    ld = jsonld({'@type': 'Organization', '@id': BASE + '#org', 'name': 'SELYVO', 'url': BASE, 'logo': BASE + 'assets/selyvo-dark.png', 'slogan': ' '.join(B['title'])},
                {'@type': 'WebSite', '@id': BASE + '#site', 'name': 'SELYVO Market', 'url': BASE, 'inLanguage': LANG[l][2], 'publisher': {'@id': BASE + '#org'}},
                ld_faq(items), ld_video(l, 'tour', C))
    return P, 'purchases', body, ld

def page_topic(l, page, C):
    P = C['pages'][page]; c = C['common']; ca = c['a']; cb = c['b']; h = P['hero']; core = page == 'operating-layer'; PB = P['b']
    area = c['areas'][PAGE_AREA[page]]
    eyebrow = '' if h['eyebrow'].strip().lower() == area.strip().lower() else '<span class="eyebrow">%s</span>' % e(h['eyebrow'])
    cta2 = '<a class="btn btn--line btn--lg" href="#video">%s%s</a>' % (svg('play'), e(cb['watchPart']))
    hero = ('<div class="band">{HEADER}<section class="phero"><div class="wrap"><div class="phero__copy">'
            '<nav class="crumbs" aria-label="%s"><a href="%s">%s</a>%s<span aria-current="page">%s</span></nav>%s<h1>%s</h1><p class="lede">%s</p>'
            '<div class="ctas"><a class="btn btn--primary btn--lg" href="#join">%s %s</a>%s</div></div>%s</div></section></div>\n'
            % (e(c['nav']['home']), link(l, l, 'index'), e(c['nav']['home']), svg('right'), e(area), eyebrow, e(h['title']), t(h['lede']),
               e(ca['getInvited']), svg('arrow'), cta2, shot(l, SHOT[page], h['shot'], True, cls='phero__media')))
    strip = ''.join('<div class="s%d"><div class="pstrip__w"><span class="ico">%s</span>%s</div><p>%s</p></div>' % (i + 1, svg(PILLAR_ICON[k]), e(cb[k]), t(PB['pillars'][i]))
                    for i, k in enumerate(['simple', 'compliant', 'performing']))
    feats = ''.join('<div class="feat"><span class="feat__n">%02d</span><h3>%s</h3><p class="text">%s</p></div>' % (i + 1, e(a), t(b_)) for i, (a, b_) in enumerate(P['features']['items']))
    body = hero + '<main id="main">\n'
    body += ('<section class="sec sec--lift"><div class="wrap" style="display:flex;flex-direction:column;gap:clamp(56px,7vw,88px)"><div class="pstrip">%s</div>'
             '<div><div class="sec__head sec__head--left"><span class="eyebrow">%s</span><h2 class="h2">%s</h2></div><div class="features">%s</div></div></div></section>\n'
             % (strip, e(area), e(P['features']['title']), feats))
    if core:
        gal = ''.join(shot(l, n, cap) for n, cap in zip(CORE_SHOTS, P['shots']))
        body += '<section class="sec sec--canvas" id="screens"><div class="wrap"><div class="gallery">%s</div></div></section>\n' % gal
    if page == 'finance-administration':
        k = ca['check']
        steps = ''.join('<li><span class="flow__n">%02d</span><h3>%s</h3><p>%s</p></li>' % (i + 1, e(a), t(b_)) for i, (a, b_) in enumerate(k['steps']))
        body += ('<section class="sec sec--navy" id="check"><div class="wrap"><div class="split"><div><span class="eyebrow">%s</span><h2 class="h2" style="color:#FFFFFF">%s</h2>'
                 '<p class="lede">%s</p></div><div style="display:flex;justify-content:center">%s</div></div><ol class="flow flow--navy" style="margin-top:48px">%s</ol></div></section>\n'
                 % (e(k['eyebrow']), e(k['title']), t(k['text']), check_card(C).replace('class="check"', 'class="check" style="width:min(380px,100%)"'), steps))
        body += '<section class="sec" id="connect"><div class="wrap">%s</div></section>\n' % row(row_copy(ca['connect']), connect_diagram(l, C), flip=True)
    if page == 'operational-scale':
        body += '<section class="sec sec--canvas" id="project"><div class="wrap">%s</div></section>\n' % row(row_copy(P['a']['project']), budget_card(l, C))
    flow = ''.join('<li><span class="flow__n">%02d</span><h3>%s</h3><p>%s</p></li>' % (i + 1, e(a), t(b_)) for i, (a, b_) in enumerate(P['flow']['steps']))
    hi = ''
    if P.get('highlight') and page != 'operational-scale':
        x = P['highlight']
        hi = ('<div class="highlight"><span class="ico">%s</span><div><h3>%s%s</h3><p>%s</p></div></div>'
              % (svg('sparkle'), e(x['title']), (' <span class="badge">%s</span>' % e(c['coming'])) if x.get('badge') == 'coming' else '', t(x['text'])))
    flow_bg = ' sec--canvas' if page != 'operational-scale' else ''
    proc = C['pages']['index']['b']['process']
    whole = ('<a class="more" href="%s#how">%s %s</a>' % (link(l, l, 'index'), e(proc['title']), svg('arrow'))
             if page in ('spend-control', 'inventory-control', 'finance-administration') else '')     # the purchase, step by step on the home page
    body += ('<section class="sec%s"><div class="wrap"><div class="sec__head sec__head--left"><h2 class="h2">%s</h2></div><div class="flowgtk"><div><ol class="flow">%s</ol>%s%s</div>%s</div></div></section>\n'
             % (flow_bg, e(P['flow']['title']), flow, hi, whole, gtk_box(C, PB['gtk'], 'gtkcard')))
    ch = PAGE_CHAPTER.get(page, 0); start = TOUR_CHAPTERS[ch]
    player, secs = tour_player(l, C, 'vpage', start)
    note = ('<p class="vid-note">%s<span>%s</span></p>' % (svg('info'), e(cb['tourNote']))) if l != 'en' else ''
    jump = ('<div class="vjump"><button type="button" class="vjump__btn" data-player="vpage" data-t="%d"><span class="vjump__play">%s</span>'
            '<span><small>%s</small><strong><span class="mono">%s</span> · %s</strong></span></button>'
            '<button type="button" class="vjump__all" data-player="vpage" data-t="0">%s</button></div>'
            % (start, svg('play'), e(cb['watchPart']), mmss(start), e(cb['chapters'][ch]), e(cb['fromStart'])))
    body += ('<section class="sec" id="video"><div class="wrap vblock"><div class="vblock__copy"><span class="eyebrow">%s · <span class="mono">%s</span></span><h2 class="h2">%s</h2>'
             '<p class="lede">%s</p>%s%s</div><div>%s</div></div></section>\n'
             % (e(C['pages']['index']['b']['video']['eyebrow']), mmss(secs), e(ca['tour']['title']), t(ca['tour']['text']), jump, note, player))
    items = [list(x) for x in P['faq']]
    if page == 'finance-administration': items.append(list(P['a']['faqAdd']))
    body += faq(C, items, cls=' sec--canvas')
    rel = ''.join(area_card(l, k, C) for k in P['related'])
    body += ('<section class="sec"><div class="wrap"><div class="sec__head sec__head--left"><h2 class="h2">%s</h2></div><div class="cards3">%s</div></div></section>\n'
             % (e(c['related']), rel))
    body += invite_contact(l, page, C) + '</main>\n'
    ld = jsonld(ld_crumbs(l, page, C), ld_faq(items), ld_video(l, 'tour', C))
    return P, SHOT[page], body, ld


def page_thanks(l, C):
    P = C['pages']['thank-you']; h = P['hero']; k = P['links']; home = link(l, l, 'index')
    body = ('<div class="band">{HEADER}</div><main id="main"><section class="sec"><div class="wrap"><div class="thanks"><span class="ico">%s</span><span class="eyebrow">%s</span><h1>%s</h1>'
            '<p class="lede">%s</p><div class="ctas"><a class="btn btn--primary" href="%s#videos">%s%s</a><a class="btn btn--ghost" href="%s#join">%s</a>'
            '<a class="btn btn--ghost" href="%s">%s</a></div></div></div></section></main>\n'
            % (svg('ok'), e(h['eyebrow']), e(h['title']), t(P['b']['lede']), home, svg('play'), e(C['pages']['index']['b']['cta2']), home, e(k['join']), home, e(k['home'])))
    return P, 'purchases', body, ''


def render(l, page):
    C = CONTENT[l]
    if page == 'index': P, sh, body, ld = page_index(l, C)
    elif page == 'thank-you': P, sh, body, ld = page_thanks(l, C)
    else: P, sh, body, ld = page_topic(l, page, C)
    og = ('core/' if sh.startswith('core-') else 'en/') + sh + '.jpg'
    hd = head(l, page, C, P, og)
    demo = '<meta name="selyvo-demo" content="1">' if MODE == 'artifact' else ''
    script = '<script src="%s" defer></script>\n' % asset(l, 'site.js')
    content = body.replace('{HEADER}', header(l, page, C), 1) + footer(l, page, C)
    if MODE == 'artifact' and l == 'en' and page == 'index':
        # the Artifact tool wraps this page in its own skeleton: the title first, no html/head/body of our own
        return ('<title>SELYVO Website</title>\n<meta name="claude:viewport-fit-sides" content="cover">\n<meta name="selyvo-lang" content="en-GB">%s\n%s%s%s%s'
                % (demo, hd.split('\n', 1)[1], ld, content, script))
    return ('<!doctype html>\n<html lang="%s" dir="ltr">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n%s%s%s</head>\n<body>\n%s%s</body>\n</html>\n'
            % (LANG[l][2], hd, demo + '\n' if demo else '', ld, content, script))

# ------------------------------------------------------------------------------------------------ the site
def build():
    os.makedirs(OUT, exist_ok=True)
    made = prepare_media()
    A = os.path.join(OUT, 'assets'); os.makedirs(A, exist_ok=True)
    shutil.copy(os.path.join(D, 'assets-src', 'site.css'), A); shutil.copy(os.path.join(D, 'assets-src', 'site.js'), A)
    from PIL import Image
    for src, dst in (('selyvo-dark.png', 'selyvo-dark.png'), ('selyvo-white.png', 'selyvo-white.png')):
        p = os.path.join(A, dst)
        if not os.path.exists(p):
            im = Image.open(os.path.join(D, 'src-site', 'assets', src)).convert('RGBA'); im = im.crop(im.getbbox())
            im.resize((round(im.width * 48 / im.height), 48), Image.LANCZOS).save(p, optimize=True)
    for f in ('favicon.svg', 'favicon.ico'): shutil.copy(os.path.join(D, 'src-site', f), OUT)
    pp = os.path.join(A, 'shots', 'process'); os.makedirs(pp, exist_ok=True)      # the process, from an idea to a paid invoice (the master's screens)
    for f in glob.glob(os.path.join(D, 'shots-process', '*.webp')): shutil.copy(f, pp)
    shutil.copy(os.path.join(D, 'src-site', 'favicon', 'apple-touch-icon.png'), A)
    n = 0
    for l in BUILT:
        for page in PAGES:
            p = os.path.join(OUT, folder(l), page + '.html'); os.makedirs(os.path.dirname(p), exist_ok=True)
            open(p, 'w', encoding='utf-8').write(render(l, page)); n += 1
    # the videos' posters (and, for the zip, the videos)
    pv = os.path.join(OUT, 'videos', 'posters'); shutil.rmtree(pv, ignore_errors=True); os.makedirs(pv, exist_ok=True)
    for f in sorted(DUR): shutil.copy(os.path.join(VIDEO_DIR, 'posters', f[:-4] + '.jpg'), pv)      # only the videos the pages use (since 3 Nov: the tour)
    # the video files themselves are not copied: package.sh puts them in their own zips (the pages expect them in videos/)
    # sitemap and robots
    urls = []
    for page in PAGES[:-1]:
        for l in BUILT:
            alts = ''.join('<xhtml:link rel="alternate" hreflang="%s" href="%s"/>' % (LANG[x][2], url(x, page)) for x in BUILT)
            alts += '<xhtml:link rel="alternate" hreflang="x-default" href="%s"/>' % url('en', page)
            urls.append('<url><loc>%s</loc><lastmod>%s</lastmod><changefreq>%s</changefreq><priority>%s</priority>%s</url>'
                        % (url(l, page), TODAY, 'weekly' if page == 'index' else 'monthly', '1.0' if page == 'index' else '0.8', alts))
    open(os.path.join(OUT, 'sitemap.xml'), 'w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
                                                      'xmlns:xhtml="http://www.w3.org/1999/xhtml">\n' + '\n'.join(urls) + '\n</urlset>\n')
    open(os.path.join(OUT, 'robots.txt'), 'w').write('User-agent: *\nAllow: /\nDisallow: /thank-you.html\nDisallow: /*/thank-you.html\n\nSitemap: %ssitemap.xml\n' % BASE)
    print('%s: %d pages in %d languages (%s), %d pictures made' % (OUT, n, len(BUILT), ' '.join(BUILT), made))
    for w in sorted(set(WARN)): print('  !', w)
    if MISSING_A: print('  ! the new words (content-a) not yet in:', ' '.join(MISSING_A), '— English shown there')
    if MISSING_B: print('  ! round 2 (content-b) not yet in:', ' '.join(MISSING_B), '— English shown there')

if __name__ == '__main__':
    build()
