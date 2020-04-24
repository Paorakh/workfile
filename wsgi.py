import os

from parsers.workfile_py import workfileparser
from parsers.workfile_flask.sample import app 

if __name__ == "__main__": 
	is_debug=os.environ.get("WORKFILE_FLASK_DEBUG", True)
	port=os.environ.get("WORKFILE_FLASK_PORT", 5000)

	print(is_debug, port)
	app.run(debug=is_debug, port=port)
