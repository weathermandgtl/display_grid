import csv

def input_neighbors(neighbors_plus_point):
    meta_row_names = list(neighbors_plus_point['forecast'][0]['meta'].keys())
    data_row_names = list(neighbors_plus_point['forecast'][0]['data'].keys())
    all_data = []
    for param in meta_row_names:
        params = [param]
        for hour in neighbors_plus_point['forecast']:
            params.append(hour['meta'][param])
        all_data.append(params)
    for param in data_row_names:
        for i in range(0, len(neighbors_plus_point['forecast'][0]['data'][param])):
            params = [param] if i == 0 else [i+1]
            for hour in neighbors_plus_point['forecast']:
                params.append(hour['data'][param][i])
            all_data.append(params)
    with open(f"forecasts/!neighbors.csv", "w") as file:
        writer = csv.writer(file)
        for row in all_data:
            writer.writerow(row)

def input_temp_conds(temp_arrays):
    input_(arrays=temp_arrays,
           csv_name="temp_cond_forecast")

def input_intensities(intensity_ranges):
    input_(arrays=intensity_ranges,
           csv_name="intensity_forecast")

def input_(arrays, csv_name):
    meta_row_names = list(arrays['forecast'][0]['meta'].keys())
    data_row_names = list(arrays['forecast'][0]['data'].keys())
    data_row_names.sort(reverse=True)
    all_data = []
    for param in meta_row_names:
        params = [param]
        for hour in arrays['forecast']:
            params.append(hour['meta'][param])
        all_data.append(params)
    for param in data_row_names:
        params = ['+' + str(param) if int(param) > 0 else param]
        for hour in arrays['forecast']:
            params.append(hour['data'][param])
        all_data.append(params)
    with open(f"forecasts/{csv_name}.csv", "w") as file:
        writer = csv.writer(file)
        for row in all_data:
            writer.writerow(row)

def input_point_forecast(forecast):
    row_names = list(forecast['forecast'][0].keys())
    all_data = [['lat/lon', forecast['meta']['lat'], forecast['meta']['lon']]]
    for param in row_names:
        params = [param]
        for hour in forecast['forecast']:
            params.append(hour[param])
        all_data.append(params)
    with open("forecasts/point_forecast.csv", "w") as file:
        writer = csv.writer(file)
        for row in all_data:
            writer.writerow(row)
