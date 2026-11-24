# Honda Civic Sedan 2020 – runda 8 (ETS2 / Prism3D): oglinzile exterioare + partea din față a bordului

Ultimele runde au avut aceeași problemă: modificările arată bine în Blender, dar **în joc nu**, și au fost declarate rezolvate fără verificare în joc. Runda asta schimbă procesul. **Nimic nu e „gata” până nu văd eu screenshot-uri din joc care se potrivesc cu referința.**

---

## 0. Procesul obligatoriu (citește-l înainte de orice)

### 0.1 Bucla de verificare în joc
1. Faci modificarea și exportul mod-ului.
2. Îmi scrii **exact** ce screenshot-uri să fac în joc, din vederile standard de mai jos. Eu apăs **F12**.
3. Citești screenshot-urile din folderul jocului (`Documente/Euro Truck Simulator 2/screenshot/`, cel mai recent fișier; dacă n-ai acces la el, ți le trimit eu). Le deschizi cu Read și **le compari cu referința, lângă ea**.
4. Listezi diferențele rămase. Repeți până nu mai există diferențe vizibile.

**Vederi standard** (aceeași poziție de cap de fiecare dată, cu camera interioară implicită):
- **V1** – privire înainte (bord + parbriz);
- **V2** – capul întors la stânga (~60°): oglinda stângă, montantul A, ușa;
- **V3** – capul întors la dreapta (~60°): oglinda dreaptă;
- **V4** – privire în jos-înainte: partea de sus a bordului, lângă parbriz;
- **V5** – V1 noaptea, cu farurile aprinse.

### 0.2 Diagnostic prin etichetare cu culori (din runda 7)
Când nu știi ce mesh produce ce se vede în joc: dai fiecărui mesh suspect o culoare plină unică (material unlit/emissive vanilla), exporți o copie `_diag`, cer screenshot-uri și identifici sursa. **Nu ghici.**

### 0.3 Interdicții
- Nu marca nimic ca rezolvat pe baza render-urilor din Blender.
- Nu inventa atribute sau efecte. Tot ce folosești trebuie să apară în fișierele vanilla sau pe wiki-ul SCS.
- Nu modifica alte părți ale mașinii în runda asta.

---

## 1. Oglinzile exterioare – sticla „plutește” fără carcasă

### 1.1 Ce se vede acum (V2 și V3)
- **Sticla oglinzii plutește în aer**, fără carcasă în jurul ei.
- Din carcasă se vede doar **o așchie albă**, cel mai probabil câteva fețe cu normale inversate sau eliminate de backface culling.
- Lângă tweeter, în colțul geamului, apare **o pată închisă, neclară**, care pare a fi baza oglinzii cu o textură de rezoluție mică.
- Reflexia funcționează (se vede scena). Problema e geometria din jurul sticlei.

### 1.2 Cum arată oglinda reală (facelift 2019+, EU)
Referințe:
- E7 – oglinda din exterior, cu semnalizarea LED pe capac: https://www.team-bhp.com/carpics/2019-honda-civic/l/exterior/2019-honda-civic-21.jpg
- E7b – oglinda de aproape, din față-lateral (forma carcasei și a bazei; camera de sub ea e specifică Indiei, la noi **nu există**): https://www.team-bhp.com/carpics/2019-honda-civic/l/exterior/2019-honda-civic-22.jpg
- E11 – profil, poziția oglinzii pe ușă: https://www.team-bhp.com/carpics/2019-honda-civic/l/exterior/2019-honda-civic-36.jpg
- vedere din partea șoferului (oglinda văzută prin geam): https://d2ivfcfbdvj3sm.cloudfront.net/7fc965ab77efe6e0fa62e4ca1ea7673bb25940590f1e3d8e88cb/stills_0640_png/MY2019/13184/13184_st0640_174.png

Descriere:
- **Montată pe ușă**, în colțul din față-sus, pe o **bază neagră** (plastic granulat), în continuarea triunghiului interior cu tweeter.
- **Carcasa**: capac în **culoarea caroseriei** (pe partea dinspre față și sus), cu partea de jos/spate neagră. Forma e alungită, cu colțurile exterioare rotunjite și ușor ascuțită spre exterior. Pe muchia din față a capacului e **banda LED portocalie de semnalizare** (E7).
- **Sticla** e **încastrată** în carcasă, cu o **ramă neagră subțire** (~4–6 mm) de jur-împrejur. Nu iese în afara carcasei și nu plutește.
- Pe sticla **șoferului** (stânga) există **o zonă asferică** pe marginea exterioară, separată printr-o linie fină. ADAC notează la acest model că oglinda stângă are o zonă asferică suplimentară.
- **Dimensiuni**: lățimea mașinii e 1 799 mm fără oglinzi și 2 076 mm cu oglinzi, deci fiecare oglindă iese **~138 mm** dincolo de caroserie. Folosește asta ca scară pentru a măsura restul pe poze.
- **Văzută din interior** (V2), oglinda apare ca o carcasă completă și solidă: se văd spatele/interiorul carcasei, rama neagră și sticla cu reflexia. Baza neagră se vede prin geam, lângă triunghiul cu tweeter. **Nicio margine transparentă, nicio fantă.**

### 1.3 Ce faci
1. **Află cum afișează ETS2 oglinzile exterioare în vederea din interior**: ce model sau accesoriu se randează (modelul exterior? un accesoriu de oglindă cu model propriu? o variantă/parte specială pentru interior?). Uită-te la 2–3 camioane vanilla și scrie-mi pe scurt mecanismul **înainte** să modifici ceva.
2. **Etichetare cu culori** (§0.2): carcasă (roșu), ramă (galben), bază (albastru), sticlă (verde), pata de lângă tweeter (magenta). Află ce lipsește, ce e inversat și de unde vine pata.
3. **Refă oglinda ca obiect închis și solid**: carcasă cu grosime (fără fețe singure), normale spre exterior (*Recalculate Outside*, verificat cu *Face Orientation*), ramă, sticlă încastrată ~3 mm, baza pe ușă. Asigură-te că **toate piesele sunt în aceeași parte/variantă** care se vede în camera interioară.
4. **Materiale**: capac = vopseaua caroseriei (același material de vopsea ca restul mașinii, ca să urmeze culoarea aleasă); jos/spate și bază = plastic negru granulat; banda LED = lampă (semnalizare, canalul R al măștii, conform sistemului de lămpi din runda 6); sticla = materialul de oglindă care funcționează deja.
5. **Pata de lângă tweeter**: înlocuiește-o cu geometria reală a bazei (neagră, granulată, cu textură de rezoluție corectă), sau elimin-o dacă e o rămășiță.
6. **Verificare**: V2 și V3 lângă referința din partea șoferului și lângă E7. Plus o vedere din exterior (cameră liberă) a oglinzii, lângă E7b.

---

## 2. Partea din față a bordului – „pare în aer”

### 2.1 Ce se vede acum (V4)
- Bordul e o suprafață **gri deschis, plată**, cu **pete albe neregulate** pe ea.
- Lângă parbriz e **o linie neagră zimțată** („fierăstrău”) pe aproape toată lățimea.
- Imediat după muchia bordului apare direct peisajul, **fără bandă neagră pe parbriz**, așa că bordul pare suspendat.
- Cerințele pentru banda ceramică din runda 6 și 7 **nu au ajuns în joc**.

### 2.2 Cum e în realitate
Referințe:
- E12 – vederea șoferului (banda ceramică cu puncte se vede sus; jos se vede bordul): https://www.team-bhp.com/carpics/2019-honda-civic/l/exterior/2019-honda-civic-18.jpg
- C10 – poziția șoferului: https://carzdeluxe.com/cdn/shop/files/5_a8b57f65-72dc-49a5-b6cb-12b69e1e5a77_1445x.jpg
- partea de sus a bordului lângă parbriz, de aproape: https://carzdeluxe.com/cdn/shop/files/RHD_1148a9b6-3b56-42eb-ae7d-a1732ea017dc_1946x.jpg

Descriere:
- Bordul e **aproape negru** (nu gri), mat, cu **granulație fină**, uniform. Fără pete.
- Merge **până la geam**: între muchia lui și parbriz nu se vede spațiu.
- Îmbinarea bord–parbriz e ascunsă de **banda neagră ceramică** de pe geam. Jos e opacă, apoi trece printr-un **gradient de puncte negre**.
- Aproape de geam e **o singură fantă de dezaburire**, îngustă, ca o linie neagră dreaptă și curată. Nu zimțată.

### 2.3 Ce faci, pas cu pas (deterministic, nu „după ochi”)
1. **Linia zimțată**: identific-o cu etichetarea cu culori. Probabil e o textură de fantă fără mipmaps sau o geometrie fragmentată. **Șterge-o** și înlocuiește-o cu o **fantă reală**: o deschidere de ~12–15 mm lățime și ~1 000 mm lungime, la ~40 mm de geam, adâncită, cu lamele fine din geometrie (pas ~3 mm), negru mat. Din V1 trebuie să apară ca o **linie neagră dreaptă și continuă**.
2. **Distanța bord–geam**: scrie un script Blender care trimite raze de-a lungul muchiei din față a bordului (la fiecare 20 mm) spre suprafața interioară a parbrizului și raportează distanța. Ținta: **≤ 3 mm peste tot**. Prelungește sau ajustează muchia acolo unde e mai mult. Raportează valoarea maximă înainte și după.
3. **Banda ceramică**: fă-o ca **mesh separat în modelul interior**, lipit de fața interioară a parbrizului (offset 1 mm), urmând curbura lui, **nu** ca modificare a texturii geamului.
   - Calculează-i **înălțimea din punctul de vedere al șoferului**: din locatorul capului din camera interioară, trimite raze prin linia de contact bord–geam. Punctul în care raza lovește geamul, **plus 20 mm**, e limita de sus a zonei **opace**.
   - Deasupra pune **~25–30 mm de gradient din puncte negre rotunde** (mari jos, din ce în ce mai mici în sus), ca în E12.
   - Material: negru opac în zona plină. La puncte: alpha test/cutout cu un efect vanilla care suportă alpha. Verifică cum e făcută banda ceramică pe parbrizele camioanelor vanilla și copiază mecanismul. Textură cu mipmaps.
   - Banda continuă și pe **marginile laterale** ale parbrizului, de-a lungul montanților A, mai îngustă.
4. **Materialul bordului**: base color ~**#161616**, roughness ~0.75, normal map de granulație fină. **Petele albe**: identifică sursa. Candidați:
   - vertex colors (unele efecte SCS înmulțesc culoarea vertexului);
   - un AO copt cu UV-uri suprapuse;
   - lumină care trece prin fante între piese (umbre);
   - specular prea mare.
   
   Repară cauza, nu o masca. Raportează ce era.
5. **Verificare**: V1 și V4 ziua, plus V5 noaptea, lângă E12 și C10. În V1 trebuie să se vadă, de jos în sus: bord negru mat → banda ceramică → drumul. Fără linie zimțată, fără pete albe, fără spațiu.

---

## 3. Dacă oglinda interioară nu e încă rezolvată
Continuă exact cu pașii din runda 7, §3: etichetare cu culori, test cu materialul oglinzii laterale, tehnica învățată din 2–3 mod-uri de mașini cu oglindă interioară funcțională. Raportează separat stadiul ei, cu screenshot din V1.

---

## 4. Ce îmi livrezi
1. Mecanismul ETS2 pentru oglinzile exterioare în vederea din interior (§1.3.1), cu fișierele vanilla studiate.
2. Rezultatul etichetării cu culori, pentru oglinzi și pentru bord (ce era fiecare problemă).
3. Distanța bord–geam (maximă înainte și după) și calculul înălțimii benzii ceramice.
4. **Screenshot-uri din joc** V1–V5, fiecare lângă referința ei, cu lista diferențelor rămase. Dacă lista nu e goală, continuă iterația.
