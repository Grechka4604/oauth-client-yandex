from flask import Flask, redirect, request
import requests

app = Flask(__name__)

CLIENT_ID = 'c2f8e3e0ecbb4d6192ba53818cb0e63a'
CLIENT_SECRET = '878f6dc1d50a4d03b07b4ac9174abe26'
REDIRECT_URI = 'http://localhost:5000/callback'

@app.route('/')
def index():
    auth_url = (
        'https://oauth.yandex.ru/authorize?response_type=code'
        f'&client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}'
        f'&force_confirm=yes'
    )
    return f'<a href="{auth_url}">Авторизоваться через Яндекс</a>'

@app.route('/callback')
def callback():
    code = request.args.get('code')
    if not code:
        return 'Ошибка: не передан код авторизации.'

    token_url = 'https://oauth.yandex.ru/token'
    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }

    response = requests.post(token_url, data=data)
    if response.status_code != 200:
        return f'Ошибка получения токена: {response.text}'

    token_data = response.json()
    return f"""
    <h2>Access Token получен!</h2>
    <pre>{token_data}</pre>
    """

if __name__ == '__main__':
    app.run(debug=True)
