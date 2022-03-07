from schemas import Event
import typing
from typing import Any, List, Union
# local imports
from features.FeatureData import FeatureData
from features.PerLevelFeature import PerLevelFeature
from schemas.Event import Event

class SliderAverageRange(PerLevelFeature):
    def __init__(self, name:str, description:str, count_index:int):
        PerLevelFeature.__init__(self, name=name, description=description, count_index=count_index)
        self._ranges = []

    def GetEventDependencies(self) -> List[str]:
        return ["CUSTOM.1"]
        # return ["SLIDER_MOVE_RELEASE"]

    def GetFeatureDependencies(self) -> List[str]:
        return []

    def GetFeatureValues(self) -> List[Any]:
        if len(self._ranges) > 0:
            return [sum(self._ranges) / len(self._ranges)]
        else:
            return [None]

    def _extractFromEvent(self, event:Event) -> None:
        self._ranges.append(event.event_data["max_val"] - event.event_data["min_val"])

    def _extractFromFeatureData(self, feature: FeatureData):
        return

    def MinVersion(self) -> Union[str,None]:
        return None

    def MaxVersion(self) -> Union[str,None]:
        return None
