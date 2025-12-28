import pandas as pd
import random
import os
from tkinter import Tk, filedialog

# ---------------- Load existing dataset ----------------
csv_file = "municipal_data.csv"  # Replace with your CSV file path
df = pd.read_csv(csv_file)

# ---------------- Select 5 images manually ----------------
root = Tk()
root.withdraw()  # Hide main window
img_files = filedialog.askopenfilenames(
    title="Select 5 building images",
    filetypes=[("Image Files", "*.jpg *.jpeg *.png")],
)

# Limit to 5 images
img_files = list(img_files)[:5]

if len(img_files) == 0:
    print("No images selected. Exiting.")
    exit()

# ---------------- Last known coordinates from last dataset entry ----------------
last_row = df.iloc[-1]
last_lat, last_lon = map(float, last_row['Coordinates'].split(','))

# ---------------- Function to generate building row ----------------
def generate_building_row(building_id, last_lat, last_lon, image_path):
    # Slightly randomize coordinates
    lat = last_lat + random.uniform(-0.01, 0.01)
    lon = last_lon + random.uniform(-0.01, 0.01)
    coordinates = f"{lat:.6f},{lon:.6f}"

    # Random building type
    building_type = random.choice(["Residential", "Commercial", "Industrial"])

    # Random dimensions
    height = round(random.uniform(10, 50), 1)       # meters
    width = round(random.uniform(10, 40), 1)        # meters
    area = round(height * width, 1)                 # simple area estimate
    floors = random.randint(1, 10)

    # Tax rate and total tax
    tax_rate = round(random.uniform(5, 15), 1)      # assume percentage
    total_tax = round(area * tax_rate, 1)

    return [building_id, coordinates, building_type, height, width, area, floors, tax_rate, total_tax, image_path]

# ---------------- Generate new building rows ----------------
new_buildings = []
starting_id = int(last_row['Building_ID'][1:]) + 1  # Next ID number

for i, img_path in enumerate(img_files):
    building_id = f"B{starting_id + i}"
    new_buildings.append(generate_building_row(building_id, last_lat, last_lon, img_path))

# ---------------- Convert to DataFrame ----------------
df_new = pd.DataFrame(new_buildings, columns=df.columns)

# ---------------- Append and save updated CSV ----------------
df_updated = pd.concat([df, df_new], ignore_index=True)
df_updated.to_csv("municipal_data.csv", index=False)

print("5 new buildings added successfully!")
