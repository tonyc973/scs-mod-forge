# Runda 3 – addendum: adaptare la ETS2 / Prism3D (înlocuiește secțiunile 2.6, 3.2 și punctele 0.4–0.5 din v3)

Corect: e ETS2 (Prism3D), deci un mod nu rulează cod. Nu există componentă `CivicCluster`, shadere custom sau camere scriptate. **Ținta vizuală din v3 rămâne aceeași** (forme, proporții, culori, comportament). Se schimbă doar **implementarea**, care trebuie să folosească exclusiv ce oferă motorul: animații de oase legate de valori ale vehiculului, UI-ul de bord (dashboard UI) și sistemul de oglinzi al jocului.

## Reguli generale
- **Sursa de adevăr pentru sintaxă**: fișierele vanilla ale jocului (extrase cu SCS Extractor din `def.scs`, `base.scs` și arhivele DLC instalate) și wiki-ul SCS, în special pagina **„Documentation/Engine/Truck Interior Animations and IDs”** de pe modding.scssoft.com. **Nu inventa atribute .sii**: orice atribut folosit trebuie să apară într-un fișier vanilla sau pe wiki. Dacă nu îl găsești, spune-mi.
- **Copiază pattern-uri de la camioanele vanilla cu bord digital** (de exemplu Volvo FH 2024, a cărui UI de bord stă în `ui/dashboard/volvo_fh_2024/`, DAF XG/XF 2021, Scania, Renault T/E-Tech). Mai întâi notează-mi exact cum e legat display-ul lor de modelul interior (materiale, accessory, `.sii`, `.mat`/`.tobj`), apoi replică același mecanism.
- Exportul se face cu **SCS Blender Tools**. Materialele folosesc efecte `eut2.*` existente, luate de la piese vanilla similare (crom, plastic, piele, display iluminat).
- Iluminarea display-urilor: efecte de luminozitate (familia `eut2.dif.lum`), ca să funcționeze și culoarea de backlight din `dashboard_color[]`, ca la vanilla.
- **Verificarea se face în joc** (screenshot-uri din cabină). Blender e doar etapă intermediară.

---

## A. Ceasurile de bord în ETS2 (înlocuiește 2.6)

Ținta vizuală e exact cea din v3, secțiunile 2.2–2.5: arc de ~210°, viteza sus, banda albă de turație, module laterale, martori. Implementarea se împarte pe 3 straturi:

### A1. Fundal static (textură)
- Generează prin script (`tools/cluster/gen_cluster.py`) tot ce e static: fundalul cu vignetă, inelul exterior, **banda colorată stinsă** a temei, gradațiile, cifrele 0–8, „x1000r/min”, zona roșie, chenarul barei de consum, etichetele C/H, E/F și iconițele stinse ale martorilor.
- Exportă **DDS cu mipmaps** (BC7 sau BC3), rezoluție mare (minim 2048 pe latura lungă pentru ecranul central). Pune-l pe un mesh-ecran cu material luminos.

### A2. Turația = animație de oase pe segmente (fără shader)
- În ETS2, acele analogice sunt **oase animate de o animație legată de turație**: timeline-ul animației corespunde valorii. Folosește același mecanism, dar în loc de un singur ac:
  - **Banda albă care se umple**: împarte arcul de 210° în **48–64 de segmente** (quad-uri subțiri, curbate, emissive, albe). Fiecare segment are **osul lui**. În **aceeași animație de turație**, segmentul *i* trece de la scale 0 la scale 1 (sau de la ascuns la vizibil) **exact la turația lui** (`i/N × 8000 rpm`), cu o tranziție foarte scurtă. Rezultatul e o bandă care se umple progresiv, practic identică cu cea din C3/C4.
  - **Marcajul portocaliu** de la capătul benzii: un os care **se rotește** pe arc, ca un ac clasic, în aceeași animație (0 → 210°).
  - **Zona roșie** (6.5–8): segmentele din zona asta folosesc o variantă **roșu aprins** în loc de alb.
- Verifică pe wiki numele animației de turație și cum se mapează timeline-ul pe valoare (interval, unități, cadre). Uită-te și la un camion vanilla cu turometru analogic.
- **Alternativă**, dacă e mai simplu sau mai curat: wiki-ul definește pentru UI-ul de bord un element **`ui_text_bar` pentru rpm (ID 1700)**, care se taie după valoarea curentă, și un **`ui_gauge` pentru rpm (ID 1440)**. `ui_text_bar` e liniar, deci nu desenează direct un arc. Îl poți folosi doar dacă găsești o metodă vanilla documentată de a-l face să urmărească un arc. Altfel rămâi la segmentele cu oase.
- **Test obligatoriu**: screenshot-uri din joc la ~800 / 3000 / 5500 / 7000 rpm (în treapta 1–2, staționar cu turații diferite, sau în mers), comparate cu C3/C4. Dacă la vreo turație nu se vede nimic, verifică: legarea animației, ordinea/adâncimea segmentelor față de fundal (offset ~0.3–0.5 mm spre șofer) și materialul.

### A3. Text dinamic = dashboard UI al jocului
- Viteza, treapta, autonomia, consumul, odometrul/tripul, ora și temperatura exterioară vin din **UI-ul de bord** (elemente legate prin **ID-uri de dashboard**). Exemple de ID-uri de pe wiki: ora 1050, combustibil 1060/1070, autonomie 1080, consum instantaneu și mediu 1160/1170, treapta/transmisie 1380. **Ia lista completă și actuală de pe pagina wiki**, inclusiv ID-ul pentru textul vitezei și pentru odometru, care nu apar în lista de mai sus.
- Poziționează fiecare text **exact** pe coordonatele din v3 §2.2, peste fundalul static. Viteza mare, cu „km/h” mic în dreapta. Rândul de jos: temperatură, odometru, oră.
- **Fontul**: verifică ce fonturi UI există în joc și dacă un mod poate adăuga unul. Alege cel mai apropiat de C1 (condensat, geometric) și potrivește-l prin overlay. Dacă singura opțiune e un font vanilla, spune-mi care și cât de departe e de original.
- **Treapta**: verifică ce afișează ID-ul de transmisie pentru o cutie manuală (cifra treptei sau doar D/N/R). Dacă nu dă cifra, caută pe wiki un ID care o dă. Dacă nu există, spune-mi și propune cea mai apropiată variantă.
- Martorii: ID-urile de show/hide (semnalizări 1570/1580, faza lungă 1590, avertizări etc.) pe pozițiile din diagrama C2.
- Temperatura motorului și combustibilul din modulele laterale: fie animație de oase pe segmente (ca la turație), fie elementele bar din UI (temperatura apei 1150, combustibil 1070), dacă se pot așeza pe arc. Alege soluția care arată ca C5/C7.
- Opțional, pentru iterații rapide: există un editor vizual de dashboard UI pentru ETS2/ATS (mbcustoms „ETS2 Dashboard Editor”, cu documentație online). Îl poți folosi ca să înțelegi structura, dar rezultatul final trebuie să fie fișiere curate în mod.

**Criteriu de acceptare (nemodificat):** overlay-ul 50/50 cu C1 (screenshot din joc, cameră fixă frontală pe cluster) arată arcul, cifrele, viteza și rândul de jos suprapuse aproape perfect. La 3000 rpm clusterul arată ca în C3.

---

## B. Oglinda retrovizoare interioară în ETS2 (înlocuiește 3.2)

- Oglinzile din ETS2 sunt randate de joc prin **camere de oglindă**. Wiki-ul menționează tipurile **main**, **side**, **front** și **hood**, identificate printr-un **prefix de unitate de cameră**. Nu putem crea o cameră nouă din cod, dar putem **configura una dintre cele existente**.
- Pași:
  1. Găsește în vanilla și pe wiki cum se definesc unitățile de cameră pentru oglinzi (poziție, orientare, FOV) și cum se leagă **sticla** unei oglinzi de imaginea camerei respective (materialul și textura-placeholder pe care o înlocuiește jocul).
  2. **Refolosește un slot neutilizat** pentru un autoturism, de regulă cel de oglindă **front** sau **hood**, care la camioane arată fața sau bordura. Configurează-l: **poziția la oglinda interioară, orientat spre spate**, prin lunetă, cu FOV vertical îngust (~14–18°) și imagine oglindită corect.
  3. Sticla oglinzii interioare primește **materialul de oglindă** al acelui slot. Acum probabil are un material de geam transparent, de aceea „se vede în față”. **Nu** sticlă transparentă și **nu** env map.
  4. Dacă oglinzile laterale funcționează deja, folosește-le ca șablon de configurare.
- Limitări de spus clar: reflexia vine de la o cameră fixă, deci **nu** are paralaxă când jucătorul mișcă capul. Interiorul (bancheta, tetierele) apare doar dacă jocul randează interiorul în oglinzi; verifică opțiunile grafice (calitatea oglinzilor, dacă interiorul e inclus).
- **Test**: un vehicul AI în spatele mașinii trebuie să apară în oglinda centrală, pe partea corectă. Screenshot din joc.
- Geometria oglinzii (v3 §3.3) rămâne valabilă: carcasă neagră plină ~250×65 mm, ramă subțire, braț spre carcasa camerei Honda Sensing.

---

## C. Mânerul de plafon și bordul (v3 §4 și §5 rămân valabile, cu precizările astea)
- **Mânerul de plafon**: modelare normală (constrângerile ETS2 nu afectează nimic aici). Material plastic granulat mat, preluat de la un plastic de plafon vanilla. Normalele trebuie să fie netede (*custom split normals* exportate corect). Verifică în joc că nu apar fațete. Confirmă din referințe dacă la locul șoferului există mâner.
- **Partea de sus a bordului**:
  - moiré-ul se rezolvă cu **DDS cu mipmaps** și setările corespunzătoare în `.tobj`; filtrarea anizotropă e o setare a jucătorului;
  - fanta de dezaburire se face din geometrie neagră mată;
  - banda ceramică (frit) cu puncte, dacă o vrei, stă pe **textura de geam a parbrizului**, în negru.
- **Emblema H (crom)**: material cu **env map** dintr-un efect vanilla de crom din interioare, ca să reflecte fără reflection probes.

## D. Ce îmi raportezi
1. Mecanismele găsite în vanilla și pe wiki pentru: display digital, animație de turație și camere de oglindă, cu fișierele vanilla folosite ca șablon.
2. Ce din v3 nu se poate face în ETS2 și varianta cea mai apropiată aleasă, cu screenshot.
3. Screenshot-urile din joc cerute mai sus (cluster la 4 turații, oglinda cu vehicul în spate, mânerul, bordul de sus).
