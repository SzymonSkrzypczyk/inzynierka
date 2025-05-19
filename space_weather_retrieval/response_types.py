from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field


class SolarFlare(BaseModel):
    beginTime: str
    catalog: str
    endTime: str
    flrID: str
    link: str
    note: str
    peakTime: str
    sourceLocation: str
    submissionTime: str
    versionId: int
    activeRegionNum: Optional[int] = None

    class Config:
        extra = "allow"


class CMEAnalyses(BaseModel):
    featureCode: str
    halfAngle: float
    imageType: str
    isMostAccurate: bool
    latitude: Optional[float] = None
    levelOfData: int
    link: str
    longitude: Optional[float] = None
    measurementTechnique: str
    speed: float
    submissionTime: str
    time21_5: str
    type: str
    tilt: Optional[float] = None
    speedMeasuredAtHeight: Optional[float] = None
    enlilList: List[Dict[str, Any]] = Field(default_factory=list)
    minorHalfWidth: Optional[float] = None
    note: Optional[str] = None


class CMEInstrument(BaseModel):
    displayName: str


class CMELinkedEvent(BaseModel):
    activityID: str


class CoronalMassEjection(BaseModel):
    cmeAnalyses: List[CMEAnalyses]
    instruments: List[CMEInstrument]
    link: str
    activityID: str
    catalog: str
    note: str
    sourceLocation: str
    startTime: str
    submissionTime: str
    versionId: int
    activeRegionNum: Optional[int] = None
    linkedEvents: Optional[List[CMELinkedEvent]] = None

    class Config:
        extra = "allow"


class CoronalMassEjectionAnalysis(BaseModel):
    associatedCMEID: str
    associatedCMEstartTime: str
    catalog: str
    dataLevel: str
    featureCode: str
    halfAngle: float
    imageType: str
    isMostAccurate: bool
    latitude: float
    link: str
    longitude: float
    measurementTechnique: str
    note: str
    speed: float
    submissionTime: str
    time21_5: str
    type: str
    versionId: int
    tilt: Optional[float] = None
    speedMeasuredAtHeight: Optional[float] = None
    minorHalfWidth: Optional[float] = None


class GSKpIndex(BaseModel):
    kpIndex: float
    observedTime: str
    source: str


class GSLinkedEvent(BaseModel):
    activityID: str


class GeomagneticStorm(BaseModel):
    allKpIndex: List[GSKpIndex]
    gstID: str
    link: str
    linkedEvents: List[GSLinkedEvent]
    startTime: str
    submissionTime: str
    versionId: int
