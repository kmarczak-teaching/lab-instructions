Uwaga: wszędzie tam, gdzie pojawia się symbol 📝, należy zapisać odpowiedzi na zadanie (wnioski, wykonane komendy do rozwiązania) do pliku z notatkami z zajęć .txt. Na koniec ćwiczeń należy przesłać ten plik do prowadzącej w załączniku maila z tytułem: <nr_grupy> Technologie Devops Lab4.

# 1. Warstwy kontenerów

Warstwy („image layers”) w Dockerze to poszczególne kroki budowania obrazu, które są zapisywane jako oddzielne, niezmienne fragmenty. Każda instrukcja w pliku Dockerfile (np. RUN, COPY, ADD) tworzy nową warstwę. Dzięki temu Docker może ponownie wykorzystywać (cache’ować) warstwy, które się nie zmieniły, co znacząco przyspiesza i optymalizuje budowanie obrazów. Jeśli zmienimy tylko jedną część Dockerfile, Docker przebuduje tylko tę warstwę i wszystko, co jest poniżej, zamiast tworzyć cały obraz od nowa. Dodatkowo warstwy są współdzielone między obrazami, co pozwala oszczędzać miejsce na dysku i efektywniej zarządzać środowiskiem.

## 1.1 Tworzenie warstw przez `docker container commit`

Uruchom maszynę wirtualną w [Play With Docker](https://labs.play-with-docker.com/) jak na ostatnich laboratoriach. Wywołaj polecenie

```bash
docker run --name=base-container -ti ubuntu 
```

Kontener został uruchomiony w trybie interaktywnym, a więc następne polecenie zostanie wykonane w środku kontenera:

```bash
apt update && apt install -y nodejs
```

Przetestuj, czy instalacja Node się powiodła:

```bash
node -e 'console.log("Hello world!")'
```

i wyjdź z kontenera komendą `exit`.
W ten sposób w kontenerze wprowadziliśmy zmianę - zawiera on nowy, doinstalowany ręcznie pakiet. Jeśli chcemy zapisać zmianę i móc użyć tak zmieniony obraz do uruchamiania nowych kontenerów, musimy zapisać - "zacommitować", podobnie jak w git - zmianę w obrazie kontenera poleceniem wykonanym tym razem w terminalu hosta:

```bash
docker container commit -m "Add node" base-container node-base
```

Następnie sprawdź warstwy tego kontenera poleceniem

```bash
docker image history node-base
```

Teraz sprawdzamy, czy nowa wersja kontenera "node-base" rzeczywiście od razu ma zainstalowany ten pakiet:

```bash
docker run node-base node -e "console.log('Hello again')"
```

## 1.2. Warstwy w Dockerfile i optymalizacja buildów

W praktyce rzadko tworzy się warstwy za pomocą `docker container commit`, a najczęściej stosowanym sposobem jest pisanie Dockerfile. Jak wspomniano wcześniej, każda instrukcja w pliku Dockerfile (FROM, RUN, WORKDIR itd.) tworzy nową warstwę kontenera, a warstwy te są *cache'owane* tak, aby móc je ponownie użyć do kolejnego buildu i zoptymalizować w ten sposób czas oraz pamięć.  
  
Sklonuj przykładową aplikację z repozytorium Dockersamples:

```bash
git clone https://github.com/dockersamples/todo-list-app
```

oraz zbuduj kontener na podstawie umieszczonego w tych plikach Dockerfile. Zwróć uwagę i zanotuj czas wykonania buildu. Zbuduj go jeszcze raz i porównaj kolejny czas wykonania buildu. Następnie zmień w dowolny sposób zawartość pliku `src/static/index.html`, zbuduj obraz jeszcze raz i porównaj czas wykonania. 📝

Ten sam kontener można zdefiniować za pomocą różnie napisanych Dockerfiles. Oznacza to, że można napisać go w sposób bardziej optymalny, który będzie wymagał przebudowywania mniejszej liczby warstw w razie zmian w kontenerze lub aplikacji. W przypadku tej przykładowej aplikacji, zmień treść Dockerfile na taką:

```Dockerfile
FROM node:22-alpine
WORKDIR /app
COPY package.json yarn.lock ./
RUN yarn install --production
COPY . .
EXPOSE 3000
CMD ["node", "src/index.js"]
```

Porównaj do **wersji początkowej** poniżej:

```Dockerfile
FROM node:22-alpine
WORKDIR /app
COPY . .
RUN yarn install --production
EXPOSE 3000
CMD ["node", "./src/index.js"]
```

### Ćwiczenie - optymalizacja warstw Dockera 📝

Na początek spróbuj samodzielnie wywnioskować, na czym polega powyższa optymalizacja, porównując treść tych plików.  
W tym samym folderze gdzie znajduje się Dockerfile, Stwórz nowy plik o nazwie `.dockerignore` (uwaga na kropkę na początku) o treści `node_modules`.
Ponownie wykonaj po kolei polecenia:

-   zbuduj obraz z nowej wersji Dockerfile
-   ponownie zmień `src/static/index.html`
-   zbuduj obraz po powyższej zmianie.

Przy każdym kroku zanotuj czas wykonania buildu i sprawdź, czy optymalizacja wpłynęła na lepsze cache'owanie buildu wykonywanego po zmianie w statycznych plikach.

# 2. Sieci dockerowe - docker network

Docker networking określa, w jaki sposób kontenery komunikują się między sobą, z hostem oraz ze światem zewnętrznym. Docker udostępnia różne „drivery” sieciowe, z których każdy oferuje inne możliwości.

## 2.1. Domyślne typy sieci Docker

-   `bridge` (domyślna)  
Tworzy izolowaną sieć na hoście Dockera. Kontenery znajdujące się w tej samej sieci bridge mogą komunikować się za pomocą nazw kontenerów. Wystarczy pominąć opcję `--network`:

```bash
docker run -d --name web nginx
```

-   `host`  
Kontener współdzieli stos sieciowy hosta. Brak izolacji, tzn. kontener używa IP i portów hosta.

```bash
docker run --network host nginx
```

-   `none` - brak dostępu do sieci, tylko loopback

```bash
docker run --rm --network none alpine:latest ip link show
```

## 2.2 Sieci typu „user-defined bridge”

Są preferowane w porównaniu z domyślną siecią bridge, ponieważ:

-   zapewniają automatyczne rozwiązywanie nazw (DNS) między kontenerami,
-   są w pełni izolowane od innych sieci użytkownika,
-   umożliwiają dodatkową konfigurację.  

Tworzenie własnej sieci:

```bash
docker network create mynet
```

Uruchamianie kontenerów w tej sieci:

```bash
docker run -d --name app --network mynet nginx
docker run -it --name tools --network mynet alpine sh
```

Z poziomu kontenera `tools` można pingować kontener `app` odwołując się do niego przez nazwę.

## 2.3. Obsługa sieci

```bash
docker network ls
docker network inspect mynet
```

## 2.4. Podłączanie i odłączanie działających kontenerów

Podłączenie i odłączenie już uruchomionego kontenera do nowej sieci:

```bash
docker network connect mynet tools
docker network disconnect mynet tools
```

## 2.5. Mapowanie portów (-p HOST:KONTENER)

Umożliwia dostęp z hosta do kontenera:

```bash
docker run -p 8080:80 nginx
```

### Ćwiczenie — Utworzenie i przetestowanie sieci user-defined 📝

Utwórz sieć o nazwie `testnet`. Uruchom dwa kontenery w trybie `-dit` uruchamiając komendę `sh` (nazwane np. c1 i c2) oparte na obrazie alpine w tej sieci. Z kontenera c1 wykonaj ping do c2 (uzyj `docker exec`).

### Ćwiczenie — mapowanie portów

Uruchom dockera nginx, udostępniając go na porcie 9090 hosta (nginx działa na porcie 80). Zweryfikuj dostęp za pomocą polecenia `curl`.

### Ćwiczenie - podłączenie kontenera do drugiej sieci 📝

Utwórz dwie sieci: `netA` i `netB`. Uruchom dowolny prosty kontener o nazwie `test` (może być ponownie oparty na alpine) w `netA`. Podłącz `test` również do `netB`. Sprawdź, że znajduje się w obu sieciach poleceniem `inspect`.

### Ćwiczenie - porównanie host vs bridge network 📝

Uruchom trzy kontenery `nginx` w następujących konfiguracjach. W kazdym podpunkcie sprawdź, czy hostowany serwer jest dostępny za pomocą odpowiedniego wywołania `curl`, a następnie zatrzymaj kontener przed uruchomieniem kolejnego.  
-   jeden z `--network host`,
-   drugi z domyślnym bridge i opcją `-p 8080:80`
-   trzeci z domyślnym bridge bez mapowania portów   

W którym z trzech przypadków nie da się dostać do serwera i dlaczego?
  
# Zadanie domowe 

Proszę, aby do następnych zajęć przygotować:
1. Skład zespołów projektowych
Proszę wybrać grupy projektowe liczące 2–3 osoby - deklaracja składu grupy jest wiążąca do końca semestru.
2. Wstępny wybór technologii
Proszę przygotować bardzo krótki, hasłowy opis planowanych technologii, obejmujący: 
- język i/lub framework dla backendu,
- język i/lub framework dla frontendu,
- wybraną bazę danych.
Dopuszczalne są późniejsze zmiany w wybranych technologiach, pod warunkiem zgłoszenia tego prowadzącej.  
3. Utworzenie repozytorium i wykonanie zadań na GitHubie
Po ustaleniu składu grupy proszę:
- utworzyć wspólne repozytorium przez jedną osobę, 
- nadać pozostałym członkom zespołu uprawnienia do edycji, 
- wykonać kilka testowych commitów na głównym branchu (każda osoba w grupie),
- utworzyć przez każdą osobę oddzielny branch, wykonać w nich testowe commity oraz wdrozyć zmiany do main poprzez pull request. Proszę wybrać opcję bez usuwania branchy po merge'u.  
Proszę przygotować repozytorium do wglądu prowadzącej na kolejnych zajęciach.
