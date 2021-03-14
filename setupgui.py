from tkinter import *
from subprocess import *
import signal
from time import sleep


# Globale Variablen
padx = 10
pady = 5

# Defaults
player_amounts = [
    ('PLAYER_AMOUNT_KUNDEN                   ', 'Spieler pro Kunde', 2),
    ('PLAYER_AMOUNT_LEITUNGSTEAM             ', 'Spieler in der Geschäftsführung', 3),
    ('PLAYER_AMOUNT_KUNDENDIENST             ', 'Spieler im Kundendienst', 5),
    ('PLAYER_AMOUNT_INTERNE_DIENSTLEISTUNG   ', 'Spieler in Interne Dienstleistung', 5),
    ('PLAYER_AMOUNT_PRODUKTIONSDIENSTLEISTUNG', 'Spieler in der Produktionsdienstleistung', 5),
    ('PLAYER_AMOUNT_PRODUKTION               ', 'Spieler in der Produktion', 5),
    ('PLAYER_AMOUNT_LIEFERANTEN              ', 'Spieler pro Lieferant', 2),
]


def main():
    # Definition der Unterfenster
    # Dialog frische Datenbank erstellen
    def setup():
        # Funktionen (gefolgt von UI)
        # Funktion Speichernbutton
        def save():
            print("\n[setupgui] ##### CREATING FRESH DATABASE... #####\n")
            print("[setupgui] Generate config.py...")
            # Generierung config.py
            # Header
            out = "\"\"\"\nDie Anzahl der Spieler jeder Organisationseinheit sind hier definiert.\n\"\"\"\n\n"
            # Digitalisierungsstufe
            out += "GAME_VERSION                            = " + str(version.get()) + '\n\n'
            # Spieleranzahlen
            for i in range(0, len(spinboxes)):
                out += player_amounts[i][0] + ' = ' + spinboxes[i].get() + '\n'

            print("[setupgui] Save config.py...")
            f = open("gtserver/gtapp/constants/config.py", "w")
            f.write(out)
            f.close()


            # Löschung Datenbank
            print("[setupgui] Delete DB...")
            run(["del","/f","gtserver\\db.sqlite3"], shell=True) 

            # Generierung Datenbank
            print("[setupgui] Create DB...")
            run(["pipenv", "run", "python", "gtserver\\manage.py", "createdb"])
            
            print("\n[setupgui] ##### CREATED FRESH DATABASE #####\n")
            close()



        # Funktion Abbrechenbutton
        def close():
            mainroot.deiconify()
            root.destroy()



        # UI
        # Fenster erstellen
        root = Toplevel(mainroot)
        root.iconbitmap('gtserver/static/favicon/favicon.ico')
        mainroot.withdraw()
        root.title("Frische Datenbank erstellen")
        root.protocol("WM_DELETE_WINDOW", close)
        row = 0

        # Einführungstext    
        Label(root, text="Mit diesem Dialog kann eine neue Datenbank erstellt werden.\n/!\\ Achtung! Alle Aufträge etc. gehen dabei verloren!", justify=LEFT).grid(row=row, column=0, padx=padx, pady=pady, sticky=[N, W])
        row += 1

        # Digitalisierungsstufe
        # Rahmen
        frame_version = LabelFrame(root, text='Digitalisierungsstufe')
        frame_version.grid(row=row, column=0, padx=padx, pady=pady, sticky=[N, W])
        row += 1

        # Kontrollvariable
        version = IntVar()

        # Hilfetext
        label_version = Label(frame_version, text="Stufe 1: ohne Schnittstellen zwischen den Systemen\nStufe 2: mit Schnittstellen zwischen den Systemen", justify=LEFT)
        label_version.grid(row=0, column=0, columnspan=2, padx=padx, pady=pady, sticky=[N, W])

        # Radiobuttons
        version1 = Radiobutton(frame_version, text='Digitalisierungsstufe 1', variable=version, value=1)
        version1.select()
        version1.grid(row=1, column=0, padx=padx, pady=pady, sticky=[N, W])
        version1 = Radiobutton(frame_version, text='Digitalisierungsstufe 2', variable=version, value=2, state=DISABLED)
        version1.grid(row=2, column=0, padx=padx, pady=pady, sticky=[N, W])
        
        # Maximale Spieleranzahlen
        # Rahmen
        frame_player_amounts = LabelFrame(root, text='Maximale Spieleranzahlen')
        frame_player_amounts.grid(row=row, column=0, padx=padx, pady=pady, sticky=[N, W])
        row += 1
        row += 1
        
        # Hilfetext
        label_player_amounts = Label(
            frame_player_amounts,
            text="Wie viele Benutzer sollen angelegt werden?\n/!\\ Achtung! Kann während des Spiels nicht erhöht werden!",
            justify=LEFT
        )
        label_player_amounts.grid(row=0, column=0, columnspan=2, padx=padx, pady=pady, sticky=[N, W])
        
        # Amount Spinboxen erstellen
        labels = []
        spinboxes = []
        
        for i, item in enumerate(player_amounts, start=1):
            spinbox = Spinbox(frame_player_amounts, from_=1, to=10, increment=1, width=3)
            spinbox.delete(0)
            spinbox.insert(0, item[2])
            label = Label(frame_player_amounts, text=item[1])

            spinbox.grid(row=i, column=0, padx=padx, pady=pady, sticky=[N, W])
            label.grid(row=i, column=1, padx=padx, pady=pady, sticky=[N, W])

            spinboxes.append(spinbox)
            labels.append(label)

        # Einführungstext    
        Label(root, text="Die Erstellung einer neuen Datenbank dauert einen Moment\n(siehe Konsolenfenster).", justify=LEFT).grid(row=row, column=0, padx=padx, pady=pady, sticky=[N, W])
        row += 1

        # Footer
        # Unsichtbarer Rahmen
        frame_btns = Frame(root)
        frame_btns.grid(row=row, column=0, sticky=[S, E])
        row += 1

        # Abbrechenbutton
        btn_close = Button(frame_btns, text='Abbrechen', command=close)
        btn_close.grid(row=0, column=0, padx=padx, pady=pady, sticky=[S, E])

        # Speichernbutton
        btn_save = Button(frame_btns, text="Frische Datenbank erstellen", command=save)
        btn_save.grid(row=0, column=1, padx=padx, pady=pady, sticky=[S, E])
        
        root.mainloop() 
        

        
        
    def runserver():
        # Funktionen
        print("\n[setupgui] ##### STARTING SERVER #####\n")
        process = Popen(["pipenv", "run", "python", "gtserver\\manage.py", "runserver", "0.0.0.0:80", "--insecure"])
        root = Tk()
        root.iconbitmap('gtserver/static/favicon/favicon.ico')

        def close():
            #mess
            #sleep(5)
            #process.terminate()
            mainroot.deiconify()
            root.destroy()
            print("\n[setupgui] ##### STOPPING SERVER... #####\n")
            # Send CTRL+C (CTRL+BREAK doesn't work) and wait until process is shut down
            process.send_signal(signal.CTRL_C_EVENT)
            try:
                while process.poll() is None:
                    sleep(0.1)
                    print('..')
            except KeyboardInterrupt:
                while process.poll() is None:
                    print('...')
                    sleep(0.1)
            print("\n[setupgui] ##### STOPPED SERVER #####\n")
        
        def openurl():
            import webbrowser
            webbrowser.open('http://10.10.10.10/accounts/urllogin/SL/4027/')

        # UI
        
        mainroot.withdraw()
        root.title("ERP Control Panel")
        root.protocol("WM_DELETE_WINDOW", close)

        row = 0

        label_runserver = Label(root, text="Der Server wurde gestartet. Es kann einige Sekunden dauern, bis\nAnfragen entgegengenommen werden (siehe Konsolenfenster).\nZugangsdaten: http://10.10.10.10/ , Nutzer SL, Passwort 4027\n\nBitte beenden Sie den Server nur über die Schaltfläche \"Server stoppen\".", justify=LEFT)
        label_runserver.grid(row=0, column=0, padx=padx, pady=pady, sticky=[N, W])
        row += 1

        # Footer
        # Unsichtbarer Rahmen
        frame_btns = Frame(root)
        frame_btns.grid(row=row, column=0, sticky=[S, E])
        row += 1

        btn_stop = Button(frame_btns, text="Server stoppen", command=close)
        btn_stop.grid(row=0, column=0, padx=padx, pady=pady, sticky=[S, E])

        btn_stop = Button(frame_btns, text="ERP-System aufrufen", command=openurl)
        btn_stop.grid(row=0, column=1, padx=padx, pady=pady, sticky=[S, E])

        root.mainloop() 

    def close():
        mainroot.destroy()

    # Hauptfenster erstellen
    mainroot = Tk()
    mainroot.iconbitmap('gtserver/static/favicon/favicon.ico')
    mainroot.title("ERP Control Panel")
    
    #mainroot.geometry("300x250")

    
    # cmd /c start powershell.exe -WindowStyle Maximized -Command pipenv run py gtserver\manage.py runserver 0.0.0.0:80 --insecure
    mainrow = 0

    # Rahmen
    frame_setup = LabelFrame(mainroot, text='Konfiguration')
    frame_setup.grid(row=mainrow, column=0, padx=padx, pady=pady, sticky=[N, W])
    mainrow += 1
    
    label_setup = Label(frame_setup, text="Um ein neues Spiel zu beginnen,\nerstellen Sie eine frische Datenbank.", justify=LEFT)
    label_setup.grid(row=0, column=0, padx=padx, pady=pady, sticky=[N, W])

    btn_setup = Button(frame_setup, text="Frische Datenbank erstellen", command=setup)
    btn_setup.grid(row=1, column=0, padx=padx, pady=pady, sticky=[S, E])

    # Rahmen 
    frame_runserver = LabelFrame(mainroot, text='Server starten')
    frame_runserver.grid(row=mainrow, column=0, padx=padx, pady=pady, sticky=[N, W])
    mainrow += 1

    label_runserver = Label(frame_runserver, text="Der Server ist aus. Um ihn zu starten,\nnutzen Sie folgenden Button.", justify=LEFT)
    label_runserver.grid(row=0, column=0, padx=padx, pady=pady, sticky=[N, W])
    
    btn_start = Button(frame_runserver, text="Server starten", command=runserver, justify=RIGHT)
    btn_start.grid(row=1, column=0, padx=padx, pady=pady, sticky=[S, E])

    btn_start = Button(mainroot, text="Schließen", command=close, justify=RIGHT)
    btn_start.grid(row=mainrow, column=0, padx=padx, pady=pady, sticky=[S, E])
    mainrow += 1

    print("\n[setupgui] ##### STARTED SETUPGUI #####\n")

    # UI-Loop
    mainroot.mainloop()



    
if __name__ == '__main__':
    main()
