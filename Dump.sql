-- Criar o banco de dados
CREATE DATABASE IF NOT EXISTS `pi` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `pi`;

-- Criar usuário e conceder privilégios
CREATE USER IF NOT EXISTS 'Teste'@'localhost' IDENTIFIED BY '12345';
GRANT ALL PRIVILEGES ON `pi`.* TO 'Teste'@'localhost';
FLUSH PRIVILEGES;

-- Criar tabelas principais
DROP TABLE IF EXISTS `Clientes`;
CREATE TABLE `Clientes` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Nome` varchar(255) NOT NULL,
  `Telefone` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`ID`)
);

DROP TABLE IF EXISTS `Fornecedor`;
CREATE TABLE `Fornecedor` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Nome` varchar(255) NOT NULL,
  `Email` varchar(255) DEFAULT NULL,
  `Telefone` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`ID`)
);

DROP TABLE IF EXISTS `Estoque`;
CREATE TABLE `Estoque` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Descricao` varchar(255) NOT NULL,
  `Categoria` enum('Alimentos','Bebidas','Laticínios','Produtos de Higiene','Padaria','Congelados','Produtos para Pet','Bazar e Utilidades') NOT NULL,
  `Validade` date DEFAULT NULL,
  `Quantidade` int(11) NOT NULL,
  PRIMARY KEY (`ID`)
);

-- Criar tabelas dependentes
DROP TABLE IF EXISTS `Vendas`;
CREATE TABLE `Vendas` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `ID_Cliente` int(11) DEFAULT NULL,
  `Preco` decimal(10,2) DEFAULT NULL,
  `Fiado` enum('SIM','NÃO') NOT NULL DEFAULT 'NÃO',
  PRIMARY KEY (`ID`),
  CONSTRAINT `fk_vendas_cliente` FOREIGN KEY (`ID_Cliente`) REFERENCES `Clientes`(`ID`) ON DELETE SET NULL
);

DROP TABLE IF EXISTS `Contas_a_Pagar`;
CREATE TABLE `Contas_a_Pagar` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Fornecedor` int(11) NOT NULL,
  `Data_de_Vencimento` date NOT NULL,
  `Valor` decimal(10,2) NOT NULL,
  `Situacao` enum('PAGA','PENDENTE') NOT NULL DEFAULT 'PENDENTE',
  PRIMARY KEY (`ID`),
  CONSTRAINT `fk_contas_pagar_fornecedor` FOREIGN KEY (`Fornecedor`) REFERENCES `Fornecedor`(`ID`) ON DELETE CASCADE
);

DROP TABLE IF EXISTS `Contas_a_Receber`;
CREATE TABLE `Contas_a_Receber` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `ID_Cliente` int(11) NOT NULL,
  `Valor` decimal(10,2) NOT NULL,
  `Data_da_Venda` date NOT NULL,
  `Situacao` enum('PAGO','PENDENTE') NOT NULL DEFAULT 'PENDENTE',
  PRIMARY KEY (`ID`),
  CONSTRAINT `fk_contas_receber_cliente` FOREIGN KEY (`ID_Cliente`) REFERENCES `Clientes`(`ID`) ON DELETE CASCADE
);

DROP TABLE IF EXISTS `Item_Venda`;
CREATE TABLE `Item_Venda` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `ID_Venda` int(11) NOT NULL,
  `ID_Produto` int(11) NOT NULL,
  `Quantidade` int(11) DEFAULT NULL,
  `Valor_Unidade` decimal(10,2) DEFAULT NULL,
  `Total` decimal(10,2) DEFAULT NULL,
  PRIMARY KEY (`ID`),
  CONSTRAINT `fk_item_venda_venda` FOREIGN KEY (`ID_Venda`) REFERENCES `Vendas`(`ID`) ON DELETE CASCADE,
  CONSTRAINT `fk_item_venda_produto` FOREIGN KEY (`ID_Produto`) REFERENCES `Estoque`(`ID`) ON DELETE CASCADE
);

