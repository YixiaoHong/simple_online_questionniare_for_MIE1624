from flask import Flask
'''
This file is the package directory of the package “app”. 
It includes several settings and configuration of the website 
package. The secret_key of the webapp is set in this file. 
'''
webapp=Flask(__name__)
from app import main
webapp.secret_key = '\x80\xa9s*\x12\xc7x\xa9d\x1f(\x03\xbeHJ:\x9f\xf0!\xb1a\xaa\x0f\xee'