import gspread
import copy

service_account = gspread.service_account('data/~service-account.json')
sheet = service_account.open("Mapout3.0")
scenario_sheet = sheet.worksheet("SCENARIO")
cover_sheet = sheet.worksheet("COVER")

sheet_rows = scenario_sheet.get_all_values()
times = snow_accu = sleet_accu = frzg_accu = total_frzn_accu = rain_accu = total_melt = slr = []
for row in sheet_rows:
    if row[0] == 'validTimeUTC':
        # times = [row[0]] + [datetime.strptime(v, "%H") for v in row[1:]]
        times = row
    elif row[0] == 'snow accu':
        snow_accu = row
    elif row[0] == 'sleet accu':
        sleet_accu = row
    elif row[0] == 'frzg accu':
        frzg_accu = row
    elif row[0] == 'total frzn accu':
        total_frzn_accu = row
    elif row[0] == 'rain accu':
        rain_accu = row
    elif row[0] == 'total melt (in/hr)':
        total_melt = row
    elif row[0] == 'slr':
        slr = row

forecast = []
for i in range(0, len(times)):
    period = {
        "validTimeUTC": times[i],
        "hourSnowAccu": snow_accu[i],
        "hourSleetAccu": sleet_accu[i],
        "hourFrzgAccu": frzg_accu[i],
        "hourFrznAccu": total_frzn_accu[i],
        "hourRainAccu": rain_accu[i],
        "hourMelt": total_melt[i],
        "hourSlr": slr[i]
    }
    forecast.append(period)

all_stacks = [[], [], [{
    "layerSnowAccu": 0,
    "layerSnowSlrAccu": 0,
    "layerSleetAccu": 0,
    "layerFrzgAccu": 0,
    "layerFrznAccu": 0}]]

for i, hour in enumerate(forecast[3:], start=3):
    hour_rain = float(hour['hourRainAccu'])
    hour_sleet = float(hour['hourSleetAccu'])
    hour_frzg = float(hour['hourFrzgAccu'])
    hour_slr = float(hour['hourSlr'])
    hour_melt = -float(hour['hourMelt'])
    if hour_rain or hour_sleet or hour_frzg:   #if mix, cap slr at 10
        hour_slr = 10 if hour_slr > 10 else hour_slr
    hour_accumulations = {
        "layerSnowAccu": float(hour['hourSnowAccu']),
        "layerSnowSlrAccu": float(hour['hourSnowAccu']) * (hour_slr / 10),
        "layerSleetAccu": hour_sleet,
        "layerFrzgAccu": hour_frzg,
        "layerFrznAccu": float(hour['hourFrznAccu']),
        "layerRainAccu": hour_rain,
        "layerSlr": hour_slr,
        "hourMelt": float(hour['hourMelt'])
    }
    previous_stack = copy.deepcopy(all_stacks[-1])
    current_stack = [hour_accumulations] + previous_stack
    for layer in current_stack:
        layer_frzn_accu = layer['layerFrznAccu']
        layer_frzn_accu_remaining = layer_frzn_accu - hour_melt / 10
        if layer_frzn_accu_remaining < 0:
            hour_melt = -layer_frzn_accu_remaining * 10
            layer_frzn_accu_remaining = 0
        else:
            hour_melt = 0
        try:
            prop_remaining = layer_frzn_accu_remaining / layer_frzn_accu
        except ZeroDivisionError:
            prop_remaining = 0
        layer['layerSnowAccu'] *= prop_remaining
        layer["layerSnowSlrAccu"] *= prop_remaining
        layer['layerSleetAccu'] *= prop_remaining
        layer['layerFrzgAccu'] *= prop_remaining
        layer['layerFrznAccu'] = layer_frzn_accu_remaining
        if hour_melt == 0:
            break
    all_stacks.append(current_stack)


snow_cover = ['snow cover']
snow_cover_slr = ['slr snow cover']
sleet_cover = ['sleet cover']
frzg_cover = ['frzg cover']
frzn_cover = ['total frzn']
for stack in all_stacks:
    stack_snow = stack_slr_snow = stack_sleet = stack_frzg = stack_frzn = 0
    for layer in stack:
        stack_snow += round(layer['layerSnowAccu'], 1)
        stack_slr_snow += round(layer['layerSnowSlrAccu'], 1)
        stack_sleet += round(layer['layerSleetAccu'], 2)
        stack_frzg += round(layer['layerFrzgAccu'], 2)
        stack_frzn += round(layer['layerFrznAccu'], 2)
    snow_cover.append(stack_snow)
    snow_cover_slr.append(stack_slr_snow)
    sleet_cover.append(stack_sleet)
    frzg_cover.append(stack_frzg)
    frzn_cover.append(stack_frzn)


cover_sheet.update('A1:AM1', [times])
cover_sheet.update('A2:AM2', [snow_cover])
cover_sheet.update('A3:AM3', [snow_cover_slr])
cover_sheet.update('A4:AM4', [sleet_cover])
cover_sheet.update('A5:AM5', [frzg_cover])
cover_sheet.update('A6:AM6', [frzn_cover])


# Stacking graphic code below






















# max_length = len(all_stacks[-1])
# stacks_horizontal = []
# for stack in all_stacks:
#     formatted_stack = [0 for i in range(max_length - len(stack))]
#     for layer in stack:
#         formatted_stack.append(round(layer['layerFrznAccu'], 3))
#     stacks_horizontal.append(formatted_stack)
#
# sums = []
# for s in stacks_horizontal:
#     sums.append(sum(s))
#
# stacks_vertical = []
# for i in range(max_length):
#     row = []
#     for stack in stacks_horizontal:
#         row.append(stack[i])
#     stacks_vertical.append(row)
#
# for stack in stacks_vertical.copy():
#     if all(layer == 0 for layer in stack):
#         stacks_vertical.remove(stack)
#
# with open('../forecasts/stacks.csv', 'w') as file:
#     writer = csv.writer(file)
#     writer.writerow(times[1:])
#     writer.writerows(stacks_vertical)
#     writer.writerow([''])
#     writer.writerow(sums)
#
# with open('../forecasts/stacks.csv', 'r') as file:
#     reader = csv.reader(file)
#     data = [next(reader)]
#     for row in reader:
#         r = [(float(v) if v != '' else v) for v in row]
#         data.append(r)
#
# cover_sheet.update(data)
