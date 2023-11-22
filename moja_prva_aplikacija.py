from functions import register
from functions import login
from functions import dashboard
import time

while True:
    print("Dobrodošli na sistem.")
    print("Molimo Vas da odaberete šta želite da uradite: ")
    print("1) Login")
    print("2) Register")
    korisnikovOdabir = int(input("Vaš odabir je: "))
    if korisnikovOdabir == 2:
        while True:
            if register() == True:
                login()
            else:
                print("Pokušajte ponovo, imate grešku u unosu.")
    elif korisnikovOdabir == 1:
        while True:
            if login() == True:
                print("Čestitamo, uspješno ste logovani na sistem.")
                while True:
                    dashboard()
            else:
                print("Molimo pokušajte ponovo.")