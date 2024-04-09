from typing import Any, List

from ogd.core.generators.Generator import GeneratorParameters
from ogd.core.generators.extractors.SessionFeature import SessionFeature
from ogd.core.schemas.Event import Event
from ogd.core.schemas.ExtractionMode import ExtractionMode
from ogd.core.schemas.FeatureData import FeatureData

class AppVersions(SessionFeature):
    """_summary_

    :param SessionFeature: _description_
    :type SessionFeature: _type_
    """
    def __init__(self, params:GeneratorParameters):
        super().__init__(params=params)
        self._versions = set()

    # *** IMPLEMENT ABSTRACT FUNCTIONS ***
    @classmethod
    def _eventFilter(cls, mode:ExtractionMode) -> List[str]:
        return ["all_events"]

    @classmethod
    def _featureFilter(cls, mode:ExtractionMode) -> List[str]:
        return []

    def _extractFromEvent(self, event:Event) -> None:
        self._versions.add(event.AppVersion)

    def _extractFromFeatureData(self, feature:FeatureData):
        return

    def _getFeatureValues(self) -> List[Any]:
        return [list(self._versions)]

    # *** Optionally override public functions. ***