# Sunetul Honda Civic 1.5 VTEC Turbo (L15B7, manuală 6 trepte) pentru mod-ul ETS2

Vreau un sunet de motor care să nu se poată distinge de mașina reală. **Am chiar mașina asta** (Civic sedan 1.5 Turbo, 182 CP, manuală), deci sursa de sunet vor fi **înregistrările mele**, nu sample-uri descărcate. Tu te ocupi de tot ce urmează după înregistrare: sincronizare, tăiere, bucle, proiectul FMOD, bank-ul, integrarea în mod și testarea.

## 0. Reguli
- Sunetul în ETS2 = **FMOD Studio** + bank-uri `.bank`. Sursa de adevăr e wiki-ul SCS: `Documentation/Engine/Sound`, `.../Sound/Modding`, `.../Sound/TruckEngine`, `.../Sound/TruckCabinFiltering`, `.../Sound/Downloads`. Plus fișierele vanilla. **Nu inventa atribute sau nume de evenimente.**
- **Versiunea FMOD Studio** trebuie să fie exact cea cerută de versiunea actuală a jocului (tabelul de pe pagina Downloads). Proiectul pornește **obligatoriu din template-ul SCS** pentru versiunea respectivă. Nu șterge bus-urile standard din template.
- Ce poți automatiza: procesarea audio în Python (`soundfile`, `numpy`, `scipy`, `librosa`). Dacă versiunea de FMOD Studio are API de scripting (JavaScript, meniul *Scripts*), scrie scripturi pentru crearea evenimentelor și a layerelor. Altfel, dă-mi pași exacți, click cu click.

## 1. Mai întâi: ghidul de înregistrare pentru mine
Scrie-mi un ghid scurt, practic (`sound/RECORDING_GUIDE.md`), după structura de mai jos. **Siguranța e prioritară**: turațiile mari doar pe un drum închis sau gol, cu un pasager care operează echipamentul, fără manevre periculoase și cu respectarea regulilor de circulație. Nimic montat lângă piese fierbinți sau în mișcare.

- **Echipament**: 2–3 surse sincronizate:
  1. **interior**: telefon sau recorder pe tetiera pasagerului / consola centrală;
  2. **evacuare**: microfon cu protecție de vânt, fixat solid la ~30–50 cm de țeavă, în afara jetului de gaze;
  3. **compartimentul motor**: doar staționar, fixat departe de curele și de galerie.
  
  WAV 48 kHz / 24 bit, vârfuri în jur de −12 dBFS.
- **Turația sincronizată**: un logger OBD (ELM327 + aplicație care salvează RPM, sarcina și clapeta în CSV, cu timestamp). La începutul fiecărei sesiuni, **o bătaie din palme** pe toate recorderele, ca să le poți alinia.
- **Lista de înregistrări**:
  1. pornire la rece, ralanti rece 60 s, ralanti cald 60 s, oprire;
  2. **turații constante la gol (în N, staționar, motor cald)**: 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000, 5500, 6000 rpm, câte ~8–10 s fiecare, fără să insiști la turații mari;
  3. **în sarcină (on-load)**: în treapta 3, accelerații lente, cu clapeta la maxim, de la ~1500 la ~6000 rpm, de 3–4 ori. Plus rampe cu clapetă parțială (~50%);
  4. **frână de motor (off-load)**: de la ~6000 la ~1500 rpm în treapta 3, fără accelerație, de 3–4 ori;
  5. **croazieră constantă** în treptele 4, 5 și 6, la ~2000, 2500 și 3000 rpm, câte 20 s;
  6. turbo: rampe în care se aude bine spool-ul și eliberarea de la ridicarea piciorului;
  7. extra (interior): schimbarea treptelor (mecanism + ambreiaj), releul semnalizării, ușa închisă, centura, claxonul (scurt, staționar).
- La fiecare înregistrare: notează treapta și ce test e, sau spune-le cu voce tare la început.

## 1b. Surse audio acceptate și formatul fișierelor de intrare

**Surse permise ca material audio în mod:**
1. înregistrările mele (preferat);
2. o bibliotecă de sunete cumpărată, cu licență care permite folosirea în mod-uri sau jocuri (salvează licența în `sound/licenses/`);
3. înregistrări publicate sub **CC0** sau CC-BY (cu atribuirea în `sound/CREDITS.md`).

**Nu folosi** audio extras din YouTube, de pe forumuri sau din alte mod-uri fără permisiunea scrisă a autorului. Clipurile acestea le poți folosi **doar ca referință de ascultare** (A/B), nu ca material în mod. Dacă primești fișiere fără licență clară, oprește-te și întreabă-mă.

**Format obligatoriu** pentru orice fișier sursă (validează-l automat la import, cu un script, și respinge ce nu corespunde):
- WAV PCM, **48 kHz, 24 bit**, **mono** pe fiecare microfon (fără mixaje stereo), vârfuri ≤ −1 dBFS, fără procesare (fără compresor, fără EQ, fără normalizare);
- denumire: `<sursa>_<test>_<treapta>_<descriere>.wav`, cu `sursa` ∈ `int` / `exh` / `bay`. Exemple: `int_onload_g3_ramp1.wav`, `exh_noload_n_3000rpm.wav`, `bay_idle_warm.wav`;
- fiecare sesiune are un `session.json` cu data, ora, temperatura exterioară, poziția microfoanelor, recorderul și offset-ul bătăii din palme (dacă îl știu);
- log OBD: CSV cu coloanele `time_s, rpm, speed_kmh, throttle_pct, load_pct` (minim `time_s, rpm`), eșantionare ≥ 5 Hz;
- structura de foldere: `sound/raw/<data_sesiunii>/{int,exh,bay,obd}/`.

## 2. Procesare (după ce îți dau fișierele)
1. **Sincronizare** audio ↔ CSV OBD după bătaia din palme (cross-correlation). Raportează decalajul găsit.
2. **Validare**: verifică pe spectrogramă că frecvența de aprindere (motor 4 cilindri, 4 timpi: **f = rpm / 30 Hz**) urmărește RPM-ul din log. Dacă nu se potrivesc, corectează sincronizarea înainte de orice altceva.
3. **Extrage bucle** pentru fiecare treaptă de turație (pas de ~500 rpm sau mai fin), separat pentru **on-load** și **off-load**, pentru **interior** și **exterior** (motor + evacuare):
   - bucle de 1–3 s, tăiate la **trecerea prin zero**, cu lungimea un multiplu de ciclul motorului la turația respectivă;
   - fără clicuri la punctul de buclă (verifică ascultând și pe formă de undă);
   - eliminare de zgomot de vânt și de drum doar dacă nu afectează motorul. Notează ce ai făcut.
4. **Normalizare consecventă** între bucle (loudness, nu vârf), ca trecerea între turații să nu aibă salturi de volum.
5. Turbo: un strat separat pentru spool/fluierat, controlat de parametrul de turbo.

## 3. Proiectul FMOD
- Evenimentele de motor din template-ul SCS (folderul `engine`): **`engine`**, **`exhaust`**, **`turbo`** (bucle 3D) și **`start_bad`** (one-shot). Parametrii documentați: `engine/play`, `engine/rpm`, `engine/load`, `engine/brake`, `engine/turbo` (+ echivalentele pentru `exhaust`).
- **Verifică pe eventul de exemplu al motorului (Downloads → Sound examples) unitatea și intervalul reale ale `engine/rpm`.** Wiki-ul e ambiguu aici. Mapează buclele pe acel interval.
- Construcție tipică (copiază tehnica din exemplul SCS):
  - layere per turație, cu **crossfade** pe `rpm` și **pitch automation** ușoară între trepte;
  - **două seturi**, on-load și off-load, amestecate după `load`. Sub ~0.05, `load` înseamnă ralanti;
  - ralanti separat la turația reală de ralanti a mașinii mele (ia-o din log).
- **Interior vs exterior**: află din pagina *TruckCabinFiltering* și din vanilla cum separă jocul sunetul din cabină de cel de afară (filtrare, ferestre deschise/închise). Folosește înregistrările de interior ca sursă principală pentru camera din cabină. **Un autoturism e mult mai silențios decât un camion**: calibrează nivelurile față de un camion vanilla, ca să nu urle.
- **Elimină sunetele de camion** care nu există la un Civic: aer comprimat, frâne pneumatice, compresor, retarder, claxonul de camion (dacă există slot, înlocuiește-l cu claxonul înregistrat). Ce nu se poate elimina, spune-mi.

## 4. Integrarea în mod
- Build bank → **Export GUIDs** → redenumește în `[bank].guids`, conform paginii *Modding*.
- Fișiere `.soundref` pentru fiecare event și intrările `sounds[]` în `accessory_engine_data`: `engine|…`, `exhaust|…`, `turbo|…`, `start_bad|…`, după modelul vanilla.
- La împachetare, fișierele din `/sound` se pun **fără compresie** (mod *store*).

## 5. Test și acceptare
- Înregistrează din joc (audio intern) aceleași manevre ca în realitate: ralanti, rampă cu accelerație maximă în treapta 3, frână de motor, croazieră la 2500 rpm în 6. Pune spectrogramele **joc vs real** una lângă alta (`sound/compare/`) și verifică:
  - frecvența de aprindere corectă la fiecare turație;
  - fără salturi de volum sau clicuri la tranziții;
  - diferența audibilă între on-load și off-load;
  - nivel interior realist față de un camion vanilla.
- Fă-mi și 4 clipuri scurte (interior și exterior, accelerare și decelerare), ca să le ascult lângă înregistrările originale.
- Raport final: ce sunet vine de unde, ce nu se poate face în ETS2 și ce înregistrări suplimentare ar mai îmbunătăți rezultatul.
