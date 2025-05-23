import pandas as pd

def analyze_pokemon(pokemon_data_list, type_chart_path='type_chart.csv'):
    df = pd.DataFrame(pokemon_data_list)
    type_chart = pd.read_csv(type_chart_path, index_col=0)

    def mult_no_stab(attacking_type, defender_type1, defender_type2):
        m = type_chart.loc[attacking_type, defender_type1]
        if defender_type2:
            m *= type_chart.loc[attacking_type, defender_type2]
        return m

    def mult_with_stab(attacking_type, attacker_types, defender_type1, defender_type2):
        m = mult_no_stab(attacking_type, defender_type1, defender_type2)
        if attacking_type in attacker_types:
            m *= 1.5
        return m

    rows = []
    for _, atk in df.iterrows():
        atk_types = [atk['TYPE1']] + ([atk['TYPE2']] if atk['TYPE2'] else [])
        tot_no = 0.0
        tot_yes = 0.0
        for _, defn in df.iterrows():
            if atk['NAME'] == defn['NAME']:
                continue
            d1, d2 = defn['TYPE1'], defn['TYPE2'] or None

            best_no = max(mult_no_stab(t, d1, d2) for t in atk_types)
            best_yes = max(mult_with_stab(t, atk_types, d1, d2) for t in atk_types)

            tot_no += best_no
            tot_yes += best_yes

        rows.append({
            'NAME': atk['NAME'],
            'TYPE1': atk['TYPE1'],
            'TYPE2': atk['TYPE2'],
            'NO_STAB': tot_no,
            'TOTAL_EFFECTIVENESS': tot_yes,
            'STAB_BONUS': tot_yes - tot_no
        })

    out = pd.DataFrame(rows)
    out = out.sort_values('TOTAL_EFFECTIVENESS', ascending=False).reset_index(drop=True)
    return out

def save_analysis_to_csv(analysis_data, filename='pokemon_analysis.csv'):
    analysis_data.to_csv(filename, index=False)
    print(f"Analysis saved to {filename}")