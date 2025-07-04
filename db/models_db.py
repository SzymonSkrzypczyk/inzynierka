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


class F107Flux(Base):
    __tablename__ = "f10_7cm_flux"
    id = Column(Integer, primary_key=True, autoincrement=True)
    time_tag = Column(DateTime, unique=True, index=True)
    f107 = Column("f10.7", Float)


class Magnetometers1Day(Base):
    __tablename__ = "magnetometers_1_day"
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
    __tablename__ = "observed_solar_cycle_indices"
    id = Column(Integer, primary_key=True, autoincrement=True)
    time_tag = Column(DateTime, unique=True, index=True)
    ssn = Column(Float)
    smoothed_ssn = Column(Float)
    observed_swpc_ssn = Column(Float)
    smoothed_swpc_ssn = Column(Float)
    f107 = Column("f10.7", Float)
    smoothed_f107 = Column("smoothed_f10.7", Float)


class PlanetaryKIndex1m(Base):
    __tablename__ = "planetary_k_index_1m"
    id = Column(Integer, primary_key=True, autoincrement=True)
    time_tag = Column(DateTime, unique=True, index=True)
    kp_index = Column(Float)
    estimated_kp = Column(Float)
    kp = Column(String)


class PredictedSolarCycle(Base):
    __tablename__ = "predicted_solar_cycle"
    id = Column(Integer, primary_key=True, autoincrement=True)
    time_tag = Column(DateTime, unique=True, index=True)
    predicted_ssn = Column(Float)
    high25_ssn = Column(Float)
    high_ssn = Column(Float)
    high75_ssn = Column(Float)
    low25_ssn = Column(Float)
    low_ssn = Column(Float)
    low75_ssn = Column(Float)
    predicted_f107 = Column(Float)
    high25_f107 = Column(Float)
    high_f107 = Column(Float)
    high75_f107 = Column(Float)
    low25_f107 = Column(Float)
    low_f107 = Column(Float)
    low75_f107 = Column(Float)


class ParticleMeasurement(Base):
    __tablename__ = "particle_measurements"
    id = Column(Integer, primary_key=True, autoincrement=True)
    time_tag = Column(DateTime)
    satellite = Column(String)
    flux = Column(Float)
    energy = Column(Float)
    particle_type = Column(Enum("electron", "proton", name="particle_type_enum"))
    aggregation = Column(Enum("differential", "integral", name="aggregation_type_enum"))
    satellite_type = Column(Enum("primary", "secondary", name="satellite_type_enum"))

    __table_args__ = (
        UniqueConstraint("time_tag", "satellite", "particle_type", "aggregation", "satellite_type", name="uq_particle_measurements"),
    )


class ProtonDifferentialExtra(Base):
    __tablename__ = "proton_differential_extras"
    id = Column(Integer, primary_key=True, autoincrement=True)
    time_tag = Column(DateTime)
    satellite = Column(String)
    yaw_flip = Column(Boolean)
    channel = Column(String)

    __table_args__ = (
        UniqueConstraint("time_tag", "satellite", name="uq_proton_extras"),
    )


class XRayMeasurement(Base):
    __tablename__ = "xray_measurements"
    id = Column(Integer, primary_key=True, autoincrement=True)
    time_tag = Column(DateTime)
    satellite = Column(String)
    flux = Column(Float)
    observed_flux = Column(Float)
    electron_correction = Column(Float)
    electron_contaminaton = Column(Float)
    energy = Column(String)
    satellite_type = Column(Enum("primary", "secondary", name="xray_satellite_type_enum"))

    __table_args__ = (
        UniqueConstraint("time_tag", "satellite", "satellite_type", name="uq_xray_measurements"),
    )


class SatelliteLongitude(Base):
    __tablename__ = "satellite_longitudes"
    id = Column(Integer, primary_key=True, autoincrement=True)
    satellite = Column(String, unique=True)
    longitude = Column(Float)


class SolarRadioFlux(Base):
    __tablename__ = "solar_radio_flux"
    id = Column(Integer, primary_key=True, autoincrement=True)
    time_tag = Column(DateTime)
    common_name = Column(String)
    details = Column(String)

    __table_args__ = (
        UniqueConstraint("time_tag", "common_name", name="uq_radio_flux"),
    )


class SolarRegion(Base):
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
