import json
import os

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def play_game(data):
    current_scene = "start"

    while True:
        clear()
        scene = data[current_scene]
        print(scene["text"])
        print()


        if not scene["choices"]:
            print("\n🎮 Fin de l'aventure !")
            break


        for i, choice in enumerate(scene["choices"], 1):
            print(f"{i}. {choice['text']}")


        choice = input("\n👉 Que fais-tu ? (numéro) : ")

        if not choice.isdigit() or int(choice) < 1 or int(choice) > len(scene["choices"]):
            input("\n⚠️ Choix invalide. Appuie sur Entrée pour réessayer.")
            continue

        next_scene = scene["choices"][int(choice) - 1]["next"]
        current_scene = next_scene

def main():
    with open("./data/data.json", "r") as f:
        data = json.load(f)

    play_game(data)

if __name__ == "__main__":
    main()
