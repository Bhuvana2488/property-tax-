# ============================================================
# 🏗 GIS BUILDING PREDICTION SYSTEM (WIDTH MODEL ONLY)
# ============================================================

import os
os.environ["TK_SILENCE_DEPRECATION"] = "1"

import cv2
import numpy as np
import pandas as pd
import joblib
import sqlite3
from datetime import datetime
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from tensorflow.keras.models import load_model
import customtkinter as ctk

# ============================================================
# MODEL + DATA
# ============================================================
width_cnn = load_model("model/width_cnn_model.h5", compile=False)
width_scaler = joblib.load("model/width_scaler.pkl")

df = pd.read_csv("updated_file.csv")
MUNICIPAL_DATA_PATH = "municipal_data.csv"

# ============================================================
# DATABASE
# ============================================================
conn = sqlite3.connect("gis_buildings.db")
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS buildings (
    Building_ID TEXT PRIMARY KEY,
    Latitude REAL,
    Longitude REAL,
    Building_Type TEXT,
    Height REAL,
    Predicted_Width REAL,
    Area REAL,
    Predicted_Floors INTEGER,
    Predicted_Tax REAL,
    Alert_Status TEXT,
    Alert_Message TEXT,
    Timestamp TEXT
)
''')
conn.commit()

# ============================================================
# IMAGE PREPROCESS
# ============================================================
def preprocess_image(img_path):
    if not os.path.exists(img_path):
        messagebox.showerror("Missing", f"Image not found: {img_path}")
        return None

    img = cv2.imread(img_path)
    img = cv2.resize(img, (128, 128))
    return img / 255.0

# ============================================================
# PREDICT FUNCTION
# ============================================================
def predict_and_display():
    coords = coord_entry.get().strip()
    if not coords:
        messagebox.showwarning("Missing Input", "Enter coordinates!")
        return

    try:
        lat, lon = map(float, coords.split(","))
    except:
        messagebox.showerror("Format Error", "Use format: 12.9716,77.5946")
        return

    record = df[df["Coordinates"].str.contains(str(lat)) &
                df["Coordinates"].str.contains(str(lon))]

    if record.empty:
        messagebox.showerror("Error", "No building found for these coordinates.")
        return

    record = record.iloc[0]
    height_final = float(record["Building_Height"])
    type_final = record["Building_Type"]

    img = preprocess_image(record["TopView_Image"])
    if img is None:
        return

    pred_scaled = width_cnn.predict(np.expand_dims(img, 0))
    pred_width = width_scaler.inverse_transform(pred_scaled)[0][0]

    floor_height = 3 if type_final.lower() == "residential" else 3.5
    tax_rate = 12.5 if type_final.lower() == "residential" else 18.0

    pred_area = pred_width * height_final
    pred_floors = round(height_final / floor_height)
    pred_tax = pred_area * pred_floors * tax_rate

    alert_status = "OK"
    alert_message = "No discrepancies."

    if os.path.exists(MUNICIPAL_DATA_PATH):
        muni_df = pd.read_csv(MUNICIPAL_DATA_PATH)
        muni = muni_df[muni_df["Coordinates"].str.contains(str(lat)) &
                       muni_df["Coordinates"].str.contains(str(lon))]

        if not muni.empty:
            muni = muni.iloc[0]
            floor_diff = pred_floors - muni.get("Floors", 0)
            tax_diff = pred_tax - muni.get("Total_Tax", 0)

            if floor_diff > 0 or tax_diff > 0:
                alert_status = "Flagged"
                alert_message = f"Extra Floors = {floor_diff}, Underpaid = ₹{tax_diff:,.2f}"

    # Insert DB
    cursor.execute("""
    INSERT OR REPLACE INTO buildings
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        record["Building_ID"], lat, lon, type_final, height_final,
        pred_width, pred_area, pred_floors, pred_tax,
        alert_status, alert_message, datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))
    conn.commit()

    result_box.delete("1.0", "end")
    result_box.insert("end",
        f"📍 Coordinates: {coords}\n"
        f"🏗 Building Type: {type_final}\n"
        f"📏 Height: {height_final:.2f} m\n"
        f"📐 Width: {pred_width:.2f} m\n"
        f"📦 Area: {pred_area:.2f} sq.m\n"
        f"🏢 Floors: {pred_floors}\n"
        f"💰 Tax: ₹{pred_tax:,.2f}\n"
    )

    if alert_status == "OK":
        big_status_label.configure(text="STATUS: OK", text_color="green")
        big_status_message.configure(text="No discrepancies found.", text_color="green")
    else:
        big_status_label.configure(text="STATUS: FLAGGED", text_color="red")
        big_status_message.configure(text=alert_message, text_color="red")


# ============================================================
# UI
# ============================================================
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("GIS Building Prediction System")
root.geometry("1100x820")

# HEADER
header = ctk.CTkFrame(root, fg_color="#1E467F", corner_radius=0)
header.pack(fill="x")

ctk.CTkLabel(
    header,
    text="🏛 GIS Building Prediction System",
    font=("Segoe UI", 26, "bold"),
    text_color="white"
).pack(pady=15)

# MAIN AREA
main = ctk.CTkFrame(root, fg_color="#E8EEF3")
main.pack(fill="both", expand=True)

main.grid_rowconfigure(0, weight=1)
main.grid_rowconfigure(1, weight=1)
main.grid_rowconfigure(2, weight=1)
main.grid_columnconfigure(0, weight=1)

# INPUT CARD
input_card = ctk.CTkFrame(main, fg_color="white", corner_radius=10)
input_card.grid(row=0, column=0, padx=30, pady=20, sticky="ew")
input_card.grid_columnconfigure(0, weight=1)
input_card.grid_columnconfigure(1, weight=1)
input_card.grid_rowconfigure(0, weight=0)
input_card.grid_rowconfigure(1, weight=0)
input_card.grid_rowconfigure(2, weight=1)   # IMPORTANT
input_card.grid_rowconfigure(3, weight=0)

# Title
ctk.CTkLabel(
    input_card,
    text="📥 Building Verification Inputs",
    font=("Segoe UI", 18, "bold"),
    text_color="#1E467F"
).grid(row=0, column=0, columnspan=2, pady=(10, 5), padx=15, sticky="w")

# Coordinates
ctk.CTkLabel(
    input_card,
    text="Coordinates (lat, lon):",
    font=("Segoe UI", 15)
).grid(row=1, column=0, padx=(15, 5), pady=10, sticky="e")

coord_entry = ctk.CTkEntry(input_card, width=300, font=("Segoe UI", 15))
coord_entry.grid(row=1, column=1, padx=(5, 15), pady=10, sticky="w")

# Fix cursor not appearing
coord_entry.focus_set()
coord_entry.bind("<Button-1>", lambda e: coord_entry.focus_set())

# Button centered
button_frame = ctk.CTkFrame(input_card, fg_color="white")
button_frame.grid(row=2, column=0, columnspan=2, pady=10)

predict_btn = ctk.CTkButton(
    button_frame,
    text="🔍 Predict & Compare",
    width=200,
    fg_color="#1E88E5",
    hover_color="#1565C0",
    font=("Segoe UI", 15, "bold"),
    command=predict_and_display
)
predict_btn.pack()

# Fix button first-click issue
predict_btn.bind("<Button-1>", lambda e: predict_btn.focus_set())

# ---------- RESULTS CARD ----------
results_card = ctk.CTkFrame(main, fg_color="white", corner_radius=10)
results_card.grid(row=1, column=0, padx=30, pady=10, sticky="nsew")

# allow results card to expand fully
main.grid_rowconfigure(1, weight=1)
results_card.grid_columnconfigure(0, weight=1)

ctk.CTkLabel(
    results_card,
    text="📊 Prediction Results",
    font=("Segoe UI", 18, "bold"),
    text_color="#1E467F"
).grid(row=0, column=0, padx=15, pady=10, sticky="w")

result_box = ctk.CTkTextbox(
    results_card,
    fg_color="#F9FAFB",
    text_color="black",
    corner_radius=8,
    font=("Segoe UI", 14),
    height=250
)
result_box.grid(row=1, column=0, padx=15, pady=10, sticky="nsew")


# STATUS CARD
status_card = ctk.CTkFrame(main, fg_color="white", corner_radius=10)
status_card.grid(row=2, column=0, padx=30, pady=15, sticky="ew")

ctk.CTkLabel(
    status_card,
    text="🔎 Verification Status",
    font=("Segoe UI", 18, "bold"),
    text_color="#1E467F"
).grid(row=0, column=0, columnspan=2, padx=15, pady=10, sticky="w")

big_status_label = ctk.CTkLabel(
    status_card,
    text="STATUS:",
    font=("Segoe UI", 20, "bold"),
    fg_color="#EEEEEE",
    text_color="black",
    corner_radius=6,
    width=240
)
big_status_label.grid(row=1, column=0, padx=15, pady=8, sticky="w")

big_status_message = ctk.CTkLabel(
    status_card,
    text="",
    font=("Segoe UI", 14),
    fg_color="#F9FAFB",
    text_color="black",
    corner_radius=6,
    width=450,
    wraplength=450,
    anchor="w",
    justify="left"
)
big_status_message.grid(row=1, column=1, padx=15, pady=8, sticky="w")

# CLOSE HANDLER
def on_close():
    conn.close()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_close)
root.mainloop()