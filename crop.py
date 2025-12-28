import cv2
import os

# ============================
# 🔧 PATH SETTINGS
# ============================
input_folder = r"C:\Users\BHUVANA\Downloads\AI_Based_Building_Tax_Verification\AI_Based_Building_Tax_Verification\img"  # Folder containing your .tif images
output_folder = "cropped_images"  # Folder to save cropped parts
os.makedirs(output_folder, exist_ok=True)

# ============================
# 🧩 LOOP OVER ALL TIF IMAGES
# ============================
for filename in os.listdir(input_folder):
    if filename.lower().endswith(".tif"):
        img_path = os.path.join(input_folder, filename)
        img = cv2.imread(img_path)

        if img is None:
            print(f"⚠️ Skipping invalid image: {filename}")
            continue

        base_name = os.path.splitext(filename)[0]
        count = 0

        print(f"\n📸 Processing: {filename}")
        print("👉 Draw boxes with your mouse. Press ENTER or SPACE to confirm crop. ESC to skip.\n")

        while True:
            # Select Region of Interest (ROI)
            r = cv2.selectROI("Select Region", img, showCrosshair=True)
            x, y, w, h = r

            # Stop if user pressed ESC or selected nothing
            if w == 0 or h == 0:
                print("✅ Done with this image.")
                break

            # Crop and save
            cropped = img[int(y):int(y+h), int(x):int(x+w)]
            count += 1
            save_name = f"crop_{base_name}_{count}.jpg"
            save_path = os.path.join(output_folder, save_name)
            cv2.imwrite(save_path, cropped)

            print(f"💾 Saved: {save_name}")

            # Ask if want to crop another region
            key = input("Crop another region in this image? (y/n): ").strip().lower()
            if key != 'y':
                break

        cv2.destroyAllWindows()

print("\n🎯 All manual crops saved in:", output_folder)
