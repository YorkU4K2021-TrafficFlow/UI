import folium
import GlobalParams


def plot(source: list, destination: list, paths: list) -> None:
    """
    This function visualises the paths in folium and saves the file in `SAVE_TO`
    :param source: a list containing longitude and latitude of source
    :param destination: a list containing longitude and latitude of destination
    :param paths: a list of Path objects
    :return: None
    """

    results_html = ''
    print(source[0])
    print(source)
    mid = [(source[0] + destination[0]) / 2, (source[1] + destination[1]) / 2]
    m = folium.Map(location=mid, zoom_start=12)
    # folium.TileLayer('cartodbdark_matter').add_to(m)
    # folium.TileLayer('stamentoner').add_to(m)
    folium.TileLayer('cartodbpositron').add_to(m)

    # markers
    folium.Marker(
        location=source,
        popup='source',
        icon=folium.Icon(color='green', prefix='fa', icon='home')
    ).add_to(m)

    folium.Marker(
        location=destination,
        popup='destination',
        icon=folium.Icon(color='red', prefix='fa', icon='star')
    ).add_to(m)
    
    i = len(paths) - 1
    for path in paths:
        pts = path.getCoordinates()
        dist = str(round(path.getDistance(), 2)) + 'Km'
        dur = str(round(path.getDuration(), 2)) + ' min' if path.getDuration() < 60 else \
              str(round(path.getDuration() / 60, 2)) + " h"
        trip_name = dist + '<br>' + dur + '<br>'
        results_html = "<button id='path_selector' onclick='selectRoute(" + str(i) + ")' >Trip " + str(i + 1) + \
                        ': <div style="padding-left:10px;">time:' + dur + '</div>' \
                        '<div style="padding-left:10px;">distance: ' + dist + '</div>' \
                        '</button>\n' + results_html
        rand_color = 'black'
        opacity_val = 1 if i == 0 else 0.5

        fg = folium.FeatureGroup(trip_name)
        folium.vector_layers.PolyLine(
            pts,
            popup='<b>' + trip_name + '</b>',
            tooltip=trip_name,
            color=rand_color,
            weight=10,
            opacity=opacity_val
        ).add_to(fg)
        fg.add_to(m)
        i -= 1

    # folium.LayerControl().add_to(m)
    m.get_root().html.add_child(folium.JavascriptLink('static/js/'+GlobalParams.INTERACTIVE_ROUTES))
    m.save('templates/'+GlobalParams.RESULTS)


# source = [43.797632, -79.421758]
# dest = [43.931866, -79.451360]
# paths = Paths(source, dest)
# paths = paths.getPaths()
# plot(source, dest, paths)