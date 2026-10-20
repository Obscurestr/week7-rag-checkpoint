# [Nedeljni izveštaj] Goran Suvačarev – Nedelja 7

*Javna kopija bez kontakt podataka; potpuna verzija dostavlja se tutoru privatno.*

## 1. Osnovne informacije

| Polje | Odgovor |
| --- | --- |
| Ime i prezime | Goran Suvačarev |
| Adresa e-pošte | Dostavlja se tutoru privatno |
| Discord korisničko ime | Dostavlja se tutoru privatno |
| Nedelja | 7 — jedno kontrolisano poboljšanje RAG sistema |
| Par / tim | Sara Trnjakov i Goran Suvačarev |
| Moj konkretan doprinos / uloga | Sa Sarom sam diskutovao o zadatku, pisao promptove i proveravao rezultate tokom rada u njenoj sesiji sa AI asistentom. U zasebnoj sesiji sam ponovo proverio kod, merenja i izveštaj i dopunio dokaze. |
| Datum predaje | 2026-10-21 (planirano) |
| Reference na rad i dokaze | Zajednički `weekly-report.md`; commit `a0dd3b0`; sačuvani rezultati `before.json`, `after.json` i njihovo poređenje. |

## 2. Moj status

**Status:** Završeno

Moj deo rada, naknadna provera i ovaj lični izveštaj su završeni. Sara je pregledala i odobrila naš zajednički rad. Predaja izveštaja je moj sledeći korak.

## 3. Rad ove nedelje

Sa Sarom sam radio na zadatku za sedmu nedelju: trebalo je izmeriti slab lokalni RAG sistem na fiksnom skupu od 12 pitanja, dokumentovati propuste, primeniti jednu promenu i uporediti rezultat pre i posle. Tokom rada u njenoj sesiji sa AI asistentom razgovarali smo o rešenju, zajedno pisali promptove i proveravali predloge i rezultate kako su nastajali. Obavezna promena bila je podela teksta po celim rečenicama, jer je početno sečenje po broju znakova razdvajalo činjenicu „5 business days“ između delova teksta koji se citiraju.

Ovu zasebnu sesiju sam iskoristio da proverim da li su kod, merenja i zajednički izveštaj međusobno usklađeni. Uz asistenta sam ponovo dobio rezultate 6/12 pre promene i 9/12 posle nje, bez regresija. Pitanja E04, E06 i E09 prešla su iz neuspeha u uspeh. Dodatni, odvojeni eksperiment sa filtriranjem dokumenata dostigao je 12/12 na istom malom skupu. Ponovljeni testovi daju 18/18 prolaznih testova, a ručna CLI provera E04 pokazuje citat koji sadrži traženu činjenicu.

Pri proveri sam uočio da sačuvani JSON rezultati nisu bili dostupni u repozitorijumu, pa su tri merenja ponovljena i sačuvana. U zajednički izveštaj dodate su pune tabele. Novi SHA-256 otisak eval datoteke razlikuje se od prvobitno navedenog zbog LF/CRLF krajeva redova na Windows checkout-u; sva tri ponovljena merenja koriste isti otisak i isti sadržaj pitanja. U obaveznom delu ostaju neuspešna E05, E10 i E11. Rezultat dodatnog eksperimenta na 12 pitanja ne dokazuje da će sistem jednako dobro raditi na novim formulacijama.

AI asistent je korišćen tokom zajedničkog rada u Sarinoj sesiji, a u ovoj sesiji za proveru koda, ponovno pokretanje merenja i uređivanje dokaza. Njegove tvrdnje proverene su rezultatom evaluacije, poređenjem, CLI izlazom i testovima. Sara je zatim pregledala i odobrila naš rad. Komentar dodeljenog drugog para nije dokumentovan u materijalima koje imam. Pomoć tutora mi trenutno nije potrebna.

## 4. Sledeći korak

Moj sledeći korak je da 21. oktobra 2026. pošaljem tutoru ovaj lični izveštaj uz zajednički izveštaj para i rezultate merenja. Korak je završen kada pošaljem mejl sa prilozima.

## 5. Poverljiva napomena za tutora

Nema dodatne napomene.
