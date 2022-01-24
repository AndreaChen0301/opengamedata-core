## import standard libraries
import logging
from typing import Any, Dict, List, Type, Union
## import local files
import utils
from extractors.FeatureLoader import FeatureLoader
from extractors.PopulationExtractor import PopulationExtractor
from games.AQUALAB.AqualabLoader import AqualabLoader
from games.CRYSTAL.CrystalLoader import CrystalLoader
from games.JOWILDER.JowilderLoader import JowilderLoader
from games.LAKELAND.LakelandLoader import LakelandLoader
from games.MAGNET.MagnetLoader import MagnetLoader
from games.SHADOWSPECT.ShadowspectLoader import ShadowspectLoader
from games.WAVES.WaveLoader import WaveLoader
from managers.Request import ExporterTypes, Request
from schemas.GameSchema import GameSchema
from schemas.Event import Event

class ExtractorManager:
    def __init__(self, game_id:str, exp_types:ExporterTypes, game_schema:GameSchema, feature_overrides:Union[List[str],None]):
        # self._settings = settings
        self._exp_types     : ExporterTypes = exp_types
        self._LoaderClass   : Union[Type[FeatureLoader],None]  = None
        self._pop_processor : Union[PopulationExtractor, None] = None
        self._prepareExtractor(game_id=game_id)
        self._prepareProcessors(exp_types=exp_types, game_schema=game_schema, feature_overrides=feature_overrides)
        self._latest_results   : Dict[str,List[Any]] = {}
        self._up_to_date       : bool                = True

    def ProcessEvent(self, event:Event) -> None:
        if self._pop_processor is not None:
            self._pop_processor.ProcessEvent(event=event)
        self._up_to_date = False

    def HasExtractor(self) -> bool:
        return self._LoaderClass is not None

    def _try_update(self):
        if not self._up_to_date:
            if self._pop_processor is not None:
                self._latest_results = self._pop_processor.GetFeatureValues(export_types=self._exp_types)
            self._up_to_date = True

    def GetFeatureValues(self, export_types:ExporterTypes):
        self._try_update()
        return self._latest_results

    def GetPopulationFeatureNames(self) -> List[str]:
        return self._pop_processor.GetPopulationFeatureNames() if self._pop_processor is not None else []
    def GetPopulationFeatures(self) -> List[Any]:
        self._try_update()
        return self._latest_results['population']

    def GetPlayerFeatureNames(self) -> List[str]:
        return self._pop_processor.GetPlayerFeatureNames() if self._pop_processor is not None else []
    def GetPlayerFeatures(self) -> List[List[Any]]:
        self._try_update()
        return self._latest_results['players']

    def GetSessionFeatureNames(self) -> List[str]:
        return self._pop_processor.GetSessionFeatureNames() if self._pop_processor is not None else []
    def GetSessionFeatures(self) -> List[List[Any]]:
        self._try_update()
        return self._latest_results['sessions']

    def ClearPopulationLines(self) -> None:
        if self._pop_processor is not None:
            self._pop_processor.ClearLines()

    def ClearPlayerLines(self) -> None:
        if self._pop_processor is not None:
            self._pop_processor.ClearPlayersLines()

    def ClearSessionLines(self) -> None:
        if self._pop_processor is not None:
            self._pop_processor.ClearSessionsLines()

    def _prepareExtractor(self, game_id:str) -> None:
        game_extractor: Union[Type[FeatureLoader],None] = None
        if game_id == "AQUALAB":
            game_extractor = AqualabLoader
        elif game_id == "CRYSTAL":
            game_extractor = CrystalLoader
        elif game_id == "JOWILDER":
            game_extractor = JowilderLoader
        elif game_id == "LAKELAND":
            game_extractor = LakelandLoader
        elif game_id == "MAGNET":
            game_extractor = MagnetLoader
        elif game_id == "SHADOWSPECT":
            game_extractor = ShadowspectLoader
        elif game_id == "WAVES":
            game_extractor = WaveLoader
        elif game_id in ["BACTERIA", "BALLOON", "CYCLE_CARBON", "CYCLE_NITROGEN", "CYCLE_WATER", "EARTHQUAKE", "SHIPWRECKS", "STEMPORTS", "WIND"]:
            # all games with data but no extractor.
            pass
        else:
            raise Exception(f"Got an invalid game ID ({game_id})!")
        self._LoaderClass = game_extractor

    def _prepareProcessors(self, exp_types:ExporterTypes, game_schema:GameSchema, feature_overrides:Union[List[str],None]):
        if self._LoaderClass is None:
            utils.Logger.toStdOut("Could not export population/session data, no game extractor given!", logging.WARN)
        else:
            if exp_types.population:
                self._pop_processor = PopulationExtractor(LoaderClass=self._LoaderClass, game_schema=game_schema, feature_overrides=feature_overrides)
            else:
                utils.Logger.toStdOut("Population features not requested, skipping population_features file.", logging.INFO)
            if exp_types.players:
                # self._play_processor = PlayerExtractor(ExtractorClass=self._LoaderClass, game_schema=game_schema, feature_overrides=feature_overrides)
                pass
            else:
                utils.Logger.toStdOut("Session features not requested, skipping session_features file.", logging.INFO)
            if exp_types.sessions:
                # self._sess_processor = SessionExtractor(ExtractorClass=self._LoaderClass, game_schema=game_schema, feature_overrides=feature_overrides)
                pass
            else:
                utils.Logger.toStdOut("Session features not requested, skipping session_features file.", logging.INFO)