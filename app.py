import os
from dash import Dash, html
import dash_leaflet as dl
import dash_leaflet.express as dlx
from dash import Dash, html, Output, Input
from dash_extensions.javascript import arrow_function, assign
import starbucks
import geopandas as gpd
import pandas as pd
import json
import map_util as mu


from demographics import import_income, import_demographics
from dash.dependencies import Output, Input

lib, pharm, murals = mu.geo_df()
lib.rename(columns ={'name':'tooltip'}, inplace=True)
print(lib.columns)


def cap(st):
    return st.title()

income = import_income()
income = income.loc[:,['neighbor', 'income_per_1000']]
income.columns = ['community','income_per_1000']

geojson_file = 'data/Boundaries - Community Areas (current).geojson'
comm_boundaries = gpd.read_file(geojson_file)
comm_boundaries['community'] = comm_boundaries.apply(lambda x: cap(x.community), axis = 1)
choro_boundaries = pd.merge(comm_boundaries, income, on='community', how='left')

classes = list(income['income_per_1000'].quantile([0, 0.2, 0.4, 0.6, 0.8, 1]))
colorscale = ['#FFEDA0', '#FED976', '#FEB24C', '#FD8D3C', '#FC4E2A', '#E31A1C']
style = dict(weight=2, opacity=1, color='white', dashArray='3', fillOpacity=0.7)
# Create colorbar.
ctg = ["{}+".format(cls, classes[i + 1]) for i, cls in enumerate(classes[:-1])] + ["{}+".format(classes[-1])]
colorbar = dlx.categorical_colorbar(categories=ctg, colorscale=colorscale, width=300, height=30, position="bottomleft")
# Geojson rendering logic, must be JavaScript as it is executed in clientside.
style_handle = assign("""function(feature, context){
    const {classes, colorscale, style, colorProp} = context.props.hideout;  // get props from hideout
    const value = feature.properties[colorProp];  // get value the determines the color
    for (let i = 0; i < classes.length; ++i) {
        if (value > classes[i]) {
            style.fillColor = colorscale[i];  // set the fill color according to the class
        }
    }
    return style;
}""")
# Create geojson.
geojson2 = dl.GeoJSON(data = json.loads(choro_boundaries.to_json()),  # url to geojson file
                     options=dict(style=style_handle),  # how to style each polygon
                     zoomToBounds=True,  # when true, zooms to bounds when data changes (e.g. on load)
                     zoomToBoundsOnClick=True,  # when true, zooms to bounds of feature (e.g. polygon) on click
                     hoverStyle=arrow_function(dict(weight=5, color='#666', dashArray='')),  # style applied on hover
                     hideout=dict(colorscale=colorscale, classes=classes, style=style, colorProp="income_per_1000"),
                     id="geojson")



#cafe_dicts = starbucks.go()

cafe_dicts = [{'name': ' West Monroe Street, Loop',
                'lat': '41.8804904',
                'lon': '-87.6375454'},
                {'name': ' East 55th Street, Hyde Park',
                'lat': '41.7952167',
                'lon': '-87.5967215'},
                {'name': ' South Stony Island Avenue, Cornell',
                'lat': '41.76586165',
                'lon': '-87.5856104836036'},
                {'name': ' West Madison Street, Loop',
                'lat': '41.8817746',
                'lon': '-87.6355264'},
                {'name': ' South Drexel Avenue, Hyde Park',
                'lat': '41.7912072',
                'lon': '-87.6039887'},
                {'name': ' East 58th Street, Hyde Park',
                'lat': '41.7897081',
                'lon': '-87.6017075'},
                {'name': ' West Jackson Boulevard, Loop',
                'lat': '41.8779958',
                'lon': '-87.6340388'},
                {'name': ' South Cicero Avenue, Archer Limits',
                'lat': '41.80740995',
                'lon': '-87.7428436690573'},
                {'name': ' West 63rd Street, Englewood',
                'lat': '41.7801609',
                'lon': '-87.6451059791159'},
                {'name': ' West 103rd Street, Washington Heights',
                'lat': '41.70636755',
                'lon': '-87.67044759816'},
                {'name': ' East Illinois Street, Streeterville',
                'lat': '41.8906383',
                'lon': '-87.6173152'},
                {'name': ' West Erie Street, Magnificent Mile',
                'lat': '41.8942218',
                'lon': '-87.6294975'},
                {'name': ' North Michigan Avenue, Streeterville',
                'lat': '41.8906238',
                'lon': '-87.624469'},
                {'name': ' Pedway, Streeterville', 'lat': '41.8862551', 'lon': '-87.6215867'},
                {'name': ' North Michigan Avenue, Loop',
                'lat': '41.8823905',
                'lon': '-87.6247215'},
                {'name': ' Merchandise Mart Plaza, Loop',
                'lat': '41.888289',
                'lon': '-87.6359031'},
                {'name': ' East Ontario Street, Streeterville',
                'lat': '41.8933007',
                'lon': '-87.6175766'},
                {'name': ' West Randolph Street, Loop',
                'lat': '41.8846116',
                'lon': '-87.6373395'},
                {'name': ' East Washington Street, Loop',
                'lat': '41.8830642',
                'lon': '-87.6264632'},
                {'name': ' West Adams Street, Loop',
                'lat': '41.8790994',
                'lon': '-87.6362226'},
                {'name': ' East Monroe Street, Loop',
                'lat': '41.8803535',
                'lon': '-87.6270098'},
                {'name': ' North Orleans Street, Cabrini-Green',
                'lat': '41.8897866',
                'lon': '-87.6371788'},
                {'name': ' West Adams Street, Loop',
                'lat': '41.8793064',
                'lon': '-87.6309801'},
                {'name': ' East Ontario Street, Magnificent Mile',
                'lat': '41.8935124',
                'lon': '-87.6265885'},
                {'name': ' North State Street, Magnificent Mile',
                'lat': '41.8926716',
                'lon': '-87.62845'},
                {'name': " South Wabash Avenue, Printer's Row",
                'lat': '41.8798703',
                'lon': '-87.6264312'},
                {'name': ' South Canal Street, Greektown',
                'lat': '41.8793973',
                'lon': '-87.640942'},
                {'name': ' East Wacker Drive, Streeterville',
                'lat': '41.8866774',
                'lon': '-87.6267246'},
                {'name': ' West Adams Street, Loop',
                'lat': '41.8795166',
                'lon': '-87.6340258'},
                {'name': " South Dearborn Street, Printer's Row",
                'lat': '41.8731754',
                'lon': '-87.6289521'},
                {'name': ' North Franklin Street, Loop',
                'lat': '41.88485465',
                'lon': '-87.6356751495342'},
                {'name': ' South Riverside Plaza, Greektown',
                'lat': '41.8787154',
                'lon': '-87.638559'},
                {'name': ' West Lake Street, Greektown',
                'lat': '41.8859048',
                'lon': '-87.6430854'},
                {'name': " South Canal Street, Printer's Row",
                'lat': '41.8681043',
                'lon': '-87.6389402'},
                {'name': ' North Riverside Plaza, Greektown',
                'lat': '41.8821839',
                'lon': '-87.6391068'},
                {'name': ' West Randolph Street, Near West Side',
                'lat': '41.8845767',
                'lon': '-87.6519538'},
                {'name': ' West Taylor Street, Illinois Medical District',
                'lat': '41.86951135',
                'lon': '-87.6630355794946'},
                {'name': ' North Wabash Avenue, Loop',
                'lat': '41.88269',
                'lon': '-87.6258048'},
                {'name': ' West Lake Street, Loop',
                'lat': '41.8854959',
                'lon': '-87.6344093'},
                {'name': ' North Wells Street, Near North Side',
                'lat': '41.8920269',
                'lon': '-87.6339103'},
                {'name': ' North La Salle Street, Loop',
                'lat': '41.8859392',
                'lon': '-87.6316738'},
                {'name': ' West Washington Street, Loop',
                'lat': '41.8833456',
                'lon': '-87.6331909'},
                {'name': ' West Kinzie Street, Loop',
                'lat': '41.8893039',
                'lon': '-87.6345963'},
                {'name': ' West Grand Avenue, Magnificent Mile',
                'lat': '41.89178285',
                'lon': '-87.6314265457118'},
                {'name': ' West Randolph Street, Loop',
                'lat': '41.8846529',
                'lon': '-87.6336735'},
                {'name': ' West North Avenue, Belgravia Terrace',
                'lat': '41.9112846',
                'lon': '-87.6348689'},
                {'name': ' North Wells Street, Near North Side',
                'lat': '41.90995675',
                'lon': '-87.6350247990805'},
                {'name': ' North Dearborn Street, Near North Side',
                'lat': '41.9037941',
                'lon': '-87.6301786'},
                {'name': ' North State Street, Magnificent Mile',
                'lat': '41.8976392',
                'lon': '-87.6283786'},
                {'name': ' North Rush Street, Gold Coast',
                'lat': '41.9009817',
                'lon': '-87.6273639'},
                {'name': ' West Belden Avenue, Lincoln Park',
                'lat': '41.9235545',
                'lon': '-87.6458622'},
                {'name': ' North Damen Avenue, Wicker Park',
                'lat': '41.9103108',
                'lon': '-87.6776508'},
                {'name': ' West Wrightwood Avenue, Lincoln Park',
                'lat': '41.9288055',
                'lon': '-87.6584501'},
                {'name': ' West Addison Street, Wrigleyville',
                'lat': '41.9470884',
                'lon': '-87.6553655'},
                {'name': ' North Clark Street, Mid-North District',
                'lat': '41.9286324',
                'lon': '-87.6421131'},
                {'name': ' West Fullerton Avenue, Hamlin Park',
                'lat': '41.925504',
                'lon': '-87.6723414'},
                {'name': ' North Clark Street, Pine Grove',
                'lat': '41.9398402',
                'lon': '-87.6507796'},
                {'name': ' North Halsted Street, Lincoln Park',
                'lat': '41.9219393',
                'lon': '-87.6488352'},
                {'name': ' West Fullerton Avenue, Lincoln Park',
                'lat': '41.9250835',
                'lon': '-87.6603561'},
                {'name': ' West North Avenue, Lincoln Park',
                'lat': '41.9105426',
                'lon': '-87.653618'},
                {'name': ' South Harper Court, Hyde Park',
                'lat': '41.7998148',
                'lon': '-87.5876046'},
                {'name': ' West Adams Street, Loop',
                'lat': '41.8792543',
                'lon': '-87.631267'},
                {'name': " South Dearborn Street, Printer's Row",
                'lat': '41.8725408',
                'lon': '-87.6289194'},
                {'name': ' North Lincoln Avenue, North Center',
                'lat': '41.9547023',
                'lon': '-87.6789343'},
                {'name': ' North Western Avenue, Bricktown',
                'lat': '41.9479399',
                'lon': '-87.6886408537216'},
                {'name': ' West Foster Avenue, North Park',
                'lat': '41.975882',
                'lon': '-87.7100736'},
                {'name': ' North Lincoln Avenue, North Center',
                'lat': '41.9647919',
                'lon': '-87.6858529'},
                {'name': ' North California Avenue, Maplewood',
                'lat': '41.92796',
                'lon': '-87.697351'},
                {'name': ' North Lincoln Avenue, North Center',
                'lat': '41.9591945',
                'lon': '-87.6820201'},
                {'name': ' North Lincoln Avenue, North Center',
                'lat': '41.959466',
                'lon': '-87.6826489'},
                {'name': ' North Damen Avenue, West Ravenswood',
                'lat': '41.967258',
                'lon': '-87.6789172'},
                {'name': ' North Lincoln Avenue, North Center',
                'lat': '41.9605977',
                'lon': '-87.6830260786035'},
                {'name': ' North Lincoln Avenue, North Center',
                'lat': '41.9594406',
                'lon': '-87.682244'},
                {'name': ' North Milwaukee Avenue, Wicker Park',
                'lat': '41.9099808',
                'lon': '-87.6763286260514'},
                {'name': ' North Milwaukee Avenue, Wicker Park',
                'lat': '41.9087192',
                'lon': '-87.6744313024278'},
                {'name': ' West Cortland Street, Wicker Park',
                'lat': '41.91573875',
                'lon': '-87.6761931903038'},
                {'name': ' North Milwaukee Avenue, Wicker Park',
                'lat': '41.909001',
                'lon': '-87.6755861'},
                {'name': ' North Milwaukee Avenue, Wicker Park',
                'lat': '41.9096819',
                'lon': '-87.6761279'},
                {'name': ' North Milwaukee Avenue, Wicker Park',
                'lat': '41.9069152',
                'lon': '-87.6717385'},
                {'name': ' North Milwaukee Avenue, Wicker Park',
                'lat': '41.9083871',
                'lon': '-87.6746231'},
                {'name': ' North Paulina Street, Wicker Park',
                'lat': '41.9058744',
                'lon': '-87.6701576'},
                {'name': ' North Elston Avenue, Bricktown',
                'lat': '41.92809935',
                'lon': '-87.68249665'},
                {'name': ' West Armitage Avenue, Wicker Park',
                'lat': '41.9175758',
                'lon': '-87.6802739'},
                {'name': ' North Leavitt Street, Bricktown',
                'lat': '41.9393133',
                'lon': '-87.6830349851111'},
                {'name': ' North Clybourn Avenue, Lincoln Park',
                'lat': '41.910787',
                'lon': '-87.6490879'},
                {'name': ' North Milwaukee Avenue, Cabrini-Green',
                'lat': '41.8913731',
                'lon': '-87.648171'},
                {'name': ' West Division Street, Wicker Park',
                'lat': '41.9031435',
                'lon': '-87.6700847'},
                {'name': ' North Greenview Avenue, Wrigleyville',
                'lat': '41.9376211',
                'lon': '-87.6660205'},
                {'name': ' North Southport Avenue, Wrigleyville',
                'lat': '41.943262',
                'lon': '-87.6638329'},
                {'name': ' North Southport Avenue, Lincoln Park',
                'lat': '41.927166',
                'lon': '-87.6636019'},
                {'name': ' West Cermak Road, Chinatown',
                'lat': '41.8526305',
                'lon': '-87.6346207'},
                {'name': ' North Kedzie Avenue, Ravenswood Manor',
                'lat': '41.9645511',
                'lon': '-87.7088137'},
                {'name': ' North Damen Avenue, West Ravenswood',
                'lat': '41.9719499',
                'lon': '-87.6790776'},
                {'name': ' North Lincoln Avenue, Lincoln Park',
                'lat': '41.9284346',
                'lon': '-87.653186'},
                {'name': ' West Wrightwood Avenue, Lincoln Park',
                'lat': '41.9287608',
                'lon': '-87.662364'},
                {'name': ' West Wrightwood Avenue, Lincoln Park',
                'lat': '41.9291567',
                'lon': '-87.6532745'},
                {'name': ' West Montana Street, Lincoln Park',
                'lat': '41.9261931',
                'lon': '-87.6585879'},
                {'name': ' North Clark Street, Summerdale',
                'lat': '41.9781363',
                'lon': '-87.6685161'},
                {'name': ' North Sheridan Road, Rogers Park',
                'lat': '42.004635',
                'lon': '-87.6611727'},
                {'name': ' West Wrightwood Avenue, Lincoln Park',
                'lat': '41.9287672',
                'lon': '-87.6620035'},
                {'name': ' West Fullerton Avenue, Lincoln Park',
                'lat': '41.9249538',
                'lon': '-87.6639407394269'},
                {'name': ' North Broadway, Edgewater Glen',
                'lat': '41.9979065',
                'lon': '-87.6609190189944'},
                {'name': ' West Irving Park Road, Irving Park',
                'lat': '41.9533541',
                'lon': '-87.7378643'},
                {'name': " O'Hare Commercial Arrivals, O'Hare",
                'lat': '41.9746712',
                'lon': '-87.9086529'},
                {'name': ' North Wolcott Avenue, Ravenswood Place',
                'lat': '41.9616382',
                'lon': '-87.6761596'},
                {'name': ' North Clinton Street, Greektown',
                'lat': '41.8858431',
                'lon': '-87.6411361'},
                {'name': ' West Webster Avenue, Lincoln Park',
                'lat': '41.9218128',
                'lon': '-87.6561701'},
                {'name': ' North Lincoln Avenue, Lincoln Park',
                'lat': '41.93185255',
                'lon': '-87.6572273154071'},
                {'name': ' West Webster Avenue, Lincoln Park',
                'lat': '41.9217617',
                'lon': '-87.6594316'},
                {'name': ' West Schubert Avenue, Lincoln Park',
                'lat': '41.9305296',
                'lon': '-87.6612825'},
                {'name': ' West Webster Avenue, Lincoln Park',
                'lat': '41.9217681',
                'lon': '-87.6585218'},
                {'name': ' West Lawrence Avenue, Ravenswood Place',
                'lat': '41.9686693',
                'lon': '-87.6730252'},
                {'name': ' West Howard Street, West Ridge',
                'lat': '42.0192022',
                'lon': '-87.6899271'},
                {'name': ' North Western Avenue, West Ridge',
                'lat': '42.01925965',
                'lon': '-87.69050765'},
                {'name': ' West Wellington Avenue, Lincoln Park',
                'lat': '41.93635565',
                'lon': '-87.661408698263'},
                {'name': ' North Lincoln Avenue, North Center',
                'lat': '41.9639939',
                'lon': '-87.685725'},
                {'name': ' North Southport Avenue, Wrigleyville',
                'lat': '41.9444316',
                'lon': '-87.6635809'},
                {'name': ' North Clark Street, Wrigleyville',
                'lat': '41.9501029',
                'lon': '-87.6590892'},
                {'name': ' North Wabash Avenue, Loop',
                'lat': '41.8855778',
                'lon': '-87.6260628'},
                {'name': ' North Wood Street, Wicker Park',
                'lat': '41.907666',
                'lon': '-87.672190157947'},
                {'name': ' North Damen Avenue, Wicker Park',
                'lat': '41.9152965',
                'lon': '-87.6777367'},
                {'name': ' North State Street, Magnificent Mile',
                'lat': '41.8906645',
                'lon': '-87.628261'},
                {'name': ' West Hubbard Street, Magnificent Mile',
                'lat': '41.88975655',
                'lon': '-87.6283391876348'},
                {'name': ' West Hubbard Street, Magnificent Mile',
                'lat': '41.8902859',
                'lon': '-87.6289325247656'},
                {'name': ' West Grand Avenue, Magnificent Mile',
                'lat': '41.8913983',
                'lon': '-87.6283923757543'},
                {'name': ' West Hubbard Street, Magnificent Mile',
                'lat': '41.8899261',
                'lon': '-87.629311'},
                {'name': ' West Wolfram Street, Lincoln Park',
                'lat': '41.9336647',
                'lon': '-87.6534457'},
                {'name': ' North Clark Street, Mid-North District',
                'lat': '41.9200282',
                'lon': '-87.6369267'}]


for cafe in cafe_dicts:
    cafe["tooltip"] = cafe['name'] + ", (Starbucks)"
    cafe['color'] = 'green'

# CREDIT THE GITHUB USER WITH ICONS OR SET UP THE REPO WITH OUR ICONS


geojson = dlx.dicts_to_geojson(cafe_dicts)

# generate icon
draw_point = assign("""function(feature, latlng){
const point = L.icon({iconUrl: `https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-${feature.properties.color}.png`, iconSize: [20, 24]});
return L.marker(latlng, {icon: point});
}""")

# Create app.

# I think we can keep them initially as pd dataframe so that we can add “tooltips” easily, and then in our GeoJSON step, we can specify data = json.loads(df.to_json())

# import statement for dropdown
from dash import Dash, html, dcc
'''
app = Dash(prevent_initial_callbacks=True)
app.layout = html.Div(dl.Map([
        dl.LayersControl([
            dl.Overlay(
                dl.LayerGroup([geojson]), name='choropleth', checked=True)
        ]),
        # add another layers control here
        dl.TileLayer(), colorbar
    ], style={'width': '100%', 'height': '50vh', 'margin': "auto", "display": "block"}, id="map")
)
'''
app = Dash()
app.layout = html.Div(
    dl.Map(
        [
            dl.LayersControl(
                [
                    dl.Overlay(
                        dl.LayerGroup([geojson2]), name='choropleth', checked=True),
                    dl.Overlay(
                        dl.LayerGroup(children=[
                            dl.TileLayer(),
                            dl.GeoJSON(data=geojson,
                            cluster=True,
                            options=dict(pointToLayer=draw_point),
                            zoomToBounds=True)]), name='starbucks', checked=True)]),
                    dl.TileLayer(), colorbar
                ],
        zoom=10,
        center=(41.8781, -87.5298),
    ),
    style={
        'width': '100%', 'height': '50vh', 'margin': "auto", "display": "block",
    }, id='map'
)


@app.callback(Output("info", "children"), [Input("geojson", "hover_feature")])
def info_hover(feature):
    return get_info(feature)


if __name__ == '__main__':
    app.run_server()


