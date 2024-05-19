from config.config_manager import ConfigManager
import os
import pandas as pd
from DBUtils import DataUtilsSQLite
from UtilsFunc import read_pdf
from UtilsFunc import extract_info
from UtilsFunc import read_docx
from UtilsFunc import find_title
import shutil

config = ConfigManager()
root_directory = config['workspace']['root_directory']
connexion=DataUtilsSQLite(config['DBsqlite']['root_db'])
environnement = config['workspace']['environnement']
archive = config['workspace']['archive']

if __name__ == "__main__":
    if environnement == 'local':

        for filename in os.listdir(root_directory):
            print(filename)
            
            ## traitement des fichiers avec extension .pdf et spécifiquement pour les comptes rendus
            if filename.endswith('.pdf'):
                IPP = filename.split("_")[0]
                ID_DOCUMENT=filename.split("_")[1].split(".")[0]
                Type_doc=filename.split(".")[1]
                document_file_path = os.path.join(root_directory, filename)
                patient_document= read_pdf(document_file_path)
                resultat = extract_info(patient_document)
            
                if any('\n' in f for f in resultat):
                    resultat_list = [f.split('\n')[0] for f in resultat]
                else:
                    resultat_list = resultat
                df_doc = pd.DataFrame([resultat_list], columns=['DOCUMENT_DATE', 'AUTHOR'])
                
                patient_document=patient_document.replace("\n", " ")
                titre = find_title(patient_document)
                df_doc = df_doc.assign(DISPLAYED_TEXT= [patient_document],ID_DOC_SOURCE= [ID_DOCUMENT],IPP= [IPP], DOCUMENT_TYPE=[Type_doc],TITLE=[titre])
                df_doc['DOCUMENT_DATE'] = pd.to_datetime(df_doc['DOCUMENT_DATE'], format='%d/%m/%Y',dayfirst=True).dt.strftime('%Y-%m-%d')
                PATIENT_NUM = connexion.get_num_patient(ipp=IPP)
                df_doc = df_doc.assign(PATIENT_NUM = [PATIENT_NUM])
                df_doc = df_doc[['PATIENT_NUM','ID_DOC_SOURCE','DOCUMENT_DATE','DISPLAYED_TEXT','AUTHOR','DOCUMENT_TYPE','TITLE']]
                df_doc.replace(["Non trouvée", "Non trouvé"], pd.NA, inplace=True)
                connexion.insert_dataframe(table_name='DWH_DOCUMENT',dataframe=df_doc)

                # transfert du fichier vers un folder "archive"
                shutil.move(root_directory + '/' + filename , archive + '/' + filename)


             ## traitement des fichiers avec extension .docx et spécifiquement pour les comptes rendus
            if filename.endswith('.docx'):
                IPP = filename.split("_")[0]
                ID_DOCUMENT=filename.split("_")[1].split(".")[0]
                Type_doc=filename.split(".")[1]
                document_file_path = os.path.join(root_directory, filename)
                patient_document= read_docx(document_file_path)
                resultat = extract_info(patient_document)
                
                if any('\n' in f for f in resultat):
                    resultat_list = [f.split('\n')[0] for f in resultat]
                else:
                    resultat_list = resultat


                df_doc = pd.DataFrame([resultat_list], columns=['DOCUMENT_DATE', 'AUTHOR'])
                patient_document=patient_document.replace("\n", " ")
                titre = find_title(patient_document)
                df_doc = df_doc.assign(DISPLAYED_TEXT= [patient_document],ID_DOC_SOURCE= [ID_DOCUMENT],IPP= [IPP], DOCUMENT_TYPE=[Type_doc],TITLE=[titre])
                df_doc['DOCUMENT_DATE'] = pd.to_datetime(df_doc['DOCUMENT_DATE'], format='%d/%m/%Y',dayfirst=True).dt.strftime('%Y-%m-%d')
                PATIENT_NUM = connexion.get_num_patient(ipp=IPP)
                df_doc = df_doc.assign(PATIENT_NUM = [PATIENT_NUM])
                df_doc = df_doc[['PATIENT_NUM','ID_DOC_SOURCE','DOCUMENT_DATE','DISPLAYED_TEXT','AUTHOR','DOCUMENT_TYPE','TITLE']]
                df_doc.replace(["Non trouvée", "Non trouvé"], pd.NA, inplace=True)
                connexion.insert_dataframe(table_name='DWH_DOCUMENT',dataframe=df_doc)

                # transfert du fichier vers un folder "archive"
                shutil.move(root_directory + '/' + filename , archive + '/' + filename)

