from tkinter import *
from tkinter.ttk import *
import json
from PIL import Image, ImageTk
from io import BytesIO
import requests
import random
import pygame

# Load JSON data
with open("pokemons.json", "r") as f:
    pokemons = json.load(f)
    
# Global variables
current_pokemon_id = None
new_window = None
photo = None
pygame.init()
# Function to display Pokemon data
def show_pokemon(pokemon_id):
    global photo, new_window
    
    # Find the Pokemon by ID
    result = None
    for pokemon in pokemons:
        if pokemon['id'] == pokemon_id:
            result = pokemon
            break
    
    if not result:
        Label(new_window, text="Pokemon not found!").grid(row=10, column=0)
        return

    # Fetch image
    url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/{pokemon_id}.png"
    response = requests.get(url)
    
    if response.status_code == 200:
        image = Image.open(BytesIO(response.content)).resize((190, 190))
        photo = ImageTk.PhotoImage(image)
        
        # Update image label
        img_label = Label(new_window, image=photo)
        img_label.image = photo
        img_label.grid(row=0, column=9, rowspan=9, padx=20)
    else:
        print("Image not found (404).")


    # Update Pokemon info
    Name = result['name']
    id_ = result['id']
    height = result['height']
    weight = result['weight']
    
    # Update labels
    Label(new_window, text=f"Name: {Name}").grid(row=0, column=0)
    Label(new_window, text=f"Id: {id_}").grid(row=1, column=0)
    Label(new_window, text=f"Height: {height} foot").grid(row=2, column=0)
    Label(new_window, text=f"Weight: {weight} lb").grid(row=3, column=0)

    # Update stats
    stats = result['stats']
    hp = stats['hp']
    attack = stats['attack']
    defense = stats['defense']
    special_attack = stats['special-attack']
    special_defense = stats['special-defense']
    speed = stats['speed']
    
    Label(new_window, text=f"HP: {hp}").grid(row=4, column=0)
    Label(new_window, text=f"Attack: {attack}").grid(row=5, column=0)
    Label(new_window, text=f"Defense: {defense}").grid(row=6, column=0)
    Label(new_window, text=f"Special Attack: {special_attack}").grid(row=7, column=0)
    Label(new_window, text=f"Special Defense: {special_defense}").grid(row=8, column=0)
    Label(new_window, text=f"Speed: {speed}").grid(row=9, column=0)

    # Fetch sound
    url1 = f"https://raw.githubusercontent.com/PokeAPI/cries/main/cries/pokemon/latest/{pokemon_id}.ogg"
    response = requests.get(url1)
    response.raise_for_status()
    sound_data = BytesIO(response.content)
    pygame.mixer.music.load(sound_data)
    pygame.mixer.music.play()

# Function to go to the next Pokemon
def next_pok():
    global current_pokemon_id
    if current_pokemon_id < 1025:  # Assuming max ID is 1025
        current_pokemon_id += 1
        show_pokemon(current_pokemon_id)
    else:
        Label(new_window, text="No more Pokemon!").grid(row=10, column=0)

# Function to go to the previus Pokemon
def previus_pok():
    global current_pokemon_id
    if current_pokemon_id>1:
        current_pokemon_id -= 1
        show_pokemon(current_pokemon_id)
    else:
        Label(new_window, text="No more Pokemon!").grid(row=10, column=0)

# Function to go to a random Pokemon
def random_pok():
    global current_pokemon_id
    current_pokemon_id = random.randint(1,1025)
    show_pokemon(current_pokemon_id)

# Main search function
def search():
    global current_pokemon_id, new_window, photo
    
    name = entry.get().strip().lower()
    result = None
    
    for pokemon in pokemons:
        if pokemon['name'].lower() == name:
            result = pokemon
            break
    
    if result:
        current_pokemon_id = result['id']
        
        # Create a new window if it doesn't exist
        if new_window is None:
            new_window = Toplevel(master)
            new_window.title("Pokemon")
            new_window.geometry("400x270")
            
            # Exit button
            Button(new_window, text="EXIT", command=new_window.destroy).grid(row=12, column=0)
            
            # Next button
            Button(new_window, text="NEXT", command=next_pok).grid(row=13, column=1)

            # Previus button
            Button(new_window, text="PREVIUS", command=previus_pok).grid(row=13, column=0)

            Button(new_window, text="RANDOM", command=random_pok).grid(row=12, column=1)
        
        # Show Pokemon data
        show_pokemon(current_pokemon_id)
    else:
        print("Pokemon not found!")

# GUI setup
master = Tk()
master.title("Pokedex")
master.geometry("350x175")
Label(master, text="Pokedex").pack()
entry = Entry(master)
entry.pack(padx=10, pady=10)
Button(master, text="Search", command=search).pack(padx=10, pady=10)
master.mainloop()