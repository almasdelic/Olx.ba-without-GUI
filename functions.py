
import mysql.connector
import time

mydb = mysql.connector.connect(
  host="your local host",
  user="your name",
  password="your password",
  database = "your database"
)

mycursor = mydb.cursor(dictionary=True)

def login():
    print("Dobrodošli na login formu: ")
    username = input("Molimo unesite Vaš username: ")
    password = input("Molimo unesite Vaš password: ")
    global user_id
    sql = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    mycursor.execute(sql)
    myresult = mycursor.fetchone()
    print(myresult)
    user_id = myresult['id']
    if myresult:
        return True
    else:
        return False

def register():
    print("Dobrodošli na registracijsku formu: ")
    username = input("Molimo unesite Vaš username: ")
    password = input("Molimo unesite Vaš password: ")
    firstname = input("Molimo unesite Vaše ime: ")
    lastname = input("Molimo unesite Vaše prezime: ")
    email = input("Molimo unesite Vaš email: ")
    sql = "INSERT INTO users (firstname, lastname, username, password, email) VALUES (%s, %s, %s, %s, %s)"
    val = (firstname, lastname, username, password, email)
    mycursor.execute(sql, val)
    mydb.commit()
    return True

def unosProizvoda():
    print("Molimo popunite sljedeći formular za unos: ")
    imeProizvoda = input("Molimo unesite ime proizvoda: ")
    cijenaProizvoda = input("Molimo unesite cijenu proizvoda: ")
    opisProizvoda = input("Molimo unesite opis proizvoda: ")

    sql = "SELECT * FROM kategorije"
    mycursor.execute(sql)
    kategorije = mycursor.fetchall()

    for kategorija in kategorije:
        print(f"ID-{kategorija['id']} : {kategorija['ime_kategorije']}")
    kategorijaProizvoda = input("Molimo unesite ID kategorije koja Vam odgovara u numerickoj vrijednosti: ")
    sql = "INSERT INTO proizvodi (ime_proizvoda, cijena_proizvoda, opis, kategorija_proizvoda) VALUES (%s, %s, %s, %s)"
    val = (imeProizvoda, cijenaProizvoda, opisProizvoda, kategorijaProizvoda)
    print("Proizvod se upravo unosi u bazu podataka...")
    time.sleep(3)
    print("Almost there..")
    time.sleep(2)
    mycursor.execute(sql, val)
    mydb.commit()
    sql = "SELECT * FROM proizvodi ORDER BY id DESC LIMIT 1;"
    mycursor.execute(sql)
    zadnjiProizvod = mycursor.fetchone()
    zadnjiProizvodId = zadnjiProizvod['id']
    sql = "INSERT INTO proizvod_user (id_usera,id_proizvoda) VALUES (%s, %s)"
    val = (user_id, zadnjiProizvodId)
    mycursor.execute(sql,val)
    mydb.commit()
    print("Proizvod je uspješno unesen u bazu podataka! ")
    print("Vraćam Vas na dashboard...")
    time.sleep(4)

    
def pretragaArtikala():
    sql = "SELECT * FROM proizvodi"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    print("Ispisujemo proizvode...")
    time.sleep(2)
    for x in myresult:
        sql = f"SELECT * FROM proizvod_user WHERE id_proizvoda={x['id']}"
        mycursor.execute(sql)
        mojProizvodUser = mycursor.fetchone()
        idUsera = mojProizvodUser['id_usera']
        sql = f"SELECT * FROM users WHERE id={idUsera}"
        mycursor.execute(sql)
        mojUser = mycursor.fetchone()
        imeUsera = mojUser['firstname']
        print("*"*50)
        print(f"ID - {x['id']}")
        print(f"Ime proizvoda je: {x['ime_proizvoda']}")
        print(f"Cijena proizvoda je: {x['cijena_proizvoda']} KM")
        print(f"Opis proizvoda je: {x['opis_proizvoda']}")
        print(f"Vlasnik proizvoda je: {imeUsera}")
        print("*"*50)

    vasOdabir = int(input("Molimo unesite ID od proizvoda za koji želite da kontaktirate korisnika: "))
    poruka = input("Molimo unesite Vasu poruku: ")
    sql = f"SELECT * FROM proizvod_user WHERE id_proizvoda={vasOdabir}"
    mycursor.execute(sql)
    mojProizvodUser = mycursor.fetchone()
    idUseraOwner = mojProizvodUser['id_usera']
    sql = "INSERT INTO poruke(poruka,id_sent_usera,id_receive_usera,id_proizvoda) VALUES (%s,%s,%s,%s)"
    val = (poruka,user_id,idUseraOwner,vasOdabir)
    print("Sistem salje poruku, stay tuned...")
    time.sleep(2)
    mycursor.execute(sql,val)
    mydb.commit()
    print("Poruka uspjesno poslana! Redirektujem Vas na Dashboard.")
    time.sleep(2)

def mojProfil():
    print("Poštovani korisnice, dobrodosli na svoj profil.")
    print("Lista Vaših artikala je: ")
    sql = f"SELECT * FROM proizvod_user WHERE id_usera ='{user_id}'"
    mycursor.execute(sql)
    povezaniProizvodi = mycursor.fetchall()
    for proizvodId in povezaniProizvodi:
        sql = f"SELECT * FROM proizvodi WHERE id='{proizvodId['id_proizvoda']}'"
        mycursor.execute(sql)
        korisnikovProizvod = mycursor.fetchone()
        print("*"*50)
        print(f"Ime proizvoda: {korisnikovProizvod['ime_proizvoda']}")
        print(f"Cijena proizvoda: {korisnikovProizvod['cijena_proizvoda']}")
        print(f"Opis proizvoda: {korisnikovProizvod['opis_proizvoda']}")
        print("*"*50)

def inbox():
    print("Dobrodosli u svoj inbox.")
    print("Upravo listamo poruke...")
    time.sleep(2)
    sql = f"SELECT * FROM poruke WHERE id_receive_usera = {user_id}"
    mycursor.execute(sql)
    mojePoruke = mycursor.fetchall()
    for poruka in mojePoruke:
        sql = f"SELECT * FROM users WHERE id = {poruka['id_sent_usera']}"
        mycursor.execute(sql)
        korisnikObjekat = mycursor.fetchone()
        imeKorisnika = korisnikObjekat['firstname']
        sql = f"SELECT * FROM proizvodi WHERE id = {poruka['id_proizvoda']}"
        mycursor.execute(sql)
        proizvodObjekat = mycursor.fetchone()
        imeProizvoda = proizvodObjekat['ime_proizvoda']
        print("*"*50)
        print(f"Korisnik - {imeKorisnika} Vam je poslao poruku")
        print(f"Radi se o artiklu - {imeProizvoda}")
        print(f"Poruka glasi: ")
        print(poruka['poruka'])


def dashboard():
    print("Poštovani korisniče, šta želite da uradite?")
    print("1) Unos novog proizvoda u sistem")
    print("2) Pretraga artikala na sistemu")
    print("3) Moj profil")
    print("4) Inbox")
    korisnikovOdabir = int(input("Vaš odabir je: "))
    if korisnikovOdabir == 1:
        unosProizvoda()
    elif korisnikovOdabir ==2:
        pretragaArtikala()
    elif korisnikovOdabir == 3:
        mojProfil()
    elif korisnikovOdabir == 4:
        inbox()


