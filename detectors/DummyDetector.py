# import standard libraries
from datetime import datetime
from typing import Any, Callable, List, Union
# import local files
from detectors.Detector import Detector
from detectors.DetectorEvent import DetectorEvent
from schemas.Event import Event

class CustomDetector(Detector):
    """Template file to serve as a guide for creating custom Feature subclasses for games.

    :param Feature: Base class for a Custom Feature class.
    :type Feature: _type_
    """

    # *** Implement abstract functions ***

    def _getEventDependencies(self) -> List[str]:
        """_summary_

        :return: _description_
        :rtype: List[str]
        """
        return [] # >>> fill in names of events this Detector should use for detecting whatever you're looking for. <<<

    def _extractFromEvent(self, event:Event) -> None:
        """_summary_

        :param event: _description_
        :type event: Event
        """
        # >>> use the data in the Event object to update state variables as needed. <<<
        # Note that this function runs once on each Event whose name matches one of the strings returned by _getEventDependencies()
        #
        # e.g. check if the event name contains the substring "Click," and if so set self._found_click to True
        # if "Click" in event.event_name:
        #     self._found_click = True
        return
    
    def _trigger_condition(self) -> bool:
        """_summary_
        """
        # >>> use the detector's state data to determine if conditions are met to trigger an event. <<<
        # Note that this function also runs once for each Event, after the _extractFromEvent(...) function is done.
        #
        # e.g. check if we have found a click event, and if so, we want to trigger the custom detector Event.
        #      in the 'True' case, we also set self._found_click back to False, so that the trigger condition is False until a new click Event is found.
        # if self._found_click == True:
        #     self._found_click = False
        #     return True
        # else:
        #     return False
        # note the code above is redundant, we could just return self._found_click to get the same result;
        # the more-verbose code is here for illustrative purposes.
        return False

    def _trigger_event(self) -> Union[Event, None]:
        """_summary_

        :return: _description_
        :rtype: List[Any]
        """
        ret_val : Event = DetectorEvent(session_id="Not Implemented", app_id="Not Implemented", timestamp=datetime.now(),
                                        event_name="CustomDetector", event_data={})
        # >>> use state variables to generate the detector's event. <<<
        # >>> definitely don't return all these "Not Implemented" things, unless you really find that useful... <<<
        #
        # e.g. for an (admittedly redundant) Event stating a click of any kind was detected:
        # ret_val : Event = Event(session_id="Unknown", app_id="CustomGame", timestamp=datetime.now(),
        #                         event_name="ClickDetected", event_data={})
        # note the code above doesn't provide much useful information to the Event;
        # we may want to use additional state variables to capture the session_id, app_id, timestamp, etc. from the click Event in _extractFromEvent(...)
        # further note the event_data can contain any extra data you desire; its contents are entirely up to you.
        return ret_val

    # *** BUILT-INS ***

    def __init__(self, name:str, description:str, count_index:int, trigger_callback:Callable[[Event], None]):
        super().__init__(name=name, description=description, count_index=count_index, trigger_callback=trigger_callback)
        # >>> create/initialize any variables to track detector state <<<
        #
        # e.g. To track whether detector found a click event yet:
        # self._found_click : bool = False

    # *** PUBLIC STATICS ***

    # *** PUBLIC METHODS ***

    # *** PRIVATE STATICS ***

    # *** PRIVATE METHODS ***
