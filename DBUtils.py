import time
import logging
import pandas as pd
import sqlite3

class DataUtilsSQLite:
    def __init__(self, db_path):
        self.db_path = db_path
        self.conn = self.create_connection()
        self.logger = logging.getLogger(__name__)

    # connexion à la base de données SQLite en utilisant le chemin vers la BDD
    def create_connection(self):
        try:
            conn = sqlite3.connect(self.db_path)
            return conn
        except sqlite3.Error as e:
            self.logger.error(f"Error connecting to SQLite database: {e}")
            return None
        
    # insertion des données dans la BDD
    def insert_dataframe(self, table_name, dataframe):
        try:
            dataframe.to_sql(table_name, self.conn, if_exists='append', index=False)
            self.logger.info("Data inserted successfully.")
        except sqlite3.Error as e:
            self.logger.error(f"Error inserting data into table {table_name}: {e}")

    # recuperer les derniers lignes inserer dans table_name
    def get_last_row_db(self, table_name,len_df):
        try:
            query = f"SELECT PATIENT_NUM FROM (SELECT PATIENT_NUM FROM {table_name} ORDER BY ROWID DESC LIMIT {len_df})ORDER BY PATIENT_NUM ASC;"
            
            last_row = pd.read_sql_query(query, self.conn)
            self.logger.info("Last row retrieved successfully.")
            return last_row
        except sqlite3.Error as e:
            self.logger.error(f"Error retrieving last row from table {table_name}: {e}")
            return None
        
    # recuperer les valeurs uniques de IPP(HOSPITAL_PATIENTT_ID) dans table_name
    def get_ipp_value(self, table_name):
        try:
            query = f"SELECT DISTINCT HOSPITAL_PATIENT_ID FROM {table_name}"
            list_ipp = pd.read_sql_query(query, self.conn)
            self.logger.info("Last row retrieved successfully.")
            return list_ipp
        except sqlite3.Error as e:
            self.logger.error(f"Error retrieving last row from table {table_name}: {e}")
            return None
        
    # recuperer le numero de patient qui correspond à l'IPP recherché dans la table DWH_PATIENT_IPPHIST 
    def get_num_patient(self, ipp):
        try:
            query = f"SELECT PATIENT_NUM FROM DWH_PATIENT_IPPHIST WHERE HOSPITAL_PATIENT_ID = {ipp}"
            result = self.conn.execute(query).fetchone()
            patient_num = result[0] if result else None
            return patient_num
        except sqlite3.Error as e:
            self.logger.error(f"Error checking if database is empty: {e}")
            return None
    
    