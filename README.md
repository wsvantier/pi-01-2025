# Projeto Integrador

Este repositório contém os arquivos do **Projeto Integrador**, que tem como objetivo o desenvolvimento de uma aplicação utilizando um framework web, banco de dados e controle de versão.

## Tecnologias Utilizadas

- **Framework Web:** Flask  
- **Banco de Dados:** MySQL e MariaDB (ambos testados e funcionando corretamente)  
- **Controle de Versão:** Git (com repositório hospedado no GitHub)

## Ambiente de Testes

O projeto foi testado nos sistemas operacionais **Windows** e **Linux**.

---

## Requisitos para Executar o Projeto

### No **Windows**

1. Instale o [Python](https://www.python.org/)
2. Instale as bibliotecas necessárias:
   ```bash
   pip install flask pymysql cryptography
   ```
3. Instale um servidor de banco de dados: [MySQL](https://dev.mysql.com/downloads/mysql/) ou [MariaDB](https://mariadb.org/)
4. Restaure o banco de dados utilizando o arquivo `Dump.sql` disponível neste repositório.

---

### No **Linux**

1. Verifique se o Python já está instalado (a maioria das distribuições já possui):
   ```bash
   python3 --version
   ```
2. Instale o `pip` e as bibliotecas:
   ```bash
   sudo apt update
   sudo apt install python3-pip
   pip3 install flask pymysql cryptography
   ```
3. Instale o MySQL ou MariaDB:
   ```bash
   sudo apt install mariadb-server
   # ou
   sudo apt install mysql-server
   ```
4. Restaure o banco de dados utilizando o arquivo `Dump.sql`:
   ```bash
   mysql -u root -p < Dump.sql
   ```

---
