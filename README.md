# AI-Based Building Tax Verification System

## 📌 Project Overview
This project is a GIS-based building verification system that uses a Convolutional Neural Network (CNN) to predict building width from top-view images and verify property tax by comparing predicted values with municipal records.  
The system helps identify discrepancies such as extra floors or underpaid tax using spatial coordinates and building attributes.

---

## 🎯 Objectives
- Predict building width using deep learning (CNN)
- Calculate building area, number of floors, and estimated property tax
- Verify predicted results with municipal data
- Flag buildings with discrepancies
- Provide a user-friendly GUI for verification

---

## 🛠 Technologies Used
- Python  
- TensorFlow (CNN)  
- OpenCV  
- NumPy, Pandas  
- CustomTkinter (GUI)  
- SQLite (Database)  
- Git & GitHub  

---

## 🧠 System Architecture
1. Input (Coordinates / Image)
2. Image Preprocessing
3. CNN-based Width Prediction
4. Area, Floor & Tax Calculation
5. Municipal Data Comparison
6. Verification Status Output (OK / FLAGGED)

---

## 📂 Project Structure
AI_Based_Building_Tax_Verification/
│
├── train.py
├── width.py
├── vdfg.py
├── test.py
├── test2.py
├── crop.py
├── dataset.py
│
├── images/
├── img/
├── model/
│
├── updated_file.csv
├── municipal_data.csv
│
├── .gitignore
└── README.md

---

## ▶️ How to Run the Project

### Step 1: Install dependencies
pip install tensorflow-cpu==2.15.0
pip install numpy==1.26.4
pip install opencv-python==4.8.1.78
pip install pandas scikit-learn pillow customtkinter joblib
---

### Step 2: Train the CNN model
python train.py


This generates:
- model/width_cnn_model.h5  
- model/width_scaler.pkl  

---

### Step 3: Run the application

Manual Input GUI:
python width.py


Coordinate-Based GUI:
python vdfg.py


---

## 🧪 Test Cases
- test.py – Model loading and prediction test
- test2.py – Verification logic and edge case testing

---

## ✅ Output
- Predicted building width
- Area and number of floors
- Estimated property tax
- Verification status: OK or FLAGGED
- Results stored using SQLite database

---

## 🎓 Use Case
This system can assist municipal authorities in detecting unauthorized constructions, identifying tax evasion, and automating property verification.

---

## 👩‍💻 Author
Bhuvana R Raj  
B.E. – Artificial Intelligence & Machine Learning  
BMS Institute of Technology and Management

---

## 📜 License
This project is developed for academic and educational purposes.
