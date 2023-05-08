from data import sheets_arrays
from data import csv_
import requests

params = {
    'lat': 39.2,
    'lon': -119.9
}
requesting = ['point', 'neighbors', 'temps', 'intensities']

if 'point' in requesting:
    response = requests.get(url=f'https://nwsgridpointsnew-production.up.railway.app/point', params=params)
    point_forecast = response.json()
    csv_.input_point_forecast(point_forecast)
    sheets_arrays.input_point_forecast()
if 'neighbors' in requesting:
    response = requests.get(url=f'https://nwsgridpointsnew-production.up.railway.app/neighbors', params=params)
    neighbors = response.json()
    csv_.input_neighbors(neighbors)
    sheets_arrays.input_neighbors()
if 'temps' in requesting:
    response = requests.get(url=f'https://nwsgridpointsnew-production.up.railway.app/temps', params=params)
    temp_arrays = response.json()
    csv_.input_temp_conds(temp_arrays)
    sheets_arrays.input_temp_conds()
if 'intensities' in requesting:
    response = requests.get(url=f'https://nwsgridpointsnew-production.up.railway.app/intensities', params=params)
    intensity_arrays = response.json()
    csv_.input_intensities(intensity_arrays)
    sheets_arrays.input_intensities()
