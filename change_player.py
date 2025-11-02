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
                #si il y en a plusieurs faire une liste pour que l'utilisateur puisse choisir
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
                #si le joueur n'a pas de parti en cours il peut la créer
            case "2":
                name = input("choisi ton nom: ")
                createPlayer(name)
                return name+".xml"
    else:
        name = input("choisi ton nom: ")
        createPlayer(name)
        return name+".xml"
    

def historique(player, narration, choix, id, index, events=None):

    """Ajoute une entrée au StoryBoard du joueur.

    events: optionnel, liste de chaînes représentant les étapes d'un combat ou d'autres logs.
    """

    path = f"player/{player}"
    tree = ET.parse(path)
    root = tree.getroot()

    storyboard = root.find('StoryBoard')
    content = ET.SubElement(storyboard, 'content', attrib={'id': str(index), 'chap': id})
    ET.SubElement(content, "text").text = narration
    ET.SubElement(content, "choix").text = choix

    # Si des événements (par ex. étapes de combat) sont fournis, les ajouter sous <combat><event>...
    if events:
        combat_elem = ET.SubElement(content, 'combat')
        for ev in events:
            ET.SubElement(combat_elem, 'event').text = ev

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

    events = []
    events.append(f"Début du combat entre {player['nom']} et {monstre['nom']}")
    print(f"\n⚔️ Combat engagé entre {player['nom']} et {monstre['nom']} ! ⚔️\n")

    tour = 1
    while pv_joueur > 0 and pv_monstre > 0:
        header = f"--- 🌀 Tour {tour} ---"
        print(header)
        events.append(header)

        # Choix du joueur : combattre ou fuir
        choix = input("Que fais-tu ? (1: Combattre, 2: Fuir) : ").strip()
        if choix == "2":
            jet_fuite = random.randint(1, 20)
            msg = f"{player['nom']} tente de fuir (jet d20 → {jet_fuite})"
            print(msg)
            events.append(msg)
            if jet_fuite < shinning:
                succ = f"{player['nom']} réussit à fuir le combat !"
                print(f"🏃 {succ}")
                events.append(succ)
                return True, pv_joueur, events  # joueur en vie + PV restants
            else:
                fail_msg = f"{player['nom']} échoue à fuir... Le monstre attaque !"
                print(f"⚠️ {fail_msg}")
                events.append(fail_msg)
                # Le joueur ne lance pas d'attaque si fuite échouée

        else:
            # Jet d'attaque du joueur
            jet_joueur = random.randint(1, 20)
            msg = f"{player['nom']} lance un d20 → {jet_joueur}"
            print(msg)
            events.append(msg)
            if jet_joueur > defense_monstre:
                degats = random.randint(1, 6)
                pv_monstre -= degats
                hit_msg = f"Attaque réussie : {monstre['nom']} perd {degats} PV (reste {max(pv_monstre, 0)} PV)"
                print(f"💥 {hit_msg}")
                events.append(hit_msg)
            else:
                miss_msg = f"{player['nom']} rate son attaque..."
                print(f"😬 {miss_msg}")
                events.append(miss_msg)

            if pv_monstre <= 0:
                win_msg = f"{player['nom']} a vaincu {monstre['nom']} !"
                print(f"\n🏆 {win_msg}")
                events.append(win_msg)
                return True, pv_joueur, events  # joueur gagne + PV restants

        # Jet d'attaque du monstre
        jet_monstre = random.randint(1, 20)
        msg_mon = f"{monstre['nom']} lance un d20 → {jet_monstre}"
        print(msg_mon)
        events.append(msg_mon)
        if jet_monstre > defense_joueur:
            degats = random.randint(1, 6)
            pv_joueur -= degats
            dmg_msg = f"{player['nom']} subit {degats} dégâts (reste {max(pv_joueur, 0)} PV)"
            print(f"🩸 {dmg_msg}")
            events.append(dmg_msg)
        else:
            evade_msg = f"{player['nom']} esquive l’attaque !"
            print(f"🛡️ {evade_msg}")
            events.append(evade_msg)

        if pv_joueur <= 0:
            dead_msg = f"{player['nom']} a été vaincu par {monstre['nom']}..."
            print(f"\n💀 {dead_msg}")
            events.append(dead_msg)
            return False, None, events  # joueur mort, pas de PV à retourner

        tour += 1
        time.sleep(1)

    # Si on sort de la boucle naturellement
    events.append(f"Fin du combat — {player['nom']} vivant")
    return True, pv_joueur, events  # joueur vivant + PV restants si combat terminé naturellement
