# 🏛 AI-Based Building Tax Verification System

## 📌 Project Overview

This project is a GIS-based building verification system that uses a **Convolutional Neural Network (CNN)** to predict building width from top-view images and validate property tax records.

The system computes building attributes such as **area, number of floors, and estimated tax**, and compares them with municipal data to detect discrepancies like **unauthorized construction or underpaid taxes**.

---

## 🎯 Objectives

* Predict building width from satellite/top-view images using deep learning
* Compute building area, number of floors, and estimated property tax
* Compare predicted values with municipal records
* Detect and flag discrepancies (e.g., extra floors, tax mismatch)
* Provide an interactive GUI for real-time verification

---

## 🛠 Technologies Used

* **Python**
* **TensorFlow / Keras (CNN Model)**
* **OpenCV** (image preprocessing)
* **NumPy, Pandas** (data processing)
* **Scikit-learn** (scaling, evaluation metrics)
* **CustomTkinter** (GUI)
* **SQLite** (data storage)
* **Git & GitHub**

---

## 🧠 System Architecture

```
Input (Image + Building Details)
        ↓
Image Preprocessing (Resize, Normalize)
        ↓
CNN Model → Width Prediction
        ↓
Area, Floors & Tax Calculation
        ↓
Comparison with Municipal Data
        ↓
Verification Output → OK / FLAGGED 🚨
```

---

## 🤖 Model Details

* Input: Top-view building image (128×128)
* Architecture:

  * Conv2D → ReLU → MaxPooling
  * Conv2D → ReLU → MaxPooling
  * Conv2D → ReLU → MaxPooling
  * Flatten → Dropout → Dense (Linear Output)
* Output: **Continuous value (building width in meters)**

### 📊 Evaluation Metrics

Since this is a **regression problem**, the model is evaluated using:

* **R² Score**
* **Mean Absolute Error (MAE)**

---

## 📂 Project Structure

```
AI_Based_Building_Tax_Verification/
│
├── train.py                # CNN model training
├── test.py                 # Dataset-based prediction GUI
├── test2.py                # Image upload + verification GUI (main app)
├── width.py                # Alternate UI version
├── vdfg.py                 # Coordinate-based version
├── dataset.py              # Dataset utilities
├── crop.py                 # Image preprocessing tools
│
├── model/
│   ├── width_cnn_model.h5
│   └── width_scaler.pkl
│
├── images/                 # Dataset images
├── img/                    # Additional images
│
├── updated_file.csv        # Training dataset
├── municipal_data.csv      # Municipal reference dataset
│
├── .gitignore
└── README.md
```

---

## ▶️ How to Run the Project

### 1️⃣ Install Dependencies

```bash
pip install tensorflow-cpu==2.15.0
pip install numpy==1.26.4
pip install opencv-python==4.8.1.78
pip install pandas scikit-learn pillow customtkinter joblib
```

---

### 2️⃣ Train the Model

```bash
python train.py
```

This generates:

* `model/width_cnn_model.h5`
* `model/width_scaler.pkl`

---

## 🧪 Testing

* `test.py` → Prediction using dataset entries
* `test2.py` → Real-time prediction using uploaded images

---

## ✅ Output

* Predicted building width
* Computed area and number of floors
* Estimated property tax
* Verification result:

  * ✅ **OK**
  * 🚨 **FLAGGED (discrepancy detected)**
* Results optionally stored in SQLite database

---

## 🎓 Use Case

This system can assist:

* Municipal authorities in detecting unauthorized constructions
* Identifying property tax evasion
* Automating large-scale building verification using AI

---
## 📸 Results & Demo

---

## 🔹 Test 1: Coordinate-Based Verification (Dataset Input)

### ✅ 1. Successful Prediction (No Discrepancy)

![text](Screenshot%202026-04-01%20195006.png)

✔️ Input is taken using coordinates from dataset
✔️ Model predicts width and computes area, floors, and tax
✔️ Status: **OK (No discrepancies found)**

---

### 🚨 2. Discrepancy Detection (FLAGGED)

![text](Screenshot%202026-04-01%20195036.png)

✔️ Predicted values differ from municipal data
✔️ Detects **underpaid tax / mismatch**
✔️ Status: **FLAGGED**

---

### ⚠️ 3. Invalid Coordinates Handling

![text](Screenshot%202026-04-01%20195051.png)

✔️ Handles cases where coordinates are not found
✔️ Displays error: *“No building found for these coordinates”*

---

### ⚠️ 4. Input Format Validation

![text](Screenshot%202026-04-01%20195105.png)

✔️ Ensures correct coordinate format
✔️ Displays helpful error message for incorrect input

---

## 🔹 Test 2: Image-Based Verification (Real-Time Input)

### 🚨 5. Image Upload + FLAGGED Detection

![text](Screenshot%202026-04-01%20195132.png)

✔️ User uploads building image manually
✔️ CNN predicts width
✔️ System detects discrepancy → **FLAGGED (extra floors / tax mismatch)**

---

### ⚠️ 6. Missing Input Validation

![text](Screenshot%202026-04-01%20195145.png)

✔️ Prevents prediction if fields or image are missing
✔️ Displays warning message

---

### ⚠️ 7. Input Error Handling

![text](Screenshot%202026-04-01%20195201.png)

✔️ Detects incorrect coordinate or height format
✔️ Ensures robust validation

---

### ✅ 8. Successful End-to-End Prediction

![text](Screenshot%202026-04-01%20195213.png)

✔️ Complete pipeline execution:

* Image → CNN Prediction → Tax Calculation → Verification
  ✔️ Status: **OK**

## 🚀 Future Enhancements

* Use real satellite imagery datasets
* Improve model accuracy with larger datasets
* Deploy as a web application
* Integrate GIS APIs for real-time mapping

---

## 👩‍💻 Author

**Bhuvana R Raj**
B.E. – Artificial Intelligence & Machine Learning
BMS Institute of Technology and Management

---

## 📜 License

This project is developed for academic and educational purposes.
