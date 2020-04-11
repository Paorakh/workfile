#!/usr/bin/env python

import os
import re
import sys
import collections

try:
	workfile = sys.argv[1]
	workdoc = open(workfile, "r")
except IndexError:
	raise ValueError("Please provide a .work file")
except IOError:
	raise ValueError("Unable to open / read the file")

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
		dump = dict(namespace=self.namespace, name=self.name, users=self.users, groups=self.groups, milestones=[], deadline=self.deadline, desc="\n".join(self.desc))
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

	def __init__(self, name, users=[], groups=[], deadline=None, priority=None, desc=[], tasks=[]):
		self.name = name
		self.users = users
		self.groups = groups
		self.deadline = deadline
		self.desc = desc
		self.priority = priority
		self.tasks = tasks

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

	def __init__(self, name, users=[], groups=[], deadline=None, priority=None, subtasks=[]):
		self.name = name
		self.users = users
		self.groups = groups
		self.deadline = deadline
		self.priority = priority
		self.subtasks = subtasks

	def serialize(self):
		dump = dict(name=self.name, users=self.users, groups=self.groups, deadline=self.deadline, priority=self.priority, desc="\n".join(self.desc), subtasks=[])
		if self.subtasks:
			for t in self.subtasks:
				dump['subtasks'].append(t.serialize())
		return dump

class TokenParser:
	project = None
	last_context = None	

	TOKENS = {
		'@u:' : 'users',
		'@g:' : 'groups',
		'$' : 'priority',
		'##' : 'milestones',
		'#' : 'project',
		'>' : 'deadline',
		'-' : 'tasks', 
		'--' : 'subtasks'
	}

	_PARSER = None

	def __init__(self):
		self.project = Project()

	@property
	def regex_parser(self):
		if self._PARSER is not None:
			return self._PARSER

		TOKENS_REGEX='(@u:|@g:)\>(#|##)\!\-(\s+\-)\$'
		REGEX = f'^([{TOKENS_REGEX}]+)\s*(.*)$'
		self._PARSER = re.compile(REGEX)

		return self._PARSER

	def run_parser(self, workdoc):
		for line in workdoc.readlines():
			cline = line.rstrip()
			if not cline:
				continue
			
			matches = self.regex_parser.match(cline)
			if not matches:
				token = "desc"
				data = cline
			else:	
				switch, data = matches.groups()
				token = self.TOKENS.get(switch.rstrip())

				# Markdown compatibility for subtasks
				if token is None:
					token = "subtasks"

			self.process(token, data)

		import pdb
		pdb.set_trace()
	
		self.finalize()
		return self.project.serialize()

	def process(self, token, data):
		if token is None:
			return
		token_fn = getattr(self, f"process_{token}")
		if token != 'project' and self.project.name is None:
			raise ValueError("Project needs to be defined first")

		token_fn(data)
	
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

		self.last_context = "project"

	def _process_usergroup_scope(self, user_or_group):
		if self.milestone:
			scope = self.task if self.task else self.milestone
		else:
			scope = self.project

		scopelist = scope.users if user_or_group == "users" else scope.groups
		return scopelist

	def process_users(self, data):
		userlist = self._process_usergroup_scope("users")
		userlist.append(data)

	def process_groups(self, data):
		grouplist = self._process_usergroup_scope("groups")
		grouplist.append(data)

	def process_tasks(self, data):
		if not self.milestone: # create default milestone
			self.process_milestones("Project Tasks")

		if self.task:		
			self.milestone.tasks.append(self.task)
			del self.task
		self.task = Task(name=data)

	def process_subtasks(self, data):
		if not self.task:
			raise ValueError("A subtask needs a parent task")
		print("-=", self.task, data)
		self.task.subtasks.append(Task(name=data, subtasks=None))

	def process_milestones(self, data):
		if self.milestone:
			self.project.milestones.append(self.milestone)
			del self.milestone

		self.milestone = Milestone(name=data)
	
	def _scope_deadline_priority_desc(self):	
		if self.task:
			objname = "task"
		elif self.milestone:
			objname = "milestone"
		else:
			objname = "project"

		return objname

	def process_deadline(self, data):
		objname = self._scope_deadline_priority_desc()
		setattr(getattr(self, objname), "deadline", data)

	def process_priority(self, data):
		objname = self._scope_deadline_priority_desc()
		setattr(getattr(self, objname), "priority", data)

	def process_desc(self, data):
		objname = self._scope_deadline_priority_desc()
		desc = getattr(getattr(self, objname), "desc")
		desc.append(data)

	def finalize(self):
		if not self.project.name:
			pass
		elif self.task:
			self.milestone.tasks.append(self.task)

		self.project.milestones.append(self.milestone)

tokenparser = TokenParser()
project_dump = tokenparser.run_parser(workdoc)
import json
print(json.dumps(project_dump, indent=2))
