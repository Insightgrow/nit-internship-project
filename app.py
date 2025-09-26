from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

@app.route("/synthesize", methods=["POST"])
def synthesize():
    data = request.get_json()
    print(data)
    er = data.get("er")
    h = data.get("h")
    formula = data.get("formula")
    zo = data.get("zo")
    elecLen = data.get("elecLen")


    
    #calculations for synthesize
    
    
    
    

    # dummy result
    result = {
        "width_mm": 2.02,
        "length_mm": 3.02
    }
    return jsonify(result)

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    print(data)
    width = data.get("width_mm")
    length = data.get("length_mm")
    formula = data.get("formula")
    width_mm = data.get("width_mm")
    length_mm = data.get("length_mm")

    #calculation for analyze


    
    #dummy result
    result = {
        "zo": 50.0,
        "elecLen": 90.0
    }
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
