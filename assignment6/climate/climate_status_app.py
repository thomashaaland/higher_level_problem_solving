#!/usr/bin/env python3
# *-* coding: utf-8 -*-

from fastapi import FastAPI
from fastapi import Request

from fastapi.templating import Jinja2Templates

from climate_status_plots import plot_climate_status

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Mount static directories here

@app.get("/")
def plot_climate_status_html(request: Request):
    """Root route for the web app.
    Handle requests that go to the path "/".
    
    """
    print("Root")
    return templates.TemplateResponse(
        "plot_climate_status.html",
        {
            "request": request,
        }
    )

@app.get("/plot_climate_status.json")
def plot_climate_status_json():
    """Return json chart from altair.
    
    Return:
        Chart (json): returns a json made from altair chart.
    
    """
    print("Trying to get chart")
    
    chart = plot_climate_status()

    return chart

def main():
    """Called when run as a script

    Launches the web app.
    """
    import uvicorn
    uvicorn.run(app, debug = True)

if __name__ == "__main__":
    main()
