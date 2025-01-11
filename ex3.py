import tkinter as tk
from tkinter import filedialog
import json

def parse_file(file_path):
    accounts_data = []

    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Split into sections based on the box separator
    sections = content.split('╔══════════════════ Login Information ══════════════════╗')

    for section in sections:
        username_match = re.search(r"Credentials: ([^:]+):", section)
        password_match = re.search(r"Credentials: [^:]+:(\S+)", section)
        country_match = re.search(r"Balance: ¥ [\d.]+\s+\• Persona Name:", section)  # Placeholder
        games_match = re.search(r"All Owned Games: (.*)", section)

        if username_match and password_match:
            username = username_match.group(1)
            password = password_match.group(1)
            country = "Unknown" if country_match else "N/A"  # Replace with actual logic if available

            # Process games and exclude 'library_600x900.jpg'
            games = (
                games_match.group(1).split(",") if games_match else []
            )
            games = [game.strip() for game in games if game.strip() != "library_600x900.jpg"]

            accounts_data.append({
                "username": username,
                "password": password,
                "country": country,
                "games": games,
            })

    return accounts_data

def main():
    # Create a Tkinter root window and hide it
    root = tk.Tk()
    root.withdraw()

    # Show file dialog to select the text file
    file_path = filedialog.askopenfilename(
        title="Select Info File",
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
    )

    if not file_path:
        print("No file selected. Exiting.")
        return

    # Parse the selected file
    accounts_data = parse_file(file_path)

    # Save the output to a JSON file
    output_file = filedialog.asksaveasfilename(
        title="Save Output JSON",
        defaultextension=".json",
        filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")]
    )

    if output_file:
        with open(output_file, 'w', encoding='utf-8') as json_file:
            json.dump(accounts_data, json_file, indent=2)
        print(f"Data saved to {output_file}")
    else:
        print("No output file selected. Exiting.")

if __name__ == "__main__":
    import re
    main()
