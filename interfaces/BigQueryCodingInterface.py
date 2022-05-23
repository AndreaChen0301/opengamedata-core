import json
import logging
import os
from datetime import datetime
from google.cloud import bigquery
from typing import Dict, List, Tuple, Optional
# import locals
from coding.Code import Code
from coding.Coder import Coder
from config.config import settings as default_settings
from interfaces.CodingInterface import CodingInterface
from schemas.IDMode import IDMode
from utils import Logger

# TODO: see about merging this back into BigQueryInterface for a unified interface.

class BigQueryCodingInterface(CodingInterface):

    # *** PUBLIC BUILT-INS ***

    def __init__(self, game_id: str, settings):
        super().__init__(game_id=game_id)
        self._settings = settings
        self.Open()

    # *** IMPLEMENT ABSTRACT FUNCTIONS ***

    def _open(self, force_reopen: bool = False) -> bool:
        if force_reopen:
            self.Close()
            self.Open(force_reopen=False)
        if not self._is_open:
            if "GITHUB_ACTIONS" in os.environ:
                self._client = bigquery.Client()
            else:
                credential_path : str
                if "GAME_SOURCE_MAP" in self._settings:
                    credential_path = self._settings["GAME_SOURCE_MAP"][self._game_id]["credential"]
                else:
                    credential_path = default_settings["GAME_SOURCE_MAP"][self._game_id]["credential"]
                os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credential_path
                self._client = bigquery.Client()
            if self._client != None:
                self._is_open = True
                Logger.Log("Connected to BigQuery database.", logging.DEBUG)
                return True
            else:
                Logger.Log("Could not connect to BigQuery Database.", logging.WARN)
                return False
        else:
            return True

    def _close(self) -> bool:
        self._client.close()
        self._is_open = False
        Logger.Log("Closed connection to BigQuery.", logging.DEBUG)
        return True

    def _dbPath(self) -> str:
        if "BIGQUERY_CONFIG" in self._settings:
            project_name = self._settings["BIGQUERY_CONFIG"][self._game_id]["PROJECT_ID"]
        else:
            project_name = default_settings["BIGQUERY_CONFIG"][self._game_id]["PROJECT_ID"]
        return f"{project_name}.coding"

    def _allCoders(self) -> Optional[List[Coder]]:
        query = f"""
            SELECT DISTINCT coder_id, name
            FROM `{self._dbPath()}.coders`,
        """
        data = self._client.query(query)
        coders = [Coder(name=str(row['name']), id=str(row['coder_id'])) for row in data]
        return coders if coders != None else []

    def _createCoder(self, coder_name:str) -> bool:
        # TODO: figure out how to make metadata available for insert.
        query = f"""
            INSERT {self._dbPath()}(coder_id, name, metadata)
            VALUES (GENERATE_UUID(), @name, NULL)
        """
        cfg = bigquery.QueryJobConfig(
            query_parameters= [
                bigquery.ScalarQueryParameter(name="name", type_="STRING", value=coder_name),
            ]
        )
        try:
            self._client.query(query=query, job_config=cfg)
        except Exception as err:
            Logger.Log(f"Error while creating a new Coder in database: {err}", level=logging.ERROR, depth=2)
            return False
        else:
            return True

    def _getCodeWordsByGame(self, game_id:str) -> Optional[List[str]]:
        pass

    def _getCodeWordsByCoder(self, coder_id:str) -> Optional[List[str]]:
        pass

    def _getCodeWordsBySession(self, session_id:str) -> Optional[List[str]]:
        pass

    def _getCodesByGame(self, game_id:str) -> Optional[List[Code]]:
        pass

    def _getCodesByCoder(self, coder_id:str) -> Optional[List[Code]]:
        pass

    def _getCodesBySession(self, session_id:str) -> Optional[List[Code]]:
        pass

    def _createCode(self, code:str, coder:Coder, events:List[Code.EventID], notes:Optional[str]=None):
        query = f"""
            INSERT {self._dbPath()}(code_id, code, coder_id, notes, events)
            VALUES (GENERATE_UUID(), @code, @coder_id, @notes, @events)
        """
        evt_params = [
            bigquery.StructQueryParameter.positional(
                bigquery.ScalarQueryParameter(name="session_id", type_="STRING", value=event.SessionID),
                bigquery.ScalarQueryParameter(name="index", type="INTEGER", value=event.Index)
            )
            for event in events
        ]
        cfg = bigquery.QueryJobConfig(
            query_parameters= [
                bigquery.ScalarQueryParameter(name="code", type_="STRING", value=code),
                bigquery.ScalarQueryParameter(name="coder_id", type_="STRING", value=coder.ID),
                bigquery.ScalarQueryParameter(name="notes", type_="STRING", value=notes),
                bigquery.ArrayQueryParameter(
                    name="events",
                    array_type="STRUCT",
                    values=evt_params
                ),
            ]
        )
        try:
            self._client.query(query=query, job_config=cfg)
        except Exception as err:
            Logger.Log(f"Error while creating a new Coder in database: {err}", level=logging.ERROR, depth=2)
            return False
        else:
            return True

    # *** PUBLIC METHODS ***
    def IsOpen(self) -> bool:
        """Overridden version of IsOpen function, checks that BigQueryInterface client has been initialized.

        :return: True if the interface is open, else False
        :rtype: bool
        """
        return True if (super().IsOpen() and self._client is not None) else False