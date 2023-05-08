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

