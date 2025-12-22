# Rozdział 5. Podsumowanie i wnioski

## 5.1 Podsumowanie zrealizowanych celów

Celem pracy było zaprojektowanie i zaimplementowanie systemu umożliwiającego w pełni automatyczne pobieranie, przetwarzanie i wizualizowanie danych dotyczących zjawisk pogody kosmicznej. W ramach realizacji celów pracy osiągnięto następujące rezultaty:

- Stworzono modularny system składający się z trzech bloków: bloku zbierania danych, bloku zapisu danych do bazy danych oraz bloku wizualizacji danych, składających się z sześciu osobnych modułów.
- Zaimplementowano w pełni automatyczne pobieranie danych pochodzących z interfejsu programistycznego SWPC oraz archiwizacje pobranych danych w postaci archiwów ZIP oraz w bez serwerowej bazie danych.
- Opracowano w pełni interaktywny moduł wizualizacji, umożliwiając analizę danych w czasie. Moduł umożliwia obserwację i wykrywanie anomalii w zjawiskach pogody kosmicznej.
- Wprowadzono system logowania i monitorowania przepływu danych, zwiększając niezawodność działania systemu i minimalizując ryzyko potencjalnej utraty danych.
- Przetwarzanie danych jest szybkie i wydajne, cały proces trwa do 4 minut nawet w przypadku powtarzania nieudanych operacji.
- System został zaprojektowany z uwzględnieniem wymagań funkcjonalnych i niefunkcjonalnych opisanych w rozdziale 2, w tym dotyczących wydajności, skalowalności, niezawodności, a także użyteczności warstwy wizualizacyjnej.

Dzięki spełnieniu wszystkich wymagań system jest gotowy do praktycznego zastosowania w analizach naukowych i w monitorowaniu bieżących zagrożeń związanych ze zjawiskami pogody kosmicznej.

## 5.2 Możliwe kierunki rozwoju projektu

Na podstawie porównania zaimplementowanego systemu z istniejącymi systemami zewnętrznymi w podrozdziale 4.4 oraz decyzji projektowych przedstawionych w podrozdziale 2.5, można wskazać obszary, w których system może być dalej rozwijany.

### 5.2.1 Rozszerzenie źródeł danych

Zastosowanie dodatkowych źródeł danych w projekcie pozwoliłoby na zwiększenie częstotliwości aktualizacji danych oraz na pobranie szerszego zakresu danych umożliwiając przeprowadzenie bardziej kompleksowych analiz.

### 5.2.2 Wprowadzenie funkcji predykcyjnych

Zastosowanie algorytmów uczenia maszynowego mogłoby umożliwić prognozowanie części zjawisk pogody kosmicznej zwiększając praktyczne zastosowanie systemu.

### 5.2.3 Zwiększenie częstotliwości aktualizacji danych

Aktualizacja danych w czasie rzeczywistym lub ze znacznie mniejszym opóźnieniem umożliwiłaby poprawę aktualności danych używanych w analizie i reagowanie na nagłe zjawiska.

## 5.3 Wnioski końcowe

W ramach pracy zaprojektowano i zaimplementowano system umożliwiający w pełni automatyczne pobieranie, przetwarzanie i wizualizowanie danych dotyczących pogody kosmicznej. System został opracowany w sposób modularny, co zapewnia jego elastyczność, łatwość utrzymania oraz możliwość dalszego rozwoju. Opracowane rozwiązanie umożliwia efektywną analizę danych, umożliwiając wykrywanie anomalii i potencjalnych zagrożeń, a zastosowane rozwiązania gwarantują niezawodność i wydajność działania. Testy i weryfikacja funkcjonalności wykazały, że system spełnia założone wymagania niefunkcjonalne i niefunkcjonalne. 

Praca wskazuje również dalsze perspektywy rozwoju, obejmujące zwiększenie częstotliwości aktualizacji danych, czy zaimplementowanie funkcjonalności predykcyjnych. Dzięki tym aspektom opracowany system może być wykorzystywany zarówno w badaniach naukowych, jak i w monitorowaniu bieżących niebezpieczeństw związanych ze zjawiskami pogody kosmicznej, potwierdzając jego znaczenie praktyczne.