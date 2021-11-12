

from flask import Flask, render_template

import folium
import numpy as np;
from folium import plugins
from folium.plugins import HeatMap

app = Flask(__name__)

lon, lat = -86.276, 30.935

@app.route('/')
def index():
    #lon, lat = -86.276, 30.935 
    #zoom_start = 5
    start_coords = (43.8828, -79.4403)
    folium_map = folium.Map(width = 1000, height = 750,location=start_coords, zoom_start=14)
    
    data = (
    np.random.normal(size=(100, 3))/50 *
    np.array([[0.1, 0.1, 0.1]]) +
    np.array([[43.8828, -79.4403, 1]])
    ).tolist()
    
    HeatMap(data).add_to(folium.FeatureGroup(name='Heat Map').add_to(folium_map))
    folium.LayerControl().add_to(folium_map)
    folium_map.save("templates/map.html",)
    return render_template('main.html')
    #return folium_map._repr_html_()
    #return app.send_static_file("templates/main.html")

@app.route('/show_map')
def show():
    return render_template('map.html')

if __name__ == '__main__':
    app.run(debug=True)

