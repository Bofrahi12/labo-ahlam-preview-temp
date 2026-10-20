#!/usr/bin/env python3
"""Labo Ahlam — EN espace-dentistes via index-keyed map + wholesale JS/JSON replacement."""
import re, os, json

OUT = os.path.dirname(os.path.abspath(__file__))
BASE = 'https://laboahlam.com'
SRC = open(os.path.join(OUT, 'espace-dentistes.html'), encoding='utf-8').read()

def extract_all(h):
    texts = set()
    for m in re.findall(r'>([^<]{2,}?)<', h):
        t = m.strip()
        if len(t) > 1: texts.add(t)
    for m in re.findall(r'(?:alt|title|content|aria-label|placeholder)="([^"]+)"', h):
        texts.add(m)
    for m in re.findall(r"'([^']{3,}?)'", h):
        if '<' not in m: texts.add(m)
    for m in re.findall(r'"([^"]{3,}?)"', h):
        if '<' not in m and ':' not in m[:12]: texts.add(m)
    return sorted(texts)

IDX = extract_all(SRC)
assert len(IDX) == 157, f'espace strings changed: {len(IDX)}'
assert IDX[95].startswith('Vous êtes') and 'Fiche de laboratoire en ligne' in IDX[51]

EN = {
29:'Arch involved, patient age, constraints, remarks…',
30:'Other / to be specified',
32:'Dentists: send your cases to the Labo Ahlam laboratory (Tangier) in 1 minute. Online lab order form — dentures, night guards, ceramic crowns. Direct reply on WhatsApp.',
33:'How do we start working together?',
34:'How do I send the impression and the case photos?',
35:'How are partner rates calculated?',
36:'How does it work, for your practice?',
37:'Lab confirmation',
39:'Ceramic crowns / veneers',
40:'Desired date', 41:'Desired date: ', 42:'Dentist / Practice: ', 43:'Dr … / Practice …',
44:'Case details', 45:'Case details: ',
46:'Send the form to the lab →',
47:'Simply send your first form via the form above (or a WhatsApp message): the lab reviews the case and replies to you directly. No prior commitment.',
48:'Send your lab orders in 1 minute — direct reply from the lab on WhatsApp.',
49:'Dentists Space', 50:'Dentists Space — Labo Ahlam',
51:'Dentists Space — Labo Ahlam | Online lab order form, Tangier',
52:'Partners Space',
53:'E.g. 3 units, full arch…', 54:'E.g. A2, B1…', 55:'E.g. before 30/10',
57:'Made at the laboratory',
58:"Online lab order form for dentists: complete and partial dentures, flexible silicone, stellite, Snap-on Smile, night guards, ceramic crowns and veneers. The form arrives directly on the lab's WhatsApp.",
59:'Lab order form',
60:'Night guard (retainer / bruxism)',
61:'I will send the impression photos right after this message.',
62:'The form + the photos',
65:'Labo Ahlam — dental prosthesis laboratory in Tangier, run by',
66:'Labo Ahlam — dental prosthesis laboratory, Tangier · WhatsApp',
67:'Dental prosthesis laboratory for dental practices',
68:'The timeline is given as soon as each case is received, depending on the type of work — no generic timeline: you know what to expect before you start.',
69:'The lab reviews the case and confirms feasibility and timeline as soon as it is received.',
70:'The work is made at the laboratory, with fitting and adjustments through to the final result.',
71:"The case photos are sent on WhatsApp right after the form. For the physical impression, how it's sent is decided together based on your city, at first contact.",
72:'Rates are worked out according to the type of work and your volume, and discussed directly with Ahlam — no generic public price applies to partner practices.',
75:'Dentist / practice name *',
76:'Number of units / teeth', 77:'Number of units: ',
78:'Our work for your patients',
79:'Complete denture', 80:'Classic partial denture / stellite', 81:'Flexible partial denture (silicone)',
82:'What are the production timelines?',
84:'Questions from practices',
88:'Tooth gems', 89:'Shade (if applicable)',
90:'Type of work *', 91:'Type of work: ', 92:'Phone / WhatsApp *',
93:'A case to discuss before sending?',
94:'You send the form below, then the impression/case photos on the same WhatsApp.',
95:'Are you a dentist? Send your cases to the laboratory in 1 minute.',
96:"The lab's WhatsApp — 0609238630",
111:'directly, fully organised',
138:"on the lab's WhatsApp, with all the case details.",
144:'· Instagram',
145:'Write directly to the laboratory on WhatsApp — replies during working hours: 10:00–13:00 / 15:00–19:30.',
147:'Working hours: 10:00–13:00 & 15:00–19:30',
148:'Booking', 149:'Services', 150:'Home', 151:'Celebrities', 152:'Dentists',
153:'— works with dental practices. Fill in the form below: it arrives',
155:'← Dentists Space',
156:'📎 After sending the form, send the model/case photos in the same WhatsApp conversation — so the complete file reaches the laboratory.',
}

h = SRC
for i in sorted(EN, key=lambda i: -len(IDX[i])):
    if IDX[i] in h: h = h.replace(IDX[i], EN[i])
    else: print('espace EN miss:', i, IDX[i][:50])

# wholesale: WhatsApp builder script
start = h.find('NOUVELLE FICHE')
s0 = h.rfind('<script', 0, start); s1 = h.find('</script>', start) + 9
new_script = """<script>
document.getElementById('labForm').addEventListener('submit', function(e){
  e.preventDefault();
  var g=function(id){return document.getElementById(id).value.trim();};
  var lines=["NEW LAB ORDER — Labo Ahlam","———————————",
  "Dentist / Practice: "+g('dName'),
  "Phone: "+g('dPhone'),
  "Type of work: "+g('dType')];
  if(g('dCount')) lines.push("Number of units: "+g('dCount'));
  if(g('dShade')) lines.push("Shade: "+g('dShade'));
  if(g('dDate')) lines.push("Desired date: "+g('dDate'));
  if(g('dNotes')) lines.push("Case details: "+g('dNotes'));
  lines.push("","I will send the impression photos right after this message.");
  window.open("https://wa.me/212609238630?text="+encodeURIComponent(lines.join("\\n")),"_blank");
});
</script>"""
h = h[:s0] + new_script + h[s1:]

# wholesale: JSON-LD
graph = {"@context": "https://schema.org", "@graph": [
  {"@type": "Service", "@id": f"{BASE}/en/espace-dentistes.html#service", "name": EN[67],
   "provider": {"@id": f"{BASE}/#business"}, "areaServed": {"@type": "Country", "name": "Morocco"},
   "description": EN[58]},
  {"@type": "BreadcrumbList", "itemListElement": [
    {"@type": "ListItem", "position": 1, "name": "Labo Ahlam", "item": f"{BASE}/en/"},
    {"@type": "ListItem", "position": 2, "name": "Dentists Space", "item": f"{BASE}/en/espace-dentistes.html"}]},
  {"@type": "FAQPage", "mainEntity": [
    {"@type": "Question", "name": EN[33], "acceptedAnswer": {"@type": "Answer", "text": EN[47]}},
    {"@type": "Question", "name": EN[82], "acceptedAnswer": {"@type": "Answer", "text": EN[68]}},
    {"@type": "Question", "name": EN[35], "acceptedAnswer": {"@type": "Answer", "text": EN[72]}},
    {"@type": "Question", "name": EN[34], "acceptedAnswer": {"@type": "Answer", "text": EN[71]}}]},
]}
j0 = h.find('"@context"'); js0 = h.rfind('<script', 0, j0); js1 = h.find('</script>', j0) + 9
h = h[:js0] + '<script type="application/ld+json">\n' + json.dumps(graph, ensure_ascii=False, indent=1) + '\n</script>' + h[js1:]

SW_CSS = '<style>.lang-sw{display:inline-flex;gap:6px;align-items:center}.lang-sw a{border:1px solid #3d6a96;color:#a9c6de;border-radius:999px;padding:7px 13px;font-weight:800;font-size:13px;text-decoration:none}.lang-sw a.on{background:#2f80ed;color:#fff;border-color:#2f80ed}</style>'
SW = '<div class="lang-sw"><a href="../espace-dentistes.html">عربي</a><a href="../fr/espace-dentistes.html">FR</a><a class="on" href="espace-dentistes.html">EN</a></div>'
h = h.replace('"labo/', '"../labo/')
h = re.sub(r'<html lang="ar" dir="rtl">', '<html lang="en" dir="ltr">', h)
h = h.replace('</nav>', '</nav>' + SW, 1) if '</nav>' in h else h.replace('</header>', SW + '</header>', 1)
blocks = (f'<link rel="canonical" href="{BASE}/en/espace-dentistes.html">'
          f'<link rel="alternate" hreflang="ar" href="{BASE}/espace-dentistes.html">'
          f'<link rel="alternate" hreflang="fr" href="{BASE}/fr/espace-dentistes.html">'
          f'<link rel="alternate" hreflang="en" href="{BASE}/en/espace-dentistes.html">'
          f'<link rel="alternate" hreflang="x-default" href="{BASE}/espace-dentistes.html">')
h = h.replace('</head>', blocks + SW_CSS + '</head>', 1)
open(os.path.join(OUT, 'en', 'espace-dentistes.html'), 'w', encoding='utf-8').write(h)

# AR espace: switcher + hreflang for consistency
p = os.path.join(OUT, 'espace-dentistes.html'); hh = open(p, encoding='utf-8').read()
if 'lang-sw' not in hh:
    SW_AR = '<div class="lang-sw"><a class="on" href="espace-dentistes.html">عربي</a><a href="fr/espace-dentistes.html">FR</a><a href="en/espace-dentistes.html">EN</a></div>'
    hh = hh.replace('</nav>', '</nav>' + SW_AR, 1) if '</nav>' in hh else hh.replace('</header>', SW_AR + '</header>', 1)
    blocks_ar = (f'<link rel="alternate" hreflang="ar" href="{BASE}/espace-dentistes.html">'
                 f'<link rel="alternate" hreflang="fr" href="{BASE}/fr/espace-dentistes.html">'
                 f'<link rel="alternate" hreflang="en" href="{BASE}/en/espace-dentistes.html">'
                 f'<link rel="alternate" hreflang="x-default" href="{BASE}/espace-dentistes.html">')
    hh = hh.replace('</head>', blocks_ar + SW_CSS + '</head>', 1)
    open(p, 'w', encoding='utf-8').write(hh); print('AR espace patched')
print('ESPACE EN DONE')
