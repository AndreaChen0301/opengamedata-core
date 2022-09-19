# import libraries
from typing import Any, List
import json
import pandas as pd
# import locals
from extractors.Extractor import ExtractorParameters
from extractors.features.SessionFeature import SessionFeature
from schemas.Event import Event
from schemas.FeatureData import FeatureData

class FunnelByUser(SessionFeature):
    def __init__(self, params:ExtractorParameters):
        super().__init__(params=params)
        self._count = 0
        self._level = None
        self._userFunnelDict = dict()

    # *** IMPLEMENT ABSTRACT FUNCTIONS ***
    @classmethod
    _getEventDependencies(cls, mode:ExtractionMode) -> List[str]:
        return ["start_level", "puzzle_started", "create_shape", "check_solution", "puzzle_complete"]

    @classmethod
    _getEventDependencies(cls, mode:ExtractionMode) -> List[str]:
        return []

    def _extractFromEvent(self, event:Event) -> None:
        if event.EventName in ["start_level", "puzzle_started"]:
            self._level = event.EventData["task_id"]["string_value"]

            if self._level not in self._userFunnelDict.keys():
                self._userFunnelDict[self._level] = json.loads('{"started": 0, "create_shape": 0, "submitted": 0, "completed": 0}')

        if event.EventName == "puzzle_started":
            self._userFunnelDict[self._level]["started"] = 1

        elif event.EventName == "create_shape":
            self._userFunnelDict[self._level]["create_shape"] = 1

        elif event.EventName == "check_solution":
            self._userFunnelDict[self._level]["submitted"] = 1

        elif event.EventName == "puzzle_complete":
            self._userFunnelDict[self._level]["completed"] = 1

    def _extractFromFeatureData(self, feature:FeatureData):
        return

    def _getFeatureValues(self) -> List[Any]:
        count = 0
        finalList = []
        listReturn = []
        finalDict = json.loads('{"started": 0, "create_shape": 0, "submitted": 0, "completed": 0}')
        for key in self._userFunnelDict.keys():
            finalList.append((self._userFunnelDict[key]["started"], self._userFunnelDict[key]["create_shape"], self._userFunnelDict[key]["submitted"], self._userFunnelDict[key]["completed"]))
        percent = round((sum([x[3] for x in finalList]) / 30) * 100, 2)
        listReturn.append(percent)
        listReturn.append(sum([x[0] for x in finalList]))
        listReturn.append(sum([x[1] for x in finalList]))
        listReturn.append(sum([x[2] for x in finalList]))
        listReturn.append(sum([x[3] for x in finalList]))
        return listReturn
        
    # *** Optionally override public functions. ***
    def Subfeatures(self) -> List[str]:
        return ["started", "create_shape", "submitted", "completed"]
