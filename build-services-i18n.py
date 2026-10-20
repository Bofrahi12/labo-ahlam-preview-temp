#!/usr/bin/env python3
"""Labo Ahlam — FR + EN service pages. Content = verified site facts only, translated."""
import json, urllib.parse, os, re

OUT = os.path.dirname(os.path.abspath(__file__))
WA = "212609238630"
BASE = "https://laboahlam.com"

# --- reuse AR data (STEPS/SHARED_FAQ/PAGES) from build-services.py without running its build ---
src = open(os.path.join(OUT, "build-services.py"), encoding="utf-8").read()
seg = src[src.index("STEPS ="):src.index("def wa_link")]
ns = {}
exec(seg, ns)
PAGES = ns["PAGES"]

# live hero images per page (patched into the AR pages)
HERO = {}
for p in PAGES:
    h = open(os.path.join(OUT, p["file"]), encoding="utf-8").read()
    HERO[p["file"]] = re.search(r'<img[^>]*src="([^"]+)"', h).group(1)  # labo/svc-*.jpg

CSS = open(os.path.join(OUT, "prothese-complete.html"), encoding="utf-8").read()
CSS = CSS[CSS.index("<style>")+7:CSS.index("</style>")]
CSS += """
.lang-sw{display:flex;gap:6px;align-items:center}
.lang-sw a{border:1px solid var(--line);color:var(--mut);border-radius:999px;padding:5px 12px;font-size:13px;font-weight:700;margin:0!important}
.lang-sw a.on{background:var(--vio);color:#fff;border-color:var(--vio)}
"""

FR = dict(
  nav=["Services", "Célébrités", "Dentistes", "Questions", "Réservation"],
  crumb=["Accueil", "Services"],
  h2points="Qu'est-ce qui rend ce service spécial ?", h2steps="Comment se déroule le service ?",
  h2faq="Questions sur ce service", h2others="Autres services du laboratoire",
  steps=[("01", "Consultation", "Vous écrivez sur WhatsApp ou en message privé, vous expliquez votre cas et ce que vous voulez, et Ahlam vous répond avec les options adaptées."),
         ("02", "Empreinte et modèle", "Nous prenons l'empreinte de votre bouche avec précision et fabriquons le modèle — c'est la base sur laquelle toute la prothèse est construite."),
         ("03", "Fabrication au laboratoire", "La prothèse est fabriquée à la main au laboratoire, dans le matériau que vous avez choisi."),
         ("04", "Essayage et suivi", "Vous essayez la prothèse et nous l'ajustons jusqu'à ce qu'elle soit confortable et naturelle en bouche — et le suivi reste ouvert.")],
  shared=[("Comment réserver un rendez-vous ?", "C'est simple : WhatsApp ou message privé sur Instagram. Horaires : 10h00–13h00 et 15h00–19h30. Envoyez le service souhaité et vous recevrez les détails en réponse."),
          ("Les prix sont-ils fixes ?", "Le prix se calcule selon le cas, le type et le matériau — c'est pourquoi Ahlam préfère vous répondre directement après avoir connu votre cas, plutôt que d'annoncer des chiffres généraux qui ne s'appliquent pas à tout le monde.")],
  cta_h="Vous voulez savoir si {name} vous convient ?",
  cta_p="Le prix se calcule selon votre cas — envoyez votre question sur WhatsApp et Ahlam vous répondra avec les détails.",
  cta_btn="Demander sur WhatsApp — 0609238630",
  foot="Labo Ahlam — laboratoire de prothèses dentaires, Tanger · WhatsApp <a href=\"https://wa.me/212609238630\">0609238630</a> · Instagram <a href=\"https://www.instagram.com/labo_ahlam\" target=\"_blank\" rel=\"noopener\">@labo_ahlam</a><br>Horaires : 10h00–13h00 et 15h00–19h30 · Prix selon le cas",
  wa_msg="Bonjour, je souhaite des informations sur {name}",
)
EN = dict(
  nav=["Services", "Celebrities", "Dentists", "Questions", "Booking"],
  crumb=["Home", "Services"],
  h2points="What makes this service special?", h2steps="How does the service work?",
  h2faq="Questions about this service", h2others="Other services at the lab",
  steps=[("01", "Consultation", "You write on WhatsApp or by private message, explain your case and what you want, and Ahlam replies with the suitable options."),
         ("02", "Impression & model", "We take a precise impression of your mouth and make the model — the base on which the whole prosthesis is built."),
         ("03", "Made in the lab", "The prosthesis is handmade in the laboratory, in the material you chose."),
         ("04", "Fitting & follow-up", "You try the prosthesis and we adjust it until it feels comfortable and natural in your mouth — and follow-up stays open.")],
  shared=[("How do I book an appointment?", "Simply: WhatsApp or a private message on Instagram. Working hours: 10:00–13:00 and 15:00–19:30. Send the service you want and you'll get the details back."),
          ("Are prices fixed?", "The price is calculated per case, type and material — that's why Ahlam prefers to answer you directly once she knows your case, instead of general numbers that don't apply to everyone.")],
  cta_h="Want to know if {name} is right for you?",
  cta_p="The price is calculated for your case — send your question on WhatsApp and Ahlam will reply with the details.",
  cta_btn="Ask on WhatsApp — 0609238630",
  foot="Labo Ahlam — dental prosthesis laboratory, Tangier · WhatsApp <a href=\"https://wa.me/212609238630\">0609238630</a> · Instagram <a href=\"https://www.instagram.com/labo_ahlam\" target=\"_blank\" rel=\"noopener\">@labo_ahlam</a><br>Working hours: 10:00–13:00 and 15:00–19:30 · Prices per case",
  wa_msg="Hello, I'd like information about {name}",
)

CONTENT = {
"prothese-complete.html": dict(
  fr_name="Prothèse complète",
  fr_h1="Prothèse complète à Tanger — dentier complet haut et bas",
  fr_lede="La prothèse complète est un dentier complet — haut et bas — pour les personnes qui ont perdu leurs dents et veulent remanger et sourire en confiance. Chez Labo Ahlam à Tanger, il existe plusieurs types et teintes, et le choix se fait selon votre goût et la forme de votre visage.",
  fr_points=["Dentier complet haut et bas (ou l'un des deux selon le cas)", "Plusieurs types et teintes — le choix selon votre goût et la forme de votre visage", "Ahlam explique les types dans ses vidéos avant que vous décidiez", "Prix selon le type et le matériau — annoncé directement sur WhatsApp"],
  fr_faq=[("Puis-je choisir la couleur et la forme des dents ?", "Oui — il existe plusieurs types et teintes, et le choix se fait selon votre goût et la forme de votre visage, comme Ahlam l'explique dans ses vidéos."),
          ("La prothèse complète couvre-t-elle les deux mâchoires ?", "La prothèse complète est un dentier complet haut et bas pour les personnes qui ont perdu leurs dents — ce qui convient exactement à votre cas se détermine lors de la consultation.")],
  en_name="Complete denture",
  en_h1="Complete denture in Tangier — full upper & lower denture",
  en_meta="Complete denture in Tangier at Labo Ahlam: full upper and lower denture, several types and shades, chosen to suit your taste and face shape. Quote on WhatsApp.",
  en_lede="A complete denture is a full set of teeth — upper and lower — for people who have lost their teeth and want to eat and smile with confidence again. At Labo Ahlam in Tangier there are several types and shades, and the choice is made to suit your taste and the shape of your face.",
  en_points=["Full upper & lower denture (or one of them, depending on the case)", "Several types and shades — chosen to suit your taste and face shape", "Ahlam explains the types in her videos before you decide", "Price depends on type and material — told to you directly on WhatsApp"],
  en_faq=[("Can I choose the colour and shape of the teeth?", "Yes — there are several types and shades, and the choice is made to suit your taste and face shape, as Ahlam explains in her videos."),
          ("Does a complete denture cover both jaws?", "A complete denture is a full upper and lower set for people who have lost their teeth — exactly what suits your case is decided at the consultation.")]),
"prothese-flexible-silicone.html": dict(
  fr_name="Prothèse flexible · Silicone",
  fr_h1="Prothèse flexible en silicone à Tanger — légère et confortable",
  fr_lede="La prothèse partielle flexible en silicone est une prothèse légère et souple qui se porte bien sans serrer. Ahlam explique dans une vidéo dédiée qu'elle est conçue pour l'usage quotidien : aliments chauds et durs, boissons chaudes.",
  fr_points=["Légère et flexible — se porte bien sans serrer", "Conçue pour un usage quotidien normal", "Remplace les dents manquantes sans châssis métallique", "Prix selon le cas — consultation sur WhatsApp"],
  fr_faq=[("La prothèse silicone résiste-t-elle aux aliments chauds et durs ?", "D'après les explications d'Ahlam dans ses vidéos : la prothèse flexible est conçue pour l'usage quotidien normal — aliments chauds, aliments durs comme les fruits secs, et boissons chaudes comme le café — avec l'entretien habituel de toute prothèse."),
          ("La flexible serre-t-elle les gencives ?", "Non — l'un de ses avantages est d'être légère et souple et de se porter sans serrer, c'est pourquoi beaucoup la choisissent pour le quotidien.")],
  en_name="Flexible silicone partial denture",
  en_h1="Flexible silicone denture in Tangier — light & comfortable",
  en_meta="Flexible silicone partial denture in Tangier (Labo Ahlam): light, flexible, made for everyday use — hot and hard food, hot drinks. Price per case.",
  en_lede="The flexible silicone partial denture is a light, supple prosthesis that fits comfortably without squeezing. Ahlam explains in a dedicated video that it is made for everyday use: hot and hard food, and hot drinks.",
  en_points=["Light & flexible — fits comfortably without squeezing", "Made for normal everyday use", "Replaces missing teeth with no metal framework", "Price per case — consultation on WhatsApp"],
  en_faq=[("Can the silicone denture handle hot and hard food?", "According to Ahlam's explanations in her videos: the flexible denture is made for normal everyday use — hot food, hard foods like nuts, and hot drinks like coffee — with the usual care any denture needs."),
          ("Does the flexible one press on the gums?", "No — one of its advantages is being light and flexible and fitting without pressure, which is why many people choose it for daily life.")]),
"prothese-stellite.html": dict(
  fr_name="Prothèse classique · Stellite",
  fr_h1="Prothèse classique Stellite à Tanger — stabilité avec châssis métallique",
  fr_lede="La prothèse partielle classique est le choix traditionnel avec un châssis métallique (Stellite) pour celles et ceux qui ont besoin de plus de stabilité. Au laboratoire, nous vous expliquons la différence entre la flexible et la classique pour que vous choisissiez ce qui convient à votre cas.",
  fr_points=["Châssis métallique Stellite pour plus de stabilité", "Le choix traditionnel, éprouvé depuis des années", "Au laboratoire, la différence avec la flexible vous est expliquée avant toute décision", "Prix selon le cas et le matériau"],
  fr_faq=[("Quelle est la différence entre flexible et classique ?", "La flexible est légère et sans châssis métallique ; la classique a un châssis métallique qui donne plus de stabilité. Au laboratoire, nous vous expliquons la différence en détail pour que vous choisissiez ce qui convient à votre cas."),
          ("À qui convient la classique ?", "Aux personnes qui ont besoin de plus de stabilité dans leur prothèse — le choix précis se fait après la consultation et la connaissance de votre cas.")],
  en_name="Classic stellite partial denture",
  en_h1="Classic Stellite denture in Tangier — stability with a metal frame",
  en_meta="Classic partial denture with a metal framework (stellite) in Tangier, at Labo Ahlam: the traditional choice for maximum stability. Differences with flexible explained at the lab.",
  en_lede="The classic partial denture is the traditional choice with a metal framework (Stellite) for people who need extra stability. At the lab we explain the difference between flexible and classic so you can choose what suits your case.",
  en_points=["Stellite metal framework for extra stability", "The traditional choice, proven over years", "At the lab, the difference with flexible is explained before any decision", "Price per case and material"],
  en_faq=[("What's the difference between flexible and classic?", "Flexible is light with no metal frame; classic has a metal framework that gives more stability. At the lab we explain the difference in detail so you can choose what suits your case."),
          ("Who is the classic one for?", "People who need more stability in their denture — the exact choice is made after the consultation, once we know your case.")]),
"snap-on-smile.html": dict(
  fr_name="Snap-on Smile",
  fr_h1="Snap-on Smile à Tanger — un nouveau sourire sans fraisage ni douleur",
  fr_lede="Snap-on Smile est un sourire amovible qui se pose sur vos dents et change leur forme instantanément — sans fraisage et sans douleur. Une solution rapide pour qui veut changer son sourire sans toucher à ses dents d'origine.",
  fr_points=["Amovible — se pose et se retire sur vos dents", "Sans fraisage et sans douleur", "Change la forme du sourire instantanément", "Témoignage client réel sur le site principal — son cas était prêt en deux semaines"],
  fr_faq=[("Snap-on Smile nécessite-t-il de fraiser les dents ?", "Non — il se pose sur les dents telles qu'elles sont, sans fraisage et sans douleur, et il est amovible à tout moment."),
          ("Combien de temps faut-il pour qu'il soit prêt ?", "Le délai varie selon le cas — par exemple, le cas d'un client Snap-on Smile était prêt en deux semaines. Le délai exact vous est annoncé dès le départ, à la réservation.")],
  en_name="Snap-on Smile",
  en_h1="Snap-on Smile in Tangier — a new smile, no drilling, no pain",
  en_meta="Snap-on Smile in Tangier at Labo Ahlam: a removable smile that clips over your teeth — no drilling, no pain. Real client testimonial: ready in two weeks.",
  en_lede="Snap-on Smile is a removable smile that clips over your teeth and changes their shape instantly — no drilling and no pain. A quick solution for anyone who wants a new smile without touching their original teeth.",
  en_points=["Removable — clips on and off over your teeth", "No drilling, no pain", "Changes the shape of your smile instantly", "Real client testimonial on the main site — his case was ready in two weeks"],
  en_faq=[("Does Snap-on Smile require drilling the teeth?", "No — it clips over your teeth as they are, with no drilling and no pain, and it's removable at any time."),
          ("How long does it take to be ready?", "Timing varies by case — for example, one Snap-on Smile client's case was ready in two weeks. Your exact timeline is confirmed right at booking.")]),
"gouttiere.html": dict(
  fr_name="Gouttière de contention",
  fr_h1="Gouttière nocturne à Tanger — après orthodontie et contre le bruxisme",
  fr_lede="La gouttière nocturne se porte la nuit pour deux raisons : après un traitement d'orthodontie, elle garde le résultat et empêche les dents de bouger à nouveau ; et pour les personnes qui grincent des dents en dormant, elle protège les dents de l'usure. Elle est fabriquée ici au Maroc, sur mesure pour votre bouche.",
  fr_points=["Garde le résultat de l'orthodontie — les dents ne reviennent pas en place", "Protège contre l'usure due au grincement nocturne (bruxisme)", "Fabriquée au Maroc, exactement sur mesure pour votre bouche", "Légère, se porte uniquement la nuit"],
  fr_faq=[("À quoi sert exactement la gouttière nocturne ?", "Deux raisons : après l'orthodontie, elle garde le résultat et empêche les dents de bouger ; et pour les personnes qui grincent des dents la nuit, elle protège les dents de l'usure."),
          ("Est-elle faite sur mesure ?", "Oui — elle est fabriquée ici au Maroc sur mesure pour votre bouche, après une prise d'empreinte précise à l'étape du modèle.")],
  en_name="Night guard (retainer & bruxism)",
  en_h1="Night guard in Tangier — after braces & against teeth grinding",
  en_meta="Retainer and anti-bruxism night guard made in Tangier at Labo Ahlam, custom-fit: protects your orthodontic result and your teeth from night-time grinding.",
  en_lede="A night guard is worn at night for two reasons: after orthodontic treatment it keeps the result and stops the teeth from drifting back, and for people who grind their teeth in their sleep it protects the teeth from wear. It is made here in Morocco, custom-fit to your mouth.",
  en_points=["Keeps your orthodontic result — teeth don't drift back", "Protects against wear from night grinding (bruxism)", "Made in Morocco, exactly to the measure of your mouth", "Lightweight — worn only at night"],
  en_faq=[("What exactly is a night guard for?", "Two reasons: after orthodontics it keeps the result and stops the teeth moving back, and for people who grind their teeth at night it protects them from wear."),
          ("Is it custom-made for me?", "Yes — it is made here in Morocco to the exact measure of your mouth, after a precise impression at the model stage.")]),
"couronnes-facettes.html": dict(
  fr_name="Couronnes · Facettes céramique",
  fr_h1="Couronnes et facettes céramique à Tanger",
  fr_lede="Les couronnes et facettes en céramique, au rendu naturel — les modèles vous sont présentés et expliqués en détail au laboratoire avant toute décision, pour que vous voyiez le résultat attendu de vos propres yeux et choisissiez en confiance.",
  fr_points=["Céramique au rendu naturel", "Les modèles vous sont présentés et expliqués en détail au laboratoire", "Aucune décision avant d'avoir vu et compris le résultat attendu", "Prix selon le nombre de dents et le type — à la consultation"],
  fr_faq=[("Le résultat aura-t-il l'air naturel ?", "L'objectif est un rendu naturel — c'est pourquoi les modèles vous sont présentés et expliqués en détail au laboratoire avant toute décision, pour que vous voyiez le résultat attendu de vos propres yeux."),
          ("Comment choisir entre couronne et facette ?", "La différence vous est expliquée au laboratoire selon l'état de votre dent et ce que vous voulez obtenir — la décision se prend après l'explication, pas avant.")],
  en_name="Ceramic crowns & veneers",
  en_h1="Ceramic crowns & veneers in Tangier",
  en_meta="Ceramic crowns and veneers in Tangier (Labo Ahlam): a natural-looking finish, with models shown and explained in detail at the lab before any decision.",
  en_lede="Ceramic crowns and veneers with a natural finish — the models are shown and explained to you in detail at the laboratory before any decision, so you can see the expected result with your own eyes and choose with confidence.",
  en_points=["Ceramic with a natural-looking finish", "Models are shown and explained to you in detail at the lab", "No decision before you've seen and understood the expected result", "Price depends on the number of teeth and the type — at the consultation"],
  en_faq=[("Will the result look natural?", "The goal is a natural finish — that's why the models are shown and explained to you in detail at the lab before any decision, so you can see the expected result with your own eyes."),
          ("How do I choose between a crown and a veneer?", "The difference is explained at the lab based on your tooth's condition and what you want to achieve — the decision comes after the explanation, not before.")]),
"strass-dentaire.html": dict(
  fr_name="Strass dentaire",
  fr_h1="Strass dentaire à Tanger — une touche d'éclat qui change le sourire",
  fr_lede="Une petite touche d'éclat qui change le sourire : des bijoux dentaires en plusieurs formes et tailles — dont la forme goutte et de petits formats délicats. Une touche esthétique rapide qui donne à votre sourire un caractère unique.",
  fr_points=["Plusieurs formes et tailles — dont la forme goutte", "Petits formats délicats pour une touche légère", "Regardez sa vidéo dans la section Instagram du site principal", "Réservation et questions sur WhatsApp"],
  fr_faq=[("Quelles formes sont disponibles ?", "Il existe plusieurs formes et tailles — dont la forme goutte et de petits formats délicats — et le choix se fait selon votre goût."),
          ("Comment voir des exemples avant de décider ?", "Regardez la vidéo des strass dentaires dans la section Instagram de la page d'accueil, ou envoyez votre question sur WhatsApp et Ahlam vous répondra avec des photos et des explications.")],
  en_name="Dental strass (tooth gems)",
  en_h1="Tooth gems in Tangier — a small sparkle that changes your smile",
  en_meta="Tooth gems in Tangier at Labo Ahlam: dental strass in several shapes and sizes (teardrop, small delicate formats) to light up your smile.",
  en_lede="A small sparkle that changes your smile: dental gems in several shapes and sizes — including a teardrop shape and small, delicate formats. A quick beauty touch that gives your smile its own character.",
  en_points=["Several shapes and sizes — including the teardrop", "Small, delicate formats for a light touch", "Watch her video in the Instagram section of the main site", "Booking & questions on WhatsApp"],
  en_faq=[("What shapes are available?", "There are several shapes and sizes — including the teardrop and small delicate formats — and the choice is up to your taste."),
          ("How can I see examples before deciding?", "Watch the tooth-gems video in the Instagram section of the home page, or send your question on WhatsApp and Ahlam will reply with photos and explanations.")]),
}

def build(p, lang):
    L = FR if lang == "fr" else EN
    C = CONTENT[p["file"]]
    name = C[f"{lang}_name"]
    meta = p["meta"] if lang == "fr" else C["en_meta"]
    lede = C[f"{lang}_lede"]
    faq_all = C[f"{lang}_faq"] + L["shared"]
    others = [o for o in PAGES if o["file"] != p["file"]]
    steps_html = "".join(f'<div class="step"><b>{n}</b><h3>{t}</h3><p>{d}</p></div>' for n, t, d in L["steps"])
    pts = "".join(f"<li>{x}</li>" for x in C[f"{lang}_points"])
    faq_html = "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in faq_all)
    def oname(o): return CONTENT[o["file"]][f"{lang}_name"]
    others_html = "".join(f'<a href="{o["file"]}">{oname(o)}<small>{o["fr"] if lang=="fr" else o["ar"]}</small></a>' for o in others)
    wa = "https://wa.me/" + WA + "?text=" + urllib.parse.quote(L["wa_msg"].format(name=name))
    pre = "" if lang == "fr" else "../fr/"
    sw = (f'<div class="lang-sw"><a href="../{p["file"]}">عربي</a>'
          f'<a href="{"" if lang=="fr" else "../fr/"}{p["file"]}"{" class=\"on\"" if lang=="fr" else ""}>FR</a>'
          f'<a href="{"" if lang=="en" else "../en/"}{p["file"]}"{" class=\"on\"" if lang=="en" else ""}>EN</a></div>')
    graph = {"@context": "https://schema.org", "@graph": [
      {"@type": "Service", "@id": f"{BASE}/{lang}/{p['file']}#service", "name": name,
       "description": lede, "provider": {"@id": f"{BASE}/#business"},
       "areaServed": {"@type": "City", "name": "Tanger"}, "serviceType": name},
      {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Labo Ahlam", "item": f"{BASE}/{lang}/"},
        {"@type": "ListItem", "position": 2, "name": L["crumb"][1], "item": f"{BASE}/{lang}/#services"},
        {"@type": "ListItem", "position": 3, "name": name, "item": f"{BASE}/{lang}/{p['file']}"}]},
      {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq_all]},
    ]}
    title = f"{name} — Labo Ahlam, Tanger" if lang == "en" else f"{name} à Tanger — Labo Ahlam"
    html = f"""<!DOCTYPE html>
<html lang="{lang}" dir="ltr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{meta}">
<meta name="robots" content="noindex,nofollow"><!-- PREVIEW ONLY -->
<link rel="canonical" href="{BASE}/{lang}/{p['file']}">
<link rel="alternate" hreflang="ar" href="{BASE}/{p['file']}">
<link rel="alternate" hreflang="fr" href="{BASE}/fr/{p['file']}">
<link rel="alternate" hreflang="en" href="{BASE}/en/{p['file']}">
<link rel="alternate" hreflang="x-default" href="{BASE}/{p['file']}">
<meta property="og:title" content="{name} — Labo Ahlam, Tanger">
<meta property="og:description" content="{meta}">
<meta property="og:image" content="{BASE}/labo/brand-poster.jpg">
<meta property="og:locale" content="{'fr_FR' if lang=='fr' else 'en_US'}">
<style>{CSS}</style>
<script type="application/ld+json">
{json.dumps(graph, ensure_ascii=False, indent=1)}
</script>
</head>
<body>
<header><div class="wrap">
<a class="logo" href="index.html">Labo <span>Ahlam</span></a>
<nav><a href="index.html#services">{L['nav'][0]}</a><a href="index.html#stars">{L['nav'][1]}</a><a href="espace-dentistes.html">{L['nav'][2]}</a><a href="index.html#faq">{L['nav'][3]}</a><a href="index.html#rdv">{L['nav'][4]}</a></nav>
{sw}
</div></header>
<main class="wrap">
<p class="crumb"><a href="index.html">{L['crumb'][0]}</a> ← <a href="index.html#services">{L['crumb'][1]}</a> ← {name}</p>
<div class="eyebrow">{name} · Labo Ahlam — Tanger</div>
<h1>{C[f'{lang}_h1']}</h1>
<p class="lede">{lede}</p>
<img class="hero-img" src="../{HERO[p['file']]}" alt="{name} — Labo Ahlam Tanger" loading="lazy">
<h2>{L['h2points']}</h2>
<div class="card"><ul>{pts}</ul></div>
<h2>{L['h2steps']}</h2>
<div class="steps">{steps_html}</div>
<h2>{L['h2faq']}</h2>
{faq_html}
<div class="cta">
<h2 style="margin-top:0">{L['cta_h'].format(name=name)}</h2>
<p>{L['cta_p']}</p>
<a class="btn" target="_blank" rel="noopener" href="{wa}">{L['cta_btn']}</a>
</div>
<h2>{L['h2others']}</h2>
<div class="others">{others_html}</div>
</main>
<footer><div class="wrap">
{L['foot']}
</div></footer>
</body>
</html>
"""
    d = os.path.join(OUT, lang)
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, p["file"]), "w", encoding="utf-8").write(html)
    print("built", lang, p["file"], len(html))

for p in PAGES:
    build(p, "fr")
    build(p, "en")
print("SERVICES I18N DONE")
