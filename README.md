# What is a workfile
Workfile is a project specification file with extension __.work__. 

It is a Markdown compatible text file, that contains an overall project milestones including assignments, priorities, deadlines, tasks etc in a single text file. 

## Inspiration
There are several project management tools available today. Each one has its pros and cons. A varying range of such tools exist because we have our own preferences. Workfile doesn't claim the best way to manage a project, but it definitely provides a different approach to project definition - better call it a "Common Instinct" approach.

## So much of Common Sense ?
__We go on a shopping with a shopping list.__ Workfile starts with something as simple as a text file where you simply remember and list down the things you want to do.
__Workfile__ is inspired by that instinct.

# Workfile v1.0.0 Specifications
*First draft - 11th April, 2020*

## Syntax
- A workfile is written in a simple text format very much inspired by the markdown format.
- A workfile has its extension .work
- Each line in a workfile has a distinct purpose. It has to be one of the variables that defines a project
- The spec follows the syntax as __TOKEN_CHARACTER__ <space> *Corresponding information* eg. `/ Namespace / Project Name`, `@u:username`, etc
- Multiline description is supported. Each line starting with a `!` (bang) represents the description and supported by projects, tasks and milestones
  
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


## Parser
Few parsers available. Looking for contributors who find .workfile as one good way to spec a project.
- Python (workfileparser.py)
- PHP (workfileparser.php)

# Supported By
-
Workfile is waiting to have you and your company name to be written below.