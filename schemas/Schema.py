## import standard libraries
import logging
import typing
## import local files
import utils

class Schema:
    def __init__(self, schema_name:str, schema_path:str = "./schemas/JSON"):
        ## define instance vars
        self._schema:                     typing.Dict      = {}
        self._feature_list:               typing.Dict      = None
        ## set instance vars
        self._schema = utils.loadJSONFile(schema_name, schema_path)
        if self._schema is None:
            logging.error("Could not find event_data_complex schemas at {}".format(schema_path))
        else:
            self._feature_list = list(self._schema["features"]["perlevel"].keys(self)) + list(self._schema["features"]["aggregate"].keys(self))

    def schema(self):
        return self._schema

    def events(self):
        return self._schema["events"]

    def event_types(self):
        return self._schema["events"].keys(self)

    def features(self):
        return self._schema["features"]

    def perlevel_features(self):
        return self._schema["features"]["perlevel"]

    def aggregate_features(self):
        return self._schema["features"]["aggregate"]

    def feature_list(self):
        return self._feature_list

    def db_columns(self):
        return self._schema["db_columns"]