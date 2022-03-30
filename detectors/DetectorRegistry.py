## import standard libraries
import enum
import json
import logging
from collections import OrderedDict
from datetime import datetime
from typing import Any, Dict, List, Union
from features.FeatureData import FeatureData
## import local files
import utils
from Detector import Detector
from schemas.Event import Event

## @class Extractor
#  Abstract base class for game feature extractors.
#  Gives a few static functions to be used across all extractor classes,
#  and defines an interface that the SessionProcessor can use.
class FeatureRegistry:
    """Class for registering features to listen for events.

    :return: [description]
    :rtype: [type]
    """
    class Listener:
        @enum.unique
        class Kinds(enum.Enum):
            AGGREGATE = enum.auto()
            PERCOUNT  = enum.auto()

        def __init__(self, name:str, kind:Kinds):
            self.name = name
            self.kind = kind
        
        def __str__(self) -> str:
            return f"{self.name} ({'aggregate' if self.kind == FeatureRegistry.Listener.Kinds.AGGREGATE else 'per-count'})"

        def __repr__(self) -> str:
            return str(self)

    @enum.unique
    class FeatureOrders(enum.Enum):
        FIRST_ORDER = 0
        SECOND_ORDER = 1

    # *** BUILT-INS ***

    # Base constructor for Registry.
    def __init__(self, order:int=len(FeatureOrders)):
        """Base constructor for Registry

        Just sets up mostly-empty dictionaries for use by the registry.
        """
        self._features : List[OrderedDict[str, Feature]] = [OrderedDict() for i in range(order)]
        # self._features : Dict[str, OrderedDict[str, Feature]] = {
        #     "first_order" : OrderedDict(),
        #     "second_order" : OrderedDict()
        # }
        self._event_registry : Dict[str,List[FeatureRegistry.Listener]] = {"all_events":[]}
        self._feature_registry: Dict[str,List[FeatureRegistry.Listener]] = {}

    # string conversion for Extractors.
    def __str__(self) -> str:
        """string conversion for Extractors.

        Creates a list of all features in the extractor, separated by newlines.
        :return: A string with line-separated stringified features.
        :rtype: str
        """
        ret_val : List[str] = []
        for order in self._features:
            ret_val += [str(feat) for feat in order.values()]
        return '\n'.join(ret_val)

    # Alternate string conversion for Extractors, with limitable number of lines.
    def to_string(self, num_lines:Union[int,None] = None) -> str:
        """Alternate string conversion for Extractors, with limitable number of lines.

        Creates a list of features in the extractor, separated by newlines.
        Optional num_lines param allows the function caller to limit number of lines in the string.
        :param num_lines: Max number of lines to include in the string.
        If None, then include all strings, defaults to None
        :type num_lines:  Union[int,None], optional
        :return: A string with line-separated stringified features.
        :rtype: str
        """
        ret_val : List[str] = []
        for order in self._features:
            ret_val += [str(feat) for feat in order.values()]
        if num_lines is None:
            return '\n'.join(ret_val)
        else:
            return '\n'.join(ret_val[:num_lines])

    # *** PUBLIC STATICS ***

    # *** PUBLIC METHODS ***
    def OrderCount(self) -> int:
        """Gets the number of "orders" of features stored in the FeatureRegistry.
        For now, there's just two of them.

        :return: _description_
        :rtype: int
        """
        return len(self._features)

    def ExtractFromEvent(self, event:Event) -> None:
        """Perform extraction of features from a row.

        :param event: [description]
        :type event: Event
        :param table_schema: A data structure containing information on how the db
                             table assiciated with this game is structured.
        :type table_schema: TableSchema
        """
        if event.event_name in self._event_registry.keys():
            # send event to every listener for the given event name.
            for listener in self._event_registry[event.event_name]:
                for order_key in range(len(self._features)):
                    if listener.name in self._features[order_key].keys():
                        self._features[order_key][listener.name].ExtractFromEvent(event)
        # don't forget to send to any features listening for "all" events
        for listener in self._event_registry["all_events"]:
            for order_key in range(len(self._features)):
                if listener.name in self._features[order_key].keys():
                    self._features[order_key][listener.name].ExtractFromEvent(event)

    def ExtractFromFeatureData(self, feature:FeatureData) -> None:
        """Perform extraction of features from a row.

        :param event: [description]
        :type event: Event
        :param table_schema: A data structure containing information on how the db
                             table assiciated with this game is structured.
        :type table_schema: TableSchema
        """
        if feature.Name() in self._feature_registry.keys():
            # send event to every listener for the given feature name.
            for listener in self._feature_registry[feature.Name()]:
                for order_key in range(len(self._features)):
                    if listener.name in self._features[order_key].keys():
                        self._features[order_key][listener.name].ExtractFromFeatureData(feature)

    def GetFeatureNames(self) -> List[str]:
        """Function to generate a list names of all enabled features, given a GameSchema
        This is different from the feature_names() function of GameSchema,
        which ignores the 'enabled' attribute and does not expand per-count features
        (e.g. this function would include 'lvl0_someFeat', 'lvl1_someFeat', 'lvl2_someFeat', etc.
        while feature_names() only would include 'someFeat').

        :param schema: The schema from which feature names should be generated.
        :type schema: GameSchema
        :return: A list of feature names.
        :rtype: List[str]
        """
        ret_val : List[str] = []
        for order in self._features:
            for feature in order.values():
                ret_val += feature.GetFeatureNames()
        return ret_val

    def GetFeatureData(self, order:int, player_id:Union[str, None]=None, sess_id:Union[str, None]=None) -> List[FeatureData]:
        ret_val : List[FeatureData] = []
        for feature in self._features[order].values():
            ret_val.append(feature.ToFeatureData(player_id=player_id, sess_id=sess_id))
        return ret_val

    def GetFeatureValues(self) -> List[Any]:
        ret_val : List[Any] = []
        for order in self._features:
            for feature in order.values():
                next_vals = feature.GetFeatureValues()
                ret_val += next_vals if next_vals != [] else [None]
        return ret_val

    def GetFeatureStringValues(self) -> List[str]:
        ret_val : List[str] = []
        _vals   : List[Any] = self.GetFeatureValues()

        for val in _vals:
            str_val : str
            if type(val) == dict:
                str_val = json.dumps(val)
            elif type(val) == datetime:
                str_val = val.isoformat()
            else:
                str_val = str(val)
            ret_val.append(str_val)
        return ret_val

    # *** PRIVATE STATICS ***

    # *** PRIVATE METHODS ***

    def Register(self, feature:Feature, kind:Listener.Kinds):
        _listener = FeatureRegistry.Listener(name=feature.Name(), kind=kind)
        _feature_types = feature.GetFeatureDependencies()
        _event_types   = feature.GetEventDependencies()
        # First, add feature to the _features dict.
        if len(_feature_types) > 0:
            self._features[FeatureRegistry.FeatureOrders.SECOND_ORDER.value][feature.Name()] = feature
        else:
            self._features[FeatureRegistry.FeatureOrders.FIRST_ORDER.value][feature.Name()] = feature
        # Register feature to listen for any requested first-order features.
        for _feature in _feature_types:
            if _feature not in self._feature_registry.keys():
                self._feature_registry[_feature] = []
            self._feature_registry[_feature].append(_listener)
        # Finally, register feature's requested events.
        if "all_events" in _event_types:
            self._event_registry["all_events"].append(_listener)
        else:
            for event in _event_types:
                if event not in self._event_registry.keys():
                    self._event_registry[event] = []
                self._event_registry[event].append(_listener)

    # def _format(obj):
    #     if obj == None:
    #         return ""
    #     elif type(obj) is timedelta:
    #         total_secs = obj.total_seconds()
    #         # h = total_secs // 3600
    #         # m = (total_secs % 3600) // 60
    #         # s = (total_secs % 3600) % 60 // 1  # just for reference
    #         # return f"{h:02.0f}:{m:02.0f}:{s:02.3f}"
    #         return str(total_secs)
    #     if obj is None:
    #         return ''
    #     else:
    #         return str(obj)