from flask import Flask
from flask import request
from compute_similarity import weighted_search

app = Flask(__name__)



@app.route("/api/search",methods=['GET', 'POST'])
def search():
    json_data = request.get_json()
    people = json_data["people"].strip()
    organization = json_data["org"].strip()
    location = json_data["loc"].strip()
    date = json_data["date"].strip()

    top_10 = weighted_search(people, location, organization, date, 100)
    
    output = ""
    for fn, s in top_10:
        if not fn.endswith("story"):
            output += fn + ".story" + "\n"
        else:
            output += fn + "\n"

    return {"result": output}
    


if __name__ == '__main__':
    app.run()