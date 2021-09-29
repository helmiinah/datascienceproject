import pandas as pd
# Installation instructions here https://github.com/pnuu/fmiopendata
from fmiopendata.wfs import download_stored_query
import datetime as dt
import numpy as np


def get_hourly_forecast():
    start_time = dt.datetime.now()
    end_time = start_time + dt.timedelta(hours=58)
    print(f"Getting weather forecast for {start_time} - {end_time}...\n")

    # The weather forecast is streamed from the FMI open data and seems to give info about the upcoming ~58 hours
    futuredata = download_stored_query("fmi::forecast::harmonie::surface::point::multipointcoverage",
                                       args=["place=helsinki", "starttime=" + str(start_time),
                                             "endtime=" + str(end_time)])

    indices = []
    rows = []
    for item in futuredata.data.items():
        indices.append(item[0])
        row = item[1]['Helsinki']
        for key in list(row.keys()):
            cell = f"{list(row[key].values())[0]}"
            row[f"{key} ({list(row[key].values())[1]})"] = cell
            del row[key]
        rows.append(row)

    # Store hourly info to a time series dataframe
    df = pd.DataFrame(data=rows, index=indices)
    # Only keep columns we use
    df = df[["Total cloud cover (%)", "Air pressure (hPa)", "Precipitation amount (mm)",
             "Air temperature (degC)", "Visibility (m)", "Wind direction (deg)", "Wind speed (m/s)"]]
    return df


def get_daily_forecast(hourly_forecast):
    df_hourly = hourly_forecast.astype("float")
    df_daily = df_hourly.resample('D').agg({'Total cloud cover (%)': np.mean, 'Air pressure (hPa)': np.mean,
                                            'Precipitation amount (mm)': np.sum, 'Air temperature (degC)': np.mean,
                                            'Visibility (m)': np.mean, 'Wind direction (deg)': np.mean,
                                            'Wind speed (m/s)': np.mean})
    df_daily = df_daily.round(1)
    return df_daily
