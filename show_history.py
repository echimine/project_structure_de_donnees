import xml.etree.ElementTree as ET

def show_history_markdown(player_file):
    #Affiche l'historique du joueur en format markdown
    tree = ET.parse(f'./player/{player_file}')
    root = tree.getroot()
    
    player_name = root.findtext("name")
    storyboard = root.find("StoryBoard")
    
    print("\n# Résumé de l'aventure\n")
    print(f"##  Aventurier : {player_name}\n")
    
    if storyboard is not None:
        for content in storyboard.findall('content'):
            scene_id = content.get('id')
            chapter = content.get('chap')
            narration = content.find('text').text
            choice = content.find('choix').text
            
            print(f"### Scène {scene_id} ({chapter})\n")
            print(f"**Situation :**\n{narration}\n")
            print(f"**Choix du joueur :**\n➜ {choice}\n")

            # Si des événements de combat existent, les afficher
            combat = content.find('combat')
            if combat is not None and len(combat.findall('event')) > 0:
                print("**Détails du combat :**")
                for ev in combat.findall('event'):
                    text = ev.text if ev.text is not None else ''
                    print(f"- {text}")
                print()
            print("---\n")