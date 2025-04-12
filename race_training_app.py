# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "beautifulsoup4==4.13.3",
#     "datetime==5.5",
#     "marimo",
#     "polars==1.26.0",
#     "requests==2.32.3",
#     "selenium==4.30.0",
# ]
# ///

import marimo

__generated_with = "0.12.8"
app = marimo.App(width="medium", app_title="Race Training App")


@app.cell
def _(mo):
    mo.md("""# Generate a Hal Higdon Training Plan""")
    return


@app.cell
def _(mo):
    mo.md(r"""***""")
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        Hal Higdon has great training plans for all distances and levels available for free on his website. However, the plans cannot be tailored to specific dates, which means you spend time reverse mapping the training plan to your calendar. I always find this to be a headache and prone to being off by a day or week.

        That's why I created this handy training plan generator. All you need to do is select a race distance, the training level, and the date of the race. That's it! The app will generate the plan with the dates all lined up and ready for you to start training!
        """
    )
    return


@app.cell
def _(input_race_date, input_race_distance, input_training_level, mo):
    mo.hstack(
        [
            input_race_distance,
            input_training_level,
            input_race_date
        ]
    ).callout("info")
    return


@app.cell
def _(df):
    df
    return


@app.cell
def ui_dropdown_race_distance(hh_training_plans, mo):
    input_race_distance = mo.ui.dropdown(
        options=hh_training_plans.keys(),
        value="5K",
        label="Select a Race Distance",
        full_width=True)
    return (input_race_distance,)


@app.cell
def ui_dropdown_training_level(fetch_training_levels, input_race_distance, mo):
    input_training_level = mo.ui.dropdown(
        options=fetch_training_levels(input_race_distance.value),
        label="Select a Training Level",
        full_width=True)
    return (input_training_level,)


@app.cell
def ui_race_date(mo):
    input_race_date = mo.ui.date(label="Select the Race Date", full_width=True)
    return (input_race_date,)


@app.cell
def _(
    generate_training_plan,
    input_race_date,
    input_race_distance,
    input_training_level,
):
    df = generate_training_plan(
        distance=input_race_distance.value,
        level=input_training_level.value,
        race_date=input_race_date.value,
        on_sunday=True)
    return (df,)


@app.cell
def modules_import():
    from datetime import datetime, timedelta
    import marimo as mo
    import polars as pl
    import requests
    from bs4 import BeautifulSoup
    from selenium import webdriver
    return BeautifulSoup, datetime, mo, pl, requests, timedelta, webdriver


@app.cell(hide_code=True)
def extract_browser_info(webdriver):
    driver = webdriver.Safari()
    user_agent = driver.execute_script("return navigator.userAgent;")
    driver.quit()
    return driver, user_agent


@app.cell(hide_code=True)
def training_plans_dictionary():
    hh_training_plans = {
        '5K': {
            'Novice': {
                "no_of_weeks": 8,
                "url": 'https://www.halhigdon.com/training-programs/5k-training/novice-5k/'
            },
            'Intermediate': {
                "no_of_weeks": 8,
                "url": 'https://www.halhigdon.com/training-programs/5k-training/intermediate-5k/'
            },
            'Advanced': {
                "no_of_weeks": 8,
                "url": 'https://www.halhigdon.com/training-programs/5k-training/advanced-5k/'
            },
            'Walkers': {
                "no_of_weeks": 8,
                "url": 'https://www.halhigdon.com/training-programs/5k-training/walkers-5k/'
            }
        },
        '8K': {
            'Novice': {
                "no_of_weeks": 8,
                "url": 'https://www.halhigdon.com/training-programs/8k-training/novice-8k/'
            },
            'Intermediate': {
                "no_of_weeks": 8,
                "url": 'https://www.halhigdon.com/training-programs/8k-training/intermediate-8k/'
            },
            'Advanced': {
                "no_of_weeks": 8,
                "url": 'https://www.halhigdon.com/training-programs/8k-training/advanced-8k/'
            }
        },
        '10K': {
            'Novice': {
                "no_of_weeks": 8,
                "url": 'https://www.halhigdon.com/training-programs/10k-training/novice-10k/'
            },
            'Intermediate': {
                "no_of_weeks": 8,
                "url": 'https://www.halhigdon.com/training-programs/10k-training/intermediate-10k/'
            },
            'Advanced': {
                "no_of_weeks": 8,
                "url": 'https://www.halhigdon.com/training-programs/10k-training/advanced-10k/'
            }
        },
        '15K / 10 Miler': {
            'Novice': {
                "no_of_weeks": 10,
                "url": 'https://www.halhigdon.com/training-programs/15k-10-mile-training/novice-15k-10-mile/'
            },
            'Intermediate': {
                "no_of_weeks": 10,
                "url": 'https://www.halhigdon.com/training-programs/15k-10-mile-training/intermediate-15k-10-mile/'
            },
            'Advanced': {
                "no_of_weeks": 10,
                "url": 'https://www.halhigdon.com/training-programs/15k-10-mile-training/advanced-15k-10-mile/'
            }
        },
        'Half-Marathon': {
            'Novice 1': {
                "no_of_weeks": 12,
                "url": 'https://www.halhigdon.com/training-programs/half-marathon-training/novice-1-half-marathon/'
            },
            'Novice 2': {
                "no_of_weeks": 12,
                "url": 'https://www.halhigdon.com/training-programs/half-marathon-training/novice-2-half-marathon/'
            },
            'Intermediate 1': {
                "no_of_weeks": 12,
                "url": 'https://www.halhigdon.com/training-programs/half-marathon-training/intermediate-1-half-marathon/'
            },
            'Intermediate 2': {
                "no_of_weeks": 12,
                "url": 'https://www.halhigdon.com/training-programs/half-marathon-training/intermediate-2-half-marathon/'
            },
            'Advanced': {
                "no_of_weeks": 12,
                "url": 'https://www.halhigdon.com/training-programs/half-marathon-training/advanced-half-marathon/'
            },
            'Half Marathon 3': {
                "no_of_weeks": 12,
                "url": 'https://www.halhigdon.com/training-programs/half-marathon-training/half-marathon-3/'
            },
            'Walkers': {
                "no_of_weeks": 12,
                "url": 'https://www.halhigdon.com/training-programs/half-marathon-training/walkers-half-marathon/'
            }
        },
        'Marathon': {
            'Novice 1': {
                "no_of_weeks": 18,
                "url": 'https://www.halhigdon.com/training-programs/marathon-training/novice-1-marathon/'
            },
            'Novice 2': {
                "no_of_weeks": 18,
                "url": 'https://www.halhigdon.com/training-programs/marathon-training/novice-1-marathon/'
            },
            'Intermediate 1': {
                "no_of_weeks": 18,
                "url": 'https://www.halhigdon.com/training-programs/marathon-training/intermediate-1-marathon/'
            },
            'Intermediate 2': {
                "no_of_weeks": 18,
                "url": 'https://www.halhigdon.com/training-programs/marathon-training/intermediate-2-marathon/'
            },
            'Advanced 1': {
                "no_of_weeks": 18,
                "url": 'https://www.halhigdon.com/training-programs/marathon-training/advanced-1-marathon/'
            },
            'Advanced 2': {
                "no_of_weeks": 18,
                "url": 'https://www.halhigdon.com/training-programs/marathon-training/advanced-2-marathon/'
            },
            'Novice Supreme': {
                "no_of_weeks": 30,
                "url": 'https://www.halhigdon.com/training-programs/marathon-training/novice-supreme/'
            },
            'Personal Best': {
                "no_of_weeks": 30,
                "url": 'https://www.halhigdon.com/training-programs/marathon-training/personal-best/'
            },
            'Senior': {
                "no_of_weeks": 8,
                "url": 'https://www.halhigdon.com/training-programs/marathon-training/senior/'
            },
            'Marathon 3': {
                "no_of_weeks": 24,
                "url": 'https://www.halhigdon.com/training-programs/marathon-training/marathon-3/'
            },
            #'Boston Bound': 'https://www.halhigdon.com/training-programs/marathon-training/boston-bound/',
            #'Multiple Marathons': 'https://www.halhigdon.com/training-programs/marathon-training/multiple-marathons/',
            #'Alternate Marathon': 'https://www.halhigdon.com/training-programs/marathon-training/alternate-marathon-program/',
            'Dopey Challenge': {
                "no_of_weeks": 18,
                "url": 'https://www.halhigdon.com/training-programs/marathon-training/dopey-challenge/'
            }
        }
    }
    return (hh_training_plans,)


@app.cell
def functions(
    BeautifulSoup,
    hh_training_plans,
    pl,
    requests,
    timedelta,
    user_agent,
):
    def generate_training_plan(distance, level, race_date, on_sunday=True):
        url = hh_training_plans[distance][level]["url"]
        weeks = hh_training_plans[distance][level]["no_of_weeks"]
        headers = {"User-Agent": user_agent}
        req = requests.get(url=url, headers=headers)
        soup = BeautifulSoup(req.text, 'html.parser')
        table = soup.find('table', class_ = 'tablesaw')

        for data in table.find_all('tbody'):
            rows = data.find_all('tr')

        weekly_schedules = []

        for row in rows:
            week = row.find_all('td')[0].text
            monday = row.find_all('td')[1].text
            tuesday = row.find_all('td')[2].text
            wednesday = row.find_all('td')[3].text
            thursday = row.find_all('td')[4].text
            friday = row.find_all('td')[5].text
            saturday = row.find_all('td')[6].text
            sunday = row.find_all('td')[7].text
            result = {
                "Week": week,
                "Monday": monday,
                "Tuesday": tuesday,
                "Wednesday": wednesday,
                "Thursday": thursday,
                "Friday": friday,
                "Saturday": saturday,
                "Sunday": sunday
            }

            weekly_schedules.append(result)

        df = pl.DataFrame(weekly_schedules)
        df = df.with_columns(pl.col("Week").cast(pl.Int32).alias("week")).drop("Week")
        df = df.unpivot(index="week", variable_name="day_of_week", value_name="training").sort("week")

        end_date = race_date
        start_date = end_date - (timedelta(weeks=weeks) - timedelta(days=1))

        delta = end_date - start_date

        training_dates = []

        for i in range(delta.days + 1):
            day = start_date + timedelta(days=i)
            training_dates.append(day)

        dates_df = pl.Series(name="date", values=training_dates).to_frame().with_columns(pl.col("date").dt.date())
        final_df = pl.concat([dates_df, df], how="horizontal")

        return final_df

    def fetch_training_levels(distance):
        return hh_training_plans[distance].keys()
    return fetch_training_levels, generate_training_plan


if __name__ == "__main__":
    app.run()
