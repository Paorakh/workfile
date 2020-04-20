// Transcrypt'ed from Python, 2020-04-13 19:49:50
var re = {};
var sys = {};
import {AssertionError, AttributeError, BaseException, DeprecationWarning, Exception, IndexError, IterableError, KeyError, NotImplementedError, RuntimeWarning, StopIteration, UserWarning, ValueError, Warning, __JsIterator__, __PyIterator__, __Terminal__, __add__, __and__, __call__, __class__, __envir__, __eq__, __floordiv__, __ge__, __get__, __getcm__, __getitem__, __getslice__, __getsm__, __gt__, __i__, __iadd__, __iand__, __idiv__, __ijsmod__, __ilshift__, __imatmul__, __imod__, __imul__, __in__, __init__, __ior__, __ipow__, __irshift__, __isub__, __ixor__, __jsUsePyNext__, __jsmod__, __k__, __kwargtrans__, __le__, __lshift__, __lt__, __matmul__, __mergefields__, __mergekwargtrans__, __mod__, __mul__, __ne__, __neg__, __nest__, __or__, __pow__, __pragma__, __proxy__, __pyUseJsNext__, __rshift__, __setitem__, __setproperty__, __setslice__, __sort__, __specialattrib__, __sub__, __super__, __t__, __terminal__, __truediv__, __withblock__, __xor__, abs, all, any, assert, bool, bytearray, bytes, callable, chr, copy, deepcopy, delattr, dict, dir, divmod, enumerate, filter, float, getattr, hasattr, input, int, isinstance, issubclass, len, list, map, max, min, object, ord, pow, print, property, py_TypeError, py_iter, py_metatype, py_next, py_reversed, py_typeof, range, repr, round, set, setattr, sorted, str, sum, tuple, zip} from './org.transcrypt.__runtime__.js';
import * as __module_sys__ from './sys.js';
__nest__ (sys, '', __module_sys__);
import * as __module_re__ from './re.js';
__nest__ (re, '', __module_re__);
var __name__ = '__main__';
export var Project =  __class__ ('Project', [object], {
	__module__: __name__,
	py_name: null,
	namespace: null,
	users: [],
	groups: [],
	milestones: [],
	deadline: null,
	desc: [],
	get __init__ () {return __get__ (this, function (self, namespace, py_name, users, groups, milestones, deadline, desc) {
		if (typeof namespace == 'undefined' || (namespace != null && namespace.hasOwnProperty ("__kwargtrans__"))) {;
			var namespace = null;
		};
		if (typeof py_name == 'undefined' || (py_name != null && py_name.hasOwnProperty ("__kwargtrans__"))) {;
			var py_name = null;
		};
		if (typeof users == 'undefined' || (users != null && users.hasOwnProperty ("__kwargtrans__"))) {;
			var users = [];
		};
		if (typeof groups == 'undefined' || (groups != null && groups.hasOwnProperty ("__kwargtrans__"))) {;
			var groups = [];
		};
		if (typeof milestones == 'undefined' || (milestones != null && milestones.hasOwnProperty ("__kwargtrans__"))) {;
			var milestones = [];
		};
		if (typeof deadline == 'undefined' || (deadline != null && deadline.hasOwnProperty ("__kwargtrans__"))) {;
			var deadline = null;
		};
		if (typeof desc == 'undefined' || (desc != null && desc.hasOwnProperty ("__kwargtrans__"))) {;
			var desc = [];
		};
		self.namespace = namespace;
		self.py_name = py_name;
		self.users = users;
		self.groups = groups;
		self.milestones = milestones;
		self.deadline = deadline;
		self.desc = desc;
	});},
	get serialize () {return __get__ (this, function (self) {
		var dump = dict (__kwargtrans__ ({namespace: self.namespace, py_name: self.py_name, users: self.users, groups: self.groups, deadline: self.deadline, desc: '\n'.join (self.desc)}));
		dump ['milestones'] = [];
		for (var m of self.milestones) {
			dump ['milestones'].append (m.serialize ());
		}
		return dump;
	});}
});
export var Milestone =  __class__ ('Milestone', [object], {
	__module__: __name__,
	py_name: null,
	users: [],
	groups: [],
	deadline: null,
	priority: null,
	desc: [],
	tasks: [],
	get __init__ () {return __get__ (this, function (self, py_name) {
		self.py_name = py_name;
		self.users = [];
		self.groups = [];
		self.deadline = null;
		self.desc = [];
		self.priority = 'Normal';
		self.tasks = [];
	});},
	get serialize () {return __get__ (this, function (self) {
		var dump = dict (__kwargtrans__ ({py_name: self.py_name, users: self.users, groups: self.groups, deadline: self.deadline, priority: self.priority, desc: '\n'.join (self.desc), tasks: []}));
		for (var t of self.tasks) {
			dump ['tasks'].append (t.serialize ());
		}
		return dump;
	});}
});
export var Task =  __class__ ('Task', [object], {
	__module__: __name__,
	py_name: null,
	users: [],
	groups: [],
	deadline: null,
	priority: null,
	subtasks: [],
	desc: [],
	get __init__ () {return __get__ (this, function (self, py_name) {
		self.py_name = py_name;
		self.users = [];
		self.groups = [];
		self.deadline = null;
		self.priority = 'Normal';
		self.subtasks = [];
	});},
	get serialize () {return __get__ (this, function (self) {
		var dump = dict (__kwargtrans__ ({py_name: self.py_name, users: self.users, groups: self.groups, deadline: self.deadline, priority: self.priority, desc: '\n'.join (self.desc), subtasks: self.subtasks}));
		return dump;
	});}
});
export var TokenParser =  __class__ ('TokenParser', [object], {
	__module__: __name__,
	project: null,
	task: null,
	milestone: null,
	TOKENS: dict ({'@u:': 'users', '@g:': 'groups', '$': 'priority', '##': 'milestones', '#': 'project', '>': 'deadline', '-': 'tasks', '--': 'subtasks', '*': 'comment'}),
	_PARSER: null,
	get __init__ () {return __get__ (this, function (self) {
		self.project = Project ();
	});},
	get regetattr () {return __get__ (this, function (self, traversal) {
		var attrs = traversal.py_split ('.');
		var last_attr = self;
		for (var someattr of attrs) {
			var last_attr = getattr (last_attr, someattr);
		}
	});},
	get _get_regex_parser () {return __get__ (this, function (self) {
		if (self._PARSER !== null) {
			return self._PARSER;
		}
		var TOKENS_REGEX = '(@u:|@g:)\\>(#|##)\\!\\*\\-(\\s+\\-)\\$';
		var REGEX = '^([{}]+)\\s*(.*)$'.format (TOKENS_REGEX);
		self._PARSER = re.compile (REGEX);
		return self._PARSER;
	});},
	get parse () {return __get__ (this, function (self, workdoc) {
		for (var line of workdoc.readlines ()) {
			var cline = line.rstrip ();
			if (!(cline)) {
				continue;
			}
			var matches = self.regex_parser.match (cline);
			if (!(matches)) {
				var token = 'desc';
				var data = cline;
			}
			else {
				var __left0__ = matches.groups ();
				var py_switch = __left0__ [0];
				var data = __left0__ [1];
				var token = self.TOKENS.py_get (py_switch.rstrip ());
				if (token === null) {
					var token = 'subtasks';
				}
				else if (token == 'comment') {
					continue;
				}
			}
			var token_fn = getattr (self, 'process_{}'.format (token));
			if (token != 'project' && self.project.py_name === null) {
				var __except0__ = ValueError ('Project needs to be defined first');
				__except0__.__cause__ = null;
				throw __except0__;
			}
			token_fn (data);
		}
		return self.project.serialize ();
	});},
	get process_project () {return __get__ (this, function (self, data) {
		if (self.project.py_name !== null) {
			var __except0__ = ValueError ('Project already defined');
			__except0__.__cause__ = null;
			throw __except0__;
		}
		if (__in__ ('/', data)) {
			var __left0__ = data.py_split ('/', 2);
			var namespace = __left0__ [0];
			var py_name = __left0__ [1];
		}
		else {
			var namespace = null;
			var py_name = data;
		}
		self.project.py_name = py_name.strip ();
		self.project.namespace = namespace.strip ();
	});},
	get _update_active_context_node () {return __get__ (this, function (self, nodeproperty, value) {
		var obj = null;
		if (self.task !== null) {
			var activenode = 'task';
			var obj = self.project.milestones [self.milestone].tasks [self.task];
		}
		else if (self.milestone !== null) {
			var activenode = 'milestone';
			var obj = self.project.milestones [self.milestone];
		}
		else {
			var activenode = 'project';
			var obj = self.project;
		}
		var current_value = getattr (obj, nodeproperty);
		if (isinstance (current_value, list)) {
			current_value.append (value);
		}
		else {
			setattr (obj, nodeproperty, value);
		}
	});},
	get process_users () {return __get__ (this, function (self, data) {
		self._update_active_context_node ('users', data);
	});},
	get process_groups () {return __get__ (this, function (self, data) {
		self._update_active_context_node ('groups', data);
	});},
	get process_tasks () {return __get__ (this, function (self, data) {
		if (self.milestone === null) {
			self.process_milestones ('Project tasks');
		}
		var value = Task (__kwargtrans__ ({py_name: data}));
		self.task = null;
		self._update_active_context_node ('tasks', value);
		self.task = len (self.project.milestones [-(1)].tasks) - 1;
	});},
	get process_subtasks () {return __get__ (this, function (self, data) {
		if (self.task === null) {
			var __except0__ = ValueError ('A subtask needs a parent task');
			__except0__.__cause__ = null;
			throw __except0__;
		}
		self._update_active_context_node ('subtasks', data);
	});},
	get process_milestones () {return __get__ (this, function (self, data) {
		var newmilestone = Milestone (__kwargtrans__ ({py_name: data}));
		self.project.milestones.append (newmilestone);
		self.milestone = len (self.project.milestones) - 1;
		self.task = null;
	});},
	get process_deadline () {return __get__ (this, function (self, data) {
		self._update_active_context_node ('deadline', data);
	});},
	get process_priority () {return __get__ (this, function (self, data) {
		self._update_active_context_node ('priority', data);
	});},
	get process_desc () {return __get__ (this, function (self, data) {
		self._update_active_context_node ('desc', data);
	});}
});
Object.defineProperty (TokenParser, 'regex_parser', property.call (TokenParser, TokenParser._get_regex_parser));;

// Example
/**
var parser = Tokenparser();
parser.parse("# Namespace / Project \n @u:someuser")
**/

//# sourceMappingURL=workfileparser.map
