## import standard libraries
import json
import logging
import math
import typing
## import local files
import utils
from GameTable import GameTable
from ProcManager import ProcManager
from RawManager import RawManager
from Request import Request
from schemas.Schema import Schema
from feature_extractors.WaveExtractor import WaveExtractor

def exportDataToCSV(db, settings, request: Request):
    db_settings = settings["db_config"]
    if request.game_id is not None:
        game_table: GameTable = GameTable(db=db, settings=settings, request=request)

        ## NOTE: I've left the bit of cache code ported from the old logger,
        ## on the off chance we ever decide to use caching again.
        # if request.read_cache:
        #     cache_query = "SELECT output FROM cache WHERE filter=%s ORDER BY time DESC LIMIT 1"
        #     cache_params = [request]
        #     try:
        #         db_cursor.execute(cache_query, cache_params)
        #         cache_result = db_cursor.fetchall()
        #         if cache_result is not []:
        #             logger.debug("cache_result: " + str(cache_result))
        #             quit()
        #     except Exception as err:
        #         utils.SQL.server500Error(err)

        parse_result: str = _getAndParseData(request, game_table, db, settings)
        
        # output results
        if parse_result is not None:
            try:
                print(json.dumps(parse_result))
            except Exception as err:
                utils.SQL.server500Error(err)
    else:
        logging.error("Game ID was not given!")

def _getAndParseData(request: Request, game_table: GameTable, db, settings):
    db_cursor = db.cursor(buffered=True)
    data_directory = settings["DATA_DIR"] + request.game_id
    db_settings = settings["db_config"]
    
    # logging.debug("complex_data_index: {}".format(complex_data_index))
    ## NOTE: Some code that could be useful to refer to if we ever decide to do something to unwrap
    ## the event_data_complex column.
    # parsed_columns = db_cursor.column_names[0:complex_data_index]                 \
    #                + tuple(json.loads(single_elem[0][complex_data_index]).keys()) \
    #                + db_cursor.column_names[complex_data_index+1:-1]

    # First, get the files and game-specific vars ready
    raw_csv_file = open("{}/{}_{}_raw.csv".format(data_directory, utils.dateToFileSafeString(request.start_date),
                                               utils.dateToFileSafeString(request.end_date)), "w")
    proc_csv_file = open("{}/{}_{}_proc.csv".format(data_directory, utils.dateToFileSafeString(request.start_date),
                                                 utils.dateToFileSafeString(request.end_date)), "w")
    game_schema: Schema
    game_extractor: type
    if request.game_id == "WAVES":
        game_schema = Schema(schema_name="WAVES.json")
        game_extractor = WaveExtractor
    else:
        raise Exception("Got an invalid game ID!")
    # Now, we're ready to set up the managers:
    raw_mgr = RawManager(game_table=game_table, game_schema=game_schema, raw_csv_file=raw_csv_file)
    proc_mgr = ProcManager(ExtractorClass=game_extractor, game_table=game_table, game_schema=game_schema, proc_csv_file=proc_csv_file )
    # Next, calculate metadata
    raw_metadata = utils.csvMetadata(game_name=request.game_id, begin_date=request.start_date, end_date=request.end_date,
                                      field_list=game_schema.db_columns_with_types())
    feature_descriptions = {**game_schema.perlevel_features(), **game_schema.aggregate_features()}
    proc_metadata = utils.csvMetadata(game_name=request.game_id, begin_date=request.start_date, end_date=request.end_date,
                                      field_list=feature_descriptions)

    # after generating the metadata, write to each file
    raw_csv_file.write(raw_metadata)
    proc_csv_file.write(proc_metadata)
    # then write the column headers for the raw csv.
    raw_mgr.WriteRawCSVHeader()
    proc_mgr.WriteProcCSVHeader()

    num_sess = len(game_table.session_ids)
    slice_size = settings["BATCH_SIZE"]
    session_slices = [[game_table.session_ids[i] for i in \
                     range( j*slice_size, min((j+1)*slice_size - 1, num_sess) )] for j in \
                     range( 0, math.ceil(num_sess / slice_size) )]
    for next_slice in session_slices:
        # grab data for the given session range. Sort by event time, so 
        filt = "app_id=\"WAVES\" AND session_id BETWEEN {} AND {}".format(next_slice[0], next_slice[-1])
        next_data_set = utils.SQL.SELECT(cursor=db_cursor, db_name=db.database, table=db_settings["table"],
                                        filter= filt, sort_columns=["client_time"], sort_direction = "ASC",
                                        distinct=False)
        # now, we process each row.
        for row in next_data_set:
            session_id = row[game_table.session_id_index]
            if session_id in game_table.session_ids:
                raw_mgr.ProcessRow(row)
                proc_mgr.ProcessRow(row)
            else:
                logging.warn("Found a session which was in the slice but not in the list of sessions for processing.")
        
    # after processing all rows for all slices, write out the session data and reset for next slice.
    raw_mgr.WriteRawCSVLines()
    raw_mgr.ClearLines()
    proc_mgr.calculateAggregateFeatures()
    proc_mgr.WriteProcCSVLines()
    proc_mgr.ClearLines()

    ## NOTE: I've left the bit of cache code ported from the old logger,
    ## on the off chance we ever decide to use caching again.
    # if request.write_cache:
    #     cache_query = "INSERT INTO cache (filter, output) VALUES (%s, %s)"
    #     cache_params = [request, ret_val]
    #     try:
    #         db_cursor.execute(cache_query, cache_params)
    #     except Exception as err:
    #         utils.SQL.server500Error(logger, err)

    return "Successfully completed."