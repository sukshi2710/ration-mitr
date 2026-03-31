import pandas as pd
import re
import os
import glob
from rapidfuzz import process, fuzz

# --- CONFIGURATION ---
DATA_FOLDER = "data"

# Words that distinguish districts (Safety Lock to prevent bad merges)
PROTECTED_KEYWORDS = set(['North', 'South', 'East', 'West', 'Central', 'Rural', 'Urban', 'Upper', 'Lower'])

def clean_district_nuclear(text):
    """
    STRICT CLEANING FUNCTION:
    Returns None if the data is "garbage" (contains numbers).
    """
    if pd.isna(text): return None
    text = str(text)
    
    # --- THE NUCLEAR RULE ---
    # If it contains ANY number (0-9), mark for DELETION.
    if re.search(r'\d', text): 
        return None
    
    # Clean junk: Remove content in brackets like (BH)
    text = re.sub(r'\(.*?\)', '', text)
    
    # Remove special chars (keep only letters, dots, hyphens, spaces)
    text = re.sub(r'[^a-zA-Z\s\-\.]', '', text)
    
    text = text.strip().title()
    
    # If the name is too short (e.g. "A"), mark for deletion
    if len(text) < 2: return None
    
    return text

def get_smart_district_map(series, threshold=88):
    """
    AI Deduplication:
    Uses 'Frequency' to decide the 'Correct' name.
    """
    # Get unique names sorted by Frequency (Most common first)
    counts = series.value_counts()
    unique_names = counts.index.tolist()
    
    print(f"      - AI analyzing {len(unique_names)} unique district variations...")
    
    mapping = {}
    accepted_names = []
    
    for name in unique_names:
        # 1. Identify "Directional" words (North/South/etc)
        name_dirs = set([w for w in name.split() if w in PROTECTED_KEYWORDS])
        
        # 2. Try to match with an already accepted (more frequent) name
        match = process.extractOne(name, accepted_names, scorer=fuzz.token_sort_ratio)
        
        found_match = False
        if match and match[1] >= threshold:
            candidate = match[0]
            
            # 3. SAFETY CHECK: Directional Words must match
            cand_dirs = set([w for w in candidate.split() if w in PROTECTED_KEYWORDS])
            
            if name_dirs == cand_dirs:
                mapping[name] = candidate # Merge typo into the common name
                found_match = True
        
        if not found_match:
            mapping[name] = name # Accept this as a new unique district
            accepted_names.append(name)
            
    return mapping

def process_files():
    # Find all CSV files in the data folder
    all_files = glob.glob(os.path.join(DATA_FOLDER, "*.csv"))
    
    if not all_files:
        print(f"No CSV files found in '{DATA_FOLDER}/'")
        return

    print(f"Found {len(all_files)} files. Starting Strict District Cleaning...\n")

    for filepath in all_files:
        filename = os.path.basename(filepath)
        
        # Skip output files so we don't process them twice
        if filename.startswith("district_cleaned_"): continue
        
        try:
            print(f"Processing: {filename}")
            df = pd.read_csv(filepath)
            
            # Normalize column names to lowercase
            df.columns = [c.lower() for c in df.columns]
            
            if 'district' not in df.columns:
                print(f"   Skipping (No 'district' column)")
                continue

            # Record stats before cleaning
            rows_before = len(df)
            
            # --- 1. DETECT & DELETE NUMERICAL ENTRIES ---
            # Apply the nuclear function
            df['clean_district'] = df['district'].apply(clean_district_nuclear)
            
            # *** CRITICAL STEP *** # Drop any row where clean_district is None (this means it had numbers)
            df = df.dropna(subset=['clean_district'])
            
            # --- 2. AI MERGE (Fix Spelling) ---
            # Generates the correction map based on the surviving valid data
            correction_map = get_smart_district_map(df['clean_district'])
            
            # Apply the map to fix typos (e.g. "Ahmed Nagar" -> "Ahmednagar")
            df['district'] = df['clean_district'].map(correction_map)
            df.drop(columns=['clean_district'], inplace=True)
            
            # Stats after cleaning
            rows_after = len(df)
            dropped_count = rows_before - rows_after
            
            # --- SAVE ---
            # Create a new filename (e.g. district_cleaned_original.csv)
            clean_name = filename.replace('cleaned_', '').replace('state_cleaned_', '')
            new_filename = f"district_cleaned_{clean_name}"
            new_path = os.path.join(DATA_FOLDER, new_filename)
            
            df.to_csv(new_path, index=False)
            
            print(f"   Saved as: {new_filename}")
            print(f"   DELETED {dropped_count} rows containing numbers (e.g. '10000')")
            print(f"   Unique Districts: {df['district'].nunique()}\n")

        except Exception as e:
            print(f"   Error: {e}\n")

if __name__ == "__main__":
    process_files()
    print("Strict District Cleaning Complete!")