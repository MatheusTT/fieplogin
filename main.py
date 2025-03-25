import sys
import ssl
import urllib3

# Usuário e senha da rede
username = sys.argv[1]
password = sys.argv[2]

# Criar um contexto SSL compatível
ssl_context = ssl.create_default_context()
ssl_context.set_ciphers("DEFAULT:@SECLEVEL=1")

# Criar um PoolManager do urllib3 com esse contexto SSL
http = urllib3.PoolManager(ssl_context=ssl_context)

# URL inicial para capturar cookies
initial_url = 'https://visitantes.fiepr.org.br/'

# Fazer a primeira requisição para capturar cookies
response = http.request("GET", initial_url)
# print("Initial request status:", response.status)

# Capturar cookies manualmente
cookies = response.headers.get("Set-Cookie", "")

# Capturar a URL final (pode ter sido redirecionado)
redirectUrl = ""

# Se necessário, ajustar a URL para evitar erros
if not redirectUrl.startswith("https://"):
    redirectUrl = "https://" + redirectUrl
if len(redirectUrl) > 255:
    redirectUrl = redirectUrl[:255]

# Preparar os dados do payload
payload = {
  'buttonClicked': 4,
  'err_flag': 0,
  'err_msg': '',
  'info_flag': 0,
  'info_msg': '',
  'redirect_url': redirectUrl,
  'network_name': 'Guest Network',
  'username': username,
  'password': password
}

# Criar os headers
headers = {
  "Content-Type": "application/x-www-form-urlencoded",
  "Cookie": cookies,
  "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

# Fazer o login com os dados no formato correto
response = http.request(
  "POST",
  "https://visitantes.fiepr.org.br/login.html",
  headers=headers,
  fields=payload,
  encode_multipart=False
)

# Exibir resposta
print("Login status code:", response.status)
