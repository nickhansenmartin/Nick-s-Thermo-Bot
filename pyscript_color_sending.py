# NOTE: This code should not be run on its own. This just saves the code for use with the OpenCV websiteimport cv2
import cv2
import numpy as np
import requests

# Convert the camera input to BGR color space
cv2_image = cv2.cvtColor(np.array(cam.raw_image), cv2.COLOR_RGB2BGR)

# Split the image into its color channels
b, g, r = cv2.split(cv2_image)

# Calculate the average intensity of each channel
avg_b = np.mean(b)
avg_r = np.mean(r)

# Determine the predominant color
predominant_color = "Blue" if avg_b > avg_r else "Red"

# Display the result
textBox.innerText = f"Predominant color: {predominant_color}"

# Replace with your Airtable API key, base ID, table name, and record ID
API_KEY = ''
BASE_ID = 'appo4v9qUBWpJUbl2'
TABLE_ID = 'tblyvGSPiqA2AINcY'
RECORD_ID = 'rec7ODEleus0mmgRQ'

# Define the URL for the Airtable API
url = f'https://api.airtable.com/v0/{BASE_ID}/{TABLE_ID}/{RECORD_ID}'

# Define your request headers
headers = {
    'Authorization': f'Bearer {API_KEY}',
    'Content-Type': 'application/json',
}

# Define the data you want to update in the record
data = {
    'fields': {
        'unit': str(predominant_color),  # Update with the color detected
    }
}

# Send a PATCH request to update the record
response = requests.patch(url, headers=headers, json=data)

