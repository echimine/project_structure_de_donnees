import json
from logging import root
import os
import yaml


from change_player import *

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def play_game(data):
    
    player = startGame()
    tree = ET.parse(f'./player/{player}')
    
    root = tree.getroot()
    player_data = {
        "nom": root.findtext("name"),
        "pv": int(root.find("PV_max").get("pv")),
        "defense": int(root.findtext("chance")),
        "shinning": int(root.find("shinning_Max").get("shinning"))
    }
    if player_data["pv"] <= 0:
        print(f"💀 {player_data['nom']} est déjà mort. Créez un nouveau personnage pour commencer une nouvelle partie.")
        return

    storyboard = root.find("StoryBoard")
    if storyboard is None or len(storyboard)==0:
        current_scene = "start"
    else:
        clear()
        current_scene = storyboard[-1].get("chap")
    index = 1
    while True:
        scene = data[current_scene]
        print(scene["text"])
        if scene["combat"] == True:
            
            with open(f'./monstre/{scene["monstre"]}.yml', 'r', encoding='utf-8') as f:
                monstre_data = yaml.safe_load(f)

            combat_result = combat(player_data, monstre_data)
            if combat_result is False:
                next_scene = scene["end"]["lose"]
                print(f"\n💀 {player_data['nom']} a été vaincu...")
                pv_element = root.find("PV_max")
                pv_element.set("pv", str(0))
                pv_element.text = str(0)
                tree.write(f'./player/{player}', encoding="utf-8", xml_declaration=True)
                return
            else:
                vivant, pv_restants = combat_result
                player_data["pv"] = pv_restants

    # Mettre à jour le XML
                pv_element = root.find("PV_max")
                pv_element.set("pv", str(pv_restants))
                pv_element.text = str(pv_restants)
                tree.write(f'./player/{player}', encoding="utf-8", xml_declaration=True)

                next_scene = scene["end"]["win"]
        if not scene["choices"]:
            print("\n🎮 bien joué")
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
