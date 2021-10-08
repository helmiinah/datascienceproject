from fastapi import FastAPI, Request
from fastapi.param_functions import File
from fastapi.responses import FileResponse
from fastapi.templating import Jinja2Templates
from requests.api import get
from starlette.responses import HTMLResponse
import pandas as pd
import datetime as dt
from random_forest import predict_birds
import matplotlib.pyplot as plt
import seaborn as sns

# Run in terminal with the command uvicorn main:app --reload
app = FastAPI()
templates = Jinja2Templates(directory="templates")
predictions = predict_birds().astype(int)
max_birds = predictions[predictions.idxmax(axis=1)]


def generate_default_plot():
    global predictions
    global max_birds
    plot = max_birds.plot.bar(rot=0)
    plt.savefig('./plots/default_plot.png')
    return plot


def generate_plot(bird):
    global predictions


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    global predictions
    global max_birds
    bird_list = list(predictions.columns)
    birdcast = predictions.to_html()
    # generate_default_plot()
    return templates.TemplateResponse("index.html", {"request": request,
                                                     "birdcast": birdcast,
                                                     "bird_number": predictions.shape[1],
                                                     "bird_list": bird_list,
                                                     "max_birds": max_birds.to_html()})
