
# ═══════════ selyvo.com, the mixed design (3 Nov 2026; concept E, made the site at 11:17): concept D with its sections in turn dark and light ═══════════
# Jiri, 07:43: "The last one looks good, please prepare a version which combines the light and dark sections."  The page alternates
# dark and light sections as Apple's product pages do (light ones in turn white and pale); the bar follows the section under it; no
# theme switch — one design for everyone.
import re as _re
TONE_SCHEME = globals().get('TONE_SCHEME', 'mixed')      # set by build_site_e.py (SCHEME=light for the all-light version)
_D_header, _D_tiles, _D_page_index, _D_page_topic, _D_page_thanks, _D_head = header, tiles, page_index, page_topic, page_thanks, head

def head(l, page, C, P, image):
    h = _D_head(l, page, C, P, image)
    h = h.replace('<meta name="color-scheme" content="light dark"><meta name="theme-color" content="#FFFFFF" media="(prefers-color-scheme: light)"><meta name="theme-color" content="#04080F" media="(prefers-color-scheme: dark)">',
                  '<meta name="theme-color" content="#04080F">', 1)
    return h

# Jiri, 3 Nov 10:22: a page chosen in the top menu opens at its top (links to a page carry #top — the viewer may otherwise bring along
# the hash of the page before, and every page has a #tour, #how, #faq…); one Get invited only, in the main bar (on a page with its own
# joining section it goes there); the page bar's first link under the main bar's first one (mixed.js lines it up).
_TOP = _re.compile(r'href="((?:\.\./)*(?:[a-z]{2}/)?(?:%s)\.html)"' % '|'.join(_re.escape(p) for p in PAGES if p != 'thank-you'))
def tops(h): return _TOP.sub(r'href="\1#top"', h)

# Jiri, 3 Nov 13:46: "there is missing language selection at the top of the pages to show pages in the other languages."  The language
# in the main bar, beside Sign in (the globe, the country code shown on the site); it opens the 15 languages, each the same page in
# that language. On a phone, where the bar has room for Get invited or the language, the languages are in the menu as well (site.js).
def lang_items(l, page):
    return ''.join('<a href="%s" hreflang="%s" lang="%s"%s><span class="cc">%s</span><span class="nm">%s</span>%s</a>'
                   % (link(l, x, page), LANG[x][2], LANG[x][2], ' aria-current="true"' if x == l else '', LANG[x][1], e(LANG[x][3]),
                      svg('tick', 'ck') if x == l else '') for x in BUILT)

def lang_picker(l, page, C):
    n = C['common']['nav']
    return ('<details class="lsel"><summary aria-label="%s: %s">%s<span class="cc">%s</span>%s</summary>'
            '<div class="lsel__panel"><p class="lsel__h">%s</p><nav class="lsel__grid" aria-label="%s">%s</nav></div></details>'
            % (e(n['language']), e(LANG[l][3]), svg('globe'), LANG[l][1], svg('chev', 'chev'), e(n['language']), e(n['language']), lang_items(l, page)))

def header(l, page, C):
    h = _D_header(l, page, C)
    h = _re.sub(r'<button type="button" class="themebtn".*?</button>', '', h, count=1, flags=_re.S)
    n = C['common']['nav']
    h = h.replace('<div class="gn__tools"><a class="signin"', '<div class="gn__tools">%s<a class="signin"' % lang_picker(l, page, C), 1)
    h = h.replace('</div></div></details></div></div></header>',
                  '</div><div class="mm__langs"><p class="lsel__h">%s</p><nav class="mm__lgrid" aria-label="%s">%s</nav></div></div></details></div></div></header>'
                  % (e(n['language']), e(n['language']), lang_items(l, page)), 1)
    lc = C['common']['d']['local']        # the page's own bar: the films too
    h = h.replace('<a href="#faq">%s</a>' % e(lc['faq']), '<a href="#tour">%s</a><a href="#faq">%s</a>' % (e(C['common']['e']['localVideo']), e(lc['faq'])), 1)
    h = _re.sub(r'(</nav>)<a class="pill pill--sm" href="#join">[^<]*</a>(</div></div>\n)$', r'\1\2', h, count=1)     # the page bar: no button of its own
    if page != 'thank-you': h = h.replace('href="%s"' % home_link(l, page, 'join'), 'href="#join"')               # Get invited: this page's own joining
    h = tops(h)
    if TONE_SCHEME == 'light': return h          # the light version: the bars light from the start
    return h.replace('<header class="gn">', '<header class="gn gn--dark">', 1).replace('<div class="ln">', '<div class="ln ln--dark">', 1)

def tiles(l, C, keys, small=False):
    h = _D_tiles(l, C, keys, small)
    if small: return h
    n = [0]
    def tone(m):
        i = n[0]; n[0] += 1
        return '<article class="tile tone-d"' if i >= 2 and TONE_SCHEME != 'light' else m.group(0)     # Jiri, 3 Nov 09:25: one row light (Sell, Buy), the second dark (Projects, Finance); the light version: all light
    return _re.sub(r'<article class="tile"', tone, h)

# Jiri, 3 Nov 12:38: "make most of the topics with white background, few of them with dark and ensure footer is always dark".
# Dark: the hero (each page opens on it), the films (a film plays best on dark) and, on the home page, "Every business. Checked.";
# every other section light — white and pale in turn, white first after a dark one; the footer always dark (footer()).
DARK_SECTIONS = {'hx', 'films'}
def tone_all(body, page=''):
    """The sections' tones: the few dark ones above, the rest light; a story's pinned stage keeps its introduction's tone."""
    tones, li = [], [0]
    def rep(m):
        cls = [c for c in m.group(1).split() if c != 'sec-d--alt']
        if cls and cls[0] == 'story' and tones: t = tones[-1]
        elif TONE_SCHEME != 'light' and (DARK_SECTIONS & set(cls) or (page == 'index' and 'vband' in cls)): t = 'd'; li[0] = 0
        else: t = ('l', 'la')[li[0] % 2]; li[0] += 1
        tones.append(t)
        return '<section class="%s tone-%s" data-tone="%s"' % (' '.join(cls), t, 'dark' if t == 'd' else 'light')
    return _re.sub(r'<section class="([^"]*)"', rep, body)

# ═══════════ 3 Nov, 09:25: the guides on the pages they belong to ═══════════
# Jiri: "add attached videos into relevant pages to make it a little bit more interactive."  One player for each page; the films that
# belong to the page as cards beside it — the one chosen plays there; the film's chapters as a timeline that fills as it plays and takes
# you to any step (the steps the film's own captions name). The tour stays: on the home page first, on the others from their part.
FILM_FILE = {'tour': 'SELYVO-market-tour-GB.mp4', 'sales': 'SELYVO-sales-guide-GB.mp4', 'buying': 'SELYVO-buying-guide-GB.mp4',
             'requestai': 'SELYVO-request-AI-suppliers-GB.mp4', 'receiving': 'SELYVO-receiving-into-stock-GB.mp4', 'freelancer': 'SELYVO-freelancer-guide-GB.mp4'}
# seconds: where each chapter's caption comes up in each film, read from the films themselves (web/content-e/film-chapters.json — the
# buying and freelancer guides have their own timing in every language); the chapters' words are in content-e
FILM_CHAPTERS = json.load(open(os.path.join(D, 'content-e', 'film-chapters.json'), encoding='utf-8'))
LOCAL_FILMS = ('buying', 'freelancer')       # made in all 15 languages (narrated and captioned; the app's 7 languages on their own screens)
PAGE_FILMS = {'index': ['tour', 'sales', 'buying', 'requestai', 'receiving', 'freelancer'],
              'revenue-acceleration': ['sales', 'tour'], 'spend-control': ['buying', 'requestai', 'tour'],
              'inventory-control': ['receiving', 'tour'], 'operational-scale': ['freelancer', 'tour'],
              'finance-administration': ['tour', 'freelancer'], 'compliance-by-design': ['tour', 'requestai'], 'operating-layer': ['tour']}
TOUR_THUMB = {'index': 47, 'revenue-acceleration': 102, 'spend-control': 141, 'inventory-control': 173, 'finance-administration': 191,
              'operational-scale': 227, 'compliance-by-design': 22, 'operating-layer': 320}     # a still from the tour's part for each page
CUR = {'page': 'index'}
FDUR = {}

def film(l, C, k, page):
    """A film as the page shows it: the language's own where it is made (the buying and freelancer guides), else the English one —
    then with a note under the player on the other languages' pages."""
    E = C['common']['e']; cc = LANG[l][1]
    if k == 'tour':
        f, _ = video_of(l, 'tour')
        ch = PAGE_CHAPTER.get(page, 0) if page != 'index' else 0
        start = TOUR_CHAPTERS[ch] if ch else 0
        starts, names = TOUR_CHAPTERS, C['common']['b']['chapters']
        title, text = C['common']['a']['tour']['title'], C['common']['a']['tour']['text']
        thumb = 'videos/thumbs/%s-%03d.jpg' % (f[:-4], TOUR_THUMB[page]); kind = E['tourWord']
    else:
        f = FILM_FILE[k]; start = 0
        if k in LOCAL_FILMS:
            own = '%s-%s.mp4' % (VNAME[k], cc)
            if os.path.exists(os.path.join(VIDEO_DIR, own)) and (MODE != 'artifact' or own in ART_VIDEOS): f = own
            elif l != 'en': WARN.append('film %s: %s shows the English one' % (k, l))
            title, text = C['common']['videos'][k]['title'], C['common']['videos'][k]['text']       # the films' own titles (round 1, every language)
        else: title, text = E['guides'][k]['title'], E['guides'][k]['text']
        starts, names = FILM_CHAPTERS.get(f), E['guides'][k]['chapters']
        if not starts: WARN.append('film %s: no chapters' % f); starts = [0]
        thumb = 'videos/thumbs/%s.jpg' % f[:-4]; kind = E['guideWord']
    if f not in FDUR:
        FDUR[f] = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', os.path.join(VIDEO_DIR, f)],
                                       capture_output=True, text=True).stdout.strip() or 0)
        if not FDUR[f]: WARN.append('film %s missing' % f)
    secs = FDUR[f]
    if len(starts) != len(names):
        WARN.append('film %s (%s): %d chapters, %d names' % (f, l, len(starts), len(names))); n = min(len(starts), len(names)); starts, names = starts[:n], names[:n]
    if MODE == 'artifact':
        src = ART_VIDEOS.get(f, '/_blob/pending')
        if f not in ART_VIDEOS: WARN.append('artifact: %s not in the asset store yet' % f)
    else: src = up(l) + 'videos/' + f
    english = f.endswith('-GB.mp4')
    return {'k': k, 'f': f, 'secs': secs, 'start': start, 'starts': starts, 'names': names, 'title': title, 'text': text,
            'src': src + ('#t=%d' % start if start else ''), 'poster': up(l) + 'videos/posters/' + f[:-4] + '.jpg', 'thumb': up(l) + thumb,
            'kind': kind + (' · %s %s' % (E['fromWord'], mmss(start)) if start else ''), 'now': '%s · %s' % (kind, mmss(secs)),
            'note': E['note'] if english and l != 'en' else '', 'lang': 'en-GB' if english else LANG[l][2]}

def fchap(fm, i, on):
    """A film's chapters: a timeline in parts that fill as it plays, and the chapters by name; a part or a name chosen plays from there."""
    ends = list(fm['starts'][1:]) + [fm['secs']]
    seg = ''.join('<button type="button" tabindex="-1" data-t="%s" style="flex-grow:%d" title="%s"><i></i></button>' % (('%g' % s), max(1, round(en - s)), e(n))
                  for s, en, n in zip(fm['starts'], ends, fm['names']))
    cur = max(j for j, s in enumerate(fm['starts']) if s <= fm['start'])
    chips = ''.join('<button type="button" data-t="%s"%s><span class="t">%s</span>%s</button>' % (('%g' % s), ' aria-current="true"' if j == cur else '', mmss(s), e(n))
                    for j, (s, n) in enumerate(zip(fm['starts'], fm['names'])))
    return '<div class="fchap" data-film="%d"%s><div class="ftl" aria-hidden="true">%s</div><div class="dchap">%s</div></div>' % (i, '' if on else ' hidden', seg, chips)

def films(l, C, page):
    c = C['common']; E = c['e']; b = c['b']
    fl = [film(l, C, k, page) for k in PAGE_FILMS[page]]
    f0 = fl[0]
    if page == 'index': title, sub = E['homeTitle'], E['homeSub']
    elif len(fl) > 1: title, sub = E['title'], E['sub']
    else:
        ch = PAGE_CHAPTER.get(page, 0)
        title, sub = c['a']['tour']['title'], '%s: <span class="mono">%s</span> · %s' % (e(b['watchPart']), mmss(f0['start']), e(b['chapters'][ch]))
    data = [{'s': fm['src'], 'p': fm['poster'], 't': fm['title'], 'x': fm['text'], 'l': fm['now'], 'st': fm['start'], 'c': fm['starts'], 'd': round(fm['secs'], 2), 'n': fm['note']} for fm in fl]
    player = ('<video id="vtour" controls preload="none" playsinline poster="%s" aria-label="%s"><source src="%s" type="video/mp4"></video>'
              % (f0['poster'], e(f0['title']), f0['src']))
    now = ('<div class="fnow"><p class="fnow__l"><span class="eq" aria-hidden="true"><i></i><i></i><i></i></span><span class="fnow__label">%s</span></p>'
           '<h3 class="fnow__t">%s</h3><p class="fnow__x">%s</p></div>' % (e(f0['now']), e(f0['title']), t(f0['text'])))
    chaps = ''.join(fchap(fm, i, i == 0) for i, fm in enumerate(fl))
    note = '<p class="vnote fnote"%s>%s</p>' % ('' if f0['note'] else ' hidden', e(f0['note'])) if l != 'en' else ''      # under an English film on the other languages' pages
    cards = ''
    if len(fl) > 1:
        cards = '<ul class="fcards" aria-label="%s">%s</ul>' % (e(E['eyebrow']), ''.join(
            '<li><button type="button" class="fcard" data-film="%d" aria-pressed="%s" aria-controls="vtour"><span class="fcard__img"><img src="%s" alt="" width="640" height="360" loading="lazy" decoding="async">'
            '<span class="fcard__play">%s</span><span class="fcard__dur">%s</span></span><span class="fcard__txt"><span class="fcard__l"><span class="eq" aria-hidden="true"><i></i><i></i><i></i></span>'
            '<span class="fcard__kind">%s</span><span class="fcard__now">%s</span></span><b>%s</b></span></button></li>'
            % (i, 'true' if i == 0 else 'false', fm['thumb'], svg('play'), mmss(fm['secs']), e(fm['kind']), e(E['nowPlaying']), e(fm['title'])) for i, fm in enumerate(fl)))
    return ('<section class="sec-d films" id="tour"><div class="wrap wrap--wide"><div class="wrap--narrow center" data-rv><p class="eyebrow-d">%s</p><h2 class="d-h2">%s</h2><p class="d-sub">%s</p></div>'
            '<div class="fplayer" data-films="%s" data-rv><div class="fstage">%s</div>%s%s%s</div>%s</div></section>\n'
            % (e(E['eyebrow']), e(title), t(sub) if '<span' not in sub else sub, e(json.dumps(data, separators=(',', ':'), ensure_ascii=False)), player, now, chaps, note, cards))

def tour(l, C, start=0, ch=0):              # the tour's section becomes the page's films
    return films(l, C, CUR['page'])

def ld_films(l, C, page):
    out = []
    for k in PAGE_FILMS[page]:
        if k == 'tour': continue
        fm = film(l, C, k, page); ends = list(fm['starts'][1:]) + [fm['secs']]
        parts = [{'@type': 'Clip', 'name': n, 'startOffset': int(s), 'endOffset': int(en), 'url': url(l, page) + '#tour'} for s, en, n in zip(fm['starts'], ends, fm['names'])]
        out.append({'@type': 'VideoObject', 'name': fm['title'], 'description': fm['text'], 'thumbnailUrl': BASE + 'videos/posters/' + fm['f'][:-4] + '.jpg',
                    'contentUrl': BASE + 'videos/' + fm['f'], 'uploadDate': TODAY, 'duration': iso_dur(fm['secs']), 'inLanguage': fm['lang'], 'hasPart': parts})
    return out

def ld_more(ld, objs):
    m = _re.match(r'<script type="application/ld\+json">(.*)</script>\n$', ld, _re.S)
    if not m or not objs: return ld
    g = json.loads(m.group(1).replace('<\\/', '</'))['@graph']
    return jsonld(*(g + objs))

def seen_hint(body, C):
    """Once every step of a process has been seen it stays as seen, without the scrolling (mixed.js); its hint then says so."""
    return _re.sub(r'<p class="hint">(<svg.*?</svg>) ([^<]*)</p>', lambda m: '<p class="hint">%s <span data-seen="%s">%s</span></p>' % (m.group(1), e(C['common']['e']['seenHint']), m.group(2)), body)

def screens_note(body, l, C):
    if l == 'en': return body
    return _re.sub(r'(<p class="hint">.*?</p>)', lambda m: m.group(1) + '<p class="vnote">%s</p>' % e(C['common']['b']['screensNote']), body, count=1)

def page_index(l, C):
    CUR['page'] = 'index'
    P, sh, body, ld = _D_page_index(l, C)
    d = C['common']['d']
    body = body.replace('<a class="lk" href="#tour">%s</a>' % e(d['watch']), '<a class="lk" href="#tour" data-play>%s</a>' % e(d['watch']), 1)
    return P, sh, tone_all(screens_note(seen_hint(tops(body), C), l, C), 'index'), ld_more(ld, ld_films(l, C, 'index'))

def page_topic(l, page, C):
    CUR['page'] = page
    P, sh, body, ld = _D_page_topic(l, page, C)
    c = C['common']
    body = body.replace('<a class="lk" href="#tour">%s</a>' % e(c['b']['watchPart']), '<a class="lk" href="#tour" data-play>%s</a>' % e(c['e']['watch']), 1)
    # the films come right after the process played as you scroll (or the trust steps), where the page has one
    fs = _re.search(r'<section class="sec-d films".*?</section>\n', body, _re.S)
    m = _re.search(r'<section class="story".*?</section>\n', body, _re.S) or _re.search(r'<section class="sec-d vband" id="how".*?</section>\n', body, _re.S)
    if fs and m and m.end() <= fs.start():
        body = body[:m.end()] + fs.group(0) + body[m.end():fs.start()] + body[fs.end():]
    return P, sh, tone_all(screens_note(seen_hint(tops(body), C), l, C), page), ld_more(ld, ld_films(l, C, page))

def page_thanks(l, C):
    P, sh, body, ld = _D_page_thanks(l, C)
    return P, sh, tone_all(tops(body), 'thank-you'), ld

_D_footer = footer
def footer(l, page, C):
    return tops(_D_footer(l, page, C).replace('<footer class="dft">', '<footer class="dft tone-d" data-tone="dark">', 1))
