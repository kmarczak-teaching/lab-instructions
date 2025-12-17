# Monitoring - Prometheus i Grafana

## Monitoring aplikacji - idea

Monitorowanie aplikacji to proces ciągłego zbierania, analizowania i reagowania na dane o jej działaniu w środowisku produkcyjnym. Dzięki monitorowaniu możemy obserwować rózne miary wydajności (np. liczba zapytańń na sekundę, czas odpowiedzi, zużycie CPU/RAM), które pomagają prześledzć, jak aplikacja jest używana przez użytkowników lub co jest dokładnym źródłem błędów. Bez systematycznego monitoringu błędy, awarie lub próby włamania do aplikacji są wykrywane dopiero przez użytkowników, co wpływa negatywnie na ich wrażenia i dostępność samej aplikacji. Monitoring pozwala nie tylko na szybką diagnostykę i rozwiązywanie problemów, ale także na analizę trendów i planowanie rozwoju infrastruktury, zanim problemy staną się krytyczne.

## Wprowadzenie do Prometheusa

Prometheus to otwarte oprogramowanie do monitorowania. Umożliwia instrumentowanie aplikacji, zbieranie metryk w postaci szeregów czasowych, a następnie ich przechowywanie, zapytania i analizę przy użyciu specjalnego języka zapytań PromQL. Prometheus działa okresowo pobierając dane metryczne z wyznaczonych celów (*targets*) i zapisując je do bazy danych. Na podstawie zebranych metryk można także definiować reguły *alertów*, które informują o nieprawidłowościach w aplikacji lub infrastrukturze w czasie rzeczywistym.

## Ćwiczenie

W trakcie laboratoriów będziemy korzystać wyłącznie z wersji Dockerowej - Prometheusa uruchomionego jako kontener. Jest to najwygodniejszy sposób jego uruchomienia, sugerowany równiez w [dokumentacji](https://prometheus.io/docs/prometheus/latest/installation/).  
Z racji formuły zdalnej, jest mozliwość wykonania ponizszych ćwiczeń na platformie Play With Docker lub lokalnie na swoim komputerze, jeśli poprawnie zainstalowaliśmy Dockera.

1. Utwórz plik `docker-compose.yaml` z zawartością podaną ponizej i drugi, na razie pusty `prometheus.yaml`. Uruchom za pomocą odpowiedniej komendy i otwórz UI Prometheusa w przeglądarce.  
```yaml
services:
  prometheus:
    image: prom/prometheus:v3.5.0
    volumes:
      - prometheus_data:/prometheus
      - ./prometheus.yaml:/etc/prometheus/prometheus.yml
    ports:
      - 9090:9090
    restart: unless-stopped

volumes:
  prometheus_data:
```
2. Dodaj pierwsze źródło danych: tzw. `node_exporter`, czyli specjalny program, który potrafi zbierać dane o zuzyciu zasobów sprzętowych i upubliczniać je tak, aby były widoczne dla Prometheusa. W tym celu zmodyfikuj najpierw `docker-compose.yml` dodając nowy serwis:
```yaml
  node-exporter:
    container_name: node-exporter
    image: prom/node-exporter:v1.9.0
    command:
      - "--path.rootfs=/host"
    volumes:
      - "/:/host:ro"
    pid: host
    restart: unless-stopped
```
a następnie uzupełniając wcześniej pusty plik konfiguracyjny Prometheusa o nastepującą treść:
```yaml
global:
  scrape_interval: 5s

scrape_configs:
  - job_name: "node-exporter"
    static_configs:
      - targets: ["node-exporter:9100"]
```
Usunąć poprzednio uruchomione kontenery (`compose down`) a następnie uruchom ponownie. Przejdź do UI Prometheusa i w zakładce `Status > Target Health` upewnij się, ze `Node-exporter` jest wdoczny i ma status `UP`.

3. Poprawnie skonfigurowany i uruchomiony Prometheus oraz `Node-exporter` pozwalają na wysłanie pierwszych zapytań, pisanych w specjalnym języku PromQL - podobnie jak SQL, słuzy on do odczytywania, agregacji i transformacji danych z bazy.  
Najwazniejsze pojęcia w języku PromQL:
- metryki (*metrics*) - monitorowana wartość, np. `node_cpu_seconds_total`, `http_requests_total`
- etykiety (*labels*) - dodatkowe parametry określające monitorowaną wartość: `node_cpu_seconds_total{cpu="0", mode="idle"}`, `http_requests_total{job="prometheus",group="canary"}`
- selektory (*selectors*) - filtry nakładane w zapytaniu do bazy, np. `node_cpu_seconds_total{mode="idle"}` - składnia jest taka sama jak dla etykiet
- funkcje (*functions*) - operacje na danych, np. `rate(), sum(), avg(), max()`; szczególnie często stosowana jest `rate` wyrazająca tempo zmian na sekundę
- zakresy (*range vectors*) - określające przedział czasu, np. `rate(node_cpu_seconds_total[5m])`
- agregacja - grupowanie wg parametru, np. `sum(rate(node_cpu_seconds_total[5m])) by (mode)`

Najwazniejsze typy metryk to:
- liczniki (*counters*) - mogą tylko rosnąć, podają całkowitą liczbę z czasem (np. `http_requests_total`)
- wskaźniki (*gauge*) - mogą rosnąć i maleć z czasem, np. `node_memory_MemAvailable_bytes`

Przetestuj następujące zapytania w Prometheusie
- `node_memory_MemAvailable_bytes` + zakładka Graph
- `node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes`
- `100 * (1 - node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)`
- `sum by (mode) (rate(node_cpu_seconds_total[5m]))`
- `rate(node_network_receive_bytes_total[10m])`

Spróbuj zapisać zapytania, które zwrócą inofmrację o:
- średnim zuzyciu CPU w sekundach w ciągu ostatnich 20 minut zagregowane po trybie (mode)
- tempo przyrostu wysyłanych pakietów przez interfejs sieciowy eth0 w ciągu ostatnich 15 minut
- średnim przepływie danych w sieci (zarówno wysłanych jak i odebranych) pogrupowanych wg interfejsu (etykieta *device*)

## Monitoring aplikacji webowej

Gdy chcemy monitorować aplikację webową, a nie jedynie jej otoczenie (np. zasoby systemowe serwera), mozna to zrobić na dwa sposoby:  
1. Korzystać z bibliotek integrujących aplikację z Prometheusem. Dotyczy to w szczególności metryk, których nie da się wywnioskować z poziomu systemu operacyjnego lub kontenera, takich jak czas odpowiedzi poszczególnych endpointów czy liczba błędów szczególnych funkcjonalności, np. przy dodawaniu przedmiotu do koszyka. W takich przypadkach konieczne jest umieszczenie kodu monitorującego bezpośrednio w kodzie źródłowym aplikacji (np. w aplikacji webowej FastAPI) i użycie biblioteki klienckiej Prometheusa, która udostępnia metryki w standardowym formacie.  
2. Stworzyć tzw. *reverse proxy* - specjalny serwer, który pośredniczy w przekazywaniu żądań od klientów do samej aplikacji. Przykładem takiego serwera jest np. Nginx. Wówczas Prometheus może monitorować nie samą aplikację webową, ale ruch, który przechodzi przez serwer proxy i w ten sposób pozwolić na monitorowanie dostępności oraz ruchu od i do aplikacji. Ten sposób nie umożliwia tak szczegółowego monitorowania jak w przypadku pierwszym, ale jest znacznie prostszy i wystarczający w większości sytuacji.    
Na dzisiejszych zajęciach skorzystamy z podejścia drugiego.

## Ćwiczenia 
  
1. Stwórz plik `docker-compose.yaml`, który uruchomi aplikację Fastapi używając obrazu pobranego z rejestru obrazów Dockerowych, np. GHCR, który "deployowaliśmy" na ostatnich zajęciach: 

```yaml
services:
  app:
    image: <adres obrazu z rejestru>
    expose:
      - "80"

  nginx:
    image: nginx:stable
    ports:
      - "8000:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - app

  nginx-exporter:
    image: nginx/nginx-prometheus-exporter:latest
    command:
      - -nginx.scrape-uri=http://nginx:8080/stub_status
    ports:
      - "9113:9113"
    depends_on:
      - nginx

  prometheus:
    image: prom/prometheus
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml:ro
    ports:
      - "9090:9090"
```

Jak widać, powyzszy plik uruchamia cztery kontenery. Wyjaśnij rolę kazdego z nich.

Uruchom odpowiednią komendą a następnie otwórz w przeglądarce UI Prometheusa i sprawdź, czy zakładka Targets wskazuje, ze monitorowana usługa jest widoczna i dostępna.

2. W polu `Query` wpisz `n` i sprawdź, jakie metryki i jakiego typu są dostępne na liście podpowiedzi. Zapisz, jakimi zapytaniami i z uzyciem których metryk sprawdzisz:
- czy aplikacja webowa w ogóle działa i jest dostępna
- czy serwer proxy obsługiwał jakieś zapytania http w ciągu ostatnich 10 minut
- ilość obsłuzonych połączeń z klientami oraz średnia liczba tych połączeń w ciągu ostatnich 10 minut (mozna ją zwiększyć otwierając aplikację w innej przeglądarce lub wysyłając zapytanie w nowym oknie konsoli z uzyciem `curl`)
- liczba klientów oczekujących na odpowiedź (*idle clients*)

## Alerty

Mając skonfigurowanego Prometheusa do monitorowania aplikacji, mamy mozliwość wykrywania niepokojących sytuacji (aplikacja nie działa, ruch jest podejrzanie wysoki itp.) i wysyłania powiadomień do administratora. W ten sposób błędy i problemy są wykrywane szybko i skutecznie, nie czekając na zgłoszenia od uzytkowników.  
Kolejno:
- tworzymy nowy plik `alerts.yml` w tym samym folderze co `prometheus.yml`:
```yaml
groups:
  - name: nginx-alerts
    rules:
    - alert: WebAppDown
      expr: nginx_up == 0
      for: 30s
      labels:
        severity: critical
      annotations:
        summary: "Web application is unreachable"
        description: "NGINX exporter cannot scrape NGINX. The application is likely down or unreachable."

```
- do konfiguracji `prometheus.yml` dodajemy informację o źródle reguł alertów, czyli namiar na stworzony w poprzednim kroku plik:
```yaml
rule_files:
  - /etc/prometheus/alerts.yml
```
Proszę tez zadbać o skopiowanie tego pliku do kontenera Prometheusa analogicznie jak dzieje się to z plikiem `prometheus.yml`.  
W tym momencie mozna uruchomić wszystkie kontenery - jeśli wszystko zostało skonfigurowane poprawnie, w Prometheusie powinny być widoczne odpowiedni wpisy zarówno w sekcji `Rules health`, jak i `Rules`. Proszę spróbować uruchomić alert, tzn. sprawić, aby zakładka `Alerts` pokazała, ze aplikacja nie jest dostępna.  

### Zadanie domowe
Napisać dwa dodatkowe alerty, które będą wykrywać nietypowo wysoki lub nietypowo niski ruch http (mozna przyjąć wartości np. 0.1 dla nietypowo niskiego ruchu i 10 dla nietypowo wysokiego - tak, aby mozna je było ręcznie przetestować i zaobserwować uruchamianie się alertów). Stopień `severity` mozna ustawić w tym przypadku na `warning`.  

### Zadanie "ponadprogramowe" dla chętnych 
To zadanie mozna zrealizować juprzy projekcie końcowym/ Tworząc dodatkową usługę Alertmanagera mozna ustawić przesyłanie powiadomień na rózne usługi: Slack, Gmail itd.  

Do pliku `docker-compose.yml` dodajemy nowy komponent:
```yaml
services:
  alertmanager:
    image: prom/alertmanager
    ports:
      - "9093:9093"
    volumes:
      - ./alertmanager.yml:/etc/alertmanager/alertmanager.yml:ro
```
Do pliku konfiguracyjnego `prometheus.yml` dodajemy sekcję:
```yaml
alerting:
  alertmanagers:
    - static_configs:
        - targets:
            - alertmanager:9093
```
Aby powyzsze kontenery uruchomiły się prawidłowo, na początek wystarczy pusty plik konfiguracyjny dla Alertmanagera `alertmanager.yml`. Zadanie polega na skonfigurowaniu go tak, aby otrzymywać alert wybraną drogą (np. na maila) w przypadku uruchomienia się wybranych alertów.   
