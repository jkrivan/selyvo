# SELYVO website — handover for development

The new public website for selyvo.com, built around **SELYVO Market** (SELYVO Core stays as an optional product page). It is a
static site: plain HTML, one stylesheet, one script with no libraries, pictures and videos. It is a mockup of content, design and
behaviour; host it as it is or move its pages into the CMS of your choice.

**Design — chosen by Jiri on 3 Nov 2026** ("Perfect, prepare the final website"). Apple's product pages were the model: one idea
per screen in very large type, the product large, **every section light** — white (#FFFFFF) and a light tint of SELYVO's teal
(#E2F2F6) in turn — and the **footer always dark** (#04080F). The four functions come first — **Sell · Buy · Projects · Finance**
— and the market's processes are **played as you scroll**: the app's own horizontal stepper fills, each step's real screen comes
up, the part that matters is marked in orange. Short films of real tasks sit on the pages they belong to. Type: Plus Jakarta Sans
(the app's face) and IBM Plex Mono for references. The buttons are SELYVO orange (#FF8C1F) with **white** text (Jiri's choice,
3 Nov: note that white on this orange reads at about 2.3 : 1, below the 4.5 : 1 the accessibility guidelines ask for text of this
size — a slightly deeper orange on buttons would raise it, if wanted).

## What is in the zips

```
SELYVO-website.zip
  index.html … thank-you.html       English (GB) at the root: the old site's file names are kept, so its URLs stay indexed
  cz/ sk/ de/ es/ dk/ se/ fr/       the other 14 languages, one folder each, named by COUNTRY code (as shown on the site)
  it/ nl/ pt/ pl/ ro/ hu/ no/
  assets/site.css, site.js          the design and its behaviour (below)
  assets/shots/master/*.webp        the approved master's screens, sharp at 2× (one demo business, NuWayMind s.r.o.; English)
  assets/shots/process/*.webp       the seven screens of the process from an idea to a paid invoice (the same demo business)
  assets/shots/core/*.webp          SELYVO Core screens (from the Core mockups, English)
  assets/shots/<lang>/register.webp the joining screen in the app's seven languages (Trust page)
  assets/shots/en/*.jpg, core/*.jpg the pages' share pictures (og:image)
  videos/*.mp4                      the films in English: the tour and the five guides
  videos/posters/*.jpg              each film's title card (the player's poster), in every language it is made in
  videos/thumbs/*.jpg               a still from inside each film for its card; the tour's per page, from that page's part
  sitemap.xml, robots.txt, favicon.svg, favicon.ico
  README.md                         this file
  source/                           everything the pages are made from (below)
SELYVO-website-videos-buying.zip      SELYVO-buying-guide-<CC>.mp4 in the other 14 languages → put them in videos/
SELYVO-website-videos-freelancer.zip  SELYVO-freelancer-guide-<CC>.mp4 in the other 14 languages → put them in videos/
```

## Pages (old URL → new content)

| URL (EN; other languages under /<cc>/) | Page |
|---|---|
| `/` (index.html) | Home: "Sell. Buy. Projects. Finance." with the Home screen rising into place; the four functions as large tiles with their screens; **from an idea to a paid invoice** — 7 steps played as you scroll; "Every business. Checked." (the trust steps light up, the numbers count up); Good to know (cards to swipe); the films — the five-minute tour and the five guides; questions; joining (by invitation) and contact |
| `/revenue-acceleration.html` | Sell — the sales pipeline played as you scroll (Lead → Closed); films: the sales guide, the tour from Sales; features; listings and customers on their screens; Good to know; questions |
| `/spend-control.html` | Buy — request → suppliers → offers → award → order, played as you scroll; films: the buying guide, a request to suppliers found by AI, the tour from Purchases; features; the request taking offers, suppliers |
| `/inventory-control.html` | Orders & deliveries — one order from placed to paid on its own "Where it stands" stepper; films: receiving goods into stock, the tour from Orders |
| `/finance-administration.html` | Finance — an invoice received, checked at SELYVO, approved, paid from your own account; films: the tour from Invoices, the freelancer guide; invoices, connected systems |
| `/operational-scale.html` | Projects — plan, do the work, accepted, billed; films: the freelancer guide (time, expenses, one invoice), the tour from Expenses; the budget, MailChat |
| `/compliance-by-design.html` | Trust — invited, found in the register, checked, qualified, rated; films: the tour from joining, a request to suppliers found by AI (each checked in its register) |
| `/operating-layer.html` | SELYVO Core (optional) — suppliers, questionnaires, request & shop, processes; the tour from Connected systems |
| `/thank-you.html` | after the contact form (noindex) |

Every function page has a page bar under the main bar (the page's name · Overview · How it works · Features · Video · Questions);
its first link starts exactly under the main bar's first (Sell). "Get invited" is in the main bar only; on a page with its own
joining section it goes there. The main bar also has **the language** (the globe and the country code, beside Sign in): it opens
the 15 languages, each the same page in that language. The phone menu lists the languages too, and so does the footer.

## Languages

| shown | folder | `lang` / hreflang | words | films in the language |
|---|---|---|---|---|
| GB | (root) | en-GB | source | all |
| CZ SK DE ES DK SE | cz/ sk/ de/ es/ dk/ se/ | cs-CZ sk-SK de-DE es-ES da-DK sv-SE | translated, reviewed | buying and freelancer guides (narrated, captioned, the app's screens in the language) |
| FR IT NL PT PL RO HU NO | fr/ it/ nl/ pt/ pl/ ro/ hu/ no/ | fr-FR it-IT nl-NL pt-PT pl-PL ro-RO hu-HU nb-NO | translated, reviewed | buying and freelancer guides (narrated and captioned; English screens) |

The other films (the tour, the sales guide, the request to suppliers found by AI, receiving into stock) are English everywhere; on
another language's page the player says "This video is in English." while one of them plays. The site's screens are the master's
English screens in every language; under each process the other languages' pages say "The screens are shown in English. The app
itself works in seven languages." The site shows COUNTRY codes (CZ, DK, SE, NO, GB…); `lang`, `hreflang` and `og:locale` use the
language codes.

## Behaviour (site.js — no libraries)

- **All light, the footer dark.** Every section carries its tone as a class (`tone-l` white, `tone-la` light teal, `tone-d` dark)
  and `data-tone`; the colours are tokens redefined per tone (site.css: mixed/site.css, then mixed/site-light.css on top). The
  generator's `tone_all` (mixed/tpl_e.py) gives the sections white and teal in turn; the footer is dark. The bars are light glass
  with the dark logo, and turn dark glass with the white logo over the footer (they follow the section under them). The same
  generator still makes the earlier version with a few dark sections: `SCHEME=mixed`.
- **A page from the menu opens at its top:** links to pages carry `#top` (the hero's id), so no section of the page before comes along.
- **The language** (`details.lsel` in the main bar; `.mm__langs` in the phone menu): the 15 languages, each a link to the same page in
  that language (`hreflang`, the current one `aria-current`); the panel closes on a click outside it and on Escape. The main bar
  always stays on one line, its links never on two (`fitBar()`): where the phone menu is shown, the language leaves the bar first
  (it is in the menu), then Get invited, and the language comes back where Get invited has gone and it fits; on a desktop the
  language stays — the bar first draws a little closer together, then Get invited goes, and where the links still do not fit they
  go into the menu as on a tablet. While the phone menu is open the bar drops its glass (`.gn--open`): an element with a
  `backdrop-filter` holds its `position: fixed` children to itself, and the menu's full-screen panel is one.
- **Things come in as you reach them** (`data-rv`, IntersectionObserver); the hero's screen **rises into place** (`data-rise`, a 3D
  tilt that flattens as you scroll); counters count up once.
- **The process played as you scroll** (`section.story[data-story]`): a tall section with a sticky stage; its height is
  `steps × 80vh + 100vh`; progress = how far the section has scrolled under the bars; the step = floor(progress × steps). The data
  (JSON in `data-story`): per step the screen's index, the marks (`[left, top, width, height]` in % of the screen) and the address
  shown in the frame. The stepper's line fills from the first step's middle to the last's; done steps get a tick; a step clicked
  scrolls to where it is played. **Played once per visit:** once the visitor has been in it at its first and at its last step, it is
  set still (a section of the stage's height, every step ticked, a step chosen shows it again) — only when it is out of sight and
  the scrolling has stopped, keeping what follows it exactly in place. It is remembered in `sessionStorage`
  (`selyvo-seen:<path>:<n>`), so it stays so for the rest of the visit in that tab. Phones (≤ 900 px), short windows (≤ 620 px
  high) and reduced motion get the steps one under another, each with a small stepper and its marked screen.
- **The films** (`.fplayer[data-films]`): one player per page; the page's films as cards (a still, the length, "Guide" or "Tour ·
  from m:ss"); a card plays its film in the player, the same card again pauses it; the playing card says "Now playing" with
  moving bars. Under the player, the film's chapters: a timeline in parts that fill as it plays, and the chapters by name — a part
  or a name plays from there; the chapter playing is marked and slides into view. "Watch the video" in the hero plays the page's
  first film. Only one video plays at a time; videos load only when played (`preload="none"`). The data (JSON in `data-films`, per
  film): `s` source, `p` poster, `t` title, `x` text, `l` label, `st` start, `c` chapter starts (s), `d` length (s), `n` the note.
- **Good to know** cards scroll sideways with arrows; the phone menu closes on a link or Escape.
- No cookies, no tracking, no external scripts. Fonts from Google Fonts (Plus Jakarta Sans, IBM Plex Mono).

## Videos

| File | Title | Length | Languages | Chapters |
|---|---|---|---|---|
| SELYVO-market-tour-GB.mp4 | SELYVO Market in five minutes | 5:51 | English | 12 |
| SELYVO-sales-guide-GB.mp4 | From a first talk to a won case | 2:58 | English | 12 |
| SELYVO-buying-guide-<CC>.mp4 | From an idea to an approved order | 3:21 (EN) | all 15 | 10 |
| SELYVO-request-AI-suppliers-GB.mp4 | A request to suppliers found by AI | 2:32 | English | 10 |
| SELYVO-receiving-into-stock-GB.mp4 | Receiving ordered goods into stock | 2:13 | English | 8 |
| SELYVO-freelancer-guide-<CC>.mp4 | Time, expenses and the invoice | 2:15 (EN) | all 15 | 8 |

1280 × 720, H.264 + AAC, `faststart`. The chapters' start times were read from the films themselves (where each caption's title
comes up) and are in `source/content-e/film-chapters.json` — the buying and freelancer guides have their own timing in every
language; the tour's are in the generator (`TOUR_CHAPTERS`). Their names are words like any other (`common.e.guides.<film>.chapters`,
the tour's `common.b.chapters`). JSON-LD lists every film as a VideoObject with its chapters as `Clip` parts.

## Search engines

- Every page: its own `<title>` and description per language, `canonical`, `hreflang` for all 15 + `x-default` (English), Open
  Graph and Twitter tags.
- JSON-LD: Organization and WebSite (home), FAQPage, BreadcrumbList (function pages), a VideoObject for each film on the page.
- `sitemap.xml`: 8 pages × 15 languages with `xhtml:link` alternates; `robots.txt` keeps the thank-you pages out.

## The contact form

Netlify Forms, as on the old site: `name="selyvo-contact"`, `data-netlify="true"`, honeypot `bot-field`. Fields: `first-name`,
`last-name`, `email`, `company`, `country`, `topic`, `message`, plus hidden `language` (e.g. de-DE) and `page`. It posts to the
`thank-you.html` of the same language; site.js checks the required fields first. On another host, point it at your handler.

## The words, changing them, adding a language

All words are JSON, one file per language and round, merged in this order (later wins):
`source/content/<lang>.json` (the first site) → `content-a/` (direction A) → `content-b/` (round 2) → `mixed/words/*.en.json` (the
mixed design's English) → `content-e/<lang>.json` (the mixed design's words in each language). `content-e/need-paths.json` lists
every word new or changed in the mixed design: in the other languages these start from the English and take the translation, so a
page never shows an older translation of a sentence the English has changed. `source/words/<lang>.json` is the result — every word
each language's pages show, in one file — the easiest place to start from when you port the site.

`source/build_site_e.py` is the generator these pages were made with (`python3 build_site_e.py zip`); it runs `build_site.py` (the
languages, URLs, SEO, sitemap and the earlier rounds' words) and then the mixed design's templates (`mixed/tpl_d.py`,
`mixed/tpl_e.py`). `check_e.py <lang>` checks a translation (keys, list lengths, untranslated texts, fixed names, no "provider",
short labels). Nothing in the templates is language-specific; a new language is one more set of JSON files.

## Links to check before going live

- "Sign in" goes to `https://market.selyvo.com/` (the product's address in the specifications).
- Canonical, hreflang and sitemap URLs use `https://selyvo.com/`.
