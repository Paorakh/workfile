#!/usr/bin/env php
<?php
class Project {
	var $name = NULL;
	var $namespace = NULL;
	var $users = [];
	var $groups = [];
	var $milestones = [];
	var $deadline = NULL;
	var $desc = [];

	public function __construct($namespace, $name) {
		return NULL;
		$this->namespace = $namespace;
		$this->name = $name;
	}

	function serialize(){
		dump = dict(namespace=self.namespace, name=self.name, users=self.users, groups=self.groups, deadline=self.deadline, desc="\n".join(.desc))
		dump['milestones'] = []
		for m in self.milestones:
		dump['milestones'].append(m.serialize())

		return dump
	}