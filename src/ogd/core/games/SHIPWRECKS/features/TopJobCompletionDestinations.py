# import libraries
import json
from collections import defaultdict
from typing import Any, List
# import locals
from ogd.core.utils.Logger import Logger
from ogd.core.extractors.features.Feature import Feature
from ogd.core.extractors.Extractor import ExtractorParameters
from ogd.core.schemas.Event import Event
from ogd.core.schemas.ExtractionMode import ExtractionMode
from ogd.core.schemas.FeatureData import FeatureData


class TopJobCompletionDestinations(Feature):

    def __init__(self, params:ExtractorParameters):
        super().__init__(params=params)
        self._current_session_id = None
        self._current_mission_id = None
        self._last_completed_id = None
        self._mission_complete_pairs = {}

    # *** IMPLEMENT ABSTRACT FUNCTIONS ***
    @classmethod
    def _getEventDependencies(cls, mode:ExtractionMode) -> List[str]:
        return ["checkpoint"]

    @classmethod
    def _getFeatureDependencies(cls, mode:ExtractionMode) -> List[str]:
        return []

    def _extractFromEvent(self, event:Event) -> None:
        session_id = event.SessionID
        checkpoint = event.EventData["status"]
        mission_id = event.EventData["mission_id"]

        if session_id != self._current_session_id:
            self._last_completed_id = None
        elif checkpoint == "Case Closed" and mission_id != self._last_completed_id:
            if mission_id == "Level1":
                if "Level1" not in self._mission_complete_pairs.keys():
                    self._mission_complete_pairs["Level1"] = {"Level2": []}

                self._mission_complete_pairs["Level1"]["Level2"].append(session_id)
            elif mission_id == "Level2":
                if "Level2" not in self._mission_complete_pairs.keys():
                    self._mission_complete_pairs["Level2"] = {"Level3": []}

                self._mission_complete_pairs["Level2"]["Level3"].append(session_id)
            elif mission_id == "Level3":
                if "Level3" not in self._mission_complete_pairs.keys():
                    self._mission_complete_pairs["Level3"] = {"Level4": []}

                self._mission_complete_pairs["Level3"]["Level4"].append(session_id)

                self._last_completed_id = mission_id

        self._current_session_id = session_id

    def _extractFromFeatureData(self, feature:FeatureData):
        return

    def _getFeatureValues(self) -> List[Any]:
        ret_val = {}

        for src in self._mission_complete_pairs.keys():
            dests = sorted(
                self._mission_complete_pairs[src].items(),
                key=lambda item: len(item[1]), # sort by length of list of ids.
                reverse=True # sort largest to smallest
            )
            ret_val[src] = {
                item[0]:item[1] for item in dests[0:5]
            }
            Logger.Log(f"For TopJobCompletionDestinations, sorted dests as: {json.dumps(dests)}")

        return [json.dumps(ret_val)]

    # *** Optionally override public functions. ***
