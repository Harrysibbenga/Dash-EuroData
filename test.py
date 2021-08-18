import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px


pd.options.plotting.backend = "plotly"

df = pd.read_csv('european_turnout.csv')

fig = px.scatter_geo(df,
                     locations="country",
                     locationmode="country names",
                     color="region",  # which column to use to set the color of markers
                     hover_name="country",  # column added to hover information
                     size="population",  # size of markers
                     projection="natural earth")
fig.show()

if __name__ == '__main__':
    app.run_server(debug=True)
