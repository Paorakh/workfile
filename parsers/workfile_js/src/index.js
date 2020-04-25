const { Parser } = require('./parser.js')


var path = "/home/aaeronn/Documents/dhrubadai/workfile/examples/01.basicsample.work"

prs = new Parser(path)
data = prs.parse()
console.log(data)