from pathlib import Path
import csv
import requests

URLS = [
    "https://services.swpc.noaa.gov/json/boulder_k_index_1m.json",
    "https://services.swpc.noaa.gov/json/planetary_k_index_1m.json",
    "https://services.swpc.noaa.gov/json/goes/satellite-longitudes.json",
    "https://services.swpc.noaa.gov/json/goes/primary/magnetometers-1-day.json",
    "https://services.swpc.noaa.gov/json/goes/primary/differential-electrons-1-day.json",
    "https://services.swpc.noaa.gov/json/goes/primary/differential-protons-1-day.json",
    "https://services.swpc.noaa.gov/json/goes/primary/integral-electrons-1-day.json",
    "https://services.swpc.noaa.gov/json/goes/primary/integral-protons-1-day.json",
    "https://services.swpc.noaa.gov/json/goes/primary/xray-1-day.json",
    "https://services.swpc.noaa.gov/json/goes/secondary/differential-electrons-1-day.json",
    "https://services.swpc.noaa.gov/json/goes/secondary/differential-protons-1-day.json",
    "https://services.swpc.noaa.gov/json/goes/secondary/integral-electrons-1-day.json",
    "https://services.swpc.noaa.gov/json/goes/secondary/integral-protons-1-day.json",
    "https://services.swpc.noaa.gov/json/goes/secondary/xray-1-day.json",
    "https://services.swpc.noaa.gov/json/solar-cycle/observed-solar-cycle-indices.json",
    "https://services.swpc.noaa.gov/json/solar-cycle/f10-7cm-flux.json",
    "https://services.swpc.noaa.gov/json/solar-cycle/predicted-solar-cycle.json",
    "https://services.swpc.noaa.gov/json/solar_regions.json",
    "https://services.swpc.noaa.gov/json/solar-radio-flux.json",
    "https://services.swpc.noaa.gov/json/dscovr/dscovr_mag_1s.json"
]