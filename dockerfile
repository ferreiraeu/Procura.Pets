# Usar uma imagem base
FROM node:14

# Definir diretório de trabalho
WORKDIR /Área de Trabalho/documentacao

# Copiar arquivos
COPY package*.json ./
RUN npm install
COPY . .

# Comando para iniciar a aplicação
CMD ["npm", "start"]
