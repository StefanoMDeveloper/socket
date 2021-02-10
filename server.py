#!/usr/bin/env python3
import socket

SERVER_ADDRESS = '127.0.0.1'

SERVER_PORT = 22224

def ricevi_comandi(sock_listen):
    
    while True:
        sock_service, addr_client = sock_listen.accept()
        print("\nConnessione ricevuta da " + str(addr_client))
        print("\nAspetto di ricevere i dati ")
        contConn=0
        while True:
            dati = sock_service.recv(2048)
            contConn+=1
            if not dati:
                print("Fine dati dal client. Reset")
                break
            
            dati = dati.decode()
            print("Ricevuto: '%s'" % dati)
            if dati=='ko':
                print("Chiudo la connessione con " + str(addr_client))
                break
            operazione, primo, secondo = dati.split(';')

            if operazione == 'piu':
                risultato = int(primo)+int(secondo)
            if operazione == 'meno':
                risultato = int(primo)-int(secondo)
            if operazione == 'per':
                risultato = int(primo)*int(secondo)
            if operazione == 'diviso':
                if int(secondo)==0:
                    print("Non è ossibile dividere per 0")
                    break
                else:
                    risultato = int(primo)/int(secondo)

            dati ="il risultato dell'operazione: " +operazione+" tra "+primo+" e "+secondo+" è: "+str(risultato)

            dati = dati.encode()

            sock_service.send(dati)
        sock_service.close()

def avvia_server(indirizzo, porta):
    sock_listen = socket.socket()
    sock_listen.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock_listen.bind((indirizzo, porta))
    sock_listen.listen(5)
    print("Server in ascolto su %s." % str((indirizzo, porta)))
    ricevi_comandi(sock_listen)

if __name__ == '__main__':
    avvia_server(SERVER_ADDRESS, SERVER_PORT)
