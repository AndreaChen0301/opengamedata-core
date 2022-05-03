# import libraries
from datetime import timedelta
from typing import Any, List
# import locals
from features.Feature import Feature
from schemas.FeatureData import FeatureData
from schemas.Event import Event

class TotalDiveTime(Feature):
    
    def __init__(self, name:str, description:str):
        super().__init__(name=name, description=description, count_index=0)
        self._session_id = None
        self._dive_start_time = None
        self._time = 0
        self._times = []

    # *** IMPLEMENT ABSTRACT FUNCTIONS ***
    def _getEventDependencies(self) -> List[str]:
        return ["begin_dive", "scene_changed"]

    def _getFeatureDependencies(self) -> List[str]:
        return []

    def _extractFromEvent(self, event:Event) -> None:
        if event.session_id != self._session_id:
            self._session_id = event.session_id
            self._times.append(self._time)
            self._time = 0

        if event.event_name == "begin_dive":
            self._dive_start_time = event.timestamp
        elif event.event_name == "scene_changed":
            if self._dive_start_time is not None:
                self._time += (event.timestamp - self._dive_start_time).total_seconds()
                self._dive_start_time = None

    def _extractFromFeatureData(self, feature: FeatureData):
        return

    def _getFeatureValues(self) -> List[Any]:
        if self._time != 0:
            self._times.append(self._time)

        if len(self._times) > 0:
            return [timedelta(seconds=sum(self._times))]
        else:
            return [0]

    # *** Optionally override public functions. ***
