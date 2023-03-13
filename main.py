# Welcome to
# __________         __    __  .__                               __
# \______   \_____ _/  |__/  |_|  |   ____   ______ ____ _____  |  | __ ____
#  |    |  _/\__  \\   __\   __\  | _/ __ \ /  ___//    \\__  \ |  |/ // __ \
#  |    |   \ / __ \|  |  |  | |  |_\  ___/ \___ \|   |  \/ __ \|    <\  ___/
#  |________/(______/__|  |__| |____/\_____>______>___|__(______/__|__\\_____>
#
# This file can be a nice home for your Battlesnake logic and helper functions.
#
# To get you started we've included code to prevent your Battlesnake from moving backwards.
# For more info see docs.battlesnake.com

import random
import typing


# info is called when you create your Battlesnake on play.battlesnake.com
# and controls your Battlesnake's appearance
# TIP: If you open your Battlesnake URL in a browser you should see this data
def info() -> typing.Dict:
    print("INFO")

    return {
        "apiversion": "1",
        "author": "CaiCanCode",  # TODO: Your Battlesnake Username
        "color": "#99004d",  # TODO: Choose color
        "head": "smart-caterpillar",  # TODO: Choose head
        "tail": "mouse",  # TODO: Choose tail
    }


# start is called when your Battlesnake begins a game
def start(game_state: typing.Dict):
    print("GAME START")


# end is called when your Battlesnake finishes a game
def end(game_state: typing.Dict):
    print("GAME OVER\n")


# move is called on every turn and returns your next move
# Valid moves are "up", "down", "left", or "right"
# See https://docs.battlesnake.com/api/example-move for available data
def move(game_state: typing.Dict) -> typing.Dict:

    is_move_safe = {
      "up": 0.5, 
      "down": 0.5, 
      "left": 0.5, 
      "right": 0.5
    }

    # We've included code to prevent your Battlesnake from moving backwards
    my_head = game_state["you"]["body"][0]  # Coordinates of your head
    my_neck = game_state["you"]["body"][1]  # Coordinates of your "neck"

      # TODO: Step 4 - Move towards food instead of random, to regain health and survive longer
    food = game_state['board']['food']
    health = game_state['you']['health']

    for i in food:
      #general incentives
      if i["x"] > my_head["x"]:
        is_move_safe["right"] += 0.0078125*0.015625*(100-health)
      elif i["x"] < my_head["x"]:
        is_move_safe["left"] += 0.0078125*0.015625*(100-health)
      if i["y"] > my_head["y"]:
        is_move_safe["up"] += 0.0078125*0.015625*(100-health)
      elif i["y"] < my_head["y"]:
        is_move_safe["down"] += 0.0078125*0.015625*(100-health)
      
      #specific incentives
      if i["x"] == my_head["x"] and i["y"] == my_head["y"] + 1:
        is_move_safe["up"] += 0.06
      elif i["x"] == my_head["x"] and i["y"] == my_head["y"] - 1:
        is_move_safe["down"] += 0.06
      elif i["y"] == my_head["y"] and i["x"] == my_head["x"] + 1:
        is_move_safe["right"] += 0.06
      elif i["y"] == my_head["y"] and i["x"] == my_head["x"] - 1:
        is_move_safe["left"] += 0.06

    if my_neck["x"] < my_head["x"]:  # Neck is left of head, don't move left
        is_move_safe["left"] = 0

    elif my_neck["x"] > my_head["x"]:  # Neck is right of head, don't move right
        is_move_safe["right"] = 0

    elif my_neck["y"] < my_head["y"]:  # Neck is below head, don't move down
        is_move_safe["down"] = 0

    elif my_neck["y"] > my_head["y"]:  # Neck is above head, don't move up
        is_move_safe["up"] = 0

    # TODO: Step 1 - Prevent your Battlesnake from moving out of bounds and incentivise moving away from walls
    board_width = game_state['board']['width']
    board_height = game_state['board']['height']

    if my_head["x"] == 0: #snake is in leftmost column
      is_move_safe["left"] = 0
      is_move_safe["right"] += 0.06

    elif my_head["x"] == board_width - 1: #snake is in rightmost column
      is_move_safe["right"] = 0
      is_move_safe["left"] += 0.06

    if my_head["y"] == 0: #snake is in bottom row
      is_move_safe["down"] = 0
      is_move_safe["up"] += 0.06

    elif my_head["y"] == board_height - 1: #snake is in top row
      is_move_safe["up"] = 0
      is_move_safe["down"] += 0.06

    #avoid moving into walls
    if my_head["x"] == 1: #snake is near leftmost column
      is_move_safe["left"] -= 0.06
      if my_head["y"] == 0 or my_head["y"] == board_height - 1:
        is_move_safe["left"] -= 0.04
    
    elif my_head["x"] == board_width - 2: #snake is near rightmost column
      is_move_safe["right"] -= 0.06
      if my_head["y"] == 0 or my_head["y"] == board_height - 1:
        is_move_safe["right"] -= 0.04

    if my_head["y"] == 1: #snake is near bottom row
      is_move_safe["down"] -= 0.06
      if my_head["x"] == 0 or my_head["x"] == board_width - 1:
        is_move_safe["down"] -= 0.04

    elif my_head["y"] == board_height - 2: #snake is near top row
      is_move_safe["up"] -= 0.06
      if my_head["x"] == 0 or my_head["x"] == board_width - 1:
        is_move_safe["up"] -= 0.04

    # TODO: Step 2 - Prevent your Battlesnake from colliding with itself
    my_body = game_state['you']['body']
  
    for i in range(2, len(my_body)-1): #My body not including my tail, my head or my neck
      if my_body[i]["x"] == my_head["x"]: #a part of my body is in the same column as my head
        if my_body[i]["y"] == my_head["y"] + 1: #a part of my body is directly above my head
          is_move_safe["up"] = 0
        elif my_body[i]["y"] == my_head["y"] - 1: #a part of my body is directly below my head
          is_move_safe["down"] = 0
      elif my_body[i]["y"] == my_head["y"]: #a part of my body is in the same row as my head
        if my_body[i]["x"] == my_head["x"] + 1: #a part of my body is directly to the right of my head
          is_move_safe["right"] = 0
        elif my_body[i]["x"] == my_head["x"] - 1: #a part of my body is directly to the left of my head
          is_move_safe["left"] = 0

      #general snake avoidance strategy
      if my_head["x"] > my_body[i]["x"] and my_head["x"] < my_body[i]["x"] + 5:
        is_move_safe["left"] -= 0.01
      elif my_head["x"] < my_body[i]["x"] and my_head["x"] > my_body[i]["x"] - 5:
        is_move_safe["right"] -= 0.01
      if my_head["y"] > my_body[i]["y"] and my_head["y"] < my_body[i]["y"] + 5:
        is_move_safe["down"] -= 0.01
      elif my_head["y"] < my_body[i]["y"] and my_head["y"] > my_body[i]["y"] - 5:
        is_move_safe["up"] -= 0.01

    # TODO: Step 3 - Prevent your Battlesnake from colliding with other Battlesnakes
    opponents = game_state['board']['snakes']

    for j in range(len(opponents)):
      if opponents[j]['body'][0] != my_head: 
        for i in range(len(opponents[j]['body'])-1): #does not include opponent tail
          if my_head["x"] == opponents[j]['body'][i]["x"]:
            if my_head["y"] == opponents[j]['body'][i]["y"] + 1:
              is_move_safe["down"] = 0
            elif my_head["y"] == opponents[j]['body'][i]["y"] - 1:
              is_move_safe["up"] = 0
          elif my_head["y"] == opponents[j]['body'][i]["y"]:
            if my_head["x"] == opponents[j]['body'][i]["x"] + 1:
              is_move_safe["left"] = 0
            elif my_head["x"] == opponents[j]['body'][i]["x"] - 1:
              is_move_safe["right"] = 0
          #general snake avoidance strategy
          if my_head["x"] > opponents[j]['body'][i]["x"] and my_head["x"] < opponents[j]['body'][i]["x"] + 5:
            is_move_safe["left"] -= 0.0078125
          elif my_head["x"] < opponents[j]['body'][i]["x"] and my_head["x"] > opponents[j]['body'][i]["x"] - 5:
            is_move_safe["right"] -= 0.0078125
          if my_head["y"] > opponents[j]['body'][i]["y"] and my_head["y"] < opponents[j]['body'][i]["y"] + 5:
            is_move_safe["down"] -= 0.0078125
          elif my_head["y"] < opponents[j]['body'][i]["y"] and my_head["y"] > opponents[j]['body'][i]["y"] - 5:
            is_move_safe["up"] -= 0.0078125
        #now check tails
        
        if my_head["x"] == opponents[j]['body'][len(opponents[j]['body']) - 1]["x"]:
          if my_head["y"] == opponents[j]['body'][len(opponents[j]['body']) - 1]["y"] + 1:
            is_move_safe["down"] -= 0.0625
          elif my_head["y"] == opponents[j]['body'][len(opponents[j]['body']) - 1]["y"] - 1:
            is_move_safe["up"] -= 0.0625
        elif my_head["y"] == opponents[j]['body'][len(opponents[j]['body']) - 1]["y"]:
          if my_head["x"] == opponents[j]['body'][len(opponents[j]['body']) - 1]["x"] + 1:
            is_move_safe["left"] -= 0.0625
          elif my_head["x"] == opponents[j]['body'][len(opponents[j]['body']) - 1]["x"] - 1:
            is_move_safe["right"] -= 0.0625
  
        #avoid head-to-head with bigger snakes
        if(len(opponents[j]['body']) >= len(opponents[0]['body'])): #other snake is bigger (or same length) than me
          if(my_head["x"] == opponents[j]['body'][0]["x"]):
            if my_head["y"] == opponents[j]['body'][0]["y"] + 2:
              is_move_safe["down"] -=0.125
            elif my_head["y"] == opponents[j]['body'][0]["y"] - 2:
              is_move_safe["up"] -=0.125
          elif my_head["x"] == opponents[j]['body'][0]["x"] + 1:
            if my_head["y"] == opponents[j]['body'][0]["y"] + 1:
              is_move_safe["down"] -= 0.125
              is_move_safe["left"] -= 0.125
            elif my_head["y"] == opponents[j]['body'][0]["y"] - 1:
              is_move_safe["up"] -= 0.125
              is_move_safe["left"] -= 0.125
          elif my_head["x"] == opponents[j]['body'][0]["x"] - 1:
            if my_head["y"] == opponents[j]['body'][0]["y"] + 1:
              is_move_safe["down"] -= 0.125
              is_move_safe["right"] -= 0.125
            elif my_head["y"] == opponents[j]['body'][0]["y"] - 1:
              is_move_safe["up"] -= 0.125
              is_move_safe["right"] -= 0.125
          elif my_head["y"] == opponents[j]['body'][0]["y"]:
            if my_head["x"] == opponents[j]['body'][0]["x"] + 2:
              is_move_safe["left"] -= 0.125
            elif my_head["x"] == opponents[j]['body'][0]["x"] - 2:
              is_move_safe["right"] -= 0.125
  



        
# Are there any safe moves left?
    not_death_moves = []
    move_weights = []
    for move, isSafe in is_move_safe.items():
        if isSafe > 0:
          not_death_moves.append(move)
          move_weights.append(isSafe)

    if len(not_death_moves) == 0:
        print(f"MOVE {game_state['turn']}: No safe moves detected! Moving down")
        return {"move": "down"}

    #USE THIS FOR MORE RANDOMNESS
    #next_move = random.choices(not_death_moves, weights=move_weights, k=1)[0]
      
    # Choose a random move from the safe ones
    best_moves = [not_death_moves[0]]
    not_death_moves.remove(not_death_moves[0])
    for move in not_death_moves:
      if is_move_safe[move] > is_move_safe[best_moves[0]]:
        best_moves = []
        best_moves.append(move)
      elif is_move_safe[move] == is_move_safe[best_moves[0]]:
        best_moves.append(move)
        
    
    #USE THIS FOR LESS RANDOMNESS    
    next_move = random.choice(best_moves)



  
    print(f"MOVE {game_state['turn']}: {next_move}")
    return {"move": next_move}


# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server

    run_server({
        "info": info, 
        "start": start, 
         "move": move, 
        "end": end
    })
