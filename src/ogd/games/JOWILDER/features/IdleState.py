# import libraries
import json
from time import time
from typing import Any, List, Optional
from datetime  import timedelta, datetime
# import local files
from ogd.core.generators.Extractor import ExtractorParameters
from ogd.core.generators.extractors.SessionFeature import SessionFeature
from ogd.core.schemas.ExtractionMode import ExtractionMode
from ogd.core.schemas.FeatureData import FeatureData
from ogd.core.schemas.Event import Event

class IdleState(SessionFeature):
    """Template file to serve as a guide for creating custom Feature subclasses for games.

    :param Feature: Base class for a Custom Feature class.
    :type Feature: _type_
    """

    IDLE_TIME_THRESHOLD = timedelta(seconds=15)

    def __init__(self, params:ExtractorParameters, threshold:int):
        super().__init__(params=params)
        self._time : timedelta = timedelta(0)
        self._count : int = 0
        self._last_timestamp : Optional[datetime] = None
        self._threshold : timedelta = timedelta(seconds=threshold)

    @staticmethod
    def defaultThreshold():
        return IdleState.IDLE_TIME_THRESHOLD

    # *** IMPLEMENT ABSTRACT FUNCTIONS ***
    @classmethod
    def _getEventDependencies(cls, mode:ExtractionMode) -> List[str]:
        return [f"CUSTOM.{i}" for i in range(3, 21)] + ["CUSTOM.1"]

    @classmethod
    def _getFeatureDependencies(cls, mode:ExtractionMode) -> List[str]:
        return []

    def _extractFromEvent(self, event:Event) -> None:
        if event.EventName == "CUSTOM.1" and not self._last_timestamp:
            self._last_timestamp = event.Timestamp
            return
        if self._last_timestamp is not None:
            time_since_last = event.Timestamp - self._last_timestamp
            if time_since_last > IdleState.IDLE_TIME_THRESHOLD:
                self._time += time_since_last
                self._count += 1
        else:
            raise ValueError("In IdleState, last timestamp is None!")
        self._last_timestamp = event.Timestamp
        return

    def _extractFromFeatureData(self, feature: FeatureData):
        return

    def _getFeatureValues(self) -> List[Any]:
        return [self._time, self._count]

    # *** Optionally override public functions. ***
    def Subfeatures(self) -> List[str]:
        return ["Count"] # >>> fill in names of Subfeatures for which this Feature should extract values. <<<
    
    def BaseFeatureSuffix(self) -> str:
        return "Time"
