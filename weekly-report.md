# Nedeljni izveštaj — Nedelja 7

## Početno stanje

Komanda `python -m pytest` nije mogla da se pokrene dok nije instaliran
`pytest==8.3.3` iz `requirements.txt`. Posle instalacije, testovi prolaze:
**18 passed**.

Pokrenuta je početna evaluacija:

```text
python -m src.eval_runner --out results/before.json
```

Otisak eval skupa je:

```text
afe46db1e75a0b85bb5c9a93b6763e3b96e5cd7b289e12da6d2671e4d8650064
```

Početni rezultat je bio 6/12 prolaznih pitanja, sa retrieval hit rate 0.7778
i prosečnom citation precision 0.4545.

## Dokumentovani propusti pre izmene

| ID | Očekivanje | Šta se desilo pre izmene | Tip propusta |
| --- | --- | --- | --- |
| E04 | Odgovor sa činjenicom `5 business days` iz `hb-01` | Sistem je pronašao `hb-01`, ali su karakter-based chunkovi presecli činjenicu: citirani chunkovi nisu sadržali celu očekivanu frazu. | chunkovanje / citat |
| E06 | Trenutna politika rada na daljinu, `3 days per week`, iz `hb-03` | U oba citata se našao superseded dokument `hb-02` sa starim pravilom `2 days per week`; nije bilo retrieval hita za `hb-03`. | retrieval / pogrešan odgovor |
| E09 | Odgovor sa činjenicom `5 business days` iz `hb-01` | Kao kod E04, činjenica je bila presečena na granici karakter-based chunkova, pa nije bila u citatu. | chunkovanje / citat |

## Specifikacija jedne promene (napisana pre implementacije)

- **Propust:** E04 i E09 ne mogu da citiraju punu činjenicu zato što je odgovor
  o vremenu zamene laptopa presečen granicom chunk-a.
- **Hipoteza:** Pakovanje celih rečenica do iste granice od 140 karaktera će
  zadržati `5 business days` u jednom citabilnom chunk-u.
- **Promena:** Implementirati strategiju `sentences` u `split_text_by_sentences`
  i promeniti samo `CHUNK_STRATEGY` iz `"chars"` u `"sentences"`.
- **Očekivani efekat:** E04 i E09 prolaze zato što citat sadrži celu očekivanu
  činjenicu.
- **Rizik regresije:** Novi chunkovi menjaju dužine i leksičke skorove celog
  korpusa, pa se mogu promeniti retrieval rezultat ili citation precision i na
  pitanjima koja nisu ciljana.
- **Provera:** Pokrenuti ceo isti eval skup, uporediti ga sa `before.json` i
  ručno proveriti izmenjeno pitanje preko CLI-ja.

## Implementacija

Implementirana je jedna namerna promena: sentence-aware chunking. Funkcija
`split_text_by_sentences` normalizuje razmake, izdvaja rečenice, zatim ih pakuje
do `CHUNK_SIZE`. Rečenica duža od limita ostaje zaseban chunk, kako ne bi bila
presečena. Preklapanje se ne koristi za ovu strategiju.

Poređenje podešavanja potvrđuje da je promenjeno samo jedno podešavanje:

```text
CHUNK_STRATEGY: 'chars' -> 'sentences'
```

## Merenje posle izmene

Pokrenuto je:

```text
python -m src.eval_runner --out results/after.json
python -m src.eval_compare results/before.json results/after.json
```

Oba fajla imaju isti otisak eval skupa kao početno merenje. Rezultat posle
izmene je 9/12 prolaznih pitanja, retrieval hit rate 0.8889 i prosečna citation
precision 0.5455.

```text
Fixed (fail -> pass): E04, E06, E09
Regressed (pass -> fail): none
Unchanged: E01, E02, E03, E05, E07, E08, E10, E11, E12

Summary:
  passed: 6 -> 9 (+3)
  total: 12 -> 12 (+0)
  behaviour_accuracy: 0.8333 -> 0.8333 (+0.0)
  retrieval_hit_rate: 0.7778 -> 0.8889 (+0.1111)
  mean_citation_precision: 0.4545 -> 0.5455 (+0.091)

Changed settings:
  CHUNK_STRATEGY: 'chars' -> 'sentences'
```

E04 i E09 potvrđuju hipotezu. E06 je dodatno popravljen: promenjeni chunkovi
su doveli aktuelni dokument `hb-03` među citate. Nema regresija.

Ručna CLI provera E04 takođe daje citat `hb-01-chunk-1` koji sadrži punu
činjenicu `handover can take up to 5 business days`, uz dokument
*Equipment replacement*, verziju 2026 i status *current*.

## Preostala ograničenja

- E05 i dalje ne prepoznaje parafrazu „new notebook computer” kao zahtev za
  zamenu laptopa.
- E10 i E11 su i dalje pogrešno odgovorena umesto odbijena; sentence-aware
  chunking ne kalibriše prag za odbijanje niti uklanja near-domain šum.
- Behaviour accuracy ostaje 0.8333 zbog ta dva pogrešna odgovora za
  nepokrivena pitanja.

## Pregled para

_Dopuniti nakon pregleda drugog para: komentar na jednu promenu, podršku
rezultata i eventualno izostavljene regresije ili ograničenja._

## Doprinosi i AI beleška

- Član 1: _dopuniti_.
- Član 2: _dopuniti_.
- Osoba koja vodi demonstraciju: _dopuniti_.
- AI je korišćen za čitanje koda, izbor i implementaciju sentence-aware
  chunkovanja i nacrt izveštaja. Predlog je proveravan pokretanjem fiksnog eval
  skupa pre i posle, alatom za poređenje, ručnim CLI pozivom i testovima.
