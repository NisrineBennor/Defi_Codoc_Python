import sqlite3
from PyPDF2 import PdfReader
from config.config_manager import ConfigManager
import os
import pandas as pd
from datetime import datetime
from DBUtils import DataUtilsSQLite
import shutil
from UtilsFunc import *
import numpy as np


config = ConfigManager()
root_directory = config['workspace']['root_directory']
connexion=DataUtilsSQLite(config['DBsqlite']['root_db'])
environnement = config['workspace']['environnement']
archive = config['workspace']['archive']

if __name__ == "__main__":
    if environnement == 'local':

        for filename in os.listdir(root_directory):
            print(filename)
           

           ## traitement du fichier avec extension .xlsx et spécifiquement pour les 
           ## fichiers qui ont le même format de que le fichier export_patient.xlsx
            if filename.endswith('.xlsx'):

                patient_file_path = os.path.join(root_directory, filename)
                df_patient = pd.read_excel(patient_file_path,sheet_name='Export Worksheet',header=0)

                rename_cols = {'NOM':'LASTNAME', 'PRENOM':'FIRSTNAME', 'DATE_NAISSANCE':'BIRTH_DATE', 'SEXE':'SEX', 'NOM_JEUNE_FILLE':'MAIDEN_NAME',
                            'ADRESSE':'RESIDENCE_ADDRESS', 'TEL':'PHONE_NUMBER', 'CP':'ZIP_CODE', 'VILLE':'RESIDENCE_CITY', 'PAYS':'RESIDENCE_COUNTRY',
                            'DATE_MORT':'DEATH_DATE'}
                
                
                df_patient= df_patient.rename(columns=rename_cols)
                print(df_patient)
                df_patient['BIRTH_DATE'] = pd.to_datetime(df_patient['BIRTH_DATE'],dayfirst=True).dt.strftime('%Y-%m-%d')
                df_patient['DEATH_DATE'] = pd.to_datetime(df_patient['DEATH_DATE'],dayfirst=True).dt.strftime('%Y-%m-%d')
                df_patient_final = df_patient.copy()
                ipp = df_patient_final.pop('HOSPITAL_PATIENT_ID')                    
                connexion.insert_dataframe(table_name='DWH_PATIENT',dataframe=df_patient_final)

               
                patient_num = connexion.get_last_row_db(table_name='DWH_PATIENT',len_df=len(df_patient_final))
                df_ipp_patient = df_patient['HOSPITAL_PATIENT_ID']
                df_ipp_patient = pd.DataFrame(df_ipp_patient)
                df_ipp_patient['PATIENT_NUM'] = patient_num

                list_ipp = connexion.get_ipp_value(table_name='DWH_PATIENT_IPPHIST')
                df_ipp_patient['HOSPITAL_PATIENT_ID']=df_ipp_patient['HOSPITAL_PATIENT_ID'].astype(str)
                df_filtered = df_ipp_patient[~df_ipp_patient['HOSPITAL_PATIENT_ID'].isin(list_ipp['HOSPITAL_PATIENT_ID'])]
                connexion.insert_dataframe(table_name='DWH_PATIENT_IPPHIST',dataframe=df_filtered)

                # transfert du fichier vers un folder "archive"
                shutil.move(root_directory + '/' + filename , archive + '/' + filename)
                print('File move to archive')
