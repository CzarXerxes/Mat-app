# Matplan

Prototype av en mobilapp som lager meny og handleliste for en valgt periode, ut fra budsjett, tilgjengelig tid, ernæringsprofil, kosthold og hensyn.

`matplan.html` er en selvstendig nettside. Åpne den i en nettleser, gjerne i mobilvisning.

- **Oppsett:** periode, personer, budsjett, måltider, maks tid, ernæringsprofil, kosthold
- **Meny:** én rett per måltid og dag, bytt enkeltretter eller lag ny variant
- **Handleliste:** samlet per butikkavdeling, med avkrysning og estimert sum
- **Pakninger og rester:** handlelisten regner hele pakninger, og menyen velges slik at åpnede pakninger blir brukt opp før de blir dårlige
- **Måltider som ikke skal planlegges:** ta ut enkeltmåltider eller gjentakende måltider (f.eks. middag på restaurant, frokost på konferanse) med årsak og notat
- **Logg:** før opp hva du faktisk spiste – som planlagt, med egne tall, eller med anslag fra beskrivelse eller bilde

Publisert som artefakt bruker appen tre tilganger: lagring på Claude-kontoen (synk mellom enheter), hvem som ser siden (for privat lagring per person) og Claude for næringsanslag. Åpnet som lokal fil lagres alt i nettleseren, og anslag gjøres grovt fra standardporsjoner.
