#!/usr/bin/env python3
"""Labo Ahlam — FR/EN index + espace pages via index-keyed translation maps (verified strings only)."""
import re, os, urllib.parse

OUT = os.path.dirname(os.path.abspath(__file__))
AR_RE = re.compile(r'[\u0600-\u06FF]')

def extract(h):
    texts = set()
    for m in re.findall(r'>([^<]{2,}?)<', h):
        t = m.strip()
        if AR_RE.search(t): texts.add(t)
    for m in re.findall(r'(?:alt|title|content|aria-label|placeholder)="([^"]+)"', h):
        if AR_RE.search(m): texts.add(m)
    for m in re.findall(r"'([^']{3,}?)'", h):
        if AR_RE.search(m): texts.add(m)
    for m in re.findall(r'wa\.me/\d+\?text=([^"&]+)', h):
        texts.add('WA: ' + urllib.parse.unquote(m))
    return sorted(texts)

IDX = extract(open(os.path.join(OUT, 'index.html'), encoding='utf-8').read())
assert len(IDX) == 187, f'index strings changed: {len(IDX)}'
assert IDX[143] == 'قبل' and IDX[89] == 'بعد' and IDX[65] == 'الخدمات' and IDX[83] == 'برينسيسا الطنجاوية'

SKIP = {1, 2, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 134}

FR = {
0:'+228 000 abonnées sur Instagram',
3:"228 000 abonnées apprennent d'elle chaque jour. Ces vidéos viennent directement de sa page :",
4:'Avant / Après', 5:'Espace Dentistes', 6:'Galerie 3D · Du laboratoire', 7:'Galerie 3D · Au cœur du laboratoire',
8:'Labo Ahlam — Ahlam Magri Zerhouni : prothèses dentaires complètes et partielles, silicone flexible, Snap-on Smile, gouttière nocturne et strass dentaire. Réservation par WhatsApp 0609238630.',
9:'Labo Ahlam — Horaires : 10h00 à 13h00 et 15h00 à 19h30',
10:'Labo Ahlam — Laboratoire de prothèses dentaires',
11:'Labo Ahlam — Laboratoire de prothèses dentaires | Tanger',
12:'Labo Ahlam — Laboratoire de prothèses dentaires | Tanger',
13:'Le parcours', 14:'Nos services', 15:'Rendez-vous',
28:'© Labo Ahlam · Site conçu par VERTEX WEB — vertex-web-tanger.onrender.com',
29:'« Merci Ahlam pour ta gentillesse et ton professionnalisme »',
30:"« Je tiens à remercier Ahlam pour le beau sourire qu'elle m'a fait — merci beaucoup »",
31:"« Je tiens à remercier Ahlam pour le beau sourire qu'elle m'a fait »",
32:'Pendant la pose — au laboratoire', 33:'Pendant la pose de la prothèse au laboratoire Labo Ahlam',
34:'Strass dentaire', 35:'Strass dentaire', 36:'Quatre étapes claires — sans surprises.',
37:'Questions', 38:'mille abonnées sur Instagram',
39:'Vous êtes chirurgien-dentiste ? Envoyez vos cas au laboratoire en 1 minute',
40:'Horaires', 41:'Instagram', 42:'Instagram et TikTok :',
43:'Des sourires connus… fabriqués ici', 44:'Sourire',
45:'Le sourire de Prinsisa Tanjawia après Snap-on Smile chez Labo Ahlam',
46:"Le sourire d'un vrai client chez Labo Ahlam",
47:'Un sourire amovible qui se pose sur les dents et change leur forme instantanément — sans fraisage et sans douleur. Regardez un vrai témoignage client dans la section vidéos ci-dessous.',
48:'Réservez votre consultation sur WhatsApp', 49:'Demander ce service →',
50:'Un formulaire de fiche structuré qui arrive directement sur le WhatsApp du laboratoire — type de travail, nombre de dents, teinte et remarques.',
51:'Les questions qui reviennent souvent', 52:'Les formes et tailles disponibles, expliquées par sa voix',
53:'Le choix traditionnel avec châssis métallique (Stellite) pour qui a besoin de plus de stabilité. Au laboratoire, nous vous expliquons la différence entre flexible et classique pour choisir ce qui convient à votre cas.',
54:'Consultation', 55:'Consultation sans engagement', 56:"L'essayage et le suivi",
57:'La transformation complète — en vidéo', 58:'Prothèse partielle classique',
59:'Prothèse partielle flexible — silicone', 60:'Prothèse complète',
61:'La prothèse est fabriquée à la main au laboratoire, dans le matériau que vous avez choisi : flexible, classique ou autre.',
62:'Couronnes et facettes céramique',
63:"Le prix se calcule selon le cas, le type et le matériau — c'est pourquoi nous préférons qu'Ahlam vous réponde directement après avoir connu votre cas, plutôt que des chiffres généraux qui ne s'appliquent pas à tout le monde.",
64:'Réservation', 65:'Services', 66:'Le service… en images 3D',
67:'Réponse pendant les horaires de travail', 68:'Réponse pendant les horaires : 10h00–13h00 · 15h00–19h30',
69:"L'explication et les photos avant toute décision", 70:'Le logo officiel — dentiste LABO AHLAM',
71:'Fabrication au laboratoire', 72:'Horaires : 10h00–13h00 · 15h00–19h30', 73:'Abonnées',
74:"Le délai varie selon le type et le cas — par exemple, le cas Snap-on Smile d'un client était prêt en deux semaines. Le délai exact vous est annoncé dès le départ, à la réservation.",
75:'Célébrités', 76:'Galerie', 77:"L'empreinte et le modèle", 78:'Téléphone / WhatsApp',
79:'La gouttière nocturne (Gouttière), à quoi sert-elle exactement ?', 80:'Gouttière nocturne',
81:"C'est simple : WhatsApp ou message privé sur Instagram. Horaires : 10h00–13h00 et 15h00–19h30. Envoyez le service souhaité et vous recevrez les détails.",
82:'Prinsisa', 83:'Prinsisa Tanjawia', 84:'Prinsisa Tanjawia après Snap-on Smile chez Labo Ahlam',
85:'Prinsisa Tanjawia — après Snap-on Smile', 86:'Prinsisa Tanjawia — photo professionnelle avant la pose chez Labo Ahlam',
87:'Prinsisa Tanjawia — vidéo améliorée chez Labo Ahlam', 88:'Prinsisa — Labo Ahlam',
89:'Après', 90:'Après le traitement chez Labo Ahlam',
91:'Vous voulez venir au laboratoire ?',
92:"Pas de formulaire, pas de complications : ouvrez WhatsApp, envoyez un seul message, et nous confirmons le rendez-vous avec vous et vous envoyons l'adresse là-bas.",
93:'Transformation réelle — avant/après',
94:'Prothèses dentaires terminées, fabriquées par le laboratoire Labo Ahlam',
95:'Prothèses complètes et partielles · silicone flexible · Snap-on Smile · strass dentaire — réservation par WhatsApp.',
96:'Prothèses terminées — fabriquées au laboratoire', 97:'Prothèses terminées — du laboratoire',
98:'Vraie prothèse dentaire complète fabriquée par le laboratoire Labo Ahlam',
99:'Prothèse dentaire flexible fabriquée par le laboratoire Labo Ahlam',
100:'Prothèse dentaire terminée, fabriquée par le laboratoire Labo Ahlam',
101:'Prothèse silicone',
102:"Une prothèse légère et flexible qui se porte bien sans serrer. Ahlam explique dans une vidéo dédiée qu'elle est conçue pour l'usage quotidien : aliments chauds et durs, et boissons chaudes.",
103:'Complète · Flexible silicone · Classique', 104:'Contact', 105:'Contactez-nous sur WhatsApp — en direct',
106:'Couronnes et facettes en céramique au rendu naturel — présentées et expliquées en détail au laboratoire avant toute décision, pour que vous voyiez le résultat attendu de vos propres yeux.',
107:'TikTok',
108:'Faites défiler les photos sur le côté, saisissez celle du centre et tournez-la avec votre doigt — comme si vous touchiez le sourire de votre main.',
109:'Faites défiler les photos sur le côté, saisissez celle du centre et tournez-la avec votre doigt — comme si vous touchiez la prothèse de votre main.',
110:"Deux raisons : après l'orthodontie, elle garde le résultat et empêche les dents de bouger à nouveau ; et pour les personnes qui grincent des dents la nuit, elle protège les dents de l'usure. Elle est fabriquée ici au Maroc, sur mesure pour votre bouche.",
111:'Des cas réels du travail du laboratoire, avant et après. Faites glisser le curseur sur chaque cas pour comparer le résultat.',
112:'Déplacez la carte avec votre doigt — une expérience 3D', 113:'Services spécialisés',
114:'Ouvrir WhatsApp →',
115:"Un client a essayé Snap-on Smile et partagé le résultat en vidéo : il a décrit l'expérience comme excellente, et le sourire était prêt après deux semaines.",
116:"Des clientes viennent chez Ahlam depuis différentes villes — le rendez-vous se confirme sur WhatsApp, et l'adresse vous est envoyée avec la confirmation.",
117:"Visite d'un chanteur célèbre", 118:'Snap-on Smile', 119:'Demandez sur WhatsApp',
120:'Silicone flexible', 121:'Combien de temps faut-il pour que la prothèse soit prête ?',
122:'Logo Labo Ahlam', 123:"Qu'ont dit les clientes ?", 124:'Que fabriquons-nous au laboratoire ?',
125:'Témoignage client', 126:'Témoignage vidéo publié sur Instagram', 127:'Voir les services',
128:'Voyez la différence de vos yeux — faites glisser le curseur', 129:'La page du service en détail →',
130:'De vraies photos… en présentation 3D', 131:'Photo professionnelle avant la pose',
132:'Le plan de travail au laboratoire Labo Ahlam',
133:"Un dentier complet haut et bas pour les personnes qui ont perdu leurs dents. Il existe plusieurs types et teintes, et le choix se fait selon votre goût et la forme de votre visage — comme Ahlam l'explique dans ses vidéos.",
135:"D'après les explications d'Ahlam dans ses vidéos : la prothèse flexible est conçue pour l'usage quotidien normal — aliments chauds, aliments durs comme les fruits secs, et boissons chaudes comme le café — avec l'entretien habituel de toute prothèse.",
136:'Espace Dentistes →', 137:'Au laboratoire', 138:'Au laboratoire — Labo Ahlam',
139:"Vidéo d'introduction — les célébrités de Labo Ahlam avant et après",
140:'Comparer avant/après — cas 1', 141:'Comparer avant/après — cas 2', 142:'Comparer avant/après — cas 3',
143:'Avant', 144:'Avant le traitement chez Labo Ahlam', 145:'Avant de commencer son parcours',
146:'De vrais modèles de travail au laboratoire Labo Ahlam',
147:"Vous essayez la prothèse et nous l'ajustons jusqu'à ce qu'elle soit confortable et naturelle en bouche — et le suivi reste ouvert.",
148:'fabriqué avec précision',
149:'Vous écrivez sur WhatsApp ou en message privé, vous expliquez votre cas et ce que vous voulez, et Ahlam vous répond avec les options adaptées.',
150:'Chaque service expliqué simplement — sans termes compliqués. Choisissez le service et passez directement sur WhatsApp pour demander les détails et le prix selon votre cas.',
151:"Nous prenons l'empreinte de votre bouche avec précision et fabriquons le modèle — c'est la base sur laquelle toute la prothèse est construite.",
152:'Nous préparons votre sourire…',
153:"Elle se porte la nuit après l'orthodontie pour que les dents ne reviennent pas en place, et elle protège aussi les personnes qui grincent des dents en dormant. Fabriquée ici au Maroc, sur mesure pour votre bouche.",
154:'Comment se déroule le service ?', 155:'Comment réserver un rendez-vous ?', 156:'Comment nous travaillons',
157:'Dentistes',
158:"Une petite touche d'éclat qui change le sourire : des strass dentaires en plusieurs formes et tailles — dont la forme goutte et de petits formats délicats. Regardez sa vidéo dans la section Instagram.",
159:'Vous ne savez pas ce qui vous convient ?',
160:"Laboratoire de prothèses dentaires d'Ahlam Magri Zerhouni",
161:"Laboratoire de prothèses dentaires d'Ahlam Magri Zerhouni : prothèses complètes et partielles, silicone flexible, Snap-on Smile, gouttière nocturne et strass dentaire — un service qui vous explique tout avant de commencer,",
162:'Célébrité Instagram — pendant la pose', 163:'Célébrité Instagram — vidéo de sa visite',
164:'Coordonnées', 165:"D'Instagram", 166:'De son Instagram — les explications par sa voix',
167:'Du laboratoire — le plan de travail', 168:'Des commentaires de ses clientes sur Instagram',
169:'Publication & vidéo éducative', 170:"Résultat réel — le sourire d'un client",
171:"Résultat réel — le sourire d'un client chez Labo Ahlam", 172:'Les stars qui nous ont visitées',
173:"C'est normal — la plupart des clientes commencent par une simple question sur WhatsApp, et nous répondons avec des explications et des photos avant tout engagement.",
174:'WhatsApp', 175:'WhatsApp :', 176:'Le mur des célébrités · Ils nous font confiance',
177:'Les prix sont-ils fixes ?', 178:'La prothèse silicone résiste-t-elle aux aliments chauds et durs ?',
179:'Résiste-t-elle à la chaleur et aux aliments durs ? Sa réponse',
180:'Des visages connus ont confié leur sourire au travail du laboratoire — leurs vraies photos et noms.',
181:'et un rendu naturel', 182:'01', 183:'02', 184:'03', 185:'04', 186:'💬 WhatsApp du labo',
}

EN = {
0:'+228K followers on Instagram',
3:'228,000 followers learn from her every day. These videos come straight from her page:',
4:'Before / After', 5:'Dentists Space', 6:'3D Gallery · From the lab', 7:'3D Gallery · Inside the lab',
8:'Labo Ahlam — Ahlam Magri Zerhouni: complete and partial dentures, flexible silicone, Snap-on Smile, night guard and tooth gems. Booking via WhatsApp 0609238630.',
9:'Labo Ahlam — Working hours: 10:00 to 13:00 and 15:00 to 19:30',
10:'Labo Ahlam — Dental prosthesis laboratory',
11:'Labo Ahlam — Dental Prosthesis Laboratory | Tangier',
12:'Labo Ahlam — Dental Prosthesis Laboratory | Tangier',
13:'The process', 14:'Our services', 15:'Booking',
28:'© Labo Ahlam · Website by VERTEX WEB — vertex-web-tanger.onrender.com',
29:'"Thank you Ahlam for your kindness and good manners"',
30:'"I want to thank Ahlam for the beautiful smile she made me — thank you so much"',
31:'"I want to thank Ahlam for the beautiful smile she made me"',
32:'During fitting — at the lab', 33:'Fitting the prosthesis at the Labo Ahlam laboratory',
34:'Tooth gems', 35:'Tooth gems', 36:'Four clear steps — no surprises.',
37:'Questions', 38:'K followers on Instagram',
39:'Are you a dentist? Send your cases to the lab in 1 minute',
40:'Working hours', 41:'Instagram', 42:'Instagram & TikTok:',
43:'Famous smiles… made here', 44:'Smile',
45:"Prinsisa Tanjawia's smile after Snap-on Smile at Labo Ahlam",
46:"A real client's smile at Labo Ahlam",
47:'A removable smile that clips over your teeth and changes their shape instantly — no drilling, no pain. Watch a real client testimonial in the videos section below.',
48:'Book your consultation on WhatsApp', 49:'Ask about this service →',
50:"A structured lab-order form delivered straight to the lab's WhatsApp — work type, number of teeth, shade and notes.",
51:'Frequently asked questions', 52:'The available shapes and sizes, explained in her own voice',
53:'The traditional choice with a metal framework (Stellite) for those who need extra stability. At the lab we explain the difference between flexible and classic so you can choose what suits your case.',
54:'Consultation', 55:'No-obligation consultation', 56:'Fitting & follow-up',
57:'The full transformation — on video', 58:'Classic partial denture',
59:'Flexible partial denture — silicone', 60:'Complete denture',
61:'The prosthesis is handmade in the laboratory, in the material you chose: flexible, classic or other.',
62:'Ceramic crowns & veneers',
63:"The price is calculated per case, type and material — that's why we prefer Ahlam to answer you directly once she knows your case, instead of general numbers that don't apply to everyone.",
64:'Booking', 65:'Services', 66:'The craft… in 3D photos',
67:'Replies during working hours', 68:'Replies during working hours: 10:00–13:00 · 15:00–19:30',
69:'Explanation & photos before any decision', 70:'The official logo — dentiste LABO AHLAM',
71:'Made in the laboratory', 72:'Hours: 10:00–13:00 · 15:00–19:30', 73:'Followers',
74:"Timing varies by type and case — for example, one client's Snap-on Smile case was ready in two weeks. Your exact timeline is confirmed right at booking.",
75:'Celebrities', 76:'Gallery', 77:'Impression & model', 78:'Phone / WhatsApp',
79:'What exactly is a night guard (Gouttière) for?', 80:'Night guard',
81:"Simply: WhatsApp or a private message on Instagram. Hours: 10:00–13:00 and 15:00–19:30. Send the service you want and you'll get the details back.",
82:'Prinsisa', 83:'Prinsisa Tanjawia', 84:'Prinsisa Tanjawia after Snap-on Smile at Labo Ahlam',
85:'Prinsisa Tanjawia — after Snap-on Smile', 86:'Prinsisa Tanjawia — professional photo before fitting at Labo Ahlam',
87:'Prinsisa Tanjawia — enhanced video at Labo Ahlam', 88:'Prinsisa — Labo Ahlam',
89:'After', 90:'After treatment at Labo Ahlam',
91:'Want to visit the lab?',
92:"No forms, no hassle: open WhatsApp, send one message, and we'll confirm your appointment and send you the address there.",
93:'Real transformation — before/after',
94:'Finished dental prostheses made by the Labo Ahlam laboratory',
95:'Complete & partial dentures · flexible silicone · Snap-on Smile · tooth gems — booking via WhatsApp.',
96:'Finished prostheses — made at the lab', 97:'Finished prostheses — from the lab',
98:'A real complete denture made by the Labo Ahlam laboratory',
99:'A flexible dental prosthesis made by the Labo Ahlam laboratory',
100:'A finished dental prosthesis made by the Labo Ahlam laboratory',
101:'Silicone denture',
102:'A light, flexible prosthesis that fits comfortably without squeezing. Ahlam explains in a dedicated video that it is made for everyday use: hot and hard food, and hot drinks.',
103:'Complete · Flexible silicone · Classic', 104:'Contact', 105:'Contact us on WhatsApp — directly',
106:'Ceramic crowns and veneers with a natural finish — shown and explained in detail at the lab before any decision, so you can see the expected result with your own eyes.',
107:'TikTok',
108:'Swipe the photos sideways, grab the one in the middle and rotate it with your finger — as if you were touching the smile with your hand.',
109:'Swipe the photos sideways, grab the one in the middle and rotate it with your finger — as if you were touching the prosthesis with your hand.',
110:'Two reasons: after orthodontics it keeps the result and stops the teeth drifting back, and for people who grind their teeth at night it protects them from wear. It is made here in Morocco, custom-fit to your mouth.',
111:"Real cases from the lab's work, before and after. Drag the slider on each case to compare the result.",
112:'Move the card with your finger — a 3D experience', 113:'Specialised services',
114:'Open WhatsApp →',
115:"A client tried Snap-on Smile and shared the result on video: he described the experience as excellent, and the smile was ready after two weeks.",
116:"Clients come to Ahlam from different cities — appointments are confirmed on WhatsApp, and the address is sent to you with the booking confirmation.",
117:'Visit from a famous singer', 118:'Snap-on Smile', 119:'Ask on WhatsApp',
120:'Flexible silicone', 121:'How long does a prosthesis take to be ready?',
122:'Labo Ahlam logo', 123:'What did clients say?', 124:'What do we make at the lab?',
125:'Client testimonial', 126:'Video testimonial posted on Instagram', 127:'See the services',
128:'See the difference yourself — drag the slider', 129:'Full service page →',
130:'Real photos… in a 3D showcase', 131:'Professional photo before fitting',
132:'The workbench at the Labo Ahlam laboratory',
133:'A full upper & lower denture for people who have lost their teeth. There are several types and shades, and the choice is made to suit your taste and face shape — as Ahlam explains in her videos.',
135:"According to Ahlam's explanations in her videos: the flexible denture is made for normal everyday use — hot food, hard foods like nuts, and hot drinks like coffee — with the usual care any denture needs.",
136:'Dentists Space →', 137:'At the lab', 138:'At the lab — Labo Ahlam',
139:'Intro video — Labo Ahlam celebrities before & after',
140:'Compare before/after — case 1', 141:'Compare before/after — case 2', 142:'Compare before/after — case 3',
143:'Before', 144:'Before treatment at Labo Ahlam', 145:'Before she started her journey',
146:'Real work models at the Labo Ahlam laboratory',
147:"You try the prosthesis and we adjust it until it feels comfortable and natural in your mouth — and follow-up stays open.",
148:'made with precision',
149:'You write on WhatsApp or by private message, explain your case and what you want, and Ahlam replies with the suitable options.',
150:'Every service explained simply — no complicated terms. Pick a service and go straight to WhatsApp to ask for details and the price for your case.',
151:'We take a precise impression of your mouth and make the model — the base on which the whole prosthesis is built.',
152:'Preparing your smile…',
153:"Worn at night after orthodontics so the teeth don't drift back, and it also protects people who grind their teeth in their sleep. Made here in Morocco, custom-fit to your mouth.",
154:'How does the service work?', 155:'How do I book an appointment?', 156:'How we work',
157:'Dentists',
158:'A small sparkle that changes your smile: tooth gems in several shapes and sizes — including the teardrop and small delicate formats. Watch her video in the Instagram section.',
159:'Not sure what suits you?',
160:"Ahlam Magri Zerhouni's dental prosthesis laboratory",
161:"Ahlam Magri Zerhouni's dental prosthesis laboratory: complete and partial dentures, flexible silicone, Snap-on Smile, night guard and tooth gems — a service that explains everything before you start,",
162:'Instagram star — during fitting', 163:'Instagram star — video from his visit',
164:'Contact information', 165:'From Instagram', 166:'From her Instagram — explained in her own voice',
167:'From the lab — the workbench', 168:"From her clients' comments on Instagram",
169:'Educational post & video', 170:"Real result — a client's smile",
171:"Real result — a client's smile at Labo Ahlam", 172:'Stars who visited us',
173:"That's normal — most clients start with a simple question on WhatsApp, and we answer with explanations and photos before any commitment.",
174:'WhatsApp', 175:'WhatsApp:', 176:'The celebrity wall · They trust us',
177:'Are prices fixed?', 178:'Can the silicone denture handle hot and hard food?',
179:'Can it handle heat and hard food? Her answer',
180:"Well-known faces trusted the lab's work for their smiles — their real photos and names.",
181:'and looks natural', 182:'01', 183:'02', 184:'03', 185:'04', 186:'💬 Lab WhatsApp',
}

WA_MAP = {
'السلام، بغيت معلومات على Snap-on Smile': ('Bonjour, je souhaite des informations sur Snap-on Smile', "Hello, I'd like information about Snap-on Smile"),
'السلام، بغيت معلومات على أحجار الأسنان Strass': ('Bonjour, je souhaite des informations sur les strass dentaires', "Hello, I'd like information about tooth gems (Strass)"),
'السلام، بغيت معلومات على التركيبة الكاملة': ('Bonjour, je souhaite des informations sur la prothèse complète', "Hello, I'd like information about the complete denture"),
'السلام، بغيت معلومات على التركيبة الكلاسيكية': ('Bonjour, je souhaite des informations sur la prothèse classique', "Hello, I'd like information about the classic denture"),
'السلام، بغيت معلومات على التركيبة المرنة سيليكون': ('Bonjour, je souhaite des informations sur la prothèse flexible silicone', "Hello, I'd like information about the flexible silicone denture"),
'السلام، بغيت معلومات على التيجان والوجوه الخزفية': ('Bonjour, je souhaite des informations sur les couronnes et facettes céramique', "Hello, I'd like information about ceramic crowns and veneers"),
'السلام، بغيت معلومات على الواقي الليلي Gouttière': ('Bonjour, je souhaite des informations sur la gouttière nocturne', "Hello, I'd like information about the night guard"),
'السلام، بغيت نستشير معاكم': ('Bonjour, je souhaite une consultation', "Hello, I'd like a consultation"),
'السلام، بغيت نستفسر': ('Bonjour, je souhaite me renseigner', 'Hello, I have a question'),
'السلام، بغيت نستفسر على تركيبات الأسنان': ('Bonjour, je souhaite me renseigner sur les prothèses dentaires', "Hello, I'd like to ask about dental prostheses"),
}

BASE = 'https://laboahlam.com'
SW_CSS = '<style>.lang-sw{display:inline-flex;gap:6px;align-items:center}.lang-sw a{border:1px solid #3d6a96;color:#a9c6de;border-radius:999px;padding:7px 13px;font-weight:800;font-size:13px;text-decoration:none}.lang-sw a.on{background:#2f80ed;color:#fff;border-color:#2f80ed}</style>'

def switcher(page, cur):
    def href(lang):
        if lang == cur: return None
        if lang == 'ar': return f'../{page}'
        return f'../{lang}/{page}' if cur != 'ar' else f'{lang}/{page}'
    def selfhref(lang):
        return f'{lang}/{page}' if cur == 'ar' else page
    out = ['<div class="lang-sw">']
    for lang, label in [('ar', 'عربي'), ('fr', 'FR'), ('en', 'EN')]:
        if lang == cur:
            out.append(f'<a class="on" href="{selfhref(lang)}">{label}</a>')
        else:
            out.append(f'<a href="{href(lang)}">{label}</a>')
    out.append('</div>')
    return ''.join(out)

def hreflang_block(page):
    return (f'<link rel="canonical" href="{BASE}/{page}">'
            f'<link rel="alternate" hreflang="ar" href="{BASE}/{page}">'
            f'<link rel="alternate" hreflang="fr" href="{BASE}/fr/{page}">'
            f'<link rel="alternate" hreflang="en" href="{BASE}/en/{page}">'
            f'<link rel="alternate" hreflang="x-default" href="{BASE}/{page}">')

def remove_toggle_script(h):
    pos = h.find("getElementById('langBtn')")
    if pos < 0: return h
    start = h.rfind('<script', 0, pos)
    end = h.find('</script>', pos) + len('</script>')
    return h[:start] + h[end:]

def build_index(lang):
    MAP = FR if lang == 'fr' else EN
    h = open(os.path.join(OUT, 'index.html'), encoding='utf-8').read()
    order = sorted(range(187), key=lambda i: -len(IDX[i]))
    missed = []
    for i in order:
        if i in SKIP: continue
        if IDX[i] in h: h = h.replace(IDX[i], MAP[i])
        else: missed.append(i)
    print(lang, 'index missed strings:', missed)
    for ar_msg, (fr_msg, en_msg) in WA_MAP.items():
        old = urllib.parse.quote(ar_msg)
        new = urllib.parse.quote(fr_msg if lang == 'fr' else en_msg)
        if old in h: h = h.replace(old, new)
    h = h.replace('"labo/', '"../labo/')
    h = h.replace('<html lang="ar" dir="rtl">', f'<html lang="{lang}" dir="ltr">')
    h = remove_toggle_script(h)
    h = h.replace('<button id="langBtn" type="button">FR</button>', switcher('index.html', lang) + SW_CSS)
    h = h.replace('</head>', hreflang_block('index.html') + '</head>', 1)
    h = h.replace('ar_MA', 'fr_FR' if lang == 'fr' else 'en_US')
    d = os.path.join(OUT, lang); os.makedirs(d, exist_ok=True)
    open(os.path.join(d, 'index.html'), 'w', encoding='utf-8').write(h)
    resid = [t for t in extract(h) if not t.startswith('WA:')]
    print(lang, 'index residual AR strings:', len(resid), resid[:8])

def build_espace_fr():
    h = open(os.path.join(OUT, 'espace-dentistes.html'), encoding='utf-8').read()
    reps = {
      'Espace Partenaires · فضاء الأطباء': 'Espace Partenaires',
      'Fiche de laboratoire — طلب عمل للمختبر': 'Fiche de laboratoire',
      'Labo Ahlam — مختبر تركيبات الأسنان، طنجة · واتساب': 'Labo Ahlam — laboratoire de prothèses dentaires, Tanger · WhatsApp',
      'أوقات العمل: 10:00–13:00 و 15:00–19:30': 'Horaires : 10h00–13h00 et 15h00–19h30',
      'الرئيسية': 'Accueil', 'الخدمات': 'Services', 'المشاهير': 'Célébrités', 'الحجز': 'Réservation', 'للأطباء': 'Dentistes',
      '📎 بعد إرسال الاستمارة، صيفط صور القالب/الحالة في نفس محادثة واتساب — هكذا كيوصل الملف كامل للمختبر.': "📎 Après l'envoi du formulaire, envoyez les photos du modèle/du cas dans la même conversation WhatsApp — ainsi le dossier arrive complet au laboratoire.",
    }
    for a, b in reps.items():
        if a in h: h = h.replace(a, b)
        else: print('espace FR miss:', a[:40])
    h = h.replace('"labo/', '"../labo/')
    h = re.sub(r'<html lang="ar" dir="rtl">', '<html lang="fr" dir="ltr">', h)
    h = h.replace('</head>', hreflang_block('espace-dentistes.html') + SW_CSS + '</head>', 1)
    open(os.path.join(OUT, 'fr', 'espace-dentistes.html'), 'w', encoding='utf-8').write(h)
    print('espace FR built; residual AR:', len([t for t in extract(h) if not t.startswith('WA:')]))

def patch_ar_pages():
    # AR index: switcher + drop old toggle + hreflang
    p = os.path.join(OUT, 'index.html'); h = open(p, encoding='utf-8').read()
    if 'lang-sw' not in h:
        h = remove_toggle_script(h)
        h = h.replace('<button id="langBtn" type="button">FR</button>', switcher('index.html', 'ar') + SW_CSS)
        h = h.replace('</head>', hreflang_block('index.html') + '</head>', 1)
        open(p, 'w', encoding='utf-8').write(h); print('AR index patched')
    # AR service pages: switcher + hreflang
    for f in ['prothese-complete.html','prothese-flexible-silicone.html','prothese-stellite.html','snap-on-smile.html','gouttiere.html','couronnes-facettes.html','strass-dentaire.html']:
        p = os.path.join(OUT, f); h = open(p, encoding='utf-8').read()
        if 'lang-sw' in h: continue
        h = h.replace('</nav>', '</nav>' + switcher(f, 'ar') + SW_CSS, 1)
        blocks = (f'<link rel="alternate" hreflang="ar" href="{BASE}/{f}">'
                  f'<link rel="alternate" hreflang="fr" href="{BASE}/fr/{f}">'
                  f'<link rel="alternate" hreflang="en" href="{BASE}/en/{f}">'
                  f'<link rel="alternate" hreflang="x-default" href="{BASE}/{f}">')
        h = h.replace('</head>', blocks + '</head>', 1)
        open(p, 'w', encoding='utf-8').write(h); print('AR service patched', f)

build_index('fr')
build_index('en')
build_espace_fr()
patch_ar_pages()
print('INDEX I18N DONE (espace EN next)')
