import dash
#import dash_core_components as dcc
from dash import dcc
#import dash_html_components as html
from dash import html
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
import numpy as np
import geopandas as gpd
from shapely.geometry import Point, LineString, Polygon, box, MultiPolygon
from pyproj import CRS, crs
import json
import warnings
warnings.filterwarnings('ignore')

app = dash.Dash()

df = pd.read_csv('../data/01x01.csv')

list_time = list(dict.fromkeys(list((df.Time))))

#colors = {'bg':'#9cb5ff',
#         'elem_bg':'#789aff',
#         'letter':'#ffffff'}
colors = {'bg':'#000000',
         'elem_bg':'#2e2e2e',
         'letter':'#ffffff'}
font = {'family':'system-ui'}
#
#app = dash.Dash(
 #   __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}]
#)
server = app.server
app.title = 'Meteo-Panama'
#app.config.suppress_callback_exceptions = True
#
#app = dash.Dash(show_undo_redo=False)
mapbox_access_token = 'pk.eyJ1IjoibWFydGFub2luZXJjaWFsIiwiYSI6ImNrdXdwNXRxczJydWkydnFydWhuZTAybTMifQ.dTpq64f-nPO3L1GLmla9Aw'
px.set_mapbox_access_token(mapbox_access_token)

app.layout = html.Div(
    children=[
        html.Div(
            className="row",
            children=[
                html.Div(
                    id='title',
                    children= [
                        html.Img(src="https://theweatherpartner.com/wp-content/uploads/2021/01/logo-twp-nw.png",
                                style={
                                    "position":'absolute',
                                    'top':'2%',
                                    'left':'1%',
                                    'width':'90px',
                                    'height':'90px'
                                }
                                ),
                        html.H1("Pronostico meteorologico de la Cuenca 102"),
                        html.Img(src="https://www.hidromet.com.pa/images/logo_etesa_hidromet.png",
                                style={
                                    "position":'absolute',
                                    'top':'2%',
                                    'right':'1%',
                                    'width':'250px',
                                    'height':'90px'
                                })
                    ],
                    style={'outline-color':colors['bg'],
                           'outline-style':'solid',
                           'display':'inline-block',
                         #  'width':'23%',
                           'width':'98%',
                           'height':'23%',
                           'backgroundColor':colors['elem_bg'],
                           'padding':'1%',
                           'outline-width':'5px',
                           'font-family':font['family'],
                           'color':colors['letter'],
                           'text-align':'center'}),
                html.Div(
                    className="two-main-columns",
                    children=[
                        html.Div(id='left-column',
                                 children=[
                                     html.Div(
                                         id='lat-lon-row',
                                         children=[
                                                 html.Div(
                                                        id='lat',
                                                        children=[html.H4('Latitude:'),
                                                                  html.H2('- º'),
                                                                 html.Br(),
                                                                 html.H4(' ')],
                                                        style={'outline-color':colors['bg'],
                                                               'outline-style':'solid',
                                                               'display':'inline-block',
                                                             #  'width':'23%',
                                                               'width':'48%',
                                                               'height':'23%',
                                                               'backgroundColor':colors['elem_bg'],
                                                               'padding':'1%',
                                                               'outline-width':'5px',
                                                               'font-family':font['family'],
                                                               'color':colors['letter'],
                                                               'text-align':'center'}),
                                                html.Div(id='lon',
                                                         children=[html.H4('Longitud:'),
                                                                   html.H2('- º'),
                                                                  html.Br(),
                                                                 html.H4('')],
                                                        style={'outline-color':colors['bg'],
                                                               'outline-style':'solid',
                                                               'display':'inline-block',
                                                          #     'width':'23%',
                                                               'width':'48%',
                                                               'height':'23%',
                                                               'backgroundColor':colors['elem_bg'],
                                                               'padding':'1%',
                                                               'outline-width':'5px',
                                                               'font-family':font['family'],
                                                               'color':colors['letter'],
                                                               'text-align':'center'}),
                                         ],
                                       #  style={},
                                     ),
                                     html.Div(
                                         id='map-row',
                                         children=[
                                             dcc.Graph(id='map',
                                                       figure = {
                                                           'data':[go.Scattermapbox(lat=df[df['Time']==list_time[-1]].Latitude,
                                                                lon=df[df['Time']==list_time[-1]].Longitude,
                                                                hoverinfo=["lon", "lat"], opacity=0.8,
                                                                mode = 'markers',
                                                                marker=go.Marker(
                                                                      #  size=5,
                                                                        color =df[df['Time']==list_time[-1]].PrecipitacionAcumulada,
                                                                        colorscale= 'PuBu',
                                                                        opacity=0.4,
                                                                        cmin=0,
                                                                        cmax=100,
                                                                        showscale=True,
                                                                        symbol = 'circle'))],
                                                          'layout':go.Layout(mapbox=dict(accesstoken=mapbox_access_token,
                                                                         center=dict(lat=8.5,lon=-82.5),
                                                                         zoom = 8),
                                                                             paper_bgcolor=colors['elem_bg'],
                                                                             plot_bgcolor=colors['elem_bg'])
                                      },style={'outline-color':colors['bg'],
                                               'outline-style':'solid',
                                               'display':'inline-block',
                                     #          'width':'48%',
                                               'width':'98%',
                                               'height':'78%',
                                               'backgroundColor':colors['elem_bg'],
                                               'padding':'1%',
                                               'outline-width':'5px',
                                              'font-family':font['family'],
                                               'color':colors['letter']})
                                         ],
                                 #        style={},
                                     ),
                                     html.Div(
                                         id='info-download-row',
                                         children=[
                                             html.Div(
                                                id='dadas',
                                                children=[html.H4('Datos del modelo:'),
                                                          html.H2('Hora UTC: 22-11-2021 00:00:00'),
                                                          html.Br(),
                                                          html.H4('')],
                                                style={'outline-color':colors['bg'],
                                                               'outline-style':'solid',
                                                               'display':'inline-block',
                                                               'min-height':'23%',
                                                            #   'width':'23%',
                                                               'backgroundColor':colors['elem_bg'],
                                                               'width':'48%',
                                                               'padding':'1%',
                                                               'outline-width':'5px',
                                                               'font-family':font['family'],
                                                               'color':colors['letter'],
                                                               'text-align':'center'}),
                                            html.Div(id='download',
                                                     children=[html.H4('Link de descarga'),
                                                               html.A(html.H2('Click para descargar los datos'),
                                                               href='https://theweatherpartner.xyz/martav/datadownload/5x5.csv'),
                                                               html.Br(),
                                                                 html.H4(' ')],
                                                     style={'outline-color':colors['bg'],
                                                               'outline-style':'solid',
                                                               'display':'inline-block',
                                                       #        'width':'23%',
                                                               'width':'48%',
                                                               'min-height':'23%',
                                                               'backgroundColor':colors['elem_bg'],
                                                               'padding':'1%',
                                                               'outline-width':'5px',
                                                               'font-family':font['family'],
                                                               'color':colors['letter'],
                                                               'text-align':'center'}),
                                         ],
                              #           style={},
                                     ),
                                 ],
                                style={
                                     'width':'50%',
                                     'display':'inline',
                                    'float':'left'
                                 }
                                ),
                        html.Div(id='right-column',
                                 children=[
                                     html.Div(
                                         id='indicators-first-row',
                                         children = [
                                                 html.Div(
                                                        id='precipMAX24',
                                                        children=[html.H4('Precipitacion acumulada:'),
                                                                  html.H2('-'),
                                                                  html.H4(' (l/m2) las proximas 24 horas')],
                                                        style={'outline-color':colors['bg'],
                                                               'outline-style':'solid',
                                                               'display':'inline-block',
                                                               'width':'48%',
                                                               'height':'23%',
                                                        #       'width':'23%',
                                                               'backgroundColor':colors['elem_bg'],
                                                               'padding':'1%',
                                                               'outline-width':'5px',
                                                               'font-family':font['family'],
                                                               'color':colors['letter'],
                                                               'text-align':'center'}),
                                                html.Div(id='intMAX24',
                                                         children=[html.H4('Intensidad maxima:'),
                                                                   html.H2('-'),
                                                                   html.H4(' (l/m2/min) las proximas 24 horas')],
                                                        style={'outline-color':colors['bg'],
                                                               'outline-style':'solid',
                                                               'display':'inline-block',
                                                               'width':'48%',
                                                               'height':'23%',
                                                          #     'width':'23%',
                                                               'backgroundColor':colors['elem_bg'],
                                                               'padding':'1%',
                                                               'outline-width':'5px',
                                                               'font-family':font['family'],
                                                               'color':colors['letter'],
                                                               'text-align':'center'})]),
                                         html.Div(
                                             id='indicators-second-row',
                                             children = [
                                                html.Div(id='precipMAX48',
                                                         children=[html.H4('Precipitacion acumulada:'),
                                                                   html.H2('-'),
                                                                   html.H4(' (l/m2) las proximas 24-48 horas')],
                                                        style={'outline-color':colors['bg'],
                                                               'outline-style':'solid',
                                                               'display':'inline-block',
                                                               'width':'48%',
                                                               'height':'23%',
                                                               'backgroundColor':colors['elem_bg'],
                                                               'padding':'1%',
                                                               'outline-width':'5px',
                                                               'font-family':font['family'],
                                                               'color':colors['letter'],
                                                               'text-align':'center'}),
                                                html.Div(id='intMAX48',
                                                         children=[html.H4('Intensidad maxima:'),
                                                                   html.H2('-'),
                                                                   html.H4(' (l/m2/min) las proximas 24-48 horas')],
                                                         style={'outline-color':colors['bg'],
                                                               'outline-style':'solid',
                                                               'display':'inline-block',
                                                                'width':'48%',
                                                               'height':'23%',
                                                               'backgroundColor':colors['elem_bg'],
                                                               'padding':'1%',
                                                               'outline-width':'5px',
                                                               'font-family':font['family'],
                                                               'color':colors['letter'],
                                                               'text-align':'center'}),
                                                     ],
                                                   #  style = {}
                                                 ),
                                     html.Div(
                                         id='graph',
                                         children = [
                                             dcc.Graph(id='scatter_chart',
                                                  figure= {'layout':go.Layout(title='Precipitacion acumulada en (lon='+', lat='')',
                                                              xaxis={'title':'Tiempo', 'color':colors['letter']},
                                                              yaxis={'title':'Precipitacion acumulada (l/m2)',
                                                                     'range':[0,df.PrecipitacionAcumulada.max()],
                                                                     'color':colors['letter']},
                                                              paper_bgcolor=colors['elem_bg'],
                                                              plot_bgcolor=colors['elem_bg'],
                                                              font={'color':colors['letter'], 'family':font['family']},
                                                              )},
                                                 style={'outline-color':colors['bg'],
                                                        'outline-style':'solid',
                                                        'display':'inline-block',
                                                        'width':'98%',
                                                        'height':'48%',
                                                        'backgroundColor':colors['elem_bg'],
                                                        'padding':'1%',
                                                        'outline-width':'5px',
                                                       'font-family':font['family'],
                                                        'color':colors['letter']}),
                                                         ],
                                #         style = {}
                                     ),
                                 ],
                                 style={
                                     'width':'50%',
                                     'display':'inline',
                                     'float':'left'
                                 }
                                ),
                    ],
                 #   style={}
                ),
                                html.Div(
                    id='timeslide',
                    children= [
                        html.Iframe(src='https://theweatherpartner.xyz/martav/dashboard_meteo_01x01.html', style={'min-height':'700px','min-width':'100%'})
                    ],
                    style={'outline-color':colors['bg'],
                           'outline-style':'solid',
                           'display':'inline-block',
                           'float':'left',
                         #  'width':'23%',
                           'width':'98%',
                      #     'min-width':'300px',
                      #     'min-height':'1000px',
                           'backgroundColor':colors['elem_bg'],
                           'padding':'1%',
                           'outline-width':'5px',
                           'font-family':font['family'],
                           'color':colors['letter'],
                           'text-align':'center'}),
            ],
        )
    ],
    #style={'backgroundColor':colors['bg'],
    #          'outline-width':'5px',
    #          'outline-color':colors['bg'],
    #          'outline-style':'solid',
    #          'padding':'1%',
           #   'height':'550px',
    #         'font-family':font['family'],
    #          'color':colors['letter'],
    #          'text-align':'center'}
)

@app.callback(
    [Output(component_id='scatter_chart', component_property='figure'),
     Output(component_id='precipMAX24', component_property='children'),
     Output(component_id='intMAX24', component_property='children'),
     Output(component_id='precipMAX48', component_property='children'),
     Output(component_id='intMAX48', component_property='children'),
     Output(component_id='lat', component_property='children'),
     Output(component_id='lon', component_property='children')],
    [Input(component_id='map', component_property='hoverData')])

def callback_graph(hoverData):
    vx = hoverData['points'][0]['lon']
    vy = hoverData['points'][0]['lat']
    dff = df[(df['Longitude']==vx)&(df['Latitude']==vy)]
    figure = {'data':[go.Scatter(x = dff.Time,
                                 y = dff.PrecipitacionAcumulada,
                                 mode = 'lines')],
              'layout':go.Layout(title='Precipitacion acumulada en (lon='+str(round(vx,2))+', lat='+str(round(vy,2))+')',
                                 xaxis={'title':'Tiempo', 'color':colors['letter']},
                                 yaxis={'title':'Precipitacion acumulada (l/m2)', 'range':[0,df.PrecipitacionAcumulada.max()],
                                        'color':colors['letter']},
                                 paper_bgcolor=colors['elem_bg'],
                                 plot_bgcolor=colors['elem_bg'],
                                 font={'color':colors['letter'], 'family':font['family']},
                                              )}
    precip = html.Div(id='precipMAX24',
                      children=[html.H4('Precipitacion acumulada: '),
                                html.H2(str(round(dff[df['Time']==list_time[0]].PrecipitacionAcumulada.max(),3)),
                                       style={'text-align':'center'}),
                                html.H4(' (l/m2) las proximas 24 horas')])
    intens = html.Div(id='intMAX24',
                      children=[html.H4('Intensidad maxima: '),
                                html.H2(str(round(dff[df['Time']==list_time[0]].Intensidad.max(),3)),
                                       style={'text-align':'center'}),
                                html.H4(' (l/m2/min) las proximas 24 horas')])
    precip2 = html.Div(id='precipMAX48',
                      children=[html.H4('Precipitacion acumulada: '),
                               html.H2(str(round(dff[df['Time']==list_time[1]].PrecipitacionAcumulada.max(),3)),
                                       style={'text-align':'center'}),
                               html.H4(' (l/m2) las proximas 24-48 horas')])
    intens2 = html.Div(id='intMAX48',
                      children=[html.H4('Intensidad maxima: '),
                                html.H2(str(round(dff[df['Time']==list_time[1]].Intensidad.max(),3)),
                                       style={'text-align':'center'}),
                                html.H4(' (l/m2/min) las proximas 24-48 horas')])
    lats = html.Div(id='lat',
                      children=[html.H4('Latitud: '),
                                html.H2(str(round(dff[df['Time']==list_time[1]].Latitude.max(),3))+' º',
                                       style={'text-align':'center'}),html.Br(),html.H4(' ')])
    lons = html.Div(id='lon',
                      children=[html.H4('Longitud: '),
                                html.H2(str(round(dff[df['Time']==list_time[1]].Longitude.max(),3))+' º',
                                       style={'text-align':'center'}),
                               html.Br(),html.H4(' ')])
    return figure, precip, intens, precip2, intens2, lats, lons

#app.run_server(debug=False)
if __name__ == "__main__":
    
    # Display app start
    logger.error('*' * 80)
    logger.error('App initialisation')
    logger.error('*' * 80)

    # Starting flask server
    app.run_server(debug=True)
