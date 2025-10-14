#crée un fichier xml pour crée un nouveau personnage

def createPlayer(Name):
    import random
    import xml.etree.ElementTree as ET
    vie = random.randint(9,15)
    chance = random.randint(3,6)
    shinning = random.randint(8,13)
    racine = ET.Element("player")
    ET.SubElement(racine, "name").text = Name
    ET.SubElement(racine, "PV_max",attrib={"pv": str(vie)}).text = str(vie)
    ET.SubElement(racine, "chance").text = str(chance)
    ET.SubElement(racine, "shinning_Max", attrib={"shinning": str(shinning)}).text = str(shinning)
    arbre = ET.ElementTree(racine)
    directory = "player/"
    extension = ".xml"
    url = f"{directory}{Name}{extension}"
    arbre.write(url, encoding="utf-8", xml_declaration=True)


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



startGame()