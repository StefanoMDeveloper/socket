#!/usr/bin/env python3
import socket



SERVER_ADDRESS = '127.0.0.1'

SERVER_PORT = 22224

sock_listen = socket.socket()

sock_listen.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

sock_listen.bind((SERVER_ADDRESS, SERVER_PORT))

sock_listen.listen(5)

print("Server in ascolto su %s." % str((SERVER_ADDRESS, SERVER_PORT)))

protocollo=["SYN", "SYN + ACK", "ACK + Data", "ACK for Data"]

while True:
    sock_service, addr_client = sock_listen.accept()
    print("\nConnessione ricevuta da " + str(addr_client))
    print("\nAspetto di ricevere i dati ")
    step=0
    
    while True:
        
        dati = sock_service.recv(2048)
        if not dati:
            print("Fine dati dal client. Reset")
            break
        
        dati = dati.decode()
        step=int(dati)
        print("Ricevuto:" + str(step) + " - " + protocollo[step])
        
        step+=1
        dati= str(step)
        if dati > '3':
            dati = dati.encode()
            sock_service.send(dati)
            print("Inviato:" + str(step) + " - " + protocollo[step])
            print("Termino la connessione con il client.")
            break
        else:
            dati = dati.encode()
            sock_service.send(dati)
            print("Inviato:" + str(step) + " - " + protocollo[step])
            step+1
            dati = str(step)
            
            
        

    sock_service.close()