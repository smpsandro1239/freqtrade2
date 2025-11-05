@echo off
echo Configurando o ambiente de trading...

REM Verificar se Docker está instalado
docker --version >nul 2>&1
if errorlevel 1 (
    echo Docker não está instalado. Por favor, instale o Docker primeiro.
    pause
    exit /b 1
)

REM Verificar se Docker Compose está instalado
docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo Docker Compose não está instalado. Por favor, instale o Docker Compose primeiro.
    pause
    exit /b 1
)

REM Copiar arquivo .env de exemplo se não existir
if not exist "docker\.env" (
    copy docker\.env.example docker\.env
    echo Arquivo .env criado. Por favor, edite docker\.env com suas chaves da Binance.
)

REM Construir e iniciar os containers
echo Construindo e iniciando containers...
docker-compose -f docker/docker-compose.yml up --build -d

REM Aguardar os serviços ficarem prontos
echo Aguardando serviços ficarem prontos...
timeout /t 10 /nobreak >nul

REM Verificar se os serviços estão rodando
docker-compose -f docker/docker-compose.yml ps | findstr "Up" >nul
if errorlevel 1 (
    echo Erro: Alguns serviços não iniciaram corretamente.
    docker-compose -f docker/docker-compose.yml logs
) else (
    echo Setup concluído com sucesso!
    echo Frontend: http://localhost:3000
    echo Backend API: http://localhost:8000
    echo Documentação da API: http://localhost:8000/docs
)

pause
