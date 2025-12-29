# Automatic Space Weather Data Retrieval, Processing and Visualization System
As it turns out it's going to be my **bachelor's thesis** ;)

## Description
This repo contains code and thesis text for my bachelor's thesis(as the name indicates ;D). It's a system for a fully automatic retrieval, processing and vizualization of selected
parameters of space weather. As mentioned the flow is fully automated using GH Actions and code written in both Python and Go, which also happened to be contenerized for convenience ;D

## Possible future steps
- extending vizualization
- migrating vizualization module to another(faster) framework
- adding simple ML module 
- increasing data retrieval frequency

## Websites 

- [Dashboard](https://inzynierka-sskrzypczyk.streamlit.app/)
- [Thesis Online](https://szymonskrzypczyk.github.io/inzynierka/)

## Setup guide
1. Fork the repo
2. Enable GH Actions in your fork - https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/enabling-features-for-your-repository/managing-github-actions-settings-for-a-repository#managing-github-actions-permissions-for-your-repository
3. Setup Dropbox app to get access token - https://www.dropbox.com/developers/apps
4. Using Dropbox app's `App key` and `App secret` generate access token - https://dropbox.github.io/dropbox-api-v2-explorer/#oauth2-token-from-oauth2-authorize, `get_refresh_token.py` [script](https://github.com/SzymonSkrzypczyk/inzynierka/blob/master/get_refresh_token.py) can help you with that
5. Setup database, I used [Neon, because of its free tier](https://neon.com/) 
6. Obtain gmail app password - https://support.google.com/accounts/answer/185833?hl=en - this is required to send email notifications, it will be needed to set up email notification
7. Set all necessary secrets in your repo settings - https://docs.github.com/en/actions/security-guides/encrypted-secrets
**Required secrets**:
   - `APP_NAME` - your application name
   - `DB_HOST` - your database host 
   - `DB_NAME` - your database name
   - `DB_USER` - your database user
   - `DB_PASSWORD` - your database password
   - `DROPBOX_APP_KEY` - your Dropbox app key
   - `DROPBOX_APP_SECRET` - your Dropbox app secret
   - `DROPBOX_REFRESH_TOKEN` - your Dropbox refresh token
   - `EMAIL_TO` - email to send notifications to
   - `MAIL_CONNECTION` - your email connection string, format is `smtps://your@gmail.com:APP_PASSWORD@smtp.gmail.com:465`
8. Go to [Streamlit Cloud](https://streamlit.io/cloud) and login with GitHub by clicking on deploy for free
9. Click on **Create App** and select forked repo, select `master` branch and provide needed env variables in `Secrets` section:
    - `DB_USER` - your application name
    - `DB_PASSWORD` - your database host 
    - `DB_HOST` - your database name
    - `DB_NAME` - your database user
    - `DB_PORT` - your database password
   
> The values for env variables for steps 7 and 9 should be the same!
