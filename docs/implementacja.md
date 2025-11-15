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

>  Rys 3.1.1 Przykładowy format danych JSON zwracanych przez punkt końcowy API SWPC

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

>  Rys 3.2.1 Fragment kodu definiujący funkcję asynchroniczną oraz tworzącą docelowy katalog w przypadku jego braku

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

> Rys 3.2.2 Fragment kodu odpowiedzialny za asynchroniczne odwoływanie się do punktu końcowego, obsługę błędów oraz ponowne próby

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

> Rys 3.2.3 Fragment kodu odpowiadający za spłaszczanie oraz zapisywanie plików w katalogu docelowym

Po integracji powyższe fragmenty umożliwiają wydajne i niezawodne pobieranie danych pochodzących z modułu źródła danych zgodnie z wymaganiami opisanymi w poprzednim rozdziale.

```python
async def retrieve_all_data():
    """
    Retrieve all data from the URLs in NAME2URL
    """
    tasks = []
    target_dir = SAVE_DIR / f"{datetime.today().date()}"
    for target_name, url in NAME2URL.items():
        tasks.append(retrieve_data(target_name, url, target_dir))
    await asyncio.gather(*tasks)
    logger.log(f"All data retrieved and saved to {target_dir}")
```

> Rys 3.2.4 Fragment kodu odpowiadający za pobieranie wszystkich danych z modułu źródła danych

## 3.3 Moduł archiwizacji danych

W module archiwizacji danych dane pobrane w poprzednim module są pakowane i kompresowane, a następnie wysyłane do katalogu w serwisie Dropbox w celu ich archiwizacji. Serwis Dropbox jest zintegrowany z systemem uwierzytelniania OAuth 2.0, przez co wymaga token odświeżania, który należy pozyskać ręcznie, wykonując proces jednorazowo przed pierwszym uruchomieniem systemu. Token odświeżania umożliwia długotrwałą autoryzację, bez potrzeby ponownego logowania, dzięki czemu jest elementem pasującym do założeń pełnej automatyzacji procesu.

```python
def get_refresh_token(app_key, app_secret):
    auth_flow = DropboxOAuth2FlowNoRedirect(
        consumer_key=app_key,
        consumer_secret=app_secret,
        token_access_type='offline'
    )

    authorize_url = auth_flow.start()
    print("1. Go to: " + authorize_url)
    print("2. Click 'Allow' (you might have to log in first).")
    print("3. Copy the authorization code.")

    auth_code = input("Enter the authorization code here: ").strip()
    oauth_result = auth_flow.finish(auth_code)

    print("Access token:", oauth_result.access_token)
    print("Refresh token:", oauth_result.refresh_token)
    print("Expires in:", oauth_result.expires_at)

    return oauth_result.refresh_token
```

> Rys 3.3.1 Fragment kodu pozyskujący token odświeżania

Archiwizacja danych rozpoczyna się w po poprawnym pozyskaniu wszystkich wymaganych danych z API SWPC. Pierwszym krokiem jest kompresja i zapakowanie katalogów docelowych do formatu zip. Dodatkowo, możliwe jest usunięcie wcześniej utworzonego katalogu docelowego w celu opróżnienia przestrzeni dyskowej.

```python
def compress_data(target_name: str, target_dir: Union[str, Path] = SAVE_DIR, remove_dir: bool = True):
    """
    Compress the data directory into a zip file

    :param target_name:
    :param target_dir:
    :param remove_dir:
    :return:
    """
    target_dir = Path(target_dir)
    target_dir.mkdir(parents=True, exist_ok=True)
    logger.log(f"Compressing data for {target_name}")
    make_archive(
        base_name=str(target_dir.parent / target_name),
        format='zip',
        root_dir=target_dir.parent,
        base_dir=target_dir.name
    )

    if remove_dir:
        logger.log(f"Removing directory {target_dir}")
        rmtree(target_dir, ignore_errors=False)
        logger.log(f"Directory {target_dir} removed")
```

Po utworzeniu archiwum zawierającego oczekiwane dane, są one wysyłane do serwisu Dropbox. W celu zapewnienia niezawodnego przesyłu danych zaimplementowane zostały systemy przetwarzania błędów oraz powtarzania procesu w przypadku błędu. Dodatkowo aby uniknąć nadmiernej liczby połączeń z serwerami Dropbox, przed każdym restartem system odczekuje wcześniej ustaloną ilość czasu.

```python
def send_to_dropbox(
    archive_path: Union[str, Path],
    dropbox_path: str,
    logger: Logger
):
    """
    Upload a file to Dropbox

    :param archive_path: Path to the file to be uploaded
    :param dropbox_path: Path in Dropbox where the file will be uploaded
    :param logger: Logger instance for logging
    """
    dbx = dropbox.Dropbox(
            app_secret=DROPBOX_APP_SECRET,
            app_key=DROPBOX_APP_KEY,
            oauth2_refresh_token=DROPBOX_REFRESH_TOKEN
        )
    retries = 0

    with open(archive_path, "rb") as f:
        logger.log(f"Uploading {archive_path} to Dropbox at {dropbox_path}")
        while retries < MAX_RETRIES:
            try:
                dbx.files_upload(f.read(), dropbox_path, mode=WriteMode('overwrite'))

                logger.log(f"Successfully uploaded {archive_path} to Dropbox at {dropbox_path}")
                return
            except ApiError as e:
                logger.log_exception(f"API error: {e}")
                retries += 1
                logger.log(f"Sleeping for {SEND_RETRY_SLEEP_TIME} seconds before retrying")
                sleep(SEND_RETRY_SLEEP_TIME)

            except AuthError as e:
                logger.log_exception(f"Authentication error: {e}")
                retries += 1
                logger.log(f"Sleeping for {SEND_RETRY_SLEEP_TIME} seconds before retrying")
                sleep(SEND_RETRY_SLEEP_TIME)
        else:
            logger.log_error(f"Failed to upload {archive_path} to Dropbox after {MAX_RETRIES} retries")
            raise Exception(f"Failed to upload {archive_path} to Dropbox after {MAX_RETRIES} retries")
```

> Rys 3.3.2 Fragment kodu przedstawiający wysyłanie danych do serwisu Dropbox

Po integracji powyższe elementy umożliwiają spełnienie założeń modułu archiwizacji danych poprzez efektywne pakowanie, kompresowanie i archiwizowanie danych pobranych w poprzednim module.

```python
compress_data(target_dir.name, target_dir)
logger.log(f"Data compressed to {target_dir}.zip")
send_to_dropbox(target_dir.parent / f"{target_dir.name}.zip", f"{DROPBOX_DIR}/{target_dir.name}.zip", logger)
```

> Rys 3.3.3 Fragment kodu przedstawiający integrację elementów opisywanego modułu

