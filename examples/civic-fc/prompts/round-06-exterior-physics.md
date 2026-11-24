# Honda Civic Sedan 2020 1.5 VTEC Turbo 6MT – runda 6: oglindă, parbriz/ștergătoare, roți, lumini, performanță (ETS2 / Prism3D)

Interiorul e aproape gata. Runda asta extinde lucrul la **exterior** și **fizică**. Regulile din rundele anterioare rămân valabile:
- doar ce permite ETS2: fără cod, efecte `eut2.*` vanilla, unități `.sii` copiate după vanilla/wiki, **fără atribute inventate**;
- **A/B obligatoriu**: screenshot înainte/după din joc, lângă referința reală. Dacă „după” nu e clar mai bun, revii la „înainte”;
- nu atingi ce funcționează deja (cluster, volan, martori, guri de ventilație), decât dacă e strict necesar.

**Sursa de adevăr pentru fizică și dimensiuni e mașina mea reală** (Civic sedan 1.5 Turbo, 182 CP, manuală 6 trepte). Unde specificațiile publice diferă sau lipsesc, îmi spui exact ce să măsor sau să citesc de pe mașină și te bazezi pe valorile mele.

---

## Referințe (descarcă-le în `refs/v6/` și deschide-le cu Read înainte de fiecare punct)

Galerie foto completă a unui **Civic sedan facelift (2019) cu 1.5 Turbo**: aceeași caroserie ca sedanul european. Atenție la diferențele specifice Indiei: camera LaneWatch din oglinda dreaptă nu există la noi, iar numărul de înmatriculare e altul.

| # | Ce arată | Link |
|---|---|---|
| E1 | Față, faruri cu LED DRL (lumină de zi) aprinse, la apus | https://www.team-bhp.com/carpics/2019-honda-civic/l/exterior/2019-honda-civic-10.jpg |
| E2 | Față, frontal, faruri stinse (formă, bara cromată) | https://www.team-bhp.com/carpics/2019-honda-civic/l/exterior/2019-honda-civic-12.jpg |
| E3 | Proiectorul de ceață + ornamentul cromat din bară | https://www.team-bhp.com/carpics/2019-honda-civic/l/exterior/2019-honda-civic-13.jpg |
| E4 | **Stop aprins noaptea**: banda LED în „C”, semnalizarea portocalie și marșarierul alb în interior | https://www.team-bhp.com/carpics/2019-honda-civic/l/exterior/2019-honda-civic-40.jpg |
| E5 | Stopul ziua (formă, continuarea pe capota portbagajului) | https://www.team-bhp.com/carpics/2019-honda-civic/l/exterior/2019-honda-civic-39.jpg |
| E6 | Spate complet (stopuri, catadioptri sau proiectoare în bară) | https://www.team-bhp.com/carpics/2019-honda-civic/l/exterior/2019-honda-civic-41.jpg |
| E7 | Semnalizarea LED din oglinda exterioară, aprinsă | https://www.team-bhp.com/carpics/2019-honda-civic/l/exterior/2019-honda-civic-21.jpg |
| E8 | **Roata față în aripă**: spațiul anvelopă–aripă, căptușeala neagră a pasajului | https://www.team-bhp.com/carpics/2019-honda-civic/l/exterior/2019-honda-civic-28.jpg |
| E9 | **Janta 17" bicoloră (diamantată), de aproape** | https://www.team-bhp.com/carpics/2019-honda-civic/l/exterior/2019-honda-civic-26.jpg |
| E10 | Roata spate + aripa, profil | https://www.team-bhp.com/carpics/2019-honda-civic/l/exterior/2019-honda-civic-30.jpg |
| E11 | Profil lateral complet (proporții roată/aripă) | https://www.team-bhp.com/carpics/2019-honda-civic/l/exterior/2019-honda-civic-36.jpg |
| E12 | **Vederea șoferului prin parbriz**: ce se vede jos (bord, ștergătoare, banda neagră cu puncte) | https://www.team-bhp.com/carpics/2019-honda-civic/l/exterior/2019-honda-civic-18.jpg |
| E13 | Ștergătoarele parcate: cât ies de sub capotă, grila de la baza parbrizului | https://www.team-bhp.com/carpics/2019-honda-civic/l/exterior/2019-honda-civic-16.jpg |
| E14 | Grila de la baza parbrizului (cowl) de aproape | https://www.team-bhp.com/carpics/2019-honda-civic/l/exterior/2019-honda-civic-17.jpg |
| R3 | **Ce se vede într-o oglindă retrovizoare de Civic gen. 10** (din runda 4) | https://www.civicx.com/forum/attachments/fullsizeoutput_4c72-jpeg.149745/ |
| C10 | Poziția șoferului: bord + baza parbrizului (din runda 4) | https://carzdeluxe.com/cdn/shop/files/5_a8b57f65-72dc-49a5-b6cb-12b69e1e5a77_1445x.jpg |

Documentație SCS (wiki):
- Sistemul de lămpi: https://modding.scssoft.com/wiki/Documentation/Tools/SCS_Blender_Tools/Materials/Lamp_system
- Lamp Switcher & Lamp UV Tool: https://modding.scssoft.com/wiki/Documentation/Tools/SCS_Blender_Tools/SCS_Tools_Sidebar/Lamp_Switcher_%26_UV_Tool
- Animații și ID-uri de interior: https://modding.scssoft.com/wiki/Documentation/Engine/Truck_Interior_Animations_and_IDs

---

## 1. Oglinda retrovizoare: arată ÎN FAȚĂ (și conturul-fantomă e tot acolo)

### 1.1 Ce arată screenshot-ul meu
- În oglindă se vede **drumul din față**, iar jos apare **capota albă**. Camera oglinzii e orientată **înainte**, nu înapoi.
- **Conturul gri mai mare, decalat spre stânga**, e acolo **a treia rundă la rând**. Deci nu e în `.blend`-ul pe care îl cureți.

### 1.2 Conturul-fantomă – găsește-l definitiv
Caută-l **în toate sursele**, nu doar în `.blend`:
- modelul interior exportat (`.pim`) și **toate accesoriile** atașate interiorului sau cabinei;
- **accesoriul de oglindă moștenit** de la vehiculul de bază din care a pornit mod-ul (un `accessory` din `.sii` care încarcă un model vanilla de oglindă);
- modelul exterior;
- variantele de interior/cabină (dacă există mai multe).

Raportează **calea exactă** a fișierului din care vine și elimină-l acolo (sau scoate referința din `.sii`). Dovada: screenshot fără contur.

### 1.3 Orientarea camerei
1. Găsește definiția exactă a camerei slotului folosit (poziție, rotație/direcție, FOV). Scrie-mi-o.
2. **Test de orientare**: rotește camera cu 180° pe axa verticală (yaw), ca să privească spre **spatele** mașinii. Verifică și convenția de axe din ETS2 (dacă „înainte” e −Z sau +Z în spațiul vehiculului) și aplică semnul corect.
3. Validare: în oglindă trebuie să apară **luneta, tetierele spate jos și drumul din spate**, nu capota.
   - Test: oprește în spatele unui camion AI, apoi lasă-l să treacă. Camionul trebuie să apară în oglinda centrală **după** ce te-a depășit (când e în spate), nu înainte.
   - Stânga și dreapta trebuie să fie oglindite corect: un vehicul care vine din spate pe banda din stânga apare în **stânga** oglinzii.
4. Restul specificațiilor din v4/v5 rămân: FOV ~26° × 7°, aspect ~3.8:1, înclinare ușoară în jos, luneta modelului exterior transparentă dinspre interior, interior spate (banchetă, tetiere, poliță) cu siluete corecte.
5. Livrează screenshot-ul final lângă **R3**.

---

## 2. Baza parbrizului: negrul e exagerat (ștergătoare / cowl / bandă ceramică)

### 2.1 Problema
De pe scaunul șoferului, la baza parbrizului apare **o bandă neagră groasă și opacă**, pe toată lățimea, între bord și drum. Într-un Civic real (E12, C10) nu există așa ceva.

### 2.2 Cum e în realitate
- De pe scaunul șoferului se văd, de jos în sus: **partea de sus a bordului** (mată, granulată), apoi **o bandă neagră ceramică subțire** pe marginea de jos a parbrizului, care se termină cu **un gradient de puncte negre** (vezi E12 și C10), apoi direct drumul.
- **Ștergătoarele parcate** stau jos, **în mare parte ascunse sub marginea din spate a capotei** (E13). Din interior se văd cel mult brațele, subțiri, spre colțuri, nu o bandă continuă.
- **Grila de la baza parbrizului** (cowl, E14) e plastic negru granulat, **sub nivelul capotei**, aproape invizibilă din interior.

### 2.3 Ce faci
1. **Identifică exact ce mesh produce banda neagră.** Ascunde pe rând: banda ceramică din textura geamului, ștergătoarele, grila de la baza parbrizului, marginea capotei, eventualele plane negre de umbră sau ocluzie din modelul interior și orice „cutie” neagră din modelul exterior. Raportează ce era.
2. **Banda ceramică**: pe textura parbrizului, înălțime realistă (~6–8 cm opacă jos, apoi 2–3 cm de gradient din puncte), după E12/C10. Puncte negre, rotunde, fine, cu mipmaps, fără moiré.
3. **Ștergătoarele**: poziția de parcare, lungimea și profilul după E13 (șofer ~65 cm, pasager ~40 cm la gen. 10; verifică pe poze). Parcate **sub linia capotei**. Brațe negre mate, lame subțiri. Animația `wiper_anim` trebuie să rămână funcțională.
4. **Grila de la bază** (E14): sub nivelul capotei, negru granulat, cu fantele vizibile doar de afară.
5. Dacă negrul vine din geometria bordului (prea înalt, atinge parbrizul), coboară sau rotunjește muchia, conform C10.
6. **A/B** din poziția șoferului, lângă E12.

---

## 3. Roți și jante: anvelopa intră prin aripă

### 3.1 Problema
Cu roțile bracate (și probabil și la compresia suspensiei), **anvelopa față trece prin aripă** (vezi screenshot-ul meu). În realitate există mereu spațiu liber, iar pasajul roții are **căptușeală neagră** (E8).

### 3.2 Date reale (verifică-le și confirmă-le cu mine)
| Parametru | Valoare publicată | De confirmat |
|---|---|---|
| Anvelope | 235/45 R17 (EU 17"); alternativ 215/50 R17 | **eu citesc de pe flancul anvelopei** |
| Diametru exterior | 235/45R17 ≈ **643 mm**; 215/50R17 ≈ 647 mm | – |
| Ampatament | ~2 698–2 700 mm | – |
| Ecartament | față **1 547 mm**, spate **1 563 mm** (sedan facelift) | – |
| Diametru de bracaj | **~11.4 m** (sedan facelift 1.5) | – |
| Garda la sol | ~124–135 mm | – |

### 3.3 Ce faci
1. **Dimensiunea roții**: raza roții din model și din definiția roții să corespundă anvelopei reale (643 mm diametru pentru 235/45R17). Lățimea anvelopei 235 mm.
2. **Poziția roților**: locatorii roților la ampatamentul și ecartamentul reale. Roata trebuie să fie **centrată în arcul aripii** pe profil (E10, E11) și să **nu iasă în afara** liniei aripii privită din față.
3. **Spațiul liber anvelopă–aripă** în poziție statică: măsoară-l pe E8/E11, raportat la diametrul anvelopei (643 mm), și reprodu-l.
4. **Bracajul**: calculează unghiul maxim al roților din diametrul de bracaj 11.4 m și ampatament (roata exterioară ≈ asin(L / R)), cu geometrie Ackermann pentru roata interioară. Configurează-l unde îl definește ETS2 pentru vehicul (găsește în vanilla și pe wiki). **Nu reduce bracajul ca să ascunzi problema**: repară geometria.
5. **Verificare de interferență în Blender**: pune roata în poziția cea mai defavorabilă (bracaj maxim stânga/dreapta + compresie maximă a suspensiei, cât permite ETS2) și verifică cu un test de intersecție (boolean / BVH overlap) că **nicio față a anvelopei nu intersectează** aripa, bara sau căptușeala. Raportează distanța minimă.
6. **Căptușeala pasajului roții**: plastic negru mat, fibros/granulat, cu adâncime reală, ca în E8. Nu caroserie albă vizibilă prin pasaj.
7. **Janta** (E9): design-ul actual e corect ca tip (17", 5 spițe duble răsucite, bicoloră). Rafinează doar după A/B:
   - fața spițelor **diamantată/frezată** (aluminiu deschis, cu striații fine radiale în roughness), zonele adâncite **gri închis-grafit**;
   - capacul central cu emblema H cromată pe negru;
   - piulițele vizibile;
   - prin spițe se văd **discul de frână și etrierul**.
8. **Anvelopa**: inscripțiile de pe flanc (marcă, dimensiune) ca normal map discret, umărul rotunjit și profilul benzii de rulare realist. Fără flanc perfect plat și lucios.
9. **A/B**: roata față bracată maxim, din exterior (cameră liberă), plus profil lateral lângă E11.

---

## 4. Lumini: farurile și stopurile nu funcționează deloc

### 4.1 Cum funcționează în ETS2 (respectă documentația)
- Suprafețele luminoase folosesc **materialul de lampă** (shader `lamp`), care are nevoie de **o a doua textură-mască RGBA**. Fiecare canal e o mască pentru un tip de lumină: **R – semnalizare stânga/dreapta; G – faza lungă, frână; B – faza scurtă, marșarier, lumini de zi (DRL); A – lumini de poziție**.
- Mai e nevoie de **un layer UV separat** pentru masca lămpii, cu **offset-ul corect de tile** pentru fiecare funcție (stânga/dreapta, față/spate). Folosește **Lamp UV Tool** din SCS Blender Tools ca să pui UV-urile pe tile-urile corecte și **Lamp Switcher** ca să verifici fiecare funcție direct în Blender.
- **Lumina efectivă** (fasciculul farurilor pe drum, halourile/flare-urile, lumina roșie a stopurilor): găsește în vanilla și pe wiki cum se definesc sursele de lumină și flare-urile pe un vehicul (locatori sau unități) și copiază structura de la un vehicul vanilla.
- **Diagnostic întâi**: de ce nu se aprinde nimic acum? Verifică materialul (e chiar `lamp`?), existența și conținutul măștii, layerul UV al lămpii și tile-urile, legarea luminilor la vehicul. Raportează cauza.

### 4.2 Cum arată luminile reale (facelift, E1–E7)
**Față (E1, E2):**
- Far cu **bandă LED de poziție/DRL** de-a lungul marginii de sus și a celei dinspre grilă (forma de „sprânceană” din E1), alb rece, **uniformă** (light guide, nu puncte separate).
- **Proiector** pentru faza scurtă/lungă în interiorul farului (lentilă, reflector cromat), cu interiorul negru/cromat, ca în E2.
- **Semnalizare** portocalie în far (verifică poziția pe E1/E2 și pe referințe EU). **Repetorul** din oglinda exterioară e o bandă LED portocalie (E7).
- **Proiector de ceață** rotund în bară, cu ornamentul cromat (E3), dacă versiunea are.

**Spate (E4, E5, E6):**
- **Banda LED în „C”** (light guide roșu, uniform, fără puncte), cu continuare pe **capota portbagajului**. Este lumina de poziție.
- **Frâna**: aceeași zonă devine **mult mai luminoasă** și/sau se aprinde zona interioară. Verifică pe referințe exact ce zonă crește la frânare.
- În interiorul lămpii, în partea de jos: **semnalizare portocalie** și **marșarier alb** (E4). Clipește numai semnalizarea.
- **A treia lampă de frână** și **proiectorul de ceață spate** (EU): verifică poziția pe referințe și pe mașina mea (îți pot trimite poze).
- Lămpile neaprinse: geam roșu translucid cu adâncime și reflector în interior, nu plastic roșu plat.

### 4.3 Comportament (fiecare testat în joc)
| Comandă | Ce se aprinde |
|---|---|
| Lumini de poziție | banda DRL față (redusă, dacă e cazul), banda „C” spate, plăcuța de înmatriculare |
| Faza scurtă | proiectoarele față + fasciculul pe drum, plus spatele ca la poziție |
| Faza lungă | proiectoarele (canalul G) + fascicul mai lung |
| Frână | zona de frână spate + a treia lampă de frână |
| Marșarier | lumina albă din stop + lumina reală pe sol în spate |
| Semnalizări / avarie | față portocaliu + repetor în oglindă + spate portocaliu, **sincron** cu martorii din cluster |
| DRL (contact pus, ziua) | banda LED față |

**Livrabile pentru lumini:** screenshot-uri din joc, ziua și noaptea, față și spate, pentru fiecare rând din tabel, lângă E1/E4. Plus o captură cu farurile pe drum, noaptea, de pe scaunul șoferului.

---

## 5. Performanța: mașina să tragă exact ca în realitate

### 5.1 Ținte (date publicate, Civic sedan 1.5 VTEC Turbo 182 CP, manuală)
- Putere **134 kW (182 CP) la 5 500 rpm**; cuplu **240 Nm între 1 900 și 5 000 rpm** (manuală); turație maximă ~6 500 rpm.
- **0–100 km/h ≈ 8.0–8.2 s**; viteză maximă **~210 km/h** (sedan).
- Masă proprie ~1 280–1 310 kg (+ șofer).
- Rapoarte cutie 6MT (gen. 10, 1.5T; **de confirmat pentru varianta EU**): **1: 3.643 · 2: 2.080 · 3: 1.361 · 4: 1.024 · 5: 0.830 · 6: 0.686 · R: 3.673 · final: 4.105**.

### 5.2 Verificare de calcul (cu 235/45R17, Ø 643 mm, final 4.105)
Turația ≈ **33.9 × viteza (km/h) × raportul treptei**. De aici:
- maxim pe treaptă la 6 500 rpm: **1: ~53 · 2: ~92 · 3: ~141 · 4: ~187 km/h** (5 și 6 sunt limitate de rezistența aerului, nu de turație);
- **la 160 km/h: treapta 4 ≈ 5 550 rpm, treapta 5 ≈ 4 500 rpm, treapta 6 ≈ 3 720 rpm**;
- **la 100 km/h în treapta 6 ≈ 2 320 rpm.**

Asta se potrivește cu ce simt eu: în a 4-a trage până la ~180+. **Eu verific pe mașina mea turația la 100 km/h în a 6-a.** Dacă iese diferit, ajustezi raportul final sau dimensiunea anvelopei.

### 5.3 Ce faci în ETS2
1. Găsește **toți** parametrii care influențează accelerația pentru vehiculul nostru: definiția motorului (cuplu, **curba de cuplu**, turație ralanti/maximă), definiția cutiei (rapoartele, raportul final), raza roților, masa vehiculului (unde se definește), orice frecare sau rezistență per vehicul. **Spune-mi ce e per-vehicul și ce e global** (fizica ETS2 e făcută pentru camioane).
2. **Curba de cuplu** reală (pornește de la asta și rafinează cu o diagramă de dinamometru pentru motorul stock de 182 CP, dacă găsești una de încredere):
   - 1 000 rpm ≈ 55%
   - 1 500 rpm ≈ 80%
   - 1 900–5 000 rpm = 100% (240 Nm)
   - 5 500 rpm ≈ 97% (corespunde cu 134 kW)
   - 6 000 rpm ≈ 85%
   - 6 500 rpm ≈ 72%
3. **Calibrează pe timpi măsurați, nu pe cifre nominale.** Dacă fizica ETS2 (masă, inerție, rezistență aerodinamică) face ca 240 Nm reali să dea o accelerație prea mică, ajustează parametrii per-vehicul până când **timpii măsurați în joc** ies ca în realitate. Notează orice abatere de la valorile reale și motivul.
4. **Măsurători în joc** (pe autostradă dreaptă, fără trafic, de 3 ori fiecare, cu media). Folosește telemetria jocului (de ex. un telemetry server/SDK local care scrie viteza în timp, într-un CSV) sau, minim, cronometrare pe înregistrare video:
   - 0–100 km/h (țintă 8.0–8.2 s);
   - 80–120 km/h în a 4-a și în a 5-a;
   - 100–160 km/h în a 5-a;
   - viteza maximă (~210 km/h);
   - turația la 100 km/h în a 6-a (~2 320 rpm) și la 160 km/h în a 5-a (~4 500 rpm).
5. Țintele pentru reprize (80–120, 100–160) **le măsor eu pe mașina mea**, cu un GPS (de ex. o aplicație de măsurat accelerația), doar pe un drum sigur și legal. Până atunci, folosește-le pe cele calculate din curba de cuplu, rapoarte și masă, și arată-mi calculul.
6. **Livrabil**: un tabel *real vs joc* pentru fiecare test, plus graficul viteză–timp de la 0 la viteza maximă, cu schimbările de treaptă la ~6 300 rpm.

---

## 6. Ordinea de lucru și livrabile
1. Oglinda (§1) → 2. Baza parbrizului (§2) → 3. Roți (§3) → 4. Lumini (§4) → 5. Performanță (§5).
- Pentru fiecare punct: diagnosticul (cauza), modificările (fișier și ce s-a schimbat), A/B lângă referință și verdictul.
- La final: lista a ce **nu** se poate face în ETS2 și varianta cea mai apropiată aleasă, plus lista de lucruri pe care trebuie să le măsor sau să le fotografiez eu pe mașina mea.
