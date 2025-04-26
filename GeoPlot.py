import folium
from folium import IFrame
import json

def lat_dms_to_decimal(lat_dms_str):
    if not lat_dms_str:
        return None
    degrees = int(lat_dms_str[:2])
    minutes = int(lat_dms_str[2:4])
    seconds = int(lat_dms_str[4:6])
    direction = lat_dms_str[-1]

    lat_decimal = degrees + minutes / 60 + seconds / 3600

    if direction in ['S']:
        lat_decimal = -lat_decimal
    return lat_decimal

def lon_dms_to_decimal(lon_dms_str):
    if not lon_dms_str:
        return None
    degrees = int(lon_dms_str[:3])
    minutes = int(lon_dms_str[3:5])
    seconds = int(lon_dms_str[5:7])
    direction = lon_dms_str[-1]

    lon_decimal = degrees + minutes / 60 + seconds / 3600

    if direction in ['W']:
        lon_decimal = -lon_decimal
    return lon_decimal


def plot_faa_notices(json_filename="faa_notices.json", output_html="faa_notices_map.html"):
    with open(json_filename, "r", encoding="utf-8") as f:
        notices = json.load(f)

    mymap = folium.Map(location=[39.8283, -98.5795], zoom_start=5)

    for notice in notices:
        lat_dms = notice.get("latitude")
        lon_dms = notice.get("longitude")


        if lat_dms and lon_dms:
            lat = lat_dms_to_decimal(lat_dms)
            lon = lon_dms_to_decimal(lon_dms)


            if lat is not None and lon is not None:
                title = notice.get("title", "No Title")
                description = notice.get("description", "No description")
                link = notice.get("link", "No link")


                html_content = f"""
                    <html>
                    <body>
                        <h4><a href="{link}" target="_blank">{title}</a></h4>
                        <p style="width: 250px;">{description}</p>
                    </body>
                    </html>
                    """

                iframe = folium.IFrame(html_content, width=300, height=400)
                popup = folium.Popup(iframe, max_width=600)

                folium.Marker(
                    location=[lat, lon],
                    popup=popup,
                    icon=folium.Icon(color="blue", icon="info-sign")
                ).add_to(mymap)

                miles_radius = 100
                miles_to_meters = miles_radius * 1609.34
                folium.Circle(
                    location=[lat, lon],
                    radius=miles_to_meters,
                    color='red',
                    fill=True,
                    fill_opacity=0.2
                ).add_to(mymap)

    mymap.save(output_html)
    print(f"\n Map saved as {output_html}")
