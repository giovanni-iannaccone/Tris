from os import *
from random import choice
from time import sleep


def pulisci_schermo():
    system("cls" if name == "nt" else "clear")


def introduzione():
    pulisci_schermo()
    print(" TRIS ".center(86, "="))

       
def chiusura():
    print(choice(["\nOk, alla prossima  :(", "\nUffa, ci vediamo இ ௰ இ", "\nVa bene, vorrà dire che mi riposerò un po' (。_。)"]))
    sleep(2)
    exit()

        
class Tris:
    

    def __init__(self):
        self.board = []
        self.simbolo = None


    def crea_tabella(self):
        self.board = []
        for i in range(3):
            row = []
            for j in range(3):
                row.append("-")
            self.board.append(row)
            

    def fix_spot(self, row, col):
        if self.board[row - 1][col - 1] == "-":
            self.board[row - 1][col - 1] = self.simbolo
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
    

    def cambio_turno(self, player):
        return giocatore1 if player == giocatore2 else giocatore2


    def mostra_tabella(self):
        for row in self.board:
            for oggetti in row:
                print(oggetti, end = " ")
            print()


    def primo_giocatore_casuale(self, modalita):
        global giocatore1, giocatore2
        giocatore1, giocatore2 = None, None
        try:
            while giocatore1 is giocatore2:
                introduzione()
                if modalita in ("A", "a"):
                    giocatore1 = input("Inserisci il nome del primo giocatore (X): ")
                    giocatore2 = input("Inserisci il nome del secondo giocatore (O): ")
                else:
                    giocatore1 = input("Come ti chiami ? ")
                    giocatore2 = "computer"
                if giocatore1 == None or giocatore2 == None:
                    if giocatore1 == None:
                        giocatore1 = "None" 
                    else:
                        giocatore2 = "None"
                        
                if giocatore1 is giocatore2:
                    print("\nI nomi dei due giocatori non possono essere uguali\n")
                
        except KeyboardInterrupt:
            tris.ricomincia_o_fine(None)
                
        return choice([giocatore1, giocatore2])


    def ricomincia_o_fine(self, testo):
        try:
            introduzione()
            if testo == None:
                risposta = input("Siete sicuri di voler uscire ? s/n " if modalita in ("A", "a") else "Sei sicuro di voler uscire ? s/n ")
                if risposta in ("S", "s"):
                    chiusura()
                else:
                    risposta = input("\nVolete ricominciare ? s/n " if modalita in ("A", "a") else "\nVuoi ricominciare ? s/n ")
                if risposta in ("S", "s"):
                    self.crea_tabella()
                else:
                    return risposta
            else:
                print(testo)
                risposta = input("Partita finita, volete ricominciare ? s/n \n" if modalita in ("A", "a") else "Partita finita, vuoi ricominciare ? s/n \n")
                self.crea_tabella() if risposta in ("S", "s") else chiusura()
                
        except KeyboardInterrupt:
            tris.ricomincia_o_fine(None)
        

    def mossa_computer(self, valido = True):
        n = len(self.board)
        spazi_liberi = 0

        for row in self.board:
            for oggetti in row:
                if oggetti == "-":
                    spazi_liberi += 1

        if spazi_liberi > 6:
            row, col = 2, 2
            valido = self.fix_spot(row,  col)
            if valido == False:
                row, col = choice([ 1, 2, 3 ]), choice([ 1, 2, 3 ])
                valido = self.fix_spot(row,  col)
            
            if valido:                                
                return row, col, valido

        z = 1
        for h in range(2):
            l = 0
            simbolo = self.simbolo if z == 1 else "X"
            for i in range(n):
                for j in range(n):
                    if self.board[i][j] == simbolo:
                        l += 1 
                        if l == 2:
                            for k in range(n):
                                row, col = i + 1, k + 1                                       
                                valido = self.fix_spot(row,  col)

                                z += 1 
                                if valido:
                                    return row, col, valido

        z = 1
        for h in range(2):
            l = 0
            simbolo = self.simbolo if z == 1 else "X"                                   
            for j in range(n):
                for i in range(n):
                    if self.board[i][j] == simbolo:
                        l += 1 
                        if l == 2:
                            for k in range(n):
                                row, col = j + 1, k + 1           
                                valido = self.fix_spot(row,  col)

                                z += 1 
                                if valido:
                                    return row, col, valido

        z = 1                        
        for h in range(2):
            l = 0
            simbolo = self.simbolo if z == 1 else "X"                                
            for i in range(n):
                i = j
                for k in range(n):
                    if self.board[i][j] == simbolo:
                        l += 1
                        if l == 2:
                            for m in range(n):
                                row, col = i + 1, j + 1
                                valido = self.fix_spot(row, col)

                                z += 1 
                                if valido:    
                                    return row, col, valido


    def due_giocatori(self, player):
        self.crea_tabella()
        if giocatore1 is giocatore2:
            self.primo_giocatore_casuale("A")
        punti_a, punti_b = 0, 0
        
        while True:
            try:
                if player == None:
                    player = choice([giocatore1, giocatore2])
            
                introduzione()
                print(f"{giocatore1}: {punti_a}".center(43 - (len(giocatore1)+len(str(punti_a))), " "), f"{giocatore2}: {punti_b}".center(43 - (len(giocatore1)+len(str(punti_a))), " "))

                valido = False

                self.simbolo = "X" if player == giocatore1 else "O"

                while valido != True:
                        
                    print(f"E' il turno di {player}")
                    self.mostra_tabella()
                    row, col = list(map(int, input(f"{player}, inserisci la riga e la colonna in cui vuoi inserire {self.simbolo}: ").split()))

                    valido = self.fix_spot(row, col)
                    if not valido:
                        print(f"{row} {col} è già occupata, riprova")            
        
                    if self.vittoria(player):
                        tris.ricomincia_o_fine(f"{player.upper()} HA VINTO")
                        if player == giocatore1:
                            punti_a += 1
                        else:
                            punti_b += 1
                        
                    if self.tabella_piena():
                        tris.ricomincia_o_fine("Pareggio!") 

                    player = tris.cambio_turno(player)
           
            except (IndexError and ValueError) or ValueError:
                print("\nInserisci due valori interi compresi tra 1 e 3 separati da uno spazio\nes: 1 2")
                sleep(2)

            except IndexError:
                print("\nInserisci due valori interi compresi tra 1 e 3 separati da uno spazio\nes: 1 2")
                sleep(2)

            except KeyboardInterrupt:
                tris.ricomincia_o_fine(None)


    def vs_computer(self, player):
        self.crea_tabella()
        if giocatore1 is giocatore2:
            self.primo_giocatore_casuale("B")
        punti_a, punti_b = 0, 0
        
        while True:
            try:
                if player == None:
                    player = choice([giocatore1, giocatore2])
                introduzione()
                print(f"{giocatore1}: {punti_a}".center(43 - (len(giocatore1)+len(str(punti_a))), " "), f"{giocatore2}: {punti_b}".center(43 - (len(giocatore1)+len(str(punti_a))), " "))

                self.mostra_tabella()
                valido = False

                self.simbolo = "X" if player == giocatore1 else "O"

                while valido != True:
                    
                    if player == giocatore1:
                        row, col = list(map(int, input(f"E' il tuo turno, inserisci la riga e la colonna in cui vuoi inserire {self.simbolo}: ").split()))
                        valido = self.fix_spot(row, col)
                        if not valido:
                            print(f"La posizione {row} {col} è già occupata, riprova") 
                        
                    else:
                        
                        row, col, valido = self.mossa_computer()

                        if valido:
                            print(f"E' il mio turno, inserisco {self.simbolo} in {row}, {col}")

                if player == giocatore2:
                    sleep(2)
                        
                if self.vittoria(player):
                    tris.ricomincia_o_fine("mi dispiace, hai perso ... ahahah un giorno i robot domineranno il mondo" if player == giocatore2 else f"complimenti {player}, hai vinto")
                    if player == giocatore1:
                        punti_a += 1
                    else:
                        punti_b += 1

                if self.tabella_piena():
                    tris.ricomincia_o_fine("Pareggio!")

                player = self.cambio_turno(player)

            except (IndexError and ValueError) or ValueError:
                print("\nInserisci due valori interi compresi tra 1 e 3 separati da uno spazio\nes: 1 2")
                sleep(2)

            except IndexError:
                print("\nInserisci due valori interi compresi tra 1 e 3 separati da uno spazio\nes: 1 2")
                sleep(2)

            except KeyboardInterrupt:
                tris.ricomincia_o_fine(None)

        
    def inizio(self):
        try:
            global modalita
            modalita = None

            introduzione()
                
            while modalita not in ("A", "a", "B", "b"):
                modalita = input("Inserisci A per la modalità due giocatori, B per la modalità contro il computer: ")

            player = tris.primo_giocatore_casuale(modalita)
                
            if modalita in ("A", "a"):
                tris.due_giocatori(player)
            else:
                tris.vs_computer(player)
                
        except KeyboardInterrupt:
            risposta = tris.ricomincia_o_fine(None)
            if risposta in ("N", "n"):
                self.inizio()
                
tris = Tris()      
tris.inizio()
