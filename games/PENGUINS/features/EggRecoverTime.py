# import libraries
import logging
from typing import Any, Dict, List, Optional
# import locals
from utils.Logger import Logger
from datetime import datetime, timedelta
from extractors.Extractor import ExtractorParameters
from extractors.features.Feature import Feature
from games.PENGUINS.features.PerRegionFeature import PerRegionFeature
from schemas.Event import Event
from schemas.ExtractionMode import ExtractionMode
from schemas.FeatureData import FeatureData
from extractors.features.SessionFeature import SessionFeature

class EggRecoverTime(SessionFeature):

    def __init__(self, params:ExtractorParameters):
        super().__init__(params=params)
        self._session_id = None
        self._argument_start_time : Optional[datetime] = None
        self._prev_timestamp = None
        self._time = 0
        self._skua_id = None

    # *** IMPLEMENT ABSTRACT FUNCTIONS ***
    @classmethod
    def _getEventDependencies(cls, mode:ExtractionMode) -> List[str]:
        return ["egg_lost", "egg_recovered"]

    @classmethod
    def _getFeatureDependencies(cls, mode:ExtractionMode) -> List[str]:
        return []

    def _extractFromEvent(self, event:Event) -> None:
        Logger.Log(f"triggered")
        if event.SessionID != self._session_id:
            self._session_id = event.SessionID
            # if we jumped to a new session, we only want to count time up to last event, not the time between sessions.
            if self._argument_start_time and self._prev_timestamp:
                self._time += (self._prev_timestamp - self._argument_start_time).total_seconds()
                self._argument_start_time = event.Timestamp

        if event.EventName == "egg_lost":
            self._skua_id = event.event_data.get("object_id")
            self._argument_start_time = event.Timestamp
            Logger.Log(f"lost time is {self._argument_start_time}")
        elif event.EventName == "egg_recovered" and self._argument_start_time is not None:
            self._time = (event.Timestamp - self._argument_start_time).total_seconds()
            self._argument_start_time = None
            return
        self._prev_timestamp = event.Timestamp
    
    def _extractFromFeatureData(self, feature:FeatureData):
        return

    def _getFeatureValues(self) -> List[Any]:
        return [timedelta(seconds=self._time)]

    