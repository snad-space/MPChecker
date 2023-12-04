import pandas as pd
import astropy.units as u
import requests

from astropy.table import Table, vstack, Column
from astroquery.imcce import Skybot
from astropy.coordinates import SkyCoord, EarthLocation
from astropy.time import Time

PALOMAR = EarthLocation(lon=-116.863, lat=33.356, height=1706)  # EarthLocation.of_site('Palomar')

def hmjd_to_earth(hmjd, coord):
    t = Time(hmjd, format="mjd")
    return t - t.light_travel_time(coord, kind="heliocentric", location=PALOMAR)

oid = input("Enter OID: ")

url = 'http://db.ztf.snad.space/api/v3/data/latest/oid/full/json?oid=' + oid

response = requests.get(url)
data = response.json()

RA = data[oid]['meta']['coord']['ra']
Dec = data[oid]['meta']['coord']['dec']

field = SkyCoord(RA*u.deg, Dec*u.deg)

# Prompt user to input HMJDs manually
user_hmjds_input = input("Enter the HMJDs separated by commas: ")

try:
    user_hmjds = [float(hmjd.strip()) for hmjd in user_hmjds_input.split(",")]
except ValueError:
    print("Invalid input. Please enter valid HMJDs.")
    exit()

# Define columns to print
columns_names = ['Number', 'Name', 'RA', 'DEC', 'V', 'centerdist', 'RA_rate', 'DEC_rate', 'heliodist', 'epoch']
units = [' ', ' ', 'deg', 'deg', 'mag', 'arcsec', 'arcsec/h', 'arcsec/h', 'AU', 'd']


for hmjd in user_hmjds:
    try:
        earthed_time = hmjd_to_earth(hmjd, field)
        results = Skybot.cone_search(field, 10 * u.arcmin, earthed_time, location='I41')

        print(f"For HMJD={hmjd}, objects found:")
        results[columns_names].pprint(max_width=150)

    except:
        continue
