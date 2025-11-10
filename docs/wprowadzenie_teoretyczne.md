W niniejszym rozdziale przedstawione zostaną podstawy teoretyczne dotyczące pogody kosmicznej, umożliwiające zrozumienie zagadnień i zjawisk omawianych w dalszej części pracy. Rozdział rozpoczyna się od definicji pogody kosmicznej, omówienia znaczenia jej monitorowania oraz wpływu zjawisk pochodzących ze Słońca na technologię i infrastrukturę. Dodatkowo przedstawione zostaną aktualne wyzwania w obserwacji i analizie pogody kosmicznej.

Następnie opisane zostaną główne zjawiska pogody kosmicznej, a rozdział zakończy się omówieniem systemów satelitarnych i centrów monitorowania, stanowiących źródło danych wykorzystywanych w analizie pogody kosmicznej.

Wiedza zawarta w tym rozdziale stanowi fundament do opracowania systemu automatycznego pobierania, analizowania i wizualizowania wybranych parametrów pogody kosmicznej stanowiącego główny cel niniejszej pracy. 

# 1. Wprowadzenie teoretyczne

## 1.1 Wprowadzenie

W podrozdziale 1.1 przestawione zostaną pojęcia związane z pogodą kosmiczną oraz jej znaczenie w kontekście jej monitorowania i analizy. Omówione zostaną kluczowe aspekty umożliwiające zrozumienie zjawisk zachodzących na Słońcu i w przestrzeni międzyplanetarnej oraz ich wpływu na technologię i infrastrukturę na Ziemi. Wiedza zawarta w tym podrozdziale stanowi podstawę do omawiania poszczególnych zjawisk pogody kosmicznej w dalszej części tego rozdziału.

### 1.1a Definicja pogody kosmicznej

Pogoda kosmiczna odnosi się do dynamicznych i wysoce zmiennych warunków panujących w przestrzeni bliskiej Ziemi, obejmujących zjawiska zachodzące na Słońcu, w przestrzeni międzyplanetarnej i systemie magnosfera-jonosfera-termosfera. Nieporządane zmiany w tych obszarach mogą obniżyć wydajność i niezawodność systemów naziemnych i satelitów, prowadząc do poważnych problemów operacyjnych. Do najważniejszych zjawisk wpływających na pogodę kosmiczną należą m.in. promieniowanie magnetometryczne, energetyczne cząstki słoneczne, czy burze geomagnetyczne([D.N Baker, 1998](https://www.sciencedirect.com/science/article/pii/S0273117797010958))

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





