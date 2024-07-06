import customtkinter as ctk
from tkinter import StringVar, messagebox, filedialog
import pyzbar.pyzbar as pyzbar
import cv2

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
    display_label.configure(text=scan_result)
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

# Start the main event loop
app.mainloop()
