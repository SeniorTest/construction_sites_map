import base64
import json
import glob
import time

# external modules
import dash
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import folium
from folium.plugins import MarkerCluster
from folium import FeatureGroup, LayerControl

# ------------- configuration
project_cards_folder = 'project_cards'


# ------------ functions
def create_map():
    status_color_map = {
        'unknown': 'gray',
        'planned': 'blue',
        'under construction': 'green'
    }

    m = folium.Map(location=[51.4392, 6.9804], zoom_start=12)

    marker_cluster = MarkerCluster().add_to(m)

    constructions_sites = []

    for file in glob.glob(project_cards_folder + '/*.json'):
        print(file)
        with open(file) as construction_site_json:
            data = json.load(construction_site_json)
            print(data)
            constructions_sites.append(data)

    constructions_sites_feature_group = FeatureGroup(name='Projects')

    # get all project status and create subgroups based on the status
    sub_groups = list(set([cs['constructionSite'].get('status', 'unknown') for cs in constructions_sites]))
    feature_groups = dict()
    for sub_group in sub_groups:
        feature_groups[sub_group] = folium.plugins.FeatureGroupSubGroup(marker_cluster, sub_group)

    for cs in constructions_sites:
        status = cs['constructionSite'].get('status', 'unknown')
        used_layer = feature_groups[status]

        folium.GeoJson(
            cs['constructionSite']['geojson'],
            name='geojson',
        ).add_to(used_layer)

        try:
            coordinates = cs['constructionSite']['geojson']['geometry']['coordinates']
        except KeyError:
            coordinates = cs['constructionSite']['geojson']['features'][0]['geometry']['coordinates']

        # get location for marker based on the first pair of coordinates
        if isinstance(coordinates[0], list):
            # for polygons
            location = [coordinates[0][0][1],
                        coordinates[0][0][0]]
        elif isinstance(coordinates[0], float):
            # for points
            location = [coordinates[1], coordinates[0]]
        else:
            print('--------- unknown coordinate format')

        popup = folium.Popup(cs['constructionSite']['marker'], max_width=2650)

        folium.Marker(
            location=location,
            popup=popup,
            icon=folium.Icon(color=status_color_map[status])
        ).add_to(used_layer)

    constructions_sites_feature_group.add_to(m)

    print(feature_groups)
    for k, v in feature_groups.items():
        print(k)
        print(v)
        v.add_to(m)
    LayerControl().add_to(m)

    html_file_name = 'index_' + str(time.time()) + '.html'
    m.save('map/' + html_file_name)
    return html_file_name


def parse_contents(contents, filename):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)

    try:
        if '.json' in filename:
            with open(project_cards_folder + '/' + filename, 'w') as json_file:
                json_file.write(decoded.decode('utf-8'))
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return filename


# ------- app layout
stock_injection_form = dbc.Row([
    dbc.Col(
        dbc.FormGroup(
            [
                html.Br(),
                dbc.Label("Upload a json file with geojson data"),
                html.Br(),
                dcc.Upload(
                    id='upload-data',
                    children=html.Div([
                        'Drag and Drop or ',
                        html.A('Select Files')
                    ]),
                    style={
                        'width': '100%',
                        'height': '60px',
                        'lineHeight': '60px',
                        'borderWidth': '1px',
                        'borderStyle': 'dashed',
                        'borderRadius': '5px',
                        'textAlign': 'center',
                        'margin': '10px'
                    },
                    # Allow multiple files to be uploaded
                    multiple=True
                ),
            ]
        ),
        width=12,
    ),
    dbc.Col(
        dbc.FormGroup(
            [
                html.Div(id='file_upload_output')
            ]
        )
    )])

app = dash.Dash()

if not glob.glob("map/*.html"):
    create_map()

srcDoc = open(glob.glob("map/*.html")[-1], 'r').read()

app.layout = html.Div([
    html.H1('Construction Sites Visualization'),
    html.Iframe(id='map', srcDoc=srcDoc, width='100%', height='600'),
    html.Button(id='map-submit-button', n_clicks=0, children='Update'),
    stock_injection_form
])


# ----------- callbacks
@app.callback(
    dash.dependencies.Output('map', 'srcDoc'),
    [dash.dependencies.Input('map-submit-button', 'n_clicks')])
def update_map(n_clicks):
    print(n_clicks)
    html_file_name = create_map()
    print('latest map: ' + html_file_name)
    return open('map/' + html_file_name, 'r').read()


@app.callback(Output('file_upload_output', 'children'),
              [Input('upload-data', 'contents')],
              [State('upload-data', 'filename')
               ])
def click_or_upload_data(list_of_contents, filename):
    if not list_of_contents:
        return dash.no_update

    if list_of_contents is not None:
        [parse_contents(c, n) for c, n in zip(list_of_contents, filename)]

        return filename
    else:
        print('---unknown input ... raising PreventUpdate')
        raise PreventUpdate


if __name__ == '__main__':
    app.run_server(debug=True)
