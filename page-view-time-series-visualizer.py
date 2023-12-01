import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters

register_matplotlib_converters()

# Import data
df = pd.read_csv("fcc-forum-pageviews.csv", index_col="date", parse_dates=True)

# Clean data
df = df.sort_values(by="value", ascending=False)
df = df[(df.value < df.value.quantile(0.975)) & (df.value > df.value.quantile(0.025))]
df = df.sort_values(by="date")


def draw_line_plot():
    # Draw line plot
    dates = df.index
    page_views = df["value"]

    font = {"size": 13}
    fig = plt.figure(figsize=(20, 6.3))

    plt.rc("font", **font)
    plt.plot(dates, page_views, color="red")
    plt.xlabel("Date")
    plt.ylabel("Page Views")
    plt.title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")

    # Save image and return fig
    fig.savefig("line_plot.png")
    return fig


def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()
    df_bar["year"] = df_bar.index.year
    df_bar["month"] = df_bar.index.month
    df_bar.reset_index(inplace=True)
    df_bar = df_bar.groupby(["year", "month"])["value"].mean()
    df_bar = df_bar.unstack()

    # Draw bar plot
    fig = df_bar.plot(kind="bar", figsize=(9, 8)).figure
    plt.xlabel("Years")
    plt.ylabel("Average Page Views")
    plt.xticks(rotation=90)
    plt.legend(
        title="Months",
        loc="upper left",
        labels=[
            "January",
            "February",
            "March",
            "April",
            "May",
            "June",
            "July",
            "August",
            "September",
            "October",
            "November",
            "December",
        ],
    )

    # Save image and return fig
    fig.savefig("bar_plot.png")
    return fig


def draw_box_plot():
    # Prepare data for box plots
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box["year"] = [d.year for d in df_box.date]
    df_box["month"] = [d.strftime("%b") for d in df_box.date]

    # Draw box plots
    fig, axes = plt.subplots(1, 2, figsize=(20, 8))
    plt.subplots_adjust(wspace=0.3)

    sns.boxplot(
        ax=axes[0],
        x="year",
        y="value",
        hue="year",
        legend=False,
        palette="tab10",
        data=df_box,
    )
    axes[0].set_title("Year-wise Box Plot (Trend)")
    axes[0].set_xlabel("Year")
    axes[0].set_ylabel("Page Views")

    sns.boxplot(
        ax=axes[1],
        x="month",
        y="value",
        hue="month",
        order=[
            "Jan",
            "Feb",
            "Mar",
            "Apr",
            "May",
            "Jun",
            "Jul",
            "Aug",
            "Sep",
            "Oct",
            "Nov",
            "Dec",
        ],
        width=0.7,
        data=df_box,
    )
    axes[1].set_title("Month-wise Box Plot (Seasonality)")
    axes[1].set_xlabel("Month")
    axes[1].set_ylabel("Page Views")

    # Save image and return fig
    fig.savefig("box_plot.png")
    return fig
