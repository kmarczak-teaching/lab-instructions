# Wprowadzenie do Dockera  

## Przygotowanie środowiska
1. Otwórz stronę [https://labs.play-with-docker.com/](https://labs.play-with-docker.com/), zaloguj się (mozna kontem Google lub Github).
3. Kliknij **“Start”**, a następnie **“+ ADD NEW INSTANCE”**, aby utworzyć nową maszynę wirtualną z dostępem do Dockera.

## Podstawowe polecenia

#### Składnia poleceń Dockera - ściąga
W nowszych wersjach Dockera polecenia mają strukturę:
```bash
docker <OBIEKT> <AKCJA>
```
Najczęściej używane:
- **Kontenery:**
```bash
docker container ls # lista uruchomionych kontenerów
docker container ls -a # wszystkie kontenery (także zatrzymane)
docker container stop <ID> # zatrzymanie kontenera
docker container rm <ID> # usunięcie kontenera
docker container exec -it <ID> bash # wejście do działającego kontenera
```
- **Obrazy:**
```bash
docker image ls # lista obrazów
docker image rm <ID> # usunięcie obrazu
docker image prune # usunięcie nieużywanych obrazów
```
- **Budowanie i uruchamianie:**
```bash
docker build -t <nazwa> . # budowa obrazu z Dockerfile w tym samym folderze
docker run -d -p 8080:80 <nazwa> # uruchomienie kontenera w tle z mapowaniem portów
```
Obiekty i akcje mozna "miksować" - wyzej mamy wspomniane `docker image prune`, ale analogiczną akcję mozemy wykonać dla kontenerów przez `docker container prune`.

Skrócone wersje poleceń występujące w starszych tutorialach (np. `docker ps`, `docker images`, `docker stop`) nadal działają - są aliasami starych wersji poleceń.
  
#### Ćwiczenia 
Wywołaj w uruchomionej maszynie wirtualnej polecenia
```bash
docker --version
docker --help
docker run hello-world
```
i zapoznaj się uwaznie z wyjściem poleceń.
  
Polecenie uruchomienia kontenera `hello-world` szuka tak nazwanego *obrazu* Dockerowego lokalnie lub pobiera go (pull) z Docker Hub jeśli go nie znajdzie, a potem tworzy i uruchamia z niego kontener.
Przeczytaj szczególnie uważnie wynik ostatniego polecenia - opisuje on dość dokładnie kroki, jakie Docker wykonał uruchamiając ten kontener.
  
Sprawdź listę uruchomionych kontenerów:
```bash
docker container ls -a
```
Zwróć uwagę na status kontenera.
  
## Do czego służą kontenery
  
Zazwyczaj kontenery używane są w trzech scenariuszach:
- **A.** Uruchamianie pojedynczych komend lub narzędzi (np. testy, skrypty).  
- **B.** Praca interaktywna w środowisku Linux (np. debugowanie, eksploracja).  
- **C.** Uruchamianie usług w tle (np. baza danych, serwer www).  
  
W kolejnych ćwiczeniach zobaczymy po jednym przykładzie do każdego z tych przypadków.

### Scenariusz A - kontener wykonujący pojedyncze polecenie

Uruchom kontener `alpine`, który tylko wyświetli nazwę hosta:
```bash
docker run alpine hostname
```
Kontener zakończy pracę zaraz po wykonaniu polecenia `hostname`.
  
Sprawdź ponownie:
```bash
docker container ls -a
```
Zwróć uwagę, że proces zakończył się automatycznie - kontener działa tylko tak długo, jak działa proces główny.
  
Przed przejściem do kolejnych ćwiczeń, **usuń** dotychczas utworzone kontenery, tak aby `docker container ls -a` wyświetlał pustą listę.

###  Scenariusz B - interaktywny kontener

Uruchom kontener Ubuntu z poleceniem bash:
```bash
docker run -it ubuntu bash
```

Teraz komendy w terminalu są wykonywane **wewnątrz kontenera**. Możesz wykonywać np.:
```bash
ls
echo "Hello from inside container!"
exit
```
Host Dockera tez musi być systemem Linux. Na Windowsie Docker działa poprzez maszynę wirtualną Linux, w której uruchamiane są kontenery.
  
Uwaga: aby zachować pliki stworzone w czasie działania kontenera na maszynie hosta, nalezy uzyc tzw. wolumenów. Kontenery z załozenia są *efemryczne*, czyli tymczasowe - po usunięciu kontenera pliki z jego systemu nieodwracalnie znikają.
  
###  Scenariusz C - usługa działająca w tle (np. baza danych)
  
Uruchom bazę danych MySQL jako kontener w tle:
```bash
 docker container run \
 --detach \
 --name mydb \
 -e MYSQL_ROOT_PASSWORD=my-secret-pw \
 mysql:latest
```
Sprawdź, co oznaczają poszczególne opcje i flagi w powyzszym poleceniu, szukając online lub korzystając z lokalnej dokumentacji --help.

Sprawdź, czy kontener działa:
```bash
docker container ls
```

Zobacz logi kontenera:
```bash
docker container logs mydb
```

Spróbuj uzyskać dostęp do powłoki kontenera:
```bash
docker exec -it mydb bash
```

Zwróć uwagę, że baza działa **wewnątrz kontenera**, a nie w systemie hosta.
Teraz przetestuj kilka operacji SQL na działającej bazie:
1. logowanie do bazy
```bash
mysql -u root -p
```
2. polecenia w bazie danych
```sql
SHOW DATABASES;
CREATE DATABASE testdb;
USE testdb;
CREATE TABLE users (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(50));
INSERT INTO users (name) VALUES ('Alice'), ('Bob');
SELECT * FROM users;
```
3. wyjście z MySQL i kontenera:
```sql
exit;
```
```bash
exit
```

---
# Tworzenie własnych kontenerów - Dockerfile

## Budowanie kontenera z gotowego Dockerfile

Sklonuj gotowe repozytorium z przykładem prostej "zdockeryzowanej" strony html:
```bash
git clone https://github.com/dockersamples/linux_tweet_app.git
cd linux_tweet_app
```

Otwórz plik `Dockerfile` i przeanalizuj jego zawartość.
Zwróć uwagę na elementy:
- `FROM` - obraz bazowy,
- `RUN` - komendy wykonywane podczas budowy obrazu,
- `COPY` - kopiowanie plików z hosta do kontenera,
- `EXPOSE` - jakich portów uzywa aplikacja w kontenerze,
- `CMD` - polecenie uruchamiane przy starcie kontenera.
  
Plik `Dockerfile` jest zestawem instrukcji, na podstawie których budujemy *obraz* Dockera, z którego z kolei uruchamiamy kontener.
Zbuduj obraz poleceniem (uwaga na kropkę na końcu):
```bash
docker build -t tweetapp .
```

Uruchom serwer:
```bash
docker run -d -p 8080:80 tweetapp
```

W Play with Docker otwórz port **8080** – powinna pokazać się strona html (ładowanie strony czasem moze potrwać kilka minut).

## Tworzenie własnego obrazu Dockera

### Minimalny przykład - "aplikacja" konsolowa w Pythonie

Utwórz nowy katalog:
```bash
mkdir myapp && cd myapp
```

Utwórz plik `app.py`:
```bash
echo 'print("Hello from my Python container!")' > app.py
```

Utwórz `Dockerfile` o treści:
```Dockerfile
FROM python:3.11-alpine
COPY app.py /app.py
CMD ["python", "/app.py"]
```

Zbuduj obraz:
```bash
docker build -t mypyapp .
```

Uruchom kontener:
```bash
docker run mypyapp
```

# Zadania

## Zadanie 1
Na podstawie przykładu z `linux-tweet-app`, stwórz podobny `Dockerfile` dla plików w repozytorium https://github.com/kmarczak-uni/TDO-lab1-webpage i uruchom kontener tak, aby mozna ją było otworzyć w przeglądarce tak jak w sekcji "Budowanie kontenera z gotowego Dockerfile".

## Zadanie 2
Podobnie jak wyzej, napisać Dockerfile dla aplikacji webowej z repozytorium https://github.com/kmarczak-teaching/minimal-flask-app 
Kontener ma bazować na obrazie `python:3.11-alpine`, instalować zależności z pliku `requirements.txt` oraz uruchamić aplikację komendą `flask run --host=0.0.0.0`.  
Następnie zbudować obraz i uruchomić kontener tak, aby strona była widoczna po otwarciu portu.  
Przykład uruchomienia kontenera z poprawnie napisanego `Dockerfile`:
```bash
docker build -t myflaskapp .
docker run -d -p 8080:5000 myflaskapp
```
