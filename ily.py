import tkinter as tk
from tkinter import font
import json
import random
import http.client
import webbrowser
import os 
import sys

levels = [1, 2, 3, 4, 5, 6, 7]

# home
root = tk.Tk()

default_font = font.nametofont("TkDefaultFont")
default_font.configure(family="Courier New")

root.title("Daily Treats for a Cute Boy")
root.geometry("1000x800")
root.configure(bg="black")

# title
title1 = tk.Label(
    root,
    text="Daily Treats for a Cute Boy",
    font=("Courier New", 35),
    bg="black",
    fg="white",
    wraplength=800,
    justify="center"
)

title1.pack(pady=20)


def resource_path(relative_path):
    """ Get absolute path to resource """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

json_path = resource_path("connections.json")

with open(json_path, "r") as f:
    data = json.load(f)

def clean_ascii(text):
    lines = text.splitlines()

    # remove empty first line if present
    if lines and lines[0].strip() == "":
        lines = lines[1:]

    # find minimum indentation
    indent = min(
        (len(line) - len(line.lstrip()))
        for line in lines
        if line.strip()
    )

    # remove indentation
    return "\n".join(line[indent:] for line in lines)

def show_letter():

    letter_select = tk.Toplevel(root)
    letter_select.title("A letter")
    letter_select.geometry("900x600")
    letter_select.configure(bg="black")

    letter_text = "Hi Love <3 This is just a little project of things I thought you could open up if you're having a bad day. Or a good one! I love you so, so much. I love all your quirks, your MBMBaM references, every little mannerism. I love your art: your music, your writing, your film knowledge and passion. You have taught me so much and added so much to my life. I love your crazy little son, and your room that you've created with so much love and care. I love how much you care about the people in your life, the sentimental value you have for their objects and gifts, and how you always, always want to help. You're such a special human and I'm so lucky to be able to live my life with you. Have a great day my love <3"

    letter = tk.Label(
        letter_select,
        text=letter_text,
        font=("Courier New", 15),
        bg="black",
        fg="white",
        wraplength=800,
        justify="center"
    )
    letter.pack()

    extra_text = "P.S. You're a nerd. And also pretty gay. But it's okay because so am I :)"

    extra = tk.Label(
        letter_select,
        text=extra_text,
        font=("Courier New", 15),
        bg="black",
        fg="white",
        wraplength=800,
        justify="center"
    )
    extra.pack()

def open_game():

    level_select = tk.Toplevel(root)
    level_select.title("Choose a Level")
    level_select.geometry("500x600")
    level_select.configure(bg="black")

    title = tk.Label(
        level_select,
        text="Select a Level",
        font=("Courier New", 28),
        bg="black",
        fg="white"
    )
    title.pack(pady=30)

    def start_level(level_number):

        level_select.destroy()

        game_window = tk.Toplevel(root)
        game_window.title(f"Connections - Level {level_number + 1}")
        game_window.geometry("900x850")
        game_window.configure(bg="#121212")

        title = tk.Label(
            game_window,
            text=f"Connections — Level {level_number + 1}",
            font=("Courier New", 30, "bold"),
            bg="#121212",
            fg="white"
        )
        title.pack(pady=20)

        game_frame = tk.Frame(game_window, bg="#121212")
        game_frame.pack()

        result_label = tk.Label(
            game_window,
            text="",
            font=("Courier New", 16),
            bg="#121212",
            fg="white",
            wraplength=800,
            justify="center"
        )
        result_label.pack(pady=20)

        selected = []
        buttons = {}
        solved = 0

        with open('connections.json', 'r') as file:
            data = json.load(file)

        level_array = data[level_number]
        all_words = []

        for connection in level_array:
            words = connection["items"]
            for word in words:
                all_words.append(word)

        random.shuffle(all_words)

        def check_group():
            nonlocal selected, solved

            correct = False
            print(level_array)

            for group in level_array:

                items = group["items"]

                print(set(selected))
                print(set(items))

                if set(selected) == set(items):

                    correct = True
                    solved += 1

                    for word in selected:
                        buttons[word].configure(
                            bg="#2ecc71",
                            state="disabled"
                        )

                    result_label.configure(
                        text=f"Correct! {group['connection']}",
                        fg="#2ecc71"
                    )

                    break

            if not correct:

                for word in selected:
                    buttons[word].configure(bg="#aa3333")

                result_label.configure(
                    text="Not a match",
                    fg="#ff5555"
                )

                game_window.after(800, reset_colors)

            selected = []

        def reset_colors():

            for word, btn in buttons.items():

                if btn["state"] != "disabled":
                    btn.configure(bg="gray")

        def select_word(word):

            print("selected: ", word)

            btn = buttons[word]

            if word in selected:

                selected.remove(word)
                btn.configure(bg="grey")

            else:

                if len(selected) < 4:
                    selected.append(word)
                    btn.configure(bg="#6666ff")
                    btn.update_idletasks()

            if len(selected) == 4:
                print ("checking group, ", selected)
                game_window.after(300, check_group)

        row = 0
        col = 0

        for word in all_words:

            btn = tk.Label(
                game_frame,
                text=word,
                width=18,
                height=4,
                bg="grey",
                fg="black",
                font=("Courier New", 11),
                relief="flat"
            )

            btn.grid(row=row, column=col, padx=8, pady=8)
            btn.bind("<Button-1>", lambda e, w=word: select_word(w))

            buttons[word] = btn

            col += 1

            if col > 3:
                col = 0
                row += 1

    # level buttons
    for i in range(len(levels)):

        btn = tk.Button(
            level_select,
            text=f"Level {i + 1}",
            font=("Courier New", 15),
            width=20,
            command=lambda x=i: start_level(x)
        )

        btn.pack(pady=10)

def get_moon_phase():
    
    def moon_phase(phase_name):
        if phase_name == "New moon":
            return clean_ascii("""
       _..._     
     .:::::::.    
    :::::::::::   NEW  MOON
    ::::::::::: 
    `:::::::::'  
      `':::''""")

        elif phase_name == "Waxing crescent":
            return clean_ascii("""
       _..._     
     .::::. `.    
    :::::::.  :    WAXING CRESCENT
    ::::::::  :  
    `::::::' .'  
      `'::'-'""")

        elif phase_name == "First quarter":
            return clean_ascii("""
       _..._     
     .::::  `.    
    ::::::    :    FIRST QUARTER
    ::::::    :  
    `:::::   .'  
      `'::.-'""")

        elif phase_name == "Waxing gibbous":
            return clean_ascii("""
       _..._     
     .::'   `.    
    :::       :    WAXING GIBBOUS
    :::       :  
    `::.     .'  
      `':..-'""")

        elif phase_name == "Full moon":
            return clean_ascii("""
       _..._     
     .'     `.    
    :         :    FULL MOON
    :         :  
    `.       .'  
      `-...-'""")

        elif phase_name == "Waning gibbous":
            return clean_ascii("""
       _..._     
     .'   `::.    
    :       :::    WANING GIBBOUS
    :       :::  
    `.     .::'  
      `-..:''""")

        elif phase_name == "Last quarter":
            return clean_ascii("""
       _..._     
     .'  ::::.    
    :    ::::::    LAST QUARTER
    :    ::::::  
    `.   :::::'  
      `-.::''""")

        elif phase_name == "Waning crescent":
            return clean_ascii("""
       _..._     
     .' .::::.    
    :  ::::::::    WANING CRESCENT
    :  ::::::::  
    `. '::::::'  
       `-.::''""")
        else:
            return "Something went wrong :( Let me know and I'll fix it!"

    moon_page = tk.Toplevel(root)
    moon_page.title("Today's Moon")
    moon_page.geometry("800x600")
    moon_page.configure(bg="black")

    title = tk.Label(
        moon_page,
        text="Today's Moon",
        font=("Courier New", 28),
        bg="black",
        fg="white",
    )
    title.pack(pady=30)

    conn = http.client.HTTPSConnection("moon-phase.p.rapidapi.com")

    headers = {
        'x-rapidapi-key': "fbdb10e7fcmshdededf4df21b648p1b73d3jsn359ce78a12e9",
        'x-rapidapi-host': "moon-phase.p.rapidapi.com",
        'Content-Type': "application/json"
    }

    conn.request("GET", "/basic", headers=headers)

    res = conn.getresponse()
    data = res.read()

    phase_name = json.loads(data.decode("utf-8"))["phase_name"]

    image = moon_phase(phase_name)

    image_display = tk.Label(
        moon_page,
        text=image,
        font=("Courier New", 15),
        bg="black",
        fg="white",
        wraplength=0,
        justify="left",
        anchor="nw"
    )
    image_display.pack(pady=30)

    print(image)

def random_mbambam():

    playlist_id = "PLaKlWAsV4eApXOe2l1m7K72dJL1fpz3A7"

    playlist_size = 224

    random_index = random.randint(1, playlist_size)

    url = f"https://www.youtube.com/playlist?list={playlist_id}&playnext=1&index={random_index}"

    print("Opening playlist at index:", random_index)
    webbrowser.open(url)

# Button 1: Letter
btn1 = tk.Button(root, text="A Letter", font=("Courier New", 15), width=30, command=show_letter)
btn1.pack(pady=10)

# Button 2: Game
btn2 = tk.Button(root, text="A Connections Game", font=("Courier New", 15), width=30, command=open_game)
btn2.pack(pady=10)

# Button 3: Moon
btn3 = tk.Button(root, text="What's the moon up to?", font=("Courier New", 15), width=30, command=get_moon_phase)
btn3.pack(pady=10)

# Button 4: Mbambam
btn4 = tk.Button(root, text="Mbambam of the day", font=("Courier New", 15), width=30, command=random_mbambam)
btn4.pack(pady=10)

root.mainloop()
