# 1. Przechowywania danych w Dockerze (Volumes & Bind Mounts)

Kiedy uruchamiamy kontener, zwykle ma on własny, tymczasowy system plików.
To oznacza, że jeśli kontener zostanie usunięty, wszystkie jego dane znikają.

Zwykle jest to wystarczające dla aplikacji bezstanowych, ale stanowi problem, gdy potrzebujemy zachować dane, np. logi, pliki baz danych, pliki konfiguracyjne czy inny wynik działania programu uruchomionego w kontenerze.
Aby to umożliwić, Docker udostępnia dwa główne sposoby przechowywania danych (persistance):
- bind mounts
- volumes  

Oba pozwalają przechowywać dane poza kontenerem, dzięki czemu przetrwają one nawet usunięcie kontenera.

## 1.1. Bind mount

Bind mount łączy folder na komputerze hosta z folderem wewnątrz kontenera. To co umieścimy w folderze hosta, pojawi się w folderze kontenera.
Cokolwiek kontener zapisze w zamontowanym folderze, pojawi się w folderze hosta.  
Używamy bind mount np. gdy chcemy edytować pliki bezpośrednio na komputerze i widzieć zmiany natychmiast w kontenerze, co jest wygodne w trakcie lokalnej pracy nad aplikacją.  
  
Przykład uzycia:
- folder hosta: /home/user/myproject
- folder w kontenerze: /usr/share/nginx/html  
Łączymy je przez bind mount:
```bash
docker run -d \
  --name mynginx \
  -p 8080:80 \
  -v /home/user/myproject:/usr/share/nginx/html \
  nginx
```
Folder projektu na hoście staje się katalogiem strony dla serwera Nginx.

## 1.2. Docker Volume

Volume to przestrzeń do przechowywania danych zarządzana przez Dockera.
W przeciwieństwie do bind mounts, wiele rzeczy jest zautomayzowanych za nas, m.in.:
- nie zarządza się ręcznie lokalizacją danych
- Docker przechowuje je w specjalnym folderze
- Docker dba o uprawnienia, właścicieli i spójność danych.
  
Zalety korzystania z volume:
- trudniej przypadkowo uszkodzić dane (np. nadpisać, usunąć itd)
- można je łatwo backupować i przenosić
- są bezpieczniejszym rozwiązaniem, bo nie udostępniają plików hosta kontenerowi (lepsza izolacja)
  
Przykład uzycia:
  
Najpierw tworzymy volume
```bash
docker volume create mydata
```
a potem podpinamy pod kontener:

```bash
docker run -d \
 --name mydb \
 -v mydata:/var/lib/mysql \
 mysql
```

Jak czytać opcję `-v`:
- mydata - volume zarządzany przez Dockera
- /var/lib/mysql - miejsce, gdzie MySQL przechowuje swoje dane
Nawet po usunięciu kontenera volume mydata pozostaje.  
Volume mozemy "obejrzeć" za pomocą `docker volume inspect <nazwa>`. 

### Ćwiczenie - użycie docker volume

Utwórz volume o nazwie `myvol` i uruchom kontener `alpine`, który go używa.  
Zapisz plik w kontenerze do tego volume (uzyj trybu interaktywnego `-it`, by stworzyć plik ręcznie z poziomu konsoli wewnątrz kontenera, lub polecenia `docker exec`). Usuń kontener i sprawdź, czy plik nadal istnieje z poziomu nowego kontenera, podpiętego pod ten sam volume lub zaglądając do odpowieedniego folderu na hoście.

# 2. Docker Compose

Docker Compose to narzędzie, które pozwala uruchamiać wiele kontenerów jako jeden zestaw usług. Zamiast wpisywać ręcznie
```bash
docker run ...
docker run ...
docker network create ...
docker run ...
```
opisujemy wszystkie kontenery i ich konfigurację w jednym pliku `docker-compose.yaml`, a następnie uruchamiamy pojedynczą komendą `docker compose up -d`.
  
W ten sposób ułatwiamy sobie wiele zadań - `compose` m.in.:
- tworzy wspólną sieć 
- uruchamia kontenery we właściwej kolejności 
- mapuje porty 
- montuje volumees 
- pozwala na łatwe skalowanie 
i wiele innych. 

## 2.1. Przykład - plik .yaml z jednym kontenerem 

Utwórz plik `docker-compose.yaml` i umieść w nim konfigurację (uwaga, format `yaml` wymaga bardzo dokładnego formatowania za pomocą wcięć, podobnie jak składania w języku Python):
```yaml
services:
  web:
    image: nginx
    ports:
      - "8080:80"
```
a po zapisaniu uruchom kontener za pomocą `docker compose up`. Zweryfikuj dostępność usługi w przeglądarce lub za pomocą `curl`, a następnie zatrzymaj kontener przez `docker compose down`.

## 2.2. Dodanie kolejnego konteneru 
  
Poprzedni plik rozbuduj o kolejny kontener - backend typu echo serwer, wysyłający co jakiś czas komunikat. Ponownie uruchom pojedynczą komendą i przetestuj działanie obydwu kontenerów.

```yaml
services:
  backend:
    image: alpine
    command: ["sh", "-c", "while true; do echo 'Hello from backend'; sleep 2; done"]

  web:
    image: nginx
    ports:
      - "8080:80"
```

Compose tworzy automatycznie sieć, więc oba kontenery mogą się komunikować - zweryfikuj odpowiednim poleceniem. 
Przed przejściem do kolejnego ćwiczenia zawsze zatrzymuj poprzednio uruchomione kontenery odpowiednią komendą.
  
## 2.3. Wykorzystanie lokalnego Dockerfile w pliku .yaml

Utwórz folder `app` i umieść w nim ponizsze pliki, zawierające minimalny przykładowy backend aplikacji w Node:
- plik `app/server.js`:
```js
const http = require('http');
const server = http.createServer((req, res) => {
  res.end("Hello from Node!");
});
server.listen(3000);
```
- plik `app/package.json`
```json
{
  "name": "webapp",
  "dependencies": {}
}
```
- plik Dockerfile
```Dockerfile
FROM node:22-alpine
WORKDIR /app
COPY . .
CMD ["node", "server.js"]
```
  
Plik `compose.yaml` wykonuje teraz build na podstawie lokalnego Dockerfile, dodatkowo tworząc tez bind mount do przechowywania danych:
```yaml
services:
  app:
    build: ./app
    ports:
      - "3000:3000"
    volumes:
      - ./app:/app

  nginx:
    image: nginx
    ports:
      - "8080:80"
```

## 2.4. Compose watch oraz podział na kilka plików .yaml

Wykonaj wszystkie ćwiczenia opisane w [tym tutorialu Dockera](https://docs.docker.com/compose/gettingstarted).  
Uwaga: Pierwsze 3 kroki polegają na skopiowaniu treści plików potrzebnych do pracy i mogą zostać wykonane przez sklonowanie [tego repozytorium](https://github.com/kmarczak-teaching/lab5-flask-redis).  
Zwróć szczególną uwagę na:
- optymalizację buildu w Dockerfile, o której była mowa na ostatnich zajęciach
- uzycie opcji `-d` aby uruchomić kontenery w tle, tak aby móc w obrębie jednego terminala wykonać pozostałe komendy
- zastosowanie `watch` do śledzenia zmian w plikach źródłowych oraz podział na dwa osobne plik `.yaml`.

# Zadanie domowe 

Zapoznaj się z przykładem i uruchom [usługę Prometheus i Grafana](https://github.com/docker/awesome-compose/tree/master/prometheus-grafana). Zwróć uwagę na nowe elementy w pliku `compose`, m.in. sposób definicji `volume`. Poszukaj informacji, jak mozna poprawić plik `compose` tak, aby uzytkownik i hasło do Grafany nie były podane w nim wprost.