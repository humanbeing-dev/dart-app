from tkinter import *
from tkinter import ttk
from Darts.users import add_user, select_user
from PIL import Image, ImageTk


root = Tk()
root.title("Dart App")
root.geometry("400x250")
nicknames = []
players = []
reset = False
i = 0


class StartGame(Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title(f"Darts - game")
        self.geometry("458x400")
        self.create_widgets()

    def create_widgets(self):
        headers = ['player_1', 'stats', 'player_2']
        widths = [25, 5, 25]

        for index, header in enumerate(headers):
            self.my_frame = Frame(self, bg='black', bd=1)
            self.my_frame.grid(row=0, column=index)
            self.lbl = Label(self.my_frame, text=header, width=widths[index])
            self.lbl.pack()

            self.update()
            print(self.lbl.winfo_width())

            # self.stats = Frame(self, width=1000, height=100, bg='black', bd=1)
            # self.stats.grid(row=0, column=1)
            # self.lbl = Label(self.stats, text="-", width=5)
            # self.lbl.pack()
            #
            # self.update()
            # print(self.lbl.winfo_width())
            #
            # self.player_2_frame = Frame(self, width=1000, height=100, bg='black', bd=1)
            # self.player_2_frame.grid(row=0, column=2)
            # self.lbl = Label(self.player_2_frame, text="Filip", width=25)
            # self.lbl.pack()
            #
            # self.update()
            # print(self.lbl.winfo_width())


def start_game():
    for widget in root.winfo_children():
        if widget.winfo_class() == "Entry" and widget.get():
            players.append({"nick": widget.get(), "score": 0, "highest": 0})
            nicknames.append(widget.get())

    values_to_start = [nicknames, game_cmb.get()]
    root.destroy()

    game = Tk()
    game.title(f"Darts - {values_to_start[1]}")
    game.geometry("450x400")

    def new_game():
        score_ent["state"] = NORMAL
        new_game_btn.grid_forget()
        submit_btn = Button(game, text="Submit score", command=submit)
        submit_btn.grid(row=0, column=2)
        for widget in game.winfo_children():
            widget_data = widget.grid_info()
            row = widget_data.get('row')
            if not row is None and row >= 3:                                # destroy everything below third row
                widget.destroy()
        global i
        i = 0
        nonlocal results
        results = [int(values_to_start[1])] * len(values_to_start[0])

    def submit(event):
        global i
        global reset
        score = score_ent.get()
        score_ent.delete(0, "end")
        cur_result = results[(i + 2) % 2] - int(score)
        results[(i + 2) % 2] = cur_result if cur_result >= 0 else results[(i + 2) % 2]
        counter = Label(game, text=f"{results[(i + 2) % 2]}", width=8, height=1, font="Helvetica, 20")
        counter.grid(row=3+(i // 2), column=(i+2) % 2)
        i += 1
        ind = (1 - (i + 2) % 2)
        players[ind]['highest'] = max(players[ind]['highest'], int(score))

        if results[0] == 0 and results[1] == 0:
            reset = True
            players[0]["score"] += 1
            players[1]["score"] += 1

        elif results[0] == 0 and i % 2 == 0:
            reset = True
            players[0]["score"] += 1

        elif results[1] == 0 and i % 2 == 0:
            reset = True
            players[1]["score"] += 1

        if reset:
            submit_btn.destroy()
            new_game_btn = Button(game, text="New game", command=new_game)
            new_game_btn.grid(row=0, column=2)
            score_ent["state"] = DISABLED
            reset = False
            players.reverse()

        res['text'] = f"{str(players[0]['score'])}:{str(players[1]['score'])}"
        game.children['player_0']["text"] = f"{players[0]['nick']}[{players[0]['highest']}]"
        game.children['player_1']["text"] = f"{players[1]['nick']}[{players[1]['highest']}]"

    header_lbl = Label(game, text="Your score:").grid(row=0, column=0)
    score_ent = Entry(game)
    score_ent.grid(row=0, column=1)
    submit_btn = Button(game, text="Submit score", command=submit)
    game.bind("<Return>", submit)
    game.bind("<KP_Enter>", submit)
    submit_btn.grid(row=0, column=2)
    new_game_btn = Button(game, text="New game", command=new_game)

    for index, player in enumerate(players):
        player_lbl = Label(game, text=f"{players[index]['nick']}[{players[index]['highest']}]", width=8, height=1, font="Helvetica, 20", name=f"player_{index}")
        player_lbl.grid(row=1, column=index)
        counter = Label(game, text=f"{values_to_start[1]}", width=8, height=1, font="Helvetica, 20", name=f"result_{index}")
        counter.grid(row=2, column=index)
    res = Label(game, text=f"0:0", width=8, height=1, font="Helvetica, 20")
    res.grid(row=1, column=2)
    results = [int(values_to_start[1])] * len(values_to_start[0])
    print(results)


class NewUserWindow(Toplevel):
    """Class to create new user"""
    def __init__(self, master=None):
        super().__init__(master=master)
        self.title(f"Darts - create new user")
        self.geometry("250x100")
        self.create_widgets()

    def create_widgets(self):
        self.user_lbl = Label(self, text=f"User nickname:", width=20, border=1)
        self.user_lbl.pack(ipady=3)
        self.user_ent = Entry(self)
        self.user_ent.pack(ipady=3)
        self.save_user = Button(self, text="Save User", width=17,
                           command=lambda: add_user(self.user_ent.get(),
                                                    db_name="darts",
                                                    tbl_name="darts_users"))
        self.save_user.pack()


class ShowUsersWindow(Toplevel):
    """Class to show all user within database"""
    def __init__(self, master=None):
        super().__init__(master=master)
        self.title(f"Darts - show all user")
        self.geometry("800x300")
        self.create_widgets()

    def create_widgets(self):
        users = select_user("", "darts_users", "darts")

        columns = ["ID", "Nick", "Highest score", "Games played", "Games won", "Games lost"]
        for index, column in enumerate(columns):
            user_lbl = Label(self, text=f"{column}", width=15, border=1)
            user_lbl.grid(row=0, column=index)

        for row, user in enumerate(users):
            for column, value in enumerate(user):
                user_lbl = Label(self, text=f"{value}", width=15, border=1)
                user_lbl.grid(row=row + 1, column=column)


players_numbers = ['first', 'second']
img = Image.open("img/user.png")
img = img.resize((16, 16))
img = ImageTk.PhotoImage(img)


for index, player in enumerate(players_numbers):
    player_lbl = Label(root, text=f"Enter {player} player nick:", width=20, height=2, anchor=W)
    player_lbl.grid(row=index, column=0, sticky=W, padx=(30, 5))
    player_ent = Entry(root, name=f"player_{index+1}")
    player_ent.grid(row=index, column=1)
    img_lbl = Label(root, image=img)
    img_lbl.grid(row=index, column=2)


game_lbl = Label(root, text=f"Pick gametype:", width=20, height=2, anchor=W)
game_lbl.grid(row=4, column=0, padx=(30, 5))
game_cmb = ttk.Combobox(root, value=[301, 501], width=18)
game_cmb.set("301")
game_cmb.grid(row=4, column=1)

add_new_user = Button(root, text="Create User", width=15, command=NewUserWindow).grid(row=5, column=0)
start_game_btn = Button(root, text="Start Game", width=15, command=StartGame).grid(row=5, column=1)
show_users = Button(root, text="Show Users", width=15, command=ShowUsersWindow).grid(row=6, column=0)
footer_lbl = Label(root, text="ProMCS 2020  v1.1", pady=10).grid(row=7, column=0, columnspan=2)


root.mainloop()
