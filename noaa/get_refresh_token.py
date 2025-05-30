from dropbox import DropboxOAuth2FlowNoRedirect


def get_refresh_token(app_key, app_secret):
    auth_flow = DropboxOAuth2FlowNoRedirect(
        consumer_key=app_key,
        consumer_secret=app_secret,
        token_access_type='offline'
    )

    authorize_url = auth_flow.start()
    print("1. Go to: " + authorize_url)
    print("2. Click 'Allow' (you might have to log in first).")
    print("3. Copy the authorization code.")

    auth_code = input("Enter the authorization code here: ").strip()
    oauth_result = auth_flow.finish(auth_code)

    print("Access token:", oauth_result.access_token)
    print("Refresh token:", oauth_result.refresh_token)
    print("Expires in:", oauth_result.expires_at)

    return oauth_result.refresh_token
