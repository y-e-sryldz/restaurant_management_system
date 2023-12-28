import tkinter as tk
from tkinter import simpledialog
import queue
import threading
import time

class GarsonArayuzu:
    def __init__(self, pencere, asci_arayuzu):
        self.pencere = pencere
        self.pencere.title("Garson Arayüzü")
        self.pencere.geometry("400x300+200+200")
        self.asci_arayuzu = asci_arayuzu

        # Masa sayısı
        self.masa_sayisi = 6

        # Masa ve siparişlerin tutulacağı sözlük
        self.masalar = {masa_numarasi: {"siparisler": [], "durum": "Boş", "yas_kontrolu": None, "thread": None, "musteri": None} for masa_numarasi in range(1, self.masa_sayisi + 1)}

        # Arayüzü oluştur
        self.arayuzu_olustur()
        # Garson arayüzüne referans ekleyin
        self.garson_arayuzu = self
        self.bekleyen_musteriler = []

    def siradakini_ekle(self):
        if self.bekleyen_musteriler:
            bekleyen_musteri = self.bekleyen_musteriler.pop(0)
            masa_numarasi = simpledialog.askinteger("Masa Seç", "Müşteri eklemek istediğiniz masa numarasını girin:")

            if masa_numarasi:
                print(f"Sıradaki müşteri {bekleyen_musteri.get('musteri_adi')}, Masa {masa_numarasi}'ye oturdu.")
                print(
                    f"Bekleyen müşteriler: {', '.join(musteri.get('musteri_adi') for musteri in self.bekleyen_musteriler)}")
                # Masa durumunu güncelle
                self.masa_durumu_guncelle(masa_numarasi, "Dolu")
                # Müşteri bilgisini sınıfa ekle
                self.masalar[masa_numarasi]["musteri"] = bekleyen_musteri.get("musteri_adi")
            else:
                print("Masaya müşteri oturtulamadı, masa_numarasi None.")

            # Diğer işlemleri ekleyebilirsiniz
        else:
            print("Bekleyen müşteri bulunmamaktadır.")

    def arayuzu_olustur(self):
        # Masa butonlarını ve yaş kontrolü için checkbox'ları oluştur
        for masa_numarasi in range(1, self.masa_sayisi + 1):
            tk.Button(self.pencere, text=f"Masa {masa_numarasi}", command=lambda numara=masa_numarasi: self.siparis_al(numara)).grid(row=masa_numarasi, column=0, padx=5, pady=5)
            yas_kontrol = tk.BooleanVar()
            yas_kontrol.set(False)
            yas_onay = tk.Checkbutton(self.pencere, text="65 yaş ve üzeri", variable=yas_kontrol)
            yas_onay.grid(row=masa_numarasi, column=1, padx=5, pady=5)
            self.masalar[masa_numarasi]["yas_kontrolu"] = yas_kontrol

        # Müşteri Ekle Butonu
        tk.Button(self.pencere, text="Müşteri Ekle", command=self.musteri_ekle).grid(row=0, column=0, padx=5, pady=5)
        # Müşteri Ekle Butonu
        tk.Button(self.pencere, text="Müşteri Ekle", command=self.musteri_ekle).grid(row=0, column=0, padx=5, pady=5)

        # Sıradakini Ekle Butonu
        tk.Button(self.pencere, text="Sıradakini Ekle", command=self.siradakini_ekle).grid(row=0, column=1, padx=5,
                                                                                           pady=5)

        # Sipariş Durumu ve Masa Durumu Gösterimi İçin Etiketler
        tk.Label(self.pencere, text="Sipariş Durumu").grid(row=0, column=2, padx=5, pady=5)
        tk.Label(self.pencere, text="Masa Durumu").grid(row=0, column=3, padx=5, pady=5)

        # Her masa için Sipariş Durumu ve Masa Durumu Gösterimi
        for masa_numarasi in range(1, self.masa_sayisi + 1):
            tk.Label(self.pencere, text="", name=f"siparis_durumu_{masa_numarasi}").grid(row=masa_numarasi, column=2,padx=5, pady=5)
            tk.Label(self.pencere, text="", name=f"masa_durumu_{masa_numarasi}").grid(row=masa_numarasi, column=3, padx=5, pady=5)

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

                # Sipariş durumu güncelle
                self.siparis_durumu_guncelle(masa_numarasi, "Sipariş İletildi")

    def siparis_durumu_guncelle(self, masa_numarasi, durum):
        self.pencere.nametowidget(f"siparis_durumu_{masa_numarasi}").config(text=durum)

    def masa_durumu_guncelle(self, masa_numarasi, durum):
        self.pencere.nametowidget(f"masa_durumu_{masa_numarasi}").config(text=durum)

    def musteri_ekle(self):
        masa_numarasi = simpledialog.askinteger("Masa Seç", "Müşteri eklemek istediğiniz masa numarasını girin (1-6):")

        if masa_numarasi and 1 <= masa_numarasi <= self.masa_sayisi:
            masa_durumu = self.masalar[masa_numarasi]["durum"]

            if masa_durumu == "Boş":
                musteri_ad = simpledialog.askstring("Müşteri Bilgisi", "Müşteri adını girin:")

                if musteri_ad:
                    self.masalar[masa_numarasi]["musteri"] = musteri_ad
                    self.masalar[masa_numarasi]["durum"] = "Dolu"
                    print(f"Masa {masa_numarasi} için {musteri_ad} isimli müşteri eklenmiştir.")
                    # Masa durumunu güncelle
                    self.garson_arayuzu.masa_durumu_guncelle(masa_numarasi, "Dolu")

                else:
                    print("Müşteri adı boş bırakılamaz.")

            elif masa_durumu == "Dolu":
                musteri_ad = simpledialog.askstring("Müşteri Bilgisi", "Müşteri adını girin:")
                print(f"Masa {masa_numarasi} dolu durumdadır. {musteri_ad} müşteri sırasına alınıyor.")
                self.bekleyen_musteriler.append({"musteri_adi": musteri_ad})
                print(f"Bekleyen müşteri sırasına alındı. Bekleyen müşteriler: {', '.join(musteri.get('musteri_adi') for musteri in self.bekleyen_musteriler)}")

class AsciArayuzu:
    def __init__(self, pencere, garson_arayuzu):
        self.pencere = pencere
        self.pencere.title("Aşçı Arayüzü")
        self.pencere.geometry("400x300+800+200")
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

        # Sipariş durumu güncelle
        self.garson_arayuzu.siparis_durumu_guncelle(masa_numarasi, "Hazır")

class KasaArayuzu:
    def __init__(self, pencere, garson_arayuzu):
        self.pencere = pencere
        self.pencere.title("Kasa Arayüzü")
        self.pencere.geometry("400x300+1400+200")
        self.garson_arayuzu = garson_arayuzu
        self.pencere.after(1000, self.otomatik_guncelle)
        # Dolu masaların listesini tutan bir ListBox ekleyin
        self.dolu_masalar_listesi = tk.Listbox(self.pencere)
        self.dolu_masalar_listesi.grid(row=1, column=0, padx=5, pady=5)
        self.secili_masa = None
        self.dolu_masalar_listesi.bind("<ButtonRelease-1>", self.masa_sec)

        # Ödeme butonunu ekleyin
        tk.Button(self.pencere, text="Ödeme Yap", command=self.odeme_yap).grid(row=0, column=0, padx=5, pady=5)

        # Dolu masalar listesini güncelle
        self.guncelle_dolu_masalar_listesi()

    def otomatik_guncelle(self):
        # Otomatik olarak dolu masalar listesini güncelle
        self.guncelle_dolu_masalar_listesi()

        # Timer'ı bir sonraki güncelleme için tekrar başlat
        self.pencere.after(1000, self.otomatik_guncelle)

    def masa_sec(self, event):
        # Listbox'tan seçili masa numarasını al
        selected_index = self.dolu_masalar_listesi.curselection()
        if selected_index:
            masa_numarasi = int(self.dolu_masalar_listesi.get(selected_index).split()[-1])

            # Seçili masayı ödeme yapmak için sakla
            self.secili_masa = f"Masa {masa_numarasi}"
            print(f"Seçili Masa: {self.secili_masa}")
        else:
            print("Lütfen bir masa seçin.")

    def odeme_yap(self):
        if self.secili_masa:
            # Masa numarasını al
            masa_numarasi = int(self.secili_masa.split()[-1])

            # Sipariş durumunu "Boş" olarak güncelle
            self.garson_arayuzu.siparis_durumu_guncelle(masa_numarasi, "")

            # Masa durumunu "Boş" olarak güncelle
            self.garson_arayuzu.masalar[masa_numarasi]["durum"] = "Boş"
            self.garson_arayuzu.masa_durumu_guncelle(masa_numarasi, "")

            # Müşteri bilgisini temizle
            self.garson_arayuzu.masalar[masa_numarasi]["musteri"] = None

            # Dolu masalar listesinden seçili masayı sil
            self.dolu_masalar_listesi.delete(tk.ACTIVE)

            # Ödeme yapıldı mesajını ekrana yazdır
            print("Ödeme yapılıyor...")
            time.sleep(1)  # Ödeme işlemi için 1 saniye bekleme
            print("Ödeme yapıldı -", self.secili_masa)

            # Seçili masayı sıfırla
            self.secili_masa = None

            # Dolu masalar listesini güncelle
            self.guncelle_dolu_masalar_listesi()

    def guncelle_dolu_masalar_listesi(self):
        # Dolu masalar listesini güncelle
        self.dolu_masalar_listesi.delete(0, tk.END)
        for masa_numarasi, masa in self.garson_arayuzu.masalar.items():
            if masa["durum"] == "Dolu":
                self.dolu_masalar_listesi.insert(tk.END, f"Masa {masa_numarasi}")


def run_kasa_arayuzu(garson_arayuzu):
    root_kasa = tk.Tk()
    kasa_arayuzu = KasaArayuzu(root_kasa, garson_arayuzu)
    root_kasa.mainloop()

def run_garson_arayuzu():
    root = tk.Tk()
    garson_pencere = tk.Toplevel(root)
    asci_pencere = tk.Toplevel(root)

    asci_arayuzu = AsciArayuzu(asci_pencere, None)
    garson_arayuzu = GarsonArayuzu(garson_pencere, asci_arayuzu)

    # asci_arayuzu'nu garson_arayuzu'na atayın
    asci_arayuzu.garson_arayuzu = garson_arayuzu

    # Kasa arayüzünü başlatın
    run_kasa_arayuzu(garson_arayuzu)

    root.mainloop()

if __name__ == "__main__":
    garson_thread = threading.Thread(target=run_garson_arayuzu)
    garson_thread.start()