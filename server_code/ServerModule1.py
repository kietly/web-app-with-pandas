import anvil.files
from anvil.files import data_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import pandas as pd
import plotly.graph_objects as go

# This is a server module. It runs on the Anvil server,
# rather than in the user's browser.
#
# To allow anvil.server.call() to call functions here, we mark
# them with @anvil.server.callable.
# Here is an example - you can replace it with your own:
#
# @anvil.server.callable
# def say_hello(name):
#   print("Hello, " + name + "!")
#   return 42
#

def csv_to_df(f):
  df = pd.read_csv(data_files[f], index_col=0)
  return df

def prepare_netflix_data():
  netflix_df = csv_to_df('netflix_titles.csv')
  netflix_df = netflix_df.loc[:,['type', 'country', 'date_added']]
  netflix_df = netflix_df.dropna(subset=['country'])
  netflix_df['country'] = [countries[0] for countries in netflix_df['country'].str.split(',')]
  country_counts = pd.DataFrame(netflix_df['country']
                                .value_counts()
                                .rename_axis('countries')
                                .reset_index(name='counts')).sort_values(by=['countries'])
  netflix_df['date_added'] = pd.to_datetime(netflix_df['date_added'],format='mixed')
  return netflix_df, country_counts
                
@anvil.server.callable
def explore():
  pd.set_option('display.width', 0)
  netflix_df = csv_to_df('netflix_titles.csv')
  print(prepare_netflix_data())

@anvil.server.callable
def create_plots():
  netflix_df, country_counts = prepare_netflix_data()
  fig1 = go.Figure(
      go.Scattergeo(
      locations=sorted(netflix_df['country'].unique().tolist()), 
      locationmode='country names',  
      text = country_counts['counts'],
      marker= dict(
        size= country_counts['counts'],
        line_width = 0,
        sizeref = 2,
        sizemode = 'area',
        color='#D90707' # Making the map bubbles red
      ))
  )
  
  fig2 = go.Figure(go.Pie(
    labels=netflix_df['type'], 
    values=netflix_df['type'].value_counts(),
    marker=dict(colors=['#D90707', '#A60311']), # Making the pie chart two different shades of red
    hole=.4, # Adding a hole to the middle of the chart
    textposition= 'inside', 
    textinfo='percent+label'
  ))
  
  fig3 = go.Figure(
    go.Scatter(
      x=netflix_df['date_added'].dt.year.value_counts().sort_index().index, 
      y=netflix_df['date_added'].dt.year.value_counts().sort_index(),
      line=dict(color='#D90707', width=3) # Making the line red
    ))

  fig1.update_layout(
  title='Production countries',
  font=dict(family='Raleway', color='white'), # Customizing the font
  margin=dict(t=60, b=30, l=0, r=0), # Changing the margin sizes of the figure
  paper_bgcolor='#363636', # Setting the card color to grey
  plot_bgcolor='#363636', # Setting background of the figure to grey
  hoverlabel=dict(font_size=14, font_family='Raleway'),
  geo=dict(
    framecolor='rgba(0,0,0,0)',
    bgcolor='rgba(0,0,0,0)',
    landcolor='#7D7D7D',
    lakecolor = 'rgba(0,0,0,0)',))

  fig2.update_layout(
  title='Content breakdown by type',
  margin=dict(t=60, b=30, l=10, r=10),
  showlegend=False,
  paper_bgcolor='#363636',
  plot_bgcolor='#363636',
  font=dict(family='Raleway', color='white'))

  fig3.update_layout(
  title='Content added over time',
  margin=dict(t=60, b=40, l=50, r=50),
  paper_bgcolor='#363636',
  plot_bgcolor='#363636',
  font=dict(family='Raleway', color='white'),
  hoverlabel=dict(font_size=14, font_family='Raleway'))

  return fig1, fig2, fig3