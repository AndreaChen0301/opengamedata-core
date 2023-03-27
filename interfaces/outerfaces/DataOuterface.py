## import standard libraries
import abc
import logging
from typing import Any, Dict, List

# import local files
from interfaces.Interface import Interface
from schemas.IDMode import IDMode
from schemas.ExportMode import ExportMode
from utils import Logger, ExportRow

class DataOuterface(Interface):

    # *** ABSTRACTS ***

    @abc.abstractmethod
    def _destination(self, mode:ExportMode) -> str:
        pass

    @abc.abstractmethod
    def _removeExportMode(self, mode:ExportMode) -> str:
        pass

    @abc.abstractmethod
    def _writeEventsHeader(self, header:List[str]) -> None:
        pass

    @abc.abstractmethod
    def _writeSessionHeader(self, header:List[str]) -> None:
        pass

    @abc.abstractmethod
    def _writePlayerHeader(self, header:List[str]) -> None:
        pass

    @abc.abstractmethod
    def _writePopulationHeader(self, header:List[str]) -> None:
        pass

    @abc.abstractmethod
    def _writeEventLines(self, events:List[ExportRow]) -> None:
        pass

    @abc.abstractmethod
    def _writeSessionLines(self, sessions:List[ExportRow]) -> None:
        pass

    @abc.abstractmethod
    def _writePlayerLines(self, players:List[ExportRow]) -> None:
        pass

    @abc.abstractmethod
    def _writePopulationLines(self, populations:List[ExportRow]) -> None:
        pass

    # *** BUILT-INS ***

    def __init__(self, game_id, config:Dict[str, Any]):
        super().__init__(config=config)
        self._game_id : str  = game_id

    def __del__(self):
        self.Close()

    # *** PUBLIC STATICS ***

    # *** PUBLIC METHODS ***

    def Destination(self, mode:ExportMode):
        return self._destination(mode=mode)

    def RemoveExportMode(self, mode:ExportMode):
        self._removeExportMode(mode)
        Logger.Log(f"Removed mode {mode} from {type(self).__name__} output.", logging.INFO)

    def WriteEventHeader(self, header:List[str]) -> None:
        self._writeEventsHeader(header=header)

    def WriteSessionHeader(self, header:List[str]) -> None:
        self._writeSessionHeader(header=header)

    def WritePlayerHeader(self, header:List[str]) -> None:
        self._writePlayerHeader(header=header)

    def WritePopulationHeader(self, header:List[str]) -> None:
        self._writePopulationHeader(header=header)

    def WriteEventLines(self, events:List[ExportRow]) -> None:
        self._writeEventLines(events=events)
        Logger.Log(f"Wrote {len(events)} events to {self.Destination(mode=ExportMode.EVENTS)}", logging.INFO, depth=2)

    def WriteSessionLines(self, sessions:List[ExportRow]) -> None:
        self._writeSessionLines(sessions=sessions)
        Logger.Log(f"Wrote {len(sessions)} sessions to {self.Destination(mode=ExportMode.SESSION)}", logging.INFO, depth=2)

    def WritePlayerLines(self, players:List[ExportRow]) -> None:
        self._writePlayerLines(players=players)
        Logger.Log(f"Wrote {len(players)} players to {self.Destination(mode=ExportMode.PLAYER)}", logging.INFO, depth=2)

    def WritePopulationLines(self, populations:List[ExportRow]) -> None:
        self._writePopulationLines(populations=populations)
        Logger.Log(f"Wrote {len(populations)} populations to {self.Destination(mode=ExportMode.POPULATION)}", logging.INFO, depth=2)

    # *** PROPERTIES ***

    # *** PRIVATE STATICS ***

    # *** PRIVATE METHODS ***
