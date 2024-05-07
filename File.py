import pypyodbc
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import time
from PIL import Image, ImageTk
import tkinter.simpledialog
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
from pathlib import Path

def kullanici_giris():
    kullanici_adi = tkinter.simpledialog.askstring("Kullanıcı Girişi", "Kullanıcı Adınız:")
    sifre = tkinter.simpledialog.askstring("Kullanıcı Girişi", "Şifreniz:", show='*')
    return kullanici_adi, sifre
def giris_kontrol():
    dogru_kullanici_adi = "admin"
    dogru_sifre = "sifre"

    kullanici_adi, sifre = kullanici_giris()

    if kullanici_adi == dogru_kullanici_adi and sifre == dogru_sifre:
        return True
    else:
        return False
    
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\askar\OneDrive\Masaüstü\VERİTABANI ÖDEVİ\build\assets\frame0")



def main():
    if not giris_kontrol():
        print("Giriş bilgileri yanlış. Program kapatılıyor.")
        messagebox.showinfo(title="Film", message="HATALI GİRİŞ. PROGRAM KAPATILIYOR")
        return

    print("Giriş başarılı. Program devam ediyor.")
    messagebox.showinfo(title="Film", message="Giriş Başarılı.Program Açılıyor")
    connection = pypyodbc.connect('DRIVER={SQL Server};SERVER=SAHIN;DATABASE=FilmTabani;UID=sa;PWD=003sahin003')   #PYPYODBC Kütüphanesi ile SQL SERVER BAĞLANTISI SAĞLADIK
    tikla = connection.cursor()

    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\askar\OneDrive\Masaüstü\VERİTABANI ÖDEVİ\build\assets\frame0")


    def relative_to_assets(path: str) -> Path:
        return ASSETS_PATH / Path(path)

    def Filmler():
        tikla.execute('SELECT * FROM FilmTaban')
        rows = tikla.fetchall()

        tablo.delete(*tablo.get_children())  # Tablodaki mevcut verileri temizle

        for row in rows:
            tablo.insert('', 'end', values=row)

    def KacFilmVar(kategori):
        tikla = connection.cursor()

        query = "SELECT COUNT(*) FROM FilmTaban WHERE Kategori LIKE ?"
        tikla.execute(query, ('%' + kategori + '%',))

        result = tikla.fetchone()[0]

        messagebox.showinfo(title=f"{kategori} Filmi Sayısı", message=f"Toplam {result} adet {kategori} filmi bulunmaktadır.")

        tikla.close()

    def YuksekIMDB():
        tikla.execute('SELECT  MAX(IMDB) AS EnYuksekIMDB FROM FilmTaban')
        rows = tikla.fetchall()

        for item in tablo.get_children():
            tablo.delete(item)

        for row in rows:
            tablo.insert('', 'end', values=EvetOscar(row))

    def TabloyaYazdir(kategori):
        tikla = connection.cursor()

        query = "SELECT * FROM FilmTaban WHERE Kategori LIKE ?"
        tikla.execute(query, ('%' + kategori + '%',))

        rows = tikla.fetchall()

        for item in tablo.get_children():
            tablo.delete(item)

        for row in rows:
            tablo.insert('', 'end', values=row)

        tikla.close()

    def KategoriSecildi(event):
        secilen_kategori = kategori_combobox.get()
        KacFilmVar(secilen_kategori)
        TabloyaYazdir(secilen_kategori)

    def OyuncuTablo(root):
        root.title("Oyuncu Tablosu")

        tikla= connection.cursor()
        tikla.execute("SELECT * FROM Oyuncu")
        rows = tikla.fetchall()

        root.geometry("1280x720+120+50")
        root.resizable(True,True)

        tablo = ttk.Treeview(root)

        tablo["columns"] = ("OyuncuID","OyuncuAdi", "OynadigiFilmler", "Memleket", "OscarOdullu")
        
        tablo.heading("OyuncuID", text="OyuncuID")
        tablo.heading("OyuncuAdi", text="Oyuncu Adı")
        tablo.heading("OynadigiFilmler", text="Filmleri")
        tablo.heading("Memleket", text="Memleketi")
        tablo.heading("OscarOdullu", text="Oscar Ödülü")

        # Set the column widths
        tablo.column("OyuncuID", width=100)
        tablo.column("OyuncuAdi", width=100)
        tablo.column("OynadigiFilmler", width=100)
        tablo.column("Memleket", width=50)
        tablo.column("OscarOdullu", width=50)

        for row in rows:
            tablo.insert('', 'end', values=row)

        tablo.pack()
        tablo.place(width=1280, height=720)

        return tablo

    def OyuncuTablosunuGoster():
        director_root = tk.Toplevel()
        tablo_oyuncu= OyuncuTablo(director_root)
        director_root.mainloop()

    def YonetmenTablo(root):
        root.title("Yonetmen Tablosu")

        tikla = connection.cursor()
        tikla.execute('SELECT * FROM Yonetmenler')
        rows = tikla.fetchall()

        root.geometry("1280x720+120+50")
        root.resizable(True, True)

        tablo = ttk.Treeview(root)

        tablo["columns"] = ("YonetmenID","YonetmenAdi", "Filmleri", "Memleketi", "OscarOdulu")
        
        tablo.heading("YonetmenID", text="YonetmenID")
        tablo.heading("YonetmenAdi", text="Yönetmen Adı")
        tablo.heading("Filmleri", text="Filmleri")
        tablo.heading("Memleketi", text="Memleketi")
        tablo.heading("OscarOdulu", text="Oscar Ödülü")

        # Set the column widths
        tablo.column("YonetmenID", width=150)
        tablo.column("YonetmenAdi", width=150)
        tablo.column("Filmleri", width=200)
        tablo.column("Memleketi", width=100)
        tablo.column("OscarOdulu", width=100)

        for row in rows:
            tablo.insert('', 'end', values=row)

        tablo.pack()
        tablo.place(width=1280, height=720)

        return tablo

    def YonetmenTablosunuGoster():
        director_root = tk.Toplevel()  # Create a new window
        tablo_yonetmen = YonetmenTablo(director_root)
        director_root.mainloop()

    def VeriTablo(root):
        root.title("Tablo")

        tikla = connection.cursor()
        tikla.execute('SELECT * FROM FilmTaban')
        rows = tikla.fetchall()

        root.geometry("1280x720+120+50")  # Pencere boyutu ayarladım '120+50' Pencerenin ekranda nerede açılacağını ayarladım.
        root.resizable(True, True)

        tablo = ttk.Treeview(root)

        tablo["columns"] = ("FilmNo", "FilmAdi", "Kategori","Yonetmen","Oyuncular","IMDB","Sure","YapimYili","Ulke","Platform","Dil","Oscar")
        
        tablo.heading("FilmNo", text="FilmNo",)
        tablo.heading("FilmAdi", text="Film Adı")
        tablo.heading("Kategori", text="Kategori")
        tablo.heading("Yonetmen", text="Yönetmen")
        tablo.heading("Oyuncular", text="Oyuncu")
        tablo.heading("IMDB", text="IMDB")
        tablo.heading("Sure", text="Süre")
        tablo.heading("YapimYili", text="Yapım Yılı")
        tablo.heading("Ulke", text="Ülke")
        tablo.heading("Platform", text="Platform")
        tablo.heading("Dil", text="Dil")
        tablo.heading("Oscar",text="Oscar")

        tablo.column("FilmNo", width=50,)
        tablo.column("FilmAdi", width=100)
        tablo.column("Kategori", width=100)
        tablo.column("Yonetmen", width=90)
        tablo.column("Oyuncular", width=200)
        tablo.column("IMDB", width=50,)
        tablo.column("Sure", width=50)
        tablo.column("YapimYili", width=50)
        tablo.column("Ulke", width=50)
        tablo.column("Platform", width=50)
        tablo.column("Dil", width=50)
        tablo.column("Oscar", width=50)



        for row in rows:
            tablo.insert('', 'end', values=row)

        tablo.pack()
        tablo.place(width=1440, height=780)

        return tablo

    def Yapimm(tablo):  

        girilen_deger = yapim_yili_giris.get()
        tikla = connection.cursor()

        query = "SELECT * FROM FilmTaban WHERE YapimYili=? "
        tikla.execute(query, (girilen_deger,))

        rows = tikla.fetchall()

        # Mevcut verileri temizler
        for item in tablo.get_children():
            tablo.delete(item)

        # Yeni Verileri Ekler
        for row in rows:
            tablo.insert('', 'end', values=row)

        result_str = ""
        for row in rows:
            result_str += str(row) + "\n"

        # Sonucu mesaj kutusunda gösterir
        messagebox.showinfo(title="Film", message=result_str)
        tikla.close()

    def YapimYilinaGore(tablo):
        tikla = connection.cursor()

        query = "SELECT * FROM FilmTaban ORDER BY YapimYili DESC"
        tikla.execute(query)

        rows = tikla.fetchall()

        # Mevcut verileri temizler
        for item in tablo.get_children():
            tablo.delete(item)

        # Yeni Verileri Ekler
        for row in rows:
            tablo.insert('', 'end', values=row)

        result_str = ""
        for row in rows:
            result_str += str(row) + "\n"

        # !Sonucu mesaj kutusunda gösterir
        messagebox.showinfo(title="Film", message=result_str)

        tikla.close()

    def YapimYiliAraliginaGore(tablo):
        girilen_alt_limit = yapim_yili_alt_limit_giris.get()
        girilen_ust_limit = yapim_yili_ust_limit_giris.get()
        tikla = connection.cursor()

        query = "SELECT * FROM FilmTaban WHERE YapimYili BETWEEN ? AND ?"
        tikla.execute(query, (girilen_alt_limit, girilen_ust_limit))

        rows = tikla.fetchall()

        for item in tablo.get_children():
            tablo.delete(item)

        for row in rows:
            tablo.insert('', 'end', values=row)

        result_str = ""
        for row in rows:
            result_str += str(row) + "\n"

        messagebox.showinfo(title="Film", message=result_str)
        tikla.close()

    def YonetmeneGore(tablo):
        girilen_deger = yonetmen_giris.get()
        tikla = connection.cursor()

        query = "SELECT * FROM FilmTaban WHERE Yonetmen LIKE ?"
        tikla.execute(query, ('%' + girilen_deger + '%',))

        rows = tikla.fetchall()

        # !Verileri temizler
        for item in tablo.get_children():
            tablo.delete(item)

        # !Verileri Ekler
        for row in rows:
            tablo.insert('', 'end', values=row)

        result_str = ""
        for row in rows:
            result_str += str(row) + "\n"

        # !Sonucu mesaj kutusunda gösterir
        messagebox.showinfo(title="Film", message=result_str)

        tikla.close()

    def OyuncularaGore(tablo):
        girilen_deger = oyuncular_giris.get()
        tikla = connection.cursor()

        query = "SELECT * FROM FilmTaban WHERE Oyuncular LIKE ?"
        tikla.execute(query, ('%' + girilen_deger + '%',))

        rows = tikla.fetchall()

        for item in tablo.get_children():
            tablo.delete(item)

        for row in rows:
            tablo.insert('', 'end', values=row)

        result_str = ""
        for row in rows:
            result_str += str(row) + "\n"

        messagebox.showinfo(title="Film", message=result_str)
        tikla.close()

    def KategoriyeGore(tablo):
        girilen_deger = kategori_giris.get()
        tikla = connection.cursor()

        query = "SELECT * FROM FilmTaban WHERE Kategori LIKE ?"
        tikla.execute(query, ('%' + girilen_deger + '%',))

        rows = tikla.fetchall()

        for item in tablo.get_children():
            tablo.delete(item)

        for row in rows:
            tablo.insert('', 'end', values=row)

        result_str = ""
        for row in rows:
            result_str += str(row) + "\n"

        messagebox.showinfo(title="Film", message=result_str)

        tikla.close()

    def FilmeGore(tablo):
        girilen_deger = film_adi_giris.get()
        tikla = connection.cursor()

        query = "SELECT * FROM FilmTaban WHERE FilmAdi LIKE ?"
        tikla.execute(query, ('%' + girilen_deger + '%',))

        rows = tikla.fetchall()

        for item in tablo.get_children():
            tablo.delete(item)

        for row in rows:
            tablo.insert('', 'end', values=row)

        result_str = ""
        for row in rows:
            result_str += str(row) + "\n"

        messagebox.showinfo(title="Film", message=result_str)
        tikla.close()

    def UlkeyeGore(tablo):
        girilen_deger = ulke_giris.get()
        tikla = connection.cursor()

        query = "SELECT * FROM FilmTaban WHERE Ulke LIKE ?"
        tikla.execute(query, ('%' + girilen_deger + '%',))

        rows = tikla.fetchall()

        for item in tablo.get_children():
            tablo.delete(item)

        for row in rows:
            tablo.insert('', 'end', values=row)

        result_str = ""
        for row in rows:
            result_str += str(row) + "\n"

        messagebox.showinfo(title="Film", message=result_str)

        tikla.close()

    def UlkeSutunu(tablo):
        girilen_deger = ulke_girissutun.get()
        tikla = connection.cursor()

        query = "SELECT FilmAdi,Kategori,YapimYili FROM FilmTaban WHERE Ulke LIKE ?"
        tikla.execute(query, ('%' + girilen_deger + '%',))

        rows = tikla.fetchall()

        for item in tablo.get_children():
            tablo.delete(item)

        for row in rows:
            tablo.insert('', 'end', values=row)

        result_str = "Sonuç Tabloya Gelmiştir"

        messagebox.showinfo(title="Film", message=result_str)

        tikla.close()

    def IMDByeGore(tablo):
        girilen_deger = imdb_giris.get()
        tikla = connection.cursor()

        query = "SELECT * FROM FilmTaban WHERE IMDB = ?"
        tikla.execute(query, (girilen_deger,))

        rows = tikla.fetchall()

        for item in tablo.get_children():
            tablo.delete(item)

        for row in rows:
            tablo.insert('', 'end', values=row)

        result_str = ""
        for row in rows:
            result_str += str(row) + "\n"

        messagebox.showinfo(title="Film", message=result_str)

        tikla.close()

    def IMDbAraliginaGore(tablo):
        girilen_alt_limit = imdb_alt_limit_giris.get()
        girilen_ust_limit = imdb_ust_limit_giris.get()
        tikla = connection.cursor()

        query = "SELECT * FROM FilmTaban WHERE IMDB BETWEEN ? AND ?"
        tikla.execute(query, (girilen_alt_limit, girilen_ust_limit))

        rows = tikla.fetchall()

        for item in tablo.get_children():
            tablo.delete(item)

        
        for row in rows:
            tablo.insert('', 'end', values=row)

    
        result_str = ""
        for row in rows:
            result_str += str(row) + "\n"

        
        messagebox.showinfo(title="Film", message=result_str)

        tikla.close()

    def IMDbYuksektenDuse(tablo):
        tikla = connection.cursor()

        query = "SELECT * FROM FilmTaban ORDER BY IMDB DESC"
        tikla.execute(query)

        rows = tikla.fetchall()

        # !Mevcut verileri temizler
        for item in tablo.get_children():
            tablo.delete(item)

        # !Yeni Verileri Ekler
        for row in rows:
            tablo.insert('', 'end', values=row)

        result_str = ""
        for row in rows:
            result_str += str(row) + "\n"

        # !Sonucu mesaj kutusunda gösterir
        messagebox.showinfo(title="Film", message=result_str)

        tikla.close()

    def AlfabetikIsmeGore(tablo):
        tikla = connection.cursor()

        query = "SELECT * FROM FilmTaban ORDER BY FilmAdi"
        tikla.execute(query)

        rows = tikla.fetchall()

        #! Mevcut verileri temizler
        for item in tablo.get_children():
            tablo.delete(item)

        # !Yeni Verileri Ekler
        for row in rows:
            tablo.insert('', 'end', values=row)

        result_str = ""
        for row in rows:
            result_str += str(row) + "\n"

        # !Sonucu mesaj kutusunda gösterir
        messagebox.showinfo(title="Film", message=result_str)

        tikla.close()

    def zaman():
        zaman_format=time.strftime('%H:%M:%S')
        zmn_label.config(text=zaman_format)
        zmn_label.after(200,zaman)

    def FilmSayisiniGoster():
        tikla.execute("SELECT COUNT(*) FROM FilmTaban")
        film_sayisi = tikla.fetchone()[0]
        messagebox.showinfo(title="Film Sayısı", message=f"Toplamda {film_sayisi} adet film bulunmaktadır.")

    def EvetOscar(row):
        return row[:-1] + ("Evet",) if row[-1] == 1 else row

    def OscarliFilmler(tablo):
        tikla.execute('SELECT * FROM FilmTaban WHERE Oscar = 1')
        rows = tikla.fetchall()

        for item in tablo.get_children():
            tablo.delete(item)

        for row in rows:
            tablo.insert('', 'end', values=EvetOscar(row))

    def KaçYönetmenVar():

        tikla = connection.cursor()
        tikla.execute("SELECT COUNT(DISTINCT Yonetmen) FROM FilmTaban")
        yönetmen_sayısı = tikla.fetchone()[0]
        messagebox.showinfo(title="Yönetmen Sayısı", message=f"Toplamda {yönetmen_sayısı} farklı yönetmen bulunmaktadır.")
        tikla.close()

    def IMDBUSTU():
        tikla.execute('SELECT FilmAdi,IMDB,Kategori FROM FilmTaban WHERE IMDB>8.5')
        rows = tikla.fetchall()

        tablo.delete(*tablo.get_children())  # Tablodaki mevcut verileri temizle

        for row in rows:
            tablo.insert('', 'end', values=row)

    def KacUlkedenFilmVar():
        tikla = connection.cursor()

        query = "SELECT Ulke, COUNT(*) AS sayı FROM FilmTaban GROUP BY Ulke"
        tikla.execute(query)

        rows = tikla.fetchall()

        #! Mevcut verileri temizler
        for item in tablo.get_children():
            tablo.delete(item)

        # !Yeni Verileri Ekler
        for row in rows:
            tablo.insert('', 'end', values=row)

        result_str = "Sonuç Tabloya Gelmiştir"

        # !Sonucu mesaj kutusunda gösterir
        messagebox.showinfo(title="Film", message=result_str)

        tikla.close()

    # !PENCERE AYARLARI
    form = tk.Tk()
    form.title("FilmTabanı")
    form.geometry("1280x720+120+50")  #!Pencere boyutu ayarladım '120+50' Pencerenin ekranda nerede açılacağını ayarladım.
    form.config(bg="beige")
    form.resizable(True, True)



    button_image_23 = PhotoImage(
    file=relative_to_assets("button_23.png"))
    button_23 = Button(
        image=button_image_23,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: print("button_23 clicked"),
        relief="flat"
    )
    button_23.place(
        x=530.0,
        y=23.0,
        width=370.0,
        height=43.0
    )

    zmn_label=tk.Label(bg="beige", font="Time 28 bold")
    zmn_label.place(x=1370, y=720)
    zaman()

    misir= ImageTk.PhotoImage(Image.open("C://Users//askar//OneDrive//Masaüstü//misir.jpg"))
    buton1=tk.Button(form,image=misir)
    buton1.pack()
    buton1.place(x=1380, y=10, width=200, height=150)

    #!YAPILABİLECEK İŞLEMLER
    listelefilm=tk.Label(form, text="Tüm Filmleri Listele", fg="Black", bg="beige", font="Times 9 bold")
    listelefilm.place(x=9, y=150) 
    #!YAPİM YİLİ
    yapim_yili=tk.Label(form, text="Yapım Yılına Göre Listele", fg="Black", bg="beige", font="Times 9 bold")
    yapim_yili.place(x=10, y=200)
    yapim_yili_giris=tk.Entry(form) 
    yapim_yili_giris.pack()
    yapim_yili_giris.place(x=150, y=200)
    #!YÖNETMEN
    yonetmen=tk.Label(form, text="Yönetmene Göre Filmleri Listele", fg="Black", bg="beige", font="Times 9 bold")
    yonetmen.place(x=10, y=250)
    yonetmen_giris=tk.Entry(form)
    yonetmen_giris.pack()
    yonetmen_giris.place(x=190, y=250)
    #!OYUNCULAR
    oyuncular=tk.Label(form, text="Oyunculara Göre Filmleri Listele", fg="Black", bg="beige", font="Times 9 bold")
    oyuncular.place(x=10, y=300)
    oyuncular_giris=tk.Entry(form)
    oyuncular_giris.pack()
    oyuncular_giris.place(x=190, y=300)
    #!KATEGORİ
    kategori=tk.Label(form, text="Kategoriye Göre Filmleri Listele", fg="Black", bg="beige", font="Times 9 bold")
    kategori.place(x=10, y=350)
    kategori_giris=tk.Entry(form)
    kategori_giris.pack()
    kategori_giris.place(x=190, y=350)
    #!FİLM ADI
    film_adi=tk.Label(form, text="Film Adına Göre Bilgileri Getir", fg="Black", bg="beige", font="Times 9 bold")
    film_adi.place(x=10, y=400)
    film_adi_giris=tk.Entry(form)
    film_adi_giris.pack()
    film_adi_giris.place(x=190, y=400)
    #!ÜLKE
    ulke=tk.Label(form, text="Ülkeye Göre Filmleri Getir", fg="Black", bg="beige", font="Times 9 bold")
    ulke.place(x=10, y=450)
    ulke_giris=tk.Entry(form)
    ulke_giris.pack()
    ulke_giris.place(x=190, y=450)
    #!IMDB
    imdb=tk.Label(form, text="IMDB Puanına Göre Filmleri Getir", fg="Black", bg="beige", font="Times 9 bold")
    imdb.place(x=10, y=500)
    imdb_giris=tk.Entry(form)
    imdb_giris.pack()
    imdb_giris.place(x=190, y=500)
    #!IMDB PUAN ARALIK
    imdlimitli=tk.Label(form, text="IMDB Puan Aralığına Göre Filmleri Getir", fg="Black", bg="beige", font="Times 9 bold")
    imdlimitli.place(x=10, y=550)
    imdb_alt_limit_giris = tk.Entry(form)
    imdb_alt_limit_giris.pack()
    imdb_alt_limit_giris.place(x=230, y=550)

    imdb_ust_limit_giris = tk.Entry(form)
    imdb_ust_limit_giris.pack()
    imdb_ust_limit_giris.place(x=360, y=550)
    #!YAPIM YILI ARALIK
    yapimyili_aralik=tk.Label(form, text="Yapım Yılı Aralığına Göre Filmleri Getir", fg="Black", bg="beige", font="Times 9 bold")
    yapimyili_aralik.place(x=10, y=600)
    yapim_yili_alt_limit_giris = tk.Entry(form)
    yapim_yili_alt_limit_giris.pack()
    yapim_yili_alt_limit_giris.place(x=230, y=600)

    yapim_yili_ust_limit_giris = tk.Entry(form)
    yapim_yili_ust_limit_giris.pack()
    yapim_yili_ust_limit_giris.place(x=360, y=600)
    #!IMDB ÇOKTAN AZA DOĞRU
    imdbsiralama=tk.Label(form, text="IMDB Puanını Çoktan Aza Doğru Sırala", fg="Black", bg="beige", font="Times 9 bold")
    imdbsiralama.place(x=550, y=150)
    #!ALFABETİK SIRAYA GÖRE
    alfabetik=tk.Label(form, text="Alfabetik Sıraya Göre Liste", fg="Black", bg="beige", font="Times 9 bold")
    alfabetik.place(x=550, y=200)
    #!KAÇ FARKLı YÖNETMEN VAR
    farkliyonetmen=tk.Label(form,text="Kaç Farklı Yönetmen İsmi Var", fg="Black", bg="beige", font="Times 9 bold")
    farkliyonetmen.place(x=550,y=250)
    # !ESKİDEN YENİYE
    yapim_zamani=tk.Label(form, text="Yeniden Eskiye Göre Listele", fg="Black", bg="beige", font="Times 9 bold")
    yapim_zamani.place(x=550, y=300)
    #!Seçilen Kategoriden Kaç Tane Film Var
    kategori_sayi=tk.Label(form, text="Seçilen Kategoriden Kaç Tane Film Var", fg="Black", bg="beige", font="Times 9 bold")
    kategori_sayi.place(x=550, y=350)
    #!FİLM SAYISINI GÖSTEREN LABEL
    film_sayi=tk.Label(form, text="VeriTabanında Kaç Tane Film Var", fg="Black", bg="beige", font="Times 9 bold")
    film_sayi.place(x=550, y=400)
    #!OSCAR ALAN FİLMLER
    oscar=tk.Label(form, text="Oscar Almış filmleri Getir", fg="Black", bg="beige", font="Times 9 bold")
    oscar.place(x=550, y=450)
    #!EN YÜKSEK IMDB PUANI
    yuksekimdb = tk.Label(form, text="En Yüksek IMDB Puanı Kaç", fg="Black",bg="beige", font="Times 9 bold")
    yuksekimdb.place(x=550, y=500)
    #!IMDB Puanı 8 üstü olan filmleri getirt.
    imdb8=tk.Label(form, text="IMDB Puanı 8 üstü olan filmleri getirt.", fg="Black", bg="beige", font="Times 9 bold")
    imdb8.place(x=550, y=550) 
    #! Tablodan 3 Sütun Veri Getirme ÜLKEYE GÖRE
    ulkesutun=tk.Label(form, text="Yazılan ülkeye göre 3 başlık altında veri getirme", fg="Black", bg="beige", font="Times 9 bold")
    ulkesutun.place(x=920, y=150)
    ulke_girissutun=tk.Entry(form)
    ulke_girissutun.pack()
    ulke_girissutun.place(x=1180, y=150)
    #! HER ÜLKEDEN KAÇ FİLM OLDUĞUNU GÖSTERME
    kacfilm=tk.Label(form, text="Her ülkeden kaç film var", fg="Black", bg="beige", font="Times 9 bold")
    kacfilm.place(x=920, y=200)


                #*YAPILABİLECEK İŞLEMLERİN BUTONLARI
    #!TÜM FİLMLERİ LİSTELE BUTONU
    button_image_3 = PhotoImage(
    file=relative_to_assets("button_3.png"))
    button_3 = Button(
        image=button_image_3,
        borderwidth=0,
        highlightthickness=0,
        command=Filmler,
        relief="flat"
    )
    button_3.place(
        x=120,
        y=150,
        width=50.0,
        height=20.0
    )
    #!HER ÜLKEDEN KAÇ FİLM BUTONU
    button_image_17 = PhotoImage(
    file=relative_to_assets("button_17.png"))
    button_17 = Button(
        image=button_image_17,
        borderwidth=0,
        highlightthickness=0,
        command=KacUlkedenFilmVar,
        relief="flat"
    )
    button_17.place(
        x=1060.0,
        y=200.0,
        width=49.17808151245117,
        height=19.829059600830078
    )
    #!YÖNETMEN TABLOSUNU AÇAN BUTON
    yonetmen_tablosu_button = tk.Button(form, text="Yönetmen Tablosunu Göster", fg="Black", bg="white", font="Times 10 bold", command=YonetmenTablosunuGoster)
    yonetmen_tablosu_button.pack()
    yonetmen_tablosu_button.place(x=10, y=650, width=200, height=30)
    #!OYUNCU TABLOSUNU AÇAN BUTON
    oyuncu_tablosu_button = tk.Button(form, text="Oyuncu Tablosunu Göster", fg="Black", bg="White", font="Times 10 bold ", command=OyuncuTablosunuGoster)
    oyuncu_tablosu_button.pack()
    oyuncu_tablosu_button.place(x=450, y= 650, width=200, height=30)
    #!YAPIM YILINA GÖRE LİSTELE BUTONU
    button_image_4 = PhotoImage(
    file=relative_to_assets("button_4.png"))
    button_4 = Button(
        image=button_image_4,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: Yapimm(tablo),
        relief="flat"
    )
    button_4.place(
        x=275,
        y=200,
        width=50.0,
        height=20.0
    )
    #!YÖNETMENE GÖRE LİSTELE BUTONU
    button_image_5 = PhotoImage(
    file=relative_to_assets("button_5.png"))
    button_5 = Button(
        image=button_image_5,
        borderwidth=0,
        highlightthickness=0,
        command=lambda:YonetmeneGore(tablo),
        relief="flat"
    )
    button_5.place(
        x=318.0,
        y=250.0,
        width=50.0,
        height=20.0
    )
    #!OYUNCULARA GÖRE LİSTELE BUTONU
    button_image_6 = PhotoImage(
    file=relative_to_assets("button_6.png"))
    button_6 = Button(
        image=button_image_6,
        borderwidth=0,
        highlightthickness=0,
        command=lambda:OyuncularaGore(tablo),
        relief="flat"
    )
    button_6.place(
        x=320.0,
        y=300.0,
        width=50.0,
        height=20.0
    )
    #!KATEGORİYE GÖRE LİSTELE BUTON
    button_image_7 = PhotoImage(
    file=relative_to_assets("button_7.png"))
    button_7 = Button(
        image=button_image_7,
        borderwidth=0,
        highlightthickness=0,
        command=lambda:KategoriyeGore(tablo),
        relief="flat"
    )
    button_7.place(
        x=320.0,
        y=350.0,
        width=50.0,
        height=20.0
    )
    #!FİLM ADINA GÖRE LİSTELE BUTONU
    button_image_8 = PhotoImage(
    file=relative_to_assets("button_8.png"))
    button_8 = Button(
        image=button_image_8,
        borderwidth=0,
        highlightthickness=0,
        command=lambda:FilmeGore(tablo),
        relief="flat"
    )
    button_8.place(
        x=320.0,
        y=400.0,
        width=50.0,
        height=20.0
    )
    #!ÜLKEYE GÖRE LİSTELE BUTONU
    button_image_9 = PhotoImage(
    file=relative_to_assets("button_9.png"))
    button_9 = Button(
        image=button_image_9,
        borderwidth=0,
        highlightthickness=0,
        command=lambda:UlkeyeGore(tablo),
        relief="flat"
    )
    button_9.place(
        x=320.0,
        y=450.0,
        width=50.0,
        height=20.0
    )
    #!ÜLKEYE GÖRE 3 SÜTUNDAN VERİ GETİRME
    button_image_22 = PhotoImage(
    file=relative_to_assets("button_22.png"))
    button_22 = Button(
        image=button_image_22,
        borderwidth=0,
        highlightthickness=0,
        command=lambda:UlkeSutunu(tablo),
        relief="flat"
    )
    button_22.place(
        x=1310.0,
        y=150.0,
        width=50.0,
        height=20.0
    )
    #!IMDB PUANINA GÖRE LİSTELE BUTONU
    button_image_10 = PhotoImage(
    file=relative_to_assets("button_10.png"))
    button_10 = Button(
        image=button_image_10,
        borderwidth=0,
        highlightthickness=0,
        command=lambda:IMDByeGore(tablo),
        relief="flat"
    )
    button_10.place(
        x=320.0,
        y=500.0,
        width=50.0,
        height=20.0
    )
    #!IMDB Puan Aralığı'na Göre LİSTELE BUTONU
    button_image_11 = PhotoImage(
    file=relative_to_assets("button_11.png"))
    button_11 = Button(
        image=button_image_11,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: IMDbAraliginaGore(tablo),
        relief="flat"
    )
    button_11.place(
        x=490.0,
        y=550.0,
        width=50.0,
        height=20.0
    )
    #!YAPIM YILI ARALIK
    button_image_12 = PhotoImage(
    file=relative_to_assets("button_12.png"))
    button_12 = Button(
        image=button_image_12,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: YapimYiliAraliginaGore(tablo),
        relief="flat"
    )
    button_12.place(
        x=490.0,
        y=600.0,
        width=50.0,
        height=20.0
    )
    #!IMDB PUANI ÇOKTAN AZA DOĞRU
    button_image_13 = PhotoImage(
    file=relative_to_assets("button_13.png"))
    button_13 = Button(
        image=button_image_13,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: IMDbYuksektenDuse(tablo),
        relief="flat"
    )
    button_13.place(
        x=770.0,
        y=150.0,
        width=49.17808151245117,
        height=19.829059600830078
    )
    #!Alfabetik İsme Göre Listele butonu
    button_image_14 = PhotoImage(
    file=relative_to_assets("button_14.png"))
    button_14 = Button(
        image=button_image_14,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: AlfabetikIsmeGore(tablo),
        relief="flat"
    )
    button_14.place(
        x=720.0,
        y=200.0,
        width=49.17808151245117,
        height=19.829059600830078
    )
    #!KAÇ FARKLI YÖNETMEN
    button_image_15 = PhotoImage(
    file=relative_to_assets("button_15.png"))
    button_15 = Button(
        image=button_image_15,
        borderwidth=0,
        highlightthickness=0,
        command=KaçYönetmenVar,
        relief="flat"
    )
    button_15.place(
        x=720.0,
        y=250.0,
        width=49.17808151245117,
        height=19.829059600830078
    )
    #!YAPIM YILI ESKİDEN YENİYE
    button_image_16 = PhotoImage(
    file=relative_to_assets("button_16.png"))
    button_16 = Button(
        image=button_image_16,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: YapimYilinaGore(tablo),
        relief="flat"
    )
    button_16.place(
        x=720.0,
        y=300.0,
        width=49.17808151245117,
        height=19.829059600830078
    )
    #!KATEGORİDEN KAÇ TANE FİLM VAR
    kategori_combobox = ttk.Combobox(form, values=["Aksiyon","Animasyon", "Dram", "Komedi", "Romantik", "Bilim Kurgu", "Korku", "Gerilim", "Fantastik"])
    kategori_combobox.bind("<<ComboboxSelected>>", KategoriSecildi)
    kategori_combobox.pack()
    kategori_combobox.place(x=760, y=350)
    #!FİLM SAYISINI GÖSTER
    button_image_18 = PhotoImage(
    file=relative_to_assets("button_18.png"))
    button_18 = Button(
        image=button_image_18,
        borderwidth=0,
        highlightthickness=0,
        command=FilmSayisiniGoster,
        relief="flat"
    )
    button_18.place(
        x=730.0,
        y=400.0,
        width=49.17808151245117,
        height=19.829059600830078
    )
    #!OSCAR ALINAN FİLMLERİ
    button_image_20 = PhotoImage(
    file=relative_to_assets("button_20.png"))
    button_20 = Button(
        image=button_image_20,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: OscarliFilmler(tablo),
        relief="flat"
    )
    button_20.place(
        x=700.0,
        y=450.0,
        width=49.17808151245117,
        height=19.829059600830078
    )
    #!EN YUKSE IMDB 
    button_image_21 = PhotoImage(
    file=relative_to_assets("button_21.png"))
    button_21 = Button(
        image=button_image_21,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: YuksekIMDB(),
        relief="flat"
    )
    button_21.place(
        x=700.0,
        y=500.0,
        width=49.17808151245117,
        height=19.829059600830078
    )
    #!IMDB Puanı 8 üstü olan filmleri getirt. BUTON
    button_image_19 = PhotoImage(
    file=relative_to_assets("button_19.png"))
    button_19 = Button(
        image=button_image_19,
        borderwidth=0,
        highlightthickness=0,
        command=IMDBUSTU,
        relief="flat"
    )
    button_19.place(
        x=760.0,
        y=550.0,
        width=49.17808151245117,
        height=19.829059600830078
    )


    if __name__ == "__main__":
        root = tk.Tk()
        tablo = VeriTablo(root)
        root.mainloop()
        form.mainloop()
    connection.close()


if __name__ == "__main__":
    main()