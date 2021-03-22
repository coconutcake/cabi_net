<p align="center">
  <a href="" rel="noopener">
 <img src="http://mign.pl/img/cabinet.png" alt="Project logo"></a>
</p>

<h3 align="center">CABI_NET</h3>

<div align="center">

[![Stauts](https://img.shields.io/travis/coconutcake/cabi_net)](https://travis-ci.org/github/coconutcake/cabi_net)
[![Requirements Status](https://requires.io/github/coconutcake/cabi_net/requirements.svg?branch=main)](https://requires.io/github/coconutcake/cabi_net/requirements/?branch=main)

</div>

---

<p align="center"> Projekt apliakacji do zarządzania szafami serwerowymi
    <br> 
</p>

## 📝 Zawartość
- [O projekcie](#about)
- [Założenia projektowe](#zalozenia)
- [Technologia i metodyka](#tech)
- [Uruchomienie](#getting_started)
- [API](#api)

## 🧐 O projekcie <a name = "about"></a>  

Projekt aplikacji django umożliwiający użytkownikowi organizacje szafy serwerowej i przygotowanie dokumentacji

## 📰 Założenia projektowe <a name = "zalozenia"></a>

#### 🛳️ Konteneryzacja i usługi:
1. Utworzenie spójnego modelu konteneryzacji z uwzględnieniem plików `Dockerfile` w osobnych folderach dla każdego kontenera.
2. Utworzenie i skonfigurowanie bazy danych postgres na osobnym kontenerze dla aplikacji i testów
3. Utworzenie kontenera dla serwera upstreamowego Nginx oraz wystawienie za jego pomoca dwuch serwerów - HTTP oraz HTTPS
4. Dodatkowa konfiguracja serwera nginx - dodanie certyfikatów SSL oraz konfiguracja proxy-reverse
5. Implementacja zmiennych środowiskowych w pliku `docker-compose.yml` za pomocą których, aplikacja oraz zależne od niej kontenery będą wstępnie prekonfigowalne na etapie developingu oraz wdrażania np. dla rozwiazania chmurowego
6. Utworzenie modułu inicjującego dla aplikacji Django celem radzenia sobie z typowymi operacjami na pliku `manage.py`
---
#### 💻 Aplikacje:
1. Przekonfigurowanie modelu logowania za pomocą email i hasła
2. Dostarczenie przeglądarki API (Swagger)
3. Podział projektu na 3 aplikacje: cabinet - do zarzadzania szafą, devices - do zarzadzania urzadzeniami, companies - do zarzadzania firmami,
4. Implementacja signals do automatycznego zapisywania ilosci pozycji zgodnych z iloscia u danej szafy przy tworzeniu nowej szafy, oraz dopiecie ownera,
5. Mozliwosc dodania firmy jako adresata szafy
6. Bazowa Authentifikacja: Sesyjna, Token, Upoważnienia: dla zalogowanej osoby

---
#### 🧩 Modele aplikacji:
 Aplikacja 💻 ***"cabinet"*** - Zarządzanie szafą serwerową, implementacja mechanizmów CRUD na modelach: 
  - cabinet
  - u
  - position

Aplikacja 💻 ***"devices"*** - Zarządzanie urządzeniami szafy serwerowej, implementacja mechanizmów CRUD na modelach:
  - device
  - type
  - manufacture

Aplikacja 💻 ***"companies"*** - Zarządzanie podmiotami u których, szafy są zlokalizowane, implementacja CRUD na modelach:
  - company
  - address

---
#### Pola:
💻 **Aplikacja cabinet**:
- 🧩 ***"Cabinet"*** - Model szafy, posiada pola tj:
  - name (CharField)
  - description (TextField)
  - owner (ForeignKey <- `User`) - wskazuje na autora szafy, moze pozostac NULL
  - company (ForeignKey <- `Company`) - wskazuje na firme dla której swiadczymy daną szafe, może pozostać NULL
  - address (ForeignKey <- `Address`) - pobierze aktualne adresy firmy jesli zostanie wybrana

- 🧩 ***"u"*** - Model pozycji u szafy, posiada pola tj:
  - number (IntegerField) - wskazuje numer u

- 🧩 ***"position"*** - model pozycji szafy który, zbiera pozycje "u" oraz podpina urządzenie, posiada pola tj:
  - u (ManyToManyField <- `u`) - przypisuje pozycje z modelu "u", do wyboru są tylko wolne pozycje dla wskazanej szafy, zastosować również validacje serializera aby nie mozna bylo wybrac u której juz sa przez szafe zajete
  - description (TextField) - opis pozycji

  **metody**:
  - __str__ ma zwracać u+number

💻 **Aplikacja devices**:
- 🧩 ***"device"*** - Model urzadzania, posiada pola tj:
  - name (CharField)
  - description (TextField)
  - manufactirer (ForeignKey <- `Company`) - wskazuje na producenta urządzenia, moze pozostac NULL
  - company (ForeignKey <- `Company`) - wskazuje na firme dla której swiadczymy daną szafe, może pozostać NULL
  - address (ForeignKey <- `Address`) - pobierze aktualne adresy firmy jesli zostanie wybrana

---
## 🧑‍🔬Technologia i metodyka <a name = "tech"></a>

#### Podział kontenerów Dockera:
- Python 3.8 z django
- Baza Postgres dla django
- Adminer
- Upstream server nginx

#### Aplikacja:

- Aplikacja wykonana wg metodyki TDD. 
- Krycie testami na poziomie ~90% 
- Projekt został zintegrowany z Travis CI -> https://travis-ci.org/github/coconutcake/djangorized
- Wersje zależności requirements -> https://requires.io/github/coconutcake/djangorized/requirements/?branch=main
- Projekt wykorzystuje konteneryzacje docker wraz composerem do uruchomienia środowisk tj: aplikacji django na pythonie 3.8, bazy danych postgresql, aplikacji adminer, oraz serwer upstream nginx
- Model usera został przebudowany w celu umozliwienia logowania za pomocą email
- W projekcie wykorzystano bibliteke wait-for-it w celu kolejkowania uruchamianych kontenerów
- Folder ./initial miescie pliki inicjujace w tym ustawienia nginxa,aplikacji django
- dostepna jest przegladarka API (Swagger)


## ⚙️ Konfiguracja <a name = "config"></a>

Za pomocą `docker-compose.yml` możliwa jest konfiguracja stacku za pomocą zmiennych środowiskowych dla poszczególnych usług:

#### postgres:

```
# Nazwa bazy danych dla aplikacji
POSTGRES_DB: app

# Nazwa Usera django do logowania na baze postgres
POSTGRES_USER: django_app

# Hasło Usera aplikacji django do logowania na baze postgres
POSTGRES_PASSWORD: asdasd123
```

#### djangoapp:

```
# Adres serwera django
ADDRESS=0.0.0.0

# Port servera django
PORT=8877

# Adres servera nginx na którego bedą wysyłane zapytania (Swagger), zmień na adres cloudowy jeśli pracujesz na chmurze!
SERVER_URL=https://127.0.0.1:5555/

# Silnik bazodanowy dla django
DB_ENGINE=django.db.backends.postgresql

# Nazwa bazy danych postgres
DB_NAME=app

# Nazwa Usera django do logowania na baze postgres
DB_USER=django_app

# Hasło Usera aplikacji django do logowania na baze postgres
DB_PASSWORD=asdasd123

# Adres kontenera z bazą danych
DB_ADDRESS=postgres

# Port bazy postgres
DB_PORT=5432

# Nazwa bazy do testów
DB_TESTS=tests

# Typ uruchomianego serwera 1-developerski, 2-produkcyjny
SERVER_TYPE=1 
```

#### nginx:

```
# Adres aplikacji django, która zostanie upstremowana do servera nginx
UPSTREAM_APP_URL=djangoapp:8877

# Proxy pass
PROXY_PASS=djangoapp

# Port wystawianego servera HTTP
HTTP_SERVER_PORT=8833

# Port wystawianego servera HTTPS
HTTPS_SERVER_PORT=5555

# Ip lub domena severa (zmiana niekonieczna)
SERVER_NAME=default_server_ip
```





## 🚀 Uruchomienie <a name = "getting_started"></a>

Wykonaj klona jesli masz juz zainstalowanego dockera:
```
git clone https://github.com/coconutcake/cabi_net.git
```

Po pobraniu klona, przejdz do folderu i zbuduj obrazy poleceniem:

```
docker-compose up --build
```

Aplikacja powinna być dostępna.
Aby zalogować sie na panel administracyjny należy pierw utworzyć konto superadmina.

```
docker exec -it djangoapp sh -c "python3 app/manage.py createsuperuser"
```

jesli uzywasz Windowsa, bedziesz musial użyć winpty:

```
winpty docker exec -it djangoapp sh -c "python3 app/manage.py createsuperuser"
```


Aby sworzyc token dla utworzonego usera - USER to login (email)

```
docker exec -it djangoapp sh -c "python3 app/manage.py drf_create_token USER" 
```

Możliwe jest równiez utworzenie tokena przez wbudowany CMS


## 🚀 Uwagi końcowe <a name = "result"></a>

- Dla serwera lokalnego ADRES moze być adresem petli zwrotnej - 127.0.0.1, dla cloudowego bedzie do adres servera cloudowego. Pamietaj o konfiguracji `docker-compose.yml` opisanej w sekcji Konfiguracja
- pole <(pk)> w adreach to pk obiektu do ktorego sie odwołujemy
