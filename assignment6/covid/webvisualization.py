#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from fastapi import FastAPI
from fastapi import Request
from typing import Optional
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from webvisualization_plots import plot_reported_cases_per_million
from webvisualization_plots import get_countries
from webvisualization_plots import get_times

# create app variable (FastAPI instance)
app = FastAPI()
templates = Jinja2Templates(directory="templates")

# mount one or more static directories,
# e.g. your auto-generated Sphinx documentation with html files
app.mount(
    # the URL where these files will be available
    "/help",
    StaticFiles(
        # the directory the files are in
        directory="docs/_build/html/",
        html=True,
    ),
    # an internal name for FastAPI
    name="static",
)


@app.get("/docs")
def serve_doc_link():
    print("Docs")
    return "https://fastapi.tiangolo.com/"


@app.get("/help/")
def serve_help_link(request: Request):
    print("Help called")
    return static.TemplateResponse(
        "index.html",
        {
            "request": request,
        },
    )


@app.get("/")
def plot_reported_cases_per_million_html(request: Request):
    """
    Root route for the web application.
    Handle requests that go to the path "/".

    """
    return templates.TemplateResponse(
        "plot_reported_cases_per_million.html",
        {
            "request": request,
            "countries": get_countries(),
            "start_time": str(get_times()[0].astype('datetime64[D]')),
            "end_time": str(get_times()[-1].astype('datetime64[D]')),
            # further template inputs here
        },
    )


@app.get("/plot_reported_cases_per_million.json")
def plot_reported_cases_per_million_json(countries: Optional[str] = None,
                                         start: Optional[str]=None,
                                         end: Optional[str]=None,
                                         rolling_average: Optional[str]=None,
                                         num_roll_avg: Optional[str]=None,
                                         cumulative: Optional[str]=None,
                                         ):
    """Return json chart from altair.

    Returns:
        chart (json): returns a JSONable vega-lite structure made from altair Chart.

    """
    if countries:
        countries = countries.split(",")
    else:
        countries = None
    if not start or not end:
        start = None
        end = None
    if rolling_average and num_roll_avg and rolling_average == "true":
        rolling_average = True
        try:
            num_roll_avg = int(num_roll_avg)
        except ValueError:
            print("The number of days to average over needs to be an integer.")
            exit(1)
    else:
        rolling_average = False
        num_roll_avg = None

    if cumulative == "true":
        cumulative = True
    else:
        cumulative = None

    chart = plot_reported_cases_per_million(countries, start, end,
                                            rolling_average, num_roll_avg,
                                            cumulative)
    return chart.to_dict()


def main():
    """Called when run as a script.
    Launces the web app.
    """

    import uvicorn
    uvicorn.run(app, debug=True)

if __name__ == "__main__":
    main()
