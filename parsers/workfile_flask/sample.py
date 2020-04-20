import os
import sys

sys.path.append(
	os.path.join(os.getcwd(), "../workfile_py")
)

from flask import Flask
from flask import request
from flask import render_template
import workfileparser

app = Flask(__name__)

@app.route('/parse', methods=['POST'])
def workfile_parser():
	payload = str(request.get_data())
	parser = workfileparser.TokenParser()
	project = parser.parse_string(payload)
	return render_template("workfile.html", project=project)	

if __name__ == '__main__':
    app.run(debug=True, port=5000) #run app in debug mode on port 5000
