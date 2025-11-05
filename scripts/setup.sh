#!/bin/bash

echo "Configurando o ambiente de trading..."

# Verificar se Docker está instalado
if ! command -v docker &> /dev/null; then
    echo "Docker não está instalado. Por favor, instale o Docker primeiro."
    exit 1
fi

# Verificar se Docker Compose está instalado
if ! command -v docker-compose &> /dev/null; then
    echo "Docker Compose não está instalado. Por favor, instale o Docker Compose primeiro."
    exit 1
fi

# Copiar arquivo .env de exemplo se não existir
if [ ! -f "docker/.env" ]; then
    cp docker/.env.example docker/.env
    echo "Arquivo .env criado. Por favor, edite docker/.env com suas chaves da Binance."
fi

# Construir e iniciar os containers
echo "Construindo e iniciando containers..."
docker-compose -f docker/docker-compose.yml up --build -d

# Aguardar os serviços ficarem prontos
echo "Aguardando serviços ficarem prontos..."
sleep 10

# Verificar se os serviços estão rodando
if docker-compose -f docker/docker-compose.yml ps | grep -q "Up"; then
    echo "Setup concluído com sucesso!"
    echo "Frontend: http://localhost:3000"
    echo "Backend API: http://localhost:8000"
    echo "Documentação da API: http://localhost:8000/docs"
else
    echo "Erro: Alguns serviços não iniciaram corretamente."
    docker-compose -f docker/docker-compose.yml logs
fi
