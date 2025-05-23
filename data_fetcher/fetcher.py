import requests
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed

MAX_POKEMON_ID = 1025
MAX_WORKERS = 20

def get_pokemon_data(pokemon_id):
    try:
        url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}"
        resp = requests.get(url)
        if resp.status_code != 200:
            print(f"Failed to fetch Pokémon ID {pokemon_id}")
            return None
        
        data = resp.json()
        name = data['name'].capitalize()
        types = [t['type']['name'].capitalize() for t in data['types']]
        type1 = types[0] if len(types) > 0 else ''
        type2 = types[1] if len(types) > 1 else ''
        
        stats = {stat['stat']['name']: stat['base_stat'] for stat in data['stats']}
        height_m = data['height'] / 10
        weight_kg = data['weight'] / 10
        
        abilities = [a['ability']['name'].replace('-', ' ').capitalize() for a in data['abilities']]
        ability1 = abilities[0] if len(abilities) > 0 else ''
        ability2 = abilities[1] if len(abilities) > 1 else ''
        hidden_ability = ''
        for a in data['abilities']:
            if a['is_hidden']:
                hidden_ability = a['ability']['name'].replace('-', ' ').capitalize()
                break
        
        species_url = data['species']['url']
        species_resp = requests.get(species_url)
        if species_resp.status_code == 200:
            species_data = species_resp.json()
            generation = int(species_data['generation']['url'].split('/')[-2].replace('generation-', ''))
            legendary = 1 if species_data['is_legendary'] else 0
        else:
            generation = 0
            legendary = 0
        
        return {
            'NUMBER': pokemon_id,
            'NAME': name,
            'TYPE1': type1,
            'TYPE2': type2,
            'HEIGHT': height_m,
            'WEIGHT': weight_kg,
            'ABILITY1': ability1,
            'ABILITY2': ability2,
            'ABILITY_HIDDEN': hidden_ability,
            'GENERATION': generation,
            'LEGENDARY': legendary,
            'HP': stats.get('hp', 0),
            'ATK': stats.get('attack', 0),
            'DEF': stats.get('defense', 0),
            'SP_ATK': stats.get('special-attack', 0),
            'SP_DEF': stats.get('special-defense', 0),
            'SPD': stats.get('speed', 0),
            'TOTAL': sum(stats.values()),
        }
    except Exception as e:
        print(f"Error with Pokémon ID {pokemon_id}: {e}")
        return None

def fetch_all_pokemon():
    pokemon_data_list = []
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {executor.submit(get_pokemon_data, pid): pid for pid in range(1, MAX_POKEMON_ID + 1)}
        for future in as_completed(futures):
            pid = futures[future]
            data = future.result()
            if data:
                pokemon_data_list.append(data)
            else:
                print(f"Skipping Pokémon ID {pid} due to error.")
    
    return pokemon_data_list

def save_to_csv(pokemon_data, filename='pokemon_data.csv'):
    df = pd.DataFrame(pokemon_data)
    df.to_csv(filename, index=False)
    print(f"Data saved to {filename}")