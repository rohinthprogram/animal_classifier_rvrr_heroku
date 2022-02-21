from flask import Flask, render_template, request

import requests, json
import os

import base64

from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

classes = list(dict(json.load(open('translation.json'))).values())

def api_call_cellstarthub(img):
    API_KEY = os.environ.get("API_KEY")

    endpoint = "https://animals-classifier-rvrr.herokuapp.com/classify"
    headers = {
    "x-api-key": API_KEY,
    "Content-Type": "application/json"
    }
    
    payload = {'img':img}   
    print(payload)
    # make a get request to load the model (needed if calling api after long time)
    # print(requests.get(endpoint, headers=headers).json())

    # Send POST request to get the output
    response = requests.post(endpoint, headers=headers, data=json.dumps(payload)).json()

    #print(response)
    return response

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == "POST":
        img = request.files['img']
        imgstr = base64.b64encode(img.read()).decode('utf-8')

        output = api_call_cellstarthub(imgstr)
        res = output
        res = list(res[1:-1])
        c = res.index(max(res))
        c = classes[c]

        return render_template('home.html', output=c, log=output)

    return render_template('home.html')


if __name__ == '__main__':
    app.run(debug=True)


