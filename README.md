# Matplan

Prototype av en mobilapp som lager meny og handleliste for en valgt periode, ut fra budsjett, tilgjengelig tid, ernæringsprofil, kosthold og hensyn.

`matplan.html` er en selvstendig nettside. Åpne den i en nettleser, gjerne i mobilvisning.

- **Oppsett:** periode, personer, budsjett, måltider, maks tid, ernæringsprofil, kosthold
- **Meny:** én rett per måltid og dag, bytt enkeltretter eller lag ny variant
- **Handleliste:** samlet per butikkavdeling, med avkrysning og estimert sum
- **Pakninger og rester:** handlelisten regner hele pakninger, og menyen velges slik at åpnede pakninger blir brukt opp før de blir dårlige
- **Måltider som ikke skal planlegges:** ta ut enkeltmåltider eller gjentakende måltider (f.eks. middag på restaurant, frokost på konferanse) med årsak og notat
- **Logg:** før opp hva du faktisk spiste – som planlagt, med egne tall, eller med anslag fra beskrivelse eller bilde

- **Om deg:** alder, kjønn, høyde, vekt, hverdagsaktivitet og mål gir daglig kaloribehov (Mifflin-St Jeor × aktivitetsnivå ± mål)
- **Fordeling og kosekvote:** andel av dagens kalorier til frokost, lunsj, middag og faste mellommåltider; resten er kosekvote som overføres dag for dag og nullstilles mandag
- **Trening:** ukentlig treningsprogram og logg av økter med anslått forbrenning (MET-verdier), som øker dagens mål og kosekvote

- **Kropp og prognose:** målinger av vekt, mage-, nakke- og hofteomkrets med fettprosent (US Navy) og sammenlikning over tid; vektprognose fra kaloribalanse med fordeling på fett og muskler ut fra protein og styrketrening

- **Egne retter:** retter fra matkasse, kokebok eller nettside med næringsinnhold (oppgitt eller anslått), fast eller tilpasset porsjon og egne ingredienser i handlelisten; resten av uka justeres for kalorier og ernæring
- **Matvarebibliotek:** egne produkter med merke, pakningsstørrelse og næringsinnhold per 100 g/ml eller per stk (tastet inn eller lest av fra bilde av næringsdeklarasjonen); i loggen velger du produktet og hvor stor andel av pakken du brukte

Publisert som artefakt bruker appen tre tilganger: lagring på Claude-kontoen (synk mellom enheter), hvem som ser siden (for privat lagring per person) og Claude for næringsanslag. Åpnet som lokal fil lagres alt i nettleseren, og anslag gjøres grovt fra standardporsjoner.

## Installere på mobilen (Android)

`docs/` er en installerbar nettapp (PWA) med eget ikon, fullskjerm og offline-støtte. Den må ligge på en HTTPS-adresse før telefonen kan installere den:

1. **Publiser `docs/`**, for eksempel med GitHub Pages: legg repoet på GitHub, gå til *Settings → Pages → Deploy from a branch → main / docs*. Adressen blir `https://<brukernavn>.github.io/<repo>/`.
2. **Åpne adressen i Chrome på telefonen**, trykk ⋮ → *Installer app* (eller *Legg til på startsiden → Installer*).
3. Matplan ligger nå i app-skuffen og åpnes i eget vindu.

Etter endringer i `matplan.html`: kjør `python3 build_pwa.py` (krever Pillow) og publiser `docs/` på nytt. Appen oppdaterer seg selv neste gang den åpnes med nett.

I den installerte appen lagres alt lokalt på telefonen, og næringsanslag gjøres grovt fra standardporsjoner. Synk mellom enheter og anslag med Claude (også fra bilde) finnes bare i artefakt-versjonen på claude.ai.

## Flytte data mellom enheter

Under Oppsett → Sikkerhetskopi og flytting kan du lagre alt som en fil («Lagre fil») eller kopiere det som tekst («Kopier som tekst»), og lese det inn på den andre enheten. «Slå sammen» beholder det som bare finnes på enheten og bruker filen der begge har noe; «Erstatt alt» bruker bare filen. Versjonen på claude.ai synkroniserer selv via Claude-kontoen; den installerte appen lagrer bare lokalt på telefonen.
