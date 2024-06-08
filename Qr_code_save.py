import customtkinter as ctk
from tkinter import StringVar , messagebox
import pyqrcode
from PIL import Image, ImageTk


# Create the main application window
app = ctk.CTk()
app.title("QR Code Generator")
app.geometry("500x500")

# Function to generate and display QR code
def generate_qr():
    # Get the text input
    input_text = text_input.get()

    # Generate QR code
    qr = pyqrcode.create(input_text)

    # Save the QR code as an image file
    qr.png('qrcode.png', scale=10)

    # Open the image file
    img = Image.open('qrcode.png')
    img = img.convert("RGB")

    # Resize the image to fit the display window
    img = img.resize((200, 200), Image.Resampling.LANCZOS)
    
    # Add a colored border to the image
    border_color = (0, 128, 0)  # Green color
    bordered_img = Image.new("RGB", (img.size[0] + 20, img.size[1] + 20), border_color)
    bordered_img.paste(img, (10, 10))

    # Convert the Image to a format tkinter can use
    qr_img = ImageTk.PhotoImage(bordered_img)

    # Display the image in the display_label
    display_label.configure(image=qr_img)
    display_label.image = qr_img

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


# Create a button to generate QR code
generate_button = ctk.CTkButton(input_frame, text="Generate QR Code", command=generate_qr, hover_color="green")
generate_button.grid(row=0, column=1, padx=10, pady=5)

# Create a button to clear the text entry
clear_button = ctk.CTkButton(input_frame, text="Clear", command=clear_text, hover_color="red")
clear_button.grid(row=1, column=1, padx=10, pady=5)

# Create a frame for displaying QR code
display_frame = ctk.CTkFrame(app, width=220, height=220, border_width=2, border_color="green")
display_frame.pack(pady=20)

# Create a label to display the QR code
display_label = ctk.CTkLabel(display_frame, text="")  # Initialize without default text
display_label.pack(expand=True)
# Create and place the 'Exit' button
exit_button = ctk.CTkButton(master=app, text="Exit", hover_color="red", command=on_exit)
exit_button.place(relx=0.9, rely=0.9, anchor=ctk.CENTER)
# Start the main event loop
app.mainloop()

