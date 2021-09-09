import pandas as pd
# Installation instructions here https://github.com/pnuu/fmiopendata
from fmiopendata.wfs import download_stored_query
import datetime as dt

start_time = dt.datetime.now()
end_time = start_time + dt.timedelta(hours=58)
print(start_time, end_time)

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

df = pd.DataFrame(data=rows, index=indices)

print(df)
