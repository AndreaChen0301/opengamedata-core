## import standard libraries
import logging
import numpy as np
import typing
import traceback
from datetime import datetime
from sklearn.linear_model import LinearRegression
from typing import Any, Dict, List, Union
## import local files
from games.AQUALAB.extractors import *
import utils
from extractors.Extractor import Extractor
from extractors.Feature import Feature
from schemas.GameSchema import GameSchema

## @class WaveExtractor
#  Extractor subclass for extracting features from Waves game data.
class AqualabExtractor(Extractor):
    ## Constructor for the WaveExtractor class.
    #  Initializes some custom private data (not present in base class) for use
    #  when calculating some features.
    #  Sets the sessionID feature.
    #  Further, initializes all Q&A features to -1, representing unanswered questions.
    #
    #  @param session_id The id number for the session whose data is being processed
    #                    by this extractor instance.
    #  @param game_table A data structure containing information on how the db
    #                    table assiciated with this game is structured. 
    #  @param game_schema A dictionary that defines how the game data itself is
    #                     structured.
    def __init__(self, session_id: str, game_schema: GameSchema):
        super().__init__(session_id=session_id, game_schema=game_schema)
        # self._last_adjust_type : Union[str,None] = None
        # self.start_times: Dict       = {}
        # self.end_times:   Dict       = {}
        # self.amp_move_counts:  Dict   = {}
        # self.off_move_counts:  Dict   = {}
        # self.wave_move_counts: Dict   = {}
        # self.saw_first_move: Dict[int, bool] = {}
        # self.latest_complete_lvl8 = None
        # self.latest_complete_lvl16 = None
        # self.latest_answer_Q0 = None
        # self.latest_answer_Q2 = None
        # self.active_begin = None
        # self.move_closenesses_tx: Dict = {}
        # self._features.setValByName(feature_name="sessionID", new_value=session_id)
        # # we specifically want to set the default value for questionAnswered to None, for unanswered.
        # for ans in self._features.getValByName(feature_name="questionAnswered").keys():
        #     self._features.setValByIndex(feature_name="questionAnswered", index=ans, new_value=None)
        # for q in self._features.getValByName(feature_name="questionCorrect"):
        #     self._features.setValByIndex(feature_name="questionCorrect", index=q, new_value=None)
        # for elem in self._features.getValByName(feature_name="firstMoveType"):
        #     self._features.setValByIndex(feature_name="firstMoveType", index=elem, new_value=None)
    
    def _loadFeature(self, feature:str, name:str, feature_args:Dict[str,Any], count_index:Union[int,None] = None) -> Feature:
        ret_val : Feature
        if feature == "JobArgumentationTime":
            if count_index is None:
                raise TypeError("Got None for count_index, should have a value!")
            ret_val = JobArgumentationTime.JobArgumentationTime(name=name, description=feature_args["description"], job_num=count_index)
        elif feature == "JobCompletionTime":
            if count_index is None:
                raise TypeError("Got None for count_index, should have a value!")
            ret_val = JobCompletionTime.JobCompletionTime(name, feature_args["description"], job_num=count_index)
        elif feature == "JobDiveSitesCount":
            ret_val = JobDiveSitesCount.JobDiveSitesCount(name=name, description=feature_args["description"], )
        else:
            raise NotImplementedError(f"'{feature}' is not a valid feature for Aqualab.")
        return ret_val
