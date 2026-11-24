# Honda Civic Sedan 2020 1.5 VTEC Turbo 6MT – runda 7 (ETS2 / Prism3D)

Runda asta are 6 puncte. **Oglinda a eșuat de 4 ori la rând**, așa că pentru ea și pentru celelalte probleme de „ce mesh e ăsta?” schimbăm metoda: **diagnostic prin etichetare cu culori în joc**, nu presupuneri în Blender. Regulile de până acum rămân valabile:
- doar ce permite ETS2, sintaxă din vanilla și de pe wiki, fără atribute inventate;
- A/B obligatoriu (înainte/după din joc, lângă referință);
- nu atingi ce merge (cluster, volan, martori), decât dacă e strict necesar.

**Regulă nouă: nu declari nimic rezolvat fără un screenshot din joc care o dovedește.** Dacă nu poți face screenshot-ul, spune-mi exact ce să verific eu în joc și **așteaptă confirmarea mea** înainte să treci la punctul următor.

---

## 0. Instrumentul de diagnostic: etichetarea cu culori (folosește-l la punctele 1, 3, 4 și 5)
Când nu e clar din ce fișier sau mesh vine ceva ce se vede în joc:
1. Fă o **copie de lucru** a mod-ului (`_diag`).
2. Dă fiecărui mesh sau material suspect **o culoare plină unică**: o textură 4×4 de o singură culoare, cu un material emissive/unlit vanilla, ca să se vadă și în umbră. De exemplu: roșu = oglinda interioară (carcasă), verde = sticla oglinzii, albastru = brațul, galben = carcasa camerei Honda Sensing, magenta = montantul A, cyan = panoul de ușă, portocaliu = geamul ușii din modelul exterior, alb = interiorul simplificat din modelul exterior etc. Ține un tabel `diag_colors.md`: culoare → fișier → obiect.
3. Pornește jocul, fă screenshot-uri din aceleași unghiuri ca ale mele.
4. **Orice element care NU și-a schimbat culoarea nu vine din fișierele etichetate.** Caută-l mai departe: alt model, un accesoriu `.sii` moștenit de la vehiculul de bază, alt mod activ în profil.
5. Raportează rezultatul, apoi șterge varianta `_diag`.

---

## 1. Montantul A stâng – urât, fațetat, enorm

### 1.1 Ce se vede acum
Un bloc mare, fațetat, cu o „aripă” lată sus spre plafon, muchii ascuțite și un triunghi negru zimțat jos, lângă bord. Ocupă mult din câmpul vizual.

### 1.2 Cum e la Civicul real
Montanții A ai Civicului gen. 10 **sunt într-adevăr lați și înclinați**. ADAC notează la acest sedan că montanții lați reduc vizibilitatea. Dar sunt **piese de ornament netede, curate**, cu suprafață continuă. Referințe:
- vedere frontală a habitaclului, cu ambii montanți pe toată lungimea: https://d2ivfcfbdvj3sm.cloudfront.net/7fc965ab77efe6e0fa62e4ca1ea7673bb25940590f1e3d8e88cb/stills_0640_png/MY2019/13184/13184_st0640_059.png
- vedere din partea șoferului (montantul stâng + ușa): https://d2ivfcfbdvj3sm.cloudfront.net/7fc965ab77efe6e0fa62e4ca1ea7673bb25940590f1e3d8e88cb/stills_0640_png/MY2019/13184/13184_st0640_174.png
- vedere din poziția șoferului (din runda 4): https://carzdeluxe.com/cdn/shop/files/5_a8b57f65-72dc-49a5-b6cb-12b69e1e5a77_1445x.jpg

Descriere:
- O **bandă lungă, cu lățime aproape constantă** (puțin mai lată jos), care urmărește marginea parbrizului de la colțul bordului până în plafon. Secțiunea e ușor convexă spre șofer. Fără fațete și fără „aripi”.
- **Sus**, intră lin sub plafon, cu un rost fin și uniform. Nu se lărgește într-o placă.
- **Jos**, se termină pe bord, în colțul de lângă triunghiul ușii cu tweeter, cu o îmbinare curată. Fără triunghiuri negre.
- Material: plastic/textil **în culoarea plafonului**, granulație fină, mat. **Eu confirm culoarea plafonului pe mașina mea** (gri închis sau negru).
- De obicei are o mică inscripție „AIRBAG” spre partea de sus (perdeaua laterală). Verifică pe referințe.

### 1.3 Ce faci
1. **Refă piesa de la zero**, nu o repara pe cea veche: curbă de ghidaj pe marginea parbrizului, secțiune profilată de-a lungul ei, quad-uri curate, Subdivision 1–2 aplicat, Solidify 3–4 mm.
2. Lățimea și unghiul: măsoară pe referințe, raportat la lățimea parbrizului, și potrivește-le prin overlay din poziția camerei șoferului.
3. Verifică și **montantul exterior** din modelul exterior: nu trebuie să se vadă prin sau pe lângă cel interior.
4. A/B din poziția șoferului și cu capul întors spre stânga, ca în screenshot-ul meu.

---

## 2. Gurile de ventilație centrale – trebuie să fie identice

### 2.1 Ce e greșit acum
- prea multe lamele, subțiri și plate, într-un gol complet negru;
- cursoarele sunt **plăcuțe gri plate**, fără crom, care par să plutească;
- **lipsește banda cromată** de deasupra gurilor;
- deschiderile sunt dreptunghiuri simple, fără forma reală a capetelor.

### 2.2 Referințe
- R4 (centrale, frontal, aproape): https://imgd.aeplcdn.com/1056x594/n/cw/ec/27074/civic-interior-front-centre-air-vents.jpeg
- R6 (centrale, alt unghi): https://cdn.civicx.com/attachments/310/310363-43bdb52b65ea95a2f2f47442b31a0009.webp
- R5 (laterală, doar jumătatea „Before”), pentru profilul lamelelor și al cursorului: https://i.ytimg.com/vi/AxF25VMh8N0/maxresdefault.jpg

### 2.3 Metoda „identic” (obligatorie)
1. **Măsoară, nu estima**: scrie un script Python (OpenCV) care, pe R4:
   - corectează perspectiva (patru colțuri ale zonei de ventilație → dreptunghi);
   - extrage **conturul fiecărei deschideri**, al carcasei butonului de avarie și al benzii cromate (contururi vectoriale);
   - măsoară, în proporții relative la lățimea totală a zonei: înălțimea și lățimea fiecărei guri, raza colțurilor, distanța dintre lamele, **numărul de lamele**, poziția și dimensiunea fiecărui cursor, dimensiunea carcasei de avarie și grosimea benzii cromate.
   
   Salvează tabelul `vents_measurements.md` și imaginea cu contururile desenate peste poză.
2. **Scară reală**: lățimea totală a zonei de guri centrale o iei ca proporție din lățimea ecranului de 7" de sub ele (diagonala 7", raport 16:9 → ~155 mm lățime activă). Verifică raportul pe R4.
3. **Modelează din contururi**: importă contururile ca curbe în Blender și construiește:
   - **rama** cu adâncime, bevel fin și material plastic negru ușor lucios;
   - **lamelele orizontale** (numărul măsurat), cu profil aerodinamic (~2 mm muchia frontală, ~20 mm adâncime), negru mat, bevel pe muchia din față;
   - **cursorul satin chrome** pe lamela corectă (poziție măsurată), ca bloc cu volum: fața cromată, laturile negre. Nu plăcuță plată;
   - **lamelele verticale** din spate (8–10), mai retrase și mai întunecate;
   - **canalul** cu pereți reali, gri foarte închis, cu AO copt. Nu negru absolut: în R4 se văd lamelele verticale;
   - **banda satin chrome** de deasupra, cu traseul exact din R4 (vine din stânga, de peste cluster, și urmărește marginea de sus);
   - **butonul de avarie** în carcasa lui (dimensiuni măsurate), triunghiul roșu cu contur, legat de `button_4way`.
4. **Overlay**: render frontal cu cameră ortografică, aliniat la R4 corectat, la 50% opacitate. Contururile trebuie să se suprapună (abatere ≤ 2% din lățime). Fă 3 iterații.
5. Aplică același tratament gurilor laterale (R5), dacă A/B arată o îmbunătățire.

---

## 3. Oglinda retrovizoare – încă neagră, cu conturul-fantomă

### 3.1 Starea actuală
- sticla complet **neagră**;
- **conturul gri decalat** în stânga, prezent din nou.

### 3.2 Pași, în ordine (cu screenshot din joc la fiecare)
1. **Etichetare cu culori** (§0) pe toate piesele oglinzii, din toate modelele și accesoriile. Află:
   - din ce fișier vine **conturul-fantomă** (dacă nu-și schimbă culoarea, vine din afara pieselor etichetate: caută în accesoriile `.sii` moștenite, în modelul exterior și în alte mod-uri active);
   - **ce suprafață e de fapt neagră**: sticla (verde) sau altceva aflat **în fața** sticlei (de ex. fața carcasei, roșu).
2. **Test de randare**: pe sticlă, pune temporar **materialul oglinzii laterale stângi**, care funcționează.
   - Dacă apare imaginea din oglinda stângă → sticla e bine, problema e la cameră/slot (pasul 3).
   - Dacă rămâne neagră → problema e la mesh: UV, normale, o suprafață care o acoperă, ordinea de randare.
3. **Învață de la un mod care funcționează**: găsește 2–3 mod-uri populare de autoturisme conduse de jucător în ETS2 care au **oglindă retrovizoare interioară funcțională**. Analizează-le definițiile **doar ca să înțelegi tehnica**, fără să copiezi asset-uri: ce slot de cameră folosesc, cum o orientează spre spate, ce material are sticla, cum leagă sticla de cameră. Scrie-mi un rezumat de 10 rânduri cu tehnica, apoi aplic-o la noi.
4. După fix, testele din runda 6 (§1.3): camionul care trece pe lângă, stânga/dreapta oglindite corect, lângă R3: https://www.civicx.com/forum/attachments/fullsizeoutput_4c72-jpeg.149745/
5. **Dacă ETS2 chiar nu permite** (dovedit cu pașii de mai sus), propune-mi alternativa și **așteaptă acordul meu**. Nimic negru sau gol nu rămâne în versiunea finală.

---

## 4. Partea din față a bordului „pare că plutește”

### 4.1 Ce se vede acum
Muchia din față a bordului, lângă parbriz, are **o linie zimțată închisă la culoare**. Imediat după ea apare drumul, fără nicio tranziție, așa că bordul pare suspendat în aer. Jos-stânga, la baza montantului, sunt cioburi negre.

### 4.2 Cum e la Civicul real (vezi E12 și C10)
- E12: https://www.team-bhp.com/carpics/2019-honda-civic/l/exterior/2019-honda-civic-18.jpg
- C10: https://carzdeluxe.com/cdn/shop/files/5_a8b57f65-72dc-49a5-b6cb-12b69e1e5a77_1445x.jpg
- Partea de sus a bordului merge **până sub parbriz**. Îmbinarea **nu se vede**, pentru că e acoperită de **banda neagră ceramică** de pe marginea de jos a parbrizului.
- Banda ceramică: o zonă **opacă** jos, apoi un **gradient de puncte negre** în sus (se vede clar în E12, sus). **Din poziția șoferului** trebuie să acopere linia de contact bord–geam plus 2–3 cm deasupra ei. În runda trecută am cerut-o mai subțire; acum a dispărut cu totul. Calibreaz-o din camera șoferului, nu din Blender.
- **Fanta de dezaburire**: o singură fantă îngustă, cu lamele, negru mat (runda 3, §5). **Nu o linie zimțată.**
- De pe scaunul șoferului, la Civic **nu se vede capota**. Se văd bordul, banda ceramică și apoi drumul.

### 4.3 Ce faci
1. Etichetare cu culori (§0) pe: muchia bordului, fanta de dezaburire, textura parbrizului, grila de la baza parbrizului, capota și cioburile de la baza montantului. Identifică ce e linia zimțată și ce sunt cioburile.
2. Prelungește bordul până la geam (fără spațiu vizibil), refă fanta, pune banda ceramică pe geam calibrată din camera șoferului, elimină cioburile.
3. A/B din camera șoferului, lângă E12 și C10.

---

## 5. Lateral: negrul acoperă geamul ușii

### 5.1 Ce se vede acum
Când mă uit spre stânga, **jumătatea de jos a geamului ușii e o bandă neagră opacă**, de la marginea ușii până aproape de mijlocul geamului. Afară se vede doar deasupra ei.

### 5.2 Cum e la Civicul real
Panoul ușii se termină sus cu o **margine moale**, cu o garnitură neagră subțire (~1 cm) la contactul cu geamul. **Geamul e transparent până jos, la linia ușii.** Prin el se văd oglinda exterioară și drumul. Referințe:
- vedere din partea șoferului: https://d2ivfcfbdvj3sm.cloudfront.net/7fc965ab77efe6e0fa62e4ca1ea7673bb25940590f1e3d8e88cb/stills_0640_png/MY2019/13184/13184_st0640_174.png
- panoul ușii gen. 10: https://imgd-ct.aeplcdn.com/1056x660/n/cw/ec/27074/civic-interior-front-right-door-pad.jpeg

### 5.3 Ce faci
1. Etichetare cu culori (§0) pe: partea de sus a panoului de ușă (interior), geamul ușii **din modelul exterior** (adesea fumuriu sau opac dinspre interior), interiorul simplificat al ușii din modelul exterior, eventuale plane negre de „acoperire” și chederul.
2. Corecții probabile: geamul exterior **transparent dinspre interior** (material de geam vanilla, fețe pe ambele părți dacă e nevoie). Elimină sau coboară orice panou negru de deasupra liniei ușii. Partea de sus a panoului interior ajunge exact la linia geamului.
3. A/B cu capul întors spre stânga, ca în screenshot-ul meu.
4. Tot aici, **mânerul interior al ușii e încă alb-gri lucios**, deși l-am cerut satin chrome în runda 5. Aplică materialul satin chrome (env map, base ~#9A9A9A, roughness ~0.3) și verifică în joc.

---

## 6. Performanța: reprizele exact ca în realitate

### 6.1 Ținte măsurate de ADAC chiar pe modelul meu
ADAC a testat **Civic Limousine 1.5 Turbo, manuală 6 trepte**, cu anvelope **215/50 R17**. Valori măsurate:

| Test | Real (ADAC) |
|---|---|
| Elasticitate 60–100 km/h **în a 4-a** | **6.0 s** |
| Elasticitate 60–100 km/h **în a 5-a** | **8.2 s** |
| Elasticitate 60–100 km/h **în a 6-a** | **11.2 s** |
| Depășire 60–100 km/h (a 2-a + a 3-a) | **4.2 s** |
| 0–100 km/h | 8.0–8.5 s (date de fabrică; ADAC listează 8.4–8.5 s) |
| Masă proprie măsurată | **1 290 kg** |
| Turație la 130 km/h (a 6-a) | **~3 100 rpm** |
| Viteză maximă | 210 km/h |

### 6.2 Calibrarea transmisiei
- Cu 215/50 R17 (Ø ≈ 647 mm) și rapoartele 6MT (1: 3.643 · 2: 2.080 · 3: 1.361 · 4: 1.024 · 5: 0.830 · 6: 0.686), **raportul final care dă ~3 100 rpm la 130 km/h în a 6-a e ~4.2**. Valoarea publicată în SUA, 4.105, dă ~3 000 rpm.
- Pornește de la 4.105, apoi **confirmă cu mine**. Eu citesc pe mașina mea turația la 100 și la 130 km/h în a 6-a și îți spun dimensiunea exactă a anvelopelor. Raportul final îl ajustezi după citirile mele.

### 6.3 Ce faci
1. Pentru fiecare test din tabel, **măsoară în joc exact același test** (pe drum drept, fără pantă și fără trafic, de 3 ori, cu media), folosind telemetria jocului într-un CSV (viteză + timp).
2. Ajustează parametrii per-vehicul (cuplu și curba de cuplu, raport final, masă dacă există, raza roților) până când **toate** testele sunt în **±5%** față de real. Prioritate au elasticitățile în a 4-a, a 5-a și a 6-a: ele dau senzația de „trage”.
3. Dacă nu poți atinge toate țintele simultan, arată-mi tabelul de compromis și ce parametru limitează (de ex. rezistența aerodinamică globală din ETS2).
4. Livrabil: tabelul *real vs joc* și graficul viteză–timp pentru 60–100 în a 4-a, a 5-a și a 6-a, suprapus cu valorile ADAC.

---

## 7. Livrabile
- Pentru fiecare punct: diagnostic (cu tabelul culorilor, unde s-a folosit), fișierele modificate, A/B din joc și verdictul.
- `vents_measurements.md` + overlay-ul gurilor de ventilație.
- Rezumatul tehnicii de oglindă învățate din alte mod-uri.
- Tabelul de performanță.
- Lista de lucruri pe care trebuie să le verific sau să le măsor eu pe mașina mea: culoarea plafonului/montanților, anvelopele, turația la 100 și 130 km/h în a 6-a, poze.
