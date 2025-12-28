import pandas as pd

# =========================================
# Load your dataset
# =========================================
df = pd.read_csv("updated_file.csv")   # Replace with your actual filename

# =========================================
# Calculate Area (Width × Height)
# =========================================
df['Area'] = df['Width'] * df['Building_Height']

# =========================================
# Estimate Floors (assuming 3 meters per floor)
# =========================================
df['Floors'] = (df['Building_Height'] / 3).round().astype(int)

# =========================================
# Assign Tax Rate based on Building Type
# =========================================
# You can adjust these values to fit your city’s municipal logic
def assign_tax_rate(building_type):
    if building_type.lower() == 'residential':
        return 12  # Example: ₹12 per sq.m. per floor
    elif building_type.lower() == 'corporate':
        return 25  # Example: ₹25 per sq.m. per floor
    else:
        return 10  # default for unknown types

df['Tax_Rate'] = df['Building_Type'].apply(assign_tax_rate)

# =========================================
# Calculate Total Tax
# =========================================
df['Total_Tax'] = df['Area'] * df['Floors'] * df['Tax_Rate']

# =========================================
# Rearrange Columns for Municipal Output
# =========================================
municipal_df = df[['Building_ID', 'Coordinates', 'Building_Type', 'Building_Height',
                   'Width', 'Area', 'Floors', 'Tax_Rate', 'Total_Tax', 'TopView_Image']]

# =========================================
# Save to CSV
# =========================================
municipal_df.to_csv("municipal_data.csv", index=False)

print("✅ Municipal data created successfully: 'municipal_data.csv'")
print(municipal_df.head())
