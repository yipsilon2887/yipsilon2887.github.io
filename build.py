"""Build a dependency-free, multilingual personal website."""
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = json.loads((ROOT / 'content.json').read_text(encoding='utf-8'))
SOCIAL = json.loads((ROOT / 'social.json').read_text(encoding='utf-8'))
RESUME = json.loads((ROOT / 'resume.json').read_text(encoding='utf-8'))
OUT = ROOT

def e(value):
    return html.escape(value, quote=True)

def prose(value):
    return e(value).replace('&lt;br&gt;', '<br>')

def display_name(d, key):
    if d['name'] != '\u53f6\u6bc5\u9676':
        return e(d['name'])
    return f'<span>{e(d["name"][:1])}</span><span class="name-given">{e(d["name"][1:])}</span>'

def social_links(key):
    icons = {
        'linkedin': '<rect x="2" y="2" width="20" height="20" rx="2" fill="currentColor"/><text x="5" y="18" fill="var(--paper)" font-family="Arial,sans-serif" font-weight="700" font-size="16">in</text>',
        'x': '<path fill="currentColor" d="M18.9 2H22l-6.8 7.8L23.2 22h-6.3l-4.9-6.5L6.3 22H3.2l7.3-8.4L.8 2h6.5l4.4 5.8L16.8 2h2.1ZM17.8 20h1.8L6.3 4H4.4l13.4 16Z"/>',
        'github': '<path fill="currentColor" d="M12 .3a12 12 0 0 0-3.8 23.4c.6.1.8-.3.8-.6v-2.3c-3.4.7-4.1-1.4-4.1-1.4-.5-1.4-1.3-1.8-1.3-1.8-1.1-.7.1-.7.1-.7 1.2.1 1.8 1.3 1.8 1.3 1 1.8 2.8 1.3 3.5 1 .1-.8.4-1.3.8-1.6-2.7-.3-5.5-1.4-5.5-6a4.7 4.7 0 0 1 1.2-3.2c-.1-.3-.5-1.6.1-3.2 0 0 1-.3 3.3 1.2a11.4 11.4 0 0 1 6 0c2.3-1.5 3.3-1.2 3.3-1.2.6 1.6.2 2.9.1 3.2a4.7 4.7 0 0 1 1.2 3.2c0 4.6-2.8 5.7-5.5 6 .4.4.8 1.1.8 2.2v3.3c0 .3.2.7.8.6A12 12 0 0 0 12 .3Z"/>',
        'email': '<g fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="m3 5 9 8 9-8"/></g>',
    }
    labels = {'linkedin': 'LinkedIn', 'x': 'X', 'github': 'GitHub', 'email': {'ja': 'メール', 'zh': '邮箱', 'en': 'Email'}[key]}
    links = []
    for platform in ['linkedin', 'x', 'github', 'email']:
        href = SOCIAL.get(platform)
        if not href:
            continue
        extra = ' target="_blank" rel="noopener noreferrer"' if href.startswith('https://') else ''
        links.append(f'<a href="{e(href)}" aria-label="{e(labels[platform])}"{extra}><svg viewBox="0 0 24 24" aria-hidden="true">{icons[platform]}</svg><span>{e(labels[platform])}</span></a>')
    return '<div class="social-links" id="contact">' + ''.join(links) + '</div>'

def icon_map(labels):
    return f'''<svg viewBox="0 0 380 265" role="img" aria-label="{e(' / '.join(labels))}">
      <g fill="none" stroke="#91a486" stroke-width="1"><circle cx="190" cy="116" r="94" stroke-dasharray="2 7"/><path d="M190 24L101 177L279 177Z"/><path d="M190 116L190 24M190 116L101 177M190 116L279 177" stroke-dasharray="3 5"/></g>
      <g fill="#edf0e5" stroke="#718667"><circle cx="190" cy="35" r="24"/><circle cx="106" cy="177" r="24"/><circle cx="274" cy="177" r="24"/></g>
      <g stroke="#476950" fill="none" stroke-width="1.5"><path d="M181 35h18m-13-7v14m8-18v22M94 183l12-18 12 18M97 177h18M262 177q3-15 6 0t6 0t6 0t6 0"/></g>
      <circle cx="190" cy="116" r="6" fill="#476950"/>
      <g fill="#40553d" font-family="Arial, sans-serif" font-size="12" text-anchor="middle"><text x="190" y="79">{e(labels[0])}</text><text x="106" y="222">{e(labels[1])}</text><text x="274" y="222">{e(labels[2])}</text></g>
    </svg>'''

def artwork(i):
    drawings = [
      '<rect x="18" y="12" width="194" height="125" rx="3"/><path d="M18 34h194M31 24h3m5 0h3m5 0h3"/><rect x="31" y="48" width="48" height="53"/><rect x="91" y="48" width="48" height="53"/><rect x="151" y="48" width="48" height="53"/><path d="M31 113h32m28 0h32m28 0h32M125 86l17 36 5-14 15-2z"/><path d="M38 78l14-18 18 31M98 85l17-22 17 15M157 87l15-25 18 20" stroke="#9baa8e"/>',
      '<path d="M25 31h180M25 76h180M25 121h180" stroke="#c0c8b8"/><path d="M45 31L84 76L136 121M84 76L159 76M45 31L180 31"/><path d="M25 148h180M66 143v10m45-10v10m45-10v10" stroke="#9baa8e"/><g fill="#476950"><circle cx="45" cy="31" r="5"/><circle cx="84" cy="76" r="5"/><circle cx="136" cy="121" r="5"/><circle cx="159" cy="76" r="5"/><circle cx="180" cy="31" r="5"/></g>',
      '<rect x="26" y="40" width="66" height="66" rx="5"/><circle cx="59" cy="73" r="18" stroke-dasharray="3 4"/><circle cx="59" cy="73" r="4" fill="#476950"/><path d="M100 73h18m-6-5 6 5-6 5M130 73q5-29 10 0t10 0t10 0t10 0t10 0t10 0t10 0M26 126h178"/><path d="M34 136v8m7-8v4m7-4v4m7-4v8m7-8v4m7-4v4m7-4v8" stroke="#9baa8e"/>'
    ]
    return '<div class="project-art" aria-hidden="true"><svg viewBox="0 0 230 164"><g fill="none" stroke="#627c59" stroke-width="1.25" stroke-linejoin="round">'+drawings[i]+'</g></svg></div>'

def header(d, key, cv=False):
    prefix = '../' if cv else ''
    # Each language has its own real URL and remains usable without JavaScript.
    links = ''.join(f'<a href="../../{k}/{"cv/" if cv else ""}" lang="{DATA[k]["lang"]}" data-language="{k}"'+(' aria-current="page"' if k == key else '')+f'>{label}</a>' for k,label in [('ja','JP'),('zh','CN'),('en','EN')])
    if not cv:
        links = links.replace('../../','../')
    nav = ''.join(f'<a href="{prefix}#{target}">{e(label)}</a>' for target,label in zip(['research','experience','about','contact'],d['nav']))
    return f'<a class="skip" href="#main">{e(d["skip"])}</a><header><div class="wrap topbar"><a class="brand" aria-label="{e(d["nickname"])}" href="{prefix or "./"}">{e(d["nickname"])}</a><nav class="nav" aria-label="Navigation">{nav}</nav><nav class="langs" aria-label="Language">{links}</nav></div></header>'

def footer(d, cv=False):
    return '<footer><div class="wrap footer-inner"><span>&copy; 2026 '+e(d['name'])+'</span><span>Tokyo, Japan</span><span>'+e(d['updated'])+'</span></div></footer>'

def shell(d,key,body,cv=False):
    base='../../' if cv else '../'
    alternates=''.join(f'<link rel="alternate" hreflang="{DATA[k]["lang"]}" href="{base}{k}/{"cv/" if cv else ""}">' for k in DATA)
    title=(d['cvTitle']+' | '+d['title']) if cv else d['title']
    return f'''<!doctype html>
<html lang="{d['lang']}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{e(title)}</title><meta name="description" content="{e(d['description'])}"><meta name="theme-color" content="#f8f6ef"><meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(d['description'])}"><meta property="og:type" content="website"><link rel="icon" href="{base}favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="{base}styles.css">{alternates}</head><body>{header(d,key,cv)}{body}{footer(d,cv)}<script src="{base}site.js" defer></script></body></html>'''

def jobs(d):
    return ''.join(f'<article class="job"><span class="date">{e(j["date"])}</span><h3>{e(j["company"])}</h3><p class="role">{e(j["role"])}</p><p>{e(j["text"])}</p></article>' for j in d['jobs'])

def listing(items):
    return '<ul>'+''.join('<li>'+e(x)+'</li>' for x in items)+'</ul>'

def home(d,key):
    cv_label = {'ja': '\u7d4c\u6b74\u3092\u898b\u308b', 'zh': '\u67e5\u770b\u5c65\u5386', 'en': 'View CV'}[key]
    projects=''.join(f'<article class="project" id="{p["id"]}"><h3>{e(p["title"].replace("<br>"," "))}</h3><p>{e(p["summary"])}</p><span class="status">{e(p["status"])}</span></article>' for p in d['projects'])
    identity=''.join(f'<div><span class="label">{e(a)}</span><p>{e(b)}</p></div>' for a,b in d['identity'])
    targets=['research','recognition','experience','about']
    tabs=''.join(f'<a role="tab" id="tab-{target}" aria-controls="{target}" aria-selected="{str(i==0).lower()}" href="#{target}"><span class="tab-no">0{i+1}</span><span><strong>{e(label)}</strong><small>{e(note)}</small></span></a>' for i,(target,label,note) in enumerate(zip(targets,d['tabLabels'],d['tabNotes'])))
    internships=''.join(f'<article class="internship"><span class="date">{e(j["date"])}</span><div><h3>{e(j["company"])}</h3><p>{e(j["role"])}</p>{"<p class=chr-note>"+e(j["text"])+"</p>" if j["text"] else ""}</div></article>' for j in d['jobs'])
    body=f'''<main id="main" class="wrap profile-layout">
      <aside class="profile-side"><div class="profile-art profile-photo"><a href="../portrait.jpg"><img src="../portrait.jpg" alt="{e(d['portraitAlt'])}" width="3024" height="4032" fetchpriority="high"></a></div>{social_links(key)}<a class="side-cv" href="cv/">{e(cv_label)} <span aria-hidden="true">&#8594;</span></a><p class="location">TOKYO, JAPAN</p></aside>
      <div class="profile-main"><section class="intro"><p class="affiliation">{e(d['affiliation'])}</p><h1 aria-label="{e(d['name'])}">{display_name(d,key)}</h1><h2>{prose(d['headline'])}</h2><p class="bio">{e(d['bio'])}</p><div class="identity-strip">{identity}</div></section>
      <div class="topic-layout"><nav class="topic-nav" aria-label="{e(d['contentsLabel'])}"><p>{e(d['contentsLabel'])}</p><div role="tablist" aria-label="{e(d['contentsLabel'])}">{tabs}</div></nav><div class="panels">
      <section class="topic-panel" id="research" role="tabpanel" aria-labelledby="tab-research"><span class="eyebrow">{e(d['researchTitle'])} / 01</span>{projects}</section>
      <section class="topic-panel" id="recognition" role="tabpanel" aria-labelledby="tab-recognition"><span class="eyebrow">{e(d['recognitionTitle'])} / 02</span><h2>{e(d['recognition'])}</h2><p>{e(d['presentation'])}</p></section>
      <section class="topic-panel" id="experience" role="tabpanel" aria-labelledby="tab-experience"><span class="eyebrow">{e(d['experienceTitle'])} / 03</span><h2>{e(d['experienceTitle'])}</h2>{internships}</section>
      <section class="topic-panel" id="about" role="tabpanel" aria-labelledby="tab-about"><span class="eyebrow">{e(d['aboutTitle'])} / 04</span><h2>{e(d['personalHeading'])}</h2>{listing(d['personalList']+d['communityList'])}</section>
      </div></div></div>
    </main>'''
    return shell(d,key,body)

def cv(d,key):
    r = RESUME[key]
    education = ''.join(f'<article class="resume-entry"><h3>{e(institution)}</h3><p>{e(degree)}</p></article>' for institution,degree in d['education'])
    research = ''.join(f'<article class="resume-entry"><h3>{e(project["title"])}</h3><p class="resume-meta">{e(project["status"])}</p>{listing(project["bullets"])}</article>' for project in r['entries'])
    internships = ''.join(f'<article class="resume-entry"><div class="resume-row"><h3>{e(job["company"])}</h3><span class="resume-date">{e(job["date"])}</span></div><p>{e(job["role"])}</p></article>' for job in d['jobs'])
    contacts = '<span>Tokyo, Japan</span>'
    for platform, label in [('email','Email'),('github','GitHub'),('linkedin','LinkedIn')]:
        if SOCIAL.get(platform):
            contacts += f'<a href="{e(SOCIAL[platform])}">{e(SOCIAL[platform].removeprefix("mailto:")) if platform == "email" else label}</a>'
    contacts += '<a href="../">Website</a>'
    body=f'''<main id="main" class="wrap resume-wrap"><article class="cv-section resume-sheet"><div class="cv-actions"><a href="../">&#8592; {e(d['back'])}</a><button class="cv-button" id="print">{e(d['print'])}</button></div><div class="resume-heading"><p class="resume-kicker">{e(r['title'])}</p><h1>{e(d['name'])}</h1><p class="resume-subtitle">{e(r['headline'])}</p><div class="resume-contacts">{contacts}</div></div>
      <section class="resume-section"><h2>{e(r['education'])}</h2>{education}<p class="resume-background">{e(r['background'])}</p></section>
      <section class="resume-section"><h2>{e(r['research'])}</h2>{research}</section>
      <section class="resume-section"><h2>{e(r['internships'])}</h2>{internships}</section>
      <section class="resume-section"><h2>{e(r['recognition'])}</h2>{listing(r['awards'])}</section>
      <section class="resume-section"><h2>{e(r['skills'])}</h2><dl class="resume-skills">{''.join('<div><dt>'+e(label)+'</dt><dd>'+e(value)+'</dd></div>' for label,value in r['skillRows'])}</dl>{listing(d['communityList'])}</section>
      <p class="resume-updated">{e(d['updated'])}</p></article></main>'''
    return shell(d,key,body,True)

# Each page remains a complete static document. Embed the other rendered languages
# so ordinary language clicks need neither a network request nor a new document.
rendered = {key+'/': home(d,key) for key,d in DATA.items()}
rendered.update({key+'/cv/': cv(d,key) for key,d in DATA.items()})
language_payload = json.dumps(rendered, ensure_ascii=False, separators=(',', ':')).replace('<', '\\u003c')
for key,d in DATA.items():
    (OUT/key/'cv').mkdir(parents=True,exist_ok=True)
    page = rendered[key+'/'].replace('<script src="../site.js"', '<script type="application/json" id="language-pages">'+language_payload+'</script><script src="../site.js"')
    (OUT/key/'index.html').write_text(page,encoding='utf-8')
    # The web CV uses only the same profile facts already shown on the homepage.
    cv_page = rendered[key+'/cv/'].replace('<script src="../../site.js"', '<script type="application/json" id="language-pages">'+language_payload+'</script><script src="../../site.js"')
    (OUT/key/'cv'/'index.html').write_text(cv_page,encoding='utf-8')
(OUT/'index.html').write_text('<!doctype html><html lang="ja"><head><meta charset="utf-8"><meta http-equiv="refresh" content="0;url=ja/"><title>Yitao Ye</title></head><body><a href="ja/">'+e(DATA['ja']['name'])+' / Japanese</a> &middot; <a href="zh/">Chinese</a> &middot; <a href="en/">English</a></body></html>',encoding='utf-8')
(OUT/'print.js').write_text("document.getElementById('print').addEventListener('click', () => window.print());\n",encoding='utf-8')
(OUT/'.nojekyll').touch()
print('Built 3 language homepages and 3 web CV pages.')
