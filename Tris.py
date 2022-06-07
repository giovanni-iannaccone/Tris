import pyfiglet
import os
import socket, subprocess
import sys

from random import choice
from rich.console import Console
from time import sleep

def introduzione():
    os.system("cls" if os.name == "nt" else "clear")
    print(" TRIS ".center(86, "="))
       
def chiusura(client):
    console.print("\n" + choice(["Ok, alla prossima  ಥ _ ಥ", "Uffa, ci vediamo இ ௰ இ", "Va bene, vorrà dire che mi riposerò un po' (._. )", "Mi mancherai （；´д｀）ゞ",
                         "Ne sei proprio sicuro ? o(￣┰￣*)ゞ", "Peccato, mi stavo divertendo tanto o(TヘTo)", "Ok, quando vuoi io sono qui ┻━┻ ︵ヽ(`Д´)ﾉ",
                         "E' sempre triste vederti andare via (;´༎ຶД༎ຶ`)", "Spero di rivederti presto ┗( T﹏T )┛", ""]), style="bold red")
    if client != None:
        client.close()
    sleep(2)
    sys.exit()

def ascii_art():
    ascii_art = pyfiglet.figlet_format("O TRIS X")
    console.print(ascii_art, style="bold green")
    console.print("X O " * 10, style="bold green")
    sleep(3)
    
#################################################################### Port Scanner ####################################################################

def scan_port(ip):
    OPEN_PORTS = []
    for porte in range(65535):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1.0)
        introduzione()
        print(f"Sto scansionando {ip}:{porte}")
        conn_status = sock.connect_ex((ip, porte))
        if conn_status == 0:
            OPEN_PORTS.append(porte)
        sock.close()

    return OPEN_PORTS

#################################################################### Port Scanner ####################################################################

class Tris:
    
    def __init__(self):
        self.board = []
        self.simbolo = None
        self.giocatore1 = None
        self.giocatore2 = None

    def crea_tabella(self):
        self.board = []
        for i in range(3):
            row = []
            for j in range(3):
                row.append("-")
            self.board.append(row)
            
    def fix_spot(self, row, col, esecuzione):
        if self.board[row - 1][col - 1] == "-" and esecuzione == True:
            self.board[row - 1][col - 1] = self.simbolo
            return True
        elif self.board[row - 1][col - 1] == "-" and esecuzione == False:
            return True
        else:
            return False

    def vittoria(self, player):
        win = None

        n = len(self.board)

        for i in range(n):
            win = True
            for j in range(n):
                if self.board[i][j] != self.simbolo:
                    win = False
                    break
            if win:
                return win

        for i in range(n):
            win = True
            for j in range(n):
                if self.board[j][i] != self.simbolo:
                    win = False
                    break
            if win:
                return win

        win = True
        for i in range(n):
            if self.board[i][i] != self.simbolo:
                win = False
                break
        if win:
            return win

        win = True
        for i in range(n):
            if self.board[i][n - 1 - i] != self.simbolo:
                win = False
                break
        if win:
            return win
        return False

        for row in self.board:
            for oggetti in row:
                if oggetti == "-":
                    return False
        return True

    def tabella_piena(self):
        for row in self.board:
            for oggetti in row:
                if oggetti == "-":
                    return False
        return True
    
    def cambio_turno(self, player, nome_giocatore2):
        if nome_giocatore2 == None:
            return self.giocatore1 if player == self.giocatore2 else self.giocatore2
        else:
            return self.giocatore1 if player == nome_giocatore2 else nome_giocatore2

    def mostra_tabella(self):
        for row in self.board:
            for oggetti in row:
                console.print(oggetti, end=" ", style="bold blue")
            print()

    def ricevi_tabella(self, client):
        print("sto ricevendo la tabella ... ")
        n = len(self.board)
        for i in range(n):
            for j in range(n):
                self.board[i][j] = client.recv(sys.getsizeof("-")).decode()

    def manda_tabella(self, client, pausa):
        print("sto mandando la tabella ...")
        n = len(self.board)
        sleep(1)
        for i in range(n):
            for j in range(n):
                sleep(pausa)
                client.send(self.board[i][j].encode())

    def primo_giocatore_casuale(self):
        try:
            while self.giocatore1 == self.giocatore2:
                introduzione()
                if modalita in ("A", "a"):
                    self.giocatore1 = str(console.input("Inserisci il nome del primo giocatore ([bold blue]X[/bold blue]): "))
                    self.giocatore2 = str(console.input("Inserisci il nome del secondo giocatore ([bold red]O[/bold red]): "))
                else:
                    self.giocatore1 = str(input("Come ti chiami ? "))
                    self.giocatore2 = "computer" if modalita in ("B", "b") else None
                    
                if self.giocatore1 == self.giocatore2:
                    print("\nI nomi dei due giocatori non possono essere uguali\n")                
        except KeyboardInterrupt:
            tris.ricomincia_o_fine(None, None)
                
        return choice([self.giocatore1, self.giocatore2])

    def ricomincia_o_fine(self, testo, client):
        try:
            introduzione()
            if testo == None:
                risposta = input("Siete sicuri di voler uscire ? s/n " if modalita in ("A", "a") else "Sei sicuro di voler uscire ? s/n ")
                if risposta in ("S", "s"):
                    chiusura(client)
                else:
                    risposta = input("\nVolete ricominciare ? s/n " if modalita in ("A", "a") else "\nVuoi ricominciare ? s/n ")
                if risposta in ("S", "s"):
                    self.crea_tabella()
                else:
                    return risposta
            else:
                print(testo)
                risposta = input("Partita finita, volete ricominciare ? s/n " if modalita in ("A", "a") else "Partita finita, vuoi ricominciare ? s/n ")
                self.crea_tabella() if risposta in ("S", "s") else chiusura(client)
                
        except KeyboardInterrupt:
            tris.ricomincia_o_fine(None, None)
        
    def mossa_computer(self, esecuzione, difficolta, valido = True):
        if difficolta == 1:
            row, col = choice([ 1, 2, 3 ]), choice([ 1, 2, 3 ])
            valido = self.fix_spot(row,  col, esecuzione)
            if not valido:
                while not valido:
                    row, col = choice([ 1, 2, 3 ]), choice([ 1, 2, 3 ])
                    valido = self.fix_spot(row,  col, esecuzione)
            return row, col, valido

        else:
            n = len(self.board)
            spazi_liberi = 0
            row, col = None, None
            for row in self.board:
                for oggetti in row:
                    if oggetti == "-":
                        spazi_liberi += 1
            if spazi_liberi > 6:
                row, col = 2, 2
                valido = self.fix_spot(row,  col, esecuzione)
                if valido == False:
                    row, col = choice([ 1, 2, 3 ]), choice([ 1, 2, 3 ])
                    valido = self.fix_spot(row,  col, esecuzione)
                
                if valido:                                
                    return row, col, valido

            for h in range(1, 2):
                simbolo = self.simbolo if h == 1 else "X"
                for i in range(n):
                    for j in range(n):
                        l = 0
                        if self.board[i][j] == simbolo:
                            l += 1 
                            if l == 2:
                                for k in range(n):
                                    row, col = i+1, k + 1                                       
                                    valido = self.fix_spot(row,  col, esecuzione)
                                    if valido:
                                        return row, col, valido

            for h in range(1, 2):
                simbolo = self.simbolo if h == 1 else "X"                                   
                for j in range(n):
                    l = 0
                    for i in range(n):
                        if self.board[i][j] == simbolo:
                            l += 1 
                            if l == 2:
                                for k in range(n):
                                    row, col = j + 1, k + 1           
                                    valido = self.fix_spot(row,  col, esecuzione)
                                    if valido:
                                        return row, col, valido
                        
            for h in range(1, 2):
                simbolo = self.simbolo if h == 1 else "X"                                
                for i in range(n):
                    i = j
                    for k in range(n):
                        l = 0
                        if self.board[i][j] == simbolo:
                            l += 1
                            if l == 2:
                                for m in range(n):
                                    row, col = i + 1, j + 1
                                    valido = self.fix_spot(row, col, esecuzione)
                                    if valido:    
                                        return row, col, valido

            for h in range(1, 2):
                simbolo = self.simbolo if h == 1 else "X"
                row, col = 1, 3
                for k in range(3):
                    valido = self.fix_spot(row, col, esecuzione)
                    if valido:    
                        return row, col, valido
                    else:
                        row += 1
                        col -= 1
                        
            if row == None and col == None:
                while valido != True:
                    row, col = choice([ 1, 2, 3 ]), choice([ 1, 2, 3 ])
                    valido = self.fix_spot(row,  col, esecuzione)
                return row, col
                    
    def preparazione_partita(self):
        try:
            risposta, opzione = None, None
            introduzione()
            while risposta not in (1, 2):
                risposta = int(input("\t-1 se vuoi cercare partita a cui connetterti\n\t-2 se vuoi creare una nuova partita\nInserisci: "))

            introduzione()
            if risposta == 1:
                client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                try:
                    while opzione not in (1, 2):
                        opzione = int(input("\t-1 se cerchi una stanza in particolare\n\t-2 se vuoi attivare una ricerca casuale di una partita disponibile\nInserisci: "))

                    introduzione()
                    if opzione == 1:
                        ip, porta = "", 65536
                        try:
                            while not ip.count("."):
                                ip = str(input("Inserisci l'ip del server della partita: "))
                        except ValueError:
                            ip = "127.0.0.1"
                        while porta > 65535:
                            porta = int(input("Inserisci la porta del server della partita: "))
                            if porta > 65535:
                                print("Le porte arrivano fino a 65535, reinserisci")
                        client.connect((ip, porta))
                            
                    else:
                        print("\t\t\t\t   -- ATTENZIONE --\n\t\tLA SCANSIONE POTREBBE ESSERE POTENZIALMENTE ILLEGALE,",
                                        "\n\t\t\tIO NON MI ASSUMO ALCUNA RESPONSABILITA'")
                        while opzione not in ("S", "s", "N", "n"):
                            opzione = str(input("\nLa scansione potrebbe richiedere molto tempo, sei sicuro di voler continuare ? s/n "))
                        if opzione in ("S", "s"):
                            global lista_ip
                            lista_ip = [] 
                            output = subprocess.run(("arp -a"), capture_output=True, text=True)
                            output = list((output.stdout).split())
                            for ip in output:
                                if bool(ip.count(".")):
                                    lista_ip.append(ip)
                            
                            for ip in lista_ip:
                                OPEN_PORTS = scan_port(ip)
                                for porta in OPEN_PORT:
                                    client.connect(ip, porta )
                                    if risposta == 1:
                                        if client.recv(2048).decode() != "Connesso":
                                            OPEN_PORTS.pop(0)
                                            continue
                                    else:
                                        client.send("Connesso".encode())
                                    
                                
                except TimeoutError or ConnectionRefusedError:
                    print("\nServer inesistente nella tua rete")
                    sleep(2)
                    sys.exit(1)
                
            else:
                porta = 65536
                ip = str(socket.gethostbyname(socket.gethostname()))
                while opzione not in ("S", "s", "N", "n"):
                    opzione = input(f"Il tuo indirizzo ip è {ip}, vuoi usare questo come ip del server ? s/n ")
                if opzione in ("N", "n"):
                    try:
                        ip = ""
                        while not ip.count("."):
                            ip = str(input("Inserisci l'indirizzo ip che vuoi usare: "))
                            if not ip.count("."):
                                print("Indirizzo ip non valido")
                    except ValueError:
                        ip = "127.0.0.1"
                while porta > 65535:
                    porta = int(input("Inserisci la porta del server della partita: "))
                    if porta > 65535:
                        print(f"Le porte arrivano fino a {porta}, reinserisci")
                try:
                    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                    client.bind((ip, porta))
                    client.listen(1)
                    introduzione()
                    console.print(f"-IP: \t[bold blue]{ip}[/bold blue]")
                    console.print(f"-Porta: [bold blue]{porta}[/bold blue]")
                    print("\nIn attesa che qualcuno si connetta ( potrebbe volerci un po' ) ...")

                except Exception as e:
                    console.print(f"Errore durante la creazione del server: [bold red]{e}[/bold red]")
                    sleep(2)
                    sys.exit(1)

                utente, addr = client.accept()
                if risposta == 1:
                    utente.send("Connesso".encode())
        
            testo, j, frase_finale = "Partita trovata", 3, "VIA !!!"
            for i in range(5):
                introduzione()
                print(testo)
                testo = (f"{testo} ... {j if j > 0 else frase_finale}")
                sleep(1)
                j -= 1

        except ConnectionRefusedError:
            console.print("\nServer inesistente nella tua rete", style="bold red")
            sleep(2)
            sys.exit(1)

        except KeyboardInterrupt:
            tris.ricomincia_o_fine(None, None)
        
        return risposta, (utente if risposta != 1 else client)

    def due_giocatori(self, player):
        self.crea_tabella()
        if self.giocatore1 == self.giocatore2:
            self.primo_giocatore_casuale()
        punti_a, punti_b = 0, 0
        
        while True:
            try:
                if player == None:
                    player = choice([self.giocatore1, self.giocatore2])
            
                introduzione()
                print(f"{self.giocatore1}: {punti_a}".center(43 - (len(self.giocatore1)+len(str(punti_a))), " "), f"{self.giocatore2}: {punti_b}".center(43 - (len(self.giocatore1)+len(str(punti_a))), " "))

                valido = False

                self.simbolo = "X" if player == self.giocatore1 else "O"

                while valido != True:
                        
                    print(f"E' il turno di {player}")
                    self.mostra_tabella()
                    row, col = list(map(int, input(f"{player}, inserisci la riga e la colonna in cui vuoi inserire {self.simbolo}: ").split()))

                    valido = self.fix_spot(row, col, True)
                    if not valido:
                        print(f"{row} {col} è già occupata, riprova")            
        
                    if self.vittoria(player):
                        tris.ricomincia_o_fine(f"{player.upper()} HA VINTO", None)
                        if player == self.giocatore1:
                            punti_a += 1
                        else:
                            punti_b += 1
                        
                    if self.tabella_piena():
                        tris.ricomincia_o_fine("Pareggio!", None) 

                    player = self.cambio_turno(player, None)
           
            except (IndexError and ValueError) or ValueError:
                print("\nInserisci due valori interi compresi tra 1 e 3 separati da uno spazio\nes: 1 2")
                sleep(2)

            except IndexError:
                print("\nInserisci due valori interi compresi tra 1 e 3 separati da uno spazio\nes: 1 2")
                sleep(2)

            except KeyboardInterrupt:
                tris.ricomincia_o_fine(None, None) 
                
    def vs_computer(self, player):
        self.crea_tabella()
        if self.giocatore1 is self.giocatore2:
            self.primo_giocatore_casuale()
        punti_a, punti_b, aiuti, difficolta = 0, 0, 1, None

        introduzione()
        print("      In questa modalità avrai a disposizione un aiuto, premi CTRL-C per usarlo")
        sleep(3)
        while difficolta not in (1, 2):
            introduzione()
            print("\t-1 per la modalità facile")
            print("\t-2 per la modalita difficile")
            difficolta = int(input("Inserisci: "))

        if difficolta == 1:
            player = self.giocatore1

        while True:
            try:
                if player == None:
                    player = choice([self.giocatore1, self.giocatore2])
                introduzione()
                print(f"{self.giocatore1}: {punti_a}".center(43 - (len(self.giocatore1)+len(str(punti_a))), " "), f"{self.giocatore2}: {punti_b}".center(43 - (len(self.giocatore1)+len(str(punti_a))), " "))

                self.mostra_tabella()
                valido = False

                self.simbolo = "X" if player == self.giocatore1 else "O"

                while valido != True:
                    
                    if player == self.giocatore1:
                        row, col = list(map(int, input(f"E' il tuo turno, inserisci la riga e la colonna in cui vuoi inserire {self.simbolo}: ").split()))
                        valido = self.fix_spot(row, col, True)
                        if not valido:
                            print(f"La posizione {row} {col} è già occupata, riprova")                        
                    else:
                        try:
                            row, col, valido = self.mossa_computer(True, difficolta)
                        except TypeError:
                            row, col = choice([1, 2, 3]), choice([1, 2, 3])
                            valido = self.fix_spot(row, col, True)
                        print(f"E' il mio turno, inserisco {self.simbolo} in {row}, {col}")

                if player == self.giocatore2:
                    sleep(2)
                        
                if self.vittoria(player):
                    testo = "mi dispiace, hai perso ... ahahah un giorno i robot domineranno il mondo" if player == self.giocatore2 else f"complimenti {player}, hai vinto"
                    tris.ricomincia_o_fine(testo, None)
                    if player == self.giocatore1:
                        punti_a += 1
                    else:
                        punti_b + 1

                if self.tabella_piena():
                    tris.ricomincia_o_fine("Pareggio!", None)

                player = self.cambio_turno(player, None)

            except (IndexError and ValueError) or IndexError:
                print("\nInserisci due valori interi compresi tra 1 e 3 separati da uno spazio\nes: 1 2")
                sleep(2)

            except ValueError:
                print("\nInserisci due valori interi compresi tra 1 e 3 separati da uno spazio\nes: 1 2")
                sleep(2)

            except KeyboardInterrupt:
                introduzione()
                if aiuti == 1 and player == self.giocatore1:
                    risposta = input("Hai bisogno di un suggerimento ? s/n ")
                    if risposta in ("S", "s"):
                        while valido != True:
                            try:
                                row, col, valido = self.mossa_computer(True, difficolta = 2)
                            except TypeError:
                                row, col = choice([1, 2, 3]), choice([1, 2, 3])
                                valido = self.fix_spot(row, col, True)
                        print(f"Mmh, fammici pensare ... suggerico di inserire {self.simbolo} in {row if row in (1, 2, 3) else row + 1} {col if col in (1, 2, 3) else col + 1}")
                        print("Adesso non hai più aiuti a disposizione")
                        sleep(2)
                        aiuti = 0
                    else:
                        tris.ricomincia_o_fine(None, None)
                else:
                    tris.ricomincia_o_fine(None, None)
                
    def gioca_online(self, player):
        risposta, client = self.preparazione_partita()
        try:
            if risposta == 1:
                nome_giocatore2 = client.recv(2048).decode()
                while self.giocatore1 == nome_giocatore2 and risposta == 1:
                    print("I nomi dei due giocatori non possono essere uguali")
                    self.giocatore1 = input("Inserisci un altro nome: ")
                client.send(self.giocatore1.encode())
                player = client.recv(2048).decode()
            else:
                client.send(self.giocatore1.encode())
                nome_giocatore2 = client.recv(2048).decode()
                client.send((player if player == self.giocatore1 else nome_giocatore2).encode())

            self.crea_tabella()

            punti_a, punti_b, pausa = 0, 0, 0.5
            while True:
                if player == None:
                    player = choice([self.giocatore1, nome_giocatore2])
                    if player == self.giocatore1:
                        client.send(player.encode())
                    else:
                        player = client.recv(2048).decode()

                introduzione()
                self.ricevi_tabella(client) if player == self.giocatore1 else self.manda_tabella(client, pausa)
                print(f"{self.giocatore1}: {punti_a}".center(43 - (len(self.giocatore1)+len(str(punti_a))), " "), f"{nome_giocatore2}: {punti_b}".center(43 - (len(self.giocatore1)+len(str(punti_a))), " "))
                valido = False

                self.simbolo = "X" if risposta != 1 else "O"
                sleep(pausa)
                while valido != True:    

                    if player == self.giocatore1:
                        introduzione()
                        self.mostra_tabella()
                        row, col = list(map(int, input(f"E' il tuo turno, inserisci la riga e la colonna in cui vuoi inserire {self.simbolo}: ").split()))
                        valido = self.fix_spot(row, col, True)
                        if not valido:
                            print(f"La posizione {row} {col} è già occupata, riprova")
                            sleep(2)
                    else:
                        try:
                            introduzione()
                            self.mostra_tabella()
                            print("Il tuo avversario sta ancora scegliendo ... ")
                            sleep(0.5)
                            dimensione_messaggio = sys.getsizeof("X")
                            if client.recv(dimensione_messaggio).decode():
                                break
                        except:
                            continue

                if player == self.giocatore1:
                    sleep(pausa)
                    client.send("X".encode())

                if player == self.giocatore1:
                    if self.vittoria(player):
                        sleep(pausa)
                        client.send("V".encode())
                        tris.ricomincia_o_fine(f"{player.upper()}, HAI VINTO", client)
                        if player == nome_giocatore2:
                            punti_a += 1
                        else:
                            punti_b += 1
                    elif self.tabella_piena():
                        client.send("P".encode())
                        tris.ricomincia_o_fine("Pareggio !", client)
                    else:
                        client.send("-".encode())

                else:
                    messaggio = client.recv(2048).decode()
                    if messaggio == "V":
                        self.ricomincia_o_fine("Mi dispiace, hai perso", client)
                    elif messaggio == "P":
                        tris.ricomincia_o_fine("Pareggio !", client)

                player = self.cambio_turno(player, nome_giocatore2)                  

        except (IndexError and ValueError) or ValueError:
            print("\nInserisci due valori interi compresi tra 1 e 3 separati da uno spazio\nes: 1 2")
            sleep(2)

        except IndexError:
            print("\nInserisci due valori interi compresi tra 1 e 3 separati da uno spazio\nes: 1 2")
            sleep(2)

        except UnboundLocalError:
            print("Il programma non ha i dati necessari per partire, è in corso il riavvio dell'applicazione ... ＞﹏＜")
            sleep(1)
            self.gioca_online(player)

        except ConnectionResetError or ConnectionAbortedError:
            print("Mi dispiace ma il tuo avversario potrebbe aver abbandonato la partita, questo significa che hai vinto ... credo")
            sleep(2)

        except KeyboardInterrupt:
            tris.ricomincia_o_fine(None, client)

    def inizio(self):
        try:
            ascii_art()
            global modalita
            modalita = None
            introduzione()
                
            while modalita not in ("A", "a", "B", "b", "C", "c"):
                modalita = input("\t-A per la modalità due giocatori\n\t-B per la modalità contro il computer\n\t-C per la modalità online\nInserisci: ")

            introduzione()
            console.print("      Durante il gioco, premi [bold blue]CTRL-C[/bold blue] per terminare la partita o ricominciarla")    
            sleep(3)
            player = self.primo_giocatore_casuale()

            if modalita in ("A", "a"):
                self.due_giocatori(player)
            elif modalita in ("B", "b"):
                self.vs_computer(player)
            else:
                self.gioca_online(player)

        except KeyboardInterrupt:
            if tris.ricomincia_o_fine(None, None) in ("N", "n"):
                self.inizio()

if __name__ == "__main__":
    console = Console()
    tris = Tris()      
    tris.inizio()
