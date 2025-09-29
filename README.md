# Satellite images retrieval tool
As it turns out it's going to be my **bachelor's thesis** ;)

## Features
Right now the tool is able to:

- retrieve a satellite image for given coordinates 
- save it in a given directory 

## To be done

- rewrite the entire tool in GoLang
- compile it so that it can be run by OS on a given schedule
- extend it by adding UI
- more...

https://www.swpc.noaa.gov/content/data-access

free to use, 

# Burze magnetyczne 
https://services.swpc.noaa.gov/json/boulder_k_index_1m.json - Indeks K mierzący aktywność geomagnetyczną na podstawie danych z magnetometru w Boulder, Colorado
https://services.swpc.noaa.gov/json/planetary_k_index_1m.json - Indeks K obliczany na podstawie danych z różnych stacji geomagnetycznych na całym świecie, odzwierciedlający globalną aktywność geomagnetyczną

# Burze radiacyjne
https://services.swpc.noaa.gov/json/goes/satellite-longitudes.json - longitudes of satelites
https://services.swpc.noaa.gov/json/goes/primary/magnetometers-1-day.json

https://services.swpc.noaa.gov/json/goes/primary/differential-electrons-1-day.json - elektrony 
https://services.swpc.noaa.gov/json/goes/primary/differential-protons-1-day.json - protony

https://services.swpc.noaa.gov/json/goes/primary/integral-electrons-1-day.json - integral electrons
https://services.swpc.noaa.gov/json/goes/primary/integral-protons-1-day.json - integral protons
https://services.swpc.noaa.gov/json/goes/primary/xrays-1-day.json - promieniowanie X

# Rozblyski Sloneczne
https://services.swpc.noaa.gov/json/solar-cycle/observed-solar-cycle-indices.json - 
https://services.swpc.noaa.gov/json/solar-cycle/f10-7cm-flux.json
https://services.swpc.noaa.gov/json/solar-cycle/predicted-solar-cycle.json
https://services.swpc.noaa.gov/json/solar_regions.json - Zawiera informacje o aktywnych regionach słonecznych, w tym o numerach plam słonecznych i ich potencjale do generowania rozbłysków.
https://services.swpc.noaa.gov/json/solar-radio-flux.json - dostarcza informacji o emisjach radiowych Słońca w paśmie 10,7 cm (2800 MHz), znanych również jako wskaźnik F10.7.

https://services.swpc.noaa.gov/json/dscovr/dscovr_mag_1s.json - do wiatru slonecznego

https://services.swpc.noaa.gov/json/goes/primary/xray-flares-7-day.json
https://services.swpc.noaa.gov/json/goes/primary/integral-protons-plot-1-day.json

# Satellites descriptions

## 13 - **[GOES-13](https://space.oscar.wmo.int/satellites/view/goes_13)**

### Known instruments:
1. Geostationary Search and Rescue([GEOS&R](https://space.oscar.wmo.int/instruments/view/geos_r)) - To relay distress signals from users in difficulty to search and rescue centres
2. SEM / Magnetometer([SEM/MAG](https://space.oscar.wmo.int/instruments/view/sem_mag)) - Observation of the geomagnetic field in the magnetosphere
3. GOES Sounder([SOUNDER](https://space.oscar.wmo.int/instruments/view/sounder)) - Atmospheric temperature/humidity sounding
4. Solar X-ray Imager([SXI](https://space.oscar.wmo.int/instruments/view/sxi)) - Space Weather - Solar activity monitoring
5. SEM / Energetic Particles Sensor([SEM/EPS](https://space.oscar.wmo.int/instruments/view/sem_eps)) - Observation of electrons, protons and alpha-particles at platform level
6. SEM / High Energy Proton and Alpha Particles Detector([SEM/HEPAD](https://space.oscar.wmo.int/instruments/view/sem_hepad)) - Observation of high-energy protons and alpha-particles at platform level
7. SEM / X-Ray Sensor - Extreme Ultra-Violet Sensor([SEM/XRS-EUV](https://space.oscar.wmo.int/instruments/view/sem_xrs_euv)) - 	To measure disk-integrated solar X-ray and EUV fluxes
8. Data Collection and Interrogation Service([DCIS](https://space.oscar.wmo.int/instruments/view/dcis)) - Data collection from in-situ Data Collection Platforms
9. GOES Imager([IMAGER](https://space.oscar.wmo.int/instruments/view/imager_goes_12_15)) - Multi-purpose imagery and wind derivation by tracking clouds and water vapour features

### Other information:
- Launch on 24 May 2006

- End of Life in October 2019

- It's inactive

## 15 - **[GOES-15](https://space.oscar.wmo.int/satellites/view/goes_15)**


### Known instruments:

1. Geostationary Search and Rescue([GEOS&R](https://space.oscar.wmo.int/instruments/view/geos_r)) - To relay distress signals from users in difficulty to search and rescue centres
2. SEM / Magnetometer([SEM/MAG](https://space.oscar.wmo.int/instruments/view/sem_mag)) - Observation of the geomagnetic field in the magnetosphere
3. GOES Sounder([SOUNDER](https://space.oscar.wmo.int/instruments/view/sounder)) - Atmospheric temperature/humidity sounding
4. Solar X-ray Imager([SXI](https://space.oscar.wmo.int/instruments/view/sxi)) - Space Weather - Solar activity monitoring
5. SEM / Energetic Particles Sensor([SEM/EPS](https://space.oscar.wmo.int/instruments/view/sem_eps)) - Observation of electrons, protons and alpha-particles at platform level
6. SEM / High Energy Proton and Alpha Particles Detector([SEM/HEPAD](https://space.oscar.wmo.int/instruments/view/sem_hepad)) - Observation of high-energy protons and alpha-particles at platform level
7. SEM / X-Ray Sensor - Extreme Ultra-Violet Sensor([SEM/XRS-EUV](https://space.oscar.wmo.int/instruments/view/sem_xrs_euv)) - 	To measure disk-integrated solar X-ray and EUV fluxes
8. Data Collection and Interrogation Service([DCIS](https://space.oscar.wmo.int/instruments/view/dcis)) - Data collection from in-situ Data Collection Platforms
9. GOES Imager([IMAGER](https://space.oscar.wmo.int/instruments/view/imager_goes_12_15)) - Multi-purpose imagery and wind derivation by tracking clouds and water vapour features

### Other information:

- Launch Date: 4 March 2010

- End of Life: June 2023

- Status: Inactive

## 14 - **[GOES-14](https://space.oscar.wmo.int/satellites/view/goes_14)**


### Known instruments:

1. Geostationary Search and Rescue([GEOS&R](https://space.oscar.wmo.int/instruments/view/geos_r)) - To relay distress signals from users in difficulty to search and rescue centres
2. SEM / Magnetometer([SEM/MAG](https://space.oscar.wmo.int/instruments/view/sem_mag)) - Observation of the geomagnetic field in the magnetosphere
3. GOES Sounder([SOUNDER](https://space.oscar.wmo.int/instruments/view/sounder)) - Atmospheric temperature/humidity sounding
4. Solar X-ray Imager([SXI](https://space.oscar.wmo.int/instruments/view/sxi)) - Space Weather - Solar activity monitoring
5. SEM / Energetic Particles Sensor([SEM/EPS](https://space.oscar.wmo.int/instruments/view/sem_eps)) - Observation of electrons, protons and alpha-particles at platform level
6. SEM / High Energy Proton and Alpha Particles Detector([SEM/HEPAD](https://space.oscar.wmo.int/instruments/view/sem_hepad)) - Observation of high-energy protons and alpha-particles at platform level
7. SEM / X-Ray Sensor - Extreme Ultra-Violet Sensor([SEM/XRS-EUV](https://space.oscar.wmo.int/instruments/view/sem_xrs_euv)) - 	To measure disk-integrated solar X-ray and EUV fluxes
8. Data Collection and Interrogation Service([DCIS](https://space.oscar.wmo.int/instruments/view/dcis)) - Data collection from in-situ Data Collection Platforms
9. GOES Imager([IMAGER](https://space.oscar.wmo.int/instruments/view/imager_goes_12_15)) - Multi-purpose imagery and wind derivation by tracking clouds and water vapour features

### Other information:

- Launch Date: 27 June 2009

- End of Life: >= 2027

- Status: Stand-by as of 29th September 2025

## 16 - **[GOES-16](https://space.oscar.wmo.int/satellites/view/goes_16)**

### Known instruments:
1. **Advanced Baseline Imager** ([ABI](https://space.oscar.wmo.int/instruments/view/abi)) - Multi-purpose VIS/IR imagery and wind derivation by tracking clouds and water vapour features
2. **Extreme Ultraviolet Sensor / X-Ray Sensor Irradiance Sensors** ([EXIS](https://space.oscar.wmo.int/instruments/view/exis)) - To monitor EUV and X-rays from the solar disk
3. **Geostationary Search and Rescue** ([GEOS&R](https://space.oscar.wmo.int/instruments/view/geos_r)) - To relay distress signals from users in difficulty to search and rescue centres
4. **Geostationary Lightning Mapper** ([GLM](https://space.oscar.wmo.int/instruments/view/glm)) - Proxy for convective precipitation, proxy for NOx generation, study of Earth electric field
5. **SEM / Magnetometer** ([SEM/MAG](https://space.oscar.wmo.int/instruments/view/sem_mag)) - Observation of the geomagnetic field in the magnetosphere
6. **Solar Ultraviolet Imager** ([SUVI](https://space.oscar.wmo.int/instruments/view/suvi)) - Space Weather - Solar activity monitoring
7. **Data Collection and Interrogation Service** ([DCIS](https://space.oscar.wmo.int/instruments/view/dcis)) - Data collection from in-situ Data Collection Platforms
9. **SEISS / Magnetospheric Particle Sensor** ([SEISS/MPS](https://space.oscar.wmo.int/instruments/view/seiss_mps)) - To monitor electrons and protons representing a hazard for the satellite
10. **SEISS / Energetic Heavy Ion Sensor** ([SEISS/EHIS](https://space.oscar.wmo.int/instruments/view/seiss_ehis)) - To measure proton, alpha-particle and heavy ion fluxes at platform level
11. **SEISS / Solar and Galactic Proton Sensor** ([SEISS/SGPS](https://space.oscar.wmo.int/instruments/view/seiss_sgps)) - To measure high-energy protons at platform level

### Other information:
- Launch Date: 19 November 2016
- End of Life: >= 2032
- Status: Back up 
