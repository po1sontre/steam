import os
import json
import tkinter as tk
from tkinter import filedialog

def extract_steam_data(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    accounts = []
    
    for line in lines:
        if not line.strip():
            continue
            
        try:
            # Split line by pipe character and clean up whitespace
            parts = [part.strip() for part in line.split('|')]
            
            # Extract username and password from first part
            credentials = parts[0].split(':')
            if len(credentials) != 2:
                continue
                
            username, password = credentials
            
            # Find country
            country = None
            for part in parts:
                if 'Country = ' in part:
                    country = part.replace('Country = ', '').strip()
                    break
            
            # Find and process games list
            games = []
            for i, part in enumerate(parts):
                if 'Games = ' in part:
                    # Start collecting games from this part
                    games_text = ''
                    current_part = part
                    
                    # Keep adding parts until we find 'Total Games = '
                    while i < len(parts) and 'Total Games = ' not in current_part:
                        if 'Games = ' in current_part:
                            # Remove 'Games = ' from the first part
                            current_part = current_part.replace('Games = ', '')
                        games_text += current_part + '|'
                        i += 1
                        if i < len(parts):
                            current_part = parts[i]
                    
                    # Clean up the games text
                    games_text = games_text.strip('|')
                    if games_text.endswith('Total Games = '):
                        games_text = games_text.replace('Total Games = ', '')
                    
                    # Split into individual games, clean up, and remove duplicates while preserving order
                    games_list = [game.strip() for game in games_text.split('|') if game.strip()]
                    
                    # Remove square brackets from first and last games if they exist
                    if games_list:
                        games_list[0] = games_list[0].lstrip('[')  # Remove leading [ from first game
                        games_list[-1] = games_list[-1].rstrip(']')  # Remove trailing ] from last game
                    
                    # Remove duplicates while preserving order
                    seen = set()
                    games = []
                    for game in games_list:
                        if game not in seen:
                            seen.add(game)
                            games.append(game)
                    break
            
            # Create account data dictionary
            account_data = {
                "username": username,
                "password": password,
                "country": country,
                "games": games
            }
            
            accounts.append(account_data)
            
        except Exception as e:
            print(f"Error processing line: {e}")
            continue

    # Convert to JavaScript format with pretty printing
    js_code = "const accountsData = " + json.dumps(accounts, indent=2, ensure_ascii=False) + ";"

    # Write the JavaScript file
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(js_code)

    print(f"Successfully processed {len(accounts)} accounts")
    print(f"JavaScript data has been written to {output_file}")


def select_file_and_generate_js():
    root = tk.Tk()
    root.withdraw()

    input_file = filedialog.askopenfilename(
        title="Select Steam Data Text File",
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
    )

    if not input_file:
        print("No file selected. Exiting.")
        return

    output_dir = filedialog.askdirectory(title="Select Output Directory")
    if not output_dir:
        print("No output directory selected. Exiting.")
        return

    output_file = os.path.join(output_dir, "accountsData.js")

    try:
        extract_steam_data(input_file, output_file)
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    select_file_and_generate_js()