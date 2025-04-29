from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field, fields, is_dataclass
# data classes with returned content


@dataclass
class SolarFlare:
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
    extra_fields: Dict[str, Any] = field(default_factory=dict, repr=False)

    def __init__(self, **kwargs):
        known_fields = {
            'beginTime', 'catalog', 'endTime', 'flrID', 'link', 'note',
            'peakTime', 'sourceLocation', 'submissionTime', 'versionId', 'activeRegionNum'
        }

        for key in known_fields:
            setattr(self, key, kwargs.pop(key, None))
        self.extra_fields = kwargs


    def serialize(self):
        """
        Serialize the object to a dictionary
        :return: dict
        """
        serialized_data = {field.name: getattr(self, field.name) for field in fields(self)}
        return serialized_data


@dataclass
class CMEAnalyses:
    featureCode: str
    halfAngle: float
    imageType: str
    isMostAccurate: bool
    latitude: float
    levelOfData: int
    link: str
    longitude: float
    measurementTechnique: str
    speed: float
    submissionTime: str
    time21_5: str
    type: str
    tilt: Optional[float] = None
    speedMeasuredAtHeight: Optional[float] = None
    enlilList: Optional[str] = None
    minorHalfWidth: Optional[float] = None
    note: Optional[str] = None

    def serialize(self):
        """
        Serialize the object to a dictionary
        :return: dict
        """
        serialized_data = {field.name: getattr(self, field.name) for field in fields(self)}
        return serialized_data


@dataclass
class CMEInstrument:
    displayName: str

@dataclass
class CoronalMassEjection:
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
    linkedEvents: Optional[List[str]] = None
    extra_fields: Dict[str, Any] = field(default_factory=dict, repr=False)

    def __init__(self, **kwargs):
        known_fields = {
            'cmeAnalyses', 'instruments', 'link', 'activityID', 'catalog',
            'note', 'sourceLocation', 'startTime', 'submissionTime', 'versionId',
            'activeRegionNum', 'linkedEvents'
        }

        for key in known_fields:
            setattr(self, key, kwargs.pop(key, None))

        self.extra_fields = kwargs

    def serialize(self) -> Dict[str, Any]:
        """
        Flatten nested dataclass fields for CSV output
        """
        result = {}
        for f in fields(self):
            value = getattr(self, f.name)
            if isinstance(value, list):
                for i, item in enumerate(value):
                    if is_dataclass(item):
                        nested = {f"{f.name}_{i}_{k}": v for k, v in item.__dict__.items()}
                        result.update(nested)
                    else:
                        result[f"{f.name}_{i}"] = item
            elif is_dataclass(value):
                nested = {f"{f.name}_{k}": v for k, v in value.__dict__.items()}
                result.update(nested)
            else:
                result[f.name] = value
        return result


@dataclass
class CoronalMassEjectionAnalysis:
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

    def serialize(self) -> Dict[str, Any]:
        """
        Flatten nested dataclass fields for CSV output
        """
        result = {}
        for f in fields(self):
            value = getattr(self, f.name)
            if isinstance(value, list):
                for i, item in enumerate(value):
                    if is_dataclass(item):
                        nested = {f"{f.name}_{i}_{k}": v for k, v in item.__dict__.items()}
                        result.update(nested)
                    else:
                        result[f"{f.name}_{i}"] = item
            elif is_dataclass(value):
                nested = {f"{f.name}_{k}": v for k, v in value.__dict__.items()}
                result.update(nested)
            else:
                result[f.name] = value
        return result


@dataclass
class GSKpIndex:
    kpIndex: float
    observedTime: str
    source: str


@dataclass
class GSLinkedEvent:
    activityID: str


@dataclass
class GeomagneticStorm:
    allKpIndex: List[GSKpIndex]
    gstID: str
    link: str
    linkedEvents: List[GSLinkedEvent]
    startTime: str
    submissionTime: str
    versionId: int

    def serialize(self) -> Dict[str, Any]:
        """
        Flatten nested dataclass fields for CSV output
        """
        result = {}
        for f in fields(self):
            value = getattr(self, f.name)
            if isinstance(value, list):
                for i, item in enumerate(value):
                    if is_dataclass(item):
                        nested = {f"{f.name}_{i}_{k}": v for k, v in item.__dict__.items()}
                        result.update(nested)
                    else:
                        result[f"{f.name}_{i}"] = item
            elif is_dataclass(value):
                nested = {f"{f.name}_{k}": v for k, v in value.__dict__.items()}
                result.update(nested)
            else:
                result[f.name] = value
        return result
