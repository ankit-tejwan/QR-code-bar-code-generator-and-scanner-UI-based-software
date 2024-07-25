############################################################################################################
# This script Scan  the qr bar code both having Encryption  with SHA 256 bit
############################################################################################################

import customtkinter as ctk
from tkinter import StringVar, messagebox, filedialog
import pyzbar.pyzbar as pyzbar
import cv2
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
import base64


# Create the main application window
app = ctk.CTk()
app.title("QR/Barcode Scanner")
app.geometry("500x500")

# Function to scan QR code or barcode from an image
def scan_code():
    # Open a file dialog to select the image file
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])

    if not file_path:
        return

    # Load the image
    img = cv2.imread(file_path)
    decoded_objects = pyzbar.decode(img)

    # Check if any QR code or barcode is detected
    if not decoded_objects:
        messagebox.showerror("Error", "No QR code or barcode detected!")
        return

    # Process each detected object
    for obj in decoded_objects:
        scan_result = obj.data.decode("utf-8")
        
        # Check if the detected code matches the selected scan mode
        if scan_mode.get() == "QR Code" and obj.type == "QRCODE":
            display_result(scan_result)
            return
        elif scan_mode.get() == "Barcode" and obj.type != "QRCODE":
            display_result(scan_result)
            return

    # If no matching code type is found
    messagebox.showerror("Error", "No matching QR code or barcode detected!")

# Function to display the scan result
def display_result(scan_result):
    # Decrypt the encrypted result  from the QR Code or Barcode data
    encrypted_result = scan_result
    
    # Function to generate a key and IV
    def generate_key_iv(password, salt):
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        key = kdf.derive(password)
        return key

    # Decryption function
    def decrypt(encrypted_message, password):
        encrypted_message_bytes = base64.b64decode(encrypted_message)
        salt = encrypted_message_bytes[:16]
        iv = encrypted_message_bytes[16:32]
        encrypted_message = encrypted_message_bytes[32:]
        key = generate_key_iv(password, salt)
        cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        decrypted_message = decryptor.update(encrypted_message) + decryptor.finalize()
        return decrypted_message.decode('utf-8')

    password = b'my_very_secure_password'
    encrypted_string = encrypted_result
    #print("data from qr and bar code ",encrypted_string)

    # Decrypt the encrypted string
    decrypted_string = decrypt(encrypted_string, password)
    #print(f"Decrypted: {decrypted_string}")

    
    display_label.configure(text=decrypted_string)
    #print("Scan result: " + str(scan_result))

# Function to clear the displayed text
def clear_display():
    display_label.configure(text="")

def on_exit():
    if messagebox.askyesno("Exit Confirmation", "Are you sure you want to exit?"):
        app.quit()

# Function to update the button text based on the scan mode
def update_button_text(*args):
    if scan_mode.get() == "QR Code":
        scan_button.configure(text="Upload QR Code")
    else:
        scan_button.configure(text="Upload Barcode")

# Create a frame for the scan mode selection
mode_frame = ctk.CTkFrame(app)
mode_frame.pack(pady=20)

scan_mode = StringVar(value="QR Code")
scan_mode.trace("w", update_button_text)

qr_radio = ctk.CTkRadioButton(mode_frame, text="Scan QR Code", variable=scan_mode, value="QR Code")
qr_radio.grid(row=0, column=0, padx=10, pady=5)
barcode_radio = ctk.CTkRadioButton(mode_frame, text="Scan Barcode", variable=scan_mode, value="Barcode")
barcode_radio.grid(row=0, column=1, padx=10, pady=5)

# Create a button to scan QR code or barcode
scan_button = ctk.CTkButton(app, text="Upload QR Code", command=scan_code, hover_color="green")
scan_button.pack(pady=10)

# Create a frame for displaying the scan result
display_frame = ctk.CTkFrame(app, width=220, height=220, border_width=2, border_color="green")
display_frame.pack(pady=20)

# Create a label to display the scan result
display_label = ctk.CTkLabel(display_frame, text="")  # Initialize without default text
display_label.pack(expand=True)

# Create and place the 'Exit' button
exit_button = ctk.CTkButton(master=app, text="Exit", hover_color="red", command=on_exit)
exit_button.place(relx=0.83, rely=0.9, anchor=ctk.CENTER)

# handle direct window close button press
app.protocol("WM_DELETE_WINDOW", on_exit)  # X button click event handler

# Start the main event loop
app.mainloop()