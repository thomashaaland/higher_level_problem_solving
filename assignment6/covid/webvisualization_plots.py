#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime

import altair as alt
import pandas as pd


def get_data_from_csv(columns, countries=None, start=None, end=None):
    """Creates pandas dataframe from .csv file.

    Data will be filtered based on data column name, list of countries to be plotted
    and time frame chosen.

    Args:
        columns- (list(string)): a list of data columns you want to include
        countries ((list(string), optional): List of countries you want to include.
        If none is passed, dataframe should be filtered for the 6 countries with the
        highest number of cases per million at the last current date available in
        the timeframe chosen.

        start (string, optional): The first date to include in the returned dataframe.
            If specified, records earlier than this will be excluded.
            Default: include earliest date
            Example format: "2021-10-10"

        end (string, optional): The latest date to include in the returned data frame.
            If specified, records later than this will be excluded.
            Example format: "2021-10-10"

    Returns:
        cases_df (dataframe): returns dataframe for the timeframe, columns, and
        countries chosen

    """

    # add path to .csv file from 6.0
    path = "./sample_data/owid-covid-data.csv"

    # read .csv file, define which columns to read
    df = pd.read_csv(
        path,
        sep=",",
        usecols=["location"] + ["date"] + columns,
        parse_dates=["date"],
        date_parser=lambda col: pd.to_datetime(col, format="%Y-%m-%d"),
    )

    if countries is None:
        # no contries specified, pick 6 countries with the highest case count at end_date
        if end is None:
            # no end date specified, pick latest date available
            end_date = df.date.iloc[-1]
        else:
            end_date = datetime.strptime(end, "%Y-%m-%d")
        df_latest_dates = df[df.date.isin([end_date])]

        worst_5_countries = df_latest_dates.sort_values(
            columns, ascending=False).head(5)["location"]

        # identify the 6 coutries with the highest case count
        # on the last included day
        countries = list(worst_5_countries)

    # now filter to inlcude only the selected countries
    cases_df = df[df.location.isin(countries)]

    # apply date filters
    if start is not None:
        start_date = datetime.strptime(start, "%Y-%m-%d")
        # exculde records earlier than start_date
        cases_df = cases_df[cases_df.date >= start_date].dropna()

    if end is not None:
        end_date = datetime.strptime(end, "%Y-%m-%d")
        if start_date is not None and start_date >= end_date:
            raise ValueError("The start date must be earlier than the end date.")

        # exclude records later than end date
        cases_df = cases_df[cases_df.date <= end_date].dropna()

    return cases_df


def get_countries():
    """Returns a list of all countries in the dataset.

    Returns:
        list(str): All countries in the dataset.

    """
    # add path to .csv file from 6.0
    path = "./sample_data/owid-covid-data.csv"

    # read .csv file, define which columns to read
    df = pd.read_csv(path, sep=",", usecols=["location"])

    countries = df.location.unique()
    return countries


def get_times():
    """Returns a list of all dates in the dataset.

    Returns:
        list(numpy.datetime64)

    """

    # add path to .csv file from 6.0
    path = "./sample_data/owid-covid-data.csv"

    # read .csv file, define which columns to read
    df = pd.read_csv(path, sep=",",
                     usecols=["date"],
                     parse_dates=["date"])

    return df.date.values


def plot_reported_cases_per_million(countries=None, start=None, end=None,
                                    rolling_average=None, num_roll_avg=None,
                                    cumulative=None):
    """Plots data of reported covid-19 cases per million using altair.

    Calls the function get_data_from_csv to receive a dataframe used for plotting.

    Args:
        countries ((list(string), optional): List of countries you want to filter.
            If none is passed, dataframe will be filtered for the 6 countries with
            the highest number of cases per million at the last current date
            available in the timeframe chosen.
        start (string, optional): a string of the start date of the table, none
            of the dates will be older then this on.
        end (string, optional): a string of the en date of the table, none of
            the dates will be newer then this one.
        rolling_average (string, optional): Takes the values false or true if
            any value. If true turns on rolling average.
        num_roll_avg (string, optional): Takes a string representation of an
            integer. This is the number of days on both back in time and ahead
            in time to average over.
        cumulative= (string, optional): Takes a string representation of a
            boolean 'true' or 'false'. If true is listed also supply a cumulative
            plot.

    Returns:
        altair Chart of number of reported covid-19 cases over time.

    """

    # choose data column to be extracted
    columns = ["new_cases_smoothed_per_million", "new_cases_per_million"]
    # create dataframe
    cases_df = get_data_from_csv(columns, countries, start, end)

    column_to_plot = columns[1]

    # Note: when you want to plot all countries simultaneously while enabling checkboxes,
    # you might need to disable altairs max row limit by commenting in the following line
    # alt.data_transformers.disable_max_rows()

    # Make title
    title = " ".join(["Daily"] +
                     [column_to_plot.split("_")[0]] +
                     ["Covid 19"] +
                     column_to_plot.split("_")[1:] +
                     ["People"]).title()

    chart_points = (
        alt.Chart(cases_df, title=title)
        # .mark_point(size=1)
        .encode(
            x=alt.X(
                "date:T",
                axis=alt.Axis(
                    format="%b, %Y", title="Date", titleFontSize=14, tickCount=20
                ),
            ),
            y=alt.Y(
                column_to_plot + ":Q",
                axis=alt.Axis(
                    title="Number of Reported Cases per Million",
                    titleFontSize=14,
                    tickCount=10,
                ),
            ),
            color=alt.Color("location:N", legend=alt.Legend(title="Country")),
            tooltip=[
                "location",
                column_to_plot,
                ],
        )
    )

    if rolling_average:
        chart_rolling_mean = alt.Chart(cases_df).mark_line(size=3).transform_window(
            rolling_mean="mean(" + column_to_plot + ")",
            frame=[-num_roll_avg, num_roll_avg],
        ).encode(
            x="date:T",
            y="rolling_mean:Q",
            color="location:N",
            tooltip=[
                "location",
                column_to_plot,
            ],
        )

        chart = (chart_points.mark_point(size=3) + chart_rolling_mean).interactive()
    else:
        chart = chart_points.mark_line(size=1).interactive()

    if cumulative:
        df_cumsum = cases_df.pivot("date", "location", column_to_plot).fillna(0).cumsum()
        df = pd.DataFrame()
        df["cumulative"] = None
        df["location"] = None
        df["date"] = None

        for location in df_cumsum.columns:
            df_temp = pd.DataFrame()
            df_temp["cumulative"] = df_cumsum[location]
            df_temp["location"] = location
            df_temp["date"] = df_cumsum.index
            df = df.append(df_temp)


# Make title
        title = " ".join(["Cumulative Covid 19"] +
                         column_to_plot.split("_")[1:] +
                         ["People"]).title()

        chart_cum = alt.Chart(df, title=title).mark_line(size=3).encode(
            x=alt.X(
                "date:T",
                axis=alt.Axis(
                    format="%b, %Y", title="Date", titleFontSize=14, tickCount=20
                ),
            ),
            y=alt.Y(
                "cumulative:Q",
                axis=alt.Axis(
                    title="Cumulative Number of Reported Cases per Million",
                    titleFontSize=14,
                    tickCount=10,
                ),
            ),
            color="location:N",
            tooltip=[
                "location:N",
                "cumulative",
            ]
        ).interactive()

        chart = chart_cum

    return chart


def main():
    """Function called when run as a script.
    Creates a chart and display it or save it to a file
    """
    chart = plot_reported_cases_per_million()
    # chart.show requires altair_viewer
    # or you could save to a file instead
    chart.show()


if __name__ == "__main__":
    main()
