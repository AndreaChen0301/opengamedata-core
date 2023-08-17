# import standard libraries
import logging
import traceback
from typing import List, Dict, Type, Optional, Set
# import local files
from schemas.FeatureData import FeatureData
from extractors.ExtractorLoader import ExtractorLoader
from extractors.registries.FeatureRegistry import FeatureRegistry
from processors.FeatureProcessor import FeatureProcessor
from schemas.Event import Event
from schemas.ExportMode import ExportMode
from schemas.ExtractionMode import ExtractionMode
from schemas.games.GameSchema import GameSchema
from utils.Logger import Logger, ExportRow

## @class SessionProcessor
#  Class to extract and manage features for a processed csv file.
class SessionProcessor(FeatureProcessor):

    # *** BUILT-INS & PROPERTIES ***

    ## Constructor for the SessionProcessor class.
    def __init__(self, LoaderClass:Type[ExtractorLoader], game_schema: GameSchema, player_id:str, session_id:str,
                 feature_overrides:Optional[List[str]]=None):
        """Constructor for the SessionProcessor class.
        Simply stores some data for use later, including the type of extractor to
        use.

        :param LoaderClass: The type of data extractor to use for input data.
                            This should correspond to whatever game_id is in the TableSchema.
        :type LoaderClass: Type[ExtractorLoader]
        :param game_schema: A dictionary that defines how the game data itself is structured.
        :type game_schema: GameSchema
        :param player_id: _description_
        :type player_id: str
        :param session_id: _description_
        :type session_id: str
        :param feature_overrides: _description_, defaults to None
        :type feature_overrides: Optional[List[str]], optional
        :param session_file: _description_, defaults to None
        :type session_file: Union[IO[str],None], optional
        """
        ## Define instance vars
        self._session_id   : str = session_id
        self._player_id    : str = player_id
        # NOTE: need session and player IDs set before we do initialization in parent.
        super().__init__(LoaderClass=LoaderClass, game_schema=game_schema, feature_overrides=feature_overrides)

    def __str__(self):
        return f"SessionProcessor({self._player_id}, {self._session_id})"

    def __repr__(self):
        return str(self)

    # *** IMPLEMENT ABSTRACT FUNCTIONS ***

    @property
    def _mode(self) -> ExtractionMode:
        return ExtractionMode.SESSION

    @property
    def _playerID(self) -> str:
        return self._player_id

    @property
    def _sessionID(self) -> str:
        return self._session_id

    def _getExtractorNames(self) -> List[str]:
        return ["PlayerID", "SessionID"] + self._registry.GetExtractorNames()

    ## Function to handle processing of a single row of data.
    def _processEvent(self, event: Event):
        """Function to handle processing of a single row of data.
        Basically just responsible for ensuring an extractor for the session corresponding
        to the row already exists, then delegating the processing to that extractor.

        :param event: Object with the data for the game event data to be processed.
        :type event: Event
        """
        self._registry.ExtractFromEvent(event)

    def _getLines(self) -> List[ExportRow]:
        ret_val : ExportRow
        # if as_str:
        #     ret_val = [self._playerID, self._sessionID] + self._registry.GetFeatureStringValues()
        # else:
        ret_val = [self._playerID, self._sessionID] + self._registry.GetFeatureValues()
        return [ret_val]

    def _getFeatureData(self, order:int) -> List[FeatureData]:
        return self._registry.GetFeatureData(order=order, player_id=self._player_id, sess_id=self._session_id)

    def _clearLines(self) -> None:
        Logger.Log(f"Clearing features from SessionProcessor for player {self._player_id}, session {self._session_id}.", logging.DEBUG, depth=2)
        self._registry = FeatureRegistry(mode=self._mode)

    # *** PUBLIC STATICS ***

    # *** PUBLIC METHODS ***

    # *** PRIVATE STATICS ***

    # *** PRIVATE METHODS ***
