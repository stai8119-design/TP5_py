import csv
from datetime import datetime
from pathlib import Path

class CsvException(Exception):
    def __init__(self, message):
        super().__init__(message)
class FichierIntrouvableException(CsvException):
    pass
class LigneInvalideException(CsvException):
    pass
class PrixNegatifException(CsvException):
    pass
def logger_erreur(message, fichier_log="erreurs.log"):
    date_actuelle = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(fichier_log, "a", encoding="utf-8") as f:
        f.write(f"[{date_actuelle}] {message}\n")
def charger_csv(chemin):
    fichier = Path(chemin)

    if not fichier.exists() or not fichier.is_file():
        msg = f"Fichier introuvable : {chemin}"
        logger_erreur(msg)
        raise FichierIntrouvableException(msg)

    articles = []

    with open(fichier, "r", encoding="utf-8") as f:
        lecteur = csv.reader(f, delimiter=";")

        for num_ligne, ligne in enumerate(lecteur, start=1):
            if not ligne or all(cellule.strip() == "" for cellule in ligne):
                continue
            if len(ligne) != 3:
                msg = f"Ligne {num_ligne} invalide : 3 colonnes attendues, recu {len(ligne)}."
                logger_erreur(msg)
                raise LigneInvalideException(msg)
            id_art = ligne[0].strip()
            nom_art = ligne[1].strip()
            prix_texte = ligne[2].strip()
            if not id_art or not nom_art:
                msg = f"Ligne {num_ligne} invalide : id ou nom vide."
                logger_erreur(msg)
                raise LigneInvalideException(msg)

            try:
                prix = float(prix_texte)
            except ValueError:
                msg = f"Ligne {num_ligne} invalide : le prix '{prix_texte}' n'est pas numerique."
                logger_erreur(msg)
                raise LigneInvalideException(msg)
            if prix <= 0:
                msg = f"Ligne {num_ligne} : le prix doit etre strictement positif ({prix})."
                logger_erreur(msg)
                raise PrixNegatifException(msg)
            articles.append({
                "id": id_art,
                "nom": nom_art,
                "prix": prix
            })
    return articles