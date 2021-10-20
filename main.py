from fastapi import FastAPI, Request
from fastapi.param_functions import File
from fastapi.templating import Jinja2Templates
from requests.api import get
from starlette.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import pandas as pd
from random_forest import predict_birds, get_star_bins
from translation import translation_dict
import matplotlib.pyplot as plt
import numpy as np

# Run in terminal with the command uvicorn main:app
app = FastAPI()
templates = Jinja2Templates(directory="templates")
predictions = predict_birds().astype(int)
star_bins = get_star_bins()
max_birds = predictions.apply(lambda s: s.abs().nlargest(3).index.tolist(), axis=1)
max_count = predictions.max().max()
translations = translation_dict()
app.mount("/static", StaticFiles(directory="static"), name="static")


def generate_default_plot():
    global max_birds
    global max_count
    global predictions

    colors=["#264a0d", "#3c7812", "#5cad23"]

    for i, row in enumerate(predictions.itertuples()):
        birds = max_birds.loc[row[0]]
        bird_series = predictions.loc[row[0]][birds]
        y_pos = range(len(bird_series.index))
        plt.subplot(1, 3, i+1)
        plt.bar(bird_series.index, height=bird_series, color=colors[i])
        plt.xticks(y_pos, bird_series.index, rotation=40)
        plt.ylim(0, max_count+int(max_count/8))
        plt.title(row[0].strftime("%d-%m-%Y"))
        if i > 0:
            plt.yticks([])
    plt.subplots_adjust(bottom=0.3)
    plt.savefig('./static/plots/default_plot.png', transparent=True)


def generate_plot(bird):
    global predictions
    bird_data = predictions[bird]
    bird_toplot = bird_data.rename(lambda x: x.strftime("%d-%m-%Y"))
    plot_bird = bird_toplot.plot.bar(rot=0, color=["#264a0d", "#3c7812", "#5cad23"], title=bird.capitalize())
    plt.savefig(f'./static/plots/{bird}_plot.png', transparent=True)
    return plot_bird


def generate_all_plots():
    global predictions
    for bird in predictions.columns:
        bird_data = predictions[bird]
        bird_toplot = bird_data.rename(lambda x: x.strftime("%d-%m-%Y"))
        plot_bird = bird_toplot.plot.bar(rot=0, color=["#264a0d", "#3c7812", "#5cad23"], title=f"{bird.capitalize()} / {translations[bird]}")
        plt.savefig(f'./static/plots/{bird}_plot.png', transparent=True)


def get_star_rating():
    global predictions
    global star_bins
    today_sum = predictions.sum(axis=1)[0]
    for i in range(len(star_bins)):
        if today_sum in star_bins[i]:
            return i + 1


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    global predictions
    bird_list = list(predictions.columns)
    star_rating = get_star_rating()
    generate_all_plots()
    generate_default_plot()
    return templates.TemplateResponse("index.html", {"request": request,
                                                     "bird_number": predictions.shape[1],
                                                     "bird_list": bird_list,
                                                     "star_rating": star_rating})
