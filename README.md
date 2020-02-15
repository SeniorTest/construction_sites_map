# construction_sites_map
Using folium and dash to display constructions sites and planned projects on OSM maps.

![](construction_site_screenshot.PNG)

## Idea
Enable easy creation of markers and polygons on maps to mark locations of constructions sites and other interesting spots.
The projects purpose is mainly to play around with the Python modules.

## Implementation
Using Python modules
* https://python-visualization.github.io/folium/quickstart.html
* https://dash.plot.ly/?_ga=2.63984175.1693067226.1579282663-51681835.1574148326

The app provides the possibility to upload a card (json data) containing geojson data together with project status and a link to the project page.
On upload the json data are stored along the app. Clicking on the update button triggers a callback which gets all stored cards and creates polygons on the map from the geojson data and marker for the status containing the link.

## Example data
Below is one example containing all information required to create a new polygon with a marker. Right now it is required to use a json file. It is planned to create an api, which allows to post the data programmatically.
More examples of cards can be found in folder project_cards. The coordinates are generated using http://geojson.io/#map=2/20.0/0.0.

 ``` json
{
  "constructionSite": {
    "geojson": {
      "type": "FeatureCollection",
      "features": [
        {
          "type": "Feature",
          "properties": {},
          "geometry": {
            "type": "Polygon",
            "coordinates": [
              [
                [
                  7.069230079650879,
                  51.463285573389854
                ],
                [
                  7.067384719848633,
                  51.46197544423673
                ],
                [
                  7.070860862731934,
                  51.461467424853744
                ],
                [
                  7.071805000305176,
                  51.462162607847056
                ],
                [
                  7.069230079650879,
                  51.463285573389854
                ]
              ]
            ]
          }
        }
      ]
    },
    "marker": "<a href=\"https://www.mbn.de/portfolio/aldi-nord-campus-in-essen/\" title=\"Aldi-Nord-Campus\">Aldi-Nord-Campus</a>",
    "status": "under construction"
  }
}
 ```
 
## Docker
To create the docker image run
 ```
  docker build -t folium_app .
 ```
 .
 
To run the docker container run
```
docker run -p 8050:8050 -it folium_app
```
. Afterwards go to
[page](http://127.0.0.1:8050).

## Heroku
An easy way to deploy and show the app to others is the usage of [Heroku](https://devcenter.heroku.com). 
After you have created an account, you can run the following commands to deploy your app:

```
heroku container:login
heroku create
heroku container:push web
heroku container:release web
```

References:

[https://devcenter.heroku.com/articles/container-registry-and-runtime](https://devcenter.heroku.com/articles/container-registry-and-runtime)

[https://medium.com/@justkrup/deploy-a-docker-container-free-on-heroku-5c803d2fdeb1](https://medium.com/@justkrup/deploy-a-docker-container-free-on-heroku-5c803d2fdeb1)

 
