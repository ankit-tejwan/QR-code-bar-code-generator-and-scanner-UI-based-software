# run CMD or Terminal to install required module 
# pip install pyqrcode 
# pip install pillow
import pyqrcode
from PIL import Image

# inputData which represents the input information 
inputData = str(input("copy paste your information  here-->>"))

# Generate QR code with saved info as in above variable name qrcode 
qrcode= pyqrcode.create(inputData) 

# Create and save the png file naming "QRcode.png" 
qrcode.png('QRcode.png', scale = 6)

# Display the QRcode.png using PIL image
img = Image.open('QRcode.png')
img.show()

