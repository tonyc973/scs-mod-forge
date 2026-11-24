# Interior Honda Civic Sedan 2020 – runda 5 (finală), ETS2 / Prism3D

Suntem foarte aproape. Runda asta are **3 puncte** și o regulă nouă: **nicio modificare nu rămâne în mod dacă nu e dovedit mai bună.** Pentru fiecare schimbare faci un screenshot **înainte/după** din joc, cu aceeași cameră, și le pui lângă referința reală. Dacă „după” nu e clar mai aproape de referință, **revii la „înainte”**.

Constrângerile ETS2 din v3.1 și v4 rămân valabile: fără cod, doar dashboard UI cu ID-uri, animații de oase, sistemul de oglinzi al jocului și efecte `eut2.*` vanilla. Sintaxa o iei din fișierele vanilla și de pe wiki. **Nu inventa atribute.** Lucrurile care merg deja (turația, consumul, martorii, volanul, simetria) **nu le atinge**, decât dacă e strict necesar pentru punctele de mai jos.

## Referințe (în `refs/v5/`; deschide-le cu Read înainte de fiecare punct)
| # | Ce arată | Link |
|---|---|---|
| C1 | **Layout-ul ecranului central, km/h**: viteza sus și **sub ea**, pe rânduri separate, autonomia și consumul mediu | https://paultan.org/image/2016/06/2016-Honda-Civic-1.5T-Premium-Instrument-Cluster-8.jpg |
| C3 | Același layout pe tema roșie, în mers (80 km/h) | https://i.ytimg.com/vi/-6PUhPeIZy8/maxresdefault.jpg |
| C5 | Cluster roșu, parcat: rândurile Range / Average Fuel clar sub viteză | https://cdn.civicx.com/attachments/373/373667-a9e9eba93c0d5257c1f42a86acc97c97.webp |
| C7 | Cluster RS (km/h, °C), temă roșie | https://d1hv7ee95zft1i.cloudfront.net/custom/blog-post-photo/gallery/2020-honda-civic-rs-turbo-digital-gauge-cluster-606a9d556a814.jpg |
| R3 | **Ce se vede în oglinda unui Civic gen. 10**: luneta, trafic, tetiere jos; carcasa camerei și consola de plafon | https://www.civicx.com/forum/attachments/fullsizeoutput_4c72-jpeg.149745/ |
| R7 | Oglinda interioară originală (Civic 2016–2021): forma carcasei, rama subțire, prinderea | https://i.ebayimg.com/images/g/QvcAAOSwUwpnbV9b/s-l1600.jpg |
| R8 | Panoul de ușă gen. 10: **mânerul interior satin chrome** în cavitatea neagră, banda cromată, tweeter-ul din colț | https://imgd-ct.aeplcdn.com/1056x660/n/cw/ec/27074/civic-interior-front-right-door-pad.jpeg |
| R4 | Guri de ventilație centrale (de verificat, nu de refăcut) | https://imgd.aeplcdn.com/1056x594/n/cw/ec/27074/civic-interior-front-centre-air-vents.jpeg |
| W | Wiki SCS: ID-uri dashboard UI și animații | https://modding.scssoft.com/wiki/Documentation/Engine/Truck_Interior_Animations_and_IDs |

---

## 1. Cluster: autonomia și consumul se suprapun peste viteză

### 1.1 Problema
În screenshot-ul meu, viteza mare („0”) e corectă, dar **„275 km” și „36.4 l/100km” sunt scrise peste ea / lipite de ea**, în dreapta-sus, plus „km/h” care se înghesuie acolo. În realitate (C1, C3, C5) nimic nu atinge cifrele vitezei.

### 1.2 Layout-ul exact (zone verticale separate, fără nicio suprapunere)
Coordonate normalizate pe ecranul central (0,0 = stânga-sus; 1,1 = dreapta-jos). Calibrează-le prin overlay pe C1.

| Zonă | Y (de la – la) | Conținut | Aliniere |
|---|---|---|---|
| A – viteză | 0.18 – 0.42 | **Viteza (ID 1020)**, cifre albe mari | centrată la X ≈ 0.52 |
| A' – unitate | baseline-ul vitezei | „km/h” mic | **imediat în dreapta** ultimei cifre, cu spațiu de ~0.3 × lățimea unei cifre; **nu** deasupra, **nu** suprapus |
| B – autonomie | 0.47 – 0.55 | stânga (X 0.30–0.50): iconița pompă + săgeată + mașinuță; dreapta (X 0.55–0.75): **ID 1080** („162 km”) | iconița aliniată la dreapta pe 0.50, valoarea aliniată la stânga pe 0.55 |
| C – consum mediu | 0.58 – 0.66 | stânga: „AVG. ⛽ A”; dreapta: **ID 1170** („3.3 km/l” sau „l/100km”) | ca la rândul B |
| D – bară consum | 0.72 – 0.80 | bara de consum instantaneu + scala 0 – 20 – 40 dedesubt | centrată, lățime ~0.40 |
| E – rândul de jos | 0.86 – 0.95 | ID 1000 (°C) stânga · ID 1030/1210 centru · ID 1050 (oră) dreapta | ca în C1 |

Reguli:
- Calculează **bounding box-ul fiecărui element de text la valoarea lui maximă**: viteză „188” sau „200”, autonomie „1234 km”, consum „99.9 l/100km”. Verifică să **nu se intersecteze** niciun box și să nu intre peste arcul turometrului sau peste cifrele 0–8. Scrie-mi tabelul cu box-urile.
- Dacă vreun text e prea lung pentru zona lui, **micșorează fontul acelui rând**, nu-l muta peste altă zonă.
- Mărimi orientative (calibrate pe C1): viteza ≈ 0.22 din înălțimea ecranului; rândurile B și C ≈ 0.065; „km/h” ≈ 0.06; rândul E ≈ 0.06.
- **Test**: screenshot-uri din joc la 0 km/h, la 88 km/h și la 188 km/h (sau cu valori de test forțate), cu autonomie de 4 cifre. Pune-le lângă C1 și C5 și fă un overlay 50/50 cu C1.

---

## 2. Oglinda retrovizoare: e neagră și are un contur-fantomă

### 2.1 Ce se vede acum
- **Sticla e complet neagră**: nicio imagine nu ajunge în ea.
- În stânga oglinzii se vede **un contur gri, mai mare și decalat**: o rămășiță din oglinda veche (ramă sau carcasă) care nu a fost ștearsă sau e duplicată.

### 2.2 Curățenie (întâi asta)
1. Găsește în Blender și în modelul exportat **toate obiectele și subobiectele oglinzii interioare**. Trebuie să rămână **doar**: carcasa nouă, sticla nouă, brațul și carcasa camerei Honda Sensing. **Șterge conturul vechi**: verifică în `OLD_*` că nu a ajuns din greșeală în export și că nu există un mesh cu fețe pe o singură parte rămas în modelul interior sau în cel exterior.
2. Verifică ambele modele (interior **și** exterior), pentru că ETS2 poate afișa piese din ambele.

### 2.3 De ce e neagră sticla – diagnostic în pași, cu screenshot după fiecare
1. **Test de legătură**: pune temporar pe sticla oglinzii interioare **exact materialul de oglindă al oglinzii laterale stângi**, care funcționează.
   - Dacă apare imaginea din oglinda stângă, legarea sticlei funcționează, iar problema e la camera slotului ales: mergi la pasul 2.
   - Dacă tot e negru, problema e la mesh, UV sau material: UV-ul sticlei 0–1, normalele spre șofer, efectul corect, fără strat negru suprapus.
2. **Slotul de cameră**: verifică în vanilla și pe wiki dacă slotul folosit (front/hood) e **efectiv randat** pentru vehiculul nostru: definit în accessory, activ, și nedezactivat de vreo setare grafică. Dacă un slot nu e randat, încearcă celălalt slot liber.
3. **Camera vede negru pentru că e „înfundată”**: dacă imaginea vine, dar e neagră, camera pornește **în interiorul unei geometrii** sau vede întâi o suprafață neagră. De verificat:
   - carcasa oglinzii sau carcasa camerei din spatele ei;
   - **cutia de interior simplificată a modelului exterior**, care adesea e un volum negru închis;
   - **geamul lunetei din modelul exterior**, văzut din interior: dacă e opac sau negru pe fața interioară, camera nu vede afară.
   
   Soluții: mută originea camerei **ușor spre spate**, în afara oricărei geometrii (5–10 cm în spatele sticlei, în habitaclu). Fă ca luneta modelului exterior să fie **transparentă și dinspre interior** (fețe pe ambele părți sau material de geam vanilla). Deschide cutia neagră a interiorului spre lunetă.
4. **Ce trebuie să vadă camera (R3)**: interiorul spate al modelului exterior trebuie să aibă **bancheta, tetierele spate cu forma corectă, polița din spate, montanții C și rama lunetei**. Toate trebuie să fie low-poly, dar cu siluete corecte și materiale negre/gri închis. Fără ele, imaginea iese goală sau neagră jos.
5. **Încadrare** (din v4): orientată spre centrul lunetei, înclinată ~3–5° în jos; FOV ~26° orizontal / ~7° vertical; aspect ~3.8:1; stânga-dreapta oglindite corect.
6. **Test final**: screenshot din joc cu un vehicul AI în spate, lângă R3. În oglindă se văd luneta luminoasă, traficul, tetierele jos. Fă screenshot-uri ziua și noaptea (farurile din spate).

### 2.4 Dacă după toți pașii ETS2 tot nu poate randa oglinda interioară
Spune-mi clar, cu dovezile (ce slot ai încercat, ce ai văzut). **Nu lăsa sticla neagră.** Ca variantă de rezervă, pune pe sticlă un material vanilla de oglindă cu **env map** (reflexie generică a cerului, ca o oglindă înclinată în lumină). Arată mult mai natural decât negrul. Așteaptă confirmarea mea înainte de varianta asta.

### 2.5 Forma (R3, R7)
Carcasă neagră mată, aproape frameless, cu o ramă neagră de ~3 mm în jurul sticlei. Dreptunghiulară, cu laturile scurte puternic rotunjite, ~250 × 65 mm. Braț scurt spre carcasa camerei Honda Sensing (neagră, granulată, lipită de parbriz). Poziția: sus, aproape de marginea superioară a parbrizului, centrată pe mașină.

---

## 3. Rafinări fine – doar dacă A/B dovedește că arată mai bine

Fă-le **în ordinea asta**, fiecare cu screenshot înainte/după din joc, comparat cu referința. Ce nu e clar mai bine, revii.

### 3.1 Montantul A stâng – mai are „dinți” (sigur de reparat)
În screenshot, pe muchia interioară a montantului A stâng (sus, spre plafon) se văd încă **zimți negri** (forme ascuțite triunghiulare). Aplică pașii din v2 §2.1 **doar pe această piesă**:
1. Găsește n-gon-urile concave și triangulează-le curat (sau refă-le cu quad-uri).
2. *Merge by Distance*; recalculează normalele spre exterior.
3. Elimină fețele coplanare suprapuse cu plafonul sau caroseria.
4. Dă-i grosime cu Solidify.
5. Verifică și **modelul exterior**: zimții pot veni din montantul exterior văzut prin geam.

Rezultat: o suprafață netedă și continuă până în plafon.

### 3.2 Mânerul interior al ușii șoferului (R8)
Acum e **gri-alb deschis, mat**, aproape luminos. În realitate e **satin chrome** (metal periat, mai întunecat, cu reflexii), într-o **cavitate neagră adâncă**, cu o **bandă subțire cromată** pe panoul de ușă (R8). Material de crom satinat cu env map, ca la ornamentele volanului. Base color mai închis (~#9A9A9A). Cavitatea: negru mat, cu AO.

### 3.3 Ambient occlusion copt pe piesele mari (bord, consolă, uși, plafon)
Interioarele vanilla ETS2 au **AO copt în texturi**. Fără el, bordul arată plat, cu umbre „de joc”.
- Coace AO în Blender (Cycles, 128–256 samples, distanță ~0.1–0.2 m) pe bord, streașina clusterului, consolă, panourile de ușă, plafon și zona de picioare.
- Înmulțește-l **discret** în difuz (forță ~0.5–0.7), fără halouri.
- **Ținte de verificat în A/B**: îmbinările bord–parbriz, gurile de ventilație, interiorul streșinii, buzunarele ușilor, sub volan. Trebuie să capete adâncime, fără să se înnegrească totul.
- Dacă unul dintre materialele vanilla folosite are slot separat de AO sau lightmap, folosește-l în locul înmulțirii în difuz.

### 3.4 Granulația plasticului (normal map de detaliu)
Partea de sus a bordului, panourile de ușă și streașina au în realitate **granulație fină** (vezi R4 și R5 din v4, unde se vede pe bord). Dacă materialele actuale nu au normal map de granulație, adaugă unul **foarte fin, la intensitate mică**, folosind efectul vanilla cu normal map. Verifică în A/B că nu apare moiré la distanță (mipmaps).

### 3.5 Verificări finale de ansamblu (fără modificări, doar raport)
Fă un screenshot din camera implicită a șoferului, ziua, și unul noaptea, cu farurile pornite (backlight-ul clusterului și al butoanelor). Pune-le lângă o poză reală din aceeași poziție: C10 din v4 sau R4. Listează-mi **ce mai e diferit**, în ordinea vizibilității, **fără să modifici nimic** din listă fără acordul meu.

---

## 4. Livrabile
1. Mod-ul actualizat + `.blend`. Ce ai înlocuit, în `OLD_v4`.
2. `renders/v5/`:
   - cluster: overlay cu C1 + screenshot-uri la 0 / 88 / 188 km/h;
   - oglinda: fiecare pas de diagnostic + rezultatul final lângă R3;
   - A/B pentru fiecare rafinare de la punctul 3, cu verdictul tău (păstrat/revenit).
3. Tabelul cu bounding box-urile textelor din cluster.
4. Raportul pentru oglindă: ce era cauza și cum ai rezolvat. Dacă n-ai rezolvat, ce ai încercat și ce variante rămân.
5. Lista finală de diferențe față de realitate, din §3.5.
