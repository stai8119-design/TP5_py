from pathlib import Path
import tempfile
import unittest

from csv_reader import (
    charger_csv,
    FichierIntrouvableException,
    LigneInvalideException,
    PrixNegatifException,
)
class TestChargerCsv(unittest.TestCase):
    def setUp(self):
        self.dossier_temp = tempfile.TemporaryDirectory()
        self.dossier = Path(self.dossier_temp.name)
    def tearDown(self):
        self.dossier_temp.cleanup()
    def creer_fichier(self, nom, contenu):
        chemin = self.dossier / nom
        chemin.write_text(contenu, encoding="utf-8")
        return chemin
    def test_csv_valide_trois_articles_avec_lignes_vides(self):
        contenu = (
            "\n"
            "1;Clavier;25.5\n"
            "   \n"
            "2;Souris;15\n"
            "3;Ecran;180.0\n"
        )
        fichier = self.creer_fichier("valide.csv", contenu)
        resultat = charger_csv(fichier)
        self.assertEqual(len(resultat), 3)
        self.assertEqual(resultat[0], {"id": "1", "nom": "Clavier", "prix": 25.5})
        self.assertEqual(resultat[1], {"id": "2", "nom": "Souris", "prix": 15.0})
        self.assertEqual(resultat[2], {"id": "3", "nom": "Ecran", "prix": 180.0})
    def test_fichier_absent(self):
        chemin_inexistant = self.dossier / "introuvable.csv"
        with self.assertRaises(FichierIntrouvableException):
            charger_csv(chemin_inexistant)
    def test_prix_non_numerique(self):
        fichier = self.creer_fichier("prix_texte.csv", "1;Stylo;abc\n")
        with self.assertRaises(LigneInvalideException):
            charger_csv(fichier)
    def test_prix_negatif(self):
        fichier = self.creer_fichier("prix_negatif.csv", "1;Cahier;-10\n")
        with self.assertRaises(PrixNegatifException):
            charger_csv(fichier)
    def test_nombre_colonnes_invalide(self):
        fichier = self.creer_fichier("colonnes.csv", "1;Livre\n")
        with self.assertRaises(LigneInvalideException):
            charger_csv(fichier)

if __name__ == "__main__":
    unittest.main()