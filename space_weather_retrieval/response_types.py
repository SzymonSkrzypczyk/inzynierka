from typing import Optional, Dict, Any
from dataclasses import dataclass, field
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
            setattr(self, key, kwargs.pop(key))