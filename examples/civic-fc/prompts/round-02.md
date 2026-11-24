# Interior Honda Civic Sedan 2020 – runda 2 de corecturi

Continuăm pe interiorul refăcut data trecută. Mai sunt 5 probleme majore, în ordinea de mai jos. Ceasurile de bord (punctul 3) sunt **prioritatea principală**: acolo vreau cel mai mult realism.

## 0. Cum lucrezi (obligatoriu, la fel ca data trecută)

1. Descarcă referințele de mai jos în `refs/v2/` (`curl -L -o ...`) și **deschide fiecare imagine cu Read** înainte să lucrezi la componenta respectivă. Nu lucra din memorie.
2. Lucrează **pe rând** la cele 5 puncte. După fiecare punct:
   - fă un render din Blender **din poziția camerei șoferului**, plus un close-up al zonei;
   - pune render-ul **lângă referința reală** într-o singură imagine, `renders/v2/compare_<punct>.png`, deschide-o cu Read și scrie-mi 3 diferențe rămase; corectează-le înainte să treci mai departe.
3. Problemele se văd **în joc**, nu doar în Blender. După fiecare punct, exportă și verifică în engine. Dacă poți, fă și un screenshot din joc. Ce arată bine în Blender și urât în joc înseamnă de obicei: normale, triangulare, fețe cu o singură parte (backface culling), shadow bias sau lipsa reflection probe-urilor.
4. Nu șterge nimic definitiv: piesele vechi le muți în colecția `OLD_v1` (ascunsă).

## 1. Referințe

**Ceasuri de bord (cele mai importante – descarcă-le pe toate)**
- Cluster RS 1.5 Turbo, **în km/h și °C** (cea mai bună pentru unitățile noastre): https://d1hv7ee95zft1i.cloudfront.net/custom/blog-post-photo/gallery/2020-honda-civic-rs-turbo-digital-gauge-cluster-606a9d556a814.jpg
- Cluster sedan 2020, temă roșie: https://cars.usnews.com/static/images/Auto/izmo/i159614407/2020_honda_civic_sedan_instrumentcluster.jpg
- Cluster sedan 2020, temă albastră (LX), foarte clar: https://www.motortrend.com/uploads/sites/10/2020/08/2020-honda-civic-lx-sedan-instrument-cluster.png
- Cluster Si sedan 2020: https://cars.usnews.com/static/images/Auto/izmo/i159614244/2020_honda_civic_si_sedan_instrumentcluster.jpg
- Galerie hi-res (2560×1440) cu cadre de cluster, de deschis în browser: https://www.caricos.com/cars/h/honda/2020_honda_civic_sedan/

**Bordul pe partea pasagerului**
- Bord complet, vedere frontală (aici se vede foarte bine banda de pe partea pasagerului): https://www.motortrend.com/uploads/sites/10/2020/08/2020-honda-civic-lx-sedan-dashboard.png
- Bord Si sedan, manuală: https://cars.usnews.com/pics/size/0x0/images/Auto/izmo/i159614244/2020_honda_civic_si_sedan_dashboard.jpg
- Torpedo / partea pasagerului: https://imgcdn.zigwheels.ph/large/gallery/interior/11/1615/honda-civic-glove-box-949559.jpg

**Volan**
- Volan RS Turbo, close-up: https://d1hv7ee95zft1i.cloudfront.net/custom/blog-post-photo/gallery/2020-honda-civic-rs-turbo-steering-wheel-606a9cfe27af6.jpg
- Volan sedan 2020 (frontal): https://cars.usnews.com/pics/size/0x0/images/Auto/izmo/i159614407/2020_honda_civic_sedan_steeringwheel.jpg
- Comenzi pe volan, close-up: https://s3.amazonaws.com/di-honda-enrollment/2020-civic-si-sedan/section-images/18-steering-wheel-mounted-controls-2020-civic-si-sedan.jpg

**Montant A / colțul oglinzii**
- Montanții se văd în cele două poze de bord de mai sus (MotorTrend și U.S. News Si).
- Triunghiul de lângă oglindă (cu tweeter-ul), doar ca formă: https://down-my.img.susercontent.com/file/92b0d16600095cd5559f59acb93e95a8. Inelul colorat din poză e accesoriu aftermarket, nu-l copia; originalul e o grilă rotundă neagră, simplă.

---

## 2. Problemele, în ordine

### 2.1 Montantul A (și colțul ușii) – geometrie zimțată, nerealistă
**Ce se vede acum:** pe marginile montantului A apar „dinți” negri ascuțiți (ca un fierăstrău), muchii zimțate și găuri prin care se vede exteriorul. Aceleași cioburi negre zimțate apar și pe **partea de sus a bordului**, lângă parbriz. Tweeter-ul e o semisferă albă, iar mânerul ușii e alb mat.

**Diagnostic (verifică în ordinea asta):**
1. **N-gon-uri concave** triangulate greșit la export: asta produce exact „dinții” de fierăstrău. Adaugă un modifier **Triangulate** (Beauty / Beauty) înainte de export, sau refă topologia cu quad-uri curate.
2. **Normale** inversate sau inconsistente: Select All → *Recalculate Outside*. Activează *Face Orientation* și verifică să nu rămână nimic roșu spre cameră.
3. **Vertecși dublați / fețe de arie zero / non-manifold**: *Merge by Distance* (0.0001), *Select → All by Trait → Non Manifold*, *Degenerate Dissolve*.
4. **Fețe suprapuse coplanare** (z-fighting) între bord și parbriz/caroserie: elimină dublura sau distanțează-le cu ≥2 mm.
5. **Grosime**: montantul e acum o simplă suprafață. Fă-l **coajă închisă** (Solidify 3–4 mm, cu rim), ca backface culling-ul din joc să nu lase găuri.
6. Dacă artefactele de pe bord dispar în Blender și rămân doar în joc, e **shadow acne**: crește shadow bias / normal bias în engine sau fă geometria bordului mai groasă.

**Cum trebuie să arate (vezi pozele de bord):**
- Ornamentul montantului A e o **piesă netedă, continuă**, cu secțiune în „D” rotunjit, mai lată jos (~90 mm) și mai îngustă sus (~55 mm), care urcă lin în plafon. Material textil sau plastic **negru mat** cu granulație fină, fără muchii ascuțite. Are bevel/fillet pe ambele margini, iar spre parbriz și spre geamul lateral lasă un rost uniform de ~2–3 mm.
- **Triunghiul din colțul ușii** (în spatele oglinzii exterioare): panou din plastic negru mat, plin, cu un **tweeter rotund** de ~55 mm. Tweeter-ul are o **grilă neagră perforată**, aproape la nivelul panoului, și un inel subțire în jur. Fără semisferă albă.
- **Mânerul interior al ușii**: satin chrome (Metallic 1, roughness ~0.3), în cavitatea lui neagră. Nu alb mat.
- **Rama superioară a ușii** se îmbină curat cu montantul, fără spații.

### 2.2 Emblema H – a rămas un contur urât în jurul/sub siglă
**Ce se vede acum:** în jurul H-ului se vede un **halou / contur gri** (probabil rămășița emblemei vechi sau baza ei, sub cea nouă, sau un AO copt greșit). În plus, H-ul arată **alb mat**, nu cromat.

**Ce faci:**
1. Izolează emblema (Local View) și **șterge orice mesh vechi** de sub ea: contur vechi, placă, decal. Verifică în Outliner să nu existe două embleme suprapuse.
2. Între H și conturul cromat, fundalul trebuie să fie **negru lucios (piano black)**, ușor adâncit. Nimic gri, nicio umbră pictată în textură.
3. Emblema stă într-un **lăcaș fin** în capacul airbag-ului, cu rost de ~0.5 mm, nu lipită deasupra cu o margine vizibilă.
4. **Cromul trebuie să reflecte și în joc**: pune un **reflection probe** în habitaclu (sau folosește un cubemap) și verifică metallic=1 / roughness 0.08–0.15 după export. Fără reflexii, cromul arată exact ca acum: alb sau gri plat.
5. Textul „SRS AIRBAG” de sub emblemă e acum prea mare și prea contrastant. În realitate e **mic (~4 mm înălțime), embosat în același material**, abia vizibil. Fă-l din normal map, fără culoare diferită.

### 2.3 Ceasurile de bord – refacere completă, cât mai realist (PRIORITATE)
**Ce se vede acum:** un cerc generic, centrat, cu „0” și „A1” portocalii și o zonă roșie. Panourile laterale au linii punctate fără legătură cu Honda. Nu seamănă deloc cu un Civic.

Deschide toate cele 4 poze de cluster și **reprodu fidel layout-ul**. Cel mai important e clusterul RS (km/h, °C).

**Structura fizică (3 zone, sub o streașină adâncă):**
- **Streașina (hood)**: plastic negru soft-touch, adâncă (~60–70 mm în față), cu buza curbată. Două **„stâlpișoare” în V** despart ecranul central de cele două module laterale. Interiorul streșinii e **negru mat**, fără reflexii.
- Pe buza superioară, deasupra ecranului central: **două benzi subțiri luminoase/argintii orizontale** (se văd clar în poze).
- **Ecranul central**: TFT dreptunghiular, mai lat decât înalt (~raport 1.6:1), ușor încastrat. Sub un **geam** cu reflexie discretă (roughness ~0.05, opacitate mică) și negru adânc (#020305) acolo unde nu e grafică.
- **Două module laterale** (stânga și dreapta), **înclinate ~25–30° spre șofer**, fiecare cu un **arc argintiu satinat** fizic (bezel curbat) pe muchia dinspre centru.

**Ecranul central – grafica (desenează-o cât mai fidel pozelor):**
- **Turometru** în formă de potcoavă (~250°), deschis în partea de jos. Scala **0–8** (×1000 r/min), cifre albe mici în interiorul arcului, cu textul „x1000r/min” mic sub cifra 4.
  - Un **inel exterior subțire** alb/argintiu și, sub el, **bara de turație** care se umple de la 0 până la turația curentă. Asta ține loc de ac; nu există ac fizic.
  - **Zona roșie** de la ~6.5 la 8, marcată pe scală.
  - Temă: **roșie** (ca la RS / Sport: bară roșu-portocaliu, gradații albe) ca variantă implicită. Fă materialul ușor de comutat și pe **tema albastră** (ca la LX: bară albastru-deschis spre alb). Ambele sunt în poze.
- **Viteza**: cifre **albe, mari, condensate**, sus în centru, imediat sub cifra 4, cu „km/h” mic în dreapta lor. **Nu portocaliu.**
- Sub viteză, **zona de informații**: „Range” și „Average Fuel” pe două rânduri, plus o bară orizontală de consum cu scală 0–20–40, exact ca în poza RS.
- **Rândul de jos** (pe toată lățimea, sub potcoavă): temperatura exterioară în °C (stânga), odometrul/tripul „A 0.0 km” (centru), ora (dreapta).
- **Colțul stânga-sus**, în afara arcului: indicatorul de treaptă, **portocaliu, mic** (unde la CVT apare „P”), și deasupra lui iconița verde **ECON** (frunză). Mută aici „A1”/treapta din joc și **șterge-l din centrul cadranului**. Pentru manuală, afișează cifra treptei (1–6, N, R) și o săgeată ▲ de upshift când e cazul.
- Font: sans-serif **condensat**, curat (de ex. Barlow Semi Condensed sau Roboto Condensed). Fără fonturi „sport” sau futuriste.

**Modulele laterale:**
- **Stânga = temperatura lichidului de răcire**: arc segmentat, de la **C** (jos) la **H** (sus), cu iconița de termometru. Segmentele urmează tema (roșu/alb sau albastru/alb).
- **Dreapta = nivelul combustibilului**: arc segmentat, de la **E** (jos) la **F** (sus), cu iconița de pompă și săgeata pentru partea bușonului.
- Martorii de bord (roșii/galbeni: centură, ulei, baterie etc.) stau în colțurile modulelor și sunt **stinși** în mod normal; aprinde-i doar la evenimente.
- Atenție, data trecută ți-am scris invers: **temperatura e în stânga, combustibilul în dreapta.** Respectă pozele.

**Implementare pentru joc (ca să fie viu, nu o poză statică):**
- Ecran central: textură de fundal **2048×1280** cu toate elementele statice (scală, cifre, etichete). Peste ea:
  - **bara de turație** ca mesh sau quad separat cu shader de tip *radial fill* (masca de unghi controlată de un parametru `rpm01`);
  - **viteza, treapta, odometrul, ora, temperatura exterioară** randate ca text/UI din engine (render texture sau world-space UI), nu coapte în textură.
- Module laterale: textură **512×1024** fiecare, cu segmentele controlate tot printr-un parametru de umplere (`temp01`, `fuel01`).
- Emission ~1.5–2.5. Negrul trebuie să rămână negru (fără ceață gri), iar ecranul nu are voie să facă bloom urât.
- Expune parametrii (`rpm`, `speed`, `gear`, `fuel01`, `temp01`) ca să-i pot lega de logica mașinii.

**Verificare specială pentru cluster:** fă un render frontal al clusterului (cameră perpendiculară pe ecran) la turație ~3000 rpm și 50 km/h și pune-l **lângă poza RS**, side-by-side. Iterează până când proporțiile potcoavei, poziția vitezei, rândul de jos și modulele laterale se suprapun vizibil cu originalul.

### 2.4 Bordul pe partea pasagerului – gaura neagră de sub panou
**Ce se vede acum:** între partea de sus a bordului și partea de jos e o **fantă neagră, goală**, pe toată lățimea dinspre ecran până la gura de ventilație din dreapta. Pare că lipsește o piesă.

**Cum trebuie să fie (vezi zoom-ul pe partea pasagerului din poza MotorTrend):**
- Partea de sus a bordului coboară și se termină într-o **buză rotunjită**. Imediat sub ea vine **o bandă decorativă orizontală continuă** (~60–70 mm înălțime), care pleacă de lângă ecran și se termină în **rama gurii de ventilație din dreapta**.
  - Pe **muchia ei de sus**: un **fir subțire satin chrome** (~3–4 mm), care urmărește toată lungimea și se arcuiește în jurul gurii de ventilație.
  - Suprafața benzii: plastic negru cu **textură fină** (granulație sau model ușor geometric/„brushed” închis), ușor bombată spre pasager.
- Sub bandă: panoul inferior al bordului, **convex**, soft-touch negru, apoi **torpedoul** cu mânerul încastrat în partea de sus-stânga a ușii lui.
- Între piese există doar **rosturi fine de 1–2 mm**, fără goluri, fără negru „infinit”. Verifică din mai multe unghiuri, inclusiv de pe scaunul șoferului, că nu se vede prin nicio deschizătură.

### 2.5 Volanul – rafinare
Arată mai bine, dar încă pare din plastic gri-bej, plat. Ce trebuie rafinat:

- **Culoare și material**: piele **neagră** (#141414), nu gri-bej. Normal map cu granulație de piele. **Zone perforate** pe părțile laterale ale jantei (orele 9–10 și 2–3), piele netedă sus și jos. Roughness 0.45–0.55 cu variație ușoară (mai lucios unde se ține mâna).
- **Cusături**: fine, gri închis, pe **muchia interioară** a jantei și la îmbinările cu spițele. Fă-le din normal map + o textură de fir, nu geometrie groasă.
- **Secțiunea jantei**: ovală, nu tub perfect rotund. Mai groasă la orele 9 și 3, cu **pernuțe ergonomice pentru degete mari** acolo unde spițele întâlnesc janta.
- **Capacul airbag-ului**: plastic soft-touch **gri foarte închis, mat** (o idee mai deschis decât pielea), cu un **rost întunecat de ~1.5 mm** între capac și spițe.
- **Ornamentele satin chrome în formă de „C”** din jurul butoanelor: profil rotunjit (bevel cu 3–4 segmente), lățime ~6–8 mm, bine vizibile și reflectorizante. Acum aproape nu se văd.
- **Spița de jos**: neagră, cu **două lamele satin chrome** în „V” (nu albe mate), ușor în relief.
- **Butoanele**: geometrie reală, nu doar textură pe un panou plat. Panoul e piano black, ușor adâncit, iar butoanele ies 1–1.5 mm, cu bevel.
  - Stânga: pad cu 4 direcții și ENTER în centru, telefon, voce, back și basculanta de volum.
  - Dreapta: cruise control (RES/+, SET/–), MAIN, CANCEL, distanța ACC, LKAS.
  - **Iconițe albe clare**, dintr-o textură de 1024 pentru fiecare panou, fără blur. Folosește close-up-ul cu comenzile ca referință.
- **În spatele volanului**: maneta de lumini (stânga) și cea de ștergătoare (dreapta), negre, cu inscripții albe pe capete; carcasa coloanei de direcție neagră, granulată. **Fără padele** (cutie manuală).

---

## 3. Bonus (le-am observat în screenshot-uri – rezolvă-le după cele 5 puncte)
- **Oglinda retrovizoare interioară e tot un contur gol** (o ramă ovală prin care se vede afară). Trebuie carcasă neagră plină și sticlă-oglindă, cu reflection probe.
- **Nuca schimbătorului e albă**. Trebuie piele neagră, cu schema treptelor gri deschis pe capac și inel satin chrome la bază (vezi referința din runda 1).
- Interiorul în ansamblu iese **gri-bej în joc** în loc de negru: verifică base color-urile după export (gamma / sRGB vs linear) și expunerea din habitaclu.

## 4. Ce îmi livrezi
- `.blend` actualizat, cu piesele vechi în `OLD_v1`.
- `renders/v2/compare_*.png` pentru fiecare punct (render lângă referință), plus un screenshot din joc din poziția șoferului.
- Clusterul cu parametrii expuși (`rpm`, `speed`, `gear`, `fuel01`, `temp01`) și o notă scurtă despre cum îi leg în cod.
- Exportul pentru joc, cu materialele denumite clar.
