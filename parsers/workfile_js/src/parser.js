
const fs = require('fs')

function normalize(str) {
	var _str = str.trim().replace(/^(@u:|@g:|\$|(#|##)\s|\-)/, '').trim()
	return _str
}

class Parser {

	/*
		'@u:' : 'users',
		'@g:' : 'groups',
		'$' : 'priority',
		'##' : 'milestones',
		'#' : 'project',
		'>' : 'deadline',
		'-' : 'tasks', 
		'--' : 'subtasks',
		'*': 'comment'
	*/

	constructor(path) {
		this.path = path
		this.result = {}
	}

	getObjFor(name="tasks") {
		var result = this.result
		var milestones = result.milestones
		if(!milestones) return false
		var milestone = milestones[milestones.length - 1]
		if(!milestone) return false
		var objs = milestone[name]
		if(!objs) return false 
		var obj = objs[objs.length - 1]
		if(!obj) return false
		return obj

	}

	performNamespace(obj, data) {
		var namespace = obj.namespace
		if(!namespace) obj.namespace = normalize(data)
	}

	performName(obj, data) {
		obj.name = data
	}

	performUser(obj, data) {
		var obj = this.getObjFor() || obj
		var users = obj.users
		if(!users) return obj.users = [normalize(data)]
		obj.users.push(normalize(data))
	}

	performGroup(obj, data) {
		var obj = this.getObjFor() || obj
		var groups = obj.groups
		if(!groups) return obj.groups = [normalize(data)]
		obj.groups.push(normalize(data))
	}

	performPriority(obj, data) {
		var obj = this.getObjFor() || obj
		obj.priority = data
	}

	performDescription(obj, data) {
		var obj = this.getObjFor() || obj
		obj.description = normalize(data)
	}

	performMilestones(obj, data) {
		var milestones = this.result.milestones
		var _data = {'name': normalize(data)}
		if(milestones) return milestones.push(_data)
		this.result.milestones = [_data]
	}

	performDeadline(obj, data) {
		var obj = this.getObjFor() || obj
		var date = data.replace(/\s/g,'').split(">")

		var start = ""
		var end = ""
		try{
			start = date[0]
		}catch(err) {}

		try{
			end = date[1]
		}catch(err) {}

		obj['deadline'] = {'start': start, 'end': end}

	}

	performTask(obj, data) {
		var tasks = obj.tasks
		var _data = {'name': normalize(data)}
		if(!tasks) return obj.tasks = [_data]
		tasks.push(_data)

	}

	performSubTask(obj, data) {
		var tasks = obj.tasks
		if(!tasks) return
		var task = tasks[tasks.length - 1]
		if(!task) return 
		var subtasks = task.subtasks
		if(subtasks) return subtasks.push(normalize(data))
		task.subtasks = [normalize(data)]
	}

	performData(obj, line) {

		if(line.startsWith("#") && !line.startsWith("##")) {
			return this.performNamespace(obj, line)
		}

		if(line.startsWith("@u:")) {
			return this.performUser(obj, line)
		}

		if(line.startsWith("@g:")) {
			return this.performGroup(obj, line)
		}

		if(line.startsWith(">")) {
			return this.performDeadline(obj, line)
		}

		if(line.startsWith("$")) {
			return this.performPriority(obj, line)
		}

		if(line.startsWith("##")) {
			return this.performMilestones(obj, line)
		}

		if(line.startsWith("-")) {
			return this.performTask(obj, line)
		}

		if(/^\s/.test(line)) {
			var trimmed = line.trim()
			if(trimmed.startsWith("-")) {
				return this.performSubTask(obj, line)
			}
		}

		this.performDescription(obj, line)

	}

	handleMain(line) {

		var obj = this.result.milestones ? this.result.milestones[this.result.milestones.length - 1] : this.result

		if(!obj) {
			this.result.milestones.push({})
			obj = this.result.milestones[this.result.milestones.length - 1]
		}
	
		this.performData(obj, line)

	}

	parse() {

		const data = fs.readFileSync(this.path, 'UTF-8')

	    const lines = data.split(/\r?\n/)

	    for(var i in lines) {

	    	var line = lines[i]

	    	if(line.startsWith("*")) continue
	    	if(!line) continue

	    	this.handleMain(line)
	    }
	    return this.result
	}
}

exports.Parser = Parser