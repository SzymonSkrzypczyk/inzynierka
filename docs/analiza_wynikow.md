W tym rozdziale przedstawiono szczegółową analizę działania projektu, w tym omówienie  przykładowych wykresów zawierających rzeczywiste dane przetworzone przez system. W końcowej części rozdziału zaprezentowano również ograniczenia projektu oraz dokonano porównania z innymi istniejącymi systemami analizy pogody kosmicznej.

# 4. Analiza wyników

## 4.1 Charakterystyka zaimplementowanego systemu

W tym podrozdziale omówione zostaną cechy systemu zaimplementowanego w trzecim rozdziale i według założeń z drugiego rozdziału. Szczególny nacisk położono na umożliwienie niezawodnego przepływu danych oraz ich natychmiastową dostępność w module wizualizacji.

Opisywany system powstał w wyniku integracji poszczególnych modułów w trzy bloki, które dodatkowo współpracują ze sobą umożliwia szybki, w pełni opisany i klarowny proces przepływ danych. Dane pochodzące z zewnętrznego interfejsu programistycznego są przetwarzane codziennie niemal bez problemów, co świadczy o niezawodności projektu. Zgrupowanie wszystkich modułów poza modułem wizualizacji w połączone ze sobą przez potok danych bloki umożliwiło usprawnienie przepływu danych.

![github action](../sketches/github_action.png)

> Rys 4.1.1 Potok danych zaimplementowany przy pomocy Github Actions

Dzięki podzieleniu przetwarzania na trzy bloki funkcjonalności i zakres poszczególnych bloków pozwolił na zamknięte przetwarzanie, które nie wpływa na procesy poza zakresem danego bloku. Role bloków rozkładają się w następujący sposób:

- blok zbierania danych - odpowiada za pobranie i archiwizację danych
- blok zapisu danych do bazy danych - odpowiada za przygotowanie danych oraz ich zapis w bazie danych
- blok wizualizacji danych - odpowiada za przygotowanie interaktywnych wykresów

Dane po każdym z opisanych bloków znajdują się w chmurze umożliwiając stały dostęp i ich przetwarzanie. Dodatkowo, zapobiega to sytuacji, w której jeden z etapów systemu próbuje uzyskać dane, które nie są aktualnie dostępne. Ponieważ każdy etap przetwarzania ma zaimplementowaną obsługę błędów potencjalne błędy nie powodują natychmiastowego zatrzymania całego systemu, a jedynie podjęcie ponownej próby przeprowadzenia danej operacji.

System jest w całości zautomatyzowany, dzięki użyciu technologii chmurowych. Ich wysoka dostępność i odseparowanie warstwy przetwarzania systemu od kodu, umożliwiają nieprzerwane przetwarzanie z ustaloną częstotliwością. Zastosowanie Github Actions jako głównego narzędzia do stworzenia potoku danych, umożliwiło odseparowanie odpowiedzialności za przepływ danych od użytkownika oraz umożliwiło codzienne przetwarzanie danych o tej samej porze wzmacniając jednolitość danych.

Zastosowanie bez serwerowej bazy danych w systemie umożliwiło ciągły dostęp do zapisanych danych oraz wymusiło przechowywanie tabel wymaganych w dalszej analizie, bez nadmiarowych szczegółów.

TBD



## 4.2 Przykłady analizy rzeczywistych danych

## 4.3 Ograniczenia projektu 

Zaprojektowany system posiada pewne ograniczenia wynikające zarówno z przyjętej architektury, jak i charakterystyki zastosowanych źródeł danych. Ograniczenia te wpływają na projekt w takich obszarach, jak dostępność danych, ilość przetworzonych danych, czy zakres przeprowadzonej analizy. Świadomość tych ograniczeń pozwala na poprawną interpretację wyników oraz wskazuje na potencjalne kierunki rozwoju. 

Poniżej omówiono główne ograniczenia systemu w kontekście danych, funkcjonalności oraz jego zastosowania.

Ograniczenia zwiazane z danymi



Ograniczenia funkcjonalne np. brak predykcji



Ograniczenia techniczne. np limit na bazie danych



Ograniczenia projektowe



## 4.4 Porównanie z istniejącymi rozwiązaniami

https://www.swpc.noaa.gov/communities/space-weather-enthusiasts-dashboard

