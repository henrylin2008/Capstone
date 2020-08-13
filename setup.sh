#!/bin/sh
export AUTH0_DOMAIN='.us.auth0.com'
export ALGORITHMS=['RS256']
export API_AUDIENCE='casting'
export CLIENT_ID=''

export FLASK_APP=app.py
export FLASK_DEBUG=true
export DATABASE_URL='postgres://'

