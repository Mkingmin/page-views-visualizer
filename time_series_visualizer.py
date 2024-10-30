import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv', index_col='date')

# Clean data
df.index = pd.to_datetime(df.index)

df = df[(df['value'] <= df['value'].quantile(0.975)) &
        (df['value'] >= df['value'].quantile(0.025))]


def draw_line_plot():
    # Draw line plot
    fig, ax = plt.subplots(figsize=(15, 6))
    ax.plot(df.index, df['value'], color='r')
    plt.xlabel('Date')
    plt.ylabel('Page Views')
    plt.title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')


    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()
    df_bar['year'] = df_bar.index.year
    df_bar['month'] = df_bar.index.month_name()
    month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    # set the order of month column
    # Use pd.Categorical instead of pd.Categories
    df_bar['month'] = pd.Categorical(df_bar['month'], categories=month_order, ordered=True) 
    # calculate the average page views by month
    # Assuming 'sort_vaues' should be 'sort_values'
    df_bar = df_bar.groupby(['year', 'month'])['value'].mean().reset_index().sort_values(['year', 'month'])
    # fillnan values
    df_bar['value'] = df_bar['value'].fillna(0)
    # create bar chart
    fig, ax = plt.subplots(figsize=(10, 8))
    # Assuming 'patlette' should be 'palette'
    chart = sns.barplot(data=df_bar, x='year', y='value', hue='month', palette='tab10') 
    plt.xlabel('Years')
    plt.ylabel('Average Page Views')
    plt.legend(title= 'Month')


    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Draw box plots (using Seaborn)
    fig, ax = plt.subplots(1, 2, figsize=(20, 10))
    # year boxplot
    sns.boxplot(x=df_box['year'], y=df_box['value'], ax=ax[0], hue=df_box['year'], palette='tab10')
    ax[0].set_title('Year-wise Box Plot (Trend)')
    ax[0].set_xlabel('Year')
    ax[0].set_ylabel('Page Views')
    # month boxplot
    month_order=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    df_box['month'] = pd.Categorical(df_box['month'], categories=month_order, ordered=True)
    sns.boxplot(x=df_box['month'], y=df_box['value'], ax=ax[1], hue=df_box['month'] , palette='tab10')
    ax[1].set_title('Month-wise Box Plot (Seasonality)')
    ax[1].set_xlabel('Month')
    ax[1].set_ylabel('Page Views')



    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
