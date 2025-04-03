# Country API

Serwis geograficzno-informacyjny
Python + FastAPI

## Lista funkcjonalności
- CRUD + logowanie
- Listy krajów odwiedzonych przez użytkowników
- Listy krajów ulubionych przez użytkowników + ranking
- Podsumowania kontynentów

## Stos technologiczny
- Python 3.12.7
- PostgreSQL 17.0
- Docker

## Jednostki w Country
- inhabitants (mieszkańcy) - mln
- area (powierzchnia calkowita kraju) - km^2
- pkb (produkt krajowy brutto) - mld USD

## Przydatne polecenia
- Instalacja zależności produkcyjnych: `pip install -r requirements.txt`
- Instalacja zależności developerskich: `pip install -r requirements-dev.txt`
- Uruchomienie serwera aplikacyjnego: `uvicorn countryapi.main:app --host 0.0.0.0 --port 8000`
- Dokumentacja API (Swagger): `http://localhost:8000/docs`
- Zbudowanie projektu za pomocą Docker'a: `docker compose build` (w przypadku odświeżenia cache: `docker compose build --no-cache`)
- Uruchomienie projektu za pomocą Docker'a: `docker compose up` (w przypadku nieodświeżonego cache: `docker compose up --force-recreate`)
