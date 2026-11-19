from csv_reader import (
    charger_csv,
    FichierIntrouvableException,
    LigneInvalideException,
    PrixNegatifException,
    CsvException,
)
def main():
    chemin_fichier = "articles.csv"

    try:
        articles = charger_csv(chemin_fichier)
        print("Articles charges avec succes :")
        for art in articles:
            print(f"  - [{art['id']}] {art['nom']} : {art['prix']} EUR")
    except FichierIntrouvableException as e:
        print("Erreur dans le fichier :", e)
    except LigneInvalideException as e:
        print("Erreur dans format de la ligne :", e)
    except PrixNegatifException as e:
        print("Erreur dans le prix :", e)
    except CsvException as e:
        print("Erreur dans CSV :", e)


if __name__ == "__main__":
    main()