import tkinter as tk
from tkinter import filedialog
import os
import pywhatkit
import time
import pandas as pd

def extractPhoneNumbers(csvFile, columnName):
    try:
        df = pd.read_csv(csvFile)

        phones = df[str(columnName)].astype(str).str.extractall(r'(\d{10})').astype(str).reset_index()[0]
        phones = phones.tolist()
        return ["+57" + number for number in phones]

    except Exception as e:
        return f"Error: {str(e)}"

def sendWhatsAppMessage():
    message = messageEntry.get()

    if not message:
        statusLabel.config(text="Enter a message")
        return

    phoneNumbers = extractPhoneNumbers(csvFile, columnName)
    waitTime = 7
    closeTab = True
    closeTime = 8

    for contact in phoneNumbers:
        pywhatkit.sendwhats_image(contact, selectedImagePath, message, waitTime, closeTab, closeTime)
        time.sleep(1)

    statusLabel.config(text="Messages sent successfully")

def browseImage():
    global selectedImagePath
    selectedImagePath = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select image", filetypes=(("Image files", "*.png;*.jpg;*.jpeg"), ("All files", "*.*")))
    photoNameLabel.config(text=f"Photo Name: {os.path.basename(selectedImagePath)}")

def updateColumnName():
    global columnName
    columnName = columnEntry.get()
    headerLabel.config(text=f"Header: {columnName}")

def selectCsvFile():
    global csvFile
    csvFile = filedialog.askopenfilename(filetypes=[('CSV files', '*.csv')],
                                         title='Select CSV file')
    fileLabel.config(text=f"File Name: {os.path.basename(csvFile)}")

root = tk.Tk()
root.title("WhatsApp Message Sending")

messageLabel = tk.Label(root, text="Message:")
messageLabel.pack(pady=5)

messageEntry = tk.Entry(root, width=30, font=("arial",14))
messageEntry.pack(pady=10)

columnLabel = tk.Label(root, text="Column Name:")
columnLabel.pack(pady=5)

columnEntry = tk.Entry(root, width=20)
columnEntry.pack(pady=10)

updateColumnButton = tk.Button(root, text="Update Column", command=updateColumnName, width=20)
updateColumnButton.pack(pady=10)

csvButton = tk.Button(root, text="Select CSV File", command=selectCsvFile, width=20)
csvButton.pack(pady=10)

imageButton = tk.Button(root, text="Select Image", command=browseImage, width=20)
imageButton.pack(pady=10)

sendButton = tk.Button(root, text="Send Message", command=sendWhatsAppMessage, width=20)
sendButton.pack(pady=20)

statusLabel = tk.Label(root, text="")
statusLabel.pack()

fileLabel = tk.Label(root, text="")
fileLabel.pack()

headerLabel = tk.Label(root, text="")
headerLabel.pack()

photoNameLabel = tk.Label(root, text="")
photoNameLabel.pack()

root.minsize(width=400, height=300)
root.maxsize(width=600, height=500)

root.resizable(width=False, height=False)

root.mainloop()