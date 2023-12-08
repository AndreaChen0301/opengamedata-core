# import libraries
from datetime import datetime, timedelta
import logging, warnings
from typing import Any, List, Optional
# import locals
from utils.Logger import Logger
from extractors.Extractor import ExtractorParameters
from extractors.features.Feature import Feature
from schemas.Event import Event
from schemas.ExtractionMode import ExtractionMode
from schemas.FeatureData import FeatureData

class TotalPlayTime(Feature):
    def __init__(self, params:ExtractorParameters, ):
        super().__init__(params=params)
        self._play_time: timedelta = timedelta(0)
        self._idle_time: timedelta = timedelta(0)
        self._active_time: timedelta = timedelta(0)
    def Subfeatures(self) -> List[str]:
        return ["Active", "Idle"]
    
    # *** IMPLEMENT ABSTRACT FUNCTIONS ***
    @classmethod
    def _getEventDependencies(cls, mode:ExtractionMode) -> List[str]:
        return []

    @classmethod
    def _getFeatureDependencies(cls, mode:ExtractionMode) -> List[str]:
        return ["SessionDuration"]

    def _extractFromEvent(self, event:Event) -> None:
        pass

    def _extractFromFeatureData(self, feature:FeatureData):
        if feature.ExportMode == ExtractionMode.SESSION:
            try:
                self._play_time += feature.FeatureValues[0]
                self._active_time += feature.FeatureValues[1]
                self._idle_time += feature.FeatureValues[2]
            except TypeError as err:
                Logger.Log(f"TotalPlayTime for player {feature.PlayerID} got non-timedelta value of {feature.FeatureValues[0]}")
    
    def _getFeatureValues(self) -> List[Any]:
        return [self._play_time, self._active_time, self._idle_time]

    # *** Optionally override public functions. ***

    @staticmethod
    def MinVersion() -> Optional[str]:
        return "1"

    @staticmethod
    def AvailableModes() -> List[ExtractionMode]:
        return [ExtractionMode.PLAYER]
