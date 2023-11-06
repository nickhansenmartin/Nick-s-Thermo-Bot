import urequests as requests
import ujson

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
}

try:
    # Make a get request to the API
    response = requests.get(url, headers=headers)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON response
        record_data = ujson.loads(response.text)
        color_val = record_data['fields']['unit']
        print(color_val)

except Exception as e:
    print(f'Error: {e}')

