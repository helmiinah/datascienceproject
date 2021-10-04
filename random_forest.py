from sklearn.ensemble import RandomForestRegressor
import pandas as pd
import numpy as np
import datetime as dt
from forecast import get_hourly_forecast, get_daily_forecast


def predict_birds():
    bird_df = pd.read_csv("data/haliasdata-2010-2019_new.csv", index_col=0).fillna(0)
    weather_df = pd.read_csv("data/weather-2010-2019-cleaned_new.csv", index_col="Date")

    bird_df.index = pd.to_datetime(bird_df.index)
    weather_df.index = pd.to_datetime(weather_df.index)

    birds = pd.DataFrame()
    weather = pd.DataFrame()
    # UNCOMMENT if want to specify weather variables! Uses all by default.
    # weather_vars = ["Precipitation amount (mm)", "Wind speed (m/s)", "Visibility (m)"]

    hourly = get_hourly_forecast()
    forecast = get_daily_forecast(hourly)

    # Use training data from years 2010-2019
    # TODO: Optimize getting the training data from the halias-data if possible
    for n in range(10):
        year = f"201{n}"
        start = dt.datetime(month=int(forecast.index[0].month), day=int(forecast.index[0].day), year=int(year)) - dt.timedelta(days=3)
        end = dt.datetime(month=int(forecast.index[-1].month), day=int(forecast.index[-1].day),  year=int(year)) + dt.timedelta(days=3)
        birds = pd.concat([birds, bird_df[start:end]])
        # UNCOMMENT next line if want to specify weather variables
        # weather = pd.concat([weather, weather_df[start:end]])[weather_vars]
        # COMMENT next line if want to specify weather variables
        weather = pd.concat([weather, weather_df[start:end]])

    # Determine species of which counts to predict
    # species_set = {"tilhi", "valkoposkihanhi", "kurki", "laulujoutsen", "västäräkki"}
    species_set = birds.columns
    predictions = pd.DataFrame(columns=species_set, index=forecast.index)

    # Predict bird counts for the next 3-4 days
    for species in species_set:
        spec_bird = birds[species]
        X, y = weather, spec_bird
        model = RandomForestRegressor(n_estimators=150)
        model.fit(X, y)
        for i in range(len(forecast.index)):
            pred_date = forecast.index[i]
            # UNCOMMENT next line if want to specify weather variables
            # test_X = np.array([forecast[weather_vars].loc[pred_date].to_numpy()])
            # COMMENT next line if want to use specific weather variables
            test_X = np.array([forecast.loc[pred_date].to_numpy()])
            pred = round(model.predict(test_X)[0])
            predictions.at[pred_date, species] = pred

    predictions = predictions.loc[:, (predictions != 0).any(axis=0)]
    return predictions


if __name__ == "__main__":
    t1 = dt.datetime.now()
    predictions = predict_birds()
    print(f"Found predictions for {predictions.shape[1]} birds: \n")
    print(predictions)
    t2 = dt.datetime.now()
    print("\nTime spent:", t2 - t1)
