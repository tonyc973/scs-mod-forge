# Interior Honda Civic Sedan 2020 – runda 3: realism de nivel „poză”

Am făcut progrese, dar încă nu arată ca un Civic adevărat. În runda asta sunt 4 puncte. **Punctul 1 (ceasurile de bord) e cel mai important**: vreau să nu se poată distinge de o poză reală și să funcționeze 100% (acum turația nu se vede deloc).

Standardul de acceptare pentru tot ce faci: **pui render-ul/screenshot-ul din joc lângă poza reală, la aceeași încadrare, și nu se vede diferența de formă, proporții, culori sau comportament.** Dacă se vede, nu e gata.

---

## 0. Metoda de lucru (obligatorie)

1. **Referințe**: descarcă TOATE imaginile din secțiunea 1 în `refs/v3/` (`curl -L -o`). **Deschide fiecare cu Read** înainte să atingi componenta respectivă. Pentru fiecare componentă, scrie-mi întâi 5–10 observații concrete din poze (forme, proporții, culori, detalii). Abia apoi modelezi.
2. **Suprapunere, nu „după ochi”**: pentru fiecare componentă pune poza ca *Reference Image* în Blender, din același unghi, și modelează peste ea. Pentru cluster, aliniază grafica peste poză la 50% opacitate.
3. **Comparație obiectivă**: după fiecare iterație generează `renders/v3/compare_<componenta>_vN.png` (stânga: referința, dreapta: render-ul tău, aceeași încadrare). Pentru cluster, fă în plus un **overlay 50/50** și o imagine de diferență (`magick compare` sau PIL). Deschide-le cu Read și listează diferențele. **Minim 3 iterații pe componentă**, până nu mai găsești diferențe vizibile.
4. **Verificare în joc**: totul trebuie să arate și să meargă în engine, nu doar în Blender. Identifică engine-ul din proiect și testează acolo, cu screenshot din poziția șoferului.
5. **Reproductibilitate**: tot ce generezi procedural (texturi de cluster, iconițe, grile) faci prin **scripturi Python versionate în repo** (`tools/cluster/…`), rulate prin Blender MCP sau separat. Nu edita manual nimic ce nu poate fi regenerat.
6. Piesele vechi le muți în colecția `OLD_v2` (ascunsă).

---

## 1. Referințe

### Ceasuri de bord (descarcă-le pe toate, sunt diferite ca scop)
| # | Ce arată | Link |
|---|---|---|
| C1 | **REFERINȚA PRINCIPALĂ** – ecranul central, foarte aproape, foarte clar, **km/h, °C, km**, temă albastră | https://paultan.org/image/2016/06/2016-Honda-Civic-1.5T-Premium-Instrument-Cluster-8.jpg |
| C2 | **Diagrama oficială din manualul Honda**: tot clusterul, inclusiv modulele laterale și **poziția fiecărui martor** | https://cdn.civicx.com/attachments/402/402937-e821ac52f3373dc2d0486b1946b61cff.webp |
| C3 | **Cum arată turația în mers** (80 km/h, temă roșie, banda albă umplută până la ~3500 rpm) | https://i.ytimg.com/vi/-6PUhPeIZy8/maxresdefault.jpg |
| C4 | Turația în mers, temă albastră (41 mph) | https://www.civicx.com/forum/attachments/gauge-jpg.813/ |
| C5 | Cluster roșu, parcat, tot ansamblul cu streașina | https://cdn.civicx.com/attachments/373/373667-a9e9eba93c0d5257c1f42a86acc97c97.webp |
| C6 | Comparație temă roșie (1.5 Turbo) vs albastră, cu tot binoclul și rama argintie | https://www.headlightmag.com/hlmwp/wp-content/uploads/2016/08/2016_07_12_Honda_Civic_Engine_05_Top_Speed_EDIT.jpg |
| C7 | Cluster RS 1.5 Turbo, km/h și °C, cu modulele laterale | https://d1hv7ee95zft1i.cloudfront.net/custom/blog-post-photo/gallery/2020-honda-civic-rs-turbo-digital-gauge-cluster-606a9d556a814.jpg |
| C8 | Cluster albastru 2020, foarte clar (mph, dar bun pentru layout) | https://www.motortrend.com/uploads/sites/10/2020/08/2020-honda-civic-lx-sedan-instrument-cluster.png |
| C9 | Cluster roșu 2020 sedan, văzut prin volan | https://cars.usnews.com/static/images/Auto/izmo/i159614407/2020_honda_civic_sedan_instrumentcluster.jpg |
| C10 | Poziția șoferului, cu clusterul în context (cum îl vede jucătorul) | https://carzdeluxe.com/cdn/shop/files/5_a8b57f65-72dc-49a5-b6cb-12b69e1e5a77_1445x.jpg |

### Oglinda retrovizoare interioară
- Bord complet, oglinda centrată, frontal: https://www.motortrend.com/uploads/sites/10/2020/08/2020-honda-civic-lx-sedan-dashboard.png
- Bord Si sedan, oglinda și carcasa camerei: https://cars.usnews.com/pics/size/0x0/images/Auto/izmo/i159614244/2020_honda_civic_si_sedan_dashboard.jpg

### Mânerul de plafon
- Mânerul montat în Civic (2017), în context, cu plafonul: https://i.ebayimg.com/00/s/MTE5OVgxNTk5/z/ukkAAeSwzvNn8MIL/$_57.JPG
- Mânerele demontate (forma exactă, din lateral): https://i.ebayimg.com/images/g/oEQAAOSw6uNmSEKN/s-l400.jpg

### Partea de sus a bordului (grila de lângă parbriz)
- Partea de sus a bordului, aproape de parbriz (suprafață, fanta de dezaburire, banda neagră de pe parbriz): https://carzdeluxe.com/cdn/shop/files/RHD_1148a9b6-3b56-42eb-ae7d-a1732ea017dc_1946x.jpg
- Bordul de aproape, cu gurile de ventilație și benzile decorative: https://cdn.civicx.com/attachments/310/310363-43bdb52b65ea95a2f2f47442b31a0009.webp

---

## 2. Ceasurile de bord – identice cu realitatea și 100% funcționale (PRIORITATE)

### 2.1 Ce e greșit acum
- E un **cerc complet**, cu cifrele 0–8 în jurul lui și viteza în centrul cercului. Pe un Civic nu arată așa: turometrul e un **arc de ~210°, deschis jos**, iar viteza stă **sus**, sub cifra 4.
- **Turația nu se vede deloc**: nu există nicio indicație care să se miște.
- Bara roșie de sub viteză și „km/h” sub cifră nu corespund layout-ului real.

### 2.2 Geometria exactă a ecranului central (măsurată pe C1 + C2; calibrează-o prin overlay)
Coordonatele sunt normalizate la ecranul central (0,0 = stânga-sus; 1,1 = dreapta-jos). **Raport ecran ≈ 1.4 : 1** (lățime : înălțime).
- **Centrul arcului turometrului**: (0.50, ~0.68). **Raza exterioară** ≈ 0.43 × lățimea.
- **Unghiul**: arcul pleacă de la **„0” jos-stânga** (~15° sub orizontală), urcă prin **„4” sus, pe verticală**, și coboară la **„8” jos-dreapta** (~15° sub orizontală). Total ≈ **210°**, cu scală **liniară**.
- **Inelul** are trei straturi, de la exterior spre interior:
  1. un fir subțire **alb-argintiu**;
  2. **banda colorată a temei**, groasă cam cât 4% din lățime: albastru cu gradient spre interior pe tema albastră, roșu pe tema roșie;
  3. **gradațiile**: majore la fiecare 1000 rpm (mai lungi, albe), medii la 500 și mici la 250. **Numără-le pe C1 și copiază exact.**
- **Zona roșie**: gradații și bandă **roșii** de la ~**6.5 la 8** (vezi C1: gradațiile se înroșesc de la ~6.3). Turația maximă a motorului 1.5 Turbo e ~6500.
- **Cifrele 0–8**: albe, în **interiorul** inelului, drepte (nu rotite), sans-serif condensat. „**x1000r/min**” mic, sub cifra 4.
- **Viteza**: cifre **albe, foarte mari** (~22% din înălțimea ecranului), centrate la ~(0.55, 0.30), cu „**km/h**” mic, **în dreapta**, pe linia de bază a cifrelor. Font subțire-mediu, geometric și condensat; potrivește-l prin overlay pe C1 (candidați: *DIN 1451*, *Barlow Semi Condensed*, *Roboto Condensed Light*). Grosimea traseului cifrelor trebuie să fie ca în C1.
- **Zona de informații** (sub viteză), exact ca în C1:
  - rândul 1, la ~0.52: iconiță pompă + săgeată + mașinuță, apoi „**162 km**” (autonomie);
  - rândul 2, la ~0.62: „**AVG. ⛽ A   3.3 km/l**” (sau „l/100km”, cum preferă jocul);
  - la ~0.76: **bara orizontală de consum instantaneu**, în formă de trapez întins, cu scală **0 – 20 – 40** dedesubt.
- **Rândul de jos** (~0.92): temperatura exterioară „**26 °C**” (~0.30), odometrul „**000170 km**” (~0.52), ora „**2:19**” (~0.85).
- **Colț stânga-sus** (~0.08, 0.10–0.20): iconița verde **ECON** (frunză) deasupra, iar dedesubt **indicatorul de treaptă** (pe CVT acolo e „P”/„D” roșu sau portocaliu). La manuala noastră afișăm **treapta curentă (1–6, N, R)** în aceeași poziție, culoare și mărime, plus o săgeată **▲ de upshift** când turația trece de un prag.
- **Colț dreapta-sus**: iconițele ACC și LKAS (C2, C4), stinse sau gri când nu sunt active.
- **Fundal**: negru-albastru foarte închis (#03060A), cu o **vignetă radială** discretă în interiorul arcului, ca în C1. Nu negru plat.

### 2.3 Cum se afișează TURAȚIA (comportamentul real – vezi C3 și C4)
- Nu există ac. Turația se vede ca o **bandă albă luminoasă** care **se umple de-a lungul inelului**, de la 0 până la turația curentă, **peste** banda colorată a temei.
- La capătul benzii albe (turația curentă) e un **marcaj subțire chihlimbar/portocaliu** care traversează inelul, ca un mini-ac (se vede clar în C3, la ~3500).
- Partea neumplută rămâne în culoarea temei, **mai stinsă**. Zona roșie rămâne roșie, iar când banda o atinge, devine roșu aprins.
- Răspuns: **interpolare lină** (constantă de timp ~60–80 ms), fără sărituri, cu ușoară inerție.
- **La pornirea motorului**: animație de măturare 0 → 8 → 0 în ~1.2 s, dacă jocul are contact și pornire.

### 2.4 Modulele laterale (C2, C5, C7)
- **Stânga = temperatura lichidului de răcire**: arc segmentat (~10–12 segmente, ca în C2), de la **C** (jos) la **H** (sus), cu iconița de termometru între ele.
- **Dreapta = combustibil**: arc segmentat, de la **E** (jos) la **F** (sus), cu iconița de pompă și săgeata spre partea bușonului.
- Fiecare modul are un **„crosă” argintie fizică** (bezel satin chrome, gros, foarte vizibil în C5 și C6), în formă de „J” culcat, care urmărește arcul. E geometrie, nu textură, cu bevel rotunjit.
- **Martorii**: pozițiile exacte sunt în C2. În stânga: airbag, centură, ulei, motor, baterie, ABS, TPMS etc. În dreapta: faza lungă, lumini, ceață, frâna de mână, BRAKE HOLD, AUTO HOLD. Desenează iconițele după C2, la proporțiile corecte, **stinse** în mod normal (abia vizibile, gri închis pe negru) și aprinse doar la evenimente.
- Segmentele se aprind **alb** pe culoarea temei, ca la turometru.

### 2.5 Structura fizică
- **Streașina**: plastic negru soft-touch, adâncă, cu buza curbată. Pe buza ei de sus sunt **două benzi orizontale albe-argintii, subțiri și luminoase**, deasupra ecranului central (foarte vizibile în C3 și C6). Interiorul streșinii e negru mat.
- **Două „stâlpișoare”** în V despart ecranul central de module.
- Ecranul central e ușor încastrat, **sub un geam** cu o reflexie fină (fresnel) și puțin praf sau micro-zgârieturi în roughness. Modulele laterale au și ele geam.
- Ecranele trebuie să arate **luminoase, ca un LCD**: emission ~2, fără bloom exagerat, negrul rămâne aproape negru, iar textul are **anti-aliasing curat** (fără pixeli zimțați).

### 2.6 Implementare (ca să funcționeze 100%)
- Generează grafica statică **procedural, prin script** (`tools/cluster/gen_cluster.py`, cu PIL/cairo/SVG), la **4096×2900** pentru ecranul central, cu mipmaps. Scriptul conține constantele de geometrie de mai sus, ca să le poți ajusta.
- **Banda de turație**: mesh separat cu UV radial sau un shader de *radial fill* cu parametrul `rpm01` (0–1). Unghiul de umplere = `startAngle + rpm01 × 210°`. Marcajul portocaliu e un quad mic, rotit la același unghi.
- **Viteza, treapta, autonomia, consumul, odometrul, ora, temperatura**: text dinamic randat de engine (render texture / world-space UI) cu fontul ales, nu copt în textură.
- **Temperatură și combustibil**: tot fill pe segmente (`temp01`, `fuel01`).
- **Legătura cu jocul**: o componentă `CivicCluster` cu `SetRpm(float)`, `SetSpeedKmh(float)`, `SetGear(int)`, `SetFuel01(float)`, `SetTemp01(float)`, conectată la modelul de vehicul existent. **Găsește în codul jocului de unde vin turația și viteza și leagă-le efectiv.**
- **Debug obligatoriu**: un mod de test (tastă sau flag) care plimbă turația 0→8000→0 în buclă și viteza 0→200. Fă un **GIF sau o serie de 4 screenshot-uri din joc** (800, 3000, 5500 și 7000 rpm) și compară-le cu C3/C4. Dacă turația nu se vede, verifică: legarea parametrului, ordinea de randare/z-offset față de fundal, masca și unghiul de start, și că materialul din engine e chiar cel nou.
- Tema **roșie** e implicită (motor 1.5 Turbo); tema **albastră** se comută dintr-un singur parametru.

**Criteriu de acceptare pentru cluster:** overlay-ul 50/50 cu C1 (adaptat la tema aleasă) arată arcul, cifrele, viteza și rândul de jos suprapuse aproape perfect. Screenshot-urile din joc la 3000 rpm arată ca C3.

---

## 3. Oglinda retrovizoare interioară – să reflecte SPATELE (rezolvă definitiv)

### 3.1 Problema
Oglinda arată acum **ce e în fața mașinii**: se vede prin ea sau reflectă scena din față. Asta se întâmplă când „sticla” e transparentă sau când reflexia vine din **SSR / reflection probe**. Nici una, nici alta nu poate arăta ce e în spatele camerei.

### 3.2 Soluția corectă (în engine)
- **Nu** te baza pe SSR, pe reflection probes sau pe transparență pentru oglindă.
- Implementează o **cameră de oglindă dedicată**, cu două variante:
  - **preferat: reflexie planară reală**. Camera principală se reflectă față de planul sticlei (poziție și orientare oglindite, oblique near-plane pe planul oglinzii). Rezultatul are paralaxă corectă când jucătorul mișcă capul.
  - alternativ: o cameră fixă orientată **spre spate**, la poziția oglinzii, FOV vertical ~14–18°, imagine **oglindită orizontal**.
- Ieșirea camerei merge într-o **RenderTexture** (~1024×256, același raport ca sticla) aplicată pe **sticla oglinzii**: material opac, unlit/emissive, cu luminozitate ~85% și un strat subțire de reflexie fresnel deasupra.
- **Culling**: camera vede **interiorul spate** (bancheta, tetierele, luneta, stâlpii C) și strada din spate, dar **nu** capul sau corpul jucătorului, dacă există, și nici HUD-ul.
- Near clip mic (~0.03 m), ca să nu taie bancheta. Update la fiecare frame (sau la fiecare al doilea, pentru performanță).
- Dacă **oglinzile laterale** funcționează deja corect, refolosește exact același sistem.
- **Test**: pune un obiect colorat în spatele mașinii și unul pe bancheta din spate. Fă screenshot din joc: ambele trebuie să apară în oglindă, în poziția oglindită corect (ce e în spatele-stânga apare în stânga oglinzii).

### 3.3 Geometria (după referințe)
- Carcasă **neagră, plină**, dreptunghiulară, cu colțuri mari rotunjite și laturi ușor curbate. Dimensiuni ~**250 × 65 mm**, adâncime ~30 mm, cu spatele bombat.
- **Ramă neagră subțire** (~4–5 mm) în jurul sticlei. Sticla e ușor încastrată.
- Brațul scurt se prinde de **carcasa camerei Honda Sensing**: o carcasă trapezoidală mare, din plastic negru granulat, lipită de parbriz, vizibilă în ambele poze de bord.
- Pe UV, sticla e un insule separată 0–1 cu material separat (`MAT_Mirror_RT`), ca engine-ul să poată aplica RenderTexture-ul.

---

## 4. Mânerul de plafon – refacere completă

### 4.1 Problema
Acum e un bloc low-poly, colțuros, cu o „cavitate” ciudată, umbre fațetate și un plafon cu poligoane vizibile în jurul lui.

### 4.2 Cum arată în realitate (vezi cele două poze eBay)
- **Formă**: un „U” turtit, foarte simplu și curat. Mânerul propriu-zis e o bară lungă de ~**260–280 mm**, cu secțiune **ovală turtită** (~26 × 16 mm), ușor arcuită (concavă spre plafon).
- **Capetele** coboară în **picioare** care se lărgesc spre plafon (~45 × 30 mm la bază), cu tranziție lină (fillet mare), fără muchii.
- Pe fiecare picior e un **capac mic dreptunghiular** care acoperă șurubul, cu un rost fin în jur (vezi poza cu mânerele demontate).
- Când nu e folosit, mânerul stă **rabatat lângă plafon**, cu un spațiu mic între bară și plafon.
- **Material**: plastic granulat mat, **în aceeași culoare cu plafonul** (puțin mai închis), roughness ~0.7. Nu lucios, nu alb.
- **Plafonul din jur**: suprafață **netedă, subdivizată**, fără fațete. Material textil (normal map cu țesătură fină, roughness ~0.9).
- **Verifică pe poze dacă la locul șoferului există mâner.** La multe Honda (inclusiv, după câte știu, Civic gen. 10) **șoferul nu are mâner de plafon**, doar pasagerul din față și cei din spate. Dacă referințele confirmă asta, scoate-l de deasupra ușii șoferului și păstrează-l doar unde există în realitate.
- **Modelare**: pornește de la o curbă-profil cu bevel sau de la un cub subdivizat. **Subdivision Surface nivel 2**, aplicat pentru export, cu edge loop-uri de sprijin la capete. Țintă ~1.5–2.5k tris.

---

## 5. Partea de sus a bordului – „grila” falsă cu puncte roșii/albe

### 5.1 Problema
Pe toată lățimea părții de sus a bordului, lângă parbriz, apare un **model repetitiv de puncte roșii și albe**, ca un zgomot. Arată a textură greșită sau a moiré (fără mipmaps), nu a piesă reală.

### 5.2 Cum e în realitate (vezi poza RHD și C10)
- Partea de sus a bordului e o **suprafață continuă, mată, din plastic soft-touch negru**, cu **granulație foarte fină**, ușor bombată. Fără modele, fără culori.
- Aproape de parbriz e **o singură fantă de dezaburire**: lungă, îngustă (~12–15 mm), pe aproape toată lățimea, cu **lamele negre fine** în interior, perpendiculare pe parbriz. Din poziția șoferului abia se vede, ca o linie neagră. Fă lamelele din **geometrie** (sau normal map + alpha cutout) în negru mat. **Fără roșu, fără alb.**
- La capetele bordului, lângă montanți: câte o **gură mică de dezaburire laterală**, spre geamurile laterale.
- Pe mijloc, aproape de parbriz: un **senzor mic de lumină** (dom negru, ~15 mm).
- **Pe parbriz** (pe sticlă, nu pe bord): banda neagră ceramică de margine (*frit*), cu **gradient din puncte negre** spre interior. Dacă modelul de puncte de acum voia să fie asta, mută-l pe sticlă: **negru**, nu roșu sau alb, și cu tranziția corectă.
- **Texturi**: activează **mipmaps și filtrare anizotropă (8–16×)** pe toate texturile de interior, ca să nu mai apară moiré pe suprafețele văzute în unghi.

---

## 6. Livrabile
1. `.blend` actualizat; piesele vechi în `OLD_v2`.
2. `tools/cluster/gen_cluster.py` + texturile generate + componenta `CivicCluster` legată de logica vehiculului.
3. `renders/v3/compare_*.png` pentru fiecare punct (referință | render) și `renders/v3/cluster_overlay.png`.
4. **Screenshot-uri din joc**: cluster la 800 / 3000 / 5500 / 7000 rpm; oglinda cu obiectele de test în spate; mânerul de plafon de aproape; partea de sus a bordului din poziția șoferului.
5. O notă scurtă: ce engine e, cum ai implementat oglinda, cum se leagă clusterul și ce diferențe față de realitate mai știi că au rămas.
