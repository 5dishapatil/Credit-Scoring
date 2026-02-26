import pandas as pd

df_raw = pd.read_csv("dataset/paysim_dataset.csv",
                 nrows=1000000)

df_raw.head()

import pandas as pd
import numpy as np
from datetime import timedelta

print("⏳ Generating Multi-Tenant MSME Database...")

# Assuming your raw 1M row PaySim dataframe is loaded as `df_raw`
company_ids = ['MSME_RETAIL_001', 'MSME_TECH_002', 'MSME_AGRI_003', 'MSME_MANUF_004', 'MSME_SERVICES_005']
all_companies_data = []

# Base start date for our simulations
base_date = pd.Timestamp("2021-01-01 08:00:00")

for company in company_ids:
    # 1. Sample 300 to 600 transactions for each company to create a rich history
    txn_count = np.random.randint(300, 600)
    df_comp = df_raw.sample(n=txn_count).copy()
    
    # 2. Assign the unique identifier
    df_comp['nameOrig'] = company
    
    # 3. Sort chronologically and create realistic dates (1-2 transactions per day)
    df_comp = df_comp.sort_values(by='step').reset_index(drop=True)
    time_deltas = [timedelta(days=np.random.uniform(0.5, 2)) for _ in range(txn_count)]
    df_comp['Date'] = base_date + pd.Series(time_deltas).cumsum()
    
    # 4. Mathematically Correct the Running Balances (Crucial for DB1 graphs)
    starting_balance = np.random.uniform(50000, 200000)
    balances = []
    current_balance = starting_balance
    
    for index, row in df_comp.iterrows():
        amount = row['amount']
        txn_type = row['type']
        
        if txn_type == 'CASH_IN':
            current_balance += amount
        else: # CASH_OUT, PAYMENT, TRANSFER, DEBIT
            # Prevent massive negative balances to keep the simulation realistic
            if current_balance - amount < 1000:
                amount = current_balance * np.random.uniform(0.1, 0.4)
                df_comp.at[index, 'amount'] = amount
            current_balance -= amount
            
        balances.append(current_balance)
        
    df_comp['Balance'] = balances
    all_companies_data.append(df_comp)

# Combine all companies into a single Master Database DataFrame
df_master_db = pd.concat(all_companies_data, ignore_index=True)

# Clean up columns for the final DB1 format
cols_to_keep = ['nameOrig', 'Date', 'type', 'amount', 'nameDest', 'Balance']
df_master_db = df_master_db[cols_to_keep]

print(f"✅ Created Master Database with {len(df_master_db)} total transactions across {len(company_ids)} companies.")
print(df_master_db.head())
print(df_master_db['nameOrig'].value_counts())

# Save this so you can use it to test your Django Uploads
df_master_db.to_csv("Multi_Company_Raw_Transactions.csv", index=False)