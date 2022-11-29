# import libraries
import json
import logging
from typing import Any, Dict, List, Optional
from extractors.Extractor import ExtractorParameters
# import local files
from extractors.features.PerCountFeature import PerCountFeature
from schemas.ExtractionMode import ExtractionMode
from schemas.FeatureData import FeatureData
from schemas.Event import Event
from games.JOWILDER import Jowilder_Enumerators as je
from utils import Logger

try:
    with open(file="./games/JOWILDER/interaction_metadata.json") as f:
        METADATA_RAW : Dict[str, Dict[str, Any]] = json.load(f)
        METADATA     : Dict[int, Dict[str, Any]] = {je.fqid_to_enum.get(v.get("fqid", "FQID NOT FOUND"), -1): v for v in METADATA_RAW.values()}
except FileNotFoundError as err:
    Logger.Log(f"Could not find ./games/JOWILDER/interaction_metadata.json")
    METADATA_RAW = {}
    METADATA     = {}

class InteractionName(PerCountFeature):

    def __init__(self, params=ExtractorParameters):
        super().__init__(params=params)

    # *** IMPLEMENT ABSTRACT FUNCTIONS ***
    def _validateEventCountIndex(self, event: Event):
        return False

    @classmethod
    def _getEventDependencies(cls, mode:ExtractionMode) -> List[str]:
        return [] 

    @classmethod
    def _getFeatureDependencies(cls, mode:ExtractionMode) -> List[str]:
        return []

    def _extractFromEvent(self, event:Event) -> None:
        return

    def _extractFromFeatureData(self, feature: FeatureData):
        return

    def _getFeatureValues(self) -> List[Any]:
        """_summary_

        :return: _description_
        :rtype: List[Any]
        """
        cur_interaction : Optional[Dict[str, Any]] = METADATA.get(self.CountIndex)
        if cur_interaction is not None:
            ret_val : List[Any] = [cur_interaction.get("fqid"), cur_interaction.get("count_boxes"), cur_interaction.get("num_words")]
        else:
            raise ValueError(f"Could not find metadata for interaction #{self.CountIndex}")
        return ret_val

    # *** Optionally override public functions. ***
    def Subfeatures(self) -> List[str]:
        return ["BoxesCount", "WordsCount"] # >>> fill in names of Subfeatures for which this Feature should extract values. <<<
    