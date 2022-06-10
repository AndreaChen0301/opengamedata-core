# import libraries
from schemas import Event
from typing import Any, List, Optional
# import locals
from extractors.features.Feature import Feature
from schemas.FeatureData import FeatureData
from schemas.Event import Event

class QuestionCorrect(Feature):
    def __init__(self, name:str, description:str, count_index:int):
        Feature.__init__(self, name=name, description=description, count_index=count_index)
        self._correct = None

    # *** IMPLEMENT ABSTRACT FUNCTIONS ***
    def _getEventDependencies(self) -> List[str]:
        return ["CUSTOM.3"]
        # return ["QUESTION_ANSWER"]

    def _getFeatureDependencies(self) -> List[str]:
        return []

    def _extractFromEvent(self, event:Event) -> None:
        if event.EventData['question'] == self.CountIndex:
            self._correct = (event.EventData['answered'] == event.EventData['answer'])

    def _extractFromFeatureData(self, feature: FeatureData):
        return

    def _getFeatureValues(self) -> List[Any]:
        return [self._correct]

    # *** Optionally override public functions. ***
