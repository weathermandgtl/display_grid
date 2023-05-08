from functions import weather
import gspread
import csv
import ast

INTENSITY = '0'
TEMP = '+3'

service_account = gspread.service_account(f'data/~service-account.json')
point_csv = "forecasts/point_forecast.csv"
temp_cond_csv = "forecasts/temp_cond_forecast.csv"
intensity_csv = "forecasts/intensity_forecast.csv"

sheet = service_account.open("Mapout3.0")
worksheet = sheet.worksheet("SCENARIO")

with open(point_csv, "r") as point_file:
    point_reader = csv.reader(point_file)
    for r in point_reader:
        if r[0] == 'lat/lon':
            lat_lon = f"{r[1]}, {r[2]}"
        elif r[0] == 'validTimeUTC':
            time_row = [r[0]] + [c.split('T')[1].split(':')[0] for c in r[1:]]
        elif r[0] == "solarAngle":
            solar_row = ['sun angle (deg)'] + [round(float(c), 1) for c in r[1:]]
        elif r[0] == "skyCover":
            cloud_row = ['cloud %'] + [int(c) for c in r[1:]]

with open(temp_cond_csv, "r") as temp_cond_file, open(intensity_csv, "r") as intensity_file:
    temp_cond_reader = csv.reader(temp_cond_file)
    intensity_reader = csv.reader(intensity_file)
    for r in temp_cond_reader:
        if r[0] == TEMP:
            temp_row = ['temp ' + r[0]] + [ast.literal_eval(c)['tempF'] for c in r[1:]]
            cond_row = ['cond '+r[0]] + [ast.literal_eval(c)['weather'] for c in r[1:]]
            cond_row = [weather.abbreviate_condition(v) for v in cond_row]
    for r in intensity_reader:
        if r[0] == INTENSITY:
            precip_row = ['precip in/hr '+r[0]] + [ast.literal_eval(c)['precipIN'] for c in r[1:]]

snow_row = ['snow in/hr']
sleet_row = ['sleet in/hr']
rain_row = ['rain in/hr']
for i in range(1, len(temp_row)):
    snow_row.append(0)
    rain_row.append(0)
    sleet_row.append(0)
    cond_row[i] = None if precip_row[i] == 0 else cond_row[i]
    if cond_row[i] == 'S':
        snow_row[-1] = precip_row[i] * 10
    elif cond_row[i] in ['R', 'FR']:
        rain_row[-1] = precip_row[i]
    elif cond_row[i] == 'RS':
        snow_row[-1] = float(precip_row[i]) * 10 / 2
        rain_row[-1] = float(precip_row[i]) / 2
    elif cond_row[i] == 'RSL':
        sleet_row[-1] = float(precip_row[i]) / 2
        rain_row[-1] = float(precip_row[i]) / 2
    elif cond_row[i] == 'SSL':
        snow_row[-1] = float(precip_row[i]) * 10 / 2
        sleet_row[-1] = float(precip_row[i]) / 2
    elif cond_row[i] == 'SL':
        sleet_row[-1] = precip_row[i]
    elif cond_row[i] == 'WM':
        snow_row[-1] = float(precip_row[i]) * 10 / 3
        rain_row[-1] = float(precip_row[i]) / 3
        sleet_row[-1] = float(precip_row[i]) / 3


empty_row = [[''] * 38]
for row in [5, 29, 7, 9, 10, 11, 12, 13, 14]:
    worksheet.update(f"A{row}:AL{row}", empty_row)

hours = 38
worksheet.update("A1", lat_lon)
worksheet.update("A5:AL5", [time_row[:hours]])
worksheet.update("A31:AL31", [solar_row[:hours]])
worksheet.update("A7:AL7", [cloud_row[:hours]])
worksheet.update("A9:AL9", [cond_row[:hours]])
worksheet.update("A10:AL10", [temp_row[:hours]])
worksheet.update("A11:AL11", [precip_row[:hours]])
worksheet.update("A12:AL12", [snow_row[:hours]])
worksheet.update("A13:AL13", [sleet_row[:hours]])
worksheet.update("A14:AL14", [rain_row[:hours]])




