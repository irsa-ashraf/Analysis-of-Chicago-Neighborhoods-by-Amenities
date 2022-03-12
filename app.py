
import dash
import dash_leaflet as dl

app = dash.Dash()
app.layout = dl.Map(dl.TileLayer(), style={'width': '1000px', 'height': '500px'}, center=[41.8781, -87.5298], zoom=10)


'''
def cluster_points(df, key, map):

    color = {'pharmacy': 'red', 'library': 'blue',
            'starbucks': 'green', 'murals':'purple'}

    icon = {'pharmacy': 'heart', 'library': 'book',
            'starbucks': 'star', 'murals':'cloud'}

    cluster = plugins.MarkerCluster(name=key).add_to(map)
    for row in df.itertuples():
        folium.Marker(
        location = (row.latitude, row.longitude),
        popup = row.name,
        icon=folium.Icon(color=color[key], icon=icon[key])
        ).add_to(cluster)

'''

if __name__ == '__main__':
    app.run_server(debug=True)

