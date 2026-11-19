from datetime import datetime

class TransactionException(Exception):
    def __init__(self, message):
        super().__init__(message)
class MontantNegatifException(TransactionException):
    def __init__(self, message="Le montant doit etre positif."):
        super().__init__(message)
class SoldeInsuffisantException(TransactionException):
    def __init__(self, message="Pour ce retrait, le solde est insuffisant."):
        super().__init__(message)

class CompteBancaire:
    def __init__(self, nom, solde=0):
        self.nom = nom
        self.solde = solde

    def enregistrer_erreur(self, message):
        date_actuelle = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open("erreurs.log", "a", encoding="utf-8") as fichier:
            fichier.write(f"[{date_actuelle}] Compte {self.nom} : {message}\n")

    def deposer(self, montant):
        try:
            if montant <= 0:
                raise MontantNegatifException("Impossible de deposer un montant qui est negatif ou nul.")
            self.solde += montant
        except MontantNegatifException as e:
            self.enregistrer_erreur(str(e))
            raise

    def retirer(self, montant):
        try:
            if montant <= 0:
                raise MontantNegatifException("Le montant doit etre positif.")
            if montant > self.solde:
                raise SoldeInsuffisantException("Pour ce retrait, le solde est insuffisant.")
            self.solde -= montant
        except TransactionException as e:
            self.enregistrer_erreur(str(e))
            raise

    def afficher(self):
        print(f"Compte: {self.nom}, Solde: {self.solde}€")

try:
    compte = CompteBancaire("Kawtar", 540)
    compte.afficher()

    compte.retirer(210)
    compte.deposer(-14)

except TransactionException as e:
    print("Erreur c'est produite:", e)