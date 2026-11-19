from datetime import datetime

class ReservationException(Exception):
    def __init__(self, message):
        super().__init__(message)
class CapaciteDepasseeException(ReservationException):
    pass
class NombreInvalideException(ReservationException):
    pass
class NomClientInvalideException(ReservationException):
    pass
class Evenement:
    def __init__(self, nom, capacite):
        self.nom = nom
        self.capacite = capacite
        self.places_reservees = 0
        self.reservations = []    
        self.file_attente = []      
        self.compteur_id = 1

    def generer_id_client(self):
        id_client = f"CLI-{self.compteur_id}"
        self.compteur_id += 1
        return id_client

    def logger(self, statut, message):
        date_actuelle = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open("reservations.log", "a", encoding="utf-8") as f:
            f.write(f"[{date_actuelle}] [{statut}] {self.nom} : {message}\n")

    def reserver(self, nom_client, nb_places):
        try:
            if not nom_client.strip():
                raise NomClientInvalideException("Nom du client requis invalide.")
            if nb_places <= 0:
                raise NombreInvalideException("Nombre de places est invalide.")
            if self.places_reservees + nb_places > self.capacite:
                self.file_attente.append((nom_client.strip(), nb_places))
                self.logger(
                    "FILE_ATTENTE",
                    f"{nom_client.strip()} ({nb_places} places) ajoute en file d'attente."
                )
                raise CapaciteDepasseeException("Capacite depassee. Ajoute en file d'attente.")

            id_client = self.generer_id_client()
            self.places_reservees += nb_places
            self.reservations.append({
                "id": id_client,
                "client": nom_client.strip(),
                "places": nb_places
            })

            message = f"Reservation confirmee pour {nom_client.strip()} [{id_client}] ({nb_places} places)."
            print(message)
            self.logger("SUCCES", message)
            return id_client

        except ReservationException as e:
            self.logger("ERREUR", str(e))
            raise

    def afficher(self):
        print(f"Evenement: {self.nom} — {self.places_reservees}/{self.capacite} places reservees")
        if self.reservations:
            print("Les Reservations confirmees:")
            for r in self.reservations:
                print(f"  - [{r['id']}] {r['client']} : {r['places']} place(s)")
        if self.file_attente:
            print("File d'attente:")
            for client, nb in self.file_attente:
                print(f"  - {client} : {nb} place(s)")

event = Evenement("Concert", 5)

for client, places in [("Sara", 6), ("Youssef", 4), ("", 1), ("Nadia", 2)]:
    try:
        event.reserver(client, places)
    except ReservationException as e:
        print("Erreur:", e)
event.afficher()