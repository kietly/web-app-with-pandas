from ._anvil_designer import Form1Template
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import plotly.graph_objects as go


class Form1(Form1Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    fig1,fig2,fig3 = anvil.server.call('create_plots')
    self.plot_1.figure = fig1
    self.plot_2.figure = fig2
    self.plot_3.figure = fig3