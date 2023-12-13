import queue
import threading
import time
import tkinter as tk
from tkinter import simpledialog


class GarsonArayuzu:
    def __init__(self, pencere, asci_arayuzu):
        self.pencere = pencere
        self.pencere.title("Garson Arayüzü")

        self.asci_arayuzu = asci_arayuzu

        # Masa sayısı
        self.masa_sayisi = 6

        # Masa ve siparişlerin tutulacağı sözlük
        self.masalar = {masa_numarasi: {"siparis": "", "durum": "Boş", "thread": None} for masa_numarasi in range(1, self.masa_sayisi + 1)}

        # Arayüzü oluştur
        self.arayuzu_olustur()

    def arayuzu_olustur(self):
        # Masa butonlarını oluştur
        for masa_numarasi in range(1, self.masa_sayisi + 1):
            tk.Button(self.pencere, text=f"Masa {masa_numarasi}", command=lambda numara=masa_numarasi: self.siparis_al(numara)).grid(row=masa_numarasi, column=0, padx=5, pady=5)

    def siparis_al(self, masa_numarasi):
        if self.masalar[masa_numarasi]["thread"] is None or not self.masalar[masa_numarasi]["thread"].is_alive():
            siparis = simpledialog.askstring("Sipariş Al", f"Masa {masa_numarasi} Sipariş:")
            if siparis:
                self.masalar[masa_numarasi]["siparis"] = siparis
                self.masalar[masa_numarasi]["durum"] = "Dolu"
                self.asci_arayuzu.siparisi_ilet(masa_numarasi, siparis)

class AsciArayuzu:
    def __init__(self, pencere):
        self.pencere = pencere
        self.pencere.title("Aşçı Arayüzü")

        # Aşçı sayısı ve sipariş kuyruğu oluştur
        self.asci_sayisi = 2
        self.siparis_kuyrugu = queue.Queue()

        # Aşçı butonlarını oluştur
        for asci_numarasi in range(1, self.asci_sayisi + 1):
            tk.Button(self.pencere, text=f"Aşçı {asci_numarasi}", command=lambda numara=asci_numarasi: self.siparisi_al(numara)).grid(row=asci_numarasi, column=0, padx=5, pady=5)

    def siparisi_ilet(self, masa_numarasi, siparis):
        self.siparis_kuyrugu.put((masa_numarasi, siparis))

    def siparisi_al(self, asci_numarasi):
        if not self.siparis_kuyrugu.empty():
            masa_numarasi, siparis = self.siparis_kuyrugu.get()
            print(f"Aşçı {asci_numarasi} - Masa {masa_numarasi} Sipariş: {siparis}")
            time.sleep(5)  # Siparişin hazırlanma sürecini simüle etmek için bekleme
            print(f"Aşçı {asci_numarasi} - Masa {masa_numarasi} Sipariş Hazır!")


if __name__ == "__main__":
    #garson ekranı
    garson = tk.Tk()
    garson.geometry("400x300")
    garson.geometry("+10+10")

    #aşçı ekranı
    asci = tk.Tk()
    asci.title("Aşçı Ekranı")
    asci.geometry("400x300")
    asci.geometry("+1100+10")

    #kasa ekranı
    kasa = tk.Tk()
    kasa.title("Kasa ekranı")
    kasa.geometry("400x300")
    kasa.geometry("+500+400")

    asci_arayuzu = AsciArayuzu(asci)

    garson_arayuzu = GarsonArayuzu(garson, asci_arayuzu)

    garson.mainloop()
    asci.mainloop()
    kasa.mainloop()