# EvalAsPython
Sublime Text 3 plugin to evaluate Python code and replace with the result inline.

## Installation
Search for EvalAsPython in package control.

## Usage
Append the result of evaluating the expression on the next line: ```Shift + Enter```
Replace the selected expression with the result: ```Control + Shift + Enter```

## Helper Functions

`sh(cmd)` -> `subprocess.Popen(cmd)` and returns stdout, stderr as a tuple, decoded as utf-8. The current working directory is obtained from the current file's view window. If this does not exist, we default to the home directory.

## Examples
Select these code fragments and press ```Shift + Enter``` to evaluate them:

Execute a shell command: 

    sh(['ls', '-al'])

Download a string from a URL:

    requests.get('http://python.org/').text

Or using curl:

    sh(['curl', 'http://python.org/'])

Join a list of strings:

    "\n".join(['line1', 'line2', 'line3'])

Split strings:

    "field1,field2,field3,field4".split(',')

Sum a bunch of numbers separated by commas:

    sum([int(x) for x in "13,24,97,28".split(',')])

Encode in base 64: 

    base64.encodebytes(b'unencoded message')
