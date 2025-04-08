#!/bin/bash

# Variáveis
PROJETO="pi-01-2025"
GIT_REPO="https://github.com/wsvantier/pi-01-2025.git"
DIR="/var/www/$PROJETO"
PYTHON_ENV="$DIR/venv"
WSGI_FILE="$DIR/wsgi.py"
APACHE_CONF="/etc/apache2/sites-available/$PROJETO.conf"

# Atualizando pacotes e instalando dependências
sudo apt update
sudo apt install -y apache2 libapache2-mod-wsgi-py3 python3 python3-pip python3-venv mysql-server build-essential libssl-dev libffi-dev python3-dev

# Clonando o repositório
sudo git clone $GIT_REPO $DIR

# Criando ambiente virtual e ativando
python3 -m venv $PYTHON_ENV
source $PYTHON_ENV/bin/activate

# Instalando dependências Python
pip install -r $DIR/requirements.txt || pip install flask pymysql cryptography

# Restaurando banco de dados (ajuste a senha se necessário)
sudo mysql -u root -p < $DIR/Dump.sql

# Criando o arquivo wsgi.py
cat <<EOF | sudo tee $WSGI_FILE
from app import app

if __name__ == "__main__":
    app.run()
EOF

# Criando configuração do Apache
cat <<EOF | sudo tee $APACHE_CONF
<VirtualHost *:80>
    ServerName 127.0.0.1

    WSGIDaemonProcess $PROJETO python-home=$PYTHON_ENV python-path=$DIR
    WSGIScriptAlias / $WSGI_FILE

    <Directory $DIR>
        Require all granted
    </Directory>

    Alias /static $DIR/static
    <Directory $DIR/static>
        Require all granted
    </Directory>

    ErrorLog \${APACHE_LOG_DIR}/${PROJETO}_error.log
    CustomLog \${APACHE_LOG_DIR}/${PROJETO}_access.log combined
</VirtualHost>
EOF

# Ativando site e permissões
sudo a2ensite $PROJETO
sudo chown -R www-data:www-data $DIR
sudo chmod -R 755 $DIR
sudo systemctl restart apache2

echo "🚀 Deploy finalizado! Acesse em: http://127.0.0.1/"

