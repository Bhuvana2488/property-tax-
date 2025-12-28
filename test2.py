# ============================================================
# 🏗 GIS BUILDING VERIFICATION SYSTEM (CustomTkinter + CNN Width)
# ============================================================

import os
import cv2
import numpy as np
import pandas as pd
import joblib
import sqlite3
from datetime import datetime
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
from tensorflow.keras.models import load_model
import customtkinter as ctk

# ============================================================
# 1️⃣ MODEL + DATA
# ============================================================
width_cnn = load_model("model/width_cnn_model.h5", compile=False)
width_scaler = joblib.load("model/width_scaler.pkl")

MUNICIPAL_PATH = "municipal_data.csv"

# (Optional) If you want DB logging like your other app:
conn = sqlite3.connect("gis_buildings_temp.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS temp_verifications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    Coordinates TEXT,
    Height REAL,
    Building_Type TEXT,
    Predicted_Width REAL,
    Area REAL,
    Predicted_Floors INTEGER,
    Predicted_Tax REAL,
    Alert_Status TEXT,
    Alert_Message TEXT,
    Timestamp TEXT
)
""")
conn.commit()

# ============================================================
# 2️⃣ IMAGE PREPROCESSING
# ============================================================
def preprocess_image(path):
    if not os.path.exists(path):
        messagebox.showerror("Error", f"Image not found:\n{path}")
        return None

    img = cv2.imread(path)
    if img is None:
        messagebox.showerror("Error", "Unable to read image file!")
        return None

    img = cv2.resize(img, (128, 128))
    return img / 255.0


# ============================================================
# 3️⃣ PREDICTION + COMPARISON
# ============================================================
def predict_all():
    coords = coord_entry.get().strip()
    height = height_entry.get().strip()
    btype = type_entry.get().strip()
    img_path = selected_image.get().strip()

    if not coords or not height or not btype or not img_path:
        messagebox.showwarning("Missing", "Fill all fields and upload image!")
        return

    # Parse inputs
    try:
        lat, lon = map(float, coords.split(","))
        height_val = float(height)
    except Exception:
        messagebox.showerror("Format Error", "Check coordinates and height format!")
        return

    # ----- IMAGE WIDTH PREDICTION -----
    img = preprocess_image(img_path)
    if img is None:
        return

    pred_scaled = width_cnn.predict(np.expand_dims(img, 0))
    width_val = float(width_scaler.inverse_transform(pred_scaled)[0][0])

    # ----- COMPUTE LOGIC -----
    floor_h = 3 if btype.lower() == "residential" else 3.5
    tax_rate = 12.5 if btype.lower() == "residential" else 18.0

    floors_pred = round(height_val / floor_h)
    area_pred = width_val * height_val
    tax_pred = area_pred * floors_pred * tax_rate

    # ----- MUNICIPAL COMPARISON -----
    status = "OK"
    msg = "No discrepancies."

    if os.path.exists(MUNICIPAL_PATH):
        muni = pd.read_csv(MUNICIPAL_PATH)

        match = muni[
            (muni["Coordinates"].astype(str).str.contains(str(lat))) &
            (muni["Coordinates"].astype(str).str.contains(str(lon)))
        ]

        if not match.empty:
            m = match.iloc[0]
            floor_diff = floors_pred - m.get("Floors", 0)
            tax_diff = tax_pred - m.get("Total_Tax", 0)

            if floor_diff > 0 or tax_diff > 0:
                status = "FLAGGED"
                msg = f"Extra Floors = {floor_diff}, Underpaid = ₹{tax_diff:,.2f}"

    # ----- OPTIONAL: SAVE TO TEMP DB -----
    cursor.execute("""
    INSERT INTO temp_verifications
    (Coordinates, Height, Building_Type, Predicted_Width, Area,
     Predicted_Floors, Predicted_Tax, Alert_Status, Alert_Message, Timestamp)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        coords, height_val, btype,
        width_val, area_pred, floors_pred, tax_pred,
        status, msg, datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))
    conn.commit()

    # ----- COLOR INDICATION -----
    status_color = "green" if status == "OK" else "red"
    msg_color = "green" if status == "OK" else "red"

    # ----- DISPLAY RESULTS -----
    result_box.delete("1.0", "end")
    result_box.insert(
        "end",
        f"📍 Coordinates: {coords}\n"
        f"🏗 Type: {btype}\n"
        f"📏 Height: {height_val:.2f} m\n"
        f"📐 Predicted Width: {width_val:.2f} m\n"
        f"📦 Area: {area_pred:.2f} sq.m\n"
        f"🏢 Floors: {floors_pred}\n"
        f"💰 Tax: ₹{tax_pred:,.2f}\n"
    )

    status_label.configure(text=f"STATUS: {status}", text_color=status_color)
    msg_label.configure(text=msg, text_color=msg_color)


# ============================================================
# 4️⃣ IMAGE CHOOSER
# ============================================================
def choose_image():
    path = filedialog.askopenfilename(
        title="Choose Top View Image",
        filetypes=[("Image Files", "*.jpg *.jpeg *.png")]
    )
    if path:
        selected_image.set(path)
        image_info_label.configure(text="Image Selected ✓", text_color="#1E88E5")


# ============================================================
# 5️⃣ GUI DESIGN (CustomTkinter, like main app)
# ============================================================
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("GIS Building Verification (Image + Inputs)")
root.geometry("1100x820")

# ---------- HEADER ----------
header = ctk.CTkFrame(root, fg_color="#1E467F", corner_radius=0)
header.pack(fill="x")

header_label = ctk.CTkLabel(
    header,
    text="🏛 GIS Building Verification System",
    font=("Segoe UI", 26, "bold"),
    text_color="white"
)
header_label.pack(pady=15)

# ---------- MAIN AREA ----------
main = ctk.CTkFrame(root, fg_color="#E8EEF3")
main.pack(fill="both", expand=True)

# ================= INPUT CARD =================
input_card = ctk.CTkFrame(main, fg_color="white", corner_radius=12)
input_card.pack(fill="x", padx=30, pady=(20, 10))

input_card.grid_columnconfigure(0, weight=0)
input_card.grid_columnconfigure(1, weight=1)

# Title
input_title = ctk.CTkLabel(
    input_card,
    text="📥 Building Inputs & Image",
    font=("Segoe UI", 18, "bold"),
    text_color="#1E467F"
)
input_title.grid(row=0, column=0, columnspan=2, padx=15, pady=(10, 5), sticky="w")

# Divider
sep1 = ctk.CTkFrame(input_card, height=1, fg_color="#D0D5DD")
sep1.grid(row=1, column=0, columnspan=2, sticky="ew", padx=15, pady=(0, 8))


# ------------------- COORDINATES -------------------
coord_label = ctk.CTkLabel(
    input_card, text="Coordinates (lat, lon):", font=("Segoe UI", 14)
)
coord_label.grid(row=2, column=0, padx=(15, 5), pady=6, sticky="e")

coord_entry = ctk.CTkEntry(
    input_card,
    width=300,
    font=("Segoe UI", 14),
    placeholder_text="12.9716,77.5946"
)
coord_entry.grid(row=2, column=1, padx=(5, 15), pady=6, sticky="w")

# Make cursor appear immediately
coord_entry.focus_set()
coord_entry.bind("<Button-1>", lambda e: coord_entry.focus_set())


# ------------------- HEIGHT -------------------
height_label = ctk.CTkLabel(
    input_card, text="Building Height (m):", font=("Segoe UI", 14)
)
height_label.grid(row=3, column=0, padx=(15, 5), pady=6, sticky="e")

height_entry = ctk.CTkEntry(
    input_card, width=300, font=("Segoe UI", 14), placeholder_text="e.g., 14"
)
height_entry.grid(row=3, column=1, padx=(5, 15), pady=6, sticky="w")


# ------------------- TYPE -------------------
type_label = ctk.CTkLabel(
    input_card, text="Building Type:", font=("Segoe UI", 14)
)
type_label.grid(row=4, column=0, padx=(15, 5), pady=6, sticky="e")

type_entry = ctk.CTkEntry(
    input_card, width=300, font=("Segoe UI", 14),
    placeholder_text="Residential / Commercial"
)
type_entry.grid(row=4, column=1, padx=(5, 15), pady=6, sticky="w")


# ------------------- IMAGE SELECTOR -------------------
selected_image = ctk.StringVar()

def choose_image():
    path = filedialog.askopenfilename(
        title="Choose Top View Image",
        filetypes=[("Image Files", "*.jpg *.jpeg *.png")]
    )
    if path:
        selected_image.set(path)
        image_info_label.configure(text="Image Selected ✓", text_color="#1E88E5")

img_btn = ctk.CTkButton(
    input_card,
    text="🖼 Upload Top View Image",
    font=("Segoe UI", 14),
    fg_color="#455A64",
    hover_color="#263238",
    command=choose_image
)
img_btn.grid(row=5, column=0, padx=(15, 5), pady=10, sticky="e")

image_info_label = ctk.CTkLabel(
    input_card,
    text="No image selected",
    font=("Segoe UI", 13),
    text_color="#666"
)
image_info_label.grid(row=5, column=1, padx=(5, 15), pady=10, sticky="w")


# ------------------- CENTER BUTTON -------------------
button_frame = ctk.CTkFrame(input_card, fg_color="white")
button_frame.grid(row=6, column=0, columnspan=2, pady=12)

predict_btn = ctk.CTkButton(
    button_frame,
    text="🔍 Predict & Compare",
    width=220,
    fg_color="#1E88E5",
    hover_color="#1565C0",
    font=("Segoe UI", 15, "bold"),
    command=lambda: root.after(1, predict_all)
)
predict_btn.pack()

# ================= RESULTS CARD =================
results_card = ctk.CTkFrame(main, fg_color="white", corner_radius=12)
results_card.pack(fill="both", expand=True, padx=30, pady=10)

results_title = ctk.CTkLabel(
    results_card,
    text="📊 Prediction Results",
    font=("Segoe UI", 18, "bold"),
    text_color="#1E467F"
)
results_title.pack(anchor="w", padx=15, pady=(10, 5))

sep2 = ctk.CTkFrame(results_card, height=1, fg_color="#D0D5DD")
sep2.pack(fill="x", padx=15, pady=(0, 8))

result_box = ctk.CTkTextbox(
    results_card,
    fg_color="#F9FAFB",
    text_color="black",
    corner_radius=8,
    font=("Segoe UI", 14),
)
result_box.pack(fill="both", expand=True, padx=15, pady=(0, 15))

# ================= STATUS CARD =================
status_card = ctk.CTkFrame(main, fg_color="white", corner_radius=12)
status_card.pack(fill="x", padx=30, pady=(5, 18))

status_title = ctk.CTkLabel(
    status_card,
    text="🔎 Verification Status",
    font=("Segoe UI", 18, "bold"),
    text_color="#1E467F"
)
status_title.pack(anchor="w", padx=15, pady=(10, 5))

status_row = ctk.CTkFrame(status_card, fg_color="white")
status_row.pack(fill="x", padx=15, pady=(5, 10))

status_label = ctk.CTkLabel(
    status_row,
    text="STATUS:",
    font=("Segoe UI", 18, "bold"),
    fg_color="#EEEEEE",
    text_color="black",
    corner_radius=6,
    width=230,
    height=40
)
status_label.pack(side="left", padx=(0, 15))

msg_label = ctk.CTkLabel(
    status_row,
    text="",
    font=("Segoe UI", 14),
    fg_color="#F9FAFB",
    text_color="black",
    corner_radius=6,
    width=500,
    wraplength=500,
    anchor="w",
    justify="left"
)
msg_label.pack(side="left")

# ============================================================
# CLOSE HANDLER
# ============================================================
def on_close():
    conn.close()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_close)
root.mainloop()