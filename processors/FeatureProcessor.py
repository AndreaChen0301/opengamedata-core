## import standard libraries
import abc
from ast import Load
import logging
from typing import Any, Dict, List, Type, Union
# import locals
from extractors.ExtractorRegistry import ExtractorRegistry
from features.FeatureLoader import FeatureLoader
from features.FeatureData import FeatureData
from processors.Processor import Processor
from schemas.GameSchema import GameSchema
from schemas.Event import Event
from schemas.Request import ExporterTypes

## @class Processor
class FeatureProcessor(Processor):

    # *** ABSTRACTS ***

    ## Abstract declaration of a function to get the calculated value of the feature, given data seen so far.
    @abc.abstractmethod
    def _getFeatureValues(self, export_types:ExporterTypes, as_str:bool=False) -> Dict[str,List[Any]]:
        pass

    @abc.abstractmethod
    def _getFeatureData(self, order:int) -> Dict[str,List[FeatureData]]:
        pass

    # *** PUBLIC BUILT-INS ***

    def __init__(self, LoaderClass:Type[FeatureLoader], game_schema: GameSchema,
                 feature_overrides:Union[List[str],None]=None):
        super().__init__(LoaderClass=LoaderClass, game_schema=game_schema, feature_overrides=feature_overrides)

    def __str__(self):
        return f""

    # *** PUBLIC STATICS ***

    # *** PUBLIC METHODS ***

    def GetFeatureValues(self, export_types:ExporterTypes, as_str:bool=False) -> Dict[str,List[Any]]:
        # TODO: add error handling code, if applicable.
        return self._getFeatureValues(export_types=export_types, as_str=as_str)

    def GetFeatureData(self, order:int) -> Dict[str,List[FeatureData]]:
        # TODO: add error handling code, if applicable.
        return self._getFeatureData(order=order)

    # *** PRIVATE STATICS ***

    # *** PRIVATE METHODS ***
