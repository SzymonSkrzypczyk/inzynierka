W tym rozdziale przedstawiono szczegółową implementację systemu, zgodnie z architekturą opisaną w poprzednim rozdziale. Rozdział został podzielony podrozdziały odpowiadające każdemu z modułów systemu. Każdy moduł został opisany pod względem wykorzystanych technologii, struktur kodu oraz sposobu działania.

##  3.1 Moduł źródła danych

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

>  Rys 2.1.1 Przykładowy format danych JSON zwracanych przez punkt końcowy API SWPC

## 3.2 Moduł pozyskiwania danych

Moduł pozyskiwania danych obejmuje wszystkie operacje związane z pobieraniem danych z modułu źródła danych. W celu spełnienia wymagań systemu dotyczących wydajności oraz sposobu pozyskiwania danych, są one pobierane asynchronicznie umożliwiając niemal jednoczesne przetwarzanie wielu punktów końcowych API. Dodatkowo każda operacja jest logowana w celu umożliwienia efektywnego rozwiązywania potencjalnych błędów wykonania. Przetwarzanie danych przychodzących rozpoczyna się od przygotowania miejsca przechowywania pobranych plików, w tym celu w przypadku braku docelowego katalogu zostanie on stworzony.

```python
async def retrieve_data(target_name: str, url: str, target_dir: Union[str, Path] = SAVE_DIR):
    """
    Retrieve a data for a specific url

    :param target_name:
    :param url:
    :param target_dir:
    :return:
    """
    target_dir = Path(target_dir)
    target_dir.mkdir(parents=True, exist_ok=True)
    logger.log(f"Retrieving data from URL {url}")
```

>  Rys 2.2.1 Fragment kodu definiujący funkcję asynchroniczną oraz tworzącą docelowy katalog w przypadku jego braku

W dalszej części funkcji wykonywane jest odwołanie do aktualnie przetwarzanego punkt końcowego. W przypadku zwrócenia błędu przez API punkt końcowy zostaje ponownie odpytany o dane, dodatkowo wszystkie informacje o błędach zostają zapisane w celu identyfikacji potencjalnych błędów. W przypadku zwrócenia błędu jest on dodany do logów systemu, a następnie jeśli aktualna próba nie przekracza limitu dopuszczalnej ilości prób cały proces zostaje powtórzony.

```python
async with aiohttp.ClientSession() as session:
    async with session.get(url) as response:
        retries = 0
        while retries < MAX_RETRIES:
            try:
                if not response.ok:
                    if response.status == 403:
                        logger.log_error(f"Forbidden: {response.status}")
                        raise Exception(f"Forbidden: {response.status}")
                    elif response.status == 500:
                        logger.log_error(f"Server error: {response.status}")
                        raise Exception(f"Server error: {response.status}")
                    elif response.status == 503:
                        logger.log_error(f"Service unavailable: {response.status}")
                        raise Exception(f"Service unavailable: {response.status}")

                data = await response.json()

                if data is None or not data:
                    logger.log_error(f"No data found for the given date range")
                    raise Exception(f"No data found for the given date range")

                ...
            except Exception as e:
                retries += 1
                logger.log_error(f"Error retrieving data from {url}: {e}. Retrying {retries}/3")
                logger.log(f"Sleeping for {RETRY_SLEEP_TIME} seconds before retrying")
                await asyncio.sleep(RETRY_SLEEP_TIME)	
        else:
            logger.log_error(f"Failed to retrieve data from {url} after {MAX_RETRIES} retries")
            raise Exception(f"Failed to retrieve data from {url} after {MAX_RETRIES} retries")
```

> Rys 2.2.2 Fragment kodu odpowiedzialny za asynchroniczne odwoływanie się do punktu końcowego, obsługę błędów oraz ponowne próby

W dalszej części sprawdzana jest struktura zwróconych danych, a w przypadku zidentyfikowania danych zagnieżdżonych, ich odpowiedniego spłaszczenia, a następnie zapisania do odpowiedniego pliku wynikowego we wcześniej utworzonym katalogu docelowym. W celu umożliwienia ciągłego przepływu danych sprawdzana jest potencjalna zawartość pliku i w wypadku obecności zawartości jest ona dopisywana.

```python
has_nested = any(isinstance(item, dict) for item in data)
if has_nested:
    logger.log_warning(f"Data contains nested structures, flattening the data for {target_name}")
    # Flatten the data if it contains nested structures
    data = [
        {**item, **{k: v for k, v in item.items() if isinstance(v, dict)}}
        for item in data
    ]


# Append the data to a CSV file
filename = target_dir / f"{target_name}_{datetime.today().date()}.csv"
with open(filename, mode='a', newline='') as file:
    writer = csv.writer(file)
    # Write the header only if the file is empty
    if file.tell() == 0:
        logger.log(f"Writing header for {target_name} to {filename}")
        writer.writerow(data[0].keys())
    for item in data:
        writer.writerow(item.values())

    logger.log(f"Data retrieved and saved to {filename}")	
```

> Rys 2.2.3 Fragment kodu odpowiadający za spłaszczanie oraz zapisywanie plików w katalogu docelowym

Po integracji powyższe fragmenty umożliwiają wydajne, bezpieczne pobieranie danych pochodzących z modułu źródła danych zgodnie z wymaganiami opisanymi w poprzednim rozdziale.

Plan +-:

W niniejszym rozdziale przedstawiono szczegółową implementację systemu, zgodnie z architekturą opisaną w poprzednim rozdziale. Rozdział został podzielony na moduły funkcjonalne, z których każdy odpowiada za inny etap przetwarzania danych. Dla każdego modułu opisano zastosowane technologie, strukturę kodu, sposób działania oraz najważniejsze decyzje projektowe.

Źródło danych
W tym podrozdziale zostanie omówione wykorzystywane źródło danych, jego format, dostępność, sposób autoryzacji oraz ograniczenia techniczne. Zaprezentowane zostaną przykładowe dane wejściowe wykorzystywane w systemie.

Moduł pobierania danych ze źródła
Opisane zostaną mechanizmy odpowiedzialne za komunikację ze źródłem danych, stosowane biblioteki, obsługa błędów, walidacja odpowiedzi oraz harmonogram wykonywania operacji pobierania.

Moduł archiwizacji danych
Przedstawiona zostanie metoda przechowywania pobranych danych, format archiwów, sposób organizacji plików, mechanizmy kompresji oraz polityka dotycząca cyklu życia danych.

Moduł przetwarzania danych
Podrozdział ten zawiera opis procesu analizy i transformacji danych, wykorzystywane algorytmy, biblioteki oraz techniki filtracji, agregacji i czyszczenia danych. Omówione zostaną również optymalizacje i decyzje dotyczące wydajności.

Moduł dodawania danych do bazy danych
Opisany zostanie sposób komunikacji z bazą danych, struktura tabel, wykorzystane narzędzia (np. ORM), obsługa transakcji oraz mechanizmy zapewniające integralność i spójność danych.

Moduł wizualizacji wyników
W tej części zostaną przedstawione rozwiązania pozwalające na prezentację wyników przetwarzania, wykorzystywane narzędzia do wizualizacji, przygotowywane wykresy lub dashboardy oraz sposób integracji modułu z pozostałymi elementami systemu.