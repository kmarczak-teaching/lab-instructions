# Opis projektu

Podstawowy wymóg do kazdej z ocen: umieć samodzielnie wyjaśnić, co robi dana linijka np. w workflow lub Dockerfile oraz umieć odpowiedzieć na pytania typu: gdzie i co zmienić aby np. dodać nowy endpoint w aplikacji, zmienić port na którym jest ona uruchamiana, dodać nowy krok w workflow itp.  
Na ocenę dobrą obowiązują wszystkie wymogi z oceny dostatecznej oraz dobrej. Na ocenę bardzo dobrą obowiązują wszystkie wymogi z ocen dst, db i bdb.

# Dostateczny
- [ ] aplikacja całkowicie skonteneryzowana, uruchamiana z pomocą `docker compose`
- [ ] rozwijana **systematycznie** z uzyciem narzędzi git, w tym branchy i pull requestów; wszystkie commit messages i nazwy branchy oraz komentarze dobrze oddają co wprowadzają do projektu (np. "fix bug in user registration form" zamiast "w koncu działa!!111")
- [ ] wyrównany podział pracy w zespole
- [ ] działające procesy CI oraz CD w GitHub Actions (co najmniej dwa workflow)
- [ ] podstawowy monitoring z Prometheusem i Grafaną: najprostsze logi typu liczba requestów http
- [ ] baza danych sqlite jest przechowywana z pomocą docker volumes

# Dobry
- [ ] kontenery zoptymalizowane pod kątem czasu wykonania (nalezy umieć wyjaśnić, jak zostały zoptymalizowane)
- [ ] wersjonowanie obrazów inne niz `:latest`
- [ ] proces CI rozbudowany o linting
- [ ] bardziej zaawansowany monitoring w Prometheusie, np. alerty przy zbyt duzej liczbie requestów
- [ ] mozliwosc edycji danych w aplikacji

# Bardzo dobry
- [ ] aplikacja działa z bazą danych Postgres
- [ ] mozliwosc edycji danych w aplikacji jest dostępna tylko dla zalogowanego uzytkownika
- [ ] dodatkowy CD z wersjonowaniem opartym na tagach gita
- [ ] dobre pokrycie testami aplikacji (kazda funkcjonalność posiada test)
- [ ] aplikacja jest stale wyhostowana i dostępna online
