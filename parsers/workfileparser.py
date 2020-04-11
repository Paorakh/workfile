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

tokens='(@u:|@g:)\>\/#!\-'
regex = f'^\s*([{tokens}]+)\s*(.*)$'
reparser = re.compile(regex)

class Project:
	name = None
	users = []
	groups = []
	milestones = []
	deadline = None
	desc = []

	def __init__(self, name=None, users=[], groups=[], milestones=[], deadline=None, desc=[]):
		self.name = name
		self.users = users
		self.groups = groups
		self.milestones = milestones
		self.deadline = deadline
		self.desc = desc

	def serialize(self):
		dump = dict(name=self.name, users=self.users, groups=self.groups, milestones=[], deadline=self.deadline, desc="\n".join(self.desc))
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
		for t in self.subtasks:
			self.subtasks.append(t.serialize())
		return dump

class TokenParser:
	project = None
	milestone = None
	task = None
	tokens = {
		'@u:' : 'users',
		'@g:' : 'groups',
		'##' : 'priority',
		'#' : 'milestones',
		'/' : 'project',
		'>' : 'deadline',
		'!' : 'desc',
		'-' : 'tasks'
	}

	def __init__(self):
		self.project = Project()

	def do(self, token, data):
		if token is None:
			return
		print(token, "===", data)
		token_fn = getattr(self, f"process_{token}")
		if token != 'project' and self.project.name is None:
			raise ValueError("Project needs to be defined first")

		token_fn(data)
	
	def process_project(self, data):
		if self.project.name is not None:
			raise ValueError("Project already defined")

		self.project.name = data

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
		self.task = Task(name=data)

	def process_milestones(self, data):
		if self.milestone:
			self.project.milestones.append(self.milestone)

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

def parse_doc(tokenparser):
	for line in workdoc.readlines():
		cline = line.strip()
		matches = reparser.match(cline)
		if not matches:
			continue
	
		switch, data = matches.groups()

		token = TokenParser.tokens.get(switch)
		tokenparser.do(token, data)

	tokenparser.finalize()
	return tokenparser.project.serialize()

tokenparser = TokenParser()
project_dump = parse_doc(tokenparser)

print(project_dump)
