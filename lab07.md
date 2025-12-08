# Wdrazanie aplikacji (deployment)

## Wstęp

Deployment (czyli wdrazanie aplikacji na serwer lub platformę hostingową) to naturalny kolejny etap po CI. Gdy kod przejdzie testy i zostanie uznany za stabilny, chcemy go przenieść do środowiska produkcyjnego lub testowego.

## Sposoby wdrazania aplikacji

"Tradycyjną" metodą wdrazania aplikacji jest deployment bezpośrednio na gotowy serwer, na którym ręcznie instaluje się wszystkie potrzebne zalezności. Nowszą, Coraz częściej stosowaną i praktyczniejszą alternatywą jest budowanie aplikacji jako obrazu kontenera, który następnie mozna przechowywać w rejestrach (tzn. udostępniać je online) i uruchamiać w sposób powtarzalny na dowolnej maszynie. Oba podejścia prowadzą do tego samego celu - udostępnienia aplikacji uzytkownikom - lecz róznią się stopniem automatyzacji i przenośności. 

### Podejście 1 - wdrazanie aplikacji bezpośrednio na serwer

Tradycyjnie rozumiane wdrazanie aplikacji polega na umieszczeniu jej bezpośrednio na serwerze, który pełni rolę stałego środowiska uruchomieniowego. W takim podejściu administrator lub programista loguje się na serwer, kopiuje pliki aplikacji, instaluje wymagane narzędzia (np. interpreter, biblioteki, serwer WWW), konfiguruje usługi oraz dba o zgodność wersji i poprawność całego środowiska. Serwer staje się więc miejscem, w którym „na zywo” odtwarza się wszystkie warunki potrzebne do działania aplikacji. W efekcie deployment oznacza ręczne przygotowanie i utrzymanie systemu, na którym aplikacja ma działać, bez izolacji czy standaryzacji, jakie zapewniają kontenery.

## Podejście 2 - umieszczenie obrazu aplikacji w rejestrze kontenerów

Dotychczas korzystaliśmy w instrukcji `FROM` (w pliku Dockerfile) z gotowych obrazów, takich jak `python:3.11` czy `node:18`, dostarczanych przez oficjalny rejestr kontenerów (*container registry*). W ten sposób pobieraliśmy gotowey kontener. Jednak równie dobrze mozna stworzyć własny obraz - zawierający konkretną aplikację i jej konfigurację - i udostępnić go innym poprzez taki sam rejestr.
  
Rejestry kontenerów, takie jak Docker Hub czy GitHub Container Registry (GHCR), pełnią funkcję repozytoriów, w których przechowuje się obrazy. Dzięki temu: 
- mozna je pobierać i uruchamiać na dowolnych maszynach bez rekonfigurowania środowiska
- łatwo udostępniać je zespołowi, innym usługom lub systemom produkcyjnym
- umozliwiają łatwe i jednoznaczne wersjonowanie aplikacji

W tym sensie przesłanie obrazu kontenera do rejestru jest etapem deploymentu: to moment, w którym aplikacja jest gotowa do uruchomienia w innych środowiskach bez konieczności ręcznej instalacji zalezności czy powtarzania kroków konfiguracyjnych.

## Przykład

### GitHub Container Repository (GHCR)

Do utworzonego na poprzednich zajęciach repozytorium dodaj nowe workflow, np. o nazwie `cd.yml` i wklej do niego następujący kod: 

```yaml
name: CD
on:
  push:
    branches: [ main ]

jobs:
  docker-deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    - name: Login to GHCR
      run: echo "${{ github.token }}" | docker login ghcr.io -u ${{ github.actor }} --password-stdin
    - name: Build and push
      run: |
        docker build -t ghcr.io/${{ github.repository_owner }}/python-app:latest .
        docker push ghcr.io/${{ github.repository_owner }}/python-app:latest
```

Zanotuj samodzielne wyjaśnienie, co i jak wykonuje się w powyzszym workflow.  
Po jego skutecznym wykonaniu przejdź do platformy Play With Docker i spróbuj uruchomić aplikację poleceniem `docker run -d -p 8000:8000 ghcr.io/{nazwa_uzytkownika_github}/python-app:latest`.  

### Docker Hub

GHCR to wygodna opcja udostępniania obrazów Dockerowych w przypadku korzystania z GitHuba, ale najczęściej dla obrazów stosuje się Docker Hub - jest to "domyślne" miejsce udostępniania obrazów dla wielu programistów. Poniewaz jest to usługa zewnętrzna względem GitHuba, wymaga dodatkowej autentykacji, tj. podania w jakiś sposób uzytkownika oraz hasła utworzonego dla platformy Docker. Oczywiście nie chcemy wpisywać tych danych bezpośrednio do pliku workflow - chcemy, podobnie jak wyzej, aby były czytane ze zmiennych dostępnych tylko dla repozytorium. W tym celu mozna dla repozytorium utworzyć tzw. `*Github secrets*.  

#### Krok 1 - konto Docker i PAT (Personal Access Token)

Zaloguj się lub utwórz nowe konto na platformie [DockerHub](https://hub.docker.com/explore). Następnie w ustawieniach swojego profilu znajdź sekcję do generowania tokenów dostępu (Menu w prawym górnym rogu z inicjałem -> Account Settings -> Personal access tokens) i wygeneruj nowy token. Zwróć dokładną uwagę na instrukcję uzywania tokenu i skopiuj go.

#### Krok 2 - GitHub secrets
W tym samym repozytorium co poprzednio, przejdź do ustawień (zakładka *Settings*, ostatnia za *Actions*) i w menu po lewej przejdź `Security > Secrets and variables > Actions > New repository secret`. Stwórz zmienne `DOCKERHUB_USERNAME` oraz `DOCKERHUB_TOKEN` i nadaj im wartości utworzone w kroku 1.  
Następnie stwórz nowe workflow i umieść w nim następujący kod:

```yaml
name: CD-to-DockerHub
on:
  push:
    branches: [ main ]

jobs:
  docker-deploy:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v4

    - name: Login to Docker Hub
      run: |
        echo "${{ secrets.DOCKERHUB_TOKEN }}" | docker login -u "${{ secrets.DOCKERHUB_USERNAME }}" --password-stdin

    - name: Build and push image
      run: |
        docker build -t ${{ secrets.DOCKERHUB_USERNAME }}/python-app:latest .
        docker push ${{ secrets.DOCKERHUB_USERNAME }}/python-app:latest
```

Jeśli zmienne zostały ustawione poprawnie, a workflow zostało zacommitowane do głównego brancha, to uruchomi się ono automatycznie i umieści obraz na DockerHub (domyślnie jako publiczny). Zweryfikuj dostępność obrazu pod adresem `https://hub.docker.com/repository/docker/{nazwa_uzytkownika_dockerhub}`.  
Przetestuj ponownie uruchamianie aplikacji na Play With Docker, tym razem pobierając obraz z rejestru DockerHub - zamiast pełnego adresu URL, wystarczy podać swój `{username}/{image_name}`.

## Wersjonowanie i tagi

W dotychczasowych przykładach pojawiał się standardowy tag `:latest`. Jest to domyślne oznaczenie obrazu i chociaz wygodne w uzyciu, nie wystarcza w realistycznych projektach programistycznych. W prawdziwej pracy konieczne jest świadome numerowanie kolejnych wersji aplikacji, aby zachować kontrolę nad procesem rozwoju i wdrazania projektu.

Wersjonowanie obrazów ma wiele zalet. Umozliwia szybkie cofnięcie się do wersji, w której ostatnim razem wszystko działało. Ma to ogromne znaczenie wtedy, gdy okaze się, ze nowa aktualizacja zawiera błędy, a uzytkownicy muszą natychmiast otrzymać działający system. Dodatkowo  kolejne zrozumiale oznaczone obrazy stanowią lepszą dokumentację historii projektu, ułatwiając analizę zmian i diagnozowanie problemów. Dodatkowo spójny system tagów pozwala uporządkować środowiska (np. testowe i produkcyjne) i śledzić źródła zmian, np. commit w repozytorium.

Tag to po prostu oznaczenie dodawane do nazwy obrazu w formacie:
```yaml
{nazwa_obrazu}:{tag}
```
Inne sposoby oznacza wersji poza `:latest` to m.in. tzw wersjonowanie semantyczne (*semver* - np. 1.0.0), datę buildu (np. 2025-12-01), oznaczenia środowisk (`:test`, `:prod`) albo hash commitu z Git, który jednoznacznie wskazuje moment zmian.

W pracy zespołowej unikamy ręcznego nadawania tagów - wymagałoby to ciągłego edytowania plików workflow i łatwo prowadziłoby do błędów. Zamiast tego stosuje się automatyczne wersjonowanie.

#### Wersjonowanie wg commitu
W workflow w GitHub Actions wystarczy uzyć:
```bash
docker tag $IMAGE:latest $IMAGE:${{ github.sha }}
```
aby stworzyć unikalny tag powiązany z ID commitu. Jest to bezpieczne w zastosowaniu, gdyz ID commitów są unikalne, ale mało wygodne - to ID to długi ciąg trudnych do zapamiętania znaków.  

#### Wersjonowanie wg czasu

W niewielkich projektach mozna oznaczać wersje od daty ich powstania. W workflow dodajemy krok
```yaml
- name: Create timestamp
  run: echo "TS=$(date +%Y-%m-%d-%H-%M-%S)" >> $GITHUB_ENV
```
a następnie odwołujemy się do zapisanego czasu w tagu obrazu:
```yaml
docker tag $IMAGE:latest $IMAGE:${{ env.TS }}
```

#### Wersjonowanie wg tagów gita

W systemie gita istnieje mozliwość tworzenia tagów. W najbardziej podstawowym wydaniu, tag to oznaczenie konretnej wersji repozytorium, którą chcemy oznaczyć jako szczególnie istotną (podobnie jak w przypadku obrazu Dockerowego). W momencie, gdy nasza aplikacja jest np. gotowa do opublikowania i udostępnienia uzytkownikom po raz pierwszy, mozemy stworzyć `git tag v1.0`, uzywając tzw. `semantic versioning`. Domyślnie taki tag trzeba wypushować, aby był widoczny na repozytorium zdalnym: `git push origin v1.0`. Wówczas mozemy uzyć tego tagu do oznaczenia odpowiadającego mu obrazu Dockerowego w Github Action:  
- workflow wykrywające wypushowanie nowego tagu
```yaml
on:
  push:
    tags:
      - 'v*'
```
- oznaczenie obrazu z uzyciem `github.ref_name`
```yaml
        VERSION="${{ github.ref_name }}"
        docker build -t $IMAGE:$VERSION .
        docker push $IMAGE:$VERSION
```

Stworzenie nowego tagu jest mozliwe z poziomu przeglądarki w repozytorium. W tym celu nalezy stworzyć `Release` w zakładce `https://github.com/{uzytkownik}/{repozytorium}/releases` i skorzystać z opcji stworzenia nowego tagu.

#### Ćwiczenie

Przetestuj w swoim repozytorium co najmniej dwa sposoby wersjonowania z trzech wymienionych powyzej.
  
## Aplikacja projektowa

Zapoznaj się z [repozytorium](https://github.com/kmarczak-teaching/final-project) aplikacji Fastapi, która jest bazą do projektu zaliczeniowego. Uruchom ją na dwa sposoby: lokalnie w Pycharmie (lub własnym preferowanym środowisku Pythonowym) oraz na platformie Play With Docker po dopisaniu odpowiedniego Dockerfile.
