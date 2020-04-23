
const fs = require('fs')

class Parser {

	constructor(path) {
		this.path = path
		this.result = {}
	}

	get tokens() {
		return {
			'@u:' : 'users',
			'@g:' : 'groups',
			'$' : 'priority',
			'##' : 'milestones',
			'#' : 'project',
			'>' : 'deadline',
			'-' : 'tasks', 
			'--' : 'subtasks',
			'*': 'comment'
		}
	}


	parse() {

		const data = fs.readFileSync(this.path, 'UTF-8')

	    const lines = data.split(/\r?\n/)

	    for(var i in in lines) {

	    	var isValid = false

	    	var line = lines[i]

	    	isValid = line.startsWith("#") && !line.startsWith("##")

	    	if isValid:
	    		this.result['namespace'] = line 
	    		continue

	    	isValid = line.startsWith("@u:") || line.startsWith("@g:")

	    	if isValid:
	    		this.result['']

	    }
	}
}

exports.Parser = Parser