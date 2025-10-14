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
    pretty_xml = reparsed.toprettyxml(indent="   ")
    directory = "player/"
    extension = ".xml"
    url = f"{directory}{Name}{extension}"
    with open(url, "w", encoding="utf-8") as f:
        f.write(pretty_xml)

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
    pretty_xml = reparsed.toprettyxml(indent="   ")

    # Écrire le XML indenté dans le fichier
    with open(path, "w", encoding="utf-8") as f:
        f.write(pretty_xml)