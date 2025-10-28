### Praca ze zdalnym repozytorium
Do wykonania dzisiejszych ćwiczeń konieczne jest załozenie konta na platformie GitHub. Proszę w miarę mozliwości o wybranie loginu wskazującego na tozsamość właściciela lub dodanie takiej informacji w opisie profilu, jeśli pracujemy na załozonym wcześniej koncie. Po załozeniu konta, proszę o przesłanie pustego maila na adres katarzyna.marczak@uken.krakow.pl z tytułem: `<login> <nazwisko> <imię> <grupa>`

### Lokalna kofiguracja gita
Na początek dzisiejszych laboratoriów proszę wykonać następujące komendy kofigurujące git w konsoli:
```bash
git config --global init.defaultBranch main
git config --global user.email "you@example.com"
git config --global user.name "username"
```
Najlepiej na koniec ćwiczeń usunąć swój email i username tak (ponownie wykonać `config` usuwając email i name), aby osoba pracująca na tym samym komputerze w następnej grupie nie wykonywała commitów podpisując się jako inny użytkownik.

### Klonowanie istniejącego repozytorium
1. Pobrać zawartość repozytorium https://github.com/kmarczak-uni/TDO-lab1-webpage za pomocą komendy `git clone`. Rozpakować folder, przejść do niego i wywołać komendę `git status`, `git log --oneline` oraz `git remote -v` i przyjrzeć się wynikowi ich działania. Sprawdzić, na czym polega róznica względem ściągnięcia kodu za pomocą opcji `Download .ZIP`. 
2. Stworzyć na GitHubie na swoim profilu nowe, puste repozytorium `tdo-lab-1` (nie korzystać z opcji dodania README, .gitignore, licencji itd.)  
Ściągnąć pliki z repozytorium https://github.com/kmarczak-uni/TDO-lab1-webpage za pomocą opcji `Download .ZIP`, rozpakować, zainicjalizować lokalnie. Następnie ustawić swoje przed chwilą utworzone na GitHubie repozytorium jako zdalne do tego lokalnie zainicjalizowanego komendą: `git remote add origin https://github.com/ <uzytkownik> /tdo-lab-1.git`, sprawdzić `git remote -v`.
3. Wykonać dowolny commit na głównym branchu i wypchnąć zmiany komendą `git push -u origin main`. Odświezyć stronę repo w przeglądarce i sprawdzić, czy najnowszy commit jest widoczny online.
```
Jeśli pojawi się błąd Authentication failed, należy zalogować się na GitHubie i wygenerować Personal Access Token (PAT):
[Settings → Developer Settings → Personal access tokens → Tokens (classic)]
Uprawnienia: repo, workflow, read:user
Tokenu używamy zamiast hasła przy push/pull.
```
4. **Symulujemy** pracę zdalną dwóch programistów pracujących na osobnych komputerach w następujący sposób:
- stworzyć nowy folder na dysku i sklonować do niego swoje repozytorium `tdo-lab-1` przez `git clone`
- w tej nowej kopii repozytorium wykonać commit dodający nowy plik `testpull.txt` i go wypushować
- wrócić do poprzedniego folderu i zaktualizować lokalne repozytorium komendą `git pull`.
5. W analogiczny sposób, pracując w dwóch osobnych folderach zawierających repozytoria posiadające ten sam `remote`:
- w jednym folderze dokonać lokalnie zmiany w pliku `testpull.txt` i zacommitować bez pushowania
- w drugim folderze dokonać lokalnie zmiany w pliku `testpull.txt` (innej niz w poprzednim kroku, np. wpisać inną treść) i zacommitować bez pushowania
- po zacommitowaniu lokalnych zmian, spróbować najpierw wypushować zmiany z jednego, a potem z drugiego repozytorium (kolejność obojętna). Zaobserwować komunikat o błędzie i rozwiązać powstały konflikt wersji
- po zakończeniu zadania obydwa lokalne repozytoria oraz zdalne na GitHubie powinny mieć identyczny stan.
6. Praca z branchami na zdalnym repozytorium:
- utworzyć lokalnie w jednym z repozytoriów nowy branch np. o nazwie `remote-test` i zacommitować na tym branchu nowy plik lub zmianę w istniejących juz plikach
- wypushować nowy branch komendą `git push -u origin remote-test`
- sprawdzić, czy nowy branch jest widoczny na GitHubie
- dokonać przez Githuba ponownej zmiany w tym samym pliku co poprzednio na branchu, korzystając z edytora pliku w przeglądarce
- w jednym repozytorium ściągnąć zmiany wykonane online komendą `git pull`; w drugim repozytorium wykonać komendę `git fetch`.
Dodatkowo poszukać informacji i wyjaśnić czym się rózni pobieranie zmian przez `pull` i `fetch`.

### Praca w obrębie organizacji i forkowanie
Ze względów praktycznych będziemy czasem pracować *forkując* repozytoria - kazdy tworzy własne repozytorium uzywając opcji `Fork`, a następnie klonując na komputer to własne repozytorium z profilu.  
Przed rozpoczęciem pracy, kazda osoba musi zostać dodana ręcznie do organizacji https://github.com/kmarczak-teaching przez prowadzącą.  
Uwaga: pojęcia organizacji oraz forków dotyczą wyłącznie pracy z usługą GitHub (podobne serwisy, jak Gitlab i bitbucket, oferują analogiczne opcje) i nie są częścią systemu kontroli wersji `git`.  
1. Po dodaniu do organizacji, wykonać fork [repozytorium](https://github.com/kmarczak-teaching/fork-test). Sklonować **swojego forka (to znaczy repozytorium, które pojawiło się na profilu, a nie repozytorium "kmarczak-teaching/fork-test". W adresie URL klonowanego repozytorium powinien się znajdować własny login studenta)**.
2. Utworzyć na lokalnym branchu commit z nowym plikiem `<number_albumu>.txt` i wypushować do zdalnego repozytorium.
3. Wprowadzić propozycję wdrozenia zmian ze swojego forka do pierwotnego repozytorium, otwierając PR, czyli Pull request z poziomu przeglądarki na Githubie. Poczekać na akceptację PR-a przez prowadzącą.
