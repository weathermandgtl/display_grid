import gspread
import csv
import ast

service_account = gspread.service_account('data/~service-account.json')
point_forecast_csv = "forecasts/point_forecast.csv"
neighbors_csv = "forecasts/!neighbors.csv"
temp_cond_csv = "forecasts/temp_cond_forecast.csv"
intensity_csv = "forecasts/intensity_forecast.csv"

sheet = service_account.open("Arrays")

def abbreviate_condition(cond):
    abbr = cond
    abbr = 'S' if cond == 'snow' else abbr
    abbr = 'R' if cond == 'rain' else abbr
    abbr = 'FR' if cond == 'freezing rain' else abbr
    abbr = 'RS' if cond == 'rain/snow' else abbr
    abbr = 'SSL' if cond == 'snow/sleet' else abbr
    abbr = 'RSL' if cond == 'rain/sleet' else abbr
    abbr = 'SL' if cond == 'sleet' else abbr
    abbr = 'WM' if cond == 'mixed' else abbr
    abbr = 'N' if cond is None or cond == 'None' else abbr
    return abbr

def input_neighbors():
    input_(sheet_name='NEIGHBOR_CONDS',
           csv_name=neighbors_csv,
           omit=[],
           param='weather')
    input_(sheet_name='NEIGHBOR_PRECIP',
           csv_name=neighbors_csv,
           omit=[],
           param='precip')
    input_(sheet_name='NEIGHBOR_TEMPS',
           csv_name=neighbors_csv,
           omit=[],
           param='temperature')
    worksheet = sheet.worksheet("NEIGHBOR_LATLONS")
    with open(neighbors_csv, "r") as file:
        reader = csv.reader(file)
        values = []
        for r in reader:
            if r[0] in ['hour', 'validTimeUTC']:
                continue
            v = [ast.literal_eval(r[1])['lat_lon']]
            values.append(v)
    worksheet.update("A3:A30", values)

def input_temp_conds():
    input_(sheet_name='CONDITIONS',
           csv_name=temp_cond_csv,
           omit=[],
           param='weather')
    input_(sheet_name='TEMPERATURES',
           csv_name=temp_cond_csv,
           omit=[],
           param='temperature')

def input_intensities():
    input_(sheet_name='PRECIPS',
           csv_name=intensity_csv,
           omit=['allAfterCut', 'point', 'nearest', 'absMinimum', 'absMaximum',
                 'rangeMinimim', 'rangeMaximum', 'rawPrecipRange', 'precipSlices'],
           param='precip')

def input_(sheet_name, csv_name, omit, param):
    worksheet = sheet.worksheet(sheet_name)
    worksheet.clear()
    with open(csv_name, "r") as file:
        reader = csv.reader(file)
        rows = []
        for r in reader:
            if r[0] in omit:
                continue
            elif r[0] == 'hour':
                pass
            elif r[0] == 'validTimeUTC':
                r = [r[0]] + [c.split('T')[1] for c in r[1:]]
            elif param == 'weather':
                r = [r[0]] + [ast.literal_eval(c)[param] for c in r[1:]]
                r = [abbreviate_condition(v) for v in r]
            else:
                r = [r[0]] + [ast.literal_eval(c)[param] for c in r[1:]]
            for i, v in enumerate(r):
                if v is None:
                    r[i] = 'None'
            rows.append(r)
        worksheet.update(rows)

def input_point_forecast():
    point_worksheet = sheet.worksheet('POINT')
    point_worksheet.clear()
    with open(point_forecast_csv, "r") as file:
        reader = csv.reader(file)
        rows = []
        omit = ['conditionString', 'windDirection', 'windSpeed',
                'windGust', 'apparentTemperature', 'validTimeLocal', 'windSpeed',
                'lat/lon', 'weatherCode', 'irradiance', 'solar']
        for r in reader:
            if r[0] in omit:
                r = None
            elif r[0] == 'hour':
                pass
            elif r[0] == 'validTimeUTC':
                r = [r[0]] + [v.split('T')[1] for v in r[1:]]
            elif r[0] == 'weather':
                r = [r[0]] + [abbreviate_condition(v) for v in r[1:]]
            elif r[0] == 'precip':
                r = [r[0]] + [round(ast.literal_eval(v), 3) for v in r[1:]]
            elif r[0] == 'solar':
                r = [r[0]] + [round(ast.literal_eval(v['altitude']), 3) for v in r[1:]]
            else:
                r = [r[0]] + [(round(ast.literal_eval(v), 0)
                               if isinstance(ast.literal_eval(v), float)
                               else ast.literal_eval(v)) for v in r[1:]]
            rows.append(r)
        print(rows)
        point_worksheet.update(rows)

# input_point_forecast()
# input_neighbors()
# input_temp_conds()
# input_intensities()
