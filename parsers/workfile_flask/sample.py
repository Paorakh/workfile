import os
import sys
import json

from flask import Flask
from flask import request
from flask import render_template
from flask import abort, make_response

from parsers.workfile_py import workfileparser

app = Flask(__name__)

def get_payload_and_project():
	if request.method == 'POST':
		payload = request.get_data().decode()
	else:
		payload = open("examples/01.basicsample.work").read()

	try:
		parser = workfileparser.TokenParser()
		project = parser.parse_string(payload)

		project_json = json.dumps(project, indent=4)
	except Exception as exc:
		return False, payload, None, None, str(exc)

	return True, payload, project, project_json, "OK"

@app.route('/', methods=['POST', 'GET'])
def workfile_html():
	status, payload, project, project_json, msg = get_payload_and_project()
	if status is False:
		return make_response(msg, 400)
	return render_template("./workfile.html", project=project, rawdata=payload)

@app.route('/parse/', methods=['POST'])
def workfile_parser():
	status, payload, project, project_json, msg = get_payload_and_project()
	if status is False:
		return make_response(msg, 400)
	return render_template("./parsed_output.html", project=project, payload=payload, project_json=project_json)


@app.route('/save/', methods=['POST'])
def save():
	filename = request.form.get('filename').split("/")[-1]
	contents = request.form.get('content')

	ff=open(f"parsers/workfile_flask/saved_files/{filename}.workfile", "w")
	ff.write(contents)
	ff.close()

	return make_response(f"File saved as {filename}")
	

@app.route('/load/', methods=['POST'])
def load_file():
	filename = request.form.get('filename').split("/")[-1]

	ff=open(f"parsers/workfile_flask/saved_files/{filename}.workfile", "r")
	dump = ff.read()
	ff.close()

	return make_response(dump)
	
