import tkinter as tk
from tkinter import messagebox


class PlayerInfoGUI:
    def __init__(self, master, players): # Oyuncu bilgileri penceresinin oluşturulması ve ayarlanması
        self.master = master
        self.players = players
        self.current_player_index = 0  # O anki oyuncunun indeksi

        self.top = tk.Toplevel(master)
        self.top.title("Oyuncu Bilgileri")
        # Oyuncu bilgilerini göstermek için etiketler oluşturulur ve düzenlenir
        self.label_player_name = tk.Label(self.top, text="Oyuncu Adı:")
        self.label_player_name.grid(row=0, column=0, padx=5, pady=5)
        self.label_resource = tk.Label(self.top, text="Kaynak Miktarı:")
        self.label_resource.grid(row=1, column=0, padx=5, pady=5)
        self.label_health = tk.Label(self.top, text="Can:")
        self.label_health.grid(row=2, column=0, padx=5, pady=5)

        self.display_player_info() # Oyuncu bilgilerinin gösterilmesi
        # "Sonraki Oyuncu" butonunun oluşturulması ve düzenlenmesi
        self.next_button = tk.Button(self.top, text="Sonraki Oyuncu", command=self.next_player)
        self.next_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

    def display_player_info(self): # Mevcut oyuncunun bilgilerini göster
        player = self.players[self.current_player_index]
        self.label_player_name.config(text=f"Oyuncu Adı: {player.name}")
        self.label_resource.config(text=f"Kaynak Miktarı: {player.resources}")
        self.label_health.config(text=f"Can: {player.health}")

    def next_player(self): # Bir sonraki oyuncuya geç
        self.current_player_index = (self.current_player_index + 1) % len(self.players)
        self.display_player_info()

# Oyuncu sınıfını güncelleyerek health (can) özelliğini ekleyin
class Player: # Oyuncu sınıfının oluşturulması ve özelliklerinin belirlenmesi
    def __init__(self, name, resources):
        self.name = name
        self.resources = resources# Oyuncunun kaynak miktarı
        self.health = 1  # Tüm oyuncuların başlangıçta 1 canı var
players = [
    Player("Oyuncu 1", 200),
    Player("Oyuncu 2", 200),
    Player("Oyuncu 3", 200),
    Player("Oyuncu 4", 200)
]
class Warrior:
    def __init__(self, canvas, row, col, nearest_guard_color):
        self.canvas = canvas
        self.row = row
        self.col = col
        self.nearest_guard_color = nearest_guard_color
        self.draw()

    def draw(self):
        raise NotImplementedError("Çizim yöntemi alt sınıflarda uygulanmalıdır.")# Alt sınıfların draw metodu çağrılacak, bu sınıfta NotImplementedError hatası alınır.
 #Bu sınıfın draw metodu alt sınıflar tarafından uygulanmalıdır, çünkü her savaşçı farklı şekillerde çizilebilir. Eğer alt sınıflar bu metodu uygulamazsa, hatası alınır.

class Muhafız(Warrior):
    def draw(self): #Her bir sınıfın draw metodu, o sınıfa özgü bir şekilde savaşçıyı çizer.
        x = self.col * 30 + 15
        y = self.row * 30 + 15
        self.canvas.create_rectangle(x - 15, y - 15, x + 15, y + 15, fill=self.nearest_guard_color, outline='white')
        self.canvas.create_text(x, y, text='M', font=('Arial', 12), fill='white')
        # Muhafızın etrafını çevreleyen dikdörtgenleri çiz
        for i in range(self.row - 1, self.row + 2):
            for j in range(self.col - 1, self.col + 2):
                if (i, j) != (self.row, self.col) and 0 <= i < self.canvas.size and 0 <= j < self.canvas.size:
                    self.canvas.create_rectangle(j * 30, i * 30, (j + 1) * 30, (i + 1) * 30,
                                                 fill=self.nearest_guard_color, outline='white')

class Okçu(Warrior):
    def draw(self):
        x = self.col * 30 + 15#Okçu savaşçısının gövdesinin x koordinatı
        y = self.row * 30 + 15 # Okçu savaşçısının gövdesinin y koordinatı
        # Okçu savaşçısının gövdesini çiz
        self.canvas.create_rectangle(x - 15, y - 15, x + 15, y + 15, fill=self.nearest_guard_color, outline='white')
        # Okçu savaşçısını temsil eden metni çiz
        self.canvas.create_text(x, y, text='O', font=('Arial', 12), fill='white')

        # Okçu savaşçısının etrafını çevreleyen dikdörtgenleri çiz
        for i in range(self.row - 1, self.row + 2):
            for j in range(self.col - 1, self.col + 2):
                # Okçu savaşçısının bulunduğu hücre dışındaki hücreleri kontrol et
                if (i, j) != (self.row, self.col) and 0 <= i < self.canvas.size and 0 <= j < self.canvas.size:
                    # Hücreyi doldur
                    self.canvas.create_rectangle(j * 30, i * 30, (j + 1) * 30, (i + 1) * 30,
                                                 fill=self.nearest_guard_color, outline='white')
class Sağlıkçı(Warrior):
    def draw(self):
        x = self.col * 30 + 15
        y = self.row * 30 + 15
        self.canvas.create_rectangle(x - 15, y - 15, x + 15, y + 15, fill=self.nearest_guard_color, outline='white')
        self.canvas.create_text(x, y, text='S', font=('Arial', 12), fill='white')

        for i in range(self.row - 1, self.row + 2):
            for j in range(self.col - 1, self.col + 2):
                if (i, j) != (self.row, self.col) and 0 <= i < self.canvas.size and 0 <= j < self.canvas.size:
                    self.canvas.create_rectangle(j * 30, i * 30, (j + 1) * 30, (i + 1) * 30,
                                                 fill=self.nearest_guard_color, outline='white')
class Topçu(Warrior):
    def draw(self):
        x = self.col * 30 + 15
        y = self.row * 30 + 15
        self.canvas.create_rectangle(x - 15, y - 15, x + 15, y + 15, fill=self.nearest_guard_color, outline='white')
        self.canvas.create_text(x, y, text='T', font=('Arial', 12), fill='white')

        for i in range(self.row - 1, self.row + 2):
            for j in range(self.col - 1, self.col + 2):
                if (i, j) != (self.row, self.col) and 0 <= i < self.canvas.size and 0 <= j < self.canvas.size:
                    self.canvas.create_rectangle(j * 30, i * 30, (j + 1) * 30, (i + 1) * 30,
                                                 fill=self.nearest_guard_color, outline='white')
class Atlı(Warrior):
    def draw(self):
        x = self.col * 30 + 15
        y = self.row * 30 + 15
        self.canvas.create_rectangle(x - 15, y - 15, x + 15, y + 15, fill=self.nearest_guard_color, outline='white')
        self.canvas.create_text(x, y, text='A', font=('Arial', 12), fill='white')

        for i in range(self.row - 1, self.row + 2):
            for j in range(self.col - 1, self.col + 2):
                if (i, j) != (self.row, self.col) and 0 <= i < self.canvas.size and 0 <= j < self.canvas.size:
                    self.canvas.create_rectangle(j * 30, i * 30, (j + 1) * 30, (i + 1) * 30,
                                                 fill=self.nearest_guard_color, outline='white')
class ChessBoardGUI:
    def __init__(self, master, size=8, total_players=2, real_players=1):
        self.master = master # Ana pencere veya frame'i kaydet
        self.size = size # Satranç tahtası boyutunu kaydet
        self.total_players =total_players # Toplam oyuncu sayısını kaydet
        self.real_players = real_players # Gerçek oyuncu sayısını kaydet
        # Canvas oluştur ve ana pencereye veya frame'e yerleştir
        self.canvas = tk.Canvas(self.master, width=size*30, height=size*30, bg='black')
        self.canvas.pack()
        self.draw_board()


    def draw_board(self):
        guard_colors = ['red', 'blue', 'green', 'yellow']  # Farklı renkte muhafızlar için renk listesi
        # Köşe pozisyonları
        corner_positions = [(0, 0), (0, self.size - 1), (self.size - 1, 0), (self.size - 1, self.size - 1)]  # Köşe pozisyonları

        # Satranç tahtasını oluşturmak için iki tane döngü kullan
        for i in range(self.size):
            for j in range(self.size):
                if (i + j) % 2 == 0:
                    x1, y1 = j * 30, i * 30 # Karelerin sol üst köşe koordinatlarını hesapla
                    x2, y2 = (j + 1) * 30, (i + 1) * 30 # Karelerin sağ alt köşe koordinatlarını hesapla
                    # Canvas üzerinde siyah kareyi çiz, beyaz kenarlığı olsun
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill='black', outline='white')
        # Köşelerdeki muhafızları yerleştirmek için döngü kullan
        for index, (row, col) in enumerate(corner_positions):
            guard_color = guard_colors[index]
            guard_name = f"M{index + 1}"  # Muhafız adı
            self.place_warrior(row, col, guard_name, guard_color)  # Her bir köşeye muhafız yerleştirme

    def place_warrior(self, row, col, warrior_name, color=None): # Köşe veya savaşçı muhafızı ise
        if warrior_name.startswith("M"):
            x = col * 30 + 15 # Muhafızın x konumunu hesapla
            y = row * 30 + 15 # Muhafızın y konumunu hesapla
            # Muhafız karesi
            self.canvas.create_rectangle(x - 15, y - 15, x + 15, y + 15, fill=color, outline='white')
            # Muhafızın adını yaz
            self.canvas.create_text(x, y, text=warrior_name, font=('Arial', 12), fill='white')

            # Muhafızın etrafındaki kareler
            for i in range(row - 1, row + 2):
                for j in range(col - 1, col + 2):
                    if (i, j) != (row, col) and 0 <= i < self.size and 0 <= j < self.size:
                        self.canvas.create_rectangle(j * 30, i * 30, (j + 1) * 30, (i + 1) * 30, fill=color,
                                                     outline='white')
        elif warrior_name == "Atlı":
            x = col * 30 + 15
            y = row * 30 + 15
            nearest_guard_color = self.get_nearest_guard_color(row, col)

            # Atlının konumunu işaretleme
            self.canvas.create_text(x, y, text="A", font=('Arial', 12), fill='white')

            # Atlının çevresindeki çapraz olarak ilerleyen 3 birimlik karelerin boyanması
            for i in range(-3, 4):
                if 0 <= row + i < self.size and 0 <= col + i < self.size:
                    self.canvas.create_rectangle((col + i) * 30, (row + i) * 30, (col + i + 1) * 30, (row + i + 1) * 30,
                                                 fill=nearest_guard_color, outline='white')
                if 0 <= row + i < self.size and 0 <= col - i < self.size:
                    self.canvas.create_rectangle((col - i) * 30, (row + i) * 30, (col - i + 1) * 30, (row + i + 1) * 30,
                                                 fill=nearest_guard_color, outline='white')
        elif warrior_name == "Topçu":
            x = col * 30 + 15
            y = row * 30 + 15
            nearest_guard_color = self.get_nearest_guard_color(row, col)

            # Topçu simgesini yerleştirme
            self.canvas.create_rectangle(x - 15, y - 15, x + 15, y + 15, fill=color, outline='white')
            self.canvas.create_text(x, y, text="T", font=('Arial', 12), fill='white')

            # Topçunun menzili
            for i in range(-2, 3):
                # Yatay menzil
                if 0 <= col + i < self.size:
                    self.canvas.create_rectangle((col + i) * 30, row * 30, (col + i + 1) * 30, (row + 1) * 30,
                                                 fill=nearest_guard_color, outline='white')
                # Dikey menzil
                if 0 <= row + i < self.size:
                    self.canvas.create_rectangle(col * 30, (row + i) * 30, (col + 1) * 30, (row + i + 1) * 30,
                                                 fill=nearest_guard_color, outline='white')
        elif warrior_name == "Okçu":
            x = col * 30 + 15
            y = row * 30 + 15
            nearest_guard_color = self.get_nearest_guard_color(row, col)

            # Okçu simgesini yerleştirme
            self.canvas.create_rectangle(x - 15, y - 15, x + 15, y + 15, fill=color, outline='white')
            self.canvas.create_text(x, y, text="O", font=('Arial', 12), fill='white')

            # Okçunun menzili
            for i in range(-2, 3):
                # Yatay menzil
                if 0 <= col + i < self.size:
                    self.canvas.create_rectangle((col + i) * 30, row * 30, (col + i + 1) * 30, (row + 1) * 30,
                                                 fill=nearest_guard_color, outline='white')
                # Dikey menzil
                if 0 <= row + i < self.size:
                    self.canvas.create_rectangle(col * 30, (row + i) * 30, (col + 1) * 30, (row + i + 1) * 30,
                                                 fill=nearest_guard_color, outline='white')
                # Çapraz menzil
                if 0 <= row + i < self.size and 0 <= col + i < self.size:
                    self.canvas.create_rectangle((col + i) * 30, (row + i) * 30, (col + i + 1) * 30, (row + i + 1) * 30,
                                                 fill=nearest_guard_color, outline='white')
                if 0 <= row + i < self.size and 0 <= col - i < self.size:
                    self.canvas.create_rectangle((col - i) * 30, (row + i) * 30, (col - i + 1) * 30, (row + i + 1) * 30,
                                                 fill=nearest_guard_color, outline='white')
        elif warrior_name == "Sağlıkçı":
            x = col * 30 + 15
            y = row * 30 + 15
            nearest_guard_color = self.get_nearest_guard_color(row, col)

            # Sağlıkçı simgesini yerleştirme
            self.canvas.create_rectangle(x - 15, y - 15, x + 15, y + 15, fill=color, outline='white')
            self.canvas.create_text(x, y, text="S", font=('Arial', 12), fill='white')

            # Sağlıkçının menzili
            for i in range(-2, 3):
                # Yatay menzil
                if 0 <= col + i < self.size:
                    self.canvas.create_rectangle((col + i) * 30, row * 30, (col + i + 1) * 30, (row + 1) * 30,
                                                 fill=nearest_guard_color, outline='white')
                # Dikey menzil
                if 0 <= row + i < self.size:
                    self.canvas.create_rectangle(col * 30, (row + i) * 30, (col + 1) * 30, (row + i + 1) * 30,
                                                 fill=nearest_guard_color, outline='white')
                # Çapraz menzil
                if 0 <= row + i < self.size and 0 <= col + i < self.size:
                    self.canvas.create_rectangle((col + i) * 30, (row + i) * 30, (col + i + 1) * 30, (row + i + 1) * 30,
                                                 fill=nearest_guard_color, outline='white')
                if 0 <= row + i < self.size and 0 <= col - i < self.size:
                    self.canvas.create_rectangle((col - i) * 30, (row + i) * 30, (col - i + 1) * 30, (row + i + 1) * 30,
                                                 fill=nearest_guard_color, outline='white')


        else:
            x = col * 30 + 15
            y = row * 30 + 15
            nearest_guard_color = self.get_nearest_guard_color(row, col)
            self.canvas.create_rectangle(x - 15, y - 15, x + 15, y + 15, fill=nearest_guard_color, outline='white')
            self.canvas.create_text(x, y, text=warrior_name[0], font=('Arial', 12), fill='white')

            # Savaşçının etrafındaki kareler
            for i in range(row - 1, row + 2):
                for j in range(col - 1, col + 2):
                    if (i, j) != (row, col) and 0 <= i < self.size and 0 <= j < self.size:
                        self.canvas.create_rectangle(j * 30, i * 30, (j + 1) * 30, (i + 1) * 30,
                                                     fill=nearest_guard_color, outline='white')

    def get_nearest_guard_color(self, row, col):
        distances = []# Köşe pozisyonları ile belirtilen muhafızların, hedef konumdan olan Manhattan mesafeleri
        corner_positions = [(0, 0), (0, self.size - 1), (self.size - 1, 0), (self.size - 1, self.size - 1)]

        for r, c in corner_positions:  # Köşe pozisyonları ile hedef konum arasındaki Manhattan mesafelerini hesapla ve listeye ekle
            distance = abs(row - r) + abs(col - c)  # Manhattan  hesaplama
            distances.append(distance)
        nearest_index = distances.index(min(distances))# En küçük Manhattan mesafesine sahip olan pozisyonun endeksini bul
        guard_colors = ['red', 'blue', 'green', 'yellow']
        return guard_colors[nearest_index]  # En yakın muhafızın rengini döndür
class WarriorPlacementMenu:
    def __init__(self, master, chess_board):
        self.master = master# Ana pencereyi veya frame'i kaydet
        self.chess_board = chess_board # Satranç tahtasını kaydet
        self.current_warrior_index = 0 # Şu anki savaşçı endeksini sakla


        self.top = tk.Toplevel(master)
        self.top.title("Savaşçı Yerleştirme")

        self.label_x = tk.Label(self.top, text="X Koordinatı:")
        self.label_x.pack()
        self.entry_x = tk.Entry(self.top)
        self.entry_x.pack()

        self.label_y = tk.Label(self.top, text="Y Koordinatı:")
        self.label_y.pack()
        self.entry_y = tk.Entry(self.top)
        self.entry_y.pack()

        self.label_warrior = tk.Label(self.top, text="Savaşçı Türünü Seçin:")
        self.label_warrior.pack()

        self.options_warrior = ["Muhafız", "Okçu", "Topçu", "Atlı", "Sağlıkçı"]
        self.selected_warrior = tk.StringVar()
        self.selected_warrior.set(self.options_warrior[0])

        self.option_menu_warrior = tk.OptionMenu(self.top, self.selected_warrior, *self.options_warrior)
        self.option_menu_warrior.pack()

        self.confirm_button = tk.Button(self.top, text="Onayla", command=self.confirm_placement)
        self.confirm_button.pack()
    def confirm_placement(self):
        # Giriş kutularından X ve Y koordinatlarını al
        x_coord = int(self.entry_x.get())
        y_coord = int(self.entry_y.get())
        # Koordinatların geçerliliğini kontrol et
        if x_coord < 1 or x_coord > self.chess_board.size or y_coord < 1 or y_coord > self.chess_board.size:
            #  geçerli değilse Hata mesajı göster
            messagebox.showerror("Hata", "Geçersiz koordinatlar. Lütfen uygun değerlerde giriniz.")
            return
        warrior_type = self.selected_warrior.get() # Seçilen savaşçı türünü al
        self.chess_board.place_warrior(x_coord - 1, y_coord - 1, warrior_type) # Satranç tahtasına savaşçıyı yerleştir
        messagebox.showinfo("Yerleştirme Onayı", f"{warrior_type} savaşçısı ({x_coord}, {y_coord}) konumuna yerleştirildi.")

        # Tüm savaşçılar yerleştirilmediyse, bir sonraki savaşçı için koordinatları iste
        if self.current_warrior_index < self.chess_board.total_players - 1:
            self.current_warrior_index += 1
            self.label_x.config(text="X Koordinatı:")
            self.label_y.config(text="Y Koordinatı:")
            self.entry_x.delete(0, tk.END)
            self.entry_y.delete(0, tk.END)
            self.selected_warrior.set(self.options_warrior[0])
            self.entry_x.focus_set()
        else:
            self.top.destroy()  # Tüm savaşçılar yerleştirildiyse menü penceresini kapat



def create_chess_board():
    selected_option = option_var.get()
    if selected_option == "Boyut Seçimi":
        user_size = int(entry.get())
        if 8 <= user_size <= 32:
            total_players = int(selected_player.get())
            real_players = int(selected_real_player.get())
            chess_board_gui = ChessBoardGUI(root, user_size, total_players, real_players)
            label_option.pack_forget()
            option_menu.pack_forget()
            label_entry.pack_forget()
            entry.pack_forget()
            label_players.pack_forget()
            option_menu_players.pack_forget()
            label_real_players.pack_forget()
            option_menu_real_players.pack_forget()
            button.pack_forget()
            WarriorPlacementMenu(root, chess_board_gui)  # Savaşçı yerleştirme menüsünü aç
        else:
            tk.messagebox.showerror("Hata", "Lütfen geçerli bir boyut girin (8 ile 32 ararasında)")
    # Önceden tanımlı boyut seçeneklerinden birine göre satranç tahtasını oluştur
    elif selected_option in ["16x16", "24x24", "32x32"]:
        total_players = int(selected_player.get())
        real_players = int(selected_real_player.get())
        chess_board_gui = ChessBoardGUI(root, int(selected_option.split("x")[0]), total_players, real_players)
        label_option.pack_forget()
        option_menu.pack_forget()
        label_players.pack_forget()
        option_menu_players.pack_forget()
        label_real_players.pack_forget()
        option_menu_real_players.pack_forget()
        button.pack_forget()
        WarriorPlacementMenu(root, chess_board_gui)  # Savaşçı yerleştirme menüsünü aç

root = tk.Tk()
root.title("Savaş Alanı")


player_info_gui = PlayerInfoGUI(root, players)


label_option = tk.Label(root, text="Seçenek:")
label_option.pack()

options = ["Boyut Seçimi ", "16x16", "24x24", "32x32"]
option_var = tk.StringVar(root)
option_var.set(options[0])

option_menu = tk.OptionMenu(root, option_var, *options)
option_menu.pack()


label_players = tk.Label(root, text="Kaç oyuncuyla oynamak istiyorsunuz?")
label_players.pack()

player_options = ["2", "3", "4"]
selected_player = tk.StringVar(root)
selected_player.set(player_options[0])

option_menu_players = tk.OptionMenu(root, selected_player, *player_options)
option_menu_players.pack()

label_real_players = tk.Label(root, text="Kaç gerçek oyuncuyla oynamak istiyorsunuz?")
label_real_players.pack()

real_player_options = ["1", "2", "3", "4"]
selected_real_player = tk.StringVar(root)
selected_real_player.set(real_player_options[0])

option_menu_real_players = tk.OptionMenu(root, selected_real_player, *real_player_options)
option_menu_real_players.pack()

button = tk.Button(root, text="Oluştur", command=create_chess_board)
button.pack()

root.mainloop()