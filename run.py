#!venv/bin/python
from app import webapp

#webapp.run('0.0.0.0',5001,debug=True)
#webapp.run('0.0.0.0',5001)

webapp.run('0.0.0.0',5000, debug=True)
