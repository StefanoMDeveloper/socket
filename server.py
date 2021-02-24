#!/usr/bin/env python3
from threading import Thread
import socket
# lasciando il campo vuoto sarebbe come localhost
SERVER_ADDRESS = '127.0.0.1'
#numero di porta, deve essere>1024 (perchè lealtre sono riservate).
SERVER_PORT = 22224

def ricevi_comandi(sock_service, addr_client):

    print("\nConnessione ricevuta da " + str(addr_client))
    print("\nAspetto di ricevere i dati ")

    while True:
        dati = sock_service.recv(2048)
        if not dati:
            print("Fine dati dal client. Reset")
            break

        dati = dati.decode()#decodifica i byte rievuti in una stringa unicode
        print("Ricevuto: '%s'" % dati)
        if dati=='ko':
            print("Chiudo la connessione con " + str(addr_client))
            break
        operazione, primo, secondo = dati.split(';')#serve per distinguere i dati inseriti nella stessa stringa
        if operazione == "piu" :
            risultato = int(primo) + int(secondo)
        if operazione == "meno" :
            risultato = int(primo) - int(secondo)
        if operazione == "per" :
            risultato = int(primo) * int(secondo)
        if operazione == "diviso" :
            if int(secondo)==0:
                print("Non è ossibile dividere per 0")
                break
            else:
                risultato = int(primo) / int(secondo)

        dati = "il risultato dell'operazione: " + operazione + " tra "+ primo+ " e "+ secondo+ " è: "+ str(risultato)
        dati = dati.encode()#codifica la stringa in byte
        sock_service.send(dati)#invia la risposta al client
    sock_service.close()#interrompe la connessione con il server

def avvia_server(indirizzo, porta ):
    try:
        #crea la socket
        sock_listen = socket.socket()
        #opzinale: permette di riavviare subito il codice
        #altrimenti bisognerebbe aspettare prima di poter riutilizzare 
        sock_listen.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        #associa indirizzo e porta. nota che l'argomento è una tupla:
        sock_listen.bind((indirizzo, porta))
        #imposta quante connessioni pendenti possono essere accodate
        sock_listen.listen(5)
        print("Server in ascolto su %s." % str((indirizzo, porta)))
    except socket.error as errore:
        print(f"Qualcosa è andato storto... \n{errore}")
    ricevi_connessioni(sock_listen)
    
def ricevi_connessioni(sock_listen):
    while True:
        sock_service, addr_client = sock_listen.accept()
        print("\nConnessione ricevuta da %s " % str(addr_client))
        print("Creo un thread per servire le richieste")
        try:
            Thread(target=ricevi_comandi, args=(sock_service, addr_client)).start()
        except:
            print("Il thread non si avvia")
            sock_listen.close()


if __name__ == '__main__':
    avvia_server(SERVER_ADDRESS,SERVER_PORT)
