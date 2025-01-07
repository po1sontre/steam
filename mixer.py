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
        # Load the first file
        with open(file1, 'r', encoding='utf-8') as f1:
            content1 = f1.read()
        accounts_data1 = json.loads(content1.replace("const accountsData = ", "").strip(";"))
        
        # Load the second file
        with open(file2, 'r', encoding='utf-8') as f2:
            content2 = f2.read()
        accounts_data2 = json.loads(content2.replace("const accountsData = ", "").strip(";"))
        
        # Combine the two lists and remove duplicates based on 'username'
        combined_accounts = accounts_data1 + accounts_data2
        seen_usernames = set()
        unique_accounts = []
        
        for account in combined_accounts:
            if account['username'] not in seen_usernames:
                seen_usernames.add(account['username'])
                unique_accounts.append(account)
        
        # Write the result to the output file
        js_code = "const accountsData = " + json.dumps(unique_accounts, indent=2, ensure_ascii=False) + ";"
        with open(output_file, 'w', encoding='utf-8') as output:
            output.write(js_code)
        
        print(f"Successfully combined files into {output_file}")
        print(f"Total unique accounts: {len(unique_accounts)}")
    
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    mix_js_files()
