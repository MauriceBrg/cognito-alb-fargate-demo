"""Demo app to display the content of the Cognito JWT and provide the logout link"""
import json
import os
import platform

from datetime import datetime

import jwt
import pytz

from flask import Flask, request, render_template, make_response, redirect

app = Flask(__name__)

JWT_HEADER_NAME = "x-amzn-oidc-data"
SESSION_COOKIE_NAME = "AWSELBAuthSessionCookie-0"

@app.route('/')
def home():
    """This is the endpoint for the main website, it displays the JWT"""

    jwt_header = request.headers.get(JWT_HEADER_NAME)

    #WARNING: In production you WANT to verify the signature!
    jwt_decoded = jwt.decode(jwt_header, verify=False)

    variables = {
        "username": jwt_decoded["username"],
        "valid_until_utc": datetime.fromtimestamp(jwt_decoded["exp"],tz=pytz.UTC).isoformat(),
        "jwt_decoded": json.dumps(jwt_decoded, indent=4),
        "hostname": platform.node(),
    }

    return render_template("index.html", **variables)

@app.route('/logout')
def logout():
    """
    This handles the logout action for the app.
    """

    # Looks a little weird, but this is the only way to get an HTTPS redirect
    response = make_response(
        redirect(
            os.environ.get("LOGOUT_URL", f"https://{request.host}/")
        )
    )

    # Invalidate the session cookie
    response.set_cookie(SESSION_COOKIE_NAME, "empty", max_age=-3600)

    return response

if __name__ == '__main__':

    app.run(debug=True, host='0.0.0.0', port=os.environ.get("PORT", 8080))
