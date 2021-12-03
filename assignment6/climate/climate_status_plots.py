#!/usr/bin/env python3
# *-* coding: utf-8 -*-

import pandas as pd
import altair as alt

def get_data_from_csv():
    """Reads data from selected csv
    
    """
    filepath = "./sample_data/"
    filename = filepath + "climate_data_combined.csv"
    df = pd.read_csv(filename, parse_dates = ["Year"])
    df["Year"] = df.Year.dt.year
    df = df.drop(["Unnamed: 0"], axis=1)
    return df
    
def plot_climate_status():
    """Plots the data

    Returns:
       json (Altair chart): A json file which can be used to plot

    """
    num2months = {1: "January", 2: "February", 3: "March", 4: "April",
              5: "May", 6: "June", 7: "July", 8: "August",
              9: "September", 10: "October", 11: "November", 12: "December"}
    months2num = {num2months[key]: key for key in num2months}
    
    climate_df = get_data_from_csv()

    column_to_plot = "Total"
    color = "Year"
    
    title = "Hello"

    print(climate_df)
    
    chart = alt.Chart(climate_df, title=title).mark_line(size=1).encode(
        x=alt.X("month:N", sort=[num2months[i] for i in range(1,13)]),
        y=alt.Y("Total:Q"),
        color=alt.Color("Year:Q"),
    )

    return chart.to_dict()

def plot_climate_status():
    """Plots the data

    Returns:
       json (Altair chart): A json file which can be used to plot

    """
    num2months = {1: "January", 2: "February", 3: "March", 4: "April",
              5: "May", 6: "June", 7: "July", 8: "August",
              9: "September", 10: "October", 11: "November", 12: "December"}
    months2num = {num2months[key]: key for key in num2months}
    monthSorted = [num2months[i] for i in range(1,13)]
    
    climate_df = get_data_from_csv()

    # Set title
    title = "Hello"

    # Format the table into seperate years
    climate_df = climate_df.pivot(index="month", columns="Year", values="Total")
    #climate_df.Year = climate_df.Year.astyp(str)
    columns = climate_df.columns
    climate_df["month"] = climate_df.index
    climate_df.index = climate_df.month.apply(lambda x: months2num[x] - 1)
    climate_df = (climate_df.sort_index())

    # Fetch the last year
    df = pd.DataFrame()
    df["Temperature"] = climate_df[columns[-1]]
    df["month"] = climate_df.month
    #print(df)

    highlight = alt.selection(
        type="single", on="mouseover")#, fields=["Temperature"])
    
    base_chart = alt.Chart(df).encode(
        x=alt.X("month", sort=monthSorted),
        y=alt.Y("Temperature"))

    points = base_chart.mark_circle().encode(
        opacity=alt.value(0),
        tooltip=[
            alt.Tooltip("month", title="Month"),
            alt.Tooltip("Temperature", title="Temperature")]
    ).add_selection(highlight)
    
    lines = base_chart.mark_line().encode(
        size=alt.condition(~highlight, alt.value(1), alt.value(3)))

    acc_chart = (points + lines).interactive()
    
    for year in columns[:-1]:
        df = pd.DataFrame()
        df["Temperature"] = climate_df[year]
        df["month"] = climate_df.month

        base_chart = alt.Chart(df).encode(
            x=alt.X("month", sort=monthSorted),
            y=alt.Y("Temperature"))
                
        lines = base_chart.mark_line().encode(
            opacity=alt.value(0.05))

        acc_chart += lines
        
    return acc_chart.properties(width=800, height=300).to_dict()

    """
    print(climate_df)

    highlight = alt.selection(
        type='single', on='mouseover', fields=["Year"], nearest=True)
    
    base_chart = alt.Chart(climate_df).encode(
        x=alt.X("month:N", sort=monthSorted,
                scale=alt.Scale(domain=monthSorted, clamp=True)),
        y=alt.Y("Value:Q", scale=alt.Scale(domain=[-2, 2])),
        color=alt.Color("Year:O", scale=alt.Scale(scheme="greenblue")))

    points = base_chart.mark_circle().encode(
        opacity=alt.value(0),
        tooltip=[
            alt.Tooltip("Year:O", title="Year"),
            alt.Tooltip("month:N", title="Month"),
            alt.Tooltip("Temperature:Q", title="Temperature")
            ]).add_selection(highlight)

    lines = base_chart.mark_line().encode(
        size=alt.condition(~highlight, alt.value(1), alt.value(3)))

    chart = (points + lines).properties(width=800, height=300).interactive()
    """
    #return chart.to_dict()
    
def main():
    plot_climate_status()
    
if __name__ == "__main__":
    main()
