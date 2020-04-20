import os
import sys

sys.path.append(
	os.path.join(os.getcwd(), "../workfile_py")
)

from flask import Flask
from flask import request
from flask import render_template
import workfileparser

import json

app = Flask(__name__)

def get_payload_and_project():
	if request.method == 'POST':
		payload = request.get_data().decode()
	else:
		payload = open(os.path.join(os.getcwd(), "../../examples/01.basicsample.work")).read()

	parser = workfileparser.TokenParser()
	project = parser.parse_string(payload)

	print(payload)

	print(project['users'])

	project_json = json.dumps(project, indent=4)

	return payload, project, project_json

@app.route('/', methods=['POST', 'GET'])
def workfile_html():
	payload, project, project_json = get_payload_and_project()
	return render_template("./workfile.html", project=project, rawdata=payload)

@app.route('/parse/', methods=['POST'])
def workfile_parser():
	payload, project, project_json = get_payload_and_project()
	return render_template("./parsed_output.html", project=project, payload=payload, project_json=project_json)


if __name__ == '__main__':
    app.run(debug=True, port=5000) #run app in debug mode on port 5000
