# import libraries
import logging
from datetime import timedelta
from typing import Any, List, Optional

# import locals
from utils import Logger
from games.AQUALAB.features.PerJobFeature import PerJobFeature
from schemas.FeatureData import FeatureData
from schemas.Event import Event

class JobExperimentationTime(PerJobFeature):

    def __init__(self, name:str, description:str, job_num:int, job_map:dict):
        super().__init__(name=name, description=description, job_num=job_num, job_map=job_map)
        self._session_id = None
        self._experiment_start_time = None
        self._prev_timestamp = None
        self._time = 0

    # *** IMPLEMENT ABSTRACT FUNCTIONS ***
    def _getEventDependencies(self) -> List[str]:
        return ["begin_experiment", "room_changed"]

    def _getFeatureDependencies(self) -> List[str]:
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

    def _extractFromFeatureData(self, feature: FeatureData):
        return

    def _getFeatureValues(self) -> List[Any]:
        return [timedelta(seconds=self._time)]

    # *** Optionally override public functions. ***
    def MinVersion(self) -> Optional[str]:
        return "1"
