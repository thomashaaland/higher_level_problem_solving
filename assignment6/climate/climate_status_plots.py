#!/usr/bin/env python3
# *-* coding: utf-8 -*-

import pandas as pd
import altair as alt

def get_data_from_csv():
    """Reads data from selected csv
    
    Returns:
       A pandas dataframe
    """
    filepath = "./sample_data/"
    filename = filepath + "climate_data_combined.csv"
    df = pd.read_csv(filename, parse_dates = ["Year"])
    df["Year"] = df.Year.dt.year
    df = df.drop(["Unnamed: 0"], axis=1)
    return df
    

def plot_climate_status():
    """Plots climate data. Yields an interactive plot
    displaying the hottest year with its temperature
    and coldest year with its temperature.

    Returns:
       json (Altair chart): A json file which can be used to plot

    """
    num2months = {1: "January", 2: "February", 3: "March", 4: "April",
              5: "May", 6: "June", 7: "July", 8: "August",
              9: "September", 10: "October", 11: "November", 12: "December"}
    months2num = {num2months[key]: key for key in num2months}
    monthSorted = [num2months[i] for i in range(1,13)]
    
    climate_df = get_data_from_csv()    
        
    # Grab coldest and hottest years
    hot = climate_df.groupby("month").max("Total")
    cold = climate_df.groupby("month").min("Total")
    hot_cold = hot.append(cold)

    hot_cold = hot_cold.reset_index()
    print(hot_cold)
    
    # Make the 'background' lines
    base_chart = alt.Chart(climate_df).encode(
        x=alt.X("month:N", sort=monthSorted,
                scale=alt.Scale(domain=monthSorted, clamp=True)),
        y=alt.Y("Total:Q", scale=alt.Scale(domain=[2, 16])),
        color=alt.Color("Year:O", scale=alt.Scale(scheme="greenblue"), legend=None)
    )
    lines = base_chart.mark_line(opacity=0.2).encode()

    # Create the max and min plots. This plot is the interactive one
    label = alt.selection_single(
        encodings=['x'],
        on="mouseover",
        nearest=True,
        empty="none"
    )

    base = alt.Chart(hot_cold).mark_line().encode(
        alt.X('month:N', sort=monthSorted),
        alt.Y('Total:Q'),
        alt.Color("Year:N")
    )

    layer = alt.layer(
        base,

        # Rule chart
        alt.Chart().mark_rule(color='#aaa').encode(
            x=alt.X('month:N', sort=monthSorted),
            ).transform_filter(label),

        # add circle marks for selected month points, hide unselected points
        base.mark_circle().encode(
            opacity=alt.condition(label, alt.value(1), alt.value(0))
        ).add_selection(label),

        # Add white stroked text to provide a legible background for labels
        base.mark_text(align='left', dx=5, dy=-5, stroke="white", strokeWidth=2).encode(
            text='Total:Q'
        ).transform_filter(label),

        # add text labels for temperature
        base.mark_text(align='left', dx=5, dy=-5, stroke="black").encode(
            text="Total:Q"
        ).transform_filter(label),

                # Add white stroked text to provide a legible background for labels
        base.mark_text(align='left', dx=5, dy=-20, stroke="white", strokeWidth=2).encode(
            text='Year:Q'
        ).transform_filter(label),

        # add text labels for temperature
        base.mark_text(align='left', dx=5, dy=-20, stroke="black").encode(
            text="Year:Q"
        ).transform_filter(label),

        data = hot_cold
    )
        
    chart = (lines + layer).properties(width=600, height=300)#.interactive()
    return chart.to_dict()
    
def main():
    plot_climate_status()
    
if __name__ == "__main__":
    main()
