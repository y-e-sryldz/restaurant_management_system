import tkinter as tk




if __name__ == "__main__":
    #garson ekranı
    garson = tk.Tk()
    garson.title("Garson ekranı")

    garson.geometry("800x600")
    garson.geometry("+10+10")

    for i in range(1,7):
        button = tk.Button(garson, text=str(i), width=8, height=5, command=lambda numara=i: butona_bas(numara))
        button.grid(row=0, column=i - 1, padx=5, pady=5)

    metin_giris = tk.Entry(garson,width=10)
    metin_giris.grid(row=0, column=1, padx=5, pady=10)

    def butona_bas(numara):
        print(f"Buton {numara}'ye basıldı.")



    #aşçı ekranı
    asci = tk.Tk()
    asci.title("Aşçı Ekranı")

    asci.geometry("800x600")
    asci.geometry("+1100+10")

    #kasa ekranı
    kasa = tk.Tk()
    kasa.title("Kasa ekranı")

    kasa.geometry("800x600")
    kasa.geometry("+500+400")

    garson.mainloop()
    asci.mainloop()
    kasa.mainloop()