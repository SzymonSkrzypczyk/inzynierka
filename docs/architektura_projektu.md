W tym rozdziale opisane zostaną głównie wymagania odnośnie projektu, podjęte decyzje projektowe oraz właściwa architektura projektu, wraz z wybranymi technologiami umożliwiającymi implementacje opisywanego systemu.

## 2.1 Analiza wymagań funkcjonalnych

W niniejszym podrozdziale przedstawiono wymagania funkcjonalne realizowanego systemu, które określają, jakie warunki powinny zostać spełnione, aby zapewnić wysoką jakość, niezawodność i prawidłowe funkcjonowanie systemu. Analiza wymagań funkcjonalnych jest kluczowym etapem projektowania systemu pozwalającym na zidentyfikowanie głównych obszarów projektowanego systemu.

### 2.1a Wymagania związane z pozyskiwaniem danych

W projektowanym systemie jednym z kluczowych obszarów jest moduł pozyskiwania danych ze źródeł dostarczonych przez interfejsy programistyczne utrzymywanych przez NOAA Space Weather Prediction Center. Ze względu na charakterystykę zadania i danych wymagane jest uwzględnienie określonych wymagań w celu zwiększenia efektywności i niezawodności gromadzenia danych.

1. Asynchroniczne pobieranie danych ze źródeł

   W celu zapewnienia skalowalności i wydajności system powinien umożliwiać jednoczesne pobieranie danych z wielu źródeł bez blokowania głównego wątku programu. Asynchroniczne odwoływanie się do źródeł pozwala na przetwarzanie danych wysyłanych w różnych odstępach czasu oraz efektywne wykorzystanie zasobów systemu.

2. Obsługa błędów i system ponawiania prób

   Podczas komunikacji z zewnętrznymi źródłami może dojść do wielu rodzajów błędów np. braku odpowiedzi serwera, zbyt długiego czasu oczekiwania na odpowiedź, czy błędnego formatu odpowiedzi. W celu zapewnienia maksymalnej niezawodności system powinien być wyposażony w automatyczny mechanizm ponawiania poboru danych w przypadku wystąpienia braku danych, uwzględniający dozwoloną liczbę ponownych zapytań oraz określony odstęp pomiędzy poszczególnymi próbami. Dodatkowo w celu umożliwienia odtworzenia całego procesu wszystkie próby oraz błędy powinny być logowane w celu dalszej analizy problemów.

3. Walidacja i normalizacja danych do wspólnego formatu 

   Dane przychodzące są otrzymywane w formacie JSON oraz z różnorodną strukturą plików, w celu efektywnego przetwarzania danych na dalszych etapach działania systemu dane powinny zostać znormalizowane do wspólnego formatu, który umożliwi efektywną analizę i przetwarzanie. Dodatkowo wszystkie pola zagnieżdżone powinny zostać spłaszczone w celu zachowania informacji przez nie przenoszone.

4. Kompresja i archiwizacja danych

   W wyniku pobierania potencjalnych dużych ilości danych powinny być kompresowane i archiwizowane w celu ograniczenia zużycia przestrzeni dyskowej oraz umożliwienia przechowywania danych historycznych.

### 2.1b Wymagania związane z przechowywaniem danych

W opisywanym systemie kluczowym obszarem jest sposób trwałego przechowywania pozyskanych danych. Baza danych stanowi centralny punkt aplikacji oraz integracji otrzymanych informacji .

1. Struktura bazy danych PostgreSQL

   System powinien wykorzystywać relacyjną bazę danych PostgreSQL, ze względu na jej wysoką wydajność, powszechną adaptację oraz operowanie w modelu Opensource. Struktura bazy danych powinna zostać zaprojektowana w sposób umożliwiający przechowywanie danych pomiarowych oraz metadanych zawierających informacje odnośnie czasu pozyskania i statusu przetwarzania otrzymanych danych, w celu umożliwienia odtworzenia procesu zapisu i przechowywania danych.

2. Ujednolicenie modeli danych

   Ze względu na różnorodność danych każdy typ pomiaru musi posiadać wspólne pola w celu ujednolicenia danych na etapie ich wizualizacji oraz analizy. Takie podejście pozwala na zunifikowany proces pobierania zróżnicowanych danych z jednej bazy danych w celu ich dalszego przetworzenia.

3. Strategia indeksowania 

   W celu zoptymalizowania dużej ilości zapytań na dalszym etapie systemu zastosowanie odpowiedniej strategii indeksowania jest niezbędne. Indeksy powinny być tworzone w szczególności dla intensywnie wykorzystywanych pól, w szczególności znaczników czasu.

### 2.1c Wymagania związane z prezentacją danych

Prezentacja danych odgrywa kluczową rolę w umożliwieniu interpretacji i analizy danych pomiarowych. System powinien udostępniać różnorodne formy wizualizacji, które pozwalają na interaktywną analizę wyświetlanych wyników.

1. Interaktywne wykresy czasowe

   W celu umożliwienia efektywnej analizy wyświetlanych wyników wykresy powinny umożliwiać interakcję z danymi. Opisywana interakcja powinna umożliwiać na szczegółowe eksplorowanie danych oraz dostosowywanie widoku do aktualnych potrzeb przeprowadzanej analizy.

2. Wizualna analiza intensywności danych

   Aplikacja powinna umożliwiać tworzenie wizualizację wspierających analizę rozkładu i intensywności zjawisk, w celu umożliwienia identyfikacji wzorców i anomalii. Dane opisywane przy użyciu tych metod powinny być odpowiednio agregowane w celu efektywnej analizy dużych zbiorów danych.

3. Wykrywanie i zaznaczanie braków w danych

   W celu zapewnienia wysokiej jakości analizy oraz prawidłowej  interpretacji wyników, aplikacja powinna automatycznie wykrywać luki w danych  i zaznaczać je na generowanych wizualizacjach. Braki danych mogą wynikać z różnych przyczyn, takich jak np. awarie sensorów, przerwy w transmisji, czy niedostępność źródeł, które mogą dostarczać dodatkowych informacji i być wartościowe przy pełnej analizie otrzymanych wyników.

## 2.2 Analiza wymagań niefunkcjonalnych

W niniejszym podrozdziale opisano wymagania niefunkcjonalne systemu, które określają na zdefiniowanie elementów jakościowych, które powinny zostać spełnione przez system, w celu zapewnienia wydajności, niezawodności i komfortu użytkowania. Analiza wymagań niefunkcjonalnych jest kluczowym etapem umożliwiającym identyfikacje elementów na skalowalność, użyteczność i niezawodność projektu.

1. Wydajność

   System powinien gwarantować szybkie i efektywne działanie na wszystkich etapach, niezależnie od ilości danych do przetworzenia. Wysoka wydajność stanowi kluczowy czynnik umożliwiający płyną pracę aplikacji. Oczekiwana wydajność powinna zostać osiągnięta poprzez optymalizacje operacji na bazie danych, równoległe przetwarzanie danych oraz wykorzystywanie pamięci podręcznej.

2. Skalowalność

   System powinien gwarantować skalowalność, umożliwiającą obsługę rosnącej ilości danych bez znacznej utraty wydajności. Wysoka skalowalność pozwala na poszerzanie okna analizy przetwarzanych danych, co umożliwiające przeprowadzenie wnikliwej i szczegółowej analizy.

3. Niezawodność

   System powinien gwarantować wysoką niezawodność, zapewniając stabilne działanie na każdym etapie, skutecznie minimalizując ryzyko awarii. Wysoka niezawodność powinna zostać osiągnięta poprzez implementacje systemów wykrywania i logowania błędów oraz mechanizmy powtarzania nieudanych prób pozyskiwania danych. Takie rozwiązania pozwolą na utrzymanie ciągłości i integralności przetwarzanych informacji.

4. Użyteczność interfejsu użytkownika

   System powinien gwarantować wysoką użytecznością interfejsu użytkownika, zapewniając spójną, intuicyjną i przejrzystą obsługę aplikacji. Wysoka 	użyteczność ułatwia wykonywanie operacji, ogranicza ryzyko błędów i przyspiesza czas potrzebny na realizacje analiz.

## 2.3 Architektura systemu

Architektura projektu została zaprojektowana w sposób modułowy, odseparowując od siebie poszczególne części, umożliwiając skalowalność oraz łatwość rozbudowy poszczególnych komponentów. Na rysunku 2.3.1 przedstawiono ogólny schemat architektury systemu.

![flowchart](../sketches/flowchart.png)

System składa się z sześciu głównych modułów z funkcjonalnościami:

1) Źródło danych
2) Moduł odpowiedzialny za pobierania danych ze źródła
3) Moduł odpowiedzialny za archiwizację danych
4) Moduł odpowiedzialny za przetwarzanie danych
5) Moduł odpowiedzialny za dodawanie danych do bazy danych
6) Moduł odpowiedzialny za wizualizację wyników

W kolejnych podrozdziałach opisano szczegółowo budowę i sposób działania każdego z wymienionych komponentów.

### 2.3.1 Źródło danych

Podstawowym źródłem danych w projekcie jest interfejs programistyczny udostępniany przez NOAA Space Weather Center. Interfejs ten zapewnia dostęp do endpointów zawierających informacje dotyczące pogody kosmicznej, aktywności słońca oraz warunków geomagnetycznych Ziemi. Dane dostępne są w formacie JSON oraz są aktualizowane na bieżąco.

### 2.3.2 Moduł pozyskiwania danych

Moduł pobierania danych odpowiada za cykliczne pobieranea danych pochodzących z modułu źródła danych oraz za ich konwersje do formatu oczekiwanego przez dalsze etapach systemu. Moduł zapewnia jednolitość i spójność danych w całym przepływie danych przez system.

### 2.3.3 Moduł archiwizacji danych

Moduł archiwizacji danych odpowiada za przechowywanie przetworzonych danych, zapewniając ich dostępność w kolejnych etapach systemu. Dodatkowo moduł zapewnia funkcjonalność kopii zapasowej, zwiększając odporność na awarie i utratę danych.

### 2.3.4 Moduł przetwarzania danych

Moduł przetwarzania danych odpowiada za przygotowanie danych do zapisu w bazie danych oraz redukcje danych uznanych za zbędne w dalszej analizy. Moduł ten zapewnia, że dane w kolejnych etapach zawierają tylko potrzebne informacje w formacie gotowym do efektywnego wykorzystania.

### 2.3.5 Moduł dodawania danych do bazy danych

Moduł dodawania danych do bazy danych odpowiada za poprawny i niezawodny zapis danych do bazy danych do odpowiednich tabel wraz z zastosowaniem poprawnych typów danych. Zapewnia to niezawodne wyświetlanie danych wynikowych na etapie wizualizacji, dodatkowo moduł pełni rolę centralnego magazynu danych, które mogą być bezpośrednio wykorzystane do analizy i interpretacji.

### 2.3.6 Moduł wizualizacji danych

Moduł wizualizacji danych odpowiada za prezentację przetworzonych danych w formie umożliwiającej ich analizę i interpretację. Dane przedstawiane są przy pomocy różnorodnych metod wizualizacji, pozwalając na uchwycenie zależności oraz wykrywanie anomalii występujących w danych.

