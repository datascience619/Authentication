import tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
import os
import cv2
from pyfingerprint.pyfingerprint import PyFingerprint
import time


# Match Threshold
SIGNATURE_THRESHOLD = 70
FINGERPRINT_THRESHOLD = 10


def browsefunc(ent):
    filename = askopenfilename(filetypes=([
        ("image", ".jpeg"),
        ("image", ".png"),
        ("image", ".jpg"),
    ]))
    ent.delete(0, tk.END)
    ent.insert(tk.END, filename)

def preprocess_fingerprint(image_path):
    """
    Preprocess a fingerprint image: grayscale conversion, Gaussian blur, and adaptive thresholding.
    """
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise FileNotFoundError("Invalid file path or image not found.")

    # Apply Gaussian Blur
    blurred = cv2.GaussianBlur(img, (5, 5), 0)

    # Adaptive Thresholding
    thresholded = cv2.adaptiveThreshold(
        blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
    )
    return thresholded

def match_images(path1, path2, mode="signature"):
    """
    Compare two images (signature or fingerprint) using OpenCV.
    """
    img1 = cv2.imread(path1, cv2.IMREAD_GRAYSCALE)
    img2 = cv2.imread(path2, cv2.IMREAD_GRAYSCALE)

    if img1 is None or img2 is None:
        raise FileNotFoundError("One of the image paths is invalid or the file does not exist.")

    if mode == "fingerprint":
        img1 = preprocess_fingerprint(path1)
        img2 = preprocess_fingerprint(path2)

    # Initialize ORB detector
    orb = cv2.ORB_create()

    # Detect keypoints and descriptors
    kp1, des1 = orb.detectAndCompute(img1, None)
    kp2, des2 = orb.detectAndCompute(img2, None)

    # Create BFMatcher and find matches
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf.match(des1, des2)

    # Sort matches by distance
    matches = sorted(matches, key=lambda x: x.distance)

    # Calculate similarity score
    similarity_score = (1 - len(matches) / max(len(kp1), len(kp2))) * 100

    return round(similarity_score, 2)


def checkSimilarity(window, path1, path2, mode="signature"):
    try:
        # Check if the images are identical
        if open(path1, "rb").read() == open(path2, "rb").read():
            messagebox.showinfo("Success: Images Match", "Images are 100% identical")
            return True

        # Determine the threshold based on mode
        threshold = SIGNATURE_THRESHOLD if mode == "signature" else FINGERPRINT_THRESHOLD

        # Perform the similarity comparison
        result = match_images(path1, path2, mode)

        # Show the result based on the threshold
        if result <= threshold:
            messagebox.showerror(
                f"Failure: {mode.capitalize()}s Do Not Match",
                f"{mode.capitalize()}s are {result}% similar!"
            )
        else:
            messagebox.showinfo(
                f"Success: {mode.capitalize()}s Match",
                f"{mode.capitalize()}s are {result}% similar!"
            )
    except FileNotFoundError as e:
        messagebox.showerror("Error", str(e))
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

    return True


def set_mode(new_mode):
    global mode
    mode = new_mode
    mode_label.config(text=f"Mode: {mode.capitalize()}")
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os


def set_mode(new_mode):
    global mode
    mode = new_mode
    mode_label.config(text=f"Mode: {mode.capitalize()}")


# Create the main window
root = tk.Tk()
root.title("Image Matching (Signature & Fingerprint)")
root.geometry("600x500")
root.configure(bg="#f5f5f5")

# Header Section
header_frame = tk.Frame(root, bg="#3b5998", height=80)
header_frame.pack(fill="x")

header_label = tk.Label(
    header_frame, text=" Fingerprint And Signature Recognition", font=("Helvetica", 20, "bold"), fg="white", bg="#3b5998"
)
header_label.pack(pady=20)

# Mode Selection Section
mode_frame = tk.Frame(root, bg="#f5f5f5")
mode_frame.pack(pady=20)

mode = "signature"  # Default mode
mode_label = tk.Label(
    mode_frame, text=f"Mode: {mode.capitalize()}", font=("Helvetica", 14), bg="#f5f5f5"
)
mode_label.grid(row=0, column=0, padx=10)

switch_to_signature = ttk.Button(
    mode_frame, text="Signature Mode", command=lambda: set_mode("signature")
)
switch_to_signature.grid(row=0, column=1, padx=10)

switch_to_fingerprint = ttk.Button(
    mode_frame, text="Fingerprint Mode", command=lambda: set_mode("fingerprint")
)
switch_to_fingerprint.grid(row=0, column=2, padx=10)

# Image Input Section
input_frame = tk.Frame(root, bg="#f5f5f5")
input_frame.pack(pady=20)

# Image 1
img1_label = tk.Label(input_frame, text="Image 1:", font=("Helvetica", 12), bg="#f5f5f5")
img1_label.grid(row=0, column=0, pady=10, sticky="e")

image1_path_entry = ttk.Entry(input_frame, width=40)
image1_path_entry.grid(row=0, column=1, padx=10)

img1_browse_button = ttk.Button(
    input_frame, text="Browse", command=lambda: browsefunc(ent=image1_path_entry)
)
img1_browse_button.grid(row=0, column=2, padx=10)

# Image 2
img2_label = tk.Label(input_frame, text="Image 2:", font=("Helvetica", 12), bg="#f5f5f5")
img2_label.grid(row=1, column=0, pady=10, sticky="e")

image2_path_entry = ttk.Entry(input_frame, width=40)
image2_path_entry.grid(row=1, column=1, padx=10)

img2_browse_button = ttk.Button(
    input_frame, text="Browse", command=lambda: browsefunc(ent=image2_path_entry)
)
img2_browse_button.grid(row=1, column=2, padx=10)

# Compare Button
compare_button = ttk.Button(
    root, text="Compare Images", command=lambda: checkSimilarity(
        window=root, path1=image1_path_entry.get(), path2=image2_path_entry.get(), mode=mode
    )
)
compare_button.pack(pady=30)

# Footer Section
footer_label = tk.Label(
    root, text="Developed by Shankar", font=("Helvetica", 10), bg="#f5f5f5", fg="#888"
)
footer_label.pack(side="bottom", pady=10)

# Styling
style = ttk.Style()
style.configure("TButton", font=("Helvetica", 10), padding=5)
style.configure("TLabel", font=("Helvetica", 12))

# Run the main loop
root.mainloop()