#!/usr/bin/env python

import re
import sys

class Project:
	name = None
	namespace = None
	users = []
	groups = []
	milestones = []
	deadline = None
	desc = []

	def __init__(self, namespace=None, name=None, users=[], groups=[], milestones=[], deadline=None, desc=[]):
		self.namespace = namespace
		self.name = name
		self.users = users
		self.groups = groups
		self.milestones = milestones
		self.deadline = deadline
		self.desc = desc

	def serialize(self):
		dump = dict(namespace=self.namespace, name=self.name, users=self.users, groups=self.groups, deadline=self.deadline, desc="\n".join(self.desc))
		dump['milestones'] = []
		for m in self.milestones:
			dump['milestones'].append(m.serialize())

		return dump

class Milestone:
	name = None
	users = []
	groups = []
	deadline = None
	priority = None
	desc = []
	tasks = []

	def __init__(self, name):
		self.name = name
		self.users = []
		self.groups = []
		self.deadline = None
		self.desc = []
		self.priority = "Normal"
		self.tasks = []

	def serialize(self):
		dump = dict(name=self.name, users=self.users, groups=self.groups, deadline=self.deadline, priority=self.priority, desc="\n".join(self.desc), tasks=[])
		for t in self.tasks:
			dump['tasks'].append(t.serialize())

		return dump

class Task:
	name = None
	users = []
	groups = []
	deadline = None
	priority = None
	subtasks = []
	desc = []

	def __init__(self, name):
		self.name = name
		self.users = []
		self.groups = []
		self.deadline = None
		self.priority = "Normal"
		self.subtasks = []

	def serialize(self):
		dump = dict(name=self.name, users=self.users, groups=self.groups, deadline=self.deadline, priority=self.priority, desc="\n".join(self.desc), subtasks=self.subtasks)
		return dump

class TokenParser:
	project = None
	task = None
	milestone = None

	TOKENS = {
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

	_PARSER = None

	def __init__(self):
		self.project = Project()

	def regetattr(self, traversal):
		attrs = traversal.split(".")
		last_attr = self
		for someattr in attrs:
			last_attr = getattr(last_attr, someattr)

	@property
	def regex_parser(self):
		if self._PARSER is not None:
			return self._PARSER

		TOKENS_REGEX='(@u:|@g:)\>(#|##)\!\*\-(\s+\-)\$'
		REGEX = f'^([{TOKENS_REGEX}]+)\s*(.*)$'
		self._PARSER = re.compile(REGEX)

		return self._PARSER

	def _parse_line(self, workline):
		workline = workline.rstrip()
		if not workline:
			return

		matches = self.regex_parser.match(workline)
		if not matches:
			token = "desc"
			data = workline
		else:	
			switch, data = matches.groups()
			token = self.TOKENS.get(switch.rstrip())

			# Markdown compatibility for subtasks
			if token is None:
				token = "subtasks"
			elif token == "comment":
				# comments are igored
				return

		token_fn = getattr(self, f"process_{token}")
		if token != 'project' and self.project.name is None:
			raise ValueError("Project needs to be defined first")

		token_fn(data)

	def parse_file(self, workdoc):
		for line in workdoc.readlines():
			self._parse_line(line)

		return self.project.serialize()
		
	def parse_string(self, workfile_text):
		for line in workfile_text.split('\n'):
			self._parse_line(line)

		return self.project.serialize()
	
	def process_project(self, data):
		if self.project.name is not None:
			raise ValueError("Project already defined")

		if "/" in data:
			namespace, name = data.split("/", 2)
		else:
			namespace = None
			name = data

		self.project.name = name.strip()
		self.project.namespace = namespace.strip()

	def _update_active_context_node(self, nodeproperty, value):
		obj = None
		if self.task is not None:
			activenode="task"
			obj = self.project.milestones[self.milestone].tasks[self.task]
		elif self.milestone is not None:
			activenode ="milestone"
			obj = self.project.milestones[self.milestone]
		else:
			activenode="project"
			obj = self.project

		current_value = getattr(obj, nodeproperty)
		if isinstance(current_value, list):
			current_value.append(value)
		else:
			setattr(obj, nodeproperty, value)

	def process_users(self, data):
		self._update_active_context_node("users", data)

	def process_groups(self, data):
		self._update_active_context_node("groups", data)

	def process_tasks(self, data):
		if self.milestone is None:
			self.process_milestones("Project tasks")

		value = Task(name=data)
		self.task = None # reset
		self._update_active_context_node("tasks", value)
		self.task = len(self.project.milestones[-1].tasks) -1  # get last reference

	def process_subtasks(self, data):
		if self.task is None:
			raise ValueError("A subtask needs a parent task")
		self._update_active_context_node("subtasks", data)

	def process_milestones(self, data):
		newmilestone = Milestone(name=data)
		self.project.milestones.append(newmilestone)

		self.milestone = len(self.project.milestones) - 1
		self.task = None

	def process_deadline(self, data):
		self._update_active_context_node("deadline", data)

	def process_priority(self, data):
		self._update_active_context_node("priority", data)

	def process_desc(self, data):
		self._update_active_context_node("desc", data)

if __name__ == "__main__":
	try:
		workfile = sys.argv[1]
		workdoc = open(workfile, "r")
	except IndexError:
		raise ValueError("Please provide a .work file")
	except IOError:
		raise ValueError("Unable to open / read the file")

	tokenparser = TokenParser()
	project_dump = tokenparser.parse_file(workdoc)
	print(project_dump)
	#print(json.dumps(project_dump, indent=2))