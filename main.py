import random
import requests
from os.path import exists
import json

# Cache to comply with the rules of Fair Use Policy but also for dev purposes
def get_cached(filename):
  filename = "cache/{}.txt".format(filename)
  result = False
  if exists(filename):
    with open(filename, 'r') as cached:
      result = cached.read()
      try:
        # print("From cache")
        result = json.loads(result)
      except:
        return result
  return result

def save_to_cache(data,filename):
  filename = "cache/{}.txt".format(filename)
  with open(filename, 'w+') as cached:
    cached.write(data)

# Prettify the stats output to make more user friendly
def format_stats(stats):
  formatted = ""
  width = 20  
  lines = 0
  formatted += "-" * width+"\n"
  for stat,key in enumerate(stats):
    if key == "name":
      formatted += " "*((width-len(stats[key]))//2)+stats[key].upper()+" "*((width-len(stats[key]))//2)+"\n"
      formatted += "-"*width+"\n"
    else:
      dots = width - (len(str(stats[key])) + len(key)) - 2
      formatted += key.capitalize()+" " + ("."* dots) +  " " +str(stats[key]) + "\n"
  formatted += "-" * width+"\n"
  return formatted

# Get pokemon by id from api and cache
def get_pokemon(id):
  # pokemon_number = random.randint(1, 151)
  # pokemon_number = 1
  pokemon = get_cached("pokemon_"+str(id))
  if not pokemon:
    # Using the Pokemon API get a Pokemon based on its ID number
    url = 'https://pokeapi.co/api/v2/pokemon/{}/'.format(id)
    response = requests.get(url)
    pokemon = response.json()
    save_to_cache(response.text,"pokemon_"+str(pokemon['id']))
  
  # Create a dictionary that contains the returned Pokemon's name, id, height and weight (https://pokeapi.co/​)
  # print(pokemon, id)
  return {
    'name': pokemon['name'],
    'id': pokemon['id'],
    'height': pokemon['height'],
    'weight': pokemon['weight'],
  }
  

def run():
  # Get a random Pokemon for the player and another for their opponent
  # Get multiple random Pokemon and let the player decide which one they want to use
  # Dev
  player_deck_dev = [95,67,116]
  player_deck = []
  comp_deck_dev = [98,60,58]
  comp_deck = []
  for i in player_deck_dev:
    player_deck.append(get_pokemon((i)))
  
  for i in comp_deck_dev:
    comp_deck.append(get_pokemon((i)))
  
  # for n in range(3):
  #   random_index = random.randint(1, 151)
  #   player_deck[random_index] = get_pokemon(random_index)
  
  # for n in range(3):
  #   random_index = random.randint(1, 151)
  #   comp_deck[random_index] = get_pokemon(random_index)
  
  is_player_turn = True
  stats = ['id','height','weight']
  stat_choice = None
  player_pokemon = None
  while len(player_deck) > 0 and len(comp_deck) > 0:

    if is_player_turn:
      # Ask the user which pokemon should they use      
      print("\nThese are your cards:")
      for card in player_deck:
        print(format_stats(card))
        
      while not player_pokemon:
        try:
          player_pokemon_choice = input('Which pokemon do you want to use? Enter the name: ')              
          player_pokemon = [card for card in player_deck if card['name'] == player_pokemon_choice][0]
        except:
          print("\nIt seems you don't have that pokemon, try again.")
        
      print(format_stats(player_pokemon))      
      
      while not stat_choice:
        # Ask the user which stat they want to use (id, height or weight)
        print("Available stats:\n0. ID\n1. Height\n2. Weight")      
        stat_choice_input = input("Which stat do you want to use? Enter the index: ")
        try:
          stat_choice = stats[int(stat_choice_input)]
        except:
          print("\nIt seems you got that wrong, enter the index of the stat you want to use.")
      
      print("\nPlayer: {} I choose you!".format(player_pokemon['name']))
      # comp pokemon
      comp_pokemon = comp_deck.pop()
      print("\nComp: {} I choose you!".format(comp_pokemon['name']))
      
    else:
      comp_pokemon = comp_deck.pop()
      print("\nComp: {} I choose you!".format(comp_pokemon['name']))
      stat_choice = random.choice(stats)
      
      # Ask the user which pokemon should they use
      print("\nThese are your cards:")
      for card in player_deck:
        print(format_stats(card))
      
      while not player_pokemon:
        try:
          player_pokemon_choice = input('Which pokemon do you want to use? Enter the name: ')              
          player_pokemon = [card for card in player_deck if card['name'] == player_pokemon_choice][0]
        except:
          print("\nIt seems you don't have that pokemon, try again.")
          
      print(format_stats(player_pokemon))
      print("\nPlayer: {} I choose you!".format(player_pokemon['name']))

    player = player_pokemon[stat_choice]
    comp = comp_pokemon[stat_choice]

    # Compare the player's and opponent's Pokemon on the chosen stat to decide who wins
    if player > comp:
      is_player_turn = True
      player_deck.insert(0,comp_pokemon)
      print("\nYou win!")
    elif player < comp:
      is_player_turn = False
      comp_deck.insert(0,comp_pokemon)
      player_deck.pop((player_deck.index(player_pokemon)))
      print("\nYou lose!")
    else:
      print("\nDraw!")
      
    stat_choice = None
    player_pokemon = None
    
    play_again = input('Play again? y/N: ')
    if play_again.lower() == "y":
      run()
    
    # Dev
    # print("player cards \n")
    # print([ (v['name']) for v in player_deck ])
    # print("comps cards \n")
    # print([ (v['name']) for v in comp_deck ])

run()