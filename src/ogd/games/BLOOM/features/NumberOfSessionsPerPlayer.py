# import libraries
from typing import Any, Dict, List, Optional
from ogd.core.generators.Generator import GeneratorParameters
from ogd.core.generators.extractors.Feature import Feature
from ogd.core.schemas.Event import Event
from ogd.core.schemas.ExtractionMode import ExtractionMode
from ogd.core.schemas.FeatureData import FeatureData

class NumberOfSessionsPerPlayer(Feature):
    def __init__(self, params: GeneratorParameters):
        super().__init__(params=params)
        self.session_count: Dict[str, int] = {}

    # *** IMPLEMENT ABSTRACT FUNCTIONS ***
    @classmethod
    def _eventFilter(cls, mode: ExtractionMode) -> List[str]:
        return ["session_start"]

    @classmethod
    def _featureFilter(cls, mode: ExtractionMode) -> List[str]:
        return []

    def _updateFromEvent(self, event: Event) -> None:
        player_id = event.user_id
        if player_id not in self.session_count:
            self.session_count[player_id] = 1
        else:
            self.session_count[player_id] += 1

    def _updateFromFeatureData(self, feature: FeatureData):
        return

    def _getFeatureValues(self) -> List[Any]:
        return [self.session_count]

    # *** Optionally override public functions. ***
    @staticmethod
    def MinVersion() -> Optional[str]:
        return "1"
