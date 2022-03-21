from typing import Any, List, Union

from features.FeatureData import FeatureData
from features.SessionFeature import SessionFeature
from schemas.Event import Event

class TotalDiveTime(SessionFeature):

    def __init__(self, name:str, description:str):
        super().__init__(name=name, description=description)

    def GetEventDependencies(self) -> List[str]:
        return ["dive_start", "dive_exit"]

    def GetFeatureDependencies(self) -> List[str]:
        return []

    def GetFeatureValues(self) -> List[Any]:
        return [self._time]

    def MinVersion(self) -> Union[str,None]:
        return "1"

    def _extractFromEvent(self, event:Event) -> None:
        if event.event_name == "dive_start":
            self._dive_start_time = event.timestamp
        elif event.event_name == "dive_exit":
            if self._dive_start_time is not None:
                self._time += (event.timestamp - self._dive_start_time).total_seconds()
                self._dive_start_time = None

    def _extractFromFeatureData(self, feature: FeatureData):
        return
