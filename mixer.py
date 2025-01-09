import json
import tkinter as tk
from tkinter import filedialog

def mix_js_files():
    root = tk.Tk()
    root.withdraw()
    
    # Select the first file
    file1 = filedialog.askopenfilename(
        title="Select the First JavaScript File",
        filetypes=[("JavaScript Files", "*.js"), ("All Files", "*.*")]
    )
    if not file1:
        print("No file selected for the first file. Exiting.")
        return

    # Select the second file
    file2 = filedialog.askopenfilename(
        title="Select the Second JavaScript File",
        filetypes=[("JavaScript Files", "*.js"), ("All Files", "*.*")]
    )
    if not file2:
        print("No file selected for the second file. Exiting.")
        return

    # Select output directory
    output_dir = filedialog.askdirectory(title="Select Output Directory")
    if not output_dir:
        print("No output directory selected. Exiting.")
        return

    output_file = f"{output_dir}/mixedAccountsData.js"

    try:
        # Function to extract JSON from JavaScript file
        def extract_json_from_js(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                # Try extracting the JSON portion
                start_index = content.find('[')
                end_index = content.rfind(']') + 1
                if start_index == -1 or end_index == -1:
                    raise ValueError("Unable to extract JSON array from JavaScript content.")
                json_content = content[start_index:end_index]
                return json.loads(json_content)

        # Load and parse both files
        accounts_data1 = extract_json_from_js(file1)
        accounts_data2 = extract_json_from_js(file2)
        
        # Combine the two lists and remove duplicates based on 'username'
        combined_accounts = accounts_data1 + accounts_data2
        seen_usernames = set()
        unique_accounts = []
        
        for account in combined_accounts:
            if account['username'] not in seen_usernames:
                seen_usernames.add(account['username'])
                unique_accounts.append(account)
        
        # Write the result to the output file with only one const accountsData
        js_code = "const accountsData = " + json.dumps(unique_accounts, indent=2, ensure_ascii=False) + ";"
        with open(output_file, 'w', encoding='utf-8') as output:
            output.write(js_code)
        
        print(f"Successfully combined files into {output_file}")
        print(f"Total unique accounts: {len(unique_accounts)}")
    
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    mix_js_files()
