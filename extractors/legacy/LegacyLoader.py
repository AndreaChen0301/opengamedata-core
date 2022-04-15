# import libraries
from typing import Any, Dict, List, Union
# import locals
from detectors.Detector import Detector
from extractors.legacy.LegacyDetector import LegacyDetector
from features.Feature import Feature
from features.FeatureLoader import FeatureLoader
from features.FeatureRegistry import FeatureRegistry
from schemas.GameSchema import GameSchema

class LegacyLoader(FeatureLoader):
    def __init__(self, player_id:str, session_id:str, game_schema:GameSchema, feature_overrides:Union[List[str],None]):
        super().__init__(player_id=player_id, session_id=session_id, game_schema=game_schema, feature_overrides=feature_overrides)

    def LoadToRegistry(self, registry:FeatureRegistry) -> None:
        feat = self.LoadFeature(feature_type="", name="", feature_args={}, count_index=0)
        # treat the monolithic LegacyFeature extractor as a single aggregate.
        registry.Register(feat, FeatureRegistry.Listener.Kinds.AGGREGATE)

    def LoadDetector(self, detector_type:str, name:str, feature_args:Dict[str,Any], count_index:Union[int,None] = None) -> Detector:
        return LegacyDetector(name=name, description=feature_args["description"])