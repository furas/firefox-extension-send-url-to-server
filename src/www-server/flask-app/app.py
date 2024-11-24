#!/usr/bin/env python3

# author: Bartlomiej "furas" Burek (https://blog.furas.pl)
# date: 2024.11.22

from datetime import datetime
from urllib.parse import unquote
from flask import Flask, request, make_response, jsonify, render_template
import pandas as pd


app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    """Get requests from any client and save it in CSV file.

    https://localhost:8080/?url=....&title=...&tags=...
    
    TODO: Value `localhost:8080` is hardcoded in firefox-extension/background.js
    TODO: Data are append to existing CVS in primitive way (doesn't resolve problem with NEW_LINE, quotes, etc.)
    """
    
    print("request.args:", request.args)

    url = unquote(request.args.get("url", ""))
    title = unquote(request.args.get("title", ""))
    tags = unquote(request.args.get("tags", ""))

    print('url  :', url)
    print('title:', title)
    print('tags :', tags)

    if url:
        dt = datetime.now()
        dt_str = dt.strftime("%Y.%m.%d;%H:%M:%S")
        with open("data.csv", "a") as f_out:
            f_out.write(f"{dt_str};{url};{title};{tags}\n")
        text = {"message": "OK"}
    else:
        text = {"message": "EMPTY"}

    # Firefox extension needs CORS to get response
    response = make_response(jsonify(text))
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"

    return response


@app.route('/data/')
def show_data():
    """Display data from CSV.
    
    It uses values in URL to folder data
    
    https://localhost:8080/data/?date=...&time=...&url=...&title=...&tags=...
    
    Pandas uses regex to filter - so it can use regex rules (example: title=^W - get all title staring with upper W)    
    """
    
    df = pd.read_csv('data.csv', sep=';', names=['date', 'time', 'url', 'title', 'tags'], keep_default_na=False, na_filter=False)
    #html = df.to_html()

    for name in ('date', 'time', 'url', 'title', 'tags'):
        value = unquote(request.args.get(name, ''))
        if value:
            print(f'filter by "{name}" = "{value}"')
            
            column = df[name]
            #print(column)
            
            mask = column.str.contains(value)
            #print(mask)
            
            df = df[mask]
            print('len(df):', len(df))

    return render_template("data.html", data=df)


if __name__ == "__main__":
    app.debug = True  # simpler to comment/uncomment
    app.run(host="0.0.0.0", port=8080)
