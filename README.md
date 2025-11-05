# 📈 Sistema de Trading Automatizado

Sistema completo de trading automatizado com interface web moderna e API robusta para análise de dados de mercado e execução de estratégias de trading automatizadas.

## 🎯 Características Principais

- **Interface Web Moderna**: Dashboard responsivo com gráficos interativos
- **API RESTful**: Backend em Python com FastAPI
- **Trading Automatizado**: Sistema de execução de estratégias com paper trading e trading real
- **Indicadores Técnicos**: Suporte para SMA, EMA, RSI, MACD, Bollinger Bands
- **Múltiplos Símbolos**: Suporte para mais de 20 pares de moedas
- **Histórico de Trades**: Registo detalhado de todas as operações
- **Monitorização em Tempo Real**: Actualizações automáticas de dados

## 🏗️ Arquitectura do Sistema

```
freqtrade2/
├── backend/              # API FastAPI em Python
│   ├── main.py           # Servidor principal
│   ├── trading_logic.py  # Lógica de trading
│   ├── requirements.txt  # Dependências Python
│   └── logs/             # Ficheiros de log
├── frontend/             # Interface web com Chart.js
│   ├── index.html        # Interface principal
│   ├── test.html         # Página de teste
│   ├── lang.js           # Sistema de idiomas
│   └── package.json      # Configurações npm
├── docker/               # Configurações Docker
│   ├── docker-compose.yml
│   ├── Dockerfile
│   ├── Dockerfile.backend
│   └── Dockerfile.frontend
├── docs/                 # Documentação
├── scripts/              # Scripts de configuração
└── README.md             # Este ficheiro
```

## 🚀 Instalação e Configuração

### Pré-requisitos

- Python 3.8+
- Node.js 14+
- Navegador web moderno

### Configuração Rápida

1. **Clone o repositório**:
   ```bash
   git clone <url-do-repositorio>
   cd freqtrade2
   ```

2. **Configure o Backend**:
   ```bash
   cd backend
   pip install -r requirements.txt
   cp .env.example .env
   # Edite o ficheiro .env com as suas chaves API
   ```

3. **Execute o Backend**:
   ```bash
   python main.py
   ```

4. **Execute o Frontend** (noutro terminal):
   ```bash
   cd frontend
   python -m http.server 8080
   ```

5. **Acesso ao Sistema**:
   - Interface Principal: http://localhost:8080/index.html
   - Página de Teste: http://localhost:8080/test.html

### Configuração Docker (Alternativa)

```bash
# Construir e executar com Docker
docker-compose up -d

# O sistema ficará disponível em:
# Frontend: http://localhost:8080
# Backend API: http://localhost:8000
```

## ⚙️ Configuração

### Chaves API Binance

Edite o ficheiro `backend/.env`:

```env
BINANCE_API_KEY=sua_chave_api_aqui
BINANCE_SECRET_KEY=sua_chave_secreta_aqui
TRADING_MODE=paper  # paper ou real
```

### Indicadores Técnicos

O sistema suporta os seguintes indicadores:
- **SMA** (Simple Moving Average)
- **EMA** (Exponential Moving Average)
- **RSI** (Relative Strength Index)
- **MACD** (Moving Average Convergence Divergence)
- **BOLL** (Bollinger Bands)

## 📊 Utilização

### Interface Web

1. **Seleccionar Par de Moedas**: Escolha o par desejado na dropdown
2. **Configurar Intervalo**: Defina o timeframe (1m, 5m, 1h, etc.)
3. **Carregar Gráfico**: Clique em "Carregar Gráfico"
4. **Activar Indicadores**: Ligue/desligue indicadores conforme necessário
5. **Iniciar Trading**: Execute a estratégia automatizada

### API Endpoints

#### Símbolos
- `GET /api/symbols` - Lista todos os símbolos disponíveis

#### Dados de Mercado
- `GET /api/klines/{symbol}` - Dados de candles
- `GET /api/indicators/{symbol}` - Indicadores técnicos

#### Trading
- `POST /api/trading/start` - Iniciar trading automatizado
- `POST /api/trading/stop` - Parar trading automatizado
- `GET /api/trading/status` - Estado actual do trading

#### Análise
- `GET /api/balance` - Saldo actual
- `GET /api/trade_history` - Histórico de trades

## 🛠️ Desenvolvimento

### Estrutura de Ficheiros

- **backend/main.py**: Servidor FastAPI principal
- **backend/trading_logic.py**: Lógica de trading e indicadores
- **frontend/index.html**: Interface principal do utilizador
- **frontend/test.html**: Página de diagnóstico e teste

### Adicionar Novos Indicadores

1. Implemente o indicador em `backend/trading_logic.py`
2. Adicione a configuração em `frontend/lang.js`
3. Actualize a interface em `frontend/index.html`

### Executar Testes

```bash
# Backend
cd backend
python -m pytest

# Frontend
cd frontend
python -m http.server 8080
# Abra http://localhost:8080/test.html
```

## 🔧 Resolução de Problemas

### Erro "TradingVue is not defined"
- Este erro foi resolvido na versão actual
- O sistema agora usa Chart.js em vez de TradingVue
- Verifique a página de teste em `/test.html`

### Problemas de Conectividade
- Verifique se o backend está a correr na porta 8000
- Confirme que as bibliotecas CDN estão a carregar
- Use a página de teste para diagnóstico

### Logs do Sistema
- **Backend**: `backend/logs/trading.log`
- **Frontend**: Consola do navegador (F12)

## 📈 Estratégias de Trading

### Estratégias Implementadas

1. **Trend Following**: Segue tendências usando SMA/EMA
2. **Mean Reversion**: Estratégia de retorno à média com Bollinger Bands
3. **Momentum**: Usa RSI e MACD para identificar momentum

### Papel Trading vs Trading Real

- **Papel Trading**: Todas as operações são simuladas, sem risco real
- **Trading Real**: Operações com capital real, máximo cuidado

## 📝 Licença

Este project está licenciado sob a Licença MIT - veja o ficheiro [LICENSE](LICENSE) para detalhes.

## 🤝 Contribuições

1. Faça um fork do repositório
2. Crie uma branch para a sua feature (`git checkout -b feature/AmazingFeature`)
3. Faça commit das suas alterações (`git commit -m 'Adicionar AmazingFeature'`)
4. Faça push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📞 Suporte

Para questões e suporte:
- Abra uma issue no GitHub
- Consulte a documentação em `/docs`
- Use a página de teste para diagnóstico

## ⚠️ Aviso de Risco

**ATENÇÃO**: O trading automatizado envolve riscos significativos de perda de capital. Este sistema é fornecido apenas para fins educacionais e de pesquisa. Nunca invista mais do que pode perder. Use sempre papel trading para testar estratégias antes de usar capital real.

---

**Versão**: 2.0.0
**Última Actualização**: 2025-11-05
**Desenvolvido em**: Python 3.8+ | FastAPI | Chart.js | Bootstrap 5
