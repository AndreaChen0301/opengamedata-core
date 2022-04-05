## import standard libraries
import abc
import logging
from datetime import datetime
from typing import Dict, List, Tuple, Union

from schemas.IDMode import IDMode
# import local files

class DataInterface(abc.ABC):

    # *** ABSTRACTS ***

    @abc.abstractmethod
    def _open(self) -> bool:
        pass

    @abc.abstractmethod
    def _close(self) -> bool:
        pass

    @abc.abstractmethod
    def _allIDs(self) -> List[str]:
        pass

    @abc.abstractmethod
    def _fullDateRange(self) -> Dict[str,datetime]:
        pass

    @abc.abstractmethod
    def _rowsFromIDs(self, id_list:List[str], id_mode:IDMode=IDMode.SESSION, versions:Union[List[int],None] = None) -> List[Tuple]:
        pass

    @abc.abstractmethod
    def _IDsFromDates(self, min:datetime, max:datetime, versions:Union[List[int],None] = None) -> List[str]:
        pass

    @abc.abstractmethod
    def _datesFromIDs(self, id_list:List[str], id_mode:IDMode=IDMode.SESSION, versions:Union[List[int],None] = None) -> Dict[str,datetime]:
        pass

    # *** PUBLIC BUILT-INS ***

    def __init__(self, game_id):
        self._game_id : str  = game_id
        self._is_open : bool = False

    def __del__(self):
        self.Close()

    # *** PUBLIC STATICS ***

    # *** PUBLIC METHODS ***

    def Open(self, force_reopen:bool = False) -> bool:
        if force_reopen or not self._is_open:
            return self._open()
        else:
            return True
    
    def IsOpen(self) -> bool:
        return True if self._is_open else False

    def Close(self) -> bool:
        if self._is_open:
            return self._close()
        else:
            return True

    def AllIDs(self) -> Union[List[str],None]:
        if not self._is_open:
            logging.warn("Can't retrieve data, the source interface is not open!")
            return None
        else:
            return self._allIDs()

    def FullDateRange(self) -> Union[Dict[str,datetime], Dict[str,None]]:
        if not self._is_open:
            logging.warn("Can't retrieve data, the source interface is not open!")
            return {'min':None, 'max':None}
        else:
            return self._fullDateRange()

    def RowsFromIDs(self, id_list:List[str], id_mode:IDMode=IDMode.SESSION, versions:Union[List[int],None]=None) -> Union[List[Tuple], None]:
        if not self._is_open:
            logging.warn("Can't retrieve data, the source interface is not open!")
            return None
        else:
            return self._rowsFromIDs(id_list=id_list, id_mode=id_mode, versions=versions)

    def IDsFromDates(self, min:datetime, max:datetime, versions: Union[List[int],None]=None) -> Union[List[str], None]:
        if not self._is_open:
            logging.warn("Can't retrieve IDs, the source interface is not open!")
            return None
        else:
            return self._IDsFromDates(min=min, max=max, versions=versions)

    def DatesFromIDs(self, id_list:List[str], id_mode:IDMode=IDMode.SESSION, versions:Union[List[int],None]=None) -> Union[Dict[str,datetime], Dict[str,None]]:
        if not self._is_open:
            logging.warn("Can't retrieve dates, the source interface is not open!")
            return {'min':None, 'max':None}
        else:
            return self._datesFromIDs(id_list=id_list, id_mode=id_mode, versions=versions)

    # *** PRIVATE STATICS ***

    # *** PRIVATE METHODS ***
