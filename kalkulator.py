import datetime


class Biblioteka:
    def __init__(self):
        self.__ksiazki = {}
        self.__czytelnicy = {}
        self.wyporzyczone_przez = None

     def raport_ksiazek(self, data):
        lista = []
        for k in self.__ksiazki.values():
            nowsze = k.egzemplarze_nowsze_niz(data)
            if len(nowsze) > 0:
                lista.append((k.tytul, k.autor, len(nowsze)))
        return sorted(lista, key = lambda t: t[0])

    def zwroc_czytelnikow(self):
        return self.__czytelnicy;

    def pobierz_czytelnika(self, nazwisko):
        try:
            return self.__czytelnicy[nazwisko]
        except KeyError:
            nowy = Czytelnik(nazwisko)
            self.__czytelnicy[nazwisko] = nowy
            return nowy

    def __pobierz_ksiazke_po_tytule(self, tytul):
        ksiazka = False
        for ksiazka in self.__ksiazki:
            if ksiazka[0] == tytul:
                break
        return ksiazka

    def dodaj_egzemplarz_ksiazki(self, tytul, autor, rok_wydania, data):
        try:
            ksiazka = self.__ksiazki[tytul]
        except KeyError:
            ksiazka = Ksiazka(tytul, autor)
            self.__ksiazki[tytul] = ksiazka
        ksiazka.egzemplarze.append(Egzemplarz(rok_wydania, ksiazka, data))
        return True

    def dostepne_egz(self, tytul):
        ksiazka = self.__ksiazki[tytul]
        listaEgzemplarzy = ksiazka.egzemplarze
        listaDostepnychEgzemplarzy = []
        for elem in listaEgzemplarzy:
            if elem.wypozyczony == False:
                listaDostepnychEgzemplarzy.append(elem)
        return listaDostepnychEgzemplarzy
    

    def wypozycz(self, nazwisko, tytul, data):
        try:
            egzemplarz = self.dostepne_egz(tytul)[0]
            czytelnik = self.__pobierz_czytelnika(nazwisko)
            return czytelnik.wypozycz(egzemplarz)
        except IndexError:
            return False

    def oddaj(self, nazwisko, tytul, data):
        czytelnik = self.__pobierz_czytelnika(nazwisko)
        data_oddania = datetime.date(*data)
        return czytelnik.oddaj(tytul)

class Ksiazka:
    def __init__(self, tytul, autor):
        self.tytul = tytul
        self.autor = autor
        self.egzemplarze = []

    def egzemplarze_nowsze_niz(self, data):
        data = datetime.date(*data)
        return [e for e in self.egzemplarze if e.data_dodania > data]

class Egzemplarz:
    def __init__(self, rok_wydania, ksiazka, data):
        self.rok_wydania = rok_wydania
        self.ksiazka = ksiazka
        self.data_dodania = datetime.date(*data)
        self.wypozyczony = False
    def jest_wypozyczana(self):
        self.wypozyczony = True
    def jest_oddawana(self):
        self.wypozyczony = False
    def pobierz_tytul(self):
        return self.ksiazka.tytul

class Czytelnik:
    limit = 3

    def __init__(self, nazwisko):
        self.nazwisko = nazwisko
        self.wypozyczone = {}

    def wypozycz(self, egzemplarz):
        tytul = egzemplarz.ksiazka.tytul
        if Czytelnik.limit > len(self.wypozyczone) and tytul not in self.wypozyczone.keys():
            egzemplarz.wypozyczony = True
            self.wypozyczone[tytul] = egzemplarz
            return True
        else:
            return False

    def oddaj(self, tytul):
        try:
            self.wypozyczone.pop(tytul).wypozyczony = False
            return True
        except KeyError:
            return False

    def opoznienie(self):
        for elem in wypozyczone:
            data_wypozyczenia = elem.data
            if(datetime.datetime.now() - data_wypozyczenia > 7):
                dni_opoznienia = datetime.datetime.now() - data_wypozyczenia
                print(self.nazwisko + "," + dni_opoznienia * 0.5)

biblioteka = Biblioteka()
for i in range(int(input())):
    t = eval(input())
    if t[0] == "dodaj":
        print(biblioteka.dodaj_egzemplarz_ksiazki(t[1], t[2], t[3], t[4]))
    elif t[0] == "wypozycz":
        print(biblioteka.wypozycz(t[1], t[2], t[3]))
    elif t[0] == "oddaj":
        print(biblioteka.oddaj(t[1], t[2], t[3]))

data_podana = eval(input())
czytelnicy = biblioteka.zwroc_czytelnikow();
for x in czytelnicy:
    print(biblioteka.pobierz_czytelnika(x).opoznienie())


#for x in biblioteka.raport_ksiazek(data_podana):
   # print(x)

