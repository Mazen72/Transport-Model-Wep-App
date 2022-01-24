# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input,Output,State,MATCH,ALL
import pandas as pd
import dash_table
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import os
from sqlalchemy.types import String
from fpdf import FPDF
import base64
import plotly.express as px
import plotly.graph_objects as go
from string import digits
import Functions
import about_us
import requests
import json
from ibm_watson_machine_learning import APIClient
import  shapely
import folium
import shapefile
import geopandas as gpd
server = Flask(__name__)
app = dash.Dash(
    __name__,server=server,
    meta_tags=[
        {
            'charset': 'utf-8',
        },
        {
            'name': 'viewport',
            'content': 'width=device-width, initial-scale=1, shrink-to-fit=no'
        }
    ] , external_stylesheets=[dbc.themes.BOOTSTRAP]
)

app.config.suppress_callback_exceptions = True

Urban_Districts = ['30101 Gamle Oslo','30102 Grünerløkka', '30103 Sagene','30104 St.Hanshaugen', '30105 Frogner','30106 Ullern', '30107 Vestre Aker','30108 Nordre Aker',
                   '30109 Bjerke','30110 Grorud', '30111 Stovner','30112 Alna', '30113 Østensjø','30114 Nordstrand',
                   '30115 Søndre Nordstrand','30116 Sentrum', '30117 Marka']

Grunnkrets = ['3012401 Tøyen Rode 1', '3012408 Tøyen Rode 8', '3012409 Tøyen Rode 9',
              '3012502 Grønland Rode 2', '3012503 Grønland Rode 3', '3012504 Grønland Rode 4', '3012505 Grønland Rode 5',
              '3012506 Grønland Rode 6','3012507 Grønland Rode 7','3012508 Grønland Rode 8','3012509 Grønland Rode 9',
              '3012601 Kampen Rode 1','3012602 Kampen Rode 2','3012603 Kampen Rode 3','3012604 Kampen Rode 4',
              '3012605 Kampen Rode 5','3012606 Kampen Rode 6','3012607 Kampen Rode 7','3012608 Kampen Rode 8',
              '3012609 Kampen Rode 9','3012610 Kampen Rode 10', '3012701 Vålerenga Rode 1', '3012702 Vålerenga Rode 2',
'3012703 Vålerenga Rode 3', '3012704 Vålerenga Rode 4', '3012705 Vålerenga Rode 5',
'3012706 Vålerenga Rode 6', '3012801 Gamlebyen Rode 1', '3012802 Gamlebyen Rode 2',
'3012803 Gamlebyen Rode 3', '3012804 Gamlebyen Rode 4', '3012805 Gamlebyen Rode 5',
'3012902 Loenga Sør', '3012903 Loenga Nord', '3013001 Grønlia', '3013513 Ryenberget',
'3013514 Nygårdskollen', '3013515 Kværner Nord', '3013516 Kværner Øst', '3013517 Kværner Sør'
, '3014202 Valle', '3014203 Etterstad', '3014204 Helsfyr', '3014210 Brynseng', '3014211 Ensjø Øst',
 '3014212 Ensjø Vest', '3014213 Ensjø Nord', '3014214 Ensjø Sør', '3015701 Øyene',
'3010207 Sentrum 2 - Rode 7', '3010210 Sentrum 2 - Rode 10', '3011305 Gamle Aker Rode 5',
'3012007 Torshov Rode 7', '3012008 Torshov Rode 8', '3012101 Sinsen Rode 1', '3012103 Sinsen Rode 3',
 '3012104 Sinsen Rode 4', '3012105 Sinsen Rode 5', '3012106 Sinsen Rode 6', '3012107 Sinsen Rode 7',
 '3012108 Sinsen Rode 8', '3012109 Sinsen Rode 9', '3012201 Rodeløkka Rode 1',
'3012202 Rodeløkka Rode 2', '3012203 Rodeløkka Rode 3', '3012204 Rodeløkka Rode 4',
'3012205 Rodeløkka Rode 5', '3012206 Rodeløkka Rode 6', '3012207 Rodeløkka Rode 7',
'3012208 Rodeløkka Rode 8', '3012209 Rodeløkka Rode 9', '3012301 Grünerløkka Rode 1',
'3012302 Grünerløkka Rode 2', '3012303 Grünerløkka Rode 3', '3012304 Grünerløkka Rode 4',
'3012305 Grünerløkka Rode 5', '3012306 Grünerløkka Rode 6', '3012307 Grünerløkka Rode 7',
'3012308 Grünerløkka Rode 8', '3012309 Grünerløkka Rode 9', '3012310 Grünerløkka Rode 10',
'3012311 Grünerløkka Rode 11', '3012312 Grünerløkka Rode 12', '3012313 Grünerløkka Rode 13',
 '3012402 Tøyen Rode 2', '3012403 Tøyen Rode 3', '3012404 Tøyen Rode 4', '3012405 Tøyen Rode 5',
 '3012406 Tøyen Rode 6', '3012407 Tøyen Rode 7', '3012410 Tøyen Rode 10', '3014304 Søndre Hovin',
 '3014306 Nordre Sinsen', '3014308 Løren Øst', '3014309 Løren Vest', '3014310 Frydenberg Øst',
 '3014311 Frydenberg Nord', '3014312 Frydenberg Vest', '3014313 Lille Tøyen Nord',
 '3014314 Lille Tøyen Vest', '3014315 Lille Tøyen Øst', '3011404 Ila Rode 4', '3011405 Ila Rode 5',
 '3011406 Ila Rode 6', '3011601 Sagene Rode 1', '3011602 Sagene Rode 2', '3011603 Sagene Rode 3',
 '3011604 Sagene Rode 4', '3011605 Sagene Rode 5', '3011606 Sagene Rode 6',
'3011607 Sagene Rode 7', '3011701 Bjølsen Rode 1', '3011702 Bjølsen Rode 2', '3011703 Bjølsen Rode 3',
 '3011704 Bjølsen Rode 4', '3011705 Bjølsen Rode 5', '3011706 Bjølsen Rode 6', '3011707 Bjølsen Rode 7', '3011708 Bjølsen Rode 8', '3011801 Sandaker Rode 1', '3011803 Sandaker Rode 3',
 '3011804 Sandaker Rode 4', '3011901 Åsen Rode 1', '3011902 Åsen Rode 2',
'3011903 Åsen Rode 3', '3011904 Åsen Rode 4', '3011906 Åsen Rode 6', '3011907 Åsen Rode 7',
'3011908 Åsen Rode 8', '3011909 Åsen Rode 9', '3011910 Åsen Rode 10', '3012001 Torshov Rode 1',
 '3012002 Torshov Rode 2', '3012003 Torshov Rode 3', '3012004 Torshov Rode 4', '3012005 Torshov Rode 5',
 '3012006 Torshov Rode 6', '3012009 Torshov Rode 9', '3012010 Torshov Rode 10',
 '3012011 Torshov Rode 11', '3012012 Torshov Rode 12', '3012102 Sinsen Rode 2', '3010201 Sentrum 2 - Rode 1',
 '3010202 Sentrum 2 - Rode 2', '3010204 Sentrum 2 - Rode 4', '3010205 Sentrum 2 - Rode 5',
 '3010206 Sentrum 2 - Rode 6', '3010208 Sentrum 2 - Rode 8', '3010209 Sentrum 2 - Rode 9'
, '3010212 Sentrum 2 - Rode 12', '3010213 Sentrum 2 - Rode 13', '3011001 Marienlyst',
 '3011101 Fagerborg Rode 1', '3011102 Fagerborg Rode 2', '3011103 Fagerborg Rode 3',
 '3011104 Fagerborg Rode 4', '3011105 Fagerborg Rode 5', '3011106 Fagerborg Rode 6',
 '3011201 St.hanshaugen Rode 1', '3011202 St.hanshaugen Rode 2', '3011203 St.hanshaugen Rode 3',
 '3011204 St.hanshaugen Rode 4', '3011205 St.hanshaugen Rode 5', '3011206 St.hanshaugen Rode 6',
 '3011207 St.hanshaugen Rode 7', '3011208 St.hanshaugen Rode 8',
'3011209 St.hanshaugen Rode 9', '3011210 St.hanshaugen Rode 10', '3011211 St.hanshaugen Rode 11',
 '3011301 Gamle Aker Rode 1', '3011302 Gamle Aker Rode 2', '3011303 Gamle Aker Rode 3',
 '3011304 Gamle Aker Rode 4', '3011401 Ila Rode 1', '3011402 Ila Rode 2”, ”3011403 Ila Rode 3',
 '3011501 Lindern Rode 1', '3011502 Lindern Rode 2', '3011503 Lindern Rode 3',
'3011504 Lindern Rode 4', '3010301 Sentrum 3 - Rode 1', '3010302 Sentrum 3 - Rode 2',
'3010303 Sentrum 3 - Rode 3', '3010304 Sentrum 3 - Rode 4', '3010308 Sentrum 3 - Rode 8',
'3010401 Filipstad', '3010501 Skillebekk Rode 1', '3010502 Skillebekk Rode 2', '3010503 Skillebekk Rode 3',
 '3010504 Skillebekk Rode 4', '3010601 Frogner Rode 1', '3010602 Frogner Rode 2',
 '3010603 Frogner Rode 3', '3010604 Frogner Rode 4', '3010605 Frogner Rode 5',
'3010606 Frogner Rode 6', '3010607 Frogner Rode 7', '3010608 Frogner Rode 8', '3010609 Frogner Rode 9',
 '3010610 Frogner Rode 10', '3010611 Frogner Rode 11', '3010612 Frogner Rode 12',
 '3010613 Frogner Rode 13', '3010614 Frogner Rode 14', '3010701 Uranienborg Rode 1',
'3010702 Uranienborg Rode 2', '3010703 Uranienborg Rode 3', '3010704 Uranienborg Rode 4',
'3010705 Uranienborg Rode 5', '3010706 Uranienborg Rode 6', '3010707 Uranienborg Rode 7',
'3010708 Uranienborg Rode 8', '3010709 Uranienborg Rode 9', '3010710 Uranienborg Rode 10',
'3010801 Homansbyen Rode 1', '3010802 Homansbyen Rode 2', '3010803 Homansbyen Rode 3',
'3010804 Homansbyen Rode 4', '3010805 Homansbyen Rode 5', '3010806 Homansbyen Rode 6',
'3010807 Homansbyen Rode 7', '3010808 Homansbyen Rode 8', '3010809 Homansbyen Rode 9',
'3010901 Majorstuen Rode 1', '3010902 Majorstuen Rode 2', '3010903 Majorstuen Rode 3',
'3010904 Majorstuen Rode 4', '3010905 Majorstuen Rode 5', '3010906 Majorstuen Rode 6',
'3010907 Majorstuen Rode 7', '3010908 Majorstuen Rode 8', '3010909 Majorstuen Rode 9',
'3010910 Majorstuen Rode 10', '3010911 Majorstuen Rode 11', '3010912 Majorstuen Rode 12',
'3010913 Majorstuen Rode 13', '3015601 Kongsgården', '3015602 Grande', '3015603 Fredriksborg',
 '3014703 Smestad', '3014706 Nordre Skøyen', '3014803 Husebybakken',
'3014804 Montebello', '3014805 Smestaddammen', '3014806 Abbedikollen', '3015206 Rolighet',
 '3015207 Ullerntoppen', '3015208 Ullernåsen', '3015210 Åsjordet', '3015301 Lysehagan',
 '3015302 Øraker', '3015303 Lysaker', '3015401 Bjørnsletta', '3015402 Furulund',
'3015403 Sollerud', '3015405 Bestum', '3015406 Vækerø', '3015407 Hoff Sør', '3015408 Hoff Nord',
 '3015501 Amalienborg', '3015502 Madserud', '3015503 Søndre Skøyen', '3015504 Sjølyst',
 '3014601 Vettakollen', '3014602 Slemdal', '3014603 Risbakken', '3014604 Vindern',
'3014611 Gråkammen', '3014701 Frøen', '3014702 Heggeli', '3014704 Volvat', '3014705 Grimelund',
'3014801 Persbråten', '3014802 Husebyskogen', '3014901 Hovseter', '3014902 Holmensletta',
 '3014903 Vestre Holmen', '3014904 Østre Holmen', '3014905 Svenstua',
'3014906 Løkkaskogen', '3014907 Lybekk', '3014908 Gressbanen', '3014909 Holmenbekken',
'3014910 Hamborg', '3014911 Jarbakken', '3014912 Arnebråten', '3015001 Lillevann',
'3015002 Østre Liaskogen', '3015003 Besserud', '3015004 Voksenåsen', '3015005 Vestre Liaskogen',
 '3015006 Bogstad', '3015007 Skogen', '3015008 Grindbakken', '3015201 Voksen',
'3015202 Sørsletta', '3015203 Røahagan', '3015204 Røa', '3015209 Myrhaugen', '3015211 Mosekollen Vest',
 '3015212 Mosekollen Øst', '3011709 Bjølsen Rode 9', '3014117 Ymers Vei',
'3014401 Frysjå', '3014402 Kjelsås', '3014403 Grefsenplatået', '3014405 Lillo Terrasse'
              ]



#dff=pd.read_csv('Params.csv')
#dff['color']='blue'
#dff.to_csv('Params.csv')
#df=dff[['Unnamed: 0','Trips',"OrigCode","DestCode","Origin","Destination",
                            #                      "OriPop19","DestEmp19","Ourban","Durban","Inc19_x","Inc19_y","Dist"]]

#divs=['Gamle Oslo','Sagene Oslo']
#df['color']='blue'
#indics=df[ df['Destination'].isin(divs)]['color'].index
#df['color'].loc[indics]='red'
#df.to_csv('df.csv')
#df.to_csv('df.csv')
#print(df[df['Origin']!=df['Destination']])
#filt_df = df[(df['Origin'] == 'Gamle Oslo') | (df['Destination'] == 'Gamle Oslo') ]
#print(filt_df)
#df.to_csv('dff.csv')
input_values = []

#print(filt_df['OriPop19'])
#print(list(filt_df.iloc[17].values))




#text=14px + (26 - 14) * ((100vw - 300px) / (1600 - 300))
#font-size: calc([minimum size] + ([maximum size] - [minimum size]) * ((100vw - [minimum viewport width]) / ([maximum viewport width] - [minimum viewport width])));

text_font_size='1.7vh'
navbar_font_size='2vh'
header_font_size='2vh'


encoded = base64.b64encode(open('kth.jpg', 'rb').read())

logo_img=html.Img(src='data:image/jpg;base64,{}'.format(encoded.decode()), id='logo_img', height='70vh',
                  style=dict(marginLeft='1vh'))

db_logo_img=dbc.Col([ logo_img] ,
        xs=dict(size=2,offset=0), sm=dict(size=2,offset=0),
        md=dict(size=1,offset=0), lg=dict(size=1,offset=0), xl=dict(size=1,offset=0))

header_text=html.Div('Transport Model For Simulating Urban Scenarios For Oslo City, Norway',style=dict(color='white',
                     fontWeight='bold',fontSize='2.8vh',marginTop='1vh',marginLeft='1.5vh'))

db_header_text=  dbc.Col([ header_text] ,
        xs=dict(size=10,offset=0), sm=dict(size=10,offset=0),
        md=dict(size=10,offset=0), lg=dict(size=10,offset=0), xl=dict(size=10,offset=0))



df=pd.read_csv('Params.csv')


hov_text=[]
for ind in df.index:
    hov_text.append('Origin : {}<br>Destination : {}<br>Trips : {}<br>Population : {}'.format(df['Origin'][ind],df['Destination'][ind],
                                                                                              df['Trips'][ind],df['OriPop19'][ind]))
df['hover']=hov_text

fig=go.Figure()
name_arr = []
for i in range(len(df)):
    if df['Origin'][i]==df['Destination'][i]:
        continue

    current_dist = df['Destination'][i]
    current_origin = df['Origin'][i]
    trips = df['Trips'][i]
    trips_reversed = df[(df['Origin'] == current_dist) & (df['Destination'] == current_origin)]['Trips'].values[0]
    total_trips = trips + trips_reversed


    if total_trips > 15000:
        color = 'red'
        name = '> 15000 Trips'

    elif total_trips <= 15000:
        color = 'black'
        name = '<= 15000 Trips'

    legend = True
    if name in name_arr:
        legend = False
    else:
        legend = True

    fig.add_trace(go.Scattermapbox(name=name,showlegend=legend,
    lon=[ df['lon-origin'][i],df['lon-dist'][i]],
    lat=[df['lat-origin'][i], df['lat-dist'][i]  ],
    mode='lines',
    marker={'color': color,'size':10,'allowoverlap':True,'opacity':0.1},
    #unselected={'marker': {'opacity': 1}},
   # selected={'marker': {'opacity': 0.5, 'size': 15}},
    hoverinfo='text',
    hovertext=['Subdivision : {}<br>Population : {}'.format(df['Origin'][i],df['OriPop19'][i]),
               'Subdivision : {}<br>Population : {}'.format(df['Destination'][i],df['OriPop19'][i])],
    customdata=[df['Origin'][i],df['Destination'][i]]
)
    )
    name_arr.append(name)




fig.update_layout(
            uirevision= 'foo', #preserves state of figure/map after callback activated
            clickmode= 'event+select',
            hovermode='closest',
            hoverdistance=2,
            mapbox=dict(
          #      bearing=25,
                style='light',
                center=dict(
                    lon=10.7347673396536,
                    lat=59.8992367
                ),
             #   pitch=40,
                zoom=10
            ) ,margin = dict(l = 0, r = 0, t = 30, b = 0), hoverlabel=dict(
        bgcolor="white",
        font_size=16,
        font_family="Rockwell")
        )
fig.update_layout(mapbox_style="open-street-map")

fig2=go.Figure(go.Scattermapbox())
fig2.update_layout(
            uirevision= 'foo2', #preserves state of figure/map after callback activated
            clickmode= 'event+select',
            hovermode='closest',
            hoverdistance=2,
            mapbox=dict(
            #    bearing=25,
                style='light',
                center=dict(
                    lon=10.7347673396536,
                    lat=59.8992367
                ),
            #    pitch=40,
                zoom=10
            ),margin = dict(l = 0, r = 0, t = 0, b = 0)
        )
fig2.update_layout(mapbox_style="open-street-map")
#open-street-map
#stamen-terrain

map_type=dbc.RadioItems(
    options=[
        {"label": "Line Map", "value": 'line_map'},
        {"label": "Size Map", "value": 'size_map'},
        {"label": "Folium Map", "value": 'folium_map'}
    ],
    value='folium_map',
    id="map_type", style=dict(fontSize='1.5vh',marginLeft='0.5vh')
)

db_map_type=dbc.Col([map_type] ,
        xs=dict(size=10,offset=0), sm=dict(size=10,offset=1),
        md=dict(size=2,offset=0), lg=dict(size=1,offset=0), xl=dict(size=1,offset=0))


map_header1=html.Div(html.H1('Existing Transport Model (2019 flows)',
                           style=dict(fontSize=header_font_size,fontWeight='bold',color='black')) ,style=dict(display='inline-block'))
map_header2=html.Div(html.H1('Simulated Transport Scenario',
                           style=dict(fontSize=header_font_size,fontWeight='bold',color='black')) ,style=dict(display='inline-block'))

map_div1=html.Div([
html.Iframe(srcDoc = open('map.html', 'r').read()
           ,style=dict(width='75vh',height='60vh')
            )
             ],id='map1_div'
        )

map_style_menu=  dcc.Dropdown(
        id='map_style_dropdown',
        options=[
            dict(label='open-street-map', value='open-street-map'), dict(label='carto-positron', value='carto-positron'),
            dict(label='carto-darkmatter', value='carto-darkmatter'), dict(label='stamen-terrain', value='stamen-terrain'),
            dict(label='stamen-toner', value='stamen-toner'), dict(label='stamen-watercolor', value='stamen-watercolor')
        ],
        value='open-street-map' , style=dict(color='black',fontWeight='bold',textAlign='center'
                                 ,width='20vh',backgroundColor='white',border='1px solid black')
    )

map_style_menu_div= html.Div([map_style_menu],
                          style=dict( fontSize=text_font_size,
                                      marginLeft='4vh',marginBottom='',display='inline-block'))


db_map_div1=dbc.Col([ map_header1,map_style_menu_div,map_div1] ,
        xs=dict(size=10,offset=1), sm=dict(size=10,offset=1),
        md=dict(size=8,offset=1), lg=dict(size=5,offset=1), xl=dict(size=5,offset=1))

map_div2=html.Div([
            dcc.Graph(id='map2', config={'displayModeBar': False, 'scrollZoom': True,'displaylogo': False},
                style={'height':'60vh'} ,figure=fig2
            ) ] ,id='map2_div'
        )

map_style_menu2=  dcc.Dropdown(
        id='map_style_dropdown2',
        options=[
            dict(label='open-street-map', value='open-street-map'), dict(label='carto-positron', value='carto-positron'),
            dict(label='carto-darkmatter', value='carto-darkmatter'), dict(label='stamen-terrain', value='stamen-terrain'),
            dict(label='stamen-toner', value='stamen-toner'), dict(label='stamen-watercolor', value='stamen-watercolor')
        ],
        value='open-street-map' , style=dict(color='black',fontWeight='bold',textAlign='center'
                                 ,width='20vh',backgroundColor='white',border='1px solid black')
    )

map_style_menu_div2= html.Div([map_style_menu2],
                          style=dict( fontSize=text_font_size,
                                      marginLeft='4vh',marginBottom='',display='inline-block'))

db_map_div2=dbc.Col([ map_header2,map_style_menu_div2,map_div2] ,
        xs=dict(size=10,offset=1), sm=dict(size=10,offset=1),
        md=dict(size=8,offset=1), lg=dict(size=5,offset=0), xl=dict(size=5,offset=0))



navigation_header=dbc.Nav(
    [
        dbc.NavItem(dbc.NavLink("Simulations", active='exact', href="/Simulations",id='Simulations',
                                style=dict(fontSize=navbar_font_size))),
        dbc.NavItem(dbc.NavLink("Register", href="/Register",active='exact',id='Register',
                                style=dict(fontSize=navbar_font_size))),
        dbc.NavItem(dbc.NavLink("About us", href="/About_us", active='exact', id='About_us',
                                style=dict(fontSize=navbar_font_size)))
    ],
    pills=True,
)
db_navigation_header=dbc.Col([navigation_header],
                             xs=dict(size=12, offset=0), sm=dict(size=12, offset=0),
                             md=dict(size=12, offset=0), lg=dict(size=8, offset=0), xl=dict(size=8, offset=0)
                             )

##1e90ff
db_map_header1=dbc.Col([map_header1],
                             xs=dict(size=10, offset=1), sm=dict(size=10, offset=1),
                             md=dict(size=5, offset=1), lg=dict(size=5, offset=1), xl=dict(size=5, offset=1)
                             )

db_map_header2=dbc.Col([map_header2],
                             xs=dict(size=10, offset=1), sm=dict(size=10, offset=1),
                             md=dict(size=5, offset=0), lg=dict(size=5, offset=0), xl=dict(size=5, offset=0)
                             )

simulation_type_text=html.Div(html.H1('Type of Simulation For Visualization: ',
                           style=dict(fontSize=text_font_size,fontWeight='bold',color='black',marginTop='1vh')),
                           style=dict(display='inline-block'))



simulation_type_menu=  dcc.Dropdown(
        id='sim_dropdown',
        options=[
            dict(label='Node-Node(Network)', value='Network'), dict(label='Zone-Zone(Flows)', value='Flows')
        ],
        value='Flows' , style=dict(color='black',fontWeight='bold',textAlign='center',
                                     width='20vh',backgroundColor='white',border='1px solid black')
    )
# height='50px' ,
# width='12%', marginLeft='1520px' marginTop='-400px' fontSize=26
#display='inline-block',  border='2px solid #082255',
simulation_type_menu_div= html.Div([simulation_type_menu],
                          style=dict(fontSize=text_font_size,
                                      marginLeft='1vh',marginBottom='-1.5vh',display='inline-block'))

#db_simulation_type_menu=dbc.Col([simulation_type_text,simulation_type_menu_div,html.Br(),html.Br()],
                             #xs=dict(size=10, offset=1), sm=dict(size=10, offset=1),
                            # md=dict(size=10, offset=1), lg=dict(size=3, offset=1), xl=dict(size=3, offset=1)
                            # )

model_type_text=html.Div(html.H1('Transport Model Used For Simulation:',
                           style=dict(fontSize=text_font_size,fontWeight='bold',color='black',marginTop='1vh')),
                         style=dict(display='inline-block',marginLeft='3vh'))


model_type_menu=  dcc.Dropdown(
        id='model_dropdown',
        options=[
            dict(label='Gravity Model(SIM)', value='SIM'), dict(label='Machine Learning(AI)', value='AI')
        ],
        value='SIM' , style=dict(color='black',fontWeight='bold',textAlign='center'
                                 ,width='20vh',backgroundColor='white',border='1px solid black')
    )
#display='inline-block',border='2px solid #082255',
model_type_menu_div= html.Div([model_type_menu],
                          style=dict( fontSize=text_font_size,
                                      marginLeft='1vh',marginBottom='-1.5vh',display='inline-block'))

#db_model_type_menu=dbc.Col([model_type_text,model_type_menu_div,html.Br(),html.Br()],
                           #  xs=dict(size=10, offset=1), sm=dict(size=10, offset=1),
                            # md=dict(size=10, offset=1), lg=dict(size=3, offset=0), xl=dict(size=3, offset=0)
                       #      )



city_text=html.Div(html.H1('City Subdivisons:',
                           style=dict(fontSize=text_font_size,fontWeight='bold',color='black',marginTop='1vh')),
                         style=dict(display='inline-block',marginLeft='3vh'))


city_menu=  dcc.Dropdown(
        id='city_dropdown',
        options=[
            dict(label='Urban Districts', value='Urban'), dict(label='Grunnkrets', value='Grunnkrets')
        ],
        value='Urban' , style=dict(color='black',fontWeight='bold',textAlign='center',
                                   width='15vh',backgroundColor='white',border='1px solid black')
    )
#display='inline-block',border='2px solid #082255'
city_menu_div= html.Div([city_menu],
                          style=dict( fontSize=text_font_size,
                                      marginLeft='1vh',marginBottom='-1.5vh',display='inline-block'))
ok_button = html.Div([dbc.Button("OK", color="primary", size='sm', n_clicks=0,
                                 id='ok_button',
                                 style=dict(fontSize='1.8vh')
                                 )], style=dict(display='inline-block', marginLeft='2vh'))

db_dropdowns=dbc.Col([simulation_type_text,simulation_type_menu_div,model_type_text,model_type_menu_div,
                      city_text,city_menu_div,ok_button],
                             xs=dict(size=7, offset=3), sm=dict(size=7, offset=3),
                             md=dict(size=11, offset=1), lg=dict(size=11, offset=1), xl=dict(size=11, offset=1)
                             )



scenario_header=html.H1('Oslo City Transport Simulation',
                           style=dict(fontSize=header_font_size,fontWeight='bold',color='black'))


db_scenario_header=dbc.Col([scenario_header],
                             xs=dict(size=10, offset=1), sm=dict(size=10, offset=1),
                             md=dict(size=8, offset=1), lg=dict(size=8, offset=1), xl=dict(size=8, offset=1)
                             )

navigation_header2=dbc.Nav(
    [
        dbc.NavItem(dbc.NavLink("Scenario Selection", active='exact', href="/Scenario",id='Scenario',
                                style=dict(fontSize=navbar_font_size))),
        dbc.NavItem(dbc.NavLink("Infographics", href="/Infographics",active='exact',id='Infographics',
                                style=dict(fontSize=navbar_font_size))),
        dbc.NavItem(dbc.NavLink("Model Analysis", href="/Analysis", active='exact', id='Analysis',
                                style=dict(fontSize=navbar_font_size))),
        dbc.NavItem(dbc.NavLink("Report", href="/Report", active='exact', id='Report',
                                style=dict(fontSize=navbar_font_size)))
    ],
    pills=True,
)



db_navigation_header2=dbc.Col([navigation_header2],
                             xs=dict(size=12, offset=0), sm=dict(size=12, offset=0),
                             md=dict(size=10, offset=1), lg=dict(size=10, offset=1), xl=dict(size=10, offset=1)
                             )


scenario_selection_text=html.Div(html.H1('Select Parameter for Simulation: ',
                           style=dict(fontSize=text_font_size,fontWeight='bold',color='black',marginTop='1vh')),
                           style=dict(display='inline-block'))


subdivision_text=html.Div(html.H1('Select the Subdivision: ',
                           style=dict(fontSize=text_font_size,fontWeight='bold',color='black',marginTop='1vh',marginLeft='3vh')),
                           style=dict(display='inline-block'))


#{ 'label':Grunnkrets_dist ,'value':Grunnkrets_dist } for Grunnkrets_dist in Grunnkrets
#display='inline-block',border='2px solid #082255'


multiple_param=html.Div([dbc.Button("Add Parameter(+)", color="primary", size='lg', n_clicks=0,id="multiple_param"
                            ,style=dict(fontSize=text_font_size,width='20vh')
                            ) ],style=dict(display='inline-block'))

remove_param=html.Div([dbc.Button("Remove Parameter(-)", color="primary", size='lg', n_clicks=0,id="remove_param"
                            ,style=dict(fontSize=text_font_size,width='20vh')
                            )],style=dict(display='inline-block',marginLeft='2vh'))

db_multiple_param=dbc.Col([html.Br(),multiple_param,remove_param],
                             xs=dict(size=10, offset=1), sm=dict(size=10, offset=1),
                             md=dict(size=8, offset=1), lg=dict(size=8, offset=0), xl=dict(size=8, offset=0)
                             )

existing_param_text=html.Div(html.H1('Existing 2019 parameter value: ',
                           style=dict(fontSize=text_font_size,fontWeight='bold',color='black',marginTop='1vh')),
                           style=dict(display='inline-block'))


revised_param_text=html.Div(html.H1('Revised Parameter Value For Simulation: ',
                           style=dict(fontSize=text_font_size,fontWeight='bold',color='black',marginTop='1vh')),
                           style=dict(display='inline-block',marginLeft='2vh'))


display_button=html.Div([ dbc.Button("Display", color="primary", size='lg', n_clicks=0,id="display_button"
                            ,style=dict(fontSize=text_font_size)
                            )  ],style=dict(display='inline-block'))

analyze_button=html.Div([dbc.Button("Analyze", color="primary", size='lg', n_clicks=0,id="analyze_button"
                            ,style=dict(fontSize=text_font_size)
                            )],style=dict(display='inline-block',marginLeft=''))

reset_map_button=html.Div([dbc.Button("Reset Map", color="primary", size='lg', n_clicks=0,id="reset_map_button"
                            ,style=dict(fontSize=text_font_size)
                            ) ],style=dict(display='inline-block',marginLeft='2vh'))

db_analyze_button=dbc.Col([html.Br(),analyze_button],
                             xs=dict(size=12, offset=0), sm=dict(size=12, offset=0),
                             md=dict(size=10, offset=1), lg=dict(size=6, offset=0), xl=dict(size=6, offset=0)
                             )
db_2_buttons=dbc.Col([html.Br(),display_button,reset_map_button],
                             xs=dict(size=12, offset=0), sm=dict(size=12, offset=0),
                             md=dict(size=10, offset=1), lg=dict(size=6, offset=1), xl=dict(size=6, offset=1)
                             )

download_pdf=dbc.Button("Generate PDF Output", color="primary", size='lg', n_clicks=0,id="download_pdf"
                            ,style=dict(fontSize=text_font_size)
                            )
db_download_pdf=dbc.Col([html.Br(),download_pdf],
                             xs=dict(size=10, offset=1), sm=dict(size=10, offset=1),
                             md=dict(size=10, offset=1), lg=dict(size=3, offset=1), xl=dict(size=3, offset=1)
                             )

results_msg=html.Div([''],id='results_msg',style=dict(fontSize='1.8vh',color='#1e90ff',fontWeight='bold') )

simulations_layout=  html.Div([dbc.Row([db_map_div1,db_map_div2]),html.Br(),
                      dbc.Row([db_dropdowns]),html.Br(),
                      dbc.Row([db_scenario_header]),html.Br(),
                      dbc.Row([db_navigation_header2]),html.Br(),
                      dbc.Row([dbc.Col([html.Div(
                      dbc.Container([dbc.Row(db_multiple_param),html.Div([],id='container'),
                                     dbc.Row(db_analyze_button),html.Br(),results_msg],
                                    style=dict(border='2px solid black',maxHeight='35vh',overflow='scroll'),fluid=True
                      ),id='container_content' )

                      ],   xs=dict(size=10, offset=1), sm=dict(size=10, offset=1),
                             md=dict(size=10, offset=1), lg=dict(size=10, offset=1), xl=dict(size=10, offset=1))
                          ]),
                      dbc.Row(db_2_buttons),
                      dbc.Row(db_download_pdf)])

app.layout=html.Div([ dbc.Row([db_logo_img,db_header_text],style=dict(backgroundColor='#2358a6') ),
                      dbc.Row([db_navigation_header]),html.Br(),html.Div(id='layout')
                      ,dcc.Location(id='url', refresh=True,pathname='/Simulations'),dcc.Store(id='trips_df'),
                        dcc.Store(id='simulated_trips',data=pd.DataFrame().to_dict('records')),
                      dcc.Store(id='parametrs_info', data=pd.DataFrame().to_dict('records')),
                      dcc.Store(id='folium_df', data=pd.DataFrame().to_dict('records'))



])

@app.callback(Output('layout','children'),
              Input('url','pathname'))
def change_page(url):
    if url == '/About_us':
        return about_us.layout

    elif url == '/Simulations':
        return simulations_layout

    else:
        return dash.no_update

@app.callback(Output('container_content','children'),
              Input('url','pathname')  ,[State('trips_df','data'),State('parametrs_info','data')],
              prevent_initial_call=True)
def change_content(url,trips,parameters):
    trips_df=pd.DataFrame(trips)
    parameters_df=pd.DataFrame(parameters)
    if url == '/Analysis':
        table1 = html.Div([dash_table.DataTable(
            columns=[
                {
                    'name': str(x),'id': str(x),'deletable': False,
                } for x in parameters_df.columns
            ], id='table2', page_size=20,data=parameters
            , style_cell=dict(textAlign='center', border='2px solid black'
                              , backgroundColor='white', color='black', fontSize='1.8vh', fontWeight='bold'),
            style_header=dict(backgroundColor='#26abff',
                              fontWeight='bold', border='1px solid black', fontSize='2vh'),
            editable=False,row_deletable=False,filter_action="native",sort_action="native",
            sort_mode="single",page_action='native',  style_table={'overflowX': 'auto'}
            # 'overflowY': 'auto',
        )],id='table_div2')

        table2 = html.Div([dash_table.DataTable(
            columns=[
                {
                    'name': str(x),'id': str(x),'deletable': False,
                } for x in trips_df.columns
            ], id='table', page_size=20,data=trips
            , style_cell=dict(textAlign='center', border='2px solid black'
                              , backgroundColor='white', color='black', fontSize='1.8vh', fontWeight='bold'),
            style_header=dict(backgroundColor='#26abff',
                              fontWeight='bold', border='1px solid black', fontSize='2vh'),
            editable=False,row_deletable=False,filter_action="native",sort_action="native",
            sort_mode="single",page_action='native',  style_table={'overflowX': 'auto'},
            style_data_conditional = [{'if': { 'filter_query': '{Simulated_Trips} != {Trips}','column_id': 'Simulated_Trips'},
                                       'backgroundColor': 'skyblue'}]
            # 'overflowY': 'auto',
        )],id='table_div')
        return dbc.Container([table1,html.Br(),table2],
                              style=dict(border='2px solid black',maxHeight='35vh',overflow='scroll'),fluid=True
                      )
    elif url == '/Scenario':
        return dbc.Container([dbc.Row(db_multiple_param),html.Div([],id='container'),
                              dbc.Row(db_analyze_button),html.Br(),results_msg],
                              style=dict(border='2px solid black',maxHeight='35vh',overflow='scroll'),fluid=True
                      )

    else:
        return dash.no_update


@app.callback([Output('results_msg','children'),Output('trips_df','data'),Output('parametrs_info','data'),Output('folium_df','data')],
              Input('analyze_button','n_clicks'),
              [State({'type': 'subdivisions_dynamic_menu', 'index': ALL}, 'value'),
               State({'type': 'parameter_menu', 'index': ALL}, 'value'),
               State({'type': 'existing_input_dynamic','index': ALL}, 'value'),
               State({'type': 'revised_input_dynamic','index': ALL}, 'value'),
               State({'type': 'dynamic_variation_text','index': ALL},'children')
               ]
              ,prevent_initial_call=True)
def analyze(clicks,subdivision,parameter,existing_input,revised_input,variation):
    ctx = dash.callback_context


    remove_digits = str.maketrans('', '', digits)
    i=0
    for subdiv in subdivision:
        subdivision[i]=subdivision[i].translate(remove_digits)
        if 'Oslo' not in subdivision[i]:
            subdivision[i]=subdivision[i][1:] + ' ' + 'Oslo'
        else:
            subdivision[i] = subdivision[i][1:]
        i+=1

    # Population,Employment,Income,Urbanisation
    input_values = []
    indices=[]
    final_df=pd.DataFrame()
    dff = pd.read_csv('Params.csv')
    print('subdivs',subdivision)
    for param, division , mod_input in zip(parameter, subdivision,revised_input):

        filt_df = dff[['Unnamed: 0', "OrigCode", "DestCode", "Origin", "Destination",
                       "OriPop19", "DestEmp19", "Ourban", "Durban", "Inc19_x", "Inc19_y", "Dist"]]
        trips_df=dff[['OrigCode','DestCode',"Origin", "Destination",'Trips']]
        if param == 'Population':
            filt_df=filt_df[filt_df['Origin']==division]
            trips_df=trips_df[trips_df['Origin']==division]
            for index, row in filt_df.iterrows():
                if index in indices:
                    continue
                row['OriPop19'] = float(mod_input)
                input_values.append(list(row.values))
                indices.append(index)

        elif param=='Employment':
            filt_df=filt_df[filt_df['Destination']==division]
            trips_df=trips_df[trips_df['Destination']==division]
            for index, row in filt_df.iterrows():
                if index in indices:
                    continue
                row['DestEmp19'] = float(mod_input)
                input_values.append(list(row.values))
                indices.append(index)

        elif param=='Income':
            filt_df= filt_df[(filt_df['Origin'] == division) | (filt_df['Destination'] == division) ]
            trips_df=trips_df[(trips_df['Origin'] == division) | (trips_df['Destination'] == division) ]
            for index, row in filt_df.iterrows():
                if index in indices:
                    continue
                if row['Origin']==division and row['Destination']==division:
                    row['Inc19_x'] = float(mod_input)
                    row['Inc19_y'] = float(mod_input)

                elif row['Origin']==division:
                    row['Inc19_x'] = float(mod_input)

                elif row['Destination']==division:
                    row['Inc19_y'] = float(mod_input)

                input_values.append(list(row.values))
                indices.append(index)

        elif param == 'Urbanisation':
            filt_df= filt_df[(filt_df['Origin'] == division) | (filt_df['Destination'] == division) ]
            trips_df=trips_df[(trips_df['Origin'] == division) | (trips_df['Destination'] == division) ]
            for index, row in filt_df.iterrows():
                if index in indices:
                    continue
                if row['Origin'] == division and row['Destination'] == division:
                    row['Ourban'] = float(mod_input)
                    row['Durban'] = float(mod_input)

                elif row['Origin'] == division:
                    row['Ourban'] = float(mod_input)

                elif row['Destination'] == division:
                    row['Durban'] = float(mod_input)

                input_values.append(list(row.values))
                indices.append(index)


        else:
            return (dash.no_update,dash.no_update,dash.no_update,dash.no_update)

        final_df = final_df.append(trips_df,ignore_index=False)
    if final_df.empty:
        return (dash.no_update, dash.no_update,dash.no_update,dash.no_update)

    final_df = final_df[~final_df.index.duplicated(keep='first')]

    print('input_values',input_values)
    print(len(input_values))

    #return (dash.no_update, dash.no_update,dash.no_update,dash.no_update)


    API_KEY = 'api_key'
    token_response = requests.post('https://iam.cloud.ibm.com/identity/token',
                                       data={"apikey": API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
    mltoken = token_response.json()["access_token"]
    header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

    payload_scoring = {"input_data": [{"fields": ['Unnamed: 0', "OrigCode", "DestCode", "Origin", "Destination",
                                                      "OPop", "DEmpl", "Ourban", "Durban", "OInc",
                                                    "DInc","Distance"],
                                        "values": input_values
                                       }]}
    response_scoring = requests.post(
           'https://eu-de.ml.cloud.ibm.com/ml/v4/deployments/deployment_id/predictions?version=2022-01-20',
           json=payload_scoring, headers=header)
    print("Scoring response")
    print(response_scoring.json())
    results=response_scoring.json()
    results=results['predictions'][0]['values']
    final_results=[]
    for trip in results:
        final_results.append(trip[0])
    final_df['Simulated_Trips']=final_results
    mod_trips_df=dff[['OrigCode','DestCode',"Origin", "Destination",'Trips']]
    mod_trips_df['Simulated_Trips']=mod_trips_df['Trips']
    mod_trips_df.loc[final_df.index]=final_df
    parameters_data = {'Parameters':parameter , 'SubDivision': subdivision, 'Exisiting_Value': existing_input,
                       'Modified_Value': revised_input, 'Variation': variation }

    parameters_df = pd.DataFrame(parameters_data)
    folium_df=mod_trips_df.groupby(['OrigCode','DestCode','Origin','Destination'],sort=True)['Trips','Simulated_Trips'].mean().reset_index()

    return ('Analysis Done',mod_trips_df.to_dict('records'),parameters_df.to_dict('records'),folium_df.to_dict('records'))

@app.callback(
    Output({'type': 'dynamic_variation_text','index': MATCH},'children'),
    Input({'type': 'revised_input_dynamic', 'index': MATCH},'value'),
    [State({'type': 'existing_input_dynamic','index': MATCH}, 'value')]
,prevent_initial_call=True
)
def update_variation(modified_input,existing_input):
    if modified_input != '' and existing_input != '' :
        variation=(float(modified_input)-float(existing_input))/float(existing_input)
        return '{}% variation..'.format(str(round(variation, 2)))
    else:
        return dash.no_update
@app.callback(
    Output({'type': 'existing_input_dynamic','index': MATCH},'value'),
    Input({'type': 'ok_button_dynamic', 'index': MATCH},'n_clicks'),
    [State({'type': 'subdivisions_dynamic_menu','index': MATCH}, 'value'),
     State({'type': 'parameter_menu','index': MATCH}, 'value')]
,prevent_initial_call=True
)
def update_existing_input(n_clicks,subdivision,parameter):
    df = pd.read_csv('Params.csv')
    remove_digits = str.maketrans('', '', digits)
    subdivision_name = subdivision.translate(remove_digits)
    subdivision_name = subdivision_name[1:]

    if parameter=='Population':
        return df[df['Origin'].str.contains(subdivision_name)]['OriPop19'].values[0]

    elif parameter=='Employment':
        return df[df['Destination'].str.contains(subdivision_name)]['DestEmp19'].values[0]

    elif parameter == 'Income':
        return df[df['Origin'].str.contains(subdivision_name)]['Inc19_x'].values[0]

    elif parameter == 'Urbanisation':
        return df[df['Origin'].str.contains(subdivision_name)]['Ourban'].values[0]

    else:
        pass


@app.callback(
    [Output({'type': 'subdivisions_dynamic_menu','index': MATCH}, 'options'),
     Output({'type': 'subdivisions_dynamic_menu','index': MATCH}, 'value')
     ],
    [Input('city_dropdown', 'value')],
    State({'type': 'subdivisions_dynamic_menu','index': MATCH}, 'value')


,prevent_initial_call=True

)
def change_subdivisions(city_subdivision,value):
    subdivisions=[]
    print('value')
    print(value)
    if city_subdivision=='Urban':
        subdivisions=Urban_Districts
        return [[{'label': division, 'value': division} for division in subdivisions],subdivisions[0]]

    elif city_subdivision== 'Grunnkrets':
        subdivisions = Grunnkrets
        return [[{'label': division, 'value': division} for division in subdivisions],subdivisions[0]]



@app.callback(
    Output('container', 'children'),
    [Input('multiple_param', 'n_clicks'),Input('remove_param', 'n_clicks')],
    [State('container', 'children'),State('city_dropdown','value')]
    ,prevent_initial_call=True
)
def add_parameter(n_clicks,n_clicks2,container_content,city_subdivision):
    ctx = dash.callback_context
    if ctx.triggered:
        input_id = ctx.triggered[0]['prop_id'].split('.')[0]

        if input_id =='remove_param':
            container_content.pop()
            return container_content

        elif input_id == 'multiple_param':
            subdivisions=[]
            if city_subdivision=='Urban':
                subdivisions=Urban_Districts
            elif city_subdivision== 'Grunnkrets':
                subdivisions = Grunnkrets

            parameter_menu = dcc.Dropdown(
        id={'type': 'parameter_menu','index': n_clicks},
        options=[
            dict(label='Population', value='Population'),
            dict(label='Employment (Jobs)', value='Employment'),
            dict(label='Income Levels', value='Income'),
            dict(label='Urbanisation', value='Urbanisation')

        ],
        value='Population', style=dict(color='black', fontWeight='bold', textAlign='center',
                                       width='20vh', backgroundColor='white', border='1px solid black')
    )

            scenario_selection_menu_div = html.Div([parameter_menu],style=dict(fontSize=text_font_size,marginLeft='1vh',
                                                                       marginBottom='-1.5vh',display='inline-block'))

            subdivision_menu = dcc.Dropdown(
        id={
            'type': 'subdivisions_dynamic_menu',
            'index': n_clicks
        },
        options=[{'label': division, 'value': division} for division in subdivisions
                 ],
        value=subdivisions[0], style=dict(color='black', fontWeight='bold', textAlign='center',
                                             width='17vh', backgroundColor='white', border='1px solid black')
    )

            subdivision_menu_div = html.Div([subdivision_menu],style=dict(fontSize=text_font_size,marginLeft='1vh',
                                                                  marginBottom='-1.5vh',display='inline-block'))

            ok_button = html.Div([dbc.Button("OK", color="primary", size='sm', n_clicks=0,
                                      id={'type': 'ok_button_dynamic', 'index': n_clicks},
                                      style=dict(fontSize='1.8vh')
                                     )], style=dict(display='inline-block',marginLeft='2vh'))

            db_menus = dbc.Col([scenario_selection_text,scenario_selection_menu_div,
                        subdivision_text, subdivision_menu_div,ok_button ,html.Br()],
                                  xs=dict(size=10, offset=1), sm=dict(size=10, offset=1),
                                  md=dict(size=10, offset=0), lg=dict(size=10, offset=0), xl=dict(size=10, offset=0)
                                  )

            existing_input = dbc.Input(id={'type': 'existing_input_dynamic','index': n_clicks},
                              placeholder='Enter Value', n_submit=0,
                              type='number', size="md", autocomplete='off',value='',
                              style=dict(width='15vh', border='1px solid black')
                                     )
#value=subdivisions[0].split()[0],
            existing_param_input_div = html.Div([existing_input],
                                        style=dict(fontSize='1.7vh', marginLeft='1vh', marginBottom='-2vh',display='inline-block'))


            revised_input=dbc.Input(id={'type': 'revised_input_dynamic','index': n_clicks},
                         placeholder='Enter Value', n_submit=0,
                         type='number', size="md",autocomplete='off', value='',
                         style=dict(width='15vh',border='1px solid black'))

            revised_param_input_div =html.Div([revised_input],style=dict(fontSize='1.7vh',marginLeft='1vh',marginBottom='-2vh',display='inline-block'))

            variation_text = html.Div(html.H1('',id={'type': 'dynamic_variation_text','index': n_clicks},
                                              style=dict(fontSize=text_font_size, fontWeight='bold', color='black',
                                                         marginTop='1vh')),
                                      style=dict(display='inline-block', marginLeft='2vh'))

            db_inputs = dbc.Col([existing_param_text,existing_param_input_div,revised_param_text,revised_param_input_div,
                         variation_text , html.Br(), html.Br()],
                           xs=dict(size=10, offset=1), sm=dict(size=10, offset=1),
                           md=dict(size=10, offset=0), lg=dict(size=11, offset=0), xl=dict(size=11, offset=0),
                           style=dict()
                           )

            new_div=html.Div([html.Br(),dbc.Row([db_menus]),html.Br(),dbc.Row([db_inputs])])

            container_content.append(new_div)

            return container_content


#map_style_dropdown
@app.callback(Output('map1_div', 'children'),
             [Input('ok_button', 'n_clicks')],State('sim_dropdown','value')
        )
def update_map1(clicks,type):
    df = pd.read_csv('Params.csv')
  #  ctx = dash.callback_context
 #   if ctx.triggered:
#        input_id = ctx.triggered[0]['prop_id'].split('.')[0]


    if type == 'Flows':

        return dcc.Graph(id='map1', config={'displayModeBar': False, 'scrollZoom': True, 'displaylogo': False},
              style={'height': '60vh'}, figure=Functions.create_combined_map(df,[])
              )


    elif type == 'Network':
        return html.Iframe(srcDoc = open('map.html', 'r').read()
           ,style=dict(width='75vh',height='60vh')
            )


@app.callback(Output('map2_div', 'children'),
             [Input('display_button', 'n_clicks')],
              [State('sim_dropdown','value'),State('trips_df','data'),State('folium_df','data'),State('parametrs_info','data')]
        )
def update_map2(clicks,type,trips,folium_data,parameters):
    df = pd.read_csv('Params.csv')
    trips_df=pd.DataFrame(trips)
    folium_df=pd.DataFrame(folium_data)
    if trips_df.empty or folium_df.empty:
        return dash.no_update

    df['Trips']=trips_df['Simulated_Trips']

    if type == 'Flows':
        param_df=pd.DataFrame(parameters)
        divsions=param_df['SubDivision'].to_list()
        return dcc.Graph(id='map2', config={'displayModeBar': False, 'scrollZoom': True, 'displaylogo': False},
              style={'height': '60vh'}, figure=Functions.create_combined_map(df,divsions)
              )


    elif type == 'Network':
        j_file = shapefile.Reader("Roads/Roads.shp").__geo_interface__

        # print(j_file)
        shp_ = gpd.read_file(r"Roads/Roads.shp")
        gpkg_ = gpd.read_file(r"UD/OsloUD.shp")

        # removing the 0 from the column bydelsnr to be able to merge
        gpkg_["bydelsnr"] = gpkg_["bydelsnr"].apply(lambda x: x[1:] if x.startswith("0") else x)
        # importing the file
        gpkg_imported = pd.read_csv("gpkg_.csv")
        # merging the 2 files
        merged = gpkg_imported.merge(folium_df, how='right', left_on='bydelsnr', right_on='OrigCode')
        # converting merged DataFrame into GeoDataFrame
        geometry = merged['geometry'].map(shapely.wkt.loads)  # mapping the geometry
        merged_geo = gpd.GeoDataFrame(merged, crs=shp_.crs,
                                      geometry=geometry)  # convert and assign the crs as the shape file
        res_intersect = merged_geo.overlay(shp_, how='intersection', keep_geom_type=False)
        m = res_intersect.explore(
            column="Simulated_Trips",  # make choropleth based on "BoroName" column
            scheme="Percentiles",  # use mapclassify's natural breaks scheme
            legend=True,  # show legend
            k=10,  # use 10 bins
            legend_kwds=dict(colorbar=True),  # do not use colorbar
            name="Simulated_Trips",
            cmap='tab10'  # name of the layer in the map
        )

        gpkg_.explore(
            m=m,  # pass the map object
            color="gray",  # use red color on all points
            marker_kwds=dict(radius=10, fill=True),  # make marker radius 10px with fill
            tooltip="bydelsnr",  # show "name" column in the tooltip
            tooltip_kwds=dict(labels=True),  # do not show column label in the tooltip
            name="bydelsnr"  # name of the layer in the map
        )
        folium.TileLayer('Cartodb dark_matter', control=True).add_to(m)  # use folium to add alternative tiles
        folium.LayerControl().add_to(m)  # use folium to add layer control

        m.save('sim_map.html')
        return html.Iframe(srcDoc = open('sim_map.html', 'r').read()
           ,style=dict(width='75vh',height='60vh')
            )


@app.callback(Output('map1', 'figure'),
             [Input('map_style_dropdown', 'value')], # this triggers the event
             [State('map1', 'figure')]
        )
def map1_style(style,fig):
    fig['layout']['mapbox']['style'] = style
    return fig





@app.callback(Output('map2', 'figure'),
             [Input('map_style_dropdown2', 'value')], # this triggers the event
             [State('map2', 'figure')]
              ,prevent_initial_call=True)
def update_map2_style(style,fig):
    fig['layout']['mapbox']['style']=style
    return fig


html.Iframe(srcDoc = open('map.html', 'r').read()
           ,style=dict(width='75vh',height='60vh')
            )
dcc.Graph(id='map1', config={'displayModeBar': True, 'scrollZoom': True, 'displaylogo': False},
              style={'height': '60vh'}, figure=fig
              )
if __name__ == '__main__':
    app.run_server(port=8700,debug=True)
