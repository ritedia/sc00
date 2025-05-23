from data_fetcher.fetcher import fetch_all_pokemon, save_to_csv
from analyzer.analyzer import analyze_pokemon, save_analysis_to_csv

def main():
    print("Starting Pokémon data collection...")
    pokemon_data = fetch_all_pokemon()
    print(f"Successfully collected data for {len(pokemon_data)} Pokémon")
    
    save_raw = input("Would you like to save the raw Pokémon data to CSV? (y/n): ").lower()
    if save_raw == 'y':
        save_to_csv(pokemon_data)
    
    print("\nAnalyzing Pokémon type effectiveness...")
    analysis_results = analyze_pokemon(pokemon_data)
    print("\nTop 10 Most Effective Pokémon:")
    print(analysis_results[['NAME', 'TYPE1', 'TYPE2', 'NO_STAB', 'TOTAL_EFFECTIVENESS']].head(10))
    
    save_analysis = input("\nWould you like to save the analysis results to CSV? (y/n): ").lower()
    if save_analysis == 'y':
        save_analysis_to_csv(analysis_results)

if __name__ == '__main__':
    main()