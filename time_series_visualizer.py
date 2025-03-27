import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv("/workspace/boilerplate-page-view-time-series-visualizer/fcc-forum-pageviews.csv", parse_dates=['date'], index_col='date')

# Clean data by filtering out days in the top and bottom 2.5% of the dataset
lower_limit = df["value"].quantile(0.025)
upper_limit = df["value"].quantile(0.975)
df = df[(df["value"] >= lower_limit) & (df["value"] <= upper_limit)]

def draw_line_plot():
    # Create a copy of the DataFrame for plotting the line plot
    df_line = df.copy()
    
    # Draw line plot
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(df_line.index, df_line['value'], color='b', linewidth=1)
    
    # Customize the plot
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Read the data and parse 'date' as datetime
    df = pd.read_csv("/workspace/boilerplate-page-view-time-series-visualizer/fcc-forum-pageviews.csv", parse_dates=['date'])

    # Check column names to ensure 'date' exists
    print(df.columns)  # Print the column names to see if 'date' is available

    # Copy the data to avoid modifying the original DataFrame
    df_bar = df.copy()

    # Ensure 'date' column is parsed as datetime
    if 'date' not in df_bar.columns:
        raise KeyError("The 'date' column is missing in the data!")

    # Extract year and month from the 'date' column
    df_bar['year'] = df_bar['date'].dt.year
    df_bar['month'] = df_bar['date'].dt.month

    # Set the correct month order using CategoricalDtype
    month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    df_bar['month'] = pd.Categorical(df_bar['month'], categories=range(1, 13), ordered=True)
    df_bar['month'] = df_bar['month'].apply(lambda x: month_order[x-1])  # Convert numeric to month name

    # Group by year and month and calculate the average value for each month
    df_grouped = df_bar.groupby(['year', 'month'])['value'].mean().unstack()

    # Plot the bar plot
    fig, ax = plt.subplots(figsize=(12, 6))
    df_grouped.plot(kind='bar', ax=ax)

    # Add labels and title
    ax.set_xlabel('Years')
    ax.set_ylabel('Average Page Views')
    ax.set_title('Average Daily Page Views for Each Month Grouped by Year')

    # Set the legend with proper title and order
    ax.legend(title="Months", labels=month_order)

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = df_box['date'].dt.year
    df_box['month'] = df_box['date'].dt.strftime('%b')

    # Draw box plots using Seaborn
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

    # Year-wise box plot
    sns.boxplot(x='year', y='value', data=df_box, ax=ax1)
    ax1.set_title('Year-wise Box Plot (Trend)')
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Page Views')

    # Month-wise box plot
    sns.boxplot(x='month', y='value', data=df_box, ax=ax2, order=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
    ax2.set_title('Month-wise Box Plot (Seasonality)')
    ax2.set_xlabel('Month')
    ax2.set_ylabel('Page Views')

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
