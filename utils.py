## @namespace utils
#  A module of utility functions used in the feature_extraction_to_csv project
import datetime
import http
import json
import logging
import math
import MySQLdb
import os
import sshtunnel
import traceback
import typing

## Function to open a given JSON file, and retrieve the data as a Python object.
#  @param filename  The name of the JSON file. If the file extension is not .json,
#                       then ".json" will be appended.
#  @param path      The path (relative or absolute) to the folder containing the
#                       JSON file. If path does not end in /, then "/" will be appended.
#  @return          A python object parsed from the JSON.
def loadJSONFile(filename: str, path:str = "./") -> object:
    if not filename.lower().endswith(".json"):
        logging.debug(f"Got a filename that didn't end with .json: {filename}, appending .json")
        filename = filename + ".json"
    if not path.endswith("/"):
        path = path + "/"
    ret_val = None
    try:
        json_file = open(path+filename, "r")
        ret_val = json.loads(json_file.read())
        json_file.close()
    except Exception as err:
        logging.error(f"Could not read file at {path+filename}  \
                      \nFull error message: {str(err)}          \
                      \nCurrent directory: {os.getcwd()}")
        raise err
    return ret_val

## Function that converts a datetime object into a filename-friendly format.
#  Yes, there is undoubtedly a built-in way to do this, but this is what I've got.
#  @param date  The datetime object to be formatted.
#  @return      Formatted string representing a date.
def dateToFileSafeString(date: datetime.datetime):
    return f"{date.month}-{date.day}-{date.year}"

## Dumb struct to collect data used to establish a connection to a SQL database.
class SQLLogin:
    def __init__(self, host: str, port: int, user: str, pword: str, db_name: str):
        self.host    = host
        self.port    = port
        self.user    = user
        self.pword   = pword
        self.db_name = db_name

## Dumb struct to collect data used to establish a connection over ssh.
class SSHLogin:
    def __init__(self, host: str, port: int, user: str, pword: str):
        self.host    = host
        self.port    = port
        self.user    = user
        self.pword   = pword

## @class SQL
#  A utility class containing some functions to assist in retrieving from a database.
#  Specifically, helps to connect to a database, make selections, and provides
#  a nicely formatted 500 error message.
class SQL:
    ## Function to set up a connection to a database, via an ssh tunnel if available.
    #  @return A tuple consisting of the tunnel and database connection, respectively.
    def prepareDB(db_settings, ssh_settings) -> typing.Tuple:
        # Load settings, set up consts.
        DB_NAME_DATA = db_settings["DB_NAME_DATA"]
        DB_USER = db_settings['DB_USER']
        DB_PW = db_settings['DB_PW']
        DB_HOST = db_settings['DB_HOST']
        DB_PORT = db_settings['DB_PORT']
        SSH_USER = ssh_settings['SSH_USER']
        SSH_PW = ssh_settings['SSH_PW']
        SSH_HOST = ssh_settings['SSH_HOST']
        SSH_PORT = ssh_settings['SSH_PORT']

        # set up other global vars as needed:
        logging.basicConfig(level=logging.INFO)
        sql_login = SQLLogin(host=DB_HOST, port=DB_PORT, user=DB_USER, pword=DB_PW, db_name=DB_NAME_DATA)
        if (SSH_HOST != "" and SSH_USER != "" and SSH_PW != ""):
            ssh_login = SSHLogin(host=SSH_HOST, port=SSH_PORT, user=SSH_USER, pword=SSH_PW)
            tunnel,db = SQL.connectToMySQLViaSSH(sql=sql_login, ssh=ssh_login)
        else:
            db = SQL.connectToMySQL(login=sql_login)
            tunnel = None
        return (tunnel, db)

    ## Function to help connect to a mySQL server.
    #  Simply tries to make a connection, and prints an error in case of failure.
    #
    #  @param host      The name of the database host server.
    #  @param port      The database server port to which we want to connect.
    #  @param user      Username for connecting to the database.
    #  @param password  The given user's password.
    #  @param database  The actual name of the database on the host.
    #  @return          An open connection to the database if successful,
    #                       otherwise None.
    @staticmethod
    def connectToMySQL(login: SQLLogin):
        try:
            return MySQLdb.connect(host = login.host, port = login.port,
                                           user = login.user, password = login.pword,
                                           database = login.db_name)
        except MySQLdb.connections.Error as err:
            logging.error("Could no connect to the MySql database: " + str(err))
            return None

    ## Function to help connect to a mySQL server over SSH.
    #  Simply tries to make a connection, and prints an error in case of failure.
    #
    #  @param host      The name of the database host server.
    #  @param port      The database server port to which we want to connect.
    #  @param user      Username for connecting to the database.
    #  @param password  The given user's password.
    #  @param database  The actual name of the database on the host.
    #  @return          An open connection to the database if successful,
    #                       otherwise None.
    @staticmethod
    def connectToMySQLViaSSH(sql: SQLLogin, ssh: SSHLogin):
        try:
            tunnel_logger = logging.getLogger('tunnel_logger')
            tunnel_logger.setLevel(logging.WARN)
            tunnel = sshtunnel.SSHTunnelForwarder(
                (ssh.host, ssh.port), ssh_username=ssh.user, ssh_password=ssh.pword,
                remote_bind_address=(sql.host, sql.port), logger=tunnel_logger
            )
            tunnel.start()
            logging.info("Connected to SSH")
            conn = MySQLdb.connect(host = sql.host, port = tunnel.local_bind_port,
                                           user = sql.user, password = sql.pword,
                                           database = sql.db_name)
            logging.info("Connected to SQL")
            return (tunnel, conn)
        except Exception as err:
            logging.error("Could not connect to the MySql database: " + str(err))
            return None

    @staticmethod
    def disconnectMySQLViaSSH(tunnel, db):
        db.close()
        if tunnel is not None:
            tunnel.stop()

    ## Function to build and execute SELECT statements on a database connection.
    #  @param cursor        A database cursor, retrieved from the active connection.
    #  @param db_name       The name of the database to which we are connected.
    #  @param table         The name of the table from which we want to make a selection.
    #  @param columns       A list of columns to be selected. If empty (or None),
    #                           all columns will be used (SELECT * FROM ...).
    #                           Default: None
    #  @param filter        A string giving the constraints for a WHERE clause.
    #                           (The "WHERE" term itself should not be part of the filter string)
    #                           Default: None
    #  @param limit         The maximum number of rows to be selected. Use -1 for no limit.
    #                           Default: -1
    #  @param sort_columns  A list of columns to sort results on. The order of columns
    #                           in the list is the order given to SQL
    #                           Default: None
    #  @param sort_direction The "direction" of sorting, either ascending or descending.
    #                           Default: "ASC"
    #  @param grouping      A column name to group results on. Subject to SQL rules for grouping.
    #                           Default: None
    #  @param distinct      A bool to determine whether to select only rows with
    #                           distinct values in the column.
    #                           Default: False
    #  @param distinct      A bool to determine whether all results should be fetched and returned.
    #                           Default: True
    #  @return              A collection of all rows from the selection, if fetch_results is true,
    #                           otherwise None.
    @staticmethod
    def SELECT(cursor, db_name: str, table: str,
               columns: typing.List[str] = None, filter: str = None, limit: int = -1,
               sort_columns: typing.List[str] = None, sort_direction = "ASC", grouping: str = None,
               distinct: bool = False, fetch_results: bool = True) -> typing.List[typing.Tuple]:
        d = "DISTINCT " if distinct else ""
        cols      = ",".join(columns)      if columns is not None      and len(columns) > 0      else "*"
        sort_cols = ",".join(sort_columns) if sort_columns is not None and len(sort_columns) > 0 else None
        table_path = db_name + "." + str(table)

        sel_clause   = "SELECT " + d + cols + " FROM " + table_path
        where_clause = "" if filter    is None else " WHERE {}".format(filter)
        group_clause = "" if grouping  is None else " GROUP BY {}".format(grouping)
        sort_clause  = "" if sort_cols is None else " ORDER BY {} {} ".format(sort_cols, sort_direction)
        lim_clause   = "" if limit < 0         else " LIMIT {}".format(str(limit))

        query = sel_clause + where_clause + group_clause + sort_clause + lim_clause + ";"
        logging.info("Running query: " + query)
        # print(f"running query: {query}")
        start = datetime.datetime.now()
        cursor.execute(query)
        time_delta = datetime.datetime.now()-start
        logging.info("Query execution completed, time to execute: {:d} min, {:.3f} sec".format( \
            math.floor(time_delta.total_seconds()/60), time_delta.total_seconds() % 60 ) \
        )
        # print("Query execution completed, time to execute: {:d} min, {:.3f} sec".format( \
        #     math.floor(time_delta.total_seconds()/60), time_delta.total_seconds() % 60 ) \
        # )
        result = cursor.fetchall() if fetch_results else None
        time_delta = datetime.datetime.now()-start
        # logging.info(f"Query fetch completed, total query time: {}")
        logging.info("Query fetch completed, total query time:    {:d} min, {:.3f} sec to get {:d} rows".format( \
            math.floor(time_delta.total_seconds()/60), time_delta.total_seconds() % 60, len(result) ) \
        )
        return result

    ## Simple function to construct and log a nice server 500 error message.
    #  @param err_msg A more detailed error message with info to help debugging.
    @staticmethod
    def server500Error(err_msg: str):
        logging.error("HTTP Response: {}{}".format(http.HTTPStatus.INTERNAL_SERVER_ERROR.value, \
                                http.HTTPStatus.INTERNAL_SERVER_ERROR.phrase ))
        logging.error(f"Error Message: {err_msg}")
