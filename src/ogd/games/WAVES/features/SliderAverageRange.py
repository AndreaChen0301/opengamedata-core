# import libraries
from ogd.core.schemas import Event
import typing
from typing import Any, List, Optional
# import locals
from ogd.core.generators.extractors.PerLevelFeature import PerLevelFeature
from ogd.core.generators.Extractor import ExtractorParameters
from ogd.core.schemas.Event import Event
from ogd.core.schemas.ExtractionMode import ExtractionMode
from ogd.core.schemas.FeatureData import FeatureData

class SliderAverageRange(PerLevelFeature):
    def __init__(self, params:ExtractorParameters):
        PerLevelFeature.__init__(self, params=params)
        self._ranges = []

    # *** IMPLEMENT ABSTRACT FUNCTIONS ***
    @classmethod
    def _getEventDependencies(cls, mode:ExtractionMode) -> List[str]:
        return ["CUSTOM.1"]
        # return ["SLIDER_MOVE_RELEASE"]

    @classmethod
    def _getFeatureDependencies(cls, mode:ExtractionMode) -> List[str]:
        return []

    def _extractFromEvent(self, event:Event) -> None:
        self._ranges.append(event.EventData["max_val"] - event.EventData["min_val"])

    def _extractFromFeatureData(self, feature:FeatureData):
        return

    def _getFeatureValues(self) -> List[Any]:
        if len(self._ranges) > 0:
            return [sum(self._ranges) / len(self._ranges)]
        else:
            return [None]

    # *** Optionally override public functions. ***
