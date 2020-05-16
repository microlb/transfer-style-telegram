TOKEN='ТОКЕН ПРОВЕРЯЮЩЕГО!' #  !! ИЗМЕНИТЬ ТОКЕН !!
REQUEST_KWARGS={
    'proxy_url': 'socks4://171.103.9.22:4145/',
    # Optional, if you need authentication:
    'urllib3_proxy_kwargs': {
      'assert_hostname': 'False',
        'cert_reqs': 'CERT_NONE'
        # 'username': 'user',
        # 'password': 'password'
    }
 }
 # прокси сейчас не используется, оставил на всякий случай