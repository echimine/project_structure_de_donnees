def createPlayer(Name):
    import random
    import xml.etree.ElementTree as ET
    vie = random.randint(9,15)
    chance = random.randint(3,6)
    shinning = random.randint(8,13)
    racine = ET.Element("player")
    ET.SubElement(racine, "name", id="1").text = Name
    ET.SubElement(racine, "PV").text = str(vie)
    ET.SubElement(racine, "chance").text = str(chance)
    ET.SubElement(racine, "shinning").text = str(shinning)
    arbre = ET.ElementTree(racine)
    directory = "player/"
    extension = ".xml"
    url = f"{directory}{Name}{extension}"
    arbre.write(url, encoding="utf-8", xml_declaration=True)

createPlayer("echimine")