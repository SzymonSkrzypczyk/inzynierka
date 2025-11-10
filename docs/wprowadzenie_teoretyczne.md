W niniejszym rozdziale przedstawione zostaną podstawy teoretyczne dotyczące pogody kosmicznej, umożliwiające zrozumienie zagadnień i zjawisk omawianych w dalszej części pracy. Rozdział rozpoczyna się od definicji pogody kosmicznej, omówienia znaczenia jej monitorowania oraz wpływu zjawisk pochodzących ze Słońca na technologię i infrastrukturę. Dodatkowo przedstawione zostaną aktualne wyzwania w obserwacji i analizie pogody kosmicznej.

Następnie opisane zostaną główne zjawiska pogody kosmicznej, a rozdział zakończy się omówieniem systemów satelitarnych i centrów monitorowania, stanowiących źródło danych wykorzystywanych w analizie pogody kosmicznej.

Wiedza zawarta w tym rozdziale stanowi fundament do opracowania systemu automatycznego pobierania, analizowania i wizualizowania wybranych parametrów pogody kosmicznej stanowiącego główny cel niniejszej pracy. 

# 1. Wprowadzenie teoretyczne

## 1.1 Wprowadzenie

W podrozdziale 1.1 przestawione zostaną pojęcia związane z pogodą kosmiczną oraz jej znaczenie w kontekście jej monitorowania i analizy. Omówione zostaną kluczowe aspekty umożliwiające zrozumienie zjawisk zachodzących na Słońcu i w przestrzeni międzyplanetarnej oraz ich wpływu na technologię i infrastrukturę na Ziemi. Wiedza zawarta w tym podrozdziale stanowi podstawę do omawiania poszczególnych zjawisk pogody kosmicznej w dalszej części tego rozdziału.

### 1.1a Definicja pogody kosmicznej

Pogoda kosmiczna odnosi się do dynamicznych i wysoce zmiennych warunków panujących w przestrzeni bliskiej Ziemi, obejmujących zjawiska zachodzące na Słońcu, w przestrzeni międzyplanetarnej i systemie magnosfera-jonosfera-termosfera. Niepożądane zmiany w tych obszarach mogą obniżyć wydajność i niezawodność systemów naziemnych i satelitów, prowadząc do poważnych problemów operacyjnych. Do najważniejszych zjawisk wpływających na pogodę kosmiczną należą m.in. promieniowanie magnetometryczne, energetyczne cząstki słoneczne, czy burze geomagnetyczne([D.N Baker, 1998](https://www.sciencedirect.com/science/article/pii/S0273117797010958))

### 1.1b Znaczenie monitorowania i analizy pogody kosmicznej

Monitorowanie pogody kosmicznej pełni kluczową rolę w przewidywaniu i ograniczaniu negatywnych skutków zjawisk słonecznych i międzyplanetarnych dla technologii i infrastruktury na Ziemi. Dane pozyskiwane w czasie rzeczywistym z satelitów i systemów naziemnych umożliwiają wczesne wykrywanie zmian w wietrze słonecznym, strumieniach cząstek i innych parametrach środowiska kosmicznego. Dzięki temu możliwe jest ostrzeganie zespołów obsługujących infrastruktury krytyczne, umożliwiając podejmowanie środków zapobiegawczych. Analizowanie i przewidywanie pogody kosmicznej pozwalają na opracowywanie odpowiednich środków zaradczych([Royal Academy of Engineering, 2013](https://raeng.org.uk/media/lz2fs5ql/space_weather_full_report_final.pdf)).

### 1.1c Wpływ zjawisk słonecznych na technologię i infrastrukturę

Zjawiska słoneczne i pogoda kosmiczna mogą znacząco zaburzyć działanie technologii i infrastruktury na Ziemi. Przykładowo, burze geomagnetyczne i koronalne wyrzuty masy(CME) mogą powodować awarie satelitów, uszkadzać systemy komunikacji lub prowadzić do awarii sieci energetycznych([Dabin Xue, 2024](https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2024SW004055)). Zaburzenia i nietypowe zachowania spowodowane silną burzą geomagnetyczną zostały odnotowane już w XIX wieku, podczas tzw. Carrington Event, 2 Września 1859 roku. Operatorzy linii telegraficznych w Europie i Ameryce Północnej odnotowali przerwy w komunikacji, iskrzenie na liniach, a nawet kontynuowali przesyłanie wiadomości po odłączeniu zasilania, wykorzystując wyindukowany przez burze geomagnetyczną prąd([C. Muller, 2014](https://link.springer.com/article/10.1007/s11084-014-9368-3)). Przykład ten pokazuje podatność infrastruktury przewodzącej prąd na skutki ekstremalnej pogody kosmicznej.

### 1.1d Aktualne wyzwania w prognozowaniu pogody kosmicznej

W literaturze dotyczącej prognozowania pogody kosmicznej podkreśla się liczne wyzwania, ograniczające skuteczność jej monitorowania i prognozowania. Do głównych problemów definiowanych w literaturze należą:

- Niepewność w modelach - modele fizyczne i prognostyczne przyjmują liczne przybliżenia, co prowadzi do istotnej niepewności w wynikach([S.K. Morley, 2019](https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2018SW002108))
- Niewielki czas wyprzedzenia prognozy - wiele modeli działa dobrze w krótkim terminie, ale ich wydajność spada dla dłuższych okresów, ograniczając ich wydajność([S.K. Morley, 2019](https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2018SW002108)).
- Problem dokładnej specyfikacji stanu wiatru słonecznego przed Ziemią - pomiary w punkcie L1 mogą nie odpowiadać dokładnie warunkom w magnetosferze Ziemi([S.K. Morley, 2019](https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2018SW002108)).
- Nierównomierne rozłożenie sieci obserwacyjnej - globalna sieć obserwacyjna nie jest w pełni równomiernie rozłożona po globie, zwłaszcza w obszarach trudno dostępnych, co ogranicza zdolność do pełnego monitorowania warunków pogody kosmicznej([J.J. Love, 2017](https://agupubs.onlinelibrary.wiley.com/doi/pdfdirect/10.1002/2017SW001665)).
- Poprawa jakości danych - aby zwiększyć użyteczność prognoz, należy zwiększyć częstotliwość próbkowania, jakość zbieranych danych oraz minimalizowanie czasu opóźnienia([J.J. Love, 2017](https://agupubs.onlinelibrary.wiley.com/doi/pdfdirect/10.1002/2017SW001665)).

Podsumowując, prognozowanie i monitorowanie pogody kosmicznej napotyka wiele wyzwań, które ograniczają jego skuteczność. Można je jednak częściowo minimalizować poprzez odpowiednie działania, takie jak poprawa jakości i częstotliwości danych. 

## 1.2 Zjawiska pogody kosmicznej 

W podrozdziale 1.2 przedstawione zostaną główne zjawiska pogody kosmicznej, które wpływają na technologię i infrastrukturę na Ziemi. Omówione zostaną kolejno: rozbłyski słoneczne, koronalne wyrzuty masy(CME), burze geomagnetyczne, protony słoneczne i cząstki energetyczne, pole magnetyczne międzyplanetarne oraz aktywne regiony słoneczne. Ich zrozumienie jest niezbędne w celu efektywnego monitorowania, pobierania i analizowania zjawisk pogody kosmicznej. 

### 1.2a Rozbłyski słoneczne

Rozbłyski słoneczne to gwałtowne uwolnienia energii magnetycznej w atmosferze Słońca, zachodzące w wyniku rekonekcji linii pola magnetycznego. Energia uwalniana podczas rozbłysku ma około 10^28 - 10^32 erg(1 erg = 1E-7 J) i przyjmuje zróżnicowane formy takie jak: energii promieniowania, kinetycznej ruchu masowego, termicznej oraz nietermicznej. 

Rozbłyski słoneczne generują fale uderzeniowe, wyrzuty plazmy i cząstek energetycznych, które mogą oddziaływać na Ziemię i systemy znajdujące się w przestrzeni kosmicznej np. satelity([K. Shibata, 2011](https://link.springer.com/article/10.12942/lrsp-2011-6)). 

Rozbłyski słoneczne są klasyfikowane ze względu na ich szczytową moc na poszczególne typy([Solar Center Stanford](https://solar-center.stanford.edu/sid/activities/flare.html)):

| Klasa | Zakres maksymalnej mocy(*I*, W/m^2) pomiędzy 1 a 8Å (1Å = 0.1nm) | Wpływ na Ziemię                                              |
| ----- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| A     | *I*  < 10E-7 W/m^2                                           | Za małe, żeby wyrządzić krzywdę                              |
| B     | 10E-7 W/m^2 <= *I*  < 10E-6 W/m^2                            | Za małe, żeby wyrządzić krzywdę                              |
| C     | 10E-6 W/m^2 <= *I*  < 10E-5 W/m^2                            | Możliwe minimalne zaburzenia w komunikacji radiowej          |
| M     | 10E-5 W/m^2 <= *I*  < 10E-4 W/m^2                            | Może powodować krótkie blackouty radiowe                     |
| X     | 10E-4 W/m^2 <= *I*                                           | Może powodować długotrwałe blackouty radiowe i burze radiacyjne |

Rozmiar i czas trwania rozbłysków zależą od ich mocy, czas trwania rozbłysku to od 10^3 do 10^4 s, a ich wysokość pętli magnetycznych przyjmuje wartości od około 10^4 km do 10^5 km([K. Shibata, 2011](https://link.springer.com/article/10.12942/lrsp-2011-6)).

### 1.2b Koronalne wyrzuty masy

Koronalne wyrzuty masy(ang. Coronal Mass Ejection, CME) to ogromne wyrzuty masy plazmy i pola magnetycznego z korony Słońca, które przemieszcza się w przestrzeni międzyplanetarnej. Plazma wyrzucana przez CME może mieć masę rzędu miliardów ton(tj. ~10^12kg lub więcej) i zawierać zamrożone w niej pola magnetyczne silniejsze niż tło wiatru słonecznego. Najszybsze CME skierowane w stronę Ziemi mogą do niej dotrzeć w czasie od 15 do 18 godzin i przemieszczają się z prędkością od ~250 km/s do ~3000 km/s, a w trakcie oddalania się od Słońca stają się coraz większe. Niektóre koronalne wyrzuty masy mogą osiągnąć rozmiar prawie ćwierć dystansu z Ziemi do Słońca([Space Weather Prediction Center](https://www.swpc.noaa.gov/phenomena/coronal-mass-ejections)).

Wyrzuty są istotnym składnikiem pogody kosmicznej i podczas kontaktu z Ziemskim środowiskiem magnetycznym mogą doprowadzić do poważnych konsekwencji takich jak np. tymczasowo podgrzać górną atmosferę Ziemi potencjalnie powodować utratę wysokości przez satelity, spowodować poważne burze geomagnetyczne, czy uszkadzać sieci energetyczne([Science NASA](https://science.nasa.gov/sun/solar-storms-and-flares/#coronal-mass-ejection)).

Ważnymi parametrami CME są rozmiar, prędkość i kierunek, są one określane na podstawie danych z koronografów satelitarnych, które pozwalają również na określenie prawdopodobieństwa dotarcia do Ziemi i jaki może mieć efekt([Space Weather Prediction Center](https://www.swpc.noaa.gov/phenomena/coronal-mass-ejections)).

### 1.2c Burze geomagnetyczne

Burza geomagnetyczna to znaczne zaburzenie magnetosfery Ziemi, wynikające z efektywnego przekazania energii wiatru słonecznego do otaczającego Ziemię środowiska kosmicznego. Wynikają głownie z przedłużonych okresów wysokiej prędkości wiatru słonecznego oraz skierowanego południowo pola magnetycznego wiatru słonecznego, co sprzyja transferowi energii([Space Weather Prediction Center](https://www.swpc.noaa.gov/phenomena/geomagnetic-storms)).

Głównymi czynnikami odpowiadającymi za powstawanie burz geomagnetycznych są koronalne wyrzuty masy(CME) oraz strumienie wiatru słonecznego dużej prędkości(HSS, high-speed solar wind streams), po spełnieniu warunku południowego pola magentycznego dochodzi do przeniesienia energii i powstania burzy([Space Weather Prediction Center](https://www.swpc.noaa.gov/phenomena/geomagnetic-storms)).

Do skutków burz geomagnetycznych należą m.in indukowanie prądu zdolnego uszkadzać transformatory([V. D. Albertson, 1974](https://ieeexplore.ieee.org/abstract/document/4075457)), zakłócanie działania systemów nawigacyjnych([P. V. S. Rama Rao, 2009](https://angeo.copernicus.org/articles/27/2101/2009/)) oraz uszkadzanie satelitów([Space Weather Canada](https://www.spaceweather.gc.ca/tech/index-en.php#sat)).

Do opisywania burz geomagnetycznych używa się indeks Kp oraz skalę G, które instytucje wykorzystują do ostrzegania przed ryzykiem występowania zaburzeń spowodowanych przez zaburzenia magnetosfery([Space Weather Prediction Center](https://www.swpc.noaa.gov/phenomena/geomagnetic-storms)). 

- Indeks Kp przyjmuje wartości od 0 do 9, gdzie niższe wartości oznaczają spokojną magnetosferę, a wartości od 5 do 9 oznaczają burze geomagnetyczne oraz jest definiowana. 
- Skala G służy do klasyfikacji burz geomagnetycznych. G-1 odpowiada wartości 5 dla Kp, a G-5 wartości 9([Space Weather Prediction Center](https://www.swpc.noaa.gov/noaa-scales-explanation)).

| Indeks Kp | Skala G | Opis burzy  | Wpływ na technologię i infrastrukturę                        |
| --------- | ------- | ----------- | ------------------------------------------------------------ |
| < 5       | N/A     | Spokojna    | Brak lub minimalne                                           |
| 5         | G-1     | Słaba       | Mały wpływ na sieci energetyczne i satelity                  |
| 6         | G-2     | Umiarkowana | Możliwe uszkodzenia transformatorów, wpływ na predykcje orbity satelitów |
| 7         | G-3     | Mocna       | Możliwe wywoływanie fałszywych alarmów w pewnych urządzeniach, zwiększony opór satelitów |
| 8         | G-4     | Poważna     | Możliwe powszechne problemy z kontrolą napięcia, problemy z namierzaniem satelitów |
| 9         | G-5     | Ekstremalna | Możliwe blackouty systemów energetycznych, problemy ze śledzeniem i komunikacją z satelitami |

