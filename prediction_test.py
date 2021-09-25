import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split, cross_val_score



# Day by species, cells contain observation counts
df = pd.read_csv("datascienceproject/data/haliasdata-2010-2019.csv").rename(columns={"Unnamed: 0": "Date"})
birds_2019 = df.loc[(df["Date"] >= "2010-01-01")].fillna(0)


# Day by weather variables
df2 = pd.read_csv("datascienceproject/data/weather-2010-2019-cleaned.csv")
weather_2019 = df2.loc[(df2["Date"] >= "2010-01-01")]

# List of bird species in data
bird_species = [item for item in birds_2019]
bird_species.remove("Date")

# List of weather variables
variables = [item for item in weather_2019]
variables.remove("Date")


# def graphing(bird_data, weather_data, bird):
#     """helps print graphs"""
#     first_column = bird_data.filter(items=["Date", str(bird)])
#     merged = pd.merge(first_column, weather_data, on="Date")
#     for var in variables:
#         merged.plot(x=str(var), y=str(bird), style="*")
#         plt.xlabel(str(var))
#         plt.ylabel(str(bird))
#         plt.show()
#
#     return merged


# TRAIN

first_column = birds_2019.filter(items=["Date", "talitiainen"])
merged = pd.merge(first_column, weather_2019, on="Date")

X = merged["talitiainen"].values.reshape(-1, 1)
y = merged["Precipitation amount (mm)"].values


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)


def get_cv_scores(model):
    scores = cross_val_score(model, X_train, y_train, cv=10, scoring='r2')

    print('CV Mean: ', np.mean(scores))
    print('STD: ', np.std(scores))
    print('\n')


lr = LinearRegression().fit(X_train, y_train)
get_cv_scores(lr)


# PREDICT
y_pred = lr.predict(X_test)

plt.scatter(X_train, y_train)
plt.plot(X_test, y_pred, color='red')
plt.show()

comparison = pd.DataFrame({"Actual":y_test, "Predicted": y_pred})
comparison.head()

