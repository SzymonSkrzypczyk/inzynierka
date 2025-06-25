# dscovr_mag_1s  
- **time_tag** – znacznik czasu (ISO 8601, co 1 s)  
- **bt** – całkowite natężenie pola magnetycznego (nanotesle) :contentReference[oaicite:0]{index=0}  
- **bx_gse**, **by_gse**, **bz_gse** – składowe pola w układzie GSE (nanotesle) :contentReference[oaicite:1]{index=1}  
- **theta_gse**, **phi_gse** – kąty inklinacji i azymutu w układzie GSE (stopnie) :contentReference[oaicite:2]{index=2}  
- **bx_gsm**, **by_gsm**, **bz_gsm** – składowe pola w układzie GSM (nanotesle) :contentReference[oaicite:3]{index=3}  
- **theta_gsm**, **phi_gsm** – kąty inklinacji i azymutu w układzie GSM (stopnie) :contentReference[oaicite:4]{index=4}  

# f10-7cm-flux  
- **time-tag** – data pomiaru (ISO, dzienna lub miesięczna) :contentReference[oaicite:5]{index=5}  
- **f10.7** – strumień radiowy F10.7 (unit sfu) :contentReference[oaicite:6]{index=6}  

# magnetometers-1-day  
- **time_tag** – znacznik czasu (ISO, dzienna agregacja)  
- **satellite** – identyfikator satelity GOES  
- **He**, **Hp**, **Hn** – składowe lub współczynniki pola charakteryzujące kierunki  
- **total** – całkowita wartość pola  
- **arcjet_flag** – flaga detekcji efektu arc-jet (oznaczenie potencjalnej anomalii)  

# observed-solar-cycle-indices  
- **time-tag** – data pomiaru (miesiąc)  
- **ssn** – obserwowana liczba plam słonecznych  
- **smoothed_ssn** – wygładzona wartość liczby plam  
- **observed_swpc_ssn** – odczyt liczby plam przez SWPC  
- **smoothed_swpc_ssn** – wygładzony odczyt liczby plam przez SWPC  
- **f10.7** – obserwowany strumień radiowy F10.7  
- **smoothed_f10.7** – wygładzony strumień F10.7  

# planetary_k_index_1m  
- **time_tag** – znacznik czasu (ISO, co minutę)  
- **kp_index** – liczbowy indeks geomet. Kp (0–9 z krokiem 1/3)  
- **estimated_kp** – szacowany indeks Kp  
- **kp** – klasyfikacja w postaci tekstowej (np. „4+”) :contentReference[oaicite:7]{index=7}  

# predicted-solar-cycle  
- **time-tag** – miesiąc (format YYYY-MM)  
- **predicted_ssn** – prognozowana medianowa liczba plam słonecznych  
- **high25_ssn**, **high_ssn**, **high75_ssn** – górne granice przedziałów 25%, mediana, 75%  
- **low25_ssn**, **low_ssn**, **low75_ssn** – dolne granice tych przedziałów  
- **predicted_f10.7** – prognozowany medianowy strumień F10.7  
- **high25_f10.7**, **high_f10.7**, **high75_f10.7** – górne prognozy F10.7 (percentyle)  
- **low25_f10.7**, **low_f10.7**, **low75_f10.7** – dolne prognozy F10.7 (percentyle) :contentReference[oaicite:8]{index=8}  

# primary-differential-electrons-1-day  
- **time_tag** – znacznik czasu (ISO, dzienna agregacja)  
- **satellite** – identyfikator satelity GOES  
- **flux** – strumień różnicowy elektronów (counts/cm²·s·sr·MeV)  
- **energy** – energia pomiaru (MeV) :contentReference[oaicite:9]{index=9}  

# primary-differential-protons-1-day  
- **time_tag** – znacznik czasu (ISO)  
- **satellite** – identyfikator satelity GOES  
- **flux** – strumień różnicowy protonów  
- **energy** – energia (MeV)  
- **yaw_flip** – informacja o odwróceniu stabilizacji satelity  
- **channel** – użyty kanał pomiarowy  

# primary-integral-electrons-1-day  
- **time_tag** – znacznik czasu (ISO)  
- **satellite** – identyfikator satelity GOES  
- **flux** – strumień całkowity elektronów (≥ próg energii)  
- **energy** – wartość progowa energii (MeV)  

# primary-integral-protons-1-day  
- analogiczny zestaw pól co wyżej, ale dla protonów  

# primary-xray-1-day  
- **time_tag** – znacznik czasu (ISO)  
- **satellite** – identyfikator satelity GOES  
- **flux** – skorygowany strumień promieniowania rentgenowskiego (W/m²)  
- **observed_flux** – surowy pomiar strumienia rentgenowskiego  
- **electron_correction** – korekta na wpływ elektronów  
- **electron_contaminaton** – stopień kontaminacji przez elektrony  
- **energy** – zakres energii kanału  

# satellite-longitudes  
- **satellite** – identyfikator satelity GOES  
- **longitude** – długość geograficzna bezpośrednio poniżej satelity (stopnie)  

# secondary-differential-electrons-1-day  
- pola takie jak w sekcji „primary-differential-electrons”, ale dot. satelity drugorzędnego GOES  

# secondary-differential-protons-1-day  
- jak w „primary-differential-protons”, plus:  
  - **yaw_flip** – flaga rotacji satelity  
  - **channel** – kanał pomiarowy  

# secondary-integral-electrons-1-day  
- analogicznie do primary-integral-electrons dla satelity drugorzędnego  

# secondary-integral-protons-1-day  
- analogicznie jak powyżej, ale dla protonów  

# secondary-xray-1-day  
- jak w primary-xray, ale dane z satelity drugorzędnego  

# solar-radio-flux  
- **time_tag** – znacznik czasu (ISO, np. miesięcznie)  
- **common_name** – nazwa mierzonej wartości (np. „F10.7”)  
- **details** – dodatkowe uwagi lub szczegóły dotyczące pomiaru  

# solar_regions  
- **observed_date** – data obserwacji regionu  
- **region** – numer regionu przydzielony przez NOAA  
- **latitude**, **longitude** – heliograficzne współrzędne regionu  
- **location** – ogólny opis położenia (np. „południowy biegun”)  
- **carrington_longitude**, **old_carrington_longitude** – bieżąca i poprzednia długość według ukł. Carringtona  
- **area** – powierzchnia regionu (w milionowych częściach półkuli słonecznej)  
- **spot_class** – klasyfikacja plam słonecznych (np. McIntosh)  
- **extent** – rozmiar i rozciągłość regionu  
- **number_spots** – liczba plam w regionie  
- **mag_class** – klasa magnetyczna regionu  
- **mag_string** – tekstowy opis klasy magnetycznej  
- **status** – stan regionu (aktywny, wygaszony)  
- **c_xray_events**, **m_xray_events**, **x_xray_events** – liczba zdarzeń rentgenowskich klas C, M, X  
- **proton_events** – liczba zdarzeń protonowych  
- **s_flares** – liczba flar miękkich (soft X-ray)  
- **impulse_flares_1** – **impulse_flares_4** – liczba flar impulsowych w czterech kategoriach  
- **protons** – całkowite zdarzenia protonowe  
- **c_flare_probability**, **m_flare_probability**, **x_flare_probability**, **proton_probability** – prawdopodobieństwo wystąpienia odpowiednich zjawisk  
- **first_date** – data pierwszego wykrycia regionu  