#crée un fichier xml pour crée un nouveau personnage

import xml.etree.ElementTree as ET
from xml.dom import minidom


def createPlayer(Name):
    import random
    vie = random.randint(9,15)
    chance = random.randint(3,6)
    shinning = random.randint(8,13)
    player = ET.Element("player")
    ET.SubElement(player, "name").text = Name
    ET.SubElement(player, "PV_max",attrib={"pv": str(vie)}).text = str(vie)
    ET.SubElement(player, "chance").text = str(chance)
    ET.SubElement(player, "shinning_Max", attrib={"shinning": str(shinning)}).text = str(shinning)
    ET.SubElement(player,"StoryBoard").text= ""
    rough_string = ET.tostring(player, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    reparsed_xml = reparsed.toprettyxml(indent="   ")
    directory = "player/"
    extension = ".xml"
    url = f"{directory}{Name}{extension}"
    with open(url, "w", encoding="utf-8") as f:
        f.write(reparsed_xml)

#fonction qui permet de commencer une parti 
def startGame():

    import os
    print("salut salut , tu viens de lancer notre JDR sur l'univers de Stephen king")

    data = os.listdir("player")
    if len(data)>0:
        print("tu as un compte => 1")
        print("crée en toi un =>2")
        choice = input("choix:")
        match choice:
            case "1":
                #retourne la parti si il n'y en a qu'une

                if len(data) == 1 :
                    return data[0]
                #si il y en a plusieur faire une liste pour que l'utilisateur puisse choisir
                else :
                    print("choisi ton compte: ")
                    for index,file in enumerate(data):
                        print(data[index]+" => "+str(index))
                    file = input("quel est ton compte?: ")
                    #tant que le joueur met une valeur interdite alors lui poser la question
                    while 0>int(file) or len(data)<int(file):
                        print("tu t'es trompé, choisi une valeur mise")
                        file = input ("choix: ")
                    return data[int(file)]  
                #si le joueur n'a pas de parti en cours il peut la crée
            case "2":
                name = input("choisi ton nom: ")
                createPlayer(name)
                return name+".xml"
    else:
        name = input("choisi ton nom: ")
        createPlayer(name)
        return name+".xml"
    

def historique(player, narration, choix, id, index):

    path = f"player/{player}"
    tree = ET.parse(path)
    root = tree.getroot()

    storyboard = root.find('StoryBoard')
    content = ET.SubElement(storyboard,'content', attrib={'id':str(index), 'chap':id})
    ET.SubElement(content, "text").text= narration
    ET.SubElement(content,"choix").text = choix

    rough_string = ET.tostring(root, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    xml = reparsed.toprettyxml(indent="  ")
    pretty_xml = "\n".join([line for line in xml.splitlines() if line.strip()])

    # Écrire le XML indenté dans le fichier
    with open(path, "w", encoding="utf-8") as f:
        f.write(pretty_xml)

import random
import time
import random
import time
import random
import time

def combat(player, monstre):
    pv_joueur = int(player["pv"])
    defense_joueur = int(player["defense"])
    shinning = int(player["shinning"])

    pv_monstre = int(monstre["pv"])
    defense_monstre = int(monstre["defense"])

    print(f"\n⚔️ Combat engagé entre {player['nom']} et {monstre['nom']} ! ⚔️\n")

    tour = 1
    while pv_joueur > 0 and pv_monstre > 0:
        print(f"--- 🌀 Tour {tour} ---")
        
        # Choix du joueur : combattre ou fuir
        choix = input("Que fais-tu ? (1: Combattre, 2: Fuir) : ").strip()
        if choix == "2":
            jet_fuite = random.randint(1, 20)
            print(f"{player['nom']} tente de fuir (jet d20 → {jet_fuite})")
            if jet_fuite < shinning:
                print(f"🏃 {player['nom']} réussit à fuir le combat !")
                return True, pv_joueur  # joueur en vie + PV restants
            else:
                print(f"⚠️ {player['nom']} échoue à fuir... Le monstre attaque !")
                # Le joueur ne lance pas d'attaque si fuite échouée

        else:
            # Jet d'attaque du joueur
            jet_joueur = random.randint(1, 20)
            print(f"{player['nom']} lance un d20 → {jet_joueur}")
            if jet_joueur > defense_monstre:
                degats = random.randint(1, 6)
                pv_monstre -= degats
                print(f"💥 Attaque réussie ! {monstre['nom']} perd {degats} PV (reste {max(pv_monstre, 0)} PV)")
            else:
                print(f"😬 {player['nom']} rate son attaque...")

            if pv_monstre <= 0:
                print(f"\n🏆 {player['nom']} a vaincu {monstre['nom']} !")
                return True, pv_joueur  # joueur gagne + PV restants

        # Jet d'attaque du monstre
        jet_monstre = random.randint(1, 20)
        print(f"{monstre['nom']} lance un d20 → {jet_monstre}")
        if jet_monstre > defense_joueur:
            degats = random.randint(1, 6)
            pv_joueur -= degats
            print(f"🩸 {player['nom']} subit {degats} dégâts (reste {max(pv_joueur, 0)} PV)")
        else:
            print(f"🛡️ {player['nom']} esquive l’attaque !")

        if pv_joueur <= 0:
            print(f"\n💀 {player['nom']} a été vaincu par {monstre['nom']}...")
            return False  # joueur mort, pas de PV à retourner

        tour += 1
        time.sleep(1)

    return True, pv_joueur  # joueur vivant + PV restants si combat terminé naturellement
