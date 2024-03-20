from typing import Any, List
from ogd.core.extractors.Extractor import ExtractorParameters
from ogd.core.extractors.features.SessionFeature import SessionFeature
from ogd.core.schemas.Event import Event
from ogd.core.schemas.ExtractionMode import ExtractionMode
from ogd.core.schemas.FeatureData import FeatureData

class TaskCompleteCount(SessionFeature):

    def __init__(self, params: ExtractorParameters, player_id: str):
        self.task_complete_count = 0
        super().__init__(params=params)

    @classmethod
    def _getEventDependencies(cls, mode: ExtractionMode) -> List[str]:
        return ["click_new_game", "click_reset_sim"]

    @classmethod
    def _getFeatureDependencies(cls, mode: ExtractionMode) -> List[str]:
        return []

    def _extractFromEvent(self, event: Event) -> None:
        if event.EventType in ["click_new_game", "click_reset_sim"]:
            if event.EventData.get("current_task"):
                is_complete = event.EventData["current_task"].get("is_complete")
                if is_complete:
                    self.task_complete_count += 1

    def _extractFromFeatureData(self, feature: FeatureData):
        return

    def _getFeatureValues(self) -> List[Any]:
        return [self.task_complete_count]
