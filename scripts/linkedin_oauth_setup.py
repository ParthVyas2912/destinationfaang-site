"""Create a LinkedIn OAuth access token and save it to GitHub Secrets.

Run locally from the repo root:
  python scripts/linkedin_oauth_setup.py

Required environment variables:
  LINKEDIN_CLIENT_ID
  LINKEDIN_CLIENT_SECRET

The script starts a temporary localhost callback server, opens LinkedIn's
authorization URL, exchanges the returned code for an access token, and stores
the token as the repository secret LINKEDIN_ACCESS_TOKEN using the gh CLI.
"""

import json
import os
import secrets
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer


AUTH_URL = "https://www.linkedin.com/oauth/v2/authorization"
TOKEN_URL = "https://www.linkedin.com/oauth/v2/accessToken"
SCOPES = ["openid", "profile", "w_organization_social"]
SECRET_NAME = "LINKEDIN_ACCESS_TOKEN"
REPO = "ParthVyas2912/destinationfaang-site"


class CallbackHandler(BaseHTTPRequestHandler):
    code = None
    state = None
    error = None

    def log_message(self, format, *args):
        return

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed.query)
        CallbackHandler.code = params.get("code", [None])[0]
        CallbackHandler.state = params.get("state", [None])[0]
        CallbackHandler.error = params.get("error", [None])[0]

        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        if CallbackHandler.code:
            message = "LinkedIn authorization succeeded. You can close this tab."
        else:
            message = "LinkedIn authorization failed. Return to the terminal."
        self.wfile.write(f"<html><body><h1>{message}</h1></body></html>".encode("utf-8"))


def require_env(name):
    value = os.environ.get(name)
    if not value:
        sys.exit(f"Missing {name}. Set it in this terminal before running the script.")
    return value


def callback_url():
    return os.environ.get("LINKEDIN_REDIRECT_URI", "http://localhost:3000/linkedin/callback")


def callback_host_port(redirect_uri):
    parsed = urllib.parse.urlparse(redirect_uri)
    if not parsed.hostname or not parsed.port:
        sys.exit(
            "LINKEDIN_REDIRECT_URI must include a host and port, e.g. "
            "http://localhost:3000/linkedin/callback"
        )
    return parsed.hostname, parsed.port


def exchange_code(client_id, client_secret, code):
    data = urllib.parse.urlencode(
        {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": callback_url(),
            "client_id": client_id,
            "client_secret": client_secret,
        }
    ).encode("utf-8")
    request = urllib.request.Request(
        TOKEN_URL,
        data=data,
        method="POST",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return json.load(response)
    except urllib.error.HTTPError as error:
        details = error.read().decode("utf-8", errors="replace")
        sys.exit(f"LinkedIn token exchange failed with HTTP {error.code}: {details}")


def save_github_secret(access_token):
    result = subprocess.run(
        ["gh", "secret", "set", SECRET_NAME, "--repo", REPO, "--body", access_token],
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        sys.exit(f"Could not save GitHub secret with gh:\n{result.stderr.strip()}")


def main():
    client_id = require_env("LINKEDIN_CLIENT_ID")
    client_secret = require_env("LINKEDIN_CLIENT_SECRET")
    redirect_uri = callback_url()
    callback_host, callback_port = callback_host_port(redirect_uri)
    state = secrets.token_urlsafe(24)
    query = urllib.parse.urlencode(
        {
            "response_type": "code",
            "client_id": client_id,
            "redirect_uri": redirect_uri,
            "scope": " ".join(SCOPES),
            "state": state,
        }
    )
    url = f"{AUTH_URL}?{query}"

    print("Opening LinkedIn authorization in your browser...")
    print(url)
    webbrowser.open(url)

    server = HTTPServer((callback_host, callback_port), CallbackHandler)
    print(f"Waiting for LinkedIn callback at {redirect_uri} ...")
    server.handle_request()

    if CallbackHandler.error:
        sys.exit(f"LinkedIn authorization failed: {CallbackHandler.error}")
    if CallbackHandler.state != state:
        sys.exit("LinkedIn authorization failed: state mismatch.")
    if not CallbackHandler.code:
        sys.exit("LinkedIn authorization failed: no code returned.")

    token_payload = exchange_code(client_id, client_secret, CallbackHandler.code)
    access_token = token_payload.get("access_token")
    if not access_token:
        sys.exit(f"LinkedIn token response did not include access_token: {token_payload}")

    save_github_secret(access_token)
    print(f"Saved {SECRET_NAME} to GitHub Secrets.")
    print(f"Token expires in {token_payload.get('expires_in', 'unknown')} seconds.")


if __name__ == "__main__":
    main()
