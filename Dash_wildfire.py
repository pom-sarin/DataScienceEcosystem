import pandas as pd 
import dash
from dash import html, dcc 
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go 
import plotly.express as px 
from dash import no_update
import datetime as dt 

#Create app
app = dash.Dash(__name__)

#Clear the layout and do not display exception till callback gets executed
app.config.suppress_callback_exceptions = True

#Read the wildfire data into pandas dataframe
df = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/Historical_Wildfires.csv')

#Extract year and month from the date column
df['Month'] = pd.to_datetime(df["Date"]).dt.month_name() #used for the names of the months
df['Year'] = pd.to_datetime(df['Date']).dt.year

#Layout section of Dash

app.layout = html.Div(children=[html.H1('Australian Wildfire Dashboard',
                                            style={'textAlign':'center', 'color':'#503D36','font-size':26}),
                                html.Div([
                                    html.Div([
                                        html.H2('Select Region:', style={'margin-right':'2em'}),
                                        dcc.RadioItems([{'label':'New South Wales','value':'NSW'},
                                                        {'label':'Nothern Territory','value':'NT'},
                                                        {'label':'Queensland','value':'QL'},
                                                        {'label':'South Australia','value':'SA'},
                                                        {'label':'Tasmania','value':'TA'},
                                                        {'label':'Victoria','value':'VI'},
                                                        {'label':'Western Australia','value':'WA'}],
                                                        value = 'NSW', id='region',inline=True)
                                    ]),
                                    html.Div([
                                        html.H2('Select Year:', style={'margin-right':'2em'}),
                                        dcc.Dropdown(df.Year.unique(),value=2005,id='year')
                                    ]),
                                    html.Div([
                                        html.Div([],id='plot1'),
                                        html.Div([],id='plot2')
                                    ], style={'display':'flex'})
                                ])
                        ])

#Add the Ouput and input components inside the app.callback decorator.
@app.callback([Output(component_id='plot1',component_property='children'),
               Output(component_id='plot2',component_property='children')],
               [Input(component_id='region',component_property='value'),
               Input(component_id='year',component_property='value')])

#Add the callback function.
def reg_year_display(input_region,input_year):
    region_data = df[df['Region'] == input_region]
    y_r_data = region_data[region_data['Year']==input_year]

    #plot one - Monthly Average Estimated Fire Area
    est_data = y_r_data.groupby('Month')['Estimated_fire_area'].mean().reset_index()
    fig1 = px.pie(est_data,values='Estimated_fire_area',names='Month', title="{} : Monthly Average Estimated Fire Area in year {}".format(input_region,input_year))

    #plot two - Monthly Average Count of Pixels for Presumed Vegetation Fires
    veg_data = y_r_data.groupby('Month')['Count'].mean().reset_index()
    fig2 = px.bar(veg_data,x='Month',y='Count',title='{} : Average Count of Pixels for Presumed Vegetation Fires in year {}'.format(input_region,input_year))

    return[dcc.Graph(figure=fig1),
            dcc.Graph(figure=fig2)]

if __name__ == '__main__':
    app.run()