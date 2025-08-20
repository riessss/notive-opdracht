# "Ctrl+Alt+Bios"
Voor "Ctrl+Alt+Bios" heb ik een schema generator gemaakt die elke week een nieuwe schema maakt voor de opvolgende week. De planner werkt en houd rekening met alle 

Ik heb het project geschreven in **Python** met de volgende libraries:
- Flask
- SQLAlchemy (flask_sqlalchemy)
- Standaard library: threading, requests
- Datetime (Voor het werken met datums)
- Sqlite

Ik was van plan om celery te gebruiken. Ik wist vantevoren niet dat dit niet direct gelinkt was aan flask. Ik had de models en configuratie in flask geschreven en het had me te veel tijd gekost om dit om te zetten naar celery. Vandaar dat ik het met threading heb gedaan.

### API
Voor de api heb ik uiteindelijk gekozen om the `discover/movie` api the kiezen en deze in twee functies te gebruiken. Op deze manier heb ik kunnen filteren voor:
- Populaire films: op een score van 8.5 (of hoger) en meer dan een bepaald aantal stemmen. 
- Oude films: op een release_date van 1995 of eerder en een gemiddelde score.

Ik heb er voor gekozen om de films bij het opstarten van de applicatie als thread the runnen. Om zo maar een keer de API te gebruiken en te voorkomen om te veel onnodige requests te sturen. 

### Database
Ik heb met de sqlite database gewerkt om zo snel te kunnen beginnen met het bouwen van een prototype. Daarnaast heb ik er voor gekozen om uiteindelijk alle films in de database op te slaan om ongelijkheden in de data te vermijden. Op het moment zijn er een heleboel films ingeladen aan het begin. In de realiteit zou dit op de achtergrond kunnen tijdens het runnen van de applicatie. 

Ik heb de rating en populariteit toegevoeg aan het movie model om zo data te kunnen filteren en de twee zalen appart in te kunnen delen. De datums heb ik allemaal in een datetime in de database gezet zodat het makkelijker is om de start tijden te berekenen. Daarnaast ben ik uitgegaan van een capaciteit van 50, dit had verder geen impact op andere data. Uiteindelijk heb ik de genres niet meer toegevoeg omdat ik in de tijdnood kwam, dit zou een goede toevoeging zijn om de films te kunnen filteren. Daarnaast staat het weekschema er wel in alleen wordt het op het moment niet optimaal gebruikt. Dit zou op een bepaalde manier beter verwerkt kunnen worden.

Een leuke functionaliteit zou kunnen zijn om te zoeken naar nieuwe films wekelijks en daar een van aan de database toe te voegen.

### Scheduler
De scheduler deelt elke week de films in voor de volgende week. Uiteindelijk heb ik dit deel werkend kunnen maken waar ik heel blij mee ben. Ik heb er voor gekozen om dit als thread in de app te zetten zodat als de app runt er elke week een nieuwe schema wordt gemaakt voor de opvolgende week. De week heb ik berekend door de time.sleep(...) te gebruiken. Dit is niet optimaal omdat het in een thread gebeurt, en ik heb de werking er van niet goed kunnen testen. 
Het werken met de tijden heeft me uiteindelijk veel uitzoek werk opgeleverd, hier heb ik in ieder geval van kunnen leren.

## Algemeen
Doordat ik tijdens het programmeren nieuwe dingen ontdekte, zoals bijvoorbeeld het werken met datums en tijden is de code niet zo clean als ik had gehoopt. Met name de structuur van de scheduler en add_movies kunnen verbeterd worden. Zo zijn er bijvoorbeeld een groot aantal dubbele films die in de database worden gestopt. Dit heb ik met exception handling kunnen verhelpen, alleen door de structuur en de stappen van de code heb ik nog niet uit kunnen zoeken waarom. Daarnaast ben ik in het begin veel tijd kwijt geweest met het uitzoeken van themoviedb. Dit had ik kunnen voorkomen door eerst te beginnen met uitzoeken voordat ik begin met het schrijven van code. Daarnaast had ik de opdracht graag bij jullie gemaakt om zo wat makklijker vragen te kunnen stellen. Ik heb in ieder geval veel plezier gehad van de opdracht.

### Verbeter punten
1. De sqlmodels hebben wel een Foreign Key maar op het moment kan de data nog niet makkelijk uit de database worden gehaald.
2. De week tabel sluit op het moment niet goed aan op de screeining tabel. Dit komt omdat ik niet wist hoe dat ik de week van het jaar kon koppelen aan de datum.
3. Op het moment is er geen rekening mee gehouden dat de films in de database eindig zijn. Dit zou betekenen dat na een bepaalde tijd er geen films meer in het schema kunnen. 
4. Op het moment gebruik ik threads om de taak te laten runnen. In productie is dit niet de beste methode omdat de thread verbroken kan worden en de data op dat moment niet meer klopt of niet meer uitvoert.
5. De routes kunnen een beter inzicht geven en per dag en week kunnen worden gesoorteerd. Daarnaast is er maar een route, het zou mooi zijn als dit per zaal en per dag kan worden gedaan. Bonus zou zijn als je het ook per film kan. 
6. De code komt error handling te kort en kan op een aantal plekken leesbaarder gemaakt worden.


## Quickstart
Requirements:
- Python (For install see 'https://www.python.org/downloads/')
- uv
- Een API key van the movie db in `.env`file (Zie template `example.env`)

Install uv:
```bash
pip install uv
# Or
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Run app:
```bash
cd notive_assignment
uv venv # Follow terminal for activation
uv sync
uv lock
uv run src/api/main.py
```
