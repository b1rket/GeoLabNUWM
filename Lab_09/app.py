
from flask import Flask, jsonify, request, render_template
import numpy as np
import rasterio
import geopandas as gpd

app = Flask(__name__)

file_path = '../soil_moisture.tif'
with rasterio.open(file_path) as src:
    bbox = src.bounds


@app.route('/get_image_bbox')
def get_image_bbox():
    return jsonify({
        'lat_max': bbox.top,
        'lat_min': bbox.bottom,
        'lon_max': bbox.right,
        'lon_min': bbox.left
    }), 200, {'Content-Type': 'application/json'}

@app.route('/get_moisture_value', methods=['GET'])
def get_moisture_value():
    lat = request.args.get('lat', type=float)
    lon = request.args.get('lon', type=float)

    if (
        lat < bbox.bottom or
        lat > bbox.top or
        lon < bbox.left or
        lon > bbox.right
    ):
        return jsonify({'moisture': 'no data'}), 404, {'Content-Type': 'application/json'}

    with rasterio.open(file_path) as src:
        row, col = src.index(lon, lat)
        moisture = src.read(1)[row, col]

    return jsonify({'moisture': float(moisture)}), 200, {'Content-Type': 'application/json'}

if __name__ == '__main__':
    app.run()
#Запозичено У Рожанчука Богдана
#https://github.com/BogdanJeN/Geo/tree/main/Lab_08
