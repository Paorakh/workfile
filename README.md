# What is a workfile
Workfile is a project specification file with extension __.work__ or __.workfile__
*In the future, for different usecases of Workfiles, separate extensions shall be recommended. *

It is a Markdown compatible text file, that contains an overall project milestones including assignments, priorities, deadlines, tasks etc in a single text file. 

## Inspiration
There are several project management tools available today. Each one has its pros and cons. A varying range of such tools exist because we have our own preferences. Workfile doesn't claim the best way to manage a project, but it definitely provides a different approach to project definition - better call it a __Common Sense__ approach.

## So much of Common Sense ?
__We go on a shopping with a shopping list.__ Workfile starts with something as simple as a text file where you simply remember and list down the things you want to do.
__Workfile__ is inspired by that instinct.

## Portability
Want to move a project file from a product to another ? Workfile specification can be for one of those several usecases. 

## Demo Setup (Heroku)
[https://workfile.herokuapp.com/](https://workfile.herokuapp.com/)

# Workfile v1.0.0 Specifications
*First draft - 11th April, 2020*

## Syntax
- A workfile is written in a simple text format very much inspired by the markdown format.
- A workfile has its extension .work
- Each line in a workfile has a distinct purpose. It has to be one of the variables that defines a project
- The spec follows the syntax as __TOKEN_CHARACTER__ <space> *Corresponding information* eg. `# Namespace / Project Name`, `@u:username`, etc
- Multiline description is supported. Each line starting without any special token represents the description and description is supported by projects, tasks and milestones
  
## Terminology
- **Namespace** : Department or something similar
- **Project** : The project (the macro definition of what needs to be done) in few words
- **deadline** : The last day to finish something
- **Milestone** : Usually a checklist with deadline
- **Task** : A smallest unit of job to be finished 
- **Users** : Direct members involved in a project, milestone or task eg. @johndoe
- **Groups** : The set of predefined members involved in a project eg. managers
- **Priority** : A descriptive word to define the intensity of a job eg. high, low, etc

## Tokens
Tokens define the grammar of a workfile.
| Workfile Token 	| Corresponding project parameter 	| Query Params 	|
|----------------	|-----------------------------------------------	|----------------------------------------------------------------------------	|
| # 	| Namespace or Project Name 	| # Sysadmin / Hardware Upgrade and Migration 	|
| @u: 	| User, whom the task / project is assigned to 	| @u:johndoe 	|
| @g: 	| Group, whom the task / project is assigned to 	| @g:sysadmin 	|
| > 	| Starting date or Deadline 	| > 2020-04-11 > 2020-04-30 	|
| `no token` | A line in any paragraph (desc) 	| (No token means a description text). ... 	|
| ## 	| Milestone 	| ## Hardware Procurement 	|
| $ 	| Priority 	| $ High 	|
| - 	| A task 	| - Vendor Finalizing 	|
| `whitespace (space or tab)` - 	| A subtask 	| (should begin with a whitespace) - Vendor Assessment |
| ** | A line of comment | ** This is a comment | 


## Parser
Few parsers available. Looking for contributors who find .workfile as one good way to spec a project.
- Python (workfileparser.py)
- PHP (workfileparser.php)

## Sample workfile
Some of the sample workfiles are available in this repo. A simple workfile looks like :
```
** A sample workfile
** This is a comment
** Comment is ignored by parsers
** Comments start with a `*` character

# Namespace/ProjectName
@u:someuser
@g:somegroup
> startdate > deadline

## A milestone
$ Priority
Project description text ...
Project description text second line
project description text third line

** Tasks
- Task 1
  - subtask 1.1
  - subtask 1.2
- Task 2
- Task 3

## Another milestone
> milestone-deadline

** Desc
milestone description text (singleline)

** Tasks
- Task 5
- Task 6
  - subtask 6.2
```

## Limitations
- Subtask don't support assignment, deadlines or any properties. Subtasks are simple checklists
- Attachments currently unsupported, however one can use markdown embed any links as required

## Compatibility with Markdown
- Bolds, Italics are supported as is
- Hyperlinks should work as is
- Markdown and Workfile parsers need to be separately run. Desc blocks can me checked with markdown for more features and rich text supports

# Supported By
Workfile is waiting to have you and your company name to be written below.
