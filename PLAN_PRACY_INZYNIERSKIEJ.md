# PLAN PRACY INŻYNIERSKIEJ

## Temat pracy
**System monitoringu i analizy pogody kosmicznej oparty na danych z satelitów NOAA**

---

## 1. WSTĘP TEORETYCZNY (15-20 stron)

### 1.1. Wprowadzenie
- Definicja pogody kosmicznej (space weather)
- Znaczenie monitoringu pogody kosmicznej
- Wpływ zjawisk słonecznych na technologię i infrastrukturę
- Aktualne wyzwania w monitoringu pogody kosmicznej

### 1.2. Zjawiska pogody kosmicznej
- **Rozbłyski słoneczne** (solar flares)
  - Klasyfikacja rozbłysków (A, B, C, M, X)
  - Promieniowanie rentgenowskie
  - Wpływ na systemy komunikacyjne i nawigacyjne
  
- **Koronalne wyrzuty masy** (Coronal Mass Ejections - CME)
  - Mechanizm powstawania
  - Interakcja z wiatrem słonecznym
  - Wpływ na magnetosferę Ziemi

- **Burze geomagnetyczne**
  - Indeks Kp - planetarny indeks geomagnetyczny
  - Lokalny indeks K (Boulder)
  - Skutki dla systemów energetycznych i nawigacji

- **Protony słoneczne i cząstki energetyczne**
  - Strumienie protonowe (differential vs integral)
  - Zagrożenia dla astronautów i satelitów
  - Pasy radiacyjne Van Allena

- **Pole magnetyczne międzyplanetarne**
  - Układ współrzędnych GSM (Geocentric Solar Magnetospheric)
  - Składowe Bx, By, Bz
  - Znaczenie składowej Bz dla procesów magnetosferycznych

- **Aktywne regiony słoneczne**
  - Klasy magnetyczne regionów (β, βγ, βγδ)
  - Związek z rozbłyskami słonecznymi
  - Cykl słoneczny i aktywność regionów

### 1.3. Satelity i systemy monitorowania
- **GOES (Geostationary Operational Environmental Satellites)**
  - GOES-13 do GOES-19 - historia i funkcjonalność
  - Instrumenty pomiarowe (EXIS, SEM, SEISS, SUVI)
  - Architektura systemu monitorowania

- **DSCOVR (Deep Space Climate Observatory)**
  - Pozycja w punkcie Lagrange'a L1
  - Magnetometr i pomiar pola magnetycznego wiatru słonecznego
  - Znaczenie dla wczesnego ostrzegania

- **NOAA Space Weather Prediction Center (SWPC)**
  - Architektura systemu
  - API i formaty danych
  - Częstotliwość aktualizacji danych

### 1.4. Metody przetwarzania i analizy danych
- Przetwarzanie danych szeregów czasowych
- Techniki wizualizacji danych naukowych
- Analiza korelacji między zjawiskami
- Detekcja anomalii i prognozowanie

---

## 2. ANALIZA WYMAGAŃ I ARCHITEKTURA SYSTEMU (10-15 stron)

### 2.1. Analiza wymagań funkcjonalnych
- **Wymagania związane z pozyskiwaniem danych:**
  - Asynchroniczne pobieranie danych z wielu źródeł
  - Obsługa błędów i retry mechanism
  - Walidacja i normalizacja danych różnorodnych formatów
  - Kompresja i archiwizacja danych

- **Wymagania związane z przechowywaniem danych:**
  - Struktura bazy danych PostgreSQL
  - Modele danych dla różnych typów pomiarów
  - Strategia indeksowania i optymalizacji zapytań
  - Backup i archiwizacja danych

- **Wymagania związane z prezentacją danych:**
  - Interaktywne wykresy czasowe
  - Wizualizacje statystyczne (histogramy, heatmapy)
  - Analiza korelacji między zjawiskami
  - Wykrywanie i zaznaczanie luk w danych

### 2.2. Analiza wymagań niefunkcjonalnych
- Wydajność (performance)
- Skalowalność systemu
- Niezawodność (reliability)
- Bezpieczeństwo danych
- User Experience (UX)

### 2.3. Architektura systemu
```
┌─────────────────┐
│  Data Sources    │  (NOAA SWPC APIs)
│  (21 endpoints) │
└────────┬─────────┘
         │
         ▼
┌─────────────────┐
│  Fetch Module    │  (Python - asyncio)
│  (fetch_data.py) │  • Async retrieval
│                  │  • Error handling
│                  │  • CSV export
└────────┬─────────┘
         │
         ▼
┌─────────────────┐
│  Dropbox Storage│  (Cloud backup)
│  (ZIP archives) │
└────────┬─────────┘
         │
         ▼
┌─────────────────┐
│  Processing     │  (Go application)
│  Module         │  • Download from Dropbox
│  (db/main.go)   │  • Extract & validate
│                  │  • Database import
└────────┬─────────┘
         │
         ▼
┌─────────────────┐
│  PostgreSQL DB  │  (Data persistence)
│  • Tables per   │
│    data type    │
└────────┬─────────┘
         │
         ▼
┌─────────────────┐
│  Dashboard      │  (Streamlit - Python)
│  (dashboard/)   │  • 5 visualization modules
│                  │  • Interactive plots
│                  │  • Real-time analysis
└─────────────────┘
```

### 2.4. Wybór technologii
- **Python** - zbieranie danych, dashboard
  - `aiohttp` - asynchroniczne HTTP requests
  - `pandas` - przetwarzanie danych
  - `streamlit` - interaktywny dashboard
  - `plotly` - zaawansowane wizualizacje
  - `sqlalchemy` - ORM dla PostgreSQL

- **Go** - przetwarzanie i import danych
  - Wysoka wydajność
  - Obsługa wielu formatów danych
  - Integracja z PostgreSQL
  - Obsługa Dropbox API

- **PostgreSQL** - baza danych
  - Zaawansowane typy danych (JSON, timestamps)
  - Wydajne zapytania
  - Skalowalność

- **Dropbox API** - archiwizacja danych
  - Integracja OAuth 2.0
  - Automatyczny backup

---

## 3. IMPLEMENTACJA SYSTEMU (25-30 stron)

### 3.1. Moduł pozyskiwania danych (fetch_data.py)

#### 3.1.1. Architektura modułu
- Asynchroniczne pobieranie danych z 21 endpointów NOAA
- Mechanizm retry z wykładniczym backoff
- Obsługa błędów HTTP (403, 500, 503)
- Flattening zagnieżdżonych struktur JSON

#### 3.1.2. Przetwarzanie danych
```python
# Pseudokod procesu
async def retrieve_data():
    - Pobierz dane z URL
    - Waliduj odpowiedź
    - Przetwórz struktury zagnieżdżone
    - Zapis do CSV z append mode
    - Obsługa headerów w plikach CSV
```

#### 3.1.3. Archiwizacja i backup
- Kompresja danych do formatu ZIP
- Wysyłka do Dropbox
- Organizacja plików według daty

**Rezultat:** Kompletny system zbierający dane z 21 źródeł NOAA.

### 3.2. Moduł przetwarzania danych (Go application)

#### 3.2.1. Struktura modułów Go
- `database/` - połączenie i operacje na bazie danych
- `dropbox/` - integracja z Dropbox API
- `extract/` - ekstrakcja plików ZIP i CSV
- `secrets/` - zarządzanie tokenami OAuth
- `utils/` - funkcje pomocnicze

#### 3.2.2. Model danych
- Tabele dla każdego typu danych:
  - `planetary_k_index_1m`
  - `boulder_k_index_1m`
  - `dscovr_mag_1s`
  - `primary_integral_protons_1_day`
  - `secondary_integral_protons_1_day`
  - `primary_xray_1_day`
  - `secondary_xray_1_day`
  - `solar_regions`
  - itd.

#### 3.2.3. Proces importu danych
```
1. Pobranie pliku ZIP z Dropbox (wsparcie dla konkretnej daty)
2. Ekstrakcja zawartości
3. Parsowanie plików CSV
4. Walidacja danych
5. Bulk insert do PostgreSQL
6. Cleanup plików tymczasowych
```

**Rezultat:** Zautomatyzowany pipeline przetwarzania danych.

### 3.3. Moduł wizualizacji (Dashboard Streamlit)

#### 3.3.1. Architektura dashboardu
- Modułowa struktura (5 niezależnych modułów)
- Cache'owanie zapytań do bazy danych
- Dynamiczne wykrywanie tabel w bazie
- Automatyczna detekcja kolumn czasowych

#### 3.3.2. Moduły wizualizacji

**A. Geomagnetyzm (geomag.py)**
- Wykres czasowy planetarnego indeksu Kp
- Heatmap Kp (dzień vs godzina)
- Wizualizacja burz geomagnetycznych (Kp ≥ 5)
- Wykres lokalnego indeksu K (Boulder)
- *Funkcje:* `_set_layout()`, `_detect_k_column()`, `add_gray_areas_empty()`

**B. Pole magnetyczne (magnetic_field.py)**
- Składniki pola magnetycznego DSCOVR (Bt, Bx, By, Bz)
- Rozkład statystyczny składowej Bz (histogram)
- Automatyczne wykrywanie kolumn magnetycznych
- *Funkcje:* `_label_for_col()`, detekcja luk w danych

**C. Protony (protons.py)**
- Strumienie protonowe primary/secondary
- Wizualizacja według energii (jeśli dostępne)
- Skala logarytmiczna
- *Funkcje:* `_parse_energy_val()`, obsługa różnorodnych formatów energii

**D. Promieniowanie X (xray.py)**
- Strumienie promieniowania X primary/secondary
- Klasyfikacja rozbłysków (A/B, C, M, X)
- Korelacja z aktywnością geomagnetyczną (Kp)
- Rozkład statystyczny strumieni
- *Funkcje:* `_classify_flux()`, integracja danych z różnych źródeł

**E. Regiony słoneczne (solar_regions.py)**
- Mapa aktywnych regionów (scatter plot)
- Ewolucja powierzchni regionów
- Statystyka liczby aktywnych regionów
- *Funkcje:* automatyczne wykrywanie kolumn dat i regionów

#### 3.3.3. Wspólne komponenty (plot_utils.py)
- `set_layout()` - ujednolicony layout wykresów
- `add_gray_areas_empty()` - zaznaczanie luk w danych
- Integracja z Plotly Express i Graph Objects

#### 3.3.4. Połączenie z bazą danych (db.py)
- Automatyczne wykrywanie tabel (`find_table_like()`)
- Cache'owanie wyników zapytań z TTL
- Inteligentne wykrywanie kolumn czasowych (`pick_time_column()`)
- Normalizacja nazw kolumn

**Rezultat:** Kompleksowy dashboard z 5 modułami analitycznymi.

---

## 4. TESTY I WALIDACJA (8-10 stron)

### 4.1. Testy modułu pozyskiwania danych
- Testy jednostkowe funkcji `retrieve_data()`
- Testy obsługi błędów (403, 500, 503)
- Testy retry mechanism
- Testy flattening zagnieżdżonych struktur
- Testy integracyjne z Dropbox API

### 4.2. Testy modułu przetwarzania danych (Go)
- Testy parsowania CSV
- Testy importu do bazy danych
- Testy ekstrakcji ZIP
- Testy walidacji danych
- Testy integracyjne z PostgreSQL

### 4.3. Testy dashboardu
- Testy renderowania wykresów
- Testy cache'owania danych
- Testy wykrywania tabel i kolumn
- Testy obsługi brakujących danych
- Testy wydajności zapytań

### 4.4. Testy end-to-end
- Pełny cykl: fetch → Dropbox → Extract → DB → Dashboard
- Testy na rzeczywistych danych
- Walidacja poprawności wizualizacji

### 4.5. Analiza wydajności
- Czas pobierania danych z 21 endpointów
- Czas przetwarzania i importu danych
- Czas renderowania dashboardu
- Wykorzystanie pamięci
- Optymalizacja zapytań SQL

---

## 5. WYNIKI I ANALIZA (15-20 stron)

### 5.1. Charakterystyka zaimplementowanego systemu
- Liczba obsługiwanych źródeł danych (21)
- Rodzaje przetwarzanych danych
- Funkcjonalności dashboardu

### 5.2. Przykłady analiz na rzeczywistych danych

#### 5.2.1. Analiza burzy geomagnetycznej
- Przebieg indeksu Kp podczas burzy
- Korelacja z aktywnością słoneczną
- Analiza składowej Bz podczas burzy
- Wizualizacja na wykresach dashboardu

#### 5.2.2. Analiza rozbłysku słonecznego klasy X
- Przebieg promieniowania rentgenowskiego
- Korelacja z aktywnymi regionami słonecznymi
- Wpływ na strumienie protonowe
- Związek z aktywnością geomagnetyczną

#### 5.2.3. Analiza cyklu słonecznego
- Ewolucja aktywnych regionów
- Zmiany w strumieniach protonowych
- Trendy w aktywności geomagnetycznej
- Porównanie z danymi historycznymi

### 5.3. Wykryte problemy i ograniczenia
- Luki w danych (gap detection)
- Niezgodności formatów danych
- Ograniczenia API NOAA
- Wydajność systemu przy dużych wolumenach

### 5.4. Porównanie z istniejącymi rozwiązaniami
- NOAA Space Weather Dashboard
- Inne systemy monitoringu pogody kosmicznej
- Zalety i wady zaimplementowanego rozwiązania

---

## 6. PODSUMOWANIE I WNIOSKI (5-7 stron)

### 6.1. Podsumowanie zrealizowanych celów
- Pozyskiwanie danych z 21 źródeł
- Automatyczne przetwarzanie i import
- Kompleksowy dashboard analityczny
- Archiwizacja i backup danych

### 6.2. Wkład naukowy/praktyczny
- Integracja heterogenicznych źródeł danych
- Zautomatyzowany pipeline przetwarzania danych
- Interaktywny system analityczny
- Potencjalne zastosowania w badaniach naukowych i operacyjnych

### 6.3. Kierunki dalszych prac
- Implementacja algorytmów predykcyjnych
- Rozszerzenie o dodatkowe źródła danych
- Ulepszenia wizualizacji (3D plots, animations)
- System alertów i powiadomień
- Machine learning dla klasyfikacji zjawisk
- Integracja z systemami operacyjnymi (np. systemy energetyczne)

### 6.4. Wnioski końcowe
- Osiągnięte cele
- Napotkane wyzwania
- Lekcje wyciągnięte z projektu

---

## 7. BIBLIOGRAFIA I ŹRÓDŁA

### 7.1. Literatura naukowa
- Publikacje dotyczące pogody kosmicznej
- Materiały dotyczące satelitów GOES i DSCOVR
- Dokumentacja NOAA SWPC
- Artykuły o analizie danych szeregów czasowych

### 7.2. Dokumentacja techniczna
- Dokumentacja API NOAA Space Weather
- Dokumentacja Streamlit, Plotly, Pandas
- Dokumentacja Go, PostgreSQL
- Dokumentacja Dropbox API

### 8. ZAŁĄCZNIKI

### 8.1. Instrukcja instalacji i uruchomienia
- Wymagania systemowe
- Instalacja zależności
- Konfiguracja zmiennych środowiskowych
- Uruchomienie poszczególnych modułów

### 8.2. Przykładowe dane
- Przykładowe pliki CSV
- Przykładowe zapytania SQL
- Screenshoty dashboardu

### 8.3. Kod źródłowy
- Struktura projektu
- Najważniejsze fragmenty kodu
- Komentarze i dokumentacja

---

## SZACUNKOWY OBJĘTOŚCIOWY PODZIAŁ STRON:

1. **Wstęp teoretyczny**: 15-20 stron
2. **Analiza wymagań i architektura**: 10-15 stron
3. **Implementacja systemu**: 25-30 stron
4. **Testy i walidacja**: 8-10 stron
5. **Wyniki i analiza**: 15-20 stron
6. **Podsumowanie i wnioski**: 5-7 stron
7. **Bibliografia**: 2-3 strony
8. **Załączniki**: 10-15 stron

**RAZEM: ~90-120 stron**

---

## KLUCZOWE ELEMENTY DO PODKREŚLENIA:

✅ **Aspekty techniczne:**
- Asynchroniczne programowanie (Python asyncio)
- Integracja wielu źródeł danych
- Optymalizacja zapytań do bazy danych
- Cache'owanie i wydajność

✅ **Aspekty naukowe:**
- Zrozumienie zjawisk pogody kosmicznej
- Analiza korelacji między zjawiskami
- Interpretacja danych satelitarnych
- Wizualizacja danych naukowych

✅ **Aspekty inżynierskie:**
- Architektura systemu rozproszonego
- Obsługa błędów i niezawodność
- Skalowalność rozwiązania
- User Experience

✅ **Aspekty praktyczne:**
- Zastosowanie w monitoringu operacyjnym
- Potencjał w badaniach naukowych
- Możliwość dalszego rozwoju
- Przykłady analiz na rzeczywistych danych

