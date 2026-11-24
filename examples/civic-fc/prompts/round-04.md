# Interior Honda Civic Sedan 2020 – runda 4 (ETS2 / Prism3D)

Progres mare: turația și consumul merg. Runda 4 are 4 puncte:
1. oglinda retrovizoare;
2. clusterul: viteza a dispărut, iar martorii (semnalizări, lumini etc.) lipsesc;
3. gurile de ventilație;
4. simetria volan–cluster și claritatea butoanelor și a inscripțiilor.

Toate constrângerile ETS2 din addendum-ul v3.1 rămân valabile: fără cod, doar animații de oase, dashboard UI cu ID-uri, sistemul de oglinzi al jocului și efecte `eut2.*` vanilla. Sintaxa o iei din fișierele vanilla și de pe wiki-ul SCS. **Nu inventa atribute.**

Standard de acceptare, același ca până acum: **screenshot din joc lângă poza reală, la aceeași încadrare, fără diferențe vizibile.** Pentru fiecare punct: minim 3 iterații, fiecare cu imaginea de comparație în `renders/v4/`.

---

## 1. Referințe noi (descarcă-le în `refs/v4/` și deschide-le cu Read înainte de fiecare punct)

| # | Ce arată | Link |
|---|---|---|
| R1 | **Volan 2020 oficial Honda, 2800×1260**: butoanele ambelor spițe, foarte clar (cea mai bună referință pentru volan) | https://s3.amazonaws.com/di-honda-enrollment/2020-civic-si-sedan/section-images/18-steering-wheel-mounted-controls-2020-civic-si-sedan.jpg |
| R2 | Spița stângă de aproape (pad, rolă de volum, cadru argintiu) | https://www.civicx.com/forum/attachments/8e34c451-8095-4177-a487-bdf7ea0772b4-webp.372918/ |
| R3 | **Oglinda retrovizoare reală în Civic gen. 10, cu ce se vede în ea**: luneta, tetierele spate, carcasa camerei, consola de plafon | https://www.civicx.com/forum/attachments/fullsizeoutput_4c72-jpeg.149745/ |
| R4 | **Gurile de ventilație centrale + butonul de avarie, foarte aproape** | https://imgd.aeplcdn.com/1056x594/n/cw/ec/27074/civic-interior-front-centre-air-vents.jpeg |
| R5 | **Gura de ventilație laterală a șoferului, foarte aproape**. Folosește **doar jumătatea stângă „Before”**; dreapta e accesoriu carbon aftermarket. | https://i.ytimg.com/vi/AxF25VMh8N0/maxresdefault.jpg |
| R6 | Gurile centrale + avarie + ecran, alt unghi | https://cdn.civicx.com/attachments/310/310363-43bdb52b65ea95a2f2f47442b31a0009.webp |
| C1 | Cluster, ecranul central, km/h, foarte clar (din v3) | https://paultan.org/image/2016/06/2016-Honda-Civic-1.5T-Premium-Instrument-Cluster-8.jpg |
| C2 | **Diagrama oficială a clusterului din manualul Honda: poziția fiecărui martor** (din v3) | https://cdn.civicx.com/attachments/402/402937-e821ac52f3373dc2d0486b1946b61cff.webp |
| C3 | Cluster în mers, temă roșie, 80 km/h (din v3) | https://i.ytimg.com/vi/-6PUhPeIZy8/maxresdefault.jpg |
| C5 | Cluster roșu complet, cu modulele laterale (din v3) | https://cdn.civicx.com/attachments/373/373667-a9e9eba93c0d5257c1f42a86acc97c97.webp |
| C7 | Cluster RS, km/h și °C (din v3) | https://d1hv7ee95zft1i.cloudfront.net/custom/blog-post-photo/gallery/2020-honda-civic-rs-turbo-digital-gauge-cluster-606a9d556a814.jpg |
| C10 | Poziția șoferului: volan centrat pe cluster (pentru simetrie) | https://carzdeluxe.com/cdn/shop/files/5_a8b57f65-72dc-49a5-b6cb-12b69e1e5a77_1445x.jpg |
| W | Wiki SCS: lista completă de ID-uri pentru dashboard UI și animații de interior | https://modding.scssoft.com/wiki/Documentation/Engine/Truck_Interior_Animations_and_IDs |

---

## 2. Oglinda retrovizoare interioară

### 2.1 Ce e greșit acum (screenshot-ul meu)
- Sticla e **semi-transparentă**: prin ea se vede gardul din fața mașinii, suprapus peste imaginea din oglindă.
- Imaginea e **întunecată, neclară, cu proporții greșite** (pare întinsă sau zoomată). Arată bucăți low-poly de interior, gri și negre, fără lunetă, fără drumul din spate și fără tetiere recognoscibile.

### 2.2 Ce trebuie să se vadă (R3)
- Sus și la mijloc, **cea mai mare parte a imaginii (~70–75%)**: luneta, cu **drumul și traficul din spate** clare și luminoase.
- Jos (~20–25% din înălțime): **siluetele tetierelor din spate** (cele două laterale, plus cea centrală dacă modelul real o are; verifică pe referințe) și muchia polițelor/banchetei, întunecate, la contrast cu luneta luminoasă.
- Pe laterale, subțire: **montanții C** și rama lunetei, negre.
- Eventual, liniile foarte fine ale dezaburitorului lunetei.

### 2.3 Diagnostic și reparare (în ordinea asta)
1. **Materialul sticlei**: trebuie să fie **exclusiv** materialul de oglindă al slotului de cameră folosit, ca la oglinzile laterale care merg. **Opacitate 100%**, fără efect de geam, alpha sau blending, fără strat suplimentar de sticlă transparentă peste. Verifică în Blender că nu există **două fețe suprapuse** (sticlă transparentă + oglindă). Dacă există, șterge-o pe cea transparentă.
2. **Ce model randează camera oglinzii**: află din vanilla și de pe wiki dacă oglinzile ETS2 randează **modelul exterior** al vehiculului (de obicei da) sau interiorul. Bucățile low-poly din imagine sunt aproape sigur interiorul simplificat din modelul exterior. Ca oglinda să arate ca în R3, **modelul exterior trebuie să aibă un interior spate decent, văzut prin lunetă**: bancheta spate, **tetierele spate cu forma corectă**, polița din spate, montanții C pe interior, rama lunetei. Materiale negre/gri închis, fără fețe lipsă, fără normale inversate. Totul low-poly, dar cu siluete corecte.
3. **Orientarea camerei**: din poziția oglinzii, orientată spre **centrul lunetei**, înclinată ușor în jos (~3–5°), ca tetierele să ocupe doar banda de jos.
4. **FOV și proporții**: o oglindă plană de ~250×65 mm, la ~0.55 m de ochii șoferului, acoperă cam **26° pe orizontală** și **~7° pe verticală**.
   - Setează FOV-ul și raportul de aspect al camerei (dacă motorul permite) să corespundă **raportului sticlei (~3.8:1)**, ca imaginea să nu fie întinsă.
   - Ca exemplu de configurare FOV la oglinzi în ETS2, uită-te la mod-urile din Workshop care modifică FOV-ul oglinzilor (de ex. „True Mirror FOV for ETS2”, care ajustează oglinzile principale când e activ `g_phys_mirrors`).
5. **UV-ul sticlei**: insulă 0–1 pe toată suprafața, **fără distorsiune**, orientată corect (verifică flip-ul orizontal, ca stânga și dreapta să fie oglindite corect).
6. **Rezoluția și calitatea** imaginii depind și de setările grafice ale jucătorului (calitatea oglinzilor). Spune-mi ce setări recomanzi pentru test.

### 2.4 Geometria oglinzii (R3)
- Carcasă **neagră mată, fără ramă vizibilă în față** (aproape frameless). Sticla ocupă aproape toată fața, cu o margine neagră de ~3 mm. Forma e dreptunghiulară, cu laturile scurte puternic rotunjite și latura de jos ușor curbată.
- În spate: **carcasa mare a camerei Honda Sensing**, neagră, granulată, lipită de parbriz, și **consola de plafon** cu lămpile de citire deasupra (vezi R3).
- **Test final**: un vehicul AI în spate, pe stânga și pe dreapta, plus screenshot-uri pe zi și pe noapte (farurile din spate trebuie să apară). Pune screenshot-ul din joc lângă R3.

---

## 3. Clusterul: viteza, martorii și finisajul

### 3.1 Viteza a dispărut – repar-o întâi
- Viteza curentă = **ID 1020** (text), din lista de pe wiki (W). Treapta = **ID 1040** (afișează N, A#, R, R# sau cifra treptei; pentru cutie manuală trebuie să dea cifra).
- Verifică, în ordine: elementul 1020 există în fișierul UI, e **vizibil** (nu ascuns de alt element sau de un `ui::group` de ecran inactiv), are **font, mărime și culoare** setate, are **unitatea** „km/h” și o **valoare implicită** pentru test, iar **ordinea de desenare/stratul** îl pune deasupra fundalului. Verifică și că **nu a fost înlocuit din greșeală** cu autonomia: acum, în locul vitezei apare „275 km”.
- Fiecare ID se poate folosi o singură dată (caching), deci nu duplica ID-uri.

### 3.2 Layout-ul corect (ca în C1 și C3)
- **Sus, centrat sub cifra 4**: viteza, cifre **albe, foarte mari** (~22% din înălțimea ecranului), cu „**km/h**” mic, în dreapta.
- Dedesubt, pe două rânduri: autonomia (**ID 1080**), cu iconița pompă → mașinuță în stânga, apoi consumul mediu (**ID 1170**), cu „AVG. ⛽ A” în stânga.
- **Bara de consum instantaneu** (ID 1350 sau 1160, după caz) în **culoarea temei**. Acum e **albastră pe tema roșie**, ceea ce e greșit. Pe tema roșie bara e roșu-portocaliu (C3, C7), pe tema albastră e albastră (C1). Scala 0 – 20 – 40 dedesubt.
- **Rândul de jos**: temperatura exterioară (**ID 1000**) stânga, odometrul (**ID 1030**, „000170 km”) sau tripul (**ID 1210**) centru, ora (**ID 1050**) dreapta.
- **Stânga-sus**: iconița verde ECO și, sub ea, **treapta (ID 1040)** în portocaliu.

### 3.3 Martorii de bord – toți, la pozițiile din C2
Fiecare martor real se leagă de semnalul ETS2 corespunzător. Fie ca element UI show/hide (ID), fie ca **iconiță 3D emissive** (efect `eut2.dif.lum`) animată cu animațiile de indicator (2 keyframe-uri, off/on) de pe wiki. Pozițiile și desenele iconițelor sunt **exact cele din C2**.

| Martor real Civic | Culoare | Poziție (după C2) | Semnal ETS2 |
|---|---|---|---|
| Semnalizare stânga / dreapta (săgeți) | verde | pe streașină, sus, stânga/dreapta ecranului central | UI 1570/1580 sau `button_left_blinker` / `button_right_blinker` |
| Faza lungă | albastru | modulul drept, coloana de iconițe | UI 1590 sau `button_high_beam_lights` |
| Faza scurtă / lumini aprinse | verde | modulul drept | UI 1480 sau `button_lights` |
| Lumini de poziție | verde | modulul drept | UI 1470 sau `indicator_position_lights` |
| Proiectoare de ceață | verde | modulul drept | `indicator_aux_lights_front` |
| Frâna de mână ((P) / BRAKE) | roșu | modulul drept | UI 1270 sau `button_parking_brake` |
| Cruise control activ | verde | ecranul central sus / modulul drept | UI 1240 sau `indicator_cruise_control` |
| Combustibil puțin | chihlimbar | modulul drept, lângă indicatorul de combustibil | UI 1200 sau `button_low_fuel` |
| Baterie / încărcare | roșu | modulul stâng | `button_battery_warning` |
| Presiune ulei | roșu | modulul stâng | `indicator_low_oil_pressure` |
| Temperatură motor mare | roșu | modulul stâng | `button_water_temp` |
| Check engine (MIL) | chihlimbar | modulul stâng | UI 1190 (avertizare avarie) sau `indicator_warning` |
| Airbag, centură, ABS, VSA, TPMS | roșu/chihlimbar | modulul stâng (C2) | fără semnal în joc: desenate **stinse** (gri foarte închis, abia vizibile) |
| Butonul de avarie din consolă (triunghiul) | roșu, clipește | consola centrală | `button_4way` (aprins sau clipind odată cu avariile) |

- **Stinse**, martorii trebuie să fie **aproape invizibili** (iconiță gri închis pe negru, ca în realitate). **Aprinși**: culoare saturată, emission ~2.5, cu un mic halo/bloom. Nu suprasatura.
- Iconițele se desenează **vectorial** după C2 (forme Honda/ISO standard), se rasterizează la rezoluție mare și **nu au voie să fie neclare**.
- **Butonul fizic TRIP** (rotund, cu tijă) din colțul modulului drept (C2) se face ca geometrie.
- **Test**: screenshot-uri din joc cu semnalizare stânga, semnalizare dreapta, faze lungi, frână de mână trasă, avarii pornite și o imagine cu tot stins, puse lângă C2/C3.

### 3.4 Finisaj cluster
- Modulele laterale: segmentele de temperatură și combustibil ca în C5 și C7 (roșu cu alb). **Crosa argintie fizică** pe fiecare modul (bezel satin chrome) trebuie să fie bine vizibilă, ca în C5.
- **Cele două benzi luminoase** de pe buza streșinii, deasupra ecranului central (C3).
- Tot textul: anti-aliasing curat, fără pixeli zimțați, fără blur. Folosește texturi de rezoluție suficientă pentru UI, cu mipmaps.

---

## 4. Gurile de ventilație – refacere completă

### 4.1 Ce e greșit acum
Gurile arată ca o **grilă neagră cu pătrățele aleatorii**, plate, fără adâncime, fără lamele reale și fără cursorul cromat.

### 4.2 Gurile centrale (R4, R6)
- **Două guri late, orizontale** (~200 × 45 mm fiecare, verifică proporția pe R4), deasupra ecranului, cu **colțuri interioare rotunjite**. Între ele e **carcasa butonului de avarie**.
- **Rama**: plastic negru/gri foarte închis, ușor lucios. **O bandă subțire satin chrome** trece pe deasupra gurilor (vine din stânga, de peste cluster, și urmărește marginea de sus a zonei de ventilație; vezi R4).
- **Lamele orizontale**: **4 lamele** subțiri pe fiecare gură (numără-le pe R4), cu profil aerodinamic (muchie frontală ~2 mm, adâncime ~20 mm), egal distanțate, **negru mat**, cu bevel fin pe muchia din față, ca să prindă o linie de lumină.
- **Cursorul de reglaj**: pe **a doua lamelă de sus**, un cursor orizontal (~40 mm lățime, ~8 mm înălțime) cu **fața satin chrome**, în poziția din R4.
- **În spatele lamelelor orizontale**: **lamele verticale** (~8–10), mai retrase și mai întunecate, abia vizibile. Apoi **canalul negru mat** (fără fund vizibil, fără lumină care „scapă” și fără fețe lipsă).
- **Butonul de avarie**: carcasă neagră dreptunghiulară (~35 × 45 mm), ușor proeminentă, cu un **buton negru lucios** pe care e **triunghiul roșu** cu contur alb/roșu deschis, centrat. Triunghiul se aprinde sau clipește cu `button_4way`.

### 4.3 Gurile laterale (R5 – doar jumătatea „Before”)
- Deschidere în formă de **trapez rotunjit**, cu **ramă satin chrome** pe marginea dinspre centru și pe cea de jos (forma de „C” din R5).
- **5 lamele orizontale** (numără-le pe R5), negre mate, cu **cursor cromat** (bloc negru cu muchia de sus cromată) pe lamela din mijloc.
- **Rotița de închidere** (thumbwheel) verticală, **zimțată**, pe marginea dinspre ușă, cu marcaje.
- În spate: lamele verticale și canal negru, ca la cele centrale.
- Suprafața bordului din jur: plastic negru cu **granulație fină** (normal map), vizibilă în R5.

### 4.4 Tehnic
- Lamelele sunt **geometrie reală** (nu textură, nu alpha), cu bevel. Țintă ~600–1200 tris pe gură.
- **Ambient occlusion copt** în textura de difuz sau într-o hartă AO (dacă materialul vanilla folosit o suportă), ca adâncimea să se citească în joc.
- Satin chrome cu env map, din același efect vanilla ca la volan.
- **Test**: screenshot din joc de aproape (cameră liberă) al gurilor centrale, lângă R4, și al gurii laterale, lângă R5 „Before”.

---

## 5. Simetria volan–cluster și claritatea volanului

### 5.1 Simetrie (problema văzută acum)
În screenshot-ul meu, **centrul volanului (emblema H) e decalat spre dreapta** față de centrul ecranului central, iar cele două module laterale nu se văd simetric prin volan. Într-un Civic real, din poziția șoferului:
- **axa coloanei de direcție**, **centrul emblemei H**, **centrul ecranului central** și **axa scaunului șoferului** sunt pe aceeași verticală, adică au **aceeași coordonată X** în modelul 3D;
- prin deschiderea de sus a volanului se vede ecranul central centrat, iar **cele două module laterale apar simetric**, fiecare tăiat la fel de jantă (C10, C9).

**Ce faci:**
1. Măsoară în Blender X-ul pentru: centrul coloanei de direcție, centrul emblemei, centrul ecranului central, centrul streșinii, centrul scaunului șoferului și locatorul camerei interioare (capul). **Raportează-mi valorile.**
2. Aliniază totul pe **o singură axă X** (toleranță ≤1 mm). Corectează piesa decalată (volan, cluster sau scaun), nu muta totul la întâmplare.
3. Verifică **unghiul volanului**: înclinarea coloanei și înălțimea față de cluster, astfel încât buza de sus a jantei să taie clusterul ca în C10: ecranul central complet vizibil, iar modulele laterale văzute până aproape de margine.
4. Verifică și **rotația volanului în repaus** (spița de jos perfect verticală când roțile sunt drepte, în `wheel_anim`).
5. Screenshot din joc din camera implicită a șoferului, lângă C10.

### 5.2 Claritatea butoanelor și a inscripțiilor (R1, R2)
Acum iconițele și textele sunt neclare, iar cadrele argintii arată plate și gri. Refă-le după R1 (rezoluție 2800×1260, foarte clar):

**Spița stângă (R1, R2):**
- **Pad rotund mare cu 4 direcții**: inel negru lucios, cu **triunghiuri albe** ▲▼◀▶ imprimate. În centru, un buton rotund negru cu **„ENTER”** alb, bold, condensat.
- În dreapta padului: **basculanta de volum** verticală, curbată după conturul padului, cu **„+”** sus și **„−”** jos.
- Sub basculantă: buton rotund cu iconița **info/display** (pagini + „i”).
- **Rândul de jos, 3 butoane**: telefon (receptor ridicat) | închidere apel + back (receptor + săgeată ↩) | comandă vocală (cap cu unde).
- **Cadru satin chrome** pe marginea exterioară și jos (forma de „C”), cu profil rotunjit și reflexie vizibilă (env map), nu gri plat.

**Spița dreaptă (R1):**
- **Buton rotund mare tip basculantă**: sus **„RES +”**, în centru **„CANCEL”** (apăsare), jos **„– SET”**, plus un mic triunghi în colțul din dreapta-jos.
- **Rândul de jos**: **„CRUISE”** | buton distanță ACC (iconiță mașină cu bare) | buton **LKAS** (iconiță bandă). Pe R1, ultimele două apar fără simbol vizibil din cauza luminii; folosește iconițele standard Honda Sensing.
- Același cadru satin chrome în formă de „C”, oglindit.

**Tehnic, pentru claritate maximă:**
- Iconițele și textele: **vectoriale** (SVG sau desenate prin script), rasterizate pe o textură dedicată de **minim 2048×2048 pentru ambele panouri**, în alb pur (#F2F2F2) pe negru. Font sans-serif **bold condensat**, apropiat de cel din R1.
- Butoanele sunt **geometrie separată**, ieșită 1–1.5 mm, cu bevel, cu **rost negru** în jur.
- Textura de inscripții: **mipmaps** generate corect. Dacă ETS2 permite, aplic-o ca **decal pe un mesh separat**, ușor deasupra butonului, ca să nu fie afectată de UV-urile mari ale volanului.
- **Janta**: benzile mai deschise de la orele 10 și 2 (vizibile acum ca segmente gri) trebuie să aibă **aceeași culoare** ca restul pielii. Doar textura de perforație diferă, nu tonul.
- **Textul „SRS AIRBAG”**: embosat ton pe ton, abia vizibil (R1).
- **Cusătura**: discretă, pe muchia interioară. Pe sedanul nostru: gri închis (cusătura roșie din R1 e specifică versiunii Si).

---

## 6. Livrabile
1. Modul actualizat + `.blend`. Piesele vechi în `OLD_v3`.
2. `renders/v4/`: comparații (referință | screenshot din joc) pentru oglindă, cluster (inclusiv martorii aprinși), guri de ventilație centrale și laterale, volan (close-up pe ambele spițe) și vederea șoferului (simetria).
3. Tabelul cu coordonatele X măsurate (simetrie), înainte și după.
4. Lista martorilor implementați, cu ID-ul sau animația folosită pentru fiecare, plus ce nu se poate lega în ETS2.
5. Ce diferențe față de realitate mai știi că au rămas și de ce.
