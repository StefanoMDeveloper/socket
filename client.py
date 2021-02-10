#!/usr/bin/env python3


#input_string = 'Hello'  per commentare tutto ctrl+K e poi ctrl+C
#print(type(input_string))
#input_bytes_encoded = input_string.encode()
#print(type(input_bytes_encoded))
#print(input_bytes_encoded)
#output_string=input_bytes_encoded.decode()
#print(type(output_string))
#print(output_string)

import socket
import sys

SERVER_ADDRESS = '127.0.0.1'
SERVER_PORT = 22224

#La funzione ricve la socket connessa al server e la utilizza per richiedere il servizio
def invia_comandi(sock_service):
    
    while True:
        try:
            dati = input("Inserisci i dati da inviare (digita ko per uscire): ")
        except EOFError:
            print("\nOkay. Exit")
            break
        if not dati:
            print("Non puoi inviare una stringa vuota!")
            continue
        if dati == 'ko':
            print("Chiudo la connessione con il server!")
            break
    
        dati = dati.encode() #trasforma i dati in byte
        sock_service.send(dati) #invia i dati al server
        dati = sock_service.recv(2048)  #riceve i dati

        if not dati:
            print("Server non risponde. Exit")
            break
        
        dati = dati.decode()

        print("Ricevuto dal server:")
        print(dati)
    sock_service.close()

#La funzione crea una socket (s) per la connesione con il server e la passa alla funzione invia_comandi
def connessione_server(address, port):
    sock_service = socket.socket()
    sock_service.connect((address, port))
    print("Connesso a " + str((address, port)))
    invia_comandi(sock_service)
    

#Questa funzione consente al nostro codice di capire se stia venendo eseguito come script a se stante,
#o se è invece stato richiamato come modulo da un qualche programma per usare una o più delle sue varie fnzioni e classi.
if __name__ == '__main__':
    connessione_server(SERVER_ADDRESS, SERVER_PORT)


