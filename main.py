import time
from fastapi import FastAPI, Request, BackgroundTasks
from fastapi.param_functions import File
from fastapi.templating import Jinja2Templates
from requests.api import get
from starlette.responses import HTMLResponse, FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
import pandas as pd
from random_forest import predict_birds, get_star_bins
from translation import translation_dict
import matplotlib.pyplot as plt
import numpy as np

# Run in terminal with the command uvicorn main:app
app = FastAPI()
templates = Jinja2Templates(directory="templates")
favicon_path = "static/favicon.ico"
app.mount("/static", StaticFiles(directory="static"), name="static")
predictions = pd.DataFrame()
translations = {}
star_bins = []
star_rating = 0
bird_list = []


def generate_default_plot(predictions, max_birds, max_count, translations):
    colors=["#264a0d", "#3c7812", "#5cad23"]

    for i, row in enumerate(predictions.itertuples()):
        birds = max_birds.loc[row[0]]
        bird_series = predictions.loc[row[0]][birds]
        y_pos = range(len(bird_series.index))
        plt.subplot(1, 3, i+1)
        plt.bar(bird_series.index, height=bird_series, color=colors[i])
        plt.xticks(y_pos, [b.capitalize() for b in list(bird_series.index)], rotation=40)
        plt.ylim(0, max_count+int(max_count/8))
        plt.title(row[0].strftime("%d-%m-%Y"))
        if i > 0:
            plt.yticks([])
    plt.subplots_adjust(bottom=0.3)
    plt.savefig('./static/plots/default_plot.png', transparent=True)


def generate_plot(bird, predictions):
    bird_data = predictions[bird]
    bird_toplot = bird_data.rename(lambda x: x.strftime("%d-%m-%Y"))
    plot_bird = bird_toplot.plot.bar(rot=0, color=["#264a0d", "#3c7812", "#5cad23"], title=bird.capitalize())
    plt.savefig(f'./static/plots/{bird}_plot.png', transparent=True)
    return plot_bird


def generate_all_plots(predictions, translations):
    for bird in predictions.columns:
        bird_data = predictions[bird]
        bird_toplot = bird_data.rename(lambda x: x.strftime("%d-%m-%Y"))
        plot_bird = bird_toplot.plot.bar(rot=0, color=["#264a0d", "#3c7812", "#5cad23"], title=f"{bird.capitalize()} / {translations[bird]}")
        plt.savefig(f'./static/plots/{bird}_plot.png', transparent=True)


def get_star_rating(predictions, star_bins):
    today_sum = predictions.sum(axis=1)[0]
    for i in range(len(star_bins)):
        if today_sum in star_bins[i]:
            return i + 1

def predict():
    print("Predicting...")
    global predictions
    global translations
    global star_bins
    global star_rating
    global bird_list
    predictions = predict_birds().astype(int)
    translations = translation_dict()
    star_bins = get_star_bins()
    star_rating = get_star_rating(predictions, star_bins)
    max_birds = predictions.apply(lambda s: s.abs().nlargest(3).index.tolist(), axis=1)
    max_count = predictions.max().max()
    generate_all_plots(predictions, translations)
    generate_default_plot(predictions, max_birds, max_count, translations)
    bird_list = list(predictions.columns)
    print("Predicted.")


@app.get('/', response_class=HTMLResponse)
async def loading(request: Request, background_tasks: BackgroundTasks):
    background_tasks.add_task(predict)
    return templates.TemplateResponse("loading.html", {"request": request})


@app.get("/birdforecast", response_class=HTMLResponse)
async def root(request: Request):
    global predictions
    global translations
    global star_rating
    global bird_list
    return templates.TemplateResponse("index.html", {"request": request,
                                                     "bird_number": predictions.shape[1],
                                                     "bird_list": bird_list,
                                                     "star_rating": star_rating,
                                                     "translations": translations})


@app.get('/favicon.ico')
async def favicon():
    return FileResponse(favicon_path)
