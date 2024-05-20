# Defi Codoc Python

*Ce dépôt comprend le code source du test technique CODOC pour traitement de fichiers médicaux.*

## Installation

Pour installer ce projet, vous pouvez suivre ces étapes :

1. Cloner ce dépôt sur votre machine :
    ```
    git clone https://github.com/NisrineBennor/Defi_Codoc_Python.git
    ```
2. Accéder au répertoire du projet :

    ```
    cd Defi_Codoc_Python
    ```
3. Créer un environnement virtuel :
La commande suivante permet d'installer l'environnement virtuel python,
 ```
python3 -m venv venv
 ```
Cette commande utilise le module python virtualenv pour créer l'environnement virtuel. S'il n'existe pas, il faut l'installer avec pip. Une fois l'environnement configuré, nous pouvons procéder à l'installation de toutes les dépendances nécessaires.

4. Activer l'environnement virtuel :

Sous macOS et Linux :
```
source venv/bin/activate
```
Sous Windows :
```
venv\Scripts\activate
```

5. Installer les dépendances :

   
```
pip install -r requirements.txt
```
### Exécution

Pour traiter le fichier export_patient.xlsx et insérer les données dans la base SQLite, il faut executer le script runner1.py en exectant la commande suivante: 

 ```
 python runner1.py
 ```
Pour traiter les fichiers avec extension .pdf et .docx des comptes rendus medicaux et insérer les données dans la BDD SQLite, il faut executer le script runner2.py en en exectant la commande suivante: 

 ```
 python runner2.py
 ```

### Jeux de données

L'ensemble de données contenues dans le folder "fichiers_sources" est utilisé comme fichiers sources alimenter la base de données SQLite.

