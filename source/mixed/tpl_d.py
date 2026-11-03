
# ═══════════ Concept D (3 Nov 2026): Apple's way ═══════════
# Jiri, 02:42: "Take apple website as good inspiration how it should look … Good point is about the scrolling animation etc. Keep in mind,
# users are split as 50/50 who like light or dark background. You can do some clever animations how it works from process perspective -
# how it's done in SELYVO market."  One idea per screen, big type, the product large; light and dark; the market's processes played as
# you scroll — the app's own stepper filling, its screens, and the part that matters marked on them, as the tour marks it.

FN = ['sell', 'buy', 'projects', 'finance']
FN_PAGE = {'sell': 'revenue-acceleration', 'buy': 'spend-control', 'projects': 'operational-scale', 'finance': 'finance-administration'}
PAGE_FN = {v: k for k, v in FN_PAGE.items()}
PAGE_KEY = {'revenue-acceleration': 'sell', 'spend-control': 'buy', 'operational-scale': 'projects', 'finance-administration': 'finance',
            'inventory-control': 'orders', 'compliance-by-design': 'trust', 'operating-layer': 'core'}
ICON = {'sell': 'sell', 'buy': 'buy', 'projects': 'projects', 'finance': 'invoices', 'orders': 'orders', 'trust': 'trust', 'core': 'core'}
ICONS['moon'] = '<path d="M20 14.5A8.5 8.5 0 1 1 9.5 4a7 7 0 0 0 10.5 10.5z"/>'
ICONS['sun'] = '<circle cx="12" cy="12" r="4"/><path d="M12 2.5v2M12 19.5v2M4.6 4.6 6 6M18 18l1.4 1.4M2.5 12h2M19.5 12h2M4.6 19.4 6 18M18 6l1.4-1.4"/>'
ICONS['left'] = '<path d="m15 6-6 6 6 6"/>'

def dname(C, key):
    c = C['common']['c']
    return c['fn'][key]['name'] if key in c['fn'] else c['nav'][key]

def shot_src(l, name):
    """A screen: the master's (2x, from the tour's stage), a process step (p-…), the Home, or a release / Core picture."""
    from PIL import Image
    if name.startswith('p-'): return asset(l, 'shots/process/%s.webp' % name[2:]), (1800, 1100)
    if name == 'register' or name.startswith('core-'):
        src, wh = shot_file(l, name); return asset(l, 'shots/' + src), wh
    p = os.path.join(DD, 'shots', name + '.webp')
    if not os.path.exists(p): p = os.path.join(CD, 'shots', name + '.webp')
    return asset(l, 'shots/master/%s.webp' % name), Image.open(p).size

def dframe(l, name, url_, alt, eager=False, cls='', inner=''):
    src, (w, h) = shot_src(l, name)
    return ('<figure class="dframe%s"><div class="dframe__bar"><i></i><i></i><i></i><span class="dframe__url">%s</span></div>'
            '<div class="dframe__screen"><img src="%s" alt="%s" width="%d" height="%d"%s>%s</div></figure>'
            % (' ' + cls if cls else '', e(url_), src, e(alt), w, h, ' fetchpriority="high"' if eager else ' loading="lazy" decoding="async"', inner))

def logo(l):
    return ('<img class="logo-l" src="%s" alt="SELYVO" width="171" height="20"><img class="logo-d" src="%s" alt="" width="169" height="20">'
            % (asset(l, 'selyvo-dark.png'), asset(l, 'selyvo-white.png')))

def head(l, page, C, P, image):
    lang, cc, hl, name, loc = LANG[l]
    alts = ''.join('<link rel="alternate" hreflang="%s" href="%s">' % (LANG[x][2], url(x, page)) for x in BUILT)
    alts += '<link rel="alternate" hreflang="x-default" href="%s">' % url('en', page)
    robots = '<meta name="robots" content="noindex, follow">' if page == 'thank-you' else ''
    canon = '' if page == 'thank-you' else '<link rel="canonical" href="%s">%s' % (url(l, page), alts)
    return ('<title>%s</title>\n<meta name="description" content="%s">\n%s%s\n'
            '<meta property="og:type" content="website"><meta property="og:site_name" content="SELYVO"><meta property="og:title" content="%s">'
            '<meta property="og:description" content="%s"><meta property="og:url" content="%s"><meta property="og:image" content="%s">'
            '<meta property="og:locale" content="%s"><meta name="twitter:card" content="summary_large_image">\n'
            '<meta name="color-scheme" content="light dark"><meta name="theme-color" content="#FFFFFF" media="(prefers-color-scheme: light)"><meta name="theme-color" content="#04080F" media="(prefers-color-scheme: dark)">\n'
            '<link rel="icon" href="%sfavicon.svg" type="image/svg+xml"><link rel="icon" href="%sfavicon.ico" sizes="any"><link rel="apple-touch-icon" href="%s">\n'
            '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
            '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@500;600&amp;family=Plus+Jakarta+Sans:wght@400;500;600;700;800&amp;display=swap">\n'
            '<link rel="stylesheet" href="%s">\n'
            '<script>(function(){var d=document.documentElement;d.classList.add(\'js\');try{var t=localStorage.getItem(\'selyvo-theme\');if(t===\'light\'||t===\'dark\')d.setAttribute(\'data-theme\',t)}catch(x){}})()</script>\n'
            % (e(P['title']), e(P['description']), robots, canon, e(P['title']), e(P['description']), url(l, page), BASE + 'assets/shots/' + image,
               loc, up(l), up(l), asset(l, 'apple-touch-icon.png'), asset(l, 'site.css')))

def header(l, page, C):
    c = C['common']; n = c['nav']; a = c['a']; cn = c['c']['nav']; d = c['d']
    cur = lambda p: ' aria-current="page"' if p == page else ''
    links = ''.join('<a href="%s"%s>%s</a>' % (link(l, l, FN_PAGE[k]), cur(FN_PAGE[k]), e(cn[k])) for k in FN)
    links += '<a href="%s"%s>%s</a><a href="%s">%s</a>' % (link(l, l, 'compliance-by-design'), cur('compliance-by-design'), e(cn['trust']), home_link(l, page, 'tour'), e(cn['tour']))
    mlinks = ''.join('<a href="%s"%s>%s</a>' % (link(l, l, FN_PAGE[k]), cur(FN_PAGE[k]), e(cn[k])) for k in FN)
    mlinks += ''.join('<a class="mm__small" href="%s"%s>%s</a>' % (link(l, l, p), cur(p), e(cn[k])) for k, p in (('orders', 'inventory-control'), ('trust', 'compliance-by-design'), ('core', 'operating-layer')))
    mlinks += '<a class="mm__small" href="%s">%s</a>' % (home_link(l, page, 'tour'), e(cn['tour']))
    join = home_link(l, page, 'join') if page != 'index' else '#join'
    theme = ('<button type="button" class="themebtn" data-theme-toggle aria-label="%s" data-l-dark="%s" data-l-light="%s">%s%s</button>'
             % (e(d['theme']['toDark']), e(d['theme']['toDark']), e(d['theme']['toLight']), svg('moon', 'i-moon'), svg('sun', 'i-sun')))
    gn = ('<a class="skip" href="#main">%s</a>\n<header class="gn"><div class="wrap wrap--wide gn__in">'
          '<a class="brand" href="%s" aria-label="SELYVO Market — %s">%s</a><nav class="gn__links" aria-label="%s">%s</nav>'
          '<div class="gn__tools">%s<a class="signin" href="https://market.selyvo.com/">%s</a><a class="pill pill--sm" href="%s">%s</a>'
          '<details class="mm"><summary aria-label="%s">%s</summary><div class="mm__panel"><nav aria-label="%s">%s</nav>'
          '<div class="mm__cta"><a class="pill" href="%s">%s</a><a class="lk" href="https://market.selyvo.com/">%s</a></div></div></details></div>'
          '</div></header>\n'
          % (e(c['skip']), link(l, l, 'index'), e(n['home']), logo(l), e(n['menu']), links, theme, e(n['signIn']), join, e(a['getInvited']),
             e(n['menu']), svg('menu'), e(n['menu']), mlinks, join, e(a['getInvited']), e(n['signIn'])))
    key = PAGE_KEY.get(page)
    if not key: return gn
    lc = d['local']
    ln = ('<div class="ln"><div class="wrap wrap--wide ln__in"><a class="ln__name" href="#top">%s</a><nav class="ln__links" aria-label="%s">'
          '<a href="#top">%s</a>%s<a href="#features">%s</a><a href="#faq">%s</a></nav><a class="pill pill--sm" href="#join">%s</a></div></div>\n'
          % (e(dname(C, key)), e(dname(C, key)), e(lc['overview']), ('<a href="#how">%s</a>' % e(lc['how'])) if C['pages'][page].get('d', {}).get('story') else '',
             e(lc['features']), e(lc['faq']), e(a['getInvited'])))
    return gn + ln

def footer(l, page, C):
    c = C['common']; f = c['footer']; n = c['nav']; cn = c['c']['nav']
    market = ''.join('<li><a href="%s">%s</a></li>' % (link(l, l, FN_PAGE[k]), e(cn[k])) for k in FN)
    market += '<li><a href="%s">%s</a></li>' % (link(l, l, 'inventory-control'), e(cn['orders']))
    comp = ('<li><a href="%s">%s</a></li><li><a href="%s">%s</a></li><li><a href="%s">%s</a></li><li><a href="%s">%s</a></li><li><a href="%s">%s</a></li>'
            '<li><a href="https://market.selyvo.com/">%s</a></li>'
            % (link(l, l, 'compliance-by-design'), e(cn['trust']), link(l, l, 'operating-layer'), e(cn['core']),
               home_link(l, page, 'tour'), e(cn['tour']), home_link(l, page, 'join'), e(n['join']), home_link(l, page, 'contact'), e(f['contact']), e(n['signIn'])))
    langs = ''.join('<a href="%s" hreflang="%s" lang="%s"%s>%s</a>' % (link(l, x, page), LANG[x][2], LANG[x][2], ' aria-current="true"' if x == l else '', e(LANG[x][3])) for x in BUILT)
    return ('<footer class="dft"><div class="wrap wrap--wide"><div class="dft__grid"><div class="dft__brand">%s<p>%s</p></div>'
            '<div><h4>%s</h4><ul>%s</ul></div><div><h4>%s</h4><ul>%s</ul></div><div><h4>%s</h4><div class="dft__langs">%s</div></div></div>'
            '<div class="dft__bottom"><span>%s</span><span>%s</span></div></div></footer>\n'
            % (logo(l), e(f['about']), e(cn['functions']), market, e(f['company']), comp, e(f['languages']), langs, e(f['rights']), e(c['a']['illustrative'])))

def story(l, C, steps, short, eyebrow, title, sub, sid='how'):
    """The market's process, played as you scroll: the app's stepper fills, each step's screen comes up, the part that matters is marked."""
    d = C['common']['d']; n = len(steps)
    shots = []
    for st in steps:
        if st['shot'] not in shots: shots.append(st['shot'])
    data = [{'s': shots.index(st['shot']), 'b': st.get('boxes', []), 'u': st['url']} for st in steps]
    lis = ''.join('<li><button type="button" data-go="%d"><span class="sdot"><span class="sdot__n">%d</span>%s</span><b>%s</b></button></li>'
                  % (i, i + 1, svg('tick'), e(s)) for i, s in enumerate(short))
    copies = ''
    for i, st in enumerate(steps):
        boxes = ''.join('<span class="hl on" style="left:%.1f%%;top:%.1f%%;width:%.1f%%;height:%.1f%%"></span>' % tuple(b) for b in st.get('boxes', []))
        mob = dframe(l, st['shot'], st['url'], st['title'], inner=boxes, cls='scm')
        gtk = ('<p class="gtkd">%s<span><b>%s</b> %s</span></p>' % (svg('bulb'), e(C['common']['c']['gtk']), t(st['gtk']))) if st.get('gtk') else ''
        bar = '<div class="scbar" style="--n:%d" aria-hidden="true">%s</div>' % (n, ''.join('<i class="%s"></i>' % ('done' if j < i else 'now' if j == i else '') for j in range(n)))
        copies += ('<div class="sc%s" data-i="%d">%s<span class="sc__n">%s %d / %d · %s</span><h3>%s</h3><p>%s</p>%s%s</div>'
                   % (' on' if i == 0 else '', i, bar, e(d['stepWord']), i + 1, n, e(short[i]), e(st['title']), t(st['text']), gtk, mob))
    figs = ''
    for k, s in enumerate(shots):
        src, (w, h) = shot_src(l, s)
        figs += ('<div class="ss%s" data-s="%d"><img src="%s" alt="" width="%d" height="%d"%s><span class="hl"></span><span class="hl"></span></div>'
                 % (' on' if k == 0 else '', k, src, w, h, '' if k == 0 else ' loading="lazy" decoding="async"'))
    return ('<section class="sec-d story-intro" id="%s"><div class="wrap wrap--narrow center" data-rv><p class="eyebrow-d">%s</p><h2 class="d-h2">%s</h2><p class="d-sub">%s</p>'
            '<p class="hint">%s %s</p></div></section>\n'
            '<section class="story" data-story=\'%s\' style="--n:%d"><div class="story__stage"><div class="wrap wrap--wide story__wrap">'
            '<div class="story__bar"><ol class="sstp" style="--n:%d"><span class="sstp__track"></span><span class="sstp__fill"></span>%s</ol></div>'
            '<div class="story__body"><div class="story__copy">%s</div>'
            '<figure class="dframe story__frame"><div class="dframe__bar"><i></i><i></i><i></i><span class="dframe__url">%s</span></div><div class="story__screens">%s</div></figure>'
            '</div></div></div></section>\n'
            % (sid, e(eyebrow), e(title), t(sub), svg('chev'), e(d['scrollHint']), json.dumps(data, separators=(',', ':')), n, n, lis, copies, e(steps[0]['url']), figs))

def tiles(l, C, keys, small=False):
    c = C['common']; d = c['d']
    out = ''
    for k in keys:
        f = d['fn'][k]; page = FN_PAGE[k]
        img = '' if small else '<div class="tile__img">%s</div>' % dframe(l, f['shot'], f['url'], c['c']['fn'][k]['name'])
        out += ('<article class="tile%s" data-rv><span class="tile__ico">%s</span><h3>%s</h3><p>%s</p><div class="ctas-d"><a class="lk" href="%s">%s</a><a class="lk" href="%s#how">%s</a></div>%s</article>'
                % (' tile--small' if small else '', svg(ICON[k]), e(c['c']['fn'][k]['name']), e(f['line']), link(l, l, page), e(d['learn']), link(l, l, page), e(d['how']), img))
    return '<div class="tiles%s">%s</div>' % (' tiles--3' if small else '', out)

def verified(l, C):
    V = C['pages']['index']['d']['verified']; cc = C['common']['c']
    steps = ''.join('<li style="--i:%d"><span class="vdot">%s</span><b>%s</b><small>%s</small></li>' % (i, svg('tick'), e(a), e(b)) for i, (a, b) in enumerate(cc['steps']['trust']))
    kpis = ''.join('<div class="kpi-d" data-rv><b data-count="%d">%d</b><span>%s</span><small>%s</small></div>' % (n, n, e(w), e(s)) for n, w, s in V['kpis'])
    return ('<section class="sec-d vband" id="trust"><div class="wrap wrap--wide center"><div class="wrap--narrow" data-rv><p class="eyebrow-d">%s</p><h2 class="d-h2">%s</h2><p class="d-sub">%s</p></div>'
            '<ol class="vsteps" data-rv style="--n:%d">%s</ol><div class="kpis">%s</div><p style="margin-top:40px"><a class="lk lk--light" href="%s">%s</a></p></div></section>\n'
            % (e(V['eyebrow']), e(V['title']), t(V['sub']), len(cc['steps']['trust']), steps, kpis, link(l, l, 'compliance-by-design'), e(V['more'])))

def gtk_gallery(l, C, items, title, sub=''):
    cc = C['common']['c']
    cards = ''.join('<li class="gcard"><span class="gcard__l">%s%s</span><p>%s</p></li>' % (svg('bulb'), e(cc['gtk']), t(x)) for x in items)
    return ('<section class="sec-d" id="good-to-know"><div class="wrap wrap--wide"><div class="head-row" data-rv><div><h2 class="d-h2">%s</h2>%s</div>'
            '<div class="galnav"><button type="button" data-gal="-1" aria-label="‹">%s</button><button type="button" data-gal="1" aria-label="›">%s</button></div></div></div>'
            '<ul class="gal" data-rv>%s</ul></section>\n'
            % (e(title), ('<p class="d-sub">%s</p>' % t(sub)) if sub else '', svg('left'), svg('right'), cards))

def tour(l, C, start=0, ch=0):
    c = C['common']; b = c['b']; V = C['pages']['index']['b']['video']; d = c['d']
    pid = 'vtour'
    player, secs = tour_player(l, C, pid, start)
    ends = TOUR_CHAPTERS[1:] + [int(secs)]
    seg = ''.join('<button type="button" tabindex="-1" data-player="%s" data-t="%d" style="flex-grow:%d" title="%s"></button>' % (pid, s, max(1, en - s), e(nm))
                  for s, en, nm in zip(TOUR_CHAPTERS, ends, b['chapters']))
    chips = ''.join('<button type="button" data-player="%s" data-t="%d"%s><span class="t">%s</span>%s</button>' % (pid, s, ' class="here"' if i == ch and start else '', mmss(s), e(nm))
                    for i, (s, nm) in enumerate(zip(TOUR_CHAPTERS, b['chapters'])))
    note = ('<p class="vnote">%s</p>' % e(d['videoNote'])) if l != 'en' else ''
    lead = ('<p class="d-sub">%s <span class="mono">%s</span> · %s</p>' % (e(b['watchPart']) + ':', mmss(start), e(b['chapters'][ch]))) if start else '<p class="d-sub">%s</p>' % t(V['lede'])
    return ('<section class="sec-d sec-d--alt" id="tour"><div class="wrap wrap--wide"><div class="wrap--narrow center" data-rv><p class="eyebrow-d">%s · <span class="mono">%s</span></p><h2 class="d-h2">%s</h2>%s</div>'
            '<div class="dvid" data-rv>%s<div class="tline" aria-hidden="true">%s</div>%s<div class="dchap" aria-label="%s">%s</div></div></div></section>\n'
            % (e(V['eyebrow']), mmss(secs), e(c['a']['tour']['title']), lead, player, seg, note, e(b['chaptersLabel']), chips))

def dfaq(C, items):
    lst = ''.join('<details><summary>%s<span class="pm"></span></summary><p>%s</p></details>' % (e(q), t(a)) for q, a in items)
    return ('<section class="sec-d" id="faq"><div class="wrap wrap--narrow"><h2 class="d-h2 center" data-rv>%s</h2><div class="dfaq" data-rv>%s</div></div></section>\n'
            % (e(C['common']['faqTitle']), lst))

def join_contact(l, page, C):
    c = C['common']; k = c['contact']; iv = C['pages']['index']['a']['invite']; I = C['pages']['index']['d']['invite']
    topics = ''.join('<option>%s</option>' % e(x) for x in k['topics'])
    netlify = ' data-netlify="true" netlify-honeypot="bot-field"' if MODE == 'zip' else ''
    mail = ('<div class="dmail" aria-hidden="true"><div class="dmail__from"><span class="dmail__av">FS</span><span><b>Form Studio s.r.o.</b><small>%s</small></span></div>'
            '<p>%s</p><span class="dmail__btn">%s</span><small>%s</small></div>' % (e(iv['mockWho']), t(iv['mockText']), e(iv['mockButton']), e(iv['mockValid'])))
    return (
      '<section class="sec-d sec-d--alt" id="join"><div class="wrap wrap--wide"><div class="djoin"><div data-rv><h2 class="d-h2">%s</h2><p class="d-sub">%s</p>'
      '<div class="ctas-d ctas-d--left"><a class="pill" href="#contact">%s</a><a class="lk" href="%s">%s</a></div></div><div data-rv>%s</div></div>'
      '<div class="dcontact" id="contact"><div data-rv><p class="eyebrow-d">%s</p><h2 class="d-h3">%s</h2><p class="d-body">%s</p></div>'
      '<form class="dform" name="selyvo-contact" method="POST" action="thank-you.html" data-thanks="thank-you.html" accept-charset="UTF-8" novalidate%s data-rv>'
      '<input type="hidden" name="form-name" value="selyvo-contact"><input type="hidden" name="language" value="%s"><input type="hidden" name="page" value="%s">'
      '<p hidden><label>Bot <input name="bot-field" tabindex="-1" autocomplete="off"></label></p>'
      '<div class="dform__row"><label>%s<input name="first-name" autocomplete="given-name" required></label><label>%s<input name="last-name" autocomplete="family-name" required></label></div>'
      '<div class="dform__row"><label>%s<input name="email" type="email" inputmode="email" autocomplete="email" spellcheck="false" required></label><label>%s<input name="company" autocomplete="organization"></label></div>'
      '<div class="dform__row"><label>%s<input name="country" autocomplete="country-name"></label><label>%s<select name="topic">%s</select></label></div>'
      '<label>%s<textarea name="message" rows="5" required></textarea></label><p class="form__err" role="alert" hidden>%s</p>'
      '<div class="dform__foot"><button class="pill" type="submit">%s</button><small>%s</small></div></form></div></div></section>\n'
      % (e(I['title']), t(I['sub']), e(c['join']['write']), (link(l, l, 'compliance-by-design') + '#tour') if page != 'compliance-by-design' else '#tour', e(iv['cta']), mail,
         e(k['eyebrow']), e(k['title']), t(k['lede']), netlify, LANG[l][2], page,
         e(k['firstName']), e(k['lastName']), e(k['email']), e(k['company']), e(k['country']), e(k['topic']), topics, e(k['message']), e(k['required']), e(k['send']), e(k['note'])))

def page_index(l, C):
    P = C['pages']['index']; D_ = P['d']; A = P['a']; B = P['b']; c = C['common']; d = c['d']
    hero = ('{HEADER}<section class="hx" id="top"><div class="wrap center"><p class="eyebrow-d" data-rv>%s</p><h1 class="d-hero" data-rv>%s</h1>'
            '<p class="d-sub" data-rv>%s</p><div class="ctas-d" data-rv><a class="pill" href="#join">%s</a><a class="lk" href="#tour">%s</a></div></div>'
            '<div class="wrap wrap--wide"><div class="hx__media" data-rise>%s</div></div></section>\n'
            % (e(D_['eyebrow']), e(D_['title']), t(D_['sub']), e(c['a']['getInvited']), e(d['watch']), dframe(l, D_['heroShot'], D_['heroUrl'], D_['heroAlt'], True)))
    S = D_['story']; steps = []
    for st, bx, name in zip(B['process']['steps'], S['boxes'], PROCESS):
        steps.append({'title': st['title'], 'text': st['text'], 'gtk': st['gtk'], 'shot': 'p-' + name, 'url': PROCESS_URL[PROCESS.index(name)], 'boxes': bx})
    items = home_faq(P)
    body = (hero + '<main id="main">\n'
            + '<section class="sec-d sec-d--tiles"><div class="wrap wrap--wide">%s</div></section>\n' % tiles(l, C, FN)
            + story(l, C, steps, P['c']['processShort'], S['eyebrow'], S['title'], S['sub'])
            + verified(l, C)
            + gtk_gallery(l, C, B['gtk']['items'], c['d']['gtkTitle'], D_['gtkSub'])
            + tour(l, C) + dfaq(C, items) + join_contact(l, 'index', C) + '</main>\n')
    ld = jsonld({'@type': 'Organization', '@id': BASE + '#org', 'name': 'SELYVO', 'url': BASE, 'logo': BASE + 'assets/selyvo-dark.png'},
                {'@type': 'WebSite', '@id': BASE + '#site', 'name': 'SELYVO Market', 'url': BASE, 'inLanguage': LANG[l][2], 'publisher': {'@id': BASE + '#org'}},
                ld_faq(items), ld_video(l, 'tour', C))
    return P, 'purchases', body, ld

def page_topic(l, page, C):
    P = C['pages'][page]; c = C['common']; cc = c['c']; d = c['d']; X = P['d']; key = PAGE_KEY[page]; name = dname(C, key)
    hero = ('{HEADER}<section class="hx hx--page" id="top"><div class="wrap center"><p class="eyebrow-d" data-rv>%s</p><h1 class="d-h1" data-rv>%s</h1>'
            '<p class="d-sub" data-rv>%s</p><div class="ctas-d" data-rv><a class="pill" href="#join">%s</a><a class="lk" href="#tour">%s</a></div></div>'
            '<div class="wrap wrap--wide"><div class="hx__media" data-rise>%s</div></div></section>\n'
            % (e(name), e(X['title']), t(X['sub']), e(c['a']['getInvited']), e(c['b']['watchPart']), dframe(l, X['heroShot'], X['heroUrl'], P['hero'].get('shot') or name, True)))
    body = hero + '<main id="main">\n'
    if X.get('story'):
        S = X['story']; steps = [dict(s) for s in S['steps']]
        short = [a for a, b in cc['steps'][key]]
        body += story(l, C, steps, short, name, S['title'], S['sub'])
    elif key == 'trust':
        body += verified(l, C).replace(' id="trust"', ' id="how"', 1)
    wide = {0, 3, 5}
    feats = ''.join('<div class="bx%s" data-rv><span class="bx__n">%02d</span><h3>%s</h3><p>%s</p></div>' % (' bx--wide' if i in wide else '', i + 1, e(a), t(b_))
                    for i, (a, b_) in enumerate(P['features']['items']))
    hi = ''
    if P.get('highlight') and page == 'spend-control':
        x = P['highlight']
        hi = ('<div class="dnote" data-rv>%s<div><b>%s</b>%s<p>%s</p></div></div>'
              % (svg('sparkle'), e(x['title']), (' <span class="soon">%s</span>' % e(c['coming'])) if x.get('badge') == 'coming' else '', t(x['text'])))
    body += ('<section class="sec-d sec-d--alt" id="features"><div class="wrap wrap--wide"><div class="wrap--narrow center" data-rv><p class="eyebrow-d">%s</p><h2 class="d-h2">%s</h2></div>'
             '<div class="bento">%s</div>%s</div></section>\n' % (e(name), e(P['features']['title']), feats, hi))
    if page == 'operating-layer':
        gal = ''.join('<div data-rv>%s<p class="cap">%s</p></div>' % (dframe(l, n_, CORE_LABEL[n_], cap), t(cap)) for n_, cap in zip(CORE_SHOTS[1:], P['shots'][1:]))
        body += '<section class="sec-d"><div class="wrap wrap--wide"><div class="dgallery">%s</div></div></section>\n' % gal
    rows = P.get('c', {}).get('rows') or []
    for r in rows:
        body += ('<section class="sec-d"><div class="wrap wrap--wide"><div class="wrap--narrow center" data-rv><p class="eyebrow-d">%s</p><h2 class="d-h2">%s</h2><p class="d-sub">%s</p>'
                 '<ul class="chips">%s</ul></div><div class="row-d" data-rise>%s</div></div></section>\n'
                 % (e(r['eyebrow']), e(r['title']), t(r['text']), ''.join('<li>%s<span>%s</span></li>' % (svg('tick'), t(x)) for x in r['points']), dframe(l, r['screen'], r['url'], r['title'])))
    gt = (P.get('b') or {}).get('gtk')
    if gt: body += gtk_gallery(l, C, gt, d['gtkTitle'])
    ch = PAGE_CHAPTER.get(page, 0)
    body += tour(l, C, TOUR_CHAPTERS[ch], ch)
    items = [list(x) for x in P['faq']]
    if page == 'finance-administration': items.append(list(P['a']['faqAdd']))
    body += dfaq(C, items)
    others = [x for x in FN if FN_PAGE[x] != page]
    body += ('<section class="sec-d sec-d--alt"><div class="wrap wrap--wide"><h2 class="d-h2 center" data-rv>%s</h2>%s</div></section>\n'
             % (e(d['others']), tiles(l, C, others, small=True)))
    body += join_contact(l, page, C).replace('sec-d sec-d--alt" id="join"', 'sec-d" id="join"', 1) + '</main>\n'
    ld = jsonld(ld_crumbs(l, page, C), ld_faq(items), ld_video(l, 'tour', C))
    return P, SHOT[page], body, ld

def ld_crumbs(l, page, C):
    return {'@type': 'BreadcrumbList', 'itemListElement': [{'@type': 'ListItem', 'position': 1, 'name': C['common']['nav']['home'], 'item': url(l, 'index')},
            {'@type': 'ListItem', 'position': 2, 'name': dname(C, PAGE_KEY[page]), 'item': url(l, page)}]}

def page_thanks(l, C):
    P = C['pages']['thank-you']; h = P['hero']; k = P['links']; home = link(l, l, 'index')
    body = ('{HEADER}<main id="main"><section class="hx" id="top"><div class="wrap center"><p class="eyebrow-d">%s</p><h1 class="d-h1">%s</h1>'
            '<p class="d-sub">%s</p><div class="ctas-d"><a class="pill" href="%s#tour">%s</a><a class="lk" href="%s#join">%s</a><a class="lk" href="%s">%s</a></div></div></section></main>\n'
            % (e(h['eyebrow']), e(h['title']), t(P['b']['lede']), home, e(C['pages']['index']['b']['cta2']), home, e(k['join']), home, e(k['home'])))
    return P, 'purchases', body, ''

def tour_player(l, C, pid, start=0):
    f, secs = video_of(l, 'tour')
    poster = up(l) + 'videos/posters/' + f[:-4] + '.jpg'
    return ('<video id="%s" controls preload="none" playsinline poster="%s" aria-label="%s"%s><source src="%s" type="video/mp4"></video>'
            % (pid, poster, e(C['common']['a']['tour']['title']), ' data-start="%d"' % start if start else '', video_src(l, f) + ('#t=%d' % start if start else '')), secs)
