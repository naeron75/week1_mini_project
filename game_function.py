# -*- coding: utf-8 -*-
#Rooms and Items

couch = {
    "name": "couch",
    "type": "furniture",
}

door_a = {
    "name": "door a",
    "type": "door",
}
door_b = {
    "name": "door b",
    "type": "door",
}
door_c = {
    "name": "door c",
    "type": "door",
}
door_d = {
    "name": "door d",
    "type": "door",
}

key_a = {
    "name": "key for door a",
    "type": "key",
    "target": door_a,
}
key_b = {
    "name": "key for door b",
    "type": "key",
    "target": door_b,
}
key_c = {
    "name": "key for door c",
    "type": "key",
    "target": door_c,
}
key_d = {
    "name": "key for door d",
    "type": "key",
    "target": door_d,
}

piano = {
    "name": "piano",
    "type": "furniture",
}

queen_bed = {
    "name": "queen bed",
    "type": "furniture",
}

double_bed = {
    "name": "double bed",
    "type": "furniture",
}

dresser = {
    "name": "dresser",
    "type": "furniture",
}

dining_table = {
    "name": "dining table",
    "type": "furniture",
}

game_room = {
    "name": "game room",
    "type": "room",
    "objects": [couch, piano, door_a]
}

bedroom_1 = {
    "name": "bedroom 1",
    "type": "room",
    "objects": [queen_bed, door_a, door_b, door_c]
}

bedroom_2 = {
    "name": "bedroom 2",
    "type": "room",
    "objects": [double_bed, dresser, door_b]
}

living_room = {
    "name": "living room",
    "type": "room",
    "objects": [dining_table, door_c, door_d]
}

outside = {
    "name": "outside",
    "type": "room",
}

# define which items/rooms are related

object_relations = {
    "game room": [couch, piano, door_a],
    "bedroom 1": [queen_bed, door_a, door_b, door_c],
    "bedroom 2": [double_bed, dresser, door_b],
    "living room": [dining_table, door_c, door_d],
    "outside": [door_d],
    "piano": [key_a],
    "queen bed": [key_b],
    "double bed": [key_c],
    "dresser": [key_d],
    "dining table": [],
    "door a": [game_room, bedroom_1],
    "door b": [bedroom_1, bedroom_2],
    "door c": [bedroom_1, living_room],
    "door d": [living_room, outside]
}

# define game state. Do not directly change this dict.
# Instead, when a new game starts, make a copy of this
# dict and use the copy to store gameplay state. This
# way you can replay the game multiple times.

INIT_GAME_STATE = {
    "current_room": game_room,
    "keys_collected": [],
    "target_room": outside
}

# Game Functions

def linebreak():
    """
    Print a line break
    """
    print("\n\n")

def start_game():
    """
    Start the game
    """
    print("You wake up on a couch and find yourself in a strange house with no windows which you have never been to before. You don't remember why you are here and what had happened before. You feel some unknown danger is approaching and you must get out of the house, NOW!")
    game_state = INIT_GAME_STATE.copy()
    play_room(game_state["current_room"], game_state)

def play_room(room, game_state):
    """
    Play a room. First check if the room being played is the target room.
    If it is, the game will end with success. Otherwise, let player either
    explore (list all items in this room) or examine an item found here.
    """
    game_state["current_room"] = room
    if(game_state["current_room"] == game_state["target_room"]):
        print("Congrats! You escaped the room!")
    else:
        print("You are now in " + room["name"])
        intended_action = input("What would you like to do? Type 'explore' or 'examine'?").lower().strip()
        if intended_action == "explore":
            explore_room(room)
            play_room(room, game_state)
        elif intended_action == "examine":
            correct_item = False
            while not correct_item:
                item_to_examine = input("What would you like to examine?").lower().strip()
                items_in_room = [item['name'] for item in room['objects']]
                if item_to_examine in items_in_room:
                    examine_item(item_to_examine, game_state)
                    correct_item = True
                else:
                    print("Sorry, this item doesn't exist or is not in this room, please enter a valid one.")
        else:
            print("Not sure what you mean. Type 'explore' or 'examine'.")
            play_room(room, game_state)
        linebreak()

def explore_room(room):
    """
    Explore a room. List all items belonging to this room.
    """
    items = [i["name"] for i in object_relations[room["name"]]]
    print("You explore the room. This is " + room["name"] + ". You find " + ", ".join(items))

def get_next_room_of_door(door, current_room):
    """
    From object_relations, find the two rooms connected to the given door.
    Return the room that is not the current_room.
    """
    connected_rooms = object_relations[door["name"]]
    return next(room for room in connected_rooms if room != current_room)

def examine_item(item_name, game_state):
    """
    Examine an item which can be a door or furniture.
    First make sure the intended item belongs to the current room.
    Then check if the item is a door. Tell player if key hasn't been
    collected yet. Otherwise ask player if they want to go to the next
    room. If the item is not a door, then check if it contains keys.
    Collect the key if found and update the game state. At the end,
    play either the current or the next room depending on the game state
    to keep playing.
    """
    current_room = game_state["current_room"]
    next_room = ""
    output = None

    for item in object_relations[current_room["name"]]:
        if(item["name"] == item_name):
            output = "You examine " + item_name + ". "
            if(item["type"] == "door"):
                have_key = False
                for key in game_state["keys_collected"]:
                    if(key["target"] == item):
                        have_key = True
                if(have_key):
                    output += "You unlock it with a key you have."
                    next_room = get_next_room_of_door(item, current_room)
                else:
                    output += "It is locked but you don't have the key."
            else:
                if(item["name"] in object_relations and len(object_relations[item["name"]])>0):
                    item_found = object_relations[item["name"]].pop()
                    game_state["keys_collected"].append(item_found)
                    output += "You find " + item_found["name"] + "."
                else:
                    output += "There isn't anything interesting about it."
            print(output)
            break

    if(output is None):
        print("The item you requested is not found in the current room.")
        
        
    if(next_room):
        correct_answer=False
        while not correct_answer:
            answer = input("Do you want to go to the next room? Enter 'yes' or 'no'").lower().strip()
            if answer=='yes':
                play_room(next_room, game_state)
                correct_answer=True
            elif answer == 'no':
                play_room(current_room, game_state)
                correct_answer=True
            else:
                print("Not a valid command, please enter yes or no only.")
    else:
        play_room(current_room, game_state)