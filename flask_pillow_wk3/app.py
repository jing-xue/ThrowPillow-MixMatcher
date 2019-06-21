from flask import Flask, render_template, request, url_for
import requests
import pandas as pd
import numpy as np
from ast import literal_eval

from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
import psycopg2
import os

recom_path = os.path.join('static','fina_recommendation.csv')
palette_path = os.path.join('static','palette_clean_hex.csv')
pillow = pd.read_csv(recom_path, index_col = 0)
palette = pd.read_csv(palette_path, index_col = 0)

random10 = list(np.array(range(100))*5)


#n = pillow.shape[0]

#Initialize app
app = Flask(__name__, static_url_path='/static')

#Define images to display
#app.config['UPLOAD_FOLDER'] = pillow_folder

#Standard home page. 'index.html' is the file in your templates that has the CSS and HTML for your app
#@app.route('/', methods=['GET', 'POST'])
#def index():
#    return render_template('index.html')

@app.route('/', methods=['GET', 'POST'])
@app.route('/index')
def show_index():
	#i = 7
	full_filename = [os.path.join('static',x) for x in pillow['image'][random10]]
	
	return render_template("index.html", image_list = full_filename, color_list = pillow['user_hex'][random10], number = len(random10))


#After they click the image, the index page redirects to recommendations.html
@app.route('/recommendations', methods=['GET', 'POST'])
def recommendations():
    
    # These are a couple examples of what the user input looks like.

    #1. user enters the total price of the wedding. The name of the variable is arbitrary and doesn't have to be the same but is less confusing later on
    locate = int(request.form['indexnum'])
    #locate = int(request.args.get('clk'))
    
    row = random10[locate]
    position_on_palette = pillow['position_on_pltt'][row]
    user_hex = pillow['user_hex'][row]
    user_img = list(pillow.index.values)[row]

    panel_hex = list(pillow[['match1_hex','match2_hex','match3_hex']].iloc[row,:])
    panel_hex.insert(position_on_palette,user_hex)
    
    panel_img = list(pillow[['match1_img','match2_img','match3_img']].iloc[row,:])
    panel_img.insert(position_on_palette,user_img)
    panel_img_path = [os.path.join('static/Pillow_select',x + '.jpg') for x in panel_img]

    palette_name = pillow['palette_name'][row]
    palette_hex = list(palette.loc[palette_name,['hex1','hex2','hex3','hex4']])
    
    return render_template('recommendations.html', palette_name = palette_name, palette_hex = palette_hex, panel_hex = panel_hex, panel_img_path = panel_img_path)
    










if __name__ == '__main__':
	#this runs your app locally
	app.run(host='0.0.0.0', port=8080, debug=True)