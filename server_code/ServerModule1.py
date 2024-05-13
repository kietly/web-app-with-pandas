import anvil.files
from anvil.files import data_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import pandas as pd

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
  netflix_df = netflix_df.drop_na(subset=['country'])

@anvil.server.callable
def explore():
  pd.set_option('display.width', 0)
  netflix_df = csv_to_df('netflix_titles.csv')
  print(netflix_df.head())