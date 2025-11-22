W tym rozdziale przedstawiono szczegółową analizę działania projektu, w tym omówienie  przykładowych wykresów zawierających rzeczywiste dane przetworzone przez system. W końcowej części rozdziału zaprezentowano również ograniczenia projektu oraz dokonano porównania z innymi istniejącymi systemami analizy pogody kosmicznej.

# 4. Analiza zaprojektowanego systemu

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

W wyniku optymalizacji procesów zastosowanych w potoku danych przetwarzanie danych trwa nie więcej niż 4 minuty nawet w przypadku ponawiania operacji w wyniku błędów. Zapisywane archiwa mają rozmiar około 500 KB dla każdego dziennego pomiaru, umożliwiając ich efektywne przechowywanie oraz szybki dostęp do danych historycznych.

Każdy etap przetwarzania jest wyposażony w mechanizmy logowania i monitorowania umożliwiając szybkie i sprawne wykrywanie i analizowanie błędów potencjalnie występujących w projekcie oraz umożliwia obserwowanie przepływu danych przez system.

Zastosowanie bez serwerowej bazy danych w systemie umożliwiło ciągły dostęp do zapisanych danych oraz wymusiło przechowywanie tabel wymaganych w dalszej analizie, bez nadmiarowych szczegółów.

Moduł wizualizacji umożliwia interaktywną analizę danych, w tym filtrowanie ze względu na analizowane zmienne, wybieranie określonych okien czasowych, a nawet zapisywanie wykresów do plików w formacie PNG.

Podsumowując, zaimplementowany system zapewnia niezawodny i szybki przepływ danych, umożliwia ich stały dostęp, monitorowanie procesów oraz interaktywną analizę. W wyniku zastosowania modularnej struktury system może być rozszerzany poprzez dodawanie nowych modułów, np. do potoku danych.

## 4.2 Przykłady analizy rzeczywistych danych



## 4.3 Ograniczenia projektu 

Zaprojektowany system posiada pewne ograniczenia wynikające zarówno z przyjętej architektury, jak i charakterystyki zastosowanych źródeł danych. Ograniczenia te wpływają na projekt w takich obszarach, jak dostępność danych, ilość przetworzonych danych, czy zakres przeprowadzonej analizy. Świadomość tych ograniczeń pozwala na poprawną interpretację wyników oraz wskazuje na potencjalne kierunki rozwoju. 

Poniżej omówiono główne ograniczenia systemu w kontekście danych, funkcjonalności oraz jego zastosowania.

### 4.3.1 Ograniczenia związane z danymi

Dane wykorzystywane przez system pochodzą z jednego źródła danych,  co naraża go na potencjalne braki danych spowodowane awarią interfejsu programistycznego SWPC. Wystąpienie problemów w module źródła danych może prowadzić do nieciągłości w danych, a w rezultacie do ograniczenia możliwości analitycznych systemu.

Dodatkowym celowym ograniczeniem jest pobieranie danych raz dziennie o tej samej porze. Rozwiązanie to zapewnia spójność danych i umożliwia przeprowadzanie porównywalnych analiz między poszczególnymi dniami. Jednocześnie prowadzi do zawężenia zakresu danych dostępnych dla systemu, potencjalnego powodując pomijanie istotnych dla danych zjawisk danych.

### 4.3.2 Ograniczenia techniczne

System posiada również ograniczenia techniczne, które wpływają na sposób jego działania oraz zakres dostępnych funkcjonalności. Ich źródłem są przede wszystkim zastosowane narzędzia oraz infrastruktura, w szczególności baza danych.

Najpoważniejszym ograniczeniem w tym obszarze jest limit przepływu danych narzucony przez dostawcę bazy danych, wynikający z użycia darmowego planu usługowego. Wymusiło to zastosowanie ograniczenie ilości wykorzystywanych tabel, w celu nie przekroczenia dozwolonego limitu. Pomimo mniejszego znaczenia usuniętych tabel dla analizy zjawisk pogody kosmicznej, wraz z ich utratą ograniczono  w pewnym stopniu analizę zjawisk o mniejszym priorytecie.

W rezultacie system działa poprawnie w ramach przyjętych założeń, jednak pełniejsza analiza byłaby możliwa po rozszerzeniu zasobów np. poprzez użycie płatnego planu usługowego.

### 4.3.3 Ograniczenia projektowe

Ograniczenia projektowe wynikają z podjętych na etapie planowania decyzji projektowych oraz sposobu ich realizacji. Ograniczenia te zostały świadomie przyjęte, aby zapewnić spójność architektury i implementacji projektu w ramach pracy inżynierskiej.

Pierwszym istotnym ograniczeniem projektowym było zawężenie funkcjonalności systemu do wybranych zjawisk pogody kosmicznej. Projekt nie obejmuje wszystkich dostępnych metryk i informacji, a jedynie te uznane za najbardziej istotnych dla przyjętych celów projektu oraz efektywnego przeprowadzanie analizy.

Kolejnym ograniczeniem jest rezygnacja z implementacji metod opartych na uczeniu maszynowym. Choć ogranicza to możliwości przeprowadzenie zaawansowanych analiz predykcyjnych, system nadal umożliwia rzetelną i efektywną analizę danych poprzez dostępne interaktywne metody wizualizacyjne.

W rezultacie system realizuje wszystkie przyjęte cele projektowe, jednocześnie wskazując potencjalne obszary rozwoju projektu o nowe funkcjonalności.

## 4.4 Porównanie z istniejącymi rozwiązaniami

https://www.swpc.noaa.gov/communities/space-weather-enthusiasts-dashboard

https://www.spaceweatherlive.com/