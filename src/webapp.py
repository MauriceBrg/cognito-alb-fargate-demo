"""Demo app to display the content of the Cognito JWT and provide the logout link"""
import json
import os
import platform

from datetime import datetime

import jwt
import requests
import pytz

from flask import Flask, request, render_template, make_response, redirect

app = Flask(__name__)

JWT_HEADER_NAME = "x-amzn-oidc-data"
ACCESS_TOKEN_HEADER_NAME = "x-amzn-oidc-accesstoken"
IDENTITY_HEADER_NAME = "x-amzn-oidc-identity"
SESSION_COOKIE_NAME = "AWSELBAuthSessionCookie-0"

@app.route('/')
def home():
    """This is the endpoint for the main website, it displays the JWT"""

    jwt_header = request.headers.get(JWT_HEADER_NAME)

    #WARNING: In production you WANT to verify the signature!
    jwt_decoded = jwt.decode(jwt_header, verify=False)


    variables = {
        "username": jwt_decoded.get("username", "N/A"),
        "identity": request.headers.get(IDENTITY_HEADER_NAME),
        "access_token": request.headers.get(ACCESS_TOKEN_HEADER_NAME),
        "valid_until_utc": datetime.fromtimestamp(jwt_decoded["exp"],tz=pytz.UTC).isoformat(),
        "jwt_decoded": json.dumps(jwt_decoded, indent=4),
        "jwt_encoded": jwt_header,
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

@app.route("/healthcheck")
def health_check():
    """Returns OK"""

    return render_template("health_check.html")

@app.route("/userinfo")
def user_info():
    """Calls the Cognito User Info endpoint"""

    url = os.environ.get("USER_INFO_URL")
    access_token = request.headers.get(ACCESS_TOKEN_HEADER_NAME)

    response = requests.get(url, headers={"Authorization": f"Bearer {access_token}"})

    return render_template(
        "user_info.html",
        user_info=json.dumps(response.json(), indent=4),
        url=url,
        access_token=access_token,
    )


if __name__ == '__main__':

    app.run(debug=True, host='0.0.0.0', port=os.environ.get("PORT", 8080))
