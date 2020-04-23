const { Parser } = require('./parser.js')


var path = "/home/aaeronn/Desktop/dhrubadai/example/sample.txt"

prs = new Parser(path)
console.log(prs.parse())