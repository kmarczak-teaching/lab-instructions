# Wprowadzenie do GitHub Actions

## Podstawowe pojęcia

GitHub Actions to wbudowany w GitHub system automatyzacji, który pozwala wykonywać różne zadania bezpośrednio w repozytorium - od testowania kodu, przez budowanie aplikacji i Dockerów, aż po automatyczne wdrażanie na serwer. Dzięki temu można stworzyć pełny proces CI/CD bez konieczności korzystania z dodatkwch narzędzi.

Główną motywacją do używania GitHub Actions jest automatyzacja powtarzalnych czynności. Zamiast uruchamiać ręcznie testy, kompilacje, narzędzia lintujące lub deployment, możemy wszystko zapisać w zestawie insutrukcji w pliku `.yaml`, a GitHub wykona je za każdym razem, gdy coś zmieni się w repozytorium. To ułatwia pracę zespołową i pozwala szybciej wychwytywać błędy.

### Workflow
Workflow to kompletny proces automatyzacji. Jest zapisany w pliku `.github/workflows/*.yaml`. Można myśleć o nim jak o „scenariuszu”, który opisuje kiedy ma się uruchomić automatyzacja oraz co ma zostać wykonane.

Przykłady workflow:
- uruchamianie testów przy każdym pushu
- budowanie obrazu Dockera
- automatyczne wdrażanie aplikacji (deployment)

### Job
Job to pojedynczy etap pracy w ramach workflow. Workflow składa się z jednego lub wielu jobów. Każdy job działa w swoim własnym środowisku (osobnej maszynie wirtualnej lub kontenerze).

Przykłady jobów:
- „build” – zbuduj aplikację
- „test” – uruchom testy jednostkowe
- „deploy” – opublikuj aplikację na serwerze

Joby mogą działać równolegle lub zależeć od siebie (np. deploy wykonany tylko po pozytywnym przejściu testów).

### Step
Step (krok) to najmniejsza jednostka wykonywalna w jobie. Każdy step może być poleceniem w linii komend (np. pip install, npm test) lub wywołaniem gotowej akcji z marketplace (bazy gotowych rozwiązań).

Job składa się z sekwencji kroków wykonywanych po kolei od góry do dołu.

### Action
Action (akcja) to moduł, który wykonuje określone zadanie - coś jak gotowa funkcja. 

Przykłady często stosowanych akcji:
- checkout kodu: `actions/checkout`
- przygotowanie środowiska dla Pythona: `actions/setup-python`
- tworzenie artefaktów: `actions/upload-artifact` (więcej o artefaktach później)

Można korzystać z gotowych akcji, pisać własne lub łączyć oba podejścia.

### Runner

Runner to maszyna, na której wykonywany jest job. Może to być:
- runner hostowany przez GitHub (dostępne: Ubuntu, Windows, macOS)
- runner własny (self-hosted), np. serwer w firmie lub w chmurze

Każdy job jest przypisany do jakiegoś runnera.

### Trigger

Trigger (wyzwalacz) określa, kiedy workflow ma się uruchomić. Najczęściej używane triggery to:
- push - gdy ktoś wypycha zmiany do repozytorium
- pull_request - przy utworzeniu lub aktualizacji PR
- workflow_dispatch - ręczne uruchomienie przez przeglądarkę
- schedule - automatyczne uruchamianie co jakiś czas

## Ćwiczenia

### Ćwiczenie - czytanie gotowego workflow

Otwórz [repozytorium](https://github.com/3b1b/manim) i znajdź plik `docs.yaml` definiujący workflow. Zapisz własnymi słowami notatkę: co, kiedy i jak wykonuje ten workflow (z ilu i jakich jobów i stepów jest złozony, pod wpływem jakiego triggera i w jakim środowisku).

### Ćwiczenie - "hello world" workflow

Do dowolnego repozytorium dodaj nowe workflow, a następnie uruchom je. Podobnie jak w poprzednim ćwiczeniu, zanotuj własnymi słowami, co kiedy i jak wykonuje to workflow. Nastepnie dopisz drugi job (moze wyświetlać np. podobny komunikat), który wykona się dopiero po pierwszym - doczytaj w tym celu o elemencie `needs`.

```yaml
name: Hello
on: workflow_dispatch
jobs:
  say-hi:
    runs-on: ubuntu-latest
    steps:
      - run: echo "Hello, GitHub Actions!"
```

# Korzystanie z gotowych akcji

## Wstęp

### Wprowadzenie 

GitHub Actions są wygodne w uzyciu, ponieważ większość zadań nie wymaga pisania własnych skryptów od zera. Zamiast tego mozna korzystać z gotowych akcji - to moduły przygotowane przez GitHuba lub innych programistów, które wykonują konkretne zadania, np.:
- pobieranie kodu z repozytorium
- instalacja środowiska
- logowanie się do usług

### Przykłady
- `actions/checkout@v4`

To jedna z najczęściej używanych akcji - pobiera kod z repozytorium do środowiska workflow.
Bez tego job nie ma dostępu do plików źródłowych projektu.
```yaml
- name: checkout
  uses: actions/checkout@v4
```
- `actions/setup-*`

Konfiguruje środowisko, np. Pythona wewnątrz runnera.
```yaml
- name: python setup
  uses: actions/setup-python@v5
  with:
    python-version: "3.12"
```

### Składnia akcji
Każda akcja ma format `uses: NAMESPACE/NAZWA_AKCJI@WERSJA`.
- NAMESPACE  
Najczęściej `actions` (oficjalne akcje GitHuba), ale mogą być też inne repozytoria, np. `docker`, `aws-actions` lub dowolny użytkownik GitHuba, np. `myusername/my-action`  
- NAZWA_AKCJI  
Konkretna akcja, np. `checkout`, `setup-node`, `upload-artifact`  
- @WERSJA  
Najlepiej podawać konkretną wersję, np. `@v4`.
Dzięki temu workflow nie zepsuje się po aktualizacji akcji.

### Akcje z parametrami

Jeśli akcja przyjmuje parametry, przekazuje się je przez sekcję `with`:
```yaml
- name: login to Docker Hub
  uses: docker/login-action@v3
  with:
    username: ${{ secrets.DOCKERHUB_USERNAME }}
    password: ${{ secrets.DOCKERHUB_PASSWORD }}
```

### Akcje vs kroki

Akcja jest jednym krokiem w jobie, ale mozna ją mieszać ze zwykłymi poleceniami, np.:
```yaml
steps:
  - uses: actions/checkout@v4
  - uses: actions/setup-python@v5
    with:
      python-version: '3.11'
  - name: install dependencies
    run: pip install -r requirements.txt
  - name: run tests
    run: pytest
```

## Ćwiczenie - skrypt Pythonowy

Do gotowego workflow podanego ponizej dopisz dowolny, prosty skrypt Pythonowy, który będzie przez niego uruchamiany. Po zweryfikowaniu, ze workflow działa, rozbuduj skrypt oraz workflow tak, aby uzywał zmiennej środowiskowej (doczytaj o uzyciu `env`).

```yaml
name: Just run
on: workflow_dispatch
jobs:
  run-it:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    - name: Run script
        run: python3 script.py
```


# Typowy workflow dla aplikacji webowej

## Wstep

W projektach typu aplikacja webowa proces CI (Continuous Integration) zwykle składa się z kilku standardowych kroków, które powtarzają się niemal w każdym projekcie. Workflow CI ma zwykle za zadanie automatycznie sprawdzać jakość i poprawność kodu, aby błędy były wykrywane jak najwcześniej. Poniżej omawiane są najczęściej spotykane etapy w pipeline CI.

### Pobranie kodu z repozytorium

Pierwszym krokiem jest pobranie zawartości repozytorium do środowiska runnera. Najczęściej odbywa się to za pomocą akcji:
```yaml
- uses: actions/checkout@v4
```

### Przygotowanie środowiska i instalacja zależności

W zależności od technologii może to oznaczać np. instalację Pythona lub Node.js, pobranie bibliotek z requirements.txt lub package.json, konfigurację narzędzi koniecznych do budowania projektu.

Przykład dla Pythona:
```yaml
- uses: actions/setup-python@v5
  with:
    python-version: "3.12"

- name: install dependencies
  run: pip install -r requirements.txt
```
Ten etap zapewnia, że aplikacja uruchomi się w powtarzalnym, świeżym środowisku.

### Linting i analiza jakości kodu

W wielu projektach kolejnym krokiem jest sprawdzenie stylu i statyczna analiza kodu, np.: flake8, black --check, mypy.

Przykład:
```yaml
- name: style check
  run: flake8 .
```

To szybki sposób na złapanie podstawowych błędów jeszcze przed kompilacją lub uruchomieniem testów.

### Uruchomienie testów automatycznych

Najważniejszy krok CI to zwykle testy jednostkowe, integracyjne lub komponentowe:
```yaml
- name: testing
  run: pytest
```
Jeśli testy zakończą się błędem, workflow zostaje przerwany a kod nie powinien trafić do produkcji ani nawet zostać zmerge'owany.

### Budowanie aplikacji

W przypadku projektów webowych może to oznaczać:
- budowanie aplikacji backendowej
- kompilację frontendu (np. `npm run build`)
- tworzenie obrazu Dockerowego

Przykład:
```yaml
- name: Build Docker image
  run: docker build -t myapp:latest .
```

### Inne, opcjonalne: 
- upload artefaktów (paczki instalacyjne, raporty z testów, zbudowane pliki frontendu, gotowe obrazy itp.)
```yaml
- uses: actions/upload-artifact@v4
  with:
    name: test report
    path: reports/
```
- weryfikacja bezpieczeństwa, np. skanowanie zależności (`pip-audit`, `npm audit`), skanowanie obrazu Dockera i inne.

## Ćwiczenie - analiza przykładu aplikacji Node.js

Wykonaj fork [tego repozytorium](https://github.com/kmarczak-teaching/lab6-nodejs), a następnie stwórz dla niego CI workflow:

```yaml
name: CI + Docker

on: [push, pull_request, workflow_dispatch]

jobs:
  build_and_test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
      - run: npm install
      - run: npm test

  docker_build:
    runs-on: ubuntu-latest
    needs: build_and_test
    permissions:
      contents: read
      packages: write
    steps:
      - uses: actions/checkout@v4

      - name: Build image
        run: docker build -t sample-app:latest .
```

Przeanalizuj co się w nim znajduje i zaobserwuj wynik uruchomienia. Spróbuj naprawić błąd samodzielnie tak, aby kolejna próba wykonania zakończyła się sukcesem.

## Ćwiczenie - workflow dla aplikacji Pythonowej (FastAPI)

Napisz od początku workflow dla [tego repozytorium](https://github.com/kmarczak-teaching/lab6-fastapi), które ma uruchomić testy komendą `pytest` zlokalizowane w folderze `test`.
