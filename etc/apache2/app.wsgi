# -*- mode: python -*-
"""Use this file for deploying the API under mod_wsgi.

See http://pecan.readthedocs.org/en/latest/deployment.html for details.
"""
from myproject.api import app

application = app.build_wsgi_app()
