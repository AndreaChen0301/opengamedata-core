## import standard libraries
import abc
import logging
from typing import Any, Dict, List, Type, Union
# import locals
from extractors.ExtractorRegistry import ExtractorRegistry
from features.FeatureLoader import FeatureLoader
from features.FeatureData import FeatureData
from schemas.GameSchema import GameSchema
from schemas.Event import Event
from schemas.Request import ExporterTypes

## @class Processor
class Processor(abc.ABC):

    # *** ABSTRACTS ***

    @abc.abstractmethod
    def _prepareRegistry(self) -> ExtractorRegistry:
        pass

    @abc.abstractmethod
    def _prepareLoader(self) -> FeatureLoader:
        pass

    ## Abstract declaration of a function to get the names of all features.
    @abc.abstractmethod
    def _getExtractorNames(self) -> List[str]:
        pass

    ## Abstract declaration of a function to get the calculated value of the feature, given data seen so far.
    @abc.abstractmethod
    def _processEvent(self, event:Event) -> None:
        pass

    @abc.abstractmethod
    def _processFeatureData(self, feature:FeatureData) -> None:
        pass

    # *** PUBLIC BUILT-INS ***

    def __init__(self, LoaderClass:Type[FeatureLoader], game_schema: GameSchema,
                 feature_overrides:Union[List[str],None]=None):
        self._game_schema : GameSchema            = game_schema
        self._overrides   : Union[List[str],None] = feature_overrides
        self._LoaderClass : Type[FeatureLoader]   = LoaderClass
        self._registry    : ExtractorRegistry     = self._prepareRegistry()
        self._loader      : FeatureLoader         = self._prepareLoader()
    def __str__(self):
        return f""

    # *** PUBLIC STATICS ***

    # *** PUBLIC METHODS ***

    def GetExtractorNames(self) -> List[str]:
        # TODO: add error handling code, if applicable.
        return self._getExtractorNames()

    def ProcessEvent(self, event:Event) -> None:
        # TODO: add error handling code, if applicable.
        self._processEvent(event=event)

    def ProcessFeatureData(self, feature:FeatureData) -> None:
        # TODO: add error handling code, if applicable.
        self._processFeatureData(feature=feature)

    # *** PRIVATE STATICS ***

    # *** PRIVATE METHODS ***
