# Wizualizacja z Grafaną

## Wstęp

Grafana jest narzędziem do wizualizacji i analizy danych pomiarowych (metrics), które bardzo często wykorzystywane jest razem z Prometheusem. Podczas gdy Prometheus odpowiada głównie za zbieranie i przechowywanie danych czasowych oraz ich zapytania (PromQL), Grafana koncentruje się na czytelnym przedstawianiu tych danych w postaci wykresów, tabel i paneli. W praktyce Grafana pełni rolę warstwy prezentacji i interakcji z danymi monitoringowymi.  
Prometheus oferuje prosty interfejs WWW, który umożliwia wykonywanie zapytań PromQL i podgląd wykresów, jednak jego możliwości wizualne są ograniczone. Grafana rozszerza ten ekosystem, wprowadzając:
-  zaawansowane i konfigurowalne wizualizacje danych
- możliwość łączenia danych z wielu różnych źródeł (nie tylko Prometheusa)
- współdzielone, zapisywalne dashboardy, które mogą być używane przez cały zespół  

Grafana jest narzędziem nastawionym na analizę, obserwowalność i skuteczną komunikację stanu systemu, a nie tylko na proste zapytania do bazy danych czasowych.  
[Przykładowe mozliwości wizualizacji Grafany są pokazane tutaj](https://grafana.com/grafana/dashboards/)

## Tutorial Grafany

Pierwszy praktyczny przykład Grafany uruchomimy na podstawie oficjalnej dokumentacji. W `Play With Docker` lub lokalnie namaszynie z Dockerem wykonaj następujące kroki:  
1. Skopiuj kod źródłowy przykładu z GitHuba
```bash
git clone https://github.com/grafana/tutorial-environment.git
```  
i uruchom przez `docker compose`. Zapoznaj się wstępnie z listą uruchomionych usług przez `docker-compose ps` oraz czytając zawartość pliku `docker-compose.yaml`.  
2. Otwórz odpowiedni port w `Play With Docker` lub otwórz w przeglądarce pod `localhost:port` aplikację webową z tego tutoriala. Przetestuj jej działanie - dodaj kilka rekordów, oddaj kilka głosów na utworzone linki, sprawdź wynik dodania pustego tytułu i/lub linku itp.  
3. Podobnie jak wyzej uruchom UI Grafany w przeglądarce. Uwaga: kofiguracja z tutoriala celowo nadaje dostęp do funkcji admina bez logowania - w produkcyjnych scenariuszach jest on ograniczony loginem i hasłem. Przejrzyj zawartość zakładki `Explore` w menu po lewej, `Drilldown > Metrics` oraz `Connections > Data sources`.  
4. W zakładce `Explore` mozemy wykonywać zapytania w `PromQL` tak jak robiliśmy to na ostatnich laboratoriach w UI Prometheusa. W menu dropdown powinien być domyślnie wybrany Prometheus jako źródło danych do zapytań. Zmień tryb pisania zapytania w menu po prawej, pod niebieskim przyciskiem `Run query` na [Code].    
Wykonaj kilka zapytań, wklejając ich treść i uruchamiając przez `Shift-Enter` lub przyciskiem `Run query`, który pozwala od razu na wybranie zakresu czasowego w dropdownie:  
- `tns_request_duration_seconds_count` - zwróc uwagę na etykiety wyniku i wyjaśnij, jakiego typu jest  to metryka oraz co monitoruje. Przejdź ponownie do aplikacji z linkami, wykonaj kilka akcji w niej tak, aby zaobserwować zmiany w wynikach zapytania.  
- dodaj kolejne zapytanie przyciskiem `+ Add query` i wprowadź do niego tę samą metrykę, ale objętą funkcją `rate()`. Jak rózni się przebieg wykresu z czasem i otrzymywane wartości w porównaniu do poprzedniego zapytania?  
- dodaj zapytanie `sum(rate(tns_request_duration_seconds_count[5m])) by(route)`. Przy kazdym nowym zapytaniu jest mała ikonka oka-jej kliknięcie pozwala na schowanie wyników danego zapytania z wykresu dla lepszej czytelności.  
- napisz zapytanie zwracające sumę czasu requestów (zapytań do aplikacji) pogrupowanych po statusie odpowiedzi http oraz drugie zapytanie pogrupowane po metodzie requestu.  

5. Analiza logów z Loki  
Grafana współpracuje z róznymi źródłami danych, a przykładowy projekt z tutoriala umozliwia integrację narzędzia Loki, słuzącego do przechowywania logów aplikacji. Uwaga: Generowanie logów przez samą aplikację, ich przechowywanie i analiza wychodzi nieco poza program tego przedmiotu - przetestujemy tutaj krótko taką mozliwość z racji ze jest juz ona zawarta w tym projekcie. Nie ma natomiast wymogu dodawania takiej funkcjonalności do projektu końcowego.  
- Na początek przechodzimy do `Connections > Data sources` i dodajemy nowe źródło danych. Jedyna potrzebna konfiguracja to wklejenie do pola URL wartości `http://loki:3100` i zapisanie na dole strony przez `Save & Test`.  
- Ponownie przechodzimy do zakładki `Explore`, zmieniamy źródło danych z Prometheusa na Loki i tryb pisania zapytania na [~~Builder~~|Code]. Wklejamy do zapytania: `{filename="/var/log/tns-app.log"}` i wykonujemy przez `Shift-Enter`. Pojawi się lista logów aplikacji wraz z wykresem słupkowym pokazującym liczbę logów w danym momencie czasowym. Wykonanie kilku akcji w aplikacji (dodanie nowego linku, oddanie głosu, próba wejścia na niepoprawny URL) wygeneruje kolejne logi. Akcje kończące się błędem mozna odfiltrować za pomocą zapytania `{filename="/var/log/tns-app.log"} |= "error"`.    


6. Budowanie pierwszego dashboardu  
Najwazniejszą częścią Grafany są dashboardy, które mozna samodzielnie budować z wielu paneli. Panel to jedno zapytanie (źródło danych) oraz powiązana z tym zapytaniem wizualizacja jego wyników.  
W sekcji `Dashboards` wchodzimy w tworzenie nowego dashboardu. Wybieramy `Add new visualisation` i klikamy na Prometheusa w oknie wyboru źródła danych. W polu zapytania wpisujemy `sum(rate(tns_request_duration_seconds_count[5m])) by(route)` i wykonujemy `Shift-Enter`. Nadajemy dowolny tytuł panelu w menu po prawej i wycofujemy się do widoku dashboardu.  
Nalezy samodzielnie dodać drugi panel z analogiczną metryką `tns_client_request_duration_seconds_count` i innym typem wizualizacji (np. wykresem kołowym - pie chart). Po dodaniu nowego panelu umieścić je obok siebie w jednym rzędzie, dodać element `Row` i nazwać rząd utworzonych paneli np. `Traffic`.  

## Konfiguracja Grafany dla własnej aplikacji

### Zadanie
Na podstawie przykładu z laboratorium 5: https://github.com/docker/awesome-compose/tree/master/prometheus-grafana oraz startowego repozytorium https://github.com/kmarczak-teaching/lab9-prom-grafana-starter   
dodaj do rozwiązania zadania z poprzednich ćwiczeń (aplikacja Pythonowa + Ngnx serwer + Prometheus) usługę Grafany. Po skutecznym uruchomieniu całego projektu z `docker compose` stwórz jeden dashboard w Grafanie, zawierający 2-3 panele z wizualizacjami zapytań napisanych w ramach tamtego zadania. **Wykorzystaj w dashboardzie róźne rodzaje wizualizacji, nie tylko *time series***, i nadawaj tytuły paneli, które będą wskazywać, co ilustruje dany panel.  
Następnie dodaj jeszcze do projektu Node exporter (dodatkowe źródło danych do Prometheusa) oraz stwórz w Grafanie drugi, osobny dashboard, który będzie poświęcony wizualizacji zuzycia zasobów systemowych (CPU, pamięć, dysk itd.). Podobnie jak w poprzednim ćwiczeniu, dodaj 2-3 panele wizualizujące zapytania, które pisaliśmy na tamtych ćwiczeniach.  
Po wykonaniu tych zadań nalezy wysłać na maila zrzut ekranu z tych dwóch dashboardów z tytułem `Devops lab9 rozwiązanie`.
