# Authentication
🖊️ Fingerprint and Signature Recognition System

A Python-based biometric image comparison tool that detects and verifies the similarity between two **fingerprint** or **signature** images using computer vision techniques. Built with **OpenCV** and a user-friendly **Tkinter GUI**, the system supports both extractive matching and adaptive image preprocessing.

 🚀 Features

* 🔍 Compare two images in **Signature** or **Fingerprint** mode
* 📷 ORB-based feature detection for robust matching
* 🧠 Adaptive preprocessing for fingerprint images (Gaussian blur + thresholding)
* 🎛️ Easy mode switching via GUI
* 🖼️ View match score (%) with pass/fail result
* 📤 Supports JPG, JPEG, and PNG image formats
* 🖥️ Clean Tkinter interface with file browser and match report

 🛠️ Tech Stack

Language: Python
Libraries: OpenCV, Tkinter, pyfingerprint (optional hardware integration), NumPy
Techniques: ORB feature detection, BFMatcher, adaptive thresholding

 📂 Use Cases

* Biometric identity verification
* Signature authentication in legal or banking sectors
* Educational demonstrations in computer vision/biometrics

 📸 Screenshots *(optional)*

*Add GUI screenshots showing fingerprint and signature comparison output.*

 🧪 Matching Logic

* Images are first converted to grayscale
* For **fingerprints**, images are additionally blurred and thresholded
* ORB features are extracted and matched using brute-force matcher
* A similarity score is calculated and displayed

