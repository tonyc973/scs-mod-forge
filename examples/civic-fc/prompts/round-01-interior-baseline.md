# Refacere interior Honda Civic Sedan 2020 (gen. 10, FC facelift) – 1.5 VTEC Turbo, manuală 6 trepte

Interiorul modelat acum în Blender nu seamănă cu mașina reală. Vreau să-l refaci **componentă cu componentă**, pe baza pozelor reale de mai jos, până când un render din poziția șoferului poate fi pus lângă o poză reală fără să pară „low-effort”.

## 0. Cum lucrezi (obligatoriu)

1. **Descarcă mai întâi referințele** într-un folder `refs/` din proiect (cu `curl -L -o`), apoi **deschide fiecare imagine cu Read și uită-te la ea** înainte să modelezi componenta respectivă. Nu modela din memorie.
2. În Blender, pune referința relevantă ca **Reference Image / image plane** în spatele componentei (vedere frontală / laterală), aliniată la scară.
3. Lucrează pe **o componentă o dată**, în ordinea din secțiunea 2. După fiecare componentă:
   - fă un render (Eevee e suficient) din aceeași poziție a camerei ca în poza de referință;
   - salvează-l în `renders/<componenta>_vN.png`, deschide-l cu Read și **compară-l cu referința**;
   - scrie-mi pe scurt 3 diferențe rămase și corectează-le înainte să treci mai departe.
4. Nu șterge modelul vechi: mută-l într-o colecție `OLD_interior` (ascunsă) ca să pot compara.
5. Interiorul merge într-un joc (export spre engine), deci: topologie curată, quad-uri, **Subdivision doar unde trebuie și aplicat la un nivel rezonabil**, bevel-uri mici pe toate muchiile vizibile (nicio muchie perfect ascuțită), materiale separate pe tip (piele, plastic soft-touch, plastic granulat, piano black, satin chrome, chrome, sticlă, ecrane emissive). Poligoane: volanul ~8–15k tris, emblema ~1–2k, schimbătorul ~3–5k.

## 1. Referințe (descarcă-le pe toate)

Vedere de ansamblu / poziția șoferului
- Cockpit șofer (Civic Si Sedan 2020, același bord): https://s3.amazonaws.com/di-honda-enrollment/2020-civic-si-sedan/gallery/03-Gallery-2020-Honda-Civic-Si-Sedan-Interior-Cockpit-Driver-POV.jpg
- Cockpit din partea pasagerului: https://di-honda-enrollment.s3.amazonaws.com/2020-civic-sedan/gallery/02-Gallery-2020-Honda-Civic-Sedan-Interior-Cockpit-Passenger-Side.jpg
- Bord complet (sedan): https://cars.usnews.com/static/images/Auto/izmo/i159614407/2020_honda_civic_sedan_dashboard.jpg
- Bord complet (Si sedan, manuală): https://cars.usnews.com/pics/size/0x0/images/Auto/izmo/i159614244/2020_honda_civic_si_sedan_dashboard.jpg
- Galerie hi-res (2560×1440) cu tot interiorul sedanului 2020 – deschide pagina și alege cadrele de interior: https://www.caricos.com/cars/h/honda/2020_honda_civic_sedan/

Volan + emblemă H
- Volan frontal, sedan 2020: https://cars.usnews.com/pics/size/0x0/images/Auto/izmo/i159614407/2020_honda_civic_sedan_steeringwheel.jpg
- Volan Si sedan 2020: https://cars.usnews.com/pics/size/0x0/images/Auto/izmo/i159614244/2020_honda_civic_si_sedan_steeringwheel.jpg
- Comenzi pe volan (close-up): https://s3.amazonaws.com/di-honda-enrollment/2020-civic-si-sedan/section-images/18-steering-wheel-mounted-controls-2020-civic-si-sedan.jpg

Ceasuri de bord
- https://cars.usnews.com/static/images/Auto/izmo/i159614407/2020_honda_civic_sedan_instrumentcluster.jpg

Consolă centrală / infotainment
- https://di-honda-enrollment.s3.amazonaws.com/2020-civic-sedan/gallery/03-Gallery-2020-Honda-Civic-Sedan-Interior-Infotainment-Stack.jpg

Schimbător manual 6 trepte
- Close-up oficial Honda (sedan, manuală): https://di-honda-enrollment.s3.amazonaws.com/2020-civic-sedan/sections/34-6-speed-manual-transmission-2020-honda-civic-sedan.jpg
- Si sedan, manuală: https://s3.amazonaws.com/di-honda-enrollment/2020-civic-si-sedan/section-images/17-6-speed-manual-transmission-2020-civic-si-sedan.jpg
- Edmunds (Si sedan, schimbător): https://media.ed.edmunds-media.com/honda/civic/2020/oem/2020_honda_civic_sedan_si_shf_oem_1_500.jpg

> Atenție: unele poze de ansamblu sunt cu cutie CVT (padele în spatele volanului, maneta P-R-N-D-S). Varianta mea e **manuală**: **fără padele**, cu schimbătorul din secțiunea 2.5 și **trei pedale**. Elementele roșii/specifice „Si” din pozele cu Si **nu** le preiau – folosesc doar geometria bordului.

## 2. Componentele, în ordine

### 2.1 Emblema H de pe volan (acum arată cel mai rău – începe cu ea)
Ce e greșit acum: H-ul e gros, turtit, gri mat, proporțiile sunt de desen animat și conturul e prea lat.
Cum trebuie să fie:
- Emblema Honda reală: un **H cromat** încadrat într-un **contur cromat subțire**, în formă de trapez cu colțuri rotunjite, **mai lat sus decât jos**; laturile laterale sunt ușor curbate în afară.
- Picioarele H-ului se **evazează spre exterior în partea de sus** (sunt mai late sus); bara orizontală e subțire și așezată puțin peste jumătate.
- Spațiul dintre H și contur e **negru lucios** (piano black), ușor adâncit față de crom.
- Construcție: desenează conturul și H-ul ca **curbe 2D** după o imagine vectorială a logo-ului (aliniază-te la referința de volan), convertește în mesh, extrudă ~1.5–2 mm, apoi **bevel rotunjit** (2–3 segmente) pe muchiile frontale ca să prindă reflexii. Nu folosi o placă plată.
- Dimensiune: ~75–80 mm lățime, centrat pe capacul airbag-ului, puțin peste centrul geometric al acestuia.
- Material crom: Metallic 1.0, Roughness 0.08–0.15, Base Color aproape alb (#E8E8E8). Ai nevoie de un **HDRI** în scenă, altfel cromul pare gri plat.
- Sub emblemă, pe capac, e embosat mic textul **„SRS AIRBAG”** (normal map sau geometrie foarte fină, aproape invizibil).

### 2.2 Volanul
Ce e greșit acum: spițe groase și „bulgărite”, butoane amorfe, cusătura albă în zig-zag pe partea de sus a jantei (nu există), nicio ornamentație argintie.
Cum trebuie să fie (compară cu pozele de volan):
- Volan cu **3 spițe**, jantă groasă, piele neagră perforată pe zonele de prindere (la ora 9 și 3), cusătură **subtilă, ton pe ton/gri închis**, doar pe muchia interioară a jantei – fără linie decorativă pe partea de sus.
- **Capacul airbag-ului**: formă de „scut” rotunjit, mai lat sus, cu o linie de separație fină la margine. Suprafață ușor bombată, plastic negru soft-touch, nu lucios.
- **Spițele laterale**: fiecare are un **ornament argintiu satinat (satin chrome) în formă de „C”** care încadrează panoul de butoane – pe stânga se deschide spre centru, pe dreapta la fel, simetric. Panourile de butoane sunt **negru lucios**, ușor adâncite.
  - Stânga (facelift 2019+): butoane audio/telefon – volum +/–, track, buton de navigare cu săgeți, telefon, voce, meniu. Simboluri albe imprimate (textură, nu geometrie).
  - Dreapta: cruise control (MAIN/CANCEL, RES/+, SET/–), distanță ACC, LKAS.
- **Spița de jos**: două bare subțiri **argintii** care coboară în formă de „V” deschis, cu negru între ele, unite de jantă jos.
- **Fără padele** în spatele volanului (versiunea manuală).
- Diametru jantă ~370 mm, grosime secțiune ~32–35 mm, ușor ovalizată.

### 2.3 Ceasurile de bord
Ce e greșit acum: un simplu cerc negru cu un „0”.
Cum trebuie să fie (vezi poza de cluster):
- Cluster digital sub o **„streașină” (binnacle)** din plastic soft-touch, cu buza superioară ușor arcuită.
- În centru: **turometru circular** cu arc gradat 0–7/8 (×1000 rpm), zona roșie la final, iar **viteza digitală mare în mijlocul cercului** (cifre albe, „km/h” dedesubt).
- Stânga și dreapta: două panouri **înclinate spre șofer** cu bare/arce pentru combustibil (stânga) și temperatura motorului (dreapta), plus zona de informații (odometru, ora) jos.
- Fă ecranul ca **o singură textură emissive** (desenează-o 2048×1024, fundal aproape negru, grafică alb/roșu/albastru deschis), pe o suprafață ușor curbată, cu un **geam deasupra** (sticlă, roughness mic) ca să apară o reflexie fină.

### 2.4 Bordul și consola centrală
- Bord pe **două niveluri**: partea de sus lungă și orizontală, soft-touch negru granulat fin; dedesubt o **bandă decorativă orizontală** care traversează partea pasagerului (textură fină/ștanțată, gri închis) și se termină în guri de ventilație.
- Gurile de ventilație centrale: **două guri înguste, orizontale**, deasupra ecranului, cu **butonul de avarie** (triunghi roșu) între ele, pe un mic panou.
- **Ecranul de 7"** încastrat în consolă, ramă neagră lucioasă, cu **butonul rotativ de volum** în stânga lui (nou la facelift) și butoane fizice pe marginea stângă (Home, Back, Day/Night).
- Sub ecran: **climatronic** – două butoane rotative pentru temperatură, cu ornament argintiu, și un rând de butoane între ele.
- Sub climatronic: un **buzunar deschis** (USB, 12V), apoi tunelul cu schimbătorul.
- Butonul **ENGINE START/STOP** e rotund, cu inel argintiu și roșu, pe bord, **în dreapta coloanei volanului**, spre consolă.
- Consola centrală e **lată și înaltă**, separată de bord prin două „picioare” verticale în laterale, fiecare cu muchie argintie subțire.

### 2.5 Schimbătorul de viteze manual (refă-l complet)
Ce e greșit acum: nu seamănă deloc cu realitatea.
Cum trebuie să fie (vezi close-up-ul oficial Honda de la link-ul 34-6-speed-manual):
- **Nuca**: aproape sferică, puțin turtită sus, din **piele neagră**, diametru ~50 mm; pe capacul de sus e **schema de trepte 1–6 + R** gravată/imprimată, gri deschis. Verifică pe poză poziția lui R și copiaz-o exact.
- La baza nucii: un **inel/colier argintiu satinat** subțire (~8 mm înălțime), apoi tija se ascunde în burduf.
- **Burduful**: piele neagră, cu pliuri moi naturale (cloth simulation sau sculpt), **cusătură gri deschis** pe cusăturile verticale; se îngustează spre nucă.
- **Rama din jurul burdufului**: ornament **argintiu satinat în formă de „U”** (deschis spre spate), care încadrează burduful și coboară spre zona frânei de mână.
- În spatele schimbătorului: **frâna de mână electronică** (comutator mic, cu un „P” roșu) și butonul **BRAKE HOLD**; în dreapta, butonul **ECON** (frunză verde). Nu există manetă clasică de frână de mână.
- Mai în spate: suporturi de pahare și cotiera centrală.

### 2.6 Pedale
- Trei pedale (ambreiaj, frână, accelerație). Pentru versiunea sport: **pedale din aluminiu cu cauciucuri negre** în formă de pastile (vezi pozele de bord), plus suportul de picior din stânga.

### 2.7 Oglinda retrovizoare interioară
Ce e greșit acum: e doar un contur gol – pare o ramă fără nimic în ea.
Cum trebuie să fie: carcasă **neagră solidă**, dreptunghiulară cu colțuri rotunjite, ~250×65 mm, cu **sticlă-oglindă** reală (material metalic, roughness ~0), pe un braț scurt prins de parbriz, cu carcasa senzorilor (cameră Honda Sensing) în spate/deasupra.

### 2.8 Montanții A, plafonul și ușile
- Montanții A sunt acum zimțați/cu artefacte: refă-i ca **suprafețe netede, continue**, îmbrăcate în material textil gri închis, cu o curbură moale spre plafon.
- Panoul de ușă al șoferului: cotieră soft-touch, mânerul interior **argintiu** încastrat, panou cu butoanele geamurilor pe cotieră, difuzor jos.

## 3. Materiale și lumină
- Piele: base color #1A1A1A, roughness 0.45–0.55, normal map cu granulație fină.
- Plastic soft-touch: #141414, roughness 0.6–0.7, granulație foarte fină.
- Piano black: #050505, roughness 0.05–0.1.
- Satin chrome (ornamentele de pe volan, inelul nucii, rama burdufului): Metallic 1.0, roughness 0.25–0.35, base #B8B8B8.
- Crom lucios (emblema H): Metallic 1.0, roughness 0.08–0.15.
- Ecrane: Emission strength 1.5–3, nu supraexpune.
- Folosește un HDRI de exterior în timpul lucrului ca să vezi corect reflexiile.

## 4. Ce îmi livrezi
- `.blend` cu colecția nouă `NEW_interior` organizată pe componente (Volan, Emblema, Cluster, Bord, Consola, Schimbator, Pedale, Oglinda, Usa_sofer).
- Pentru fiecare componentă: render final lângă referința reală (side-by-side într-o singură imagine), salvat în `renders/compare_<componenta>.png`.
- Un render final din poziția șoferului, cu aceeași perspectivă ca poza „Cockpit-Driver-POV”.
- Export pentru joc (FBX/GLB, cum folosește deja proiectul), cu materialele denumite clar.
