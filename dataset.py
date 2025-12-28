### ================================================================
### 🔹 Auto Dataset Generator (Clean Paths + Full Dummy Data)
### ================================================================
### Generates a realistic building dataset from only images.
### Each record: Building_ID, Coordinates, Relative Image Path,
### Height, Type, Width
### ================================================================
##
##import os
##import pandas as pd
##import random
##
### ------------------ CONFIG ------------------
### 👇 Change this to your image folder
##image_folder = r""
##output_csv = os.path.join(image_folder, "building.csv")
##
### Starting coordinate (Bangalore reference)
##base_lat = 12.9716
##base_lon = 77.5946
##
### Create folder if not exists
##os.makedirs(os.path.dirname(output_csv), exist_ok=True)
##
### ------------------ STEP 1: READ IMAGES ------------------
##images = sorted([
##    f for f in os.listdir(image_folder)
##    if f.lower().endswith(('.jpg', '.jpeg', '.png', '.tif'))
##])
##
##if not images:
##    print(f"❌ No images found in: {image_folder}")
##    exit()
##
### Get the folder name (e.g., 'cropped_images')
##folder_name = os.path.basename(image_folder.rstrip("/\\"))
##
### ------------------ STEP 2: GENERATE DUMMY DATA ------------------
##data = []
##
### if there are fewer than 20 images, repeat some to create a larger dataset
##num_records = max(20, len(images))
##
##for i in range(num_records):
##    img_name = images[i % len(images)]  # loop through images again if needed
##    building_id = f"B{str(i+1).zfill(3)}"
##
##    # Generate random nearby coordinates
##    lat = round(base_lat + random.uniform(-0.01, 0.01), 6)
##    lon = round(base_lon + random.uniform(-0.01, 0.01), 6)
##    coordinates = f"{lat},{lon}"
##
##    # Randomly assign values
##    height = random.randint(10, 40)  # building height (m)
##    btype = random.choice(["Residential", "Corporate"])
##    width = round(random.uniform(8, 18), 1)  # building width (m)
##
##    # ✅ only folder name + image name
##    img_path = f"{folder_name}/{img_name}"
##
##    data.append({
##        "Building_ID": building_id,
##        "Coordinates": coordinates,
##        "TopView_Image": img_path,
##        "Building_Height": height,
##        "Building_Type": btype,
##        "Width": width
##    })
##
### ------------------ STEP 3: SAVE TO CSV ------------------
##df = pd.DataFrame(data)
##df.to_csv(output_csv, index=False)
##
##print(f"✅ Dataset successfully created at: {output_csv}")
##print(df.head(10))
##print("\n📊 Total records created:", len(df))



import pandas as pd

# Load your dataset
df = pd.read_csv(r"D:\champa\projects\home\cropped_images\building.csv")

# Add a new column 'Building_Type' based on the width condition
df['Building_Type'] = df['Width'].apply(lambda x: 'Residential' if x <= 15 else 'Corporate')

# Save the updated dataset
df.to_csv("building_updated.csv", index=False)

print("✅ Building types assigned successfully!")
print(df.head())

