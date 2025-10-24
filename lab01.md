### Podstawy gita
1. Utworzyć nowy folder a w nim zainicjalizować nowe repozytorium `git`. Przed jakąkowliek zmianą, sprawdzić efekt komend `git status` i `git diff`.
2. Utworzyć w folderze nowy plik `.txt` z dowolną zawartością, ponownie wywołać komendy `git status`, `git diff` oraz `git diff --staged`, zaobserwować zmiany.
3. Dodać zmiany (*stage*) za pomocą komendy `git add`, ponownie wykonać `git status`, `git diff` oraz `git diff --staged`.
4. Wykonać pierwszy *commit* za pomocą `git commit -m "my 1st commit"` lub podobną, sprawdzić `status`, `diff`  oraz wynik komendy `git log`.
5. Wprowadzić jeszcze jedną dowolną zmianę w pliku lub nowy plik i zrobić commit, tak aby w historii repozytorium były dwa rózne commity.
### Usuwanie i przywracanie plików
6. Usunąć całkowicie plik `.txt` z folderu np. przez `Shift-Delete` (w systemie Windows zwykle nieodwracalnie usuwa to plik z pominięciem kosza). Ponownie sprawdzić `status` oraz `diff`. Przywrócić plik zgodnie z podpowiedzią systemu git.
7. Dodać nowy plik w folderze, zacommitować, a następnie usunąć z dysku. Tym razem zmianę polegającą na usunięciu pliku zatwierdzić kolejnym commitem. 
(git checkout HEAD^ -- deleted_file.txt)
### Podstawy branchowania  
8. Utworzyć nowy *branch*. Obecnie powszechnie stosuje się do tego dwie komendy:
- wykonać polecenie `git branch feature-a` a następnie `git switch feature-a`.  Dokonać dowolnej zmiany w pliku, wykonać commit a następnie wrócić do głównego brancha za pomocą `git switch main`. Sprawdzić np. w notatniku, czy wprowadzona na branchu `feature-a` zmiana jest w nim widoczna oraz sprawdzić `git log`.
- powtórzyć całe powyzsze ćwiczenie z nowym branchem nazwanym `feature-b`, wykorzystując do tego polecenie `git checkout` (parametry znaleźć samodzielnie w dokumentacji).
- wrócić do `main` i wdrozyć (*merge / zmerge'ować*) zmiany z obydwu utworzonych powyzej branchy do `main` za pomocą polecenia `git merge`.
### Rozwiązywanie konfliktów
9. Stworzyć nowy plik, np. `conflict.txt` z jedną linijką, zacommitować. Utworzyć nowy branch np. `bugfix-a` i na tym branchu zmienić (oraz zacommitować) treść pliku `conflict.txt`. Następnie **wrócić na `main`** i utworzyć nowy branch `bugfix-b`, równiez na tym branchu wprowadzić zmiany w pliku `conflict.txt`, inne niz te na branchu `bugfix-a`.
Wrócić na `main`, zmerge'ować `bugfix-a`, a następnie zmerge'ować `bugfix-b`. Ostatnia operacja powinna zgłosić *merge conflict*, który rozwiązujemy (*resolve*) ręcznie edytując plik będący źródłem konfliktu tak, aby pozostały wybrane przez nas zmiany (usuwamy zmiany odrzucone oraz *markery* konfliktu, czyli oznaczenia `<<<<<<< HEAD`, `======` itd.)
Po ręcznej edycji i zapisaniu docelowej, "zwycięskiej" wersji nalezy zmianę wprowadzić jak dotychczas przed `add` a następnie `commit`, przykładowo z odpowiednim *commit message*, np. `resolve merge conflict between bugfix-a and bugfix-b`.
### .gitignore
10. Utworzyć plik `.gitignore`, w którym nalezy wpisać treść: `*.md`, zacommitować. Następnie utworzyć plik `notatki.md` z dowolną zawartością. Za pomocą `git status` sprawdzić, czy nowy plik `.md` został wykryty w lokalnych zmianach.
  
### Ćwiczenie / zadanie domowe
1. Ściągnąć z repozytorium https://github.com/kmarczak-uni/TDO-lab1-webpage wszystkie pliki za pomocą opcji `Download ZIP` (tak, aby ściągnąć same pliki, bez zainicjalizowanego repozytorium - celowo unikamy tym razem klonowania). Na bazie tego prostego projektu strony internetowej, powtórzyć wszystkie wprowadzone w tym laboratorium komendy i operacje gitowe:
- zainicjalizować repozytorium, dodać i zacommitować pierowtny stan projektu
- wprowadzić dowolne zmiany w treści strony, np. zmienić treść tytułu lub przycisku, następnie zacommitować na głównym branchu
- za pośrednictwem nowego brancha dodać np. nowy przycisk na stronie lub zmienić jego działanie, a następnie zmerge'ować nowy branch do `main`
- zasymulować scenariusz konfliktowy analogicznie do wcześniej omawianego, np. zmieniając równolegle na dwóch osobnych branchach styl (wygląd) któregoś z elementów w pliku `style.css` i rozwiązując konflikt.
#### Na koniec zapisać logi gita do pliku tekstowego nazwisko_imie_lab1.txt i przesłać na adres katarzyna.marczak@uken.krakow.pl, mozna uzyć formatki maila:
tytuł: Technologie Devops Lab 1
Szanowna Pani,
przesyłam rozwiązanie z laboratoriów.
Z powazaniem,
<podpis>  
2. Przejść przez pierwsze 4 zadania z https://learngitbranching.js.org/ 
