import marimo

__generated_with = "0.12.4"
app = marimo.App(width="medium", app_title="The Mustachioed Runner")


@app.cell(hide_code=True)
def session_configs():
    import altair as alt
    import gspread
    import json
    import marimo as mo
    import polars as pl
    import polars.selectors as cs
    import time
    from datetime import datetime, timedelta
    from great_tables import GT
    from stravalib import Client
    return (
        Client,
        GT,
        alt,
        cs,
        datetime,
        gspread,
        json,
        mo,
        pl,
        time,
        timedelta,
    )


@app.cell(hide_code=True)
def strava_api_client(Client, json, time):
    client = Client()

    client_id, client_secret = open("strava_client.txt").read().split(',')

    with open("strava_token.json", "r") as _f:
        strava_token = json.load(_f)

    if time.time() > strava_token["expires_at"]:
        print("")
        print("****User can ignore the ERROR and WARNING messages above.****")
        print("")
        print("Token has expired. Will refresh.")
        print("")
        refresh_response = client.refresh_access_token(
            client_id=client_id,
            client_secret=client_secret,
            refresh_token=strava_token["refresh_token"])
        client.access_token = refresh_response["access_token"]
        client.refresh_token = refresh_response["refresh_token"]
        client.token_expires_at = refresh_response["expires_at"]
    else:
        print("")
        print("****User can ignore the ERROR and WARNING messages above.****")
        print("")
        print("Token still valid. Expires at {}.".format(time.strftime("%a, %d %b %Y %H:%M:%S %Z", time.localtime(strava_token["expires_at"]))))
        print("")
        client.access_token = strava_token["access_token"]
        client.refresh_token = strava_token["refresh_token"]
        client.token_expires_at = strava_token["expires_at"]
    return client, client_id, client_secret, refresh_response, strava_token


@app.cell(hide_code=True)
def functions(pl, timedelta):
    def get_total_miles(df: pl.DataFrame ,year: int) -> dict:
        _output = (
            df
            .filter(pl.col("date").dt.year() == year)
            .with_columns(pl.col("date").dt.year().alias("year"))
            .select("year", "distance_miles")
            .group_by("year")
            .sum()
            .drop("year")
            .to_dict(as_series=False)
        )
        _output_dict = {year: _output}
        return _output

    def get_avg_run_pace(df: pl.DataFrame, year: [int, float]) -> dict:
        _output = (
            df
            .filter(pl.col("date").dt.year() == year)
            .select("secs_per_mile")
            .mean()
            .with_columns(pl.col("secs_per_mile").round(0))
            .with_columns(
                pl.col("secs_per_mile")
                .map_elements(lambda n: str(timedelta(seconds=n)), return_dtype=pl.String)
                .alias("mins_per_mile"))
            .drop("secs_per_mile")
            .to_dict(as_series=False)
        )
        _output_dict = {year: _output}
        return _output

    def get_no_of_races(df: pl.DataFrame,  year: int) -> dict:
        _output = (
            df
            .filter(
                (pl.col("date").dt.year() == year) & 
                (pl.col("official_time").is_not_null())
            )
            .select(pl.len().alias("no_of_races"))
            .to_dict(as_series=False)
        )
        _output_dict = {year: _output}
        return _output

    def get_race_miles(df: pl.DataFrame, year: int) -> dict:
        _output = (
            df
            .filter(
                (pl.col("date").dt.year() == year) & 
                (pl.col("official_time").is_not_null())
            )
            .select(pl.col("miles").alias("race_miles"))
            .sum()
            .to_dict(as_series=False)
        )
        _output_dict = {year: _output}
        return _output

    def get_avg_race_pace(df: pl.DataFrame, year: int) -> dict:
        """
        Parameters
        ----------
        df : polars DataFrame
            A polars DataFrame containing both a "date" and "official_pace" column.

        year: int
            An integer value of the year

        Returns
        -------
        dict
            A dictionary with a list value.

        Notes
        -----
        Rename your columns to be "date" and "official_pace" if they aren't already named that.

        Example
        --------
        >>> get_avg_race_pace(df=official_race_results_df, year=2024)
        {
            "official_pace": [
                0: 00:08:09.733333
            ]
        }
        """
        _output = (
            df
            .filter(
                (pl.col("date").dt.year() == year) & 
                (pl.col("official_time").is_not_null())
            )
            .select("official_pace_in_seconds")
            .mean()
            .select("official_pace_in_seconds")
            .to_dict(as_series=False)
        )
        _output_dict = {year: _output}
        return _output
    return (
        get_avg_race_pace,
        get_avg_run_pace,
        get_no_of_races,
        get_race_miles,
        get_total_miles,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.vstack([
        mo.md("# **The Mustachioed Runner**"),
        mo.md("***")
    ])
    return


@app.cell(hide_code=True)
def _(mo, yearly_metrics):
    select_year = mo.ui.dropdown(
        options=yearly_metrics.keys(),
        value=max(yearly_metrics.keys()),
        label="Select a Year",
        full_width=True
    )

    mo.hstack(
        [
            select_year
        ]
    )
    return (select_year,)


@app.cell(disabled=True, hide_code=True)
def yearly_metrics_display(mo, select_year, timedelta, yearly_metrics):
    total_miles_value = "{:,.2f}".format(yearly_metrics[select_year.value]["distance_miles"][0])

    avg_run_pace_value_timedelta = yearly_metrics[select_year.value]["mins_per_mile"][0]
    avg_run_pace_value = yearly_metrics[select_year.value]["mins_per_mile"][0] - timedelta(microseconds=avg_run_pace_value_timedelta.microseconds)

    no_of_races_ran_value = yearly_metrics[select_year.value]["no_of_races"][0]
    no_of_race_miles_ran_value = "{:,.2f}".format(yearly_metrics[select_year.value]["race_miles"][0])

    # Debug - This value needs to have the microseconds sliced off of it so that it displays as 00:00 /mile
    avg_race_pace_value = yearly_metrics[select_year.value]["official_pace"][0]

    total_miles_stat = mo.stat(
        label="Total Miles",
        bordered=True,
        value=f"{total_miles_value} miles"
    )

    avg_run_pace_stat = mo.stat(
        label="Average Run Pace",
        bordered=True,
        value=f"{avg_run_pace_value}/mile"
    )

    no_of_races_ran_stat = mo.stat(
        label="No. of Races Ran",
        bordered=True,
        value=f"{no_of_races_ran_value} races"
    )

    no_of_race_miles_ran_stat = mo.stat(
        label="No. of Race Miles Ran",
        bordered=True,
        value=f"{no_of_race_miles_ran_value} miles"
    )

    avg_race_pace_stat = mo.stat(
        label="Average Race Pace",
        bordered=True,
        value=f"{avg_race_pace_value}/mile"
    )
    mo.hstack(
        [
            total_miles_stat,
            avg_run_pace_stat,
            no_of_races_ran_stat,
            no_of_race_miles_ran_stat,
            avg_race_pace_stat
        ],
        widths="equal",
        gap=1
    )
    return (
        avg_race_pace_stat,
        avg_race_pace_value,
        avg_run_pace_stat,
        avg_run_pace_value,
        avg_run_pace_value_timedelta,
        no_of_race_miles_ran_stat,
        no_of_race_miles_ran_value,
        no_of_races_ran_stat,
        no_of_races_ran_value,
        total_miles_stat,
        total_miles_value,
    )


@app.cell(hide_code=True)
def _(alt, df_runs, mo, pl, select_year):
    _df = (
        df_runs
        .filter(
            (pl.col("is_race") == False) & 
            (pl.col("date").dt.year() == select_year.value)
        )
        .select("date", "time_in_secs", "distance_miles", "secs_per_mile")
    )

    _input = df_runs.filter(pl.col("date").dt.year() == select_year.value).select("date", "distance_miles")

    _bar_chart = alt.Chart(data=_input).mark_bar().encode(
        x='date',
        y='distance_miles'
    )

    mo.hstack(
        [
            _df,
            _bar_chart
        ],
        widths="equal",
        gap=1
    )
    return


@app.cell(hide_code=True)
def _(df_runs_import, pl):
    df_runs = (
        df_runs_import
        .with_columns(
            (pl.col("distance") * 0.000621371).round(2).alias("distance_miles"), # meters to miles
            pl.col("elapsed_time").alias("time_in_secs"),
            (pl.col("total_elevation_gain") * 3.28084).round(2).alias("total_elev_gain_ft"), # meters to feet
            (pl.col("elev_high") * 3.28084).round(2).alias("elev_high_ft"), # meters to feet
            (pl.col("elev_low") * 3.28084).round(2).alias("elev_low_ft"), # meters to feet
            ((26.8224/pl.col("average_speed")) * 60).alias("secs_per_mile"),
            pl.when(pl.col("external_id").str.contains("garmin"))
                .then(pl.lit("Recorded w/ Garmin GPS"))
                .otherwise(pl.lit("Not Recorded w/Garmin GPS"))
                .alias("tracking_method"),
            pl.col("start_date").cast(pl.Date).alias("date"),
            pl.when(pl.col("workout_type") == 1).then(True).otherwise(False).alias("is_race"),
            pl.when(pl.col("workout_type") == 1).then(pl.col("name")).otherwise(None)
        )
        .select(
            "id",
            "name",
            "is_race",
            "date",
            "time_in_secs",
            "distance_miles",
            "secs_per_mile",
            "total_elev_gain_ft",
            "elev_low_ft",
            "elev_high_ft",
            "average_cadence",
            "average_heartrate",
            "max_heartrate",
            "workout_type",
            "gear_id",
            "tracking_method"
        )
    )
    return (df_runs,)


@app.cell(hide_code=True)
def strava_import(client, pl):
    _data = []
    for activity in client.get_activities(after="2021-12-31"):
        _dict = {
            "name": activity.name,
            "distance": activity.distance,
            "elapsed_time": activity.elapsed_time,
            "total_elevation_gain": activity.total_elevation_gain,
            "type": activity.sport_type.root,
            "workout_type": activity.workout_type,
            "id": activity.id,
            "start_date": activity.start_date_local,
            "gear_id": activity.gear_id,
            "average_speed": activity.average_speed,
            "average_cadence": activity.average_cadence,
            "average_heartrate": activity.average_heartrate,
            "max_heartrate": activity.max_heartrate,
            "elev_high": activity.elev_high,
            "elev_low": activity.elev_low,
            "external_id": activity.external_id,
        }

        _data.append(_dict)

    df_runs_import = pl.DataFrame(_data).filter(pl.col("type") == "Run").drop("type")
    df_rides_import = pl.DataFrame(_data).filter(pl.col("type") == "Ride").drop("type")
    return activity, df_rides_import, df_runs_import


@app.cell(hide_code=True)
def race_history_via_google_sheets(gspread, pl):
    _gc = gspread.service_account("./service_account.json")
    _sh = _gc.open("Race History")
    _worksheet = _sh.sheet1

    official_race_results_df_import = pl.DataFrame(_worksheet.get_all_records()).with_columns(pl.col("date").str.to_date())

    race_schedule = official_race_results_df_import.filter(pl.col("official_time").is_null())
    official_race_results_df = official_race_results_df_import.filter(pl.col("official_time").is_not_null())
    return (
        official_race_results_df,
        official_race_results_df_import,
        race_schedule,
    )


@app.cell
def yearly_metrics_generation(
    datetime,
    df_runs,
    get_avg_race_pace,
    get_avg_run_pace,
    get_no_of_races,
    get_race_miles,
    get_total_miles,
    official_race_results_df,
):
    yearly_metrics = dict.fromkeys(range(2022, datetime.today().year + 1))

    for year in range(2022, datetime.today().year + 1):    
        _output_total_miles = get_total_miles(df=df_runs, year=year)
        _output_avg_run_pace = get_avg_run_pace(df=df_runs, year=year)
        _output_no_of_races = get_no_of_races(df=official_race_results_df, year=year)
        _output_race_miles = get_race_miles(df=official_race_results_df, year=year)
        _output_avg_race_pace = get_avg_race_pace(df=official_race_results_df, year=year)

        yearly_metrics[year] = _output_total_miles | _output_avg_run_pace | _output_no_of_races | _output_race_miles | _output_avg_race_pace
    return year, yearly_metrics


@app.cell
def _(df_runs):
    df_runs
    return


if __name__ == "__main__":
    app.run()
