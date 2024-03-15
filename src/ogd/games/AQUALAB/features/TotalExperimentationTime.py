# import libraries
from datetime import timedelta
from typing import Any, List
# import locals
from ogd.core.extractors.Extractor import ExtractorParameters
from ogd.core.extractors.features.Feature import Feature
from ogd.core.schemas.Event import Event
from ogd.core.schemas.ExtractionMode import ExtractionMode
from ogd.core.schemas.FeatureData import FeatureData

class TotalExperimentationTime(Feature):

    def __init__(self, params:ExtractorParameters):
        super().__init__(params=params)
        self._session_id = None
        self._experiment_start_time = None
        self._prev_timestamp = None
        self._time = 0

    # *** IMPLEMENT ABSTRACT FUNCTIONS ***
    @classmethod
    def _getEventDependencies(cls, mode:ExtractionMode) -> List[str]:
        return ["begin_experiment", "room_changed"]

    @classmethod
    def _getFeatureDependencies(cls, mode:ExtractionMode) -> List[str]:
        return []

    def _extractFromEvent(self, event:Event) -> None:
        if event.SessionID != self._session_id:
            self._session_id = event.SessionID

            if self._experiment_start_time:
                self._time += (self._prev_timestamp - self._experiment_start_time).total_seconds()
                self._experiment_start_time = event.Timestamp

        if event.EventName == "begin_experiment":
            self._experiment_start_time = event.Timestamp
        elif event.EventName == "room_changed":
            if self._experiment_start_time is not None:
                self._time += (event.Timestamp - self._experiment_start_time).total_seconds()
                self._experiment_start_time = None

        self._prev_timestamp = event.Timestamp

    def _extractFromFeatureData(self, feature:FeatureData):
        return

    def _getFeatureValues(self) -> List[Any]:
        return [timedelta(seconds=self._time)]

    # *** Optionally override public functions. ***