from schemas import Event
from typing import Any, List, Union
# local imports
from features.Feature import Feature
from features.FeatureData import FeatureData
from schemas.Event import Event

class PercentWavelengthMoves(Feature):
    def __init__(self, name:str, description:str, count_index:int):
        Feature.__init__(self, name=name, description=description, count_index=count_index)
        self._wavelength_count = 0
        self._count = 0

    def GetEventDependencies(self) -> List[str]:
        return ["CUSTOM.1", "CUSTOM.2"]
        # return ["SLIDER_MOVE_RELEASE", "ARROW_MOVE_RELEASE"]

    def GetFeatureDependencies(self) -> List[str]:
        return []

    def GetFeatureValues(self) -> List[Any]:
        return [self._wavelength_count / self._count if self._count != 0 else None]

    def _extractFromEvent(self, event:Event) -> None:
        self._count += 1
        if event.event_data['slider'].upper() == 'WAVELENGTH':
            self._wavelength_count += 1

    def _extractFromFeatureData(self, feature: FeatureData):
        return

    def MinVersion(self) -> Union[str,None]:
        return None

    def MaxVersion(self) -> Union[str,None]:
        return None
