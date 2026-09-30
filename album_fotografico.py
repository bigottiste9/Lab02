import csv

#funzione 1: carica l'album dal file

def carica_da_file(file_path):
    #questa funzione legge il file csv e crea la struttura
    #dati che rappresentano il nostro album
    #creo un dizionario vuoto
    #la chiave sarà l'anno
    #il valore sarà una lista di foto di quell'anno
    album = { }

    try:
        #apro il file in modalità lettura
        #encoding="utf-8" mi permette di leggere correttamente anche caratteri particolari
        with open(file_path, "r", newline="", encoding= "utf-8") as file:

            #DictReader legge ogni riga come un dizionario.
            #i nomi delle colonne sono quelli della prima riga
            lettore = csv.DictReader(file, skipinitialspace=True)
            #print(lettore.fieldnames)

            #scorro tutte le righe del file
            for riga in lettore:

                #leggo i dati della foto della riga
                codice = riga["codice"]
                titolo = riga["titolo"]
                autore = riga["autore"]

                #mese e anno devono essere numeri, quindi li trasformo da stringa ad intero
                mese = int(riga["mese"])
                anno = int(riga["anno"])

                #creo un dizionario che rappresenta una foto
                foto = {
                    "codice": codice,
                    "titolo": titolo,
                    "autore": autore,
                    "mese": mese,
                    "anno": anno,
                }

                #controllo se l'anno è gia presente nell'album
                if anno not in album:

                    #se non è presente creo una nuova lista per contenere le foto di quell'anno
                    album[anno]= []

                #aggiungo la foto alla lista dell'anno
                album[anno].append(foto)

        #restituisco l'album completo
        return album
    #se il file non esiste, viene generata questa eccezione
    except FileNotFoundError:

        #restituisco none, come richiesto dalla consegna
        return None

#funzione 2: aggiunge una nuova foto

def aggiungi_foto(album, codice, titolo, autore, mese, anno, file_path):

    #controllo che il mese sia compreso tra 1 e 12
    if mese < 1 or mese > 12:
        return None

    #controllo che il codice non sia già presente, perchè identifica una foto
    for anno_album in album:

        #scorro tutte le foto di quell'anno
        for foto in album[anno_album]:

            #se trovo lo stesso codice, la foto esiste già.
            if foto["codice"] == codice:
                return None

    #creo il dizionario che rappresenta la nuova foto
    foto= {
        "codice": codice,
        "titolo": titolo,
        "autore": autore,
        "mese": mese,
        "anno": anno,
    }

    #controllo se l'anno è gia presente nell'album
    if anno not in album:

        #se l'anno non esiste, creo una nuova lista
        album[anno] = []

    #aggiungo la nuova foto alla struttura dati
    album[anno].append(foto)

    #ora devo aggiornare anche il file csv
    #"a" significa append, cioè aggiungo in fondo senza cacellare il contenuto precedente.
    with open(file_path, "a", newline="", encoding= "utf-8") as file:

        #creo lo scrittore del file csv
        scrittore= csv.writer(file)

        #scrivo la nuova riga.
        scrittore.writerow([
            codice,
            titolo,
            autore,
            mese,
            anno
        ])

    #se tutto è andato bene, restituisco la foto aggiunta
    return foto

#funzione 3 : cerca una foto tramite un codice

def cerca_foto(album, codice):
    #scorro tutti gli anni presenti nell'album
    for anno in album:

        #scorro tutte le foto di quell'anno
        for foto in album[anno]:

            #controllo se il codice della foto corrisponde a quello cercato
            if foto["codice"] == codice:

                #se trovo una foto restituisco una stringa con tutte le sue info
                return f'{foto["codice"]}, {foto["titolo"]}, {foto["autore"]}, {foto["mese"]}, {foto["anno"]}'

    #se arrivo qui significa che non ho trovto la foto
    return None

#funzione 4: elenco le foto di un anno ordinato in modo alfabetico per il titolo

def elenco_foto_anno_per_titolo(album, anno):

    #controllo se l'anno è presente nell'album
    if anno not in album:

        #se non esiste:
        return None

    #creo una lista vuota dove inserire i titoli
    titoli = []

    #scorro tutte le foto dell'anno richiesto
    for foto in album[anno]:

        #aggiungo alla lista il titolo della foto
        titoli.append(foto["titolo"])

    #ordino alfabeticamente la lista
    titoli.sort()

    #restituisco la lista ordinata
    return titoli

#funzione main

def main():
    album = {}
    file_path = "album_fotografico.csv"

    #il menu deve essere mostrato continuamente, quindi utilizzo un ciclo infinito
    while True:
        print("\n--- MENU ALBUM FOTOGRAFICO ---")
        print("1. Carica album da file")
        print("2. Aggiungi una nuova foto")
        print("3. Cerca una foto per codice")
        print("4. Elenco foto di un anno (ordinato per titolo)")
        print("5. Esci")

        #chiedo all'utente quale operazione vuole eseguire
        scelta = input("Scegli un'opzione >> ").strip()

#opzione 1: carica l'album

        if scelta == "1":

            #continuo a chiedere il file finche non ne trovo uno valido
            while True:
                file_path = input("Inserisci il path del file da caricare: ").strip()

                #chiamo la funzione che legge il file
                album = carica_da_file(file_path)

                #se l'album non è None significa che il file è stato trovato e caricato correttamente
                if album is not None:
                    print("Album caricato con successo!")
                    break

                #se arrivo qui il file non è stato trovato
                print("Errore: file non trovato.")

        #opzione 2: aggiungi una foto

        elif scelta == "2":

            #non posso aggiungere una foto se prima non ho caricato l'album
            if not album:
                print("Prima carica l'album da file.")
                continue

            #chiedo i dati della nuova foto
            codice = input("Codice della foto: ").strip()
            titolo = input("Titolo: ").strip()
            autore = input("Autore: ").strip()

            #mese e anno devono essere numeri per quello che utilizzo try e except
            try:
                mese = int(input("Mese (1-12): ").strip())
                anno = int(input("Anno: ").strip())

            #se l'utente inserisce qualcosa diverso d aun numero, viene generato ValueError
            except ValueError:
                print("Errore: inserire valori numerici validi per mese e anno.")
                continue

            #chiamo la funzione che aggiunge la foto
            foto = aggiungi_foto(album, codice, titolo, autore, mese, anno, file_path)

            #se la funzione restituisce una foto significa che l'inserimento è riuscito
            if foto:
                print(f"Foto aggiunta con successo!")

            #se restituisce None qualcosa è adato storto
            else:
                print("Non è stato possibile aggiungere la foto.")

        #opzione 3: cerca una foto

        elif scelta == "3":

            #controllo che l'album non sia vuoto
            if not album:
                print("L'album è vuoto.")
                continue

            #chiedo il codice della foto
            codice = input("Inserisci il codice della foto da cercare: ").strip()

            #chiamo la funzione cerca_foto
            risultato = cerca_foto(album, codice)

            #se il risultato non è None, la foto è stata trovata
            if risultato:
                print(f"Foto trovata: {risultato}")
            else:
                print("Foto non trovata.")

        #opzione 4: elenco foto di un anno

        elif scelta == "4":
            #controllo che l'album non sia vuoto
            if not album:
                print("L'album è vuoto.")
                continue

            #l'anno deve essere un numero
            try:
                anno = int(input("Inserisci l'anno da consultare: ").strip())
            except ValueError:
                print("Errore: inserire un valore numerico valido.")
                continue

            #chiamo la funzione che restituisce i titoli ordinati alfabeticamente
            titoli = elenco_foto_anno_per_titolo(album, anno)

            #se l'anno esiste, titoli sarà una lista
            if titoli is not None:
                print(f'\nFoto del {anno}:')

                #stampo ogni titolo della lista
                for titolo in titoli:
                    print(f'- {titolo}')

            #se l'anno non esiste
            else:
                print(f"Nessuna foto trovata per l'anno {anno}.")

        #opzione 5: esci

        elif scelta == "5":
            print("Uscita dal programma...")

            #break interrompe il while True e quindi termina il programma
            break

        #scelta non valida

        else:
            print("Opzione non valida. Riprova.")


#avvio del programma

#questo controlla che il file venga eseguito direttamente
if __name__ == "__main__":
    main()
