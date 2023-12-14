import tkinter as tk
from tkinter import simpledialog
import queue
import time

class GarsonArayuzu:
    def __init__(self, pencere, asci_arayuzu):
        self.pencere = pencere
        self.pencere.title("Garson Arayüzü")
        self.asci_arayuzu = asci_arayuzu

        # Masa sayısı
        self.masa_sayisi = 6

        # Masa ve siparişlerin tutulacağı sözlük
        self.masalar = {masa_numarasi: {"siparisler": [], "durum": "Boş", "yas_kontrolu": None, "thread": None} for masa_numarasi in range(1, self.masa_sayisi + 1)}

        # Arayüzü oluştur
        self.arayuzu_olustur()

    def arayuzu_olustur(self):
        # Masa butonlarını ve yaş kontrolü için checkbox'ları oluştur
        for masa_numarasi in range(1, self.masa_sayisi + 1):
            tk.Button(self.pencere, text=f"Masa {masa_numarasi}", command=lambda numara=masa_numarasi: self.siparis_al(numara)).grid(row=masa_numarasi, column=0, padx=5, pady=5)
            yas_kontrol = tk.BooleanVar()
            yas_kontrol.set(False)
            yas_onay = tk.Checkbutton(self.pencere, text="65 yaş ve üzeri", variable=yas_kontrol)
            yas_onay.grid(row=masa_numarasi, column=1, padx=5, pady=5)
            self.masalar[masa_numarasi]["yas_kontrolu"] = yas_kontrol

    def siparis_al(self, masa_numarasi):
        if self.masalar[masa_numarasi]["thread"] is None or not self.masalar[masa_numarasi]["thread"].is_alive():
            yas_kontrol = self.masalar[masa_numarasi]["yas_kontrolu"].get()

            # Eğer yaş kontrolü işaretli değilse sadece sipariş almak üzere bir diyalog penceresi göster
            siparis = simpledialog.askstring("Sipariş Al", f"Masa {masa_numarasi} Sipariş:")
            if siparis:
                self.masalar[masa_numarasi]["siparisler"].append({"siparis": siparis, "yas": None})
                self.masalar[masa_numarasi]["durum"] = "Dolu"
                # Sipariş bilgisini aşçı arayüzüne ileti
                self.asci_arayuzu.siparisi_ilet(masa_numarasi, yas_kontrol)

class AsciArayuzu:
    def __init__(self, pencere, garson_arayuzu):
        self.pencere = pencere
        self.pencere.title("Aşçı Arayüzü")
        self.garson_arayuzu = garson_arayuzu

        # Aşçı sayısı ve sipariş kuyrukları oluştur
        self.asci_sayisi = 2
        self.oncekiler_kuyrugu = queue.Queue()
        self.siparis_kuyrugu = queue.Queue()

        # Aşçı butonlarını oluştur
        for asci_numarasi in range(1, self.asci_sayisi + 1):
            tk.Button(self.pencere, text=f"Aşçı {asci_numarasi}", command=lambda numara=asci_numarasi: self.siparisi_al(numara)).grid(row=asci_numarasi, column=0, padx=5, pady=5)

    def siparisi_ilet(self, masa_numarasi, yas_kontrol):
        # Sipariş bilgisini kuyruklara ekleyerek iletişimi sağla
        if yas_kontrol:
            self.oncekiler_kuyrugu.put((masa_numarasi, yas_kontrol))
        else:
            self.siparis_kuyrugu.put(masa_numarasi)

    def siparisi_al(self, asci_numarasi):
        # Öncelikli kuyruktan öncelikli sipariş al
        if not self.oncekiler_kuyrugu.empty():
            masa_numarasi, yas_kontrol = self.oncekiler_kuyrugu.get()
            self.hazirla_ve_bildir(masa_numarasi, yas_kontrol, asci_numarasi)
        elif not self.siparis_kuyrugu.empty():
            masa_numarasi = self.siparis_kuyrugu.get()
            self.hazirla_ve_bildir(masa_numarasi, False, asci_numarasi)

    def hazirla_ve_bildir(self, masa_numarasi, yas_kontrol, asci_numarasi):
        # Siparişi hazırla ve aşçının işini tamamladığını bildir
        if yas_kontrol:
            print(f"Aşçı {asci_numarasi} - Öncelikli Masa {masa_numarasi} Siparişi Hazırlanıyor...")
        else:
            print(f"Aşçı {asci_numarasi} - Masa {masa_numarasi} Siparişi Hazırlanıyor...")

        # Yaş kontrolü yap, 65 yaş ve üzeri ise bekleme süresini kısalt
        bekleme_suresi = 5 if yas_kontrol else 2
        time.sleep(bekleme_suresi)  # Siparişin hazırlanma sürecini simüle etmek için bekleme

        if yas_kontrol:
            print(f"Aşçı {asci_numarasi} - Öncelikli Masa {masa_numarasi} Siparişi Hazır!")
        else:
            print(f"Aşçı {asci_numarasi} - Masa {masa_numarasi} Siparişi Hazır!")

if __name__ == "__main__":
    root = tk.Tk()
    garson_pencere = tk.Toplevel(root)
    asci_pencere = tk.Toplevel(root)

    asci_arayuzu = AsciArayuzu(asci_pencere, None)  # None, aşçı arayüzü için bir ana pencere olmadığını belirtir
    garson_arayuzu = GarsonArayuzu(garson_pencere, asci_arayuzu)

    root.mainloop()
