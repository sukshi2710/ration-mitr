import pandas as pd
import re
import os
import glob
from difflib import get_close_matches

# --- CONFIGURATION ---
DATA_FOLDER = "data"  # Ensure your files are in this folder

# 1. THE OFFICIAL "GOLD STANDARD" LIST (36 States/UTs)
OFFICIAL_STATES = [
    "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh", "Goa", "Gujarat", 
    "Haryana", "Himachal Pradesh", "Jharkhand", "Karnataka", "Kerala", "Madhya Pradesh", 
    "Maharashtra", "Manipur", "Meghalaya", "Mizoram", "Nagaland", "Odisha", "Punjab", 
    "Rajasthan", "Sikkim", "Tamil Nadu", "Telangana", "Tripura", "Uttar Pradesh", "Uttarakhand", 
    "West Bengal", "Andaman and Nicobar Islands", "Chandigarh", 
    "Dadra and Nagar Haveli", "Daman and Diu", "Delhi", "Jammu and Kashmir", "Ladakh", 
    "Lakshadweep", "Puducherry"
]

# 2. COMMON TYPO MAPPING (Lowercase keys)
STATE_ALIASES = {
    "orissa": "Odisha",
    "pondicherry": "Puducherry",
    "uttaranchal": "Uttarakhand",
    "telengana": "Telangana",
    "dadra & nagar haveli": "Dadra and Nagar Haveli and Daman and Diu",
    "daman & diu": "Dadra and Nagar Haveli and Daman and Diu",
    "west bangal": "West Bengal",
    "westbengal": "West Bengal",
    "andhra pradesh": "Andhra Pradesh",
    "jammu & kashmir": "Jammu and Kashmir"
}

def clean_state_name(text):
    """
    Analyzes and standardizes state names.
    Returns: Official State Name OR None (if invalid)
    """
    if pd.isna(text): return None
    text = str(text).strip()
    
    # 1. REMOVE NUMBERS (Crucial for "10000", "Karnataka1")
    # If the state name contains digits, we scrub them or drop if it's purely numeric
    if re.search(r'\d', text):
        # If it looks like a purely numeric ID (e.g. "10000"), it's garbage.
        if re.match(r'^\d+$', text): 
            return None
        # Otherwise, try to strip numbers (e.g. "Karnataka1" -> "Karnataka")
        text = re.sub(r'[^a-zA-Z\s]', '', text).strip()

    if len(text) < 2: return None

    # 2. ALIAS CHECK
    lower_text = text.lower()
    if lower_text in STATE_ALIASES:
        return STATE_ALIASES[lower_text]
    
    # 3. EXACT MATCH (Case Insensitive)
    for official in OFFICIAL_STATES:
        if official.lower() == lower_text:
            return official

    # 4. FUZZY MATCH (Fixes "West Bangal" -> "West Bengal")
    # Uses python's built-in library (no pip install needed)
    matches = get_close_matches(text, OFFICIAL_STATES, n=1, cutoff=0.8)
    if matches:
        return matches[0]

    return None # If no match found, mark as Invalid

def process_files():
    # Find all CSV files in the data folder
    all_files = glob.glob(os.path.join(DATA_FOLDER, "*.csv"))
    
    if not all_files:
        print(f"No CSV files found in '{DATA_FOLDER}/'")
        return

    print(f"Found {len(all_files)} files. Starting State Analysis & Cleaning...\n")

    for filepath in all_files:
        filename = os.path.basename(filepath)
        
        # Skip files we just created to avoid loops
        if filename.startswith("state_cleaned_"): continue
        
        try:
            print(f"Processing: {filename}")
            df = pd.read_csv(filepath)
            
            # Normalize column names to lowercase for safety
            df.columns = [c.lower() for c in df.columns]
            
            if 'state' not in df.columns:
                print(f"   Skipping (No 'state' column found)")
                continue

            # --- ANALYSIS BEFORE ---
            unique_before = df['state'].nunique()
            print(f"   Unique States Before: {unique_before}")
            
            # --- CLEANING ---
            df['clean_state'] = df['state'].apply(clean_state_name)
            
            # Drop rows where state is None (Garbage/Numeric)
            invalid_count = df['clean_state'].isna().sum()
            df = df.dropna(subset=['clean_state'])
            
            # Overwrite the original state column with the clean one
            df['state'] = df['clean_state']
            df.drop(columns=['clean_state'], inplace=True)

            # --- ANALYSIS AFTER ---
            unique_after = df['state'].nunique()
            
            # --- SAVE ---
            # We save with a prefix so you know it's the final version
            new_filename = f"state_cleaned_{filename.replace('cleaned_', '')}" 
            new_path = os.path.join(DATA_FOLDER, new_filename)
            
            df.to_csv(new_path, index=False)
            
            print(f"   Saved as: {new_filename}")
            print(f"   Removed {invalid_count} garbage rows (e.g. '10000')")
            print(f"   Reduced duplicates: {unique_before} -> {unique_after} unique states\n")

        except Exception as e:
            print(f"   Error: {e}\n")

if __name__ == "__main__":
    process_files()
    print("State Cleaning Complete!")