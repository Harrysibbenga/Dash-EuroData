import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

# Initialize App
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

pd.options.plotting.backend = "plotly"

df = pd.read_csv('european_turnout.csv')

years_list = df['year']

app.layout = html.Div([

    # Create Graph object
    html.Div([
        dcc.Graph(id='my_graph'),
        # Create Dropdown Menu (Store Type)
        dcc.Dropdown(
            id='my_dropdown',
            options=[
             {'label': 'Western', 'value': 'Western'},
             {'label': 'Central/Eastern', 'value': 'Central/Eastern'},
             {'label': 'All Regions', 'value': 'All Regions'}
             ],
            value='Region Filter',
            multi=False,
            clearable=False,
            style={"width": "50%"}
        ),
        # # Create Range Slider (Year)
        dcc.RangeSlider(
            id='my-range-slider',
            min=df['year'].min(),
            max=df['year'].max(),
            step=1,
            value=[2014, 2019],
            dots=True,
            allowCross=False,
            marks={
                str(year): {
                    'label': str(year),
                    'style': {'color': '#7fafdf'}
                }
                for year in years_list
            }
        ),
        html.Div(id='output-container-range-slider')
    ])
])

# Callback


@app.callback(
    Output('my_graph', 'figure'),
    [Input('my-range-slider', 'value'),
     Input(component_id='my_dropdown', component_property='value')]
)
# Update Graph Based on Slider & Dropdown
def build_graph(years, dd_selection):
    # # Filter Based on Year
    df_filtered = df.loc[df['year'] > years[0]]
    df_filtered = df_filtered.loc[df['year'] < years[1]]
    # Separate DataFrames for Different Store Types
    df_western = df_filtered.loc[df_filtered['region'] == 'Western']
    df_central_west = df_filtered.loc[df_filtered['region']
                                      == 'Central/Eastern']

    title_brand = ''

    if dd_selection == 'Western':
        fig = px.scatter_geo(df_western,
                             locations="country",
                             locationmode="country names",
                             color="region",  # which column to use to set the color of markers
                             hover_name="country",  # column added to hover information
                             size="population",  # size of markers
                             projection="natural earth",
                             title=title_brand)
        title_brand = 'Western'
    elif dd_selection == 'Central/Eastern':
        fig = px.scatter_geo(df_central_west,
                             locations="country",
                             locationmode="country names",
                             color="region",  # which column to use to set the color of markers
                             hover_name="country",  # column added to hover information
                             size="population",  # size of markers
                             projection="natural earth",
                             title=title_brand)
        title_brand = 'Central/Eastern'
    else:
        fig = px.scatter_geo(df_filtered,
                             locations="country",
                             locationmode="country names",
                             color="region",
                             hover_name="country",
                             size="population",
                             projection="natural earth",
                             title=title_brand)
        title_brand = 'All Regions'

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
