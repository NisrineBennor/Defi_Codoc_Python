from PyPDF2 import PdfReader
import re
from docx import Document
import numpy as np


# lire le contenu du fichier(compte rendu) PDF en extrayant le texte de chaque page
def read_pdf(file_path):
    texte = ""
    with open(file_path, 'rb') as pdf_file:
        pdf_reader = PdfReader(pdf_file)
        for page_number in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_number]
            texte += page.extract_text()
    return texte


# utilise de texte recuperer pour rechercher la date du compte rendu 
## et le nom du medecin en se basant sur les expréssiosn regulières.
def extract_info(texte):
    
    # Recherche de la date du document
    date_match = re.search(r"(Compte-Rendu d’hospitalisation|Compte de rendu de consultation)(?:\s*du)?\s*(\d{1,2}/\d{1,2}/\d{4})", texte)
    date = date_match.group(2) if date_match else "Non trouvée"

    date_match_ordo = re.search(r"\b\d{1,2}/\d{1,2}/\d{4}\b", texte)
    date_ordo = date_match_ordo.group(0) if date_match_ordo else "Non trouvée"

    # Recherche du nom du médecin
    doctors = re.findall(r"Dr\.?\s+([A-Za-z]+(?:\s+[A-Za-z]+)*)", texte, flags=re.IGNORECASE)
    doctor_name = doctors[-1] if doctors else "Non trouvé"

    if date == "Non trouvée":
        return [date_ordo.strip(), doctor_name.strip()]
    else:
        return [date.strip(), doctor_name.strip()]

# Lire le contenu du fichier DOCX
def read_docx(file_path):
    try:  
        doc = Document(file_path)      
        texte = ""        
        for paragraph in doc.paragraphs:
            texte += paragraph.text + "\n"    
        return texte
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier DOCX : {e}")
        return None

# rechercher et identifier le titre du document en fonction des mots-clés
def find_title(texte):
    TITLE = ['ordonnance', 'compte de rendu de consultation', "compte-rendu d’hospitalisation"]
    for title in TITLE:
        if title.lower() in texte.lower():
            return title
    return np.nan

