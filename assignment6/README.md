# README.md Assignment 6

## Task 6

### Prerequisites

Version of python used is python 3.9.7.

List of prerequisites can be found in [requirements.txt](./requirements.txt). 

#### Tested on the following platforms
* Operating system: Ubuntu 20.04.3 LTS
  	    Kernel: Linux 5.11.0-37-generic

### Functionality

#### Covid Visualization

Runs a server which displays some data on Covid-19 on a webpage. It is possible to select the time period to show the data, day to day new cases, rolling average and cumulative plots. It is possible to access a help page and the FastAP Docs on the top banner. 

#### Climate Visualization

Runs a server which displays some climate data. It is displayed year by year superimposed plotted by temperature according to month. When hovering over the plot, the hottest and coldest year on record is displayed along with the temperatures for that month.

### Missing functionality

The Climate data user interface is sparse and lacks proper description of what is displayed.

### Usage

You need to install dependencies first. You build a virtual environment using the [requirements.txt](requirements.txt) file.

#### Covid visualization

Run the script `/covid/webvisualization.py` to start the server. You can now open the url `http://127.0.0.1:8000` to see the page.

#### Climate Visualization

Run the script `/climate/climate_status_app.py` to start the server. You can now open the url `https://127.0.0.1:8000` to see the resulting page.

## Assumptions

`get_data_from_csv` use the "new_cases_smoothed_per_million" column from the file `owid-covid-data.csv`. By default it chooses the 6 countries with the highest number of new cases to plot. The start date is by default whenever the data starts and ends whenever the data ends.