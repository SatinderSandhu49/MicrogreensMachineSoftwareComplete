import sys
import time
import datetime

import board
import adafruit_dht
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Type of sensor, can be `adafruit_dht.DHT11` or `adafruit_dht.DHT22`.
# For the AM2302, use the `adafruit_dht.DHT22` class.
DHT_TYPE = adafruit_dht.DHT11

# Example of sensor connected to Raspberry Pi Pin 23
DHT_PIN  = board.D4
# Example of sensor connected to Beaglebone Black Pin P8_11
# DHT_PIN  = 'P8_11'

# Initialize the dht device, with data pin connected to:
dhtDevice = DHT_TYPE(DHT_PIN, use_pulseio=False)

# Google Docs OAuth credential JSON file.  Note that the process for authenticating
# with Google docs has changed as of ~April 2015.  You _must_ use OAuth2 to log
# in and authenticate with the gspread library.  Unfortunately this process is much
# more complicated than the old process.  You _must_ carefully follow the steps on
# this page to create a new OAuth service in your Google developer console:
#   http://gspread.readthedocs.org/en/latest/oauth2.html
#
# Once you've followed the steps above you should have downloaded a .json file with
# your OAuth2 credentials.  This file has a name like SpreadsheetData-<gibberish>.json.
# Place that file in the same directory as this python script.
#
# Now one last _very important_ step before updating the spreadsheet will work.
# Go to your spreadsheet in Google Spreadsheet and share it to the email address
# inside the 'client_email' setting in the SpreadsheetData-*.json file.  For example
# if the client_email setting inside the .json file has an email address like:
#   [email protected]account.com
# Then use the File -> Share... command in the spreadsheet to share it with read
# and write acess to the email address above.  If you don't do this step then the
# updates to the sheet will fail!
GDOCS_OAUTH_JSON       = 'microgreensmachine-984d935f3ec9.json'

# Google Docs spreadsheet name.
GDOCS_SPREADSHEET_NAME = 'microgreens'

# How long to wait (in seconds) between measurements.
FREQUENCY_SECONDS      = 5


def login_open_sheet(oauth_key_file, spreadsheet):
    """Connect to Google Docs spreadsheet and return the first worksheet."""
    try:
        scope =  ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        credentials = ServiceAccountCredentials.from_json_keyfile_name(oauth_key_file, scope)
        gc = gspread.authorize(credentials)
        worksheet = gc.open(spreadsheet).sheet1 # pylint: disable=redefined-outer-name
        return worksheet
    except Exception as ex: # pylint: disable=bare-except, broad-except
        print('Unable to login and get spreadsheet.  Check OAuth credentials, spreadsheet name, \
        and make sure spreadsheet is shared to the client_email address in the OAuth .json file!')
        print('Google sheet login failed with error:', ex)
        sys.exit(1)


print('Logging sensor measurements to\
 {0} every {1} seconds.'.format(GDOCS_SPREADSHEET_NAME, FREQUENCY_SECONDS))
print('Press Ctrl-C to quit.')
worksheet = None
while True:
    try:
    # Login if necessary.
        if worksheet is None:
            worksheet = login_open_sheet(GDOCS_OAUTH_JSON, GDOCS_SPREADSHEET_NAME)

        # Attempt to get sensor reading.
        temp = dhtDevice.temperature
        humidity = dhtDevice.humidity
        test = 1

        # Skip to the next reading if a valid measurement couldn't be taken.
        # This might happen if the CPU is under a lot of load and the sensor
        # can't be reliably read (timing is critical to read the sensor).
        if humidity is None or temp is None:
            time.sleep(2)
            continue

        print('Temperature: {0:0.1f} C'.format(temp))
        print('Humidity:    {0:0.1f} %'.format(humidity))

        # Append the data in the spreadsheet, including a timestamp
    
        worksheet.append_row((datetime.datetime.now().isoformat(), temp, humidity, test))
    except: # pylint: disable=bare-except, broad-except
        # Error appending data, most likely because credentials are stale.
        # Null out the worksheet so a login is performed at the top of the loop.
        print('Append error, logging in again')
        worksheet = None
        time.sleep(FREQUENCY_SECONDS)
        continue

    # Wait 30 seconds before continuing
    print('Wrote a row to {0}'.format(GDOCS_SPREADSHEET_NAME))
    time.sleep(FREQUENCY_SECONDS)