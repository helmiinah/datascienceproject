from sklearn.ensemble import RandomForestRegressor
import pandas as pd
import numpy as np
import datetime as dt
from forecast import get_hourly_forecast, get_daily_forecast


def predict_birds():
    bird_df = pd.read_csv("./data/haliasdata-2010-2019.csv", index_col=0).fillna(0)
    weather_df = pd.read_csv("./data/weather-2010-2019-cleaned_new.csv", index_col="Date")

    bird_df.index = pd.to_datetime(bird_df.index)
    weather_df.index = pd.to_datetime(weather_df.index)

    birds = pd.DataFrame()
    weather = pd.DataFrame()
    weather_vars = ["Precipitation amount (mm)", "Wind speed (m/s)", "Visibility (m)"]

    hourly = get_hourly_forecast()
    forecast = get_daily_forecast(hourly)

    # Use training data from years 2010-2019
    for n in range(10):
        year = f"201{n}"
        start = dt.datetime(month=int(forecast.index[0].month), day=int(forecast.index[0].day), year=int(year)) - dt.timedelta(days=3)
        end = dt.datetime(month=int(forecast.index[-1].month), day=int(forecast.index[-1].day),  year=int(year)) + dt.timedelta(days=3)
        birds = pd.concat([birds, bird_df[start:end]])
        weather = pd.concat([weather, weather_df[start:end]])[weather_vars]

    # Determine species of which counts to predict
    species_set = {"tilhi", "valkoposkihanhi", "kurki", "laulujoutsen", "västäräkki"}
    # species_set = birds.columns

    # Predict bird counts for the next 3-4 years
    # TODO: Only show birds with more than 0 prediction counts
    for species in species_set:
        spec_bird = birds[species]
        X, y = weather, spec_bird
        model = RandomForestRegressor(n_estimators=150)
        model.fit(X, y)
        for i in range(len(forecast.index)):
            pred_date = forecast.index[i]
            test_X = np.array([forecast[weather_vars].loc[pred_date].to_numpy()])
            print("Species:", species)
            print("date:", pred_date.strftime("%d-%m-%Y"))
            pred = round(model.predict(test_X)[0])
            print("prediction:", pred, "\n")


if __name__ == "__main__":
    predict_birds()
