#!/usr/bin/env python3
# *-* coding: utf-8 -*-

import pandas as pd
from requests_html import HTMLSession
from bs4 import BeautifulSoup

def get_anomaly_data_from_csv():
    """Creates a pandas dataframe from .csv file downloaded.

    """
    
    url = ("https://www.ncdc.noaa.gov/cag/global/"
           + "time-series/globe/land_ocean/all/1/1880-2020/data.csv")
    
    df = pd.read_csv(
        url,
        delimiter=",",
        header=4,
        parse_dates=["Year"],
        date_parser=lambda col: pd.to_datetime(col, format="%Y%m"),
        infer_datetime_format=True,
    )    
    return df

def get_mean_data_from_website():
    """Creating a dict from data scraped from website

    """
    url = "https://www.ncdc.noaa.gov/monitoring-references/faq/anomalies.php#mean"

    session = HTMLSession()
    response = session.get(url)
    response.html.render()

    html_string = response.html.html
    
    soup = BeautifulSoup(html_string, "html.parser")
    
    tables = soup.find(id="monitoring-content").find_all("table")

    combined_table = tables[0]

    combined_data = [data.text for data in combined_table.find_all("tr")[1].find_all("td")]
        
    return {i: combined_data[i] for i in range(1, 13)}
    
def get_combined_data():
    """Returns a panda dataframe with combined data

    """
    means = get_mean_data_from_website()
    divergence = get_anomaly_data_from_csv()
    months = {1: "January", 2: "February", 3: "March", 4: "April",
              5: "May", 6: "June", 7: "July", 8: "August",
              9: "September", 10: "October", 11: "November", 12: "December"}
    
    divergence["Total"] = (divergence.Value.astype(float)
                           + divergence.Year.dt.month.apply(lambda x: means[x]).astype(float))
    divergence["month"] = divergence.Year.dt.month.apply(lambda x: months[x])
    
    return divergence

def write_data_to_disk(filename):
    """Writes data to disk for later use.

    """
    data = get_combined_data()
    data.to_csv(filename)

def main():
    filepath = "./sample_data/"
    filename = filepath + "climate_data_combined.csv"
    write_data_to_disk(filename)
    
if __name__ == "__main__":
    main()
