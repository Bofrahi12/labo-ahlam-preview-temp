#!/usr/bin/env python3
"""Labo Ahlam — 7 answer-first service pages. Content = verified site facts only."""
import json, urllib.parse, os

OUT = os.path.dirname(os.path.abspath(__file__))
WA = "212609238630"

CSS = """
:root{--bg:#061626;--bg2:#081f36;--panel:#0d2a45;--line:#1e4266;--hair:rgba(190,225,255,.12);--txt:#eef7ff;--mut:#a9c6de;--pink:#56ccf2;--vio:#2f80ed;--wa:#22c064}
*{margin:0;padding:0;box-sizing:border-box}
body{background:var(--bg);color:var(--txt);font-family:'Segoe UI',Tahoma,Arial,sans-serif;line-height:1.8}
.wrap{max-width:920px;margin:0 auto;padding:0 20px}
header{border-bottom:1px solid var(--hair);padding:16px 0}
header .wrap{display:flex;justify-content:space-between;align-items:center;gap:12px}
.logo{font-weight:800;font-size:19px;color:var(--txt);text-decoration:none}
.logo span{color:var(--pink)}
nav a{color:var(--mut);text-decoration:none;margin-inline-start:16px;font-size:15px}
nav a:hover{color:var(--pink)}
.crumb{color:var(--mut);font-size:13px;padding:18px 0 0}
.crumb a{color:var(--mut)}
.eyebrow{color:var(--pink);font-size:14px;font-weight:700;letter-spacing:.4px;margin-top:14px}
h1{font-size:31px;line-height:1.45;margin:6px 0 12px}
h2{font-size:23px;margin:34px 0 12px}
p,li{color:#d7e9f7;font-size:16.5px}
.lede{font-size:18px;color:var(--txt)}
.hero-img{width:100%;border-radius:18px;border:1px solid var(--hair);margin:20px 0 6px;aspect-ratio:16/8;object-fit:cover}
ul{padding-inline-start:22px}
.card{background:var(--panel);border:1px solid var(--hair);border-radius:16px;padding:20px 22px;margin:14px 0}
.steps{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:14px;margin-top:12px}
.step{background:var(--panel);border:1px solid var(--hair);border-radius:14px;padding:16px}
.step b{color:var(--pink)}
.step h3{font-size:16px;margin:4px 0}
.step p{font-size:14.5px;color:var(--mut)}
details{background:var(--panel);border:1px solid var(--hair);border-radius:12px;padding:14px 18px;margin:10px 0}
summary{cursor:pointer;font-weight:700}
details p{margin-top:8px;color:var(--mut)}
.cta{background:linear-gradient(150deg,#0d3054,#071c31);border:1px solid var(--line);border-radius:18px;padding:26px;text-align:center;margin:36px 0}
.btn{display:inline-block;background:var(--wa);color:#fff;font-weight:800;text-decoration:none;padding:13px 26px;border-radius:999px;margin-top:12px}
.others{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:12px}
.others a{background:var(--panel);border:1px solid var(--hair);border-radius:12px;padding:14px 16px;color:var(--txt);text-decoration:none}
.others a:hover{border-color:var(--pink)}
.others small{display:block;color:var(--mut)}
footer{border-top:1px solid var(--hair);padding:26px 0 40px;color:var(--mut);font-size:14.5px;margin-top:20px}
footer a{color:var(--pink);text-decoration:none}
"""

STEPS = [
 ("01", "الاستشارة", "كتواصلي في واتساب أو رسالة خاصة، كتشرحي حالتك وشنو بغيتي، وكتجاوبك أحلام بالخيارات المناسبة."),
 ("02", "المقاس والقالب", "كناخدو مقاس فمك بدقة ونصايبو القالب — هادي هي القاعدة اللي كتبنى عليها التركيبة كاملة."),
 ("03", "الصناعة في المختبر", "التركيبة كتصايب يدوياً في المختبر بالمادة اللي اخترتي."),
 ("04", "التجربة والمتابعة", "كتجربي التركيبة وكنعدّلو عليها حتى تولي مريحة وطبيعية في فمك — والمتابعة كتبقى مفتوحة."),
]
SHARED_FAQ = [
 ("كيفاش كنحجز موعد؟", "ببساطة: واتساب أو رسالة خاصة في إنستغرام. أوقات العمل: 10:00–13:00 و 15:00–19:30. صيفطي الخدمة اللي بغيتي وغادي تجاوبك بالتفاصيل."),
 ("واش الأسعار ثابتة؟", "الثمن كيتحسب على حساب الحالة والنوع والمادة — داكشي علاش كنفضلو تجاوبك أحلام مباشرة من بعد ما تعرف حالتك، بلا أرقام عامة ما كتنطبقش على كلشي."),
]

PAGES = [
 dict(file="prothese-complete.html", fr="Prothèse complète", ar="التركيبة الكاملة", img="labo/img/img3.webp",
   h1="التركيبة الكاملة في طنجة — طقم أسنان علوي وسفلي",
   meta="Prothèse complète à Tanger chez Labo Ahlam : dentier complet haut et bas, plusieurs types et teintes, choix selon votre goût et la forme de votre visage. Devis par WhatsApp.",
   lede="التركيبة الكاملة هي طقم أسنان كامل — علوي وسفلي — للناس اللي فقدو أسنانهم وبغاو يرجعو ياكلو ويضحكو بثقة. في Labo Ahlam بطنجة كاينين أنواع وألوان مختلفة، والاختيار كيكون على حساب ذوقك وشكل وجهك.",
   points=["طقم كامل علوي وسفلي (أو واحد منهما حسب الحالة)", "أنواع وألوان مختلفة — الاختيار على حساب ذوقك وشكل وجهك", "أحلام كتشرح الأنواع في فيديوهاتها قبل ما تقرري", "الثمن على حساب النوع والمادة — كيتقال لك مباشرة في واتساب"],
   faq=[("واش نقدر نختار لون وشكل الأسنان؟", "نعم — كاينين أنواع وألوان مختلفة، والاختيار كيكون على حساب ذوقك وشكل وجهك، كيف ما كتشرح أحلام في فيديوهاتها."),
        ("واش التركيبة الكاملة كتكون للفك العلوي والسفلي بجوج؟", "التركيبة الكاملة هي طقم كامل علوي وسفلي للناس اللي فقدو أسنانهم — وشنو يناسب حالتك بالضبط كيتحدد في الاستشارة.")]),
 dict(file="prothese-flexible-silicone.html", fr="Flexible · Silicone", ar="التركيبة الجزئية المرنة — سيليكون", img="labo/img/img2.webp",
   h1="التركيبة المرنة بالسيليكون في طنجة — خفيفة وكتلبس مزيان",
   meta="Prothèse partielle flexible en silicone à Tanger (Labo Ahlam) : légère, souple, conçue pour l'usage quotidien — repas chauds et durs, boissons chaudes. Prix selon le cas.",
   lede="التركيبة الجزئية المرنة بالسيليكون هي تركيبة خفيفة ومرنة كتلبس مزيان بلا ما تضغط. أحلام كتشرح في فيديو خاص أنها مصممة تتحمل الاستعمال اليومي: الماكلة السخونة والقاصحة والمشروبات السخونة.",
   points=["خفيفة ومرنة — كتلبس مزيان بلا ما تضغط", "مصممة للاستعمال اليومي العادي", "كتحل بلاص الأسنان الناقصة بلا هيكل معدني", "الثمن على حساب الحالة — الاستشارة في واتساب"],
   faq=[("واش تركيبة السيليكون كتتحمل الماكلة السخونة والقاصحة؟", "على حساب شرح أحلام في فيديوهاتها: التركيبة المرنة مصممة للاستعمال اليومي العادي — الماكلة السخونة، الحوايج القاصحة بحال المكسرات، والمشروبات السخونة بحال القهوة — مع العناية العادية بأي تركيبة."),
        ("واش المرنة كتضغط على اللثة؟", "لا — من مميزاتها أنها خفيفة ومرنة وكتلبس مزيان بلا ما تضغط، وهادشي علاش بزاف كيختاروها للاستعمال اليومي.")]),
 dict(file="prothese-stellite.html", fr="Classique · Stellite", ar="التركيبة الجزئية الكلاسيكية", img="labo/img/img6.webp",
   h1="التركيبة الكلاسيكية Stellite في طنجة — ثبات أكبر بهيكل معدني",
   meta="Prothèse partielle classique à châssis métallique (stellite) à Tanger, chez Labo Ahlam : le choix traditionnel pour une stabilité maximale. Différences avec le flexible expliquées au laboratoire.",
   lede="التركيبة الجزئية الكلاسيكية هي الاختيار التقليدي بهيكل معدني (Stellite) للي كيحتاج ثبات أكبر. في المختبر كنشرحو لك الفرق بين المرنة والكلاسيكية باش تختاري اللي يناسب حالتك.",
   points=["هيكل معدني Stellite لثبات أكبر", "الاختيار التقليدي المجرب من سنين", "في المختبر كيتشرح لك الفرق مع المرنة قبل أي قرار", "الثمن على حساب الحالة والمادة"],
   faq=[("شنو الفرق بين المرنة والكلاسيكية؟", "المرنة خفيفة وبلا هيكل معدني، والكلاسيكية فيها هيكل معدني كيعطي ثبات أكبر. في المختبر كنشرحو لك الفرق بالتفصيل باش تختاري اللي يناسب حالتك."),
        ("شكون كتناسبو الكلاسيكية؟", "الناس اللي كيحتاجو ثبات أكبر في التركيبة — والتحديد المضبوط كيكون من بعد الاستشارة ومعرفة حالتك.")]),
 dict(file="snap-on-smile.html", fr="Snap-on Smile", ar="سناب-أون سمايل", img="labo/img/img1.webp",
   h1="Snap-on Smile في طنجة — ابتسامة جديدة بلا حفر وبلا ألم",
   meta="Snap-on Smile à Tanger chez Labo Ahlam : un sourire amovible qui se pose sur vos dents, sans fraisage et sans douleur. Témoignage client réel : prêt en deux semaines.",
   lede="سناب-أون سمايل هي ابتسامة قابلة للإزالة كتلبس فوق الأسنان وكتبدل الشكل في الحين — بلا حفر وبلا ألم. حل سريع للي بغا يبدل ابتسامتو بلا ما يمس أسنانو الأصلية.",
   points=["قابلة للإزالة — كتلبس وكتحيد فوق أسنانك", "بلا حفر وبلا ألم", "كتبدل شكل الابتسامة في الحين", "شهادة زبون حقيقية على الموقع الرئيسي — حالتو وجدت في أسبوعين"],
   faq=[("واش Snap-on Smile كيحتاج حفر الأسنان؟", "لا — كتلبس فوق الأسنان كما هي، بلا حفر وبلا ألم، وقابلة للإزالة في أي وقت."),
        ("شحال ديال الوقت كتاخد حتى توجد؟", "المدة كتختلف على حساب الحالة — مثلاً شهادة زبون Snap-on Smile وجدت في أسبوعين. الوقت المضبوط كيتقال لك من الأول ملي كتحجزي.")]),
 dict(file="gouttiere.html", fr="Gouttière de contention", ar="الواقي الليلي — Gouttière", img="labo/img/img7.webp",
   h1="الواقي الليلي Gouttière في طنجة — بعد التقويم وضد صرير الأسنان",
   meta="Gouttière de contention et anti-bruxisme fabriquée à Tanger chez Labo Ahlam, sur mesure : protège le résultat de l'orthodontie et les dents contre le grincement nocturne.",
   lede="الواقي الليلي كيتلبس بالليل لجوج أسباب: بعد تقويم الأسنان كيحافظ على النتيجة وكيمنع الأسنان ترجع تتحرك، وبالنسبة للناس اللي كيصرّو أسنانهم وهم ناعسين كيحمي الأسنان من التآكل. كيتصايب هنا في المغرب على مقاس فمك.",
   points=["كيحافظ على نتيجة التقويم — الأسنان ما كترجعش لبلاصتها", "كيحمي من التآكل بسبب الصرير الليلي (Bruxisme)", "كيتصايب في المغرب على مقاس فمك بالضبط", "خفيف وكيتلبس غير بالليل"],
   faq=[("الواقي الليلي علاش كيصلح بالضبط؟", "جوج أسباب: بعد تقويم الأسنان كيحافظ على النتيجة وكيمنع الأسنان ترجع تتحرك، وبالنسبة للناس اللي كيصرّو أسنانهم بالليل كيحمي الأسنان من التآكل."),
        ("واش كيتصايب على مقاسي؟", "نعم — كيتصايب هنا في المغرب على مقاس فمك، من بعد ما كناخدو القالب بدقة في مرحلة المقاس.")]),
 dict(file="couronnes-facettes.html", fr="Couronnes · Facettes", ar="التيجان والوجوه الخزفية", img="labo/img/img5.webp",
   h1="التيجان والوجوه الخزفية في طنجة — Couronnes et Facettes",
   meta="Couronnes et facettes en céramique à Tanger (Labo Ahlam) : rendu naturel, modèles présentés et expliqués en détail au laboratoire avant toute décision.",
   lede="التيجان والوجوه (Facettes) الخزفية بلمسة طبيعية — كيتعرضو ويتشرحو لك بالتفصيل في المختبر قبل أي قرار، باش تشوفي النتيجة المتوقعة بعينيك وتختاري بثقة.",
   points=["سيراميك بلمسة طبيعية", "النماذج كتتعرض وتتشرح لك بالتفصيل في المختبر", "حتى قرار قبل ما تشوفي وتفهمي النتيجة المتوقعة", "الثمن على حساب عدد الأسنان والنوع — في الاستشارة"],
   faq=[("واش النتيجة غادي تبان طبيعية؟", "الهدف هو لمسة طبيعية — وداكشي علاش النماذج كيتعرضو ويتشرحو لك بالتفصيل في المختبر قبل أي قرار، باش تشوفي النتيجة المتوقعة بعينيك."),
        ("كيفاش كنختار بين تاج ووجه خزفي؟", "الفرق كيتشرح لك في المختبر على حساب حالة سنك وشنو بغيتي توصلي ليه — القرار كيتاخد من بعد الشرح، ماشي قبلو.")]),
 dict(file="strass-dentaire.html", fr="Strass dentaire", ar="أحجار الأسنان — Strass", img="labo/img/img4.webp",
   h1="أحجار الأسنان Strass في طنجة — لمعة صغيرة كتبدل الابتسامة",
   meta="Strass dentaire à Tanger chez Labo Ahlam : bijoux dentaires en plusieurs formes et tailles (goutte, petits formats délicats) pour illuminer le sourire.",
   lede="لمعة صغيرة كتبدل الابتسامة: أحجار أسنان بأشكال وأحجام مختلفة — منها شكل الدمعة والأحجام الصغيرة الرقيقة. لمسة تجميلية سريعة كتعطي لابتسامتك طابع خاص.",
   points=["أشكال وأحجام مختلفة — منها شكل الدمعة", "أحجام صغيرة رقيقة للي بغا لمسة خفيفة", "شوفي الفيديو ديالها في قسم إنستغرام في الموقع الرئيسي", "الحجز والاستفسار في واتساب"],
   faq=[("شنو الأشكال المتوفرة؟", "كاينين أشكال وأحجام مختلفة — منها شكل الدمعة والأحجام الصغيرة الرقيقة — والاختيار كيكون على حساب ذوقك."),
        ("كيفاش كنشوف أمثلة قبل ما نقرر؟", "شوفي الفيديو ديال أحجار الأسنان في قسم إنستغرام في الصفحة الرئيسية، أو صيفطي سؤالك في واتساب وغادي تجاوبك أحلام بالصور والشرح.")]),
]

def wa_link(ar_name):
    msg = f"السلام، بغيت معلومات على {ar_name}"
    return f"https://wa.me/{WA}?text=" + urllib.parse.quote(msg)

def build(p):
    faq_all = p["faq"] + SHARED_FAQ
    others = [o for o in PAGES if o["file"] != p["file"]]
    steps_html = "".join(f'<div class="step"><b>{n}</b><h3>{t}</h3><p>{d}</p></div>' for n, t, d in STEPS)
    pts = "".join(f"<li>{x}</li>" for x in p["points"])
    faq_html = "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in faq_all)
    others_html = "".join(f'<a href="{o["file"]}">{o["ar"]}<small>{o["fr"]}</small></a>' for o in others)
    graph = {"@context": "https://schema.org", "@graph": [
      {"@type": "Service", "@id": f"https://laboahlam.com/{p['file']}#service", "name": p["fr"],
       "alternateName": p["ar"], "description": p["lede"], "provider": {"@id": "https://laboahlam.com/#business"},
       "areaServed": {"@type": "City", "name": "Tanger"}, "serviceType": p["fr"]},
      {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Labo Ahlam", "item": "https://laboahlam.com/"},
        {"@type": "ListItem", "position": 2, "name": "الخدمات", "item": "https://laboahlam.com/#services"},
        {"@type": "ListItem", "position": 3, "name": p["ar"], "item": f"https://laboahlam.com/{p['file']}"}]},
      {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq_all]},
    ]}
    html = f"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{p['ar']} في طنجة — Labo Ahlam | {p['fr']}</title>
<meta name="description" content="{p['meta']}">
<meta name="robots" content="noindex,nofollow"><!-- PREVIEW ONLY: remove noindex at laboahlam.com launch -->
<link rel="canonical" href="https://laboahlam.com/{p['file']}">
<meta property="og:title" content="{p['ar']} — Labo Ahlam, Tanger">
<meta property="og:description" content="{p['meta']}">
<meta property="og:image" content="https://laboahlam.com/labo/brand-poster.jpg">
<meta property="og:locale" content="ar_MA">
<style>{CSS}</style>
<script type="application/ld+json">
{json.dumps(graph, ensure_ascii=False, indent=1)}
</script>
</head>
<body>
<header><div class="wrap">
<a class="logo" href="index.html">Labo <span>Ahlam</span></a>
<nav><a href="index.html#services">الخدمات</a><a href="index.html#stars">المشاهير</a><a href="index.html#faq">أسئلة</a><a href="index.html#rdv">الحجز</a></nav>
</div></header>
<main class="wrap">
<p class="crumb"><a href="index.html">الرئيسية</a> ← <a href="index.html#services">الخدمات</a> ← {p['ar']}</p>
<div class="eyebrow">{p['fr']} · Labo Ahlam — Tanger</div>
<h1>{p['h1']}</h1>
<p class="lede">{p['lede']}</p>
<img class="hero-img" src="{p['img']}" alt="{p['ar']} — Labo Ahlam Tanger" loading="lazy">
<h2>شنو كيخلي هاد الخدمة مميزة؟</h2>
<div class="card"><ul>{pts}</ul></div>
<h2>كيفاش كتمشي الخدمة؟</h2>
<div class="steps">{steps_html}</div>
<h2>أسئلة على هاد الخدمة</h2>
{faq_html}
<div class="cta">
<h2 style="margin-top:0">بغيتي تعرفي واش {p['ar']} يناسبك؟</h2>
<p>الثمن كيتحسب على حساب حالتك — صيفطي سؤالك في واتساب وغادي تجاوبك أحلام بالتفاصيل.</p>
<a class="btn" target="_blank" rel="noopener" href="{wa_link(p['ar'])}">اسألي في واتساب — 0609238630</a>
</div>
<h2>خدمات أخرى في المختبر</h2>
<div class="others">{others_html}</div>
</main>
<footer><div class="wrap">
Labo Ahlam — مختبر تركيبات الأسنان، طنجة · واتساب <a href="https://wa.me/{WA}">0609238630</a> · إنستغرام <a href="https://www.instagram.com/labo_ahlam" target="_blank" rel="noopener">@labo_ahlam</a><br>
أوقات العمل: 10:00–13:00 و 15:00–19:30 · الأسعار حسب الحالة
</div></footer>
</body>
</html>
"""
    open(os.path.join(OUT, p["file"]), "w").write(html)
    print("built", p["file"], len(html))

for p in PAGES:
    build(p)
