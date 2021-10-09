from fastapi import FastAPI, Request
from fastapi.param_functions import File
from fastapi.responses import FileResponse
from fastapi.templating import Jinja2Templates
from requests.api import get
from starlette.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import pandas as pd
import datetime as dt
from random_forest import predict_birds
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Run in terminal with the command uvicorn main:app --reload
app = FastAPI()
templates = Jinja2Templates(directory="templates")
predictions = predict_birds().astype(int)
max_birds = predictions[predictions.idxmax(axis=1)]
app.mount("/static", StaticFiles(directory="static"), name="static")


def generate_default_plot():
    global predictions
    global max_birds
    diag = pd.Series(np.diag(max_birds), index=[max_birds.index, max_birds.columns])
    diag.index = diag.index.map(lambda t: t[0].strftime("%d-%m-%Y") + "\n" + str(t[1]))
    plot_def = diag.plot.bar(rot=0, ylabel="Predicted number of birds", color=["#264a0d", "#3c7812", "#5cad23"], title="Daily birds")
    plt.savefig('./static/default_plot.png', transparent=True)
    return plot_def


def generate_plot(bird):
    global predictions
    bird_data = predictions[bird]
    bird_toplot = bird_data.rename(lambda x: x.strftime("%d-%m-%Y"))
    plot_bird = bird_toplot.plot.bar(rot=0, color=["#264a0d", "#3c7812", "#5cad23"], title=bird.capitalize())
    plt.savefig(f'./static/{bird}_plot.png', transparent=True)
    return plot_bird
    

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    global predictions
    global max_birds
    bird_list = list(predictions.columns)
    birdcast = predictions.to_html()
    generate_plot("haapana")
    generate_default_plot()
    return templates.TemplateResponse("index.html", {"request": request,
                                                     "birdcast": birdcast,
                                                     "bird_number": predictions.shape[1],
                                                     "bird_list": bird_list,
                                                     "max_birds": max_birds.to_html()})
