Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing
Add-Type -AssemblyName System.Web.Extensions  # Para serializar JSON

# Caminho do arquivo JSON
$savePath = "$env:APPDATA\fieplogin_userdata.json"

# Função para carregar dados salvos
function Load-UserData {
    if (Test-Path $savePath) {
        $json = Get-Content $savePath -Raw | ConvertFrom-Json
        return $json
    }
    return @{ username = ""; password = "" }
}

# Função para salvar dados
function Save-UserData($username, $password) {
    $data = @{ username = $username; password = $password }
    $json = $data | ConvertTo-Json -Compress
    $json | Set-Content -Path $savePath
}

# Carregar dados prévios
$userData = Load-UserData

# Criação da janela principal
$form = New-Object System.Windows.Forms.Form
$form.Text = "Fieplogin"
$form.Size = New-Object System.Drawing.Size(300,200)
$form.StartPosition = "CenterScreen"

# Label e TextBox para o usuário
$labelUser = New-Object System.Windows.Forms.Label
$labelUser.Text = "Usuario:"
$labelUser.Location = New-Object System.Drawing.Point(10,20)
$labelUser.Size = New-Object System.Drawing.Size(60,20)
$form.Controls.Add($labelUser)

$textUser = New-Object System.Windows.Forms.TextBox
$textUser.Location = New-Object System.Drawing.Point(80,18)
$textUser.Size = New-Object System.Drawing.Size(180,20)
$textUser.Text = $userData.username
$form.Controls.Add($textUser)

# Label e TextBox para a senha
$labelPass = New-Object System.Windows.Forms.Label
$labelPass.Text = "Senha:"
$labelPass.Location = New-Object System.Drawing.Point(10,60)
$labelPass.Size = New-Object System.Drawing.Size(60,20)
$form.Controls.Add($labelPass)

$textPass = New-Object System.Windows.Forms.TextBox
$textPass.Location = New-Object System.Drawing.Point(80,58)
$textPass.Size = New-Object System.Drawing.Size(180,20)
$textPass.UseSystemPasswordChar = $true
$textPass.Text = $userData.password
$form.Controls.Add($textPass)

# Botão de login
$buttonLogin = New-Object System.Windows.Forms.Button
$buttonLogin.Text = "Login"
$buttonLogin.Location = New-Object System.Drawing.Point(100,100)
$buttonLogin.Size = New-Object System.Drawing.Size(75,30)

$buttonLogin.Add_Click({
    $username = $textUser.Text
    $password = $textPass.Text

    # Salvar dados
    Save-UserData -username $username -password $password

    # Caminho do Python e script
    $pythonPath = "python"
    $scriptPath = "$env:USERPROFILE\Documents\fieplogin\main.py"
    $outputFile = "$env:TEMP\fieplogin_output.txt"

    # Executar script Python
    Start-Process -FilePath $pythonPath -ArgumentList "`"$scriptPath`" `"$username`" `"$password`"" -NoNewWindow -RedirectStandardOutput $outputFile -Wait

    # Mostrar resposta
    $output = Get-Content $outputFile
    [System.Windows.Forms.MessageBox]::Show($output -join "`n", "Resultado do Login")
})
$form.Controls.Add($buttonLogin)

# Exibir janela
$form.ShowDialog()
