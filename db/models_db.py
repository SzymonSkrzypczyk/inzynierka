from sqlalchemy import (
    Column, Integer, String, Float, DateTime, Boolean, Enum, UniqueConstraint
)
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class DscovrMag1s(Base):
    __tablename__ = "dscovr_mag_1s"
    id = Column(Integer, primary_key=True, autoincrement=True)
    time_tag = Column(DateTime, unique=True, index=True)
    bt = Column(Float)
    bx_gse = Column(Float)
    by_gse = Column(Float)
    bz_gse = Column(Float)
    theta_gse = Column(Float)
    phi_gse = Column(Float)
    bx_gsm = Column(Float)
    by_gsm = Column(Float)
    bz_gsm = Column(Float)
    theta_gsm = Column(Float)
    phi_gsm = Column(Float)


class F107cmFlux(Base):
    __tablename__ = "f10-7cm-flux"
    id = Column(Integer, primary_key=True, autoincrement=True)
    time_tag = Column(DateTime, unique=True, index=True)
    f10_7 = Column("f10.7", Float)


class Magnetometers1Day(Base):
    __tablename__ = "magnetometers-1-day"
    id = Column(Integer, primary_key=True, autoincrement=True)
    time_tag = Column(DateTime)
    satellite = Column(String)
    He = Column(Float)
    Hp = Column(Float)
    Hn = Column(Float)
    total = Column(Float)
    arcjet_flag = Column(Boolean)

    __table_args__ = (
        UniqueConstraint("time_tag", "satellite", name="uq_magnetometers_time_satellite"),
    )


class ObservedSolarCycleIndices(Base):
    __tablename__ = "observed-solar-cycle-indices"
    id = Column(Integer, primary_key=True, autoincrement=True)
    time_tag = Column(DateTime, unique=True, index=True)
    ssn = Column(Float)
    smoothed_ssn = Column(Float)
    observed_swpc_ssn = Column(Float)
    smoothed_swpc_ssn = Column(Float)
    f10_7 = Column("f10.7", Float)
    smoothed_f10_7 = Column("smoothed_f10.7", Float)


class PlanetaryKIndex1m(Base):
    __tablename__ = "planetary_k_index_1m"
    id = Column(Integer, primary_key=True, autoincrement=True)
    time_tag = Column(DateTime, unique=True, index=True)
    kp_index = Column(Float)
    estimated_kp = Column(Float)
    kp = Column(String)


class PredictedSolarCycle(Base):
    __tablename__ = "predicted-solar-cycle"
    id = Column(Integer, primary_key=True, autoincrement=True)
    time_tag = Column(DateTime, unique=True, index=True)
    predicted_ssn = Column(Float)
    high25_ssn = Column(Float)
    high_ssn = Column(Float)
    high75_ssn = Column(Float)
    low25_ssn = Column(Float)
    low_ssn = Column(Float)
    low75_ssn = Column(Float)
    predicted_f10_7 = Column("predicted_f10.7", Float)
    high25_f10_7 = Column("high25_f10.7", Float)
    high_f10_7 = Column("high_f10.7", Float)
    high75_f10_7 = Column("high75_f10.7", Float)
    low25_f10_7 = Column("low25_f10.7", Float)
    low_f10_7 = Column("low_f10.7", Float)
    low75_f10_7 = Column("low75_f10.7", Float)


class PrimaryDifferentialElectrons1Day(Base):
    __tablename__ = "primary-differential-electrons-1-day"
    id = Column(Integer, primary_key=True, autoincrement=True)
    time_tag = Column(DateTime)
    satellite = Column(String)
    flux = Column(Float)
    energy = Column(Float)


class PrimaryDifferentialProtons1Day(Base):
    __tablename__ = "primary-differential-protons-1-day"
    id = Column(Integer, primary_key=True, autoincrement=True)
    time_tag = Column(DateTime)
    satellite = Column(String)
    flux = Column(Float)
    energy = Column(Float)
    yaw_flip = Column(Boolean)
    channel = Column(String)


class PrimaryIntegralElectrons1Day(Base):
    __tablename__ = "primary-integral-electrons-1-day"
    id = Column(Integer, primary_key=True, autoincrement=True)
    time_tag = Column(DateTime)
    satellite = Column(String)
    flux = Column(Float)
    energy = Column(Float)


class PrimaryIntegralProtons1Day(Base):
    __tablename__ = "primary-integral-protons-1-day"
    id = Column(Integer, primary_key=True, autoincrement=True)
    time_tag = Column(DateTime)
    satellite = Column(String)
    flux = Column(Float)
    energy = Column(Float)


class PrimaryXray1Day(Base):
    __tablename__ = "primary-xray-1-day"
    id = Column(Integer, primary_key=True, autoincrement=True)
    time_tag = Column(DateTime)
    satellite = Column(String)
    flux = Column(Float)
    observed_flux = Column(Float)
    electron_correction = Column(Float)
    electron_contaminaton = Column(Float)
    energy = Column(String)


class SatelliteLongitudes(Base):
    __tablename__ = "satellite-longitudes"
    id = Column(Integer, primary_key=True, autoincrement=True)
    satellite = Column(String, unique=True)
    longitude = Column(Float)


class SecondaryDifferentialElectrons1Day(Base):
    __tablename__ = "secondary-differential-electrons-1-day"
    id = Column(Integer, primary_key=True, autoincrement=True)
    time_tag = Column(DateTime)
    satellite = Column(String)
    flux = Column(Float)
    energy = Column(Float)


class SecondaryDifferentialProtons1Day(Base):
    __tablename__ = "secondary-differential-protons-1-day"
    id = Column(Integer, primary_key=True, autoincrement=True)
    time_tag = Column(DateTime)
    satellite = Column(String)
    flux = Column(Float)
    energy = Column(Float)
    yaw_flip = Column(Boolean)
    channel = Column(String)


class SecondaryIntegralElectrons1Day(Base):
    __tablename__ = "secondary-integral-electrons-1-day"
    id = Column(Integer, primary_key=True, autoincrement=True)
    time_tag = Column(DateTime)
    satellite = Column(String)
    flux = Column(Float)
    energy = Column(Float)


class SecondaryIntegralProtons1Day(Base):
    __tablename__ = "secondary-integral-protons-1-day"
    id = Column(Integer, primary_key=True, autoincrement=True)
    time_tag = Column(DateTime)
    satellite = Column(String)
    flux = Column(Float)
    energy = Column(Float)


class SecondaryXray1Day(Base):
    __tablename__ = "secondary-xray-1-day"
    id = Column(Integer, primary_key=True, autoincrement=True)
    time_tag = Column(DateTime)
    satellite = Column(String)
    flux = Column(Float)
    observed_flux = Column(Float)
    electron_correction = Column(Float)
    electron_contaminaton = Column(Float)
    energy = Column(String)


class SolarRadioFlux(Base):
    __tablename__ = "solar-radio-flux"
    id = Column(Integer, primary_key=True, autoincrement=True)
    time_tag = Column(DateTime)
    common_name = Column(String)
    details = Column(String)

    __table_args__ = (
        UniqueConstraint("time_tag", "common_name", name="uq_radio_flux"),
    )


class SolarRegions(Base):
    __tablename__ = "solar_regions"
    id = Column(Integer, primary_key=True, autoincrement=True)
    observed_date = Column(DateTime)
    region = Column(Integer)
    latitude = Column(Float)
    longitude = Column(Float)
    location = Column(String)
    carrington_longitude = Column(Float)
    old_carrington_longitude = Column(Float)
    area = Column(Float)
    spot_class = Column(String)
    extent = Column(String)
    number_spots = Column(Integer)
    mag_class = Column(String)
    mag_string = Column(String)
    status = Column(String)
    c_xray_events = Column(Integer)
    m_xray_events = Column(Integer)
    x_xray_events = Column(Integer)
    proton_events = Column(Integer)
    s_flares = Column(Integer)
    impulse_flares_1 = Column(Integer)
    impulse_flares_2 = Column(Integer)
    impulse_flares_3 = Column(Integer)
    impulse_flares_4 = Column(Integer)
    protons = Column(Integer)
    c_flare_probability = Column(Float)
    m_flare_probability = Column(Float)
    x_flare_probability = Column(Float)
    proton_probability = Column(Float)
    first_date = Column(DateTime)

    __table_args__ = (
        UniqueConstraint("observed_date", "region", name="uq_solar_region"),
    )
