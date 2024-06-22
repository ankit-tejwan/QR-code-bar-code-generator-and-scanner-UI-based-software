import customtkinter as ctk
from tkinter import StringVar, messagebox
import pyqrcode
from PIL import Image, ImageTk
import barcode
from barcode.writer import ImageWriter
import datetime
import os

# Create the main application window
app = ctk.CTk()
app.title("Code Generator")
app.geometry("500x600")

# Function to generate and display QR code or Barcode
def generate_code():
    try:
        # Get the text input
        input_text = text_input.get()

        # Get the selected mode (QR code or Barcode)
        mode = selection_mode.get()

        # Generate a unique filename based on date and time
        current_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        
        if mode == "QR Code":
            # Generate QR code
            qr = pyqrcode.create(input_text)
            filename = f"qrcode_{current_time}.png"
            qr_folder = os.path.join(os.getcwd(), "qrCodedata")
            
            if not os.path.exists(qr_folder):
                os.makedirs(qr_folder)
            
            filepath = os.path.join(qr_folder, filename)
            qr.png(filepath, scale=10)

            # Add border to QR code
            img = Image.open(filepath)
            border_size = 10
            bordered_img = Image.new("RGB", (img.size[0] + 2*border_size, img.size[1] + 2*border_size), "white")
            bordered_img.paste(img, (border_size, border_size))
            bordered_img.save(filepath)
            
            # Open and display the image
            img = Image.open(filepath)
            img = img.convert("RGB")
            img = img.resize((200, 200), Image.LANCZOS)
            code_img = ImageTk.PhotoImage(img)
            display_label.configure(image=code_img)
            display_label.image = code_img

        elif mode == "Barcode":
            # Generate Barcode
            barcode_class = barcode.get_barcode_class('code128')
            barcode_obj = barcode_class(input_text, writer=ImageWriter())
            filename = f"barcode_{current_time}"  # Omit the .png extension
            barcode_folder = os.path.join(os.getcwd(), "barcodeData")
            
            if not os.path.exists(barcode_folder):
                os.makedirs(barcode_folder)
            
            filepath = os.path.join(barcode_folder, filename)

            barcode_obj.save(filepath, options={"module_width": 0.2, "module_height": 15.0, "font_size": 10, "text_distance": 10.0, "write_text": False})

            # Append the correct extension for the filepath check
            filepath_with_extension = f"{filepath}.png"

            # Check if the file exists
            if os.path.exists(filepath_with_extension):
                print("Barcode image generated successfully.")
                
                # Open and display the image
                img = Image.open(filepath_with_extension)
                img = img.convert("RGB")
                img = img.resize((200, 200), Image.LANCZOS)
                code_img = ImageTk.PhotoImage(img)
                display_label.configure(image=code_img)
                display_label.image = code_img
            else:
                raise FileNotFoundError("Barcode image not found after generation.")
                
    except Exception as e:
        print(f"Error: {e}")
        messagebox.showerror("Error", f"Error generating code: {e}")

# Function to clear the text entry
def clear_text():
    text_input.set("")

def on_exit():
    if messagebox.askyesno("Exit Confirmation", "Are you sure you want to exit?"):
        app.quit()

# Create a frame for input and button
input_frame = ctk.CTkFrame(app)
input_frame.pack(pady=20)

text_input = StringVar()
text_entry = ctk.CTkEntry(input_frame, textvariable=text_input, width=300, height=40, font=("Helvetica", 20))
text_entry.grid(row=0, column=0, padx=10, pady=5)

# Create an option menu for selection mode
selection_mode = StringVar(value="QR Code")
mode_options = ctk.CTkOptionMenu(input_frame, values=["QR Code", "Barcode"], variable=selection_mode)
mode_options.grid(row=0, column=1, padx=10, pady=5)

# Create a button to generate QR code or Barcode
generate_button = ctk.CTkButton(input_frame, text="Generate", command=generate_code, hover_color="green")
generate_button.grid(row=1, column=0, padx=10, pady=5)

# Create a button to clear the text entry
clear_button = ctk.CTkButton(input_frame, text="Clear", command=clear_text, hover_color="red")
clear_button.grid(row=1, column=1, padx=10, pady=5)

# Create a frame for displaying QR code or Barcode
display_frame = ctk.CTkFrame(app, width=220, height=220, border_width=2, border_color="green")
display_frame.pack(pady=20)

# Create a label to display the QR code or Barcode
display_label = ctk.CTkLabel(display_frame, text="")  # Initialize without default text
display_label.pack(expand=True)

# Create and place the 'Exit' button
exit_button = ctk.CTkButton(master=app, text="Exit", hover_color="red", command=on_exit)
exit_button.place(relx=0.83, rely=0.9, anchor=ctk.CENTER)

# Start the main event loop
app.mainloop()
