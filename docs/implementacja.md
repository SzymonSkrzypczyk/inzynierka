W tym rozdziale przedstawiono szczegółową implementację systemu, zgodnie z architekturą opisaną w poprzednim rozdziale. Rozdział został podzielony podrozdziały odpowiadające każdemu z modułów systemu. Każdy moduł został opisany pod względem wykorzystanych technologii, struktur kodu oraz sposobu działania.

# 3.1 Moduł źródła danych

Moduł źródła danych obejmuje wszystkie interfejsy programistyczne udostępniane przez Space Weather Prediction Center, które zostały wykorzystane w projekcie. Dane są udostępniane bezpłatnie i bez mechanizmów autoryzacji umożliwiając swobodny dostęp oraz pozyskiwanie danych. Wszystkie wykorzystywane punkty końcowe API zwracają dane w formacie JSON, co umożliwia ich ustrukturyzowane przetwarzanie. Wszystkie punkty końcowe API są dostępne pod adresem `https://services.swpc.noaa.gov/json/`, gdzie dane są na bieżąco aktualizowane. Większość pobieranych danych zawiera unikatowe pola dostępne tylko dla danego punktu końcowego. Istnieje jednak zbiór pól uniwersalnych np. `time_tag`, zawierający znacznik czasu umożliwiający unikatowe zidentyfikowanie danych. W ramach systemu wykorzystywane jest 20 różnych punktów końcowych API SWPC.

```json
[
  {
    "time_tag": "2025-11-14T19:50:00Z",
    "satellite": 18,
    "flux": 647.32666015625,
    "energy": "\u003E=1 MeV"
  },
  {
    "time_tag": "2025-11-14T19:50:00Z",
    "satellite": 18,
    "flux": 5.15482759475708,
    "energy": "\u003E=10 MeV"
  }
]
```

Rys 2.1.1 Przykładowy format danych JSON zwracanych przez punkt końcowy API SWPC

## 2.2 Moduł pozyskiwania danych





