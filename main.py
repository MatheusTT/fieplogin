import requests, sys

# Usuário e senha da rede
username = sys.argv[1]
password = sys.argv[2]

# Iniciar uma sessão
session = requests.Session()

# URL inicial para capturar cookies e possivelmente tokens
initial_url = 'http://visitantes.fiepr.org.br/'

# Primeiro request para obter cookies e possivelmente tokens
response = session.get(initial_url)
print("Initial request cookies:", session.cookies.get_dict())

# Preparar os dados do payload e headers
login_url = 'https://visitantes.fiepr.org.br/login.html'
payload = {
    'buttonClicked': 4,
    'err_flag': 0,
    'err_msg': '',
    'info_flag': 0,
    'info_msg': '',
    'redirect_url': '',  # Vamos atualizar isso dinamicamente
    'network_name': 'Guest Network',
    'username': username,
    'password': password
}

# Capturar a URL de redirecionamento se existir
link = response.url
searchString = "?redirect="
equalIndex = link.find(searchString)
redirectUrl = ""
if equalIndex > 0:
    equalIndex += len(searchString)
    redirectUrl = link[equalIndex:]
    if not redirectUrl.startswith("http"):
        redirectUrl = "http://" + redirectUrl
if len(redirectUrl) > 255:
    redirectUrl = redirectUrl[:255]

# Atualizar o payload com a URL de redirecionamento
payload['redirect_url'] = redirectUrl

# Enviar o request de login com cookies capturados
# response = session.post(login_url, headers=headers, data=payload)
response = session.post(login_url, data=payload)
