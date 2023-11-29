# import standard libraries
from datetime import datetime
from typing import Any, List, Optional
# import local files
from ogd.core.extractors.detectors.Detector import Detector
from ogd.core.extractors.Extractor import ExtractorParameters
from ogd.core.schemas.Event import EventSource
from ogd.core.schemas.Event import Event
from ogd.core.schemas.ExtractionMode import ExtractionMode

class LegacyDetector(Detector):
    """Dummy version of a detector, so that LegacyLoader can return something that's not None.
    """

    # *** IMPLEMENT ABSTRACT FUNCTIONS ***

    @classmethod
    def _getEventDependencies(cls, mode:ExtractionMode) -> List[str]:
        """_summary_

        :return: _description_
        :rtype: List[str]
        """
        return [] # >>> fill in names of events this Feature should use for extraction. <<<

    def _extractFromEvent(self, event:Event) -> None:
        """_summary_

        :param event: _description_
        :type event: Event
        """
        return

    def _trigger_condition(self) -> bool:
        return False

    def _trigger_event(self) -> Optional[Event]:
        """_summary_

        :return: _description_
        :rtype: List[Any]
        """
        ret_val : Event = Event(session_id="Not Implemented", app_id="Not Implemented", timestamp=datetime.now(),
                                event_name="CustomDetector", event_data={}, event_source=EventSource.GENERATED)
        return ret_val

    # *** BUILT-INS & PROPERTIES ***

    def __init__(self, params:ExtractorParameters):
        super().__init__(params=params, trigger_callback=lambda x : None)