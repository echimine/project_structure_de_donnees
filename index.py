import json
import os


from change_player import *

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def play_game(data):
    player = startGame()
    current_scene = "start"
    index = 1
    while True:
        
        scene = data[current_scene]
        print(scene["text"])




        if not scene["choices"]:
            print("\n🎮 Fin de l'aventure !")
            break


        for i, choice in enumerate(scene["choices"], 1):
            print(f"{i}. {choice['text']}")


        choice = input("\n👉 Que fais-tu ? (numéro) : ")

        if not choice.isdigit() or int(choice) < 1 or int(choice) > len(scene["choices"]):
            input("\n⚠️ Choix invalide. Appuie sur Entrée pour réessayer.")
            continue
        historique(player,scene["text"],scene["choices"][int(choice) - 1]["text"], scene["id"], index)
        next_scene = scene["choices"][int(choice) - 1]["next"]
        current_scene = next_scene
        index= index +1


with open("./data/data.json", "r", encoding="utf_8") as f:
    data = json.load(f)
    play_game(data)
