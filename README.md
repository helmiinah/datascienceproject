# datascienceproject
A FastAPI application that predicts counts of migratory birds for the following days based on historical bird observation data and weather. Project for the course Introduction to Data Science by the University of Helsinki.

### How to use

1) Clone the repository with `git clone`

2) You can create a virtual environment with `python3 -m venv birdforecast_env` (windows: `py -3 -m venv birdforecast_env`)

3) Activate virtual environment `. birdforecast_env/bin/activate` (windows: `birdforecast_env/Scripts/activate`)

4) Go to **datascienceproject** folder

5) Install dependencies with `pip3 install -r requirements.txt` (or `pip install -r requirements.txt`)

6) Run the app with the command `uvicorn main:app`

### Data sources:

- Helsingin Seudun Lintutieteellinen Yhdistys Tringa ry (2020) Hangon lintuaseman aineisto: päiväsummat (versio 1.4). Ladattu osoitteesta www.halias.fi/pitkaaikaisaineisto 8.9.2021
- Ilmatieteenlaitos (Finnish Meteorological Institute), open weather observation data, downloaded from www.ilmatieteenlaitos.fi/havaintojen-lataus 8.9.2021. Some variable names are changed, and the formatting of the data is modified.
- Forecast data is streamed from Ilmatieteenlaitos (Finnish Meteorological Institute)
- Our group member Jussi-Veikka Hynynen owns the rights to all images of birds