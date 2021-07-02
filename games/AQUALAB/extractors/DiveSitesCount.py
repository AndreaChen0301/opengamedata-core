from typing import Any, List

from extractors.Feature import Feature
from schemas.Event import Event

class DiveSitesCount(Feature):
    
    def __init__(self, name:str, description:str, sessionID:str):
        min_data_version = None
        max_data_version = None
        super().__init__(name, description, min_data_version, max_data_version)
        self._sessionID = sessionID
        self._count = 0
        self._visited_sites = []

    def GetEventTypes(self) -> List[str]:
        return []

    def CalculateFinalValues(self) -> Any:
        return self._count

    def _extractFromEvent(self, event:Event) -> None:
        if event.event_name == "begin_dive" and event.event_data["site_id"] not in self._visited_sites:
            self._count += 1
            self._visited_sites.append(event.event_data["site_id"])