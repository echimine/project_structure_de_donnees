import json
from logging import root
import os
import yaml


from change_player import *
from show_history import show_history_markdown

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
            # Enregistrer le début du combat
            historique(player, scene["text"], "Engager le combat", scene["id"], index)
            index += 1

            # combat_result now has the shape (success: bool, pv_remaining_or_None, events:list)
            success, pv_restants, events = combat_result

            if not success:
                next_scene = scene["end"]["lose"]
                print(f"\n💀 {player_data['nom']} a été vaincu...")
<<<<<<< HEAD
                # Mettre à jour la PV dans le XML avant d'ajouter l'entrée d'historique sur le disque
=======

    # 🔁 Recharge le XML avant écriture
                tree = ET.parse(f'./player/{player}')
                root = tree.getroot()

>>>>>>> clement
                pv_element = root.find("PV_max")
                pv_element.set("pv", str(0))
                pv_element.text = str(0)

                tree.write(f'./player/{player}', encoding="utf-8", xml_declaration=True)

                # Enregistrer la défaite + log du combat (historique lira le fichier et y ajoutera les events)
                historique(player, f"Combat contre {monstre_data['nom']}", "Défaite - Mort au combat", next_scene, index, events)

                print("\n📖 Voici le résumé de ton aventure :")
                show_history_markdown(player)
                return
            else:
                # victoire
                player_data["pv"] = pv_restants

<<<<<<< HEAD
                # Mettre à jour le XML
=======
    # 🔁 Recharge le XML avant écriture
                tree = ET.parse(f'./player/{player}')
                root = tree.getroot()

>>>>>>> clement
                pv_element = root.find("PV_max")
                pv_element.set("pv", str(pv_restants))
                pv_element.text = str(pv_restants)

                tree.write(f'./player/{player}', encoding="utf-8", xml_declaration=True)

<<<<<<< HEAD
                # Enregistrer la victoire + log du combat
=======

>>>>>>> clement
                next_scene = scene["end"]["win"]
                historique(player, f"Combat contre {monstre_data['nom']}", "Victoire au combat", next_scene, index, events)
                index += 1
        if not scene["choices"]:
            print("\n🎮 Bien joué ! Voici le résumé de ton aventure :")
            show_history_markdown(player)
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
