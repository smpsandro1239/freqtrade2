# Gráficos TradingView-like com Indicadores e Automação Binance

Este projeto implementa um sistema completo para visualização de gráficos similares ao TradingView, com integração de indicadores técnicos e automação de trading na Binance.

## Funcionalidades

- **Gráficos Interativos**: Visualização de candlesticks em tempo real com zoom e pan
- **10 Indicadores TradingView**: SMA, EMA, RSI, MACD, Bollinger Bands, Stochastic, Volume, SAR Parabólico, Ichimoku Cloud, ADX
- **Toggle de Indicadores**: Ativar/desativar cada indicador individualmente
- **Automação de Trading**: Execução automática de ordens baseada em sinais dos indicadores
- **Interface Multilíngue**: Suporte para português-PT e inglês
- **Docker**: Instalação automatizada compatível com Linux e Windows

## Requisitos

- Docker e Docker Compose
- Chaves API da Binance (para trading real)

## Instalação Rápida

### Windows
```bash
scripts\setup.bat
```

### Linux/Mac
```bash
chmod +x scripts/setup.sh
./scripts/setup.sh
```

## Configuração

1. **Chaves da Binance**: Edite `docker/.env` com suas chaves API da Binance
2. **Acesso**: Após instalação, acesse:
   - Interface Web: http://localhost:3000
   - API Backend: http://localhost:8000
   - Documentação API: http://localhost:8000/docs

## Uso

### Interface Web
1. Selecione o par de moedas (ex: BTC/USDT)
2. Escolha o intervalo temporal
3. Ative os indicadores desejados
4. Clique em "Carregar Gráfico"
5. Use os botões de automação para iniciar/parar trading

### API REST
O backend fornece endpoints para:
- `/api/klines/{symbol}`: Dados históricos de preços
- `/api/indicators/{symbol}`: Cálculo de indicadores
- `/api/trade`: Execução de ordens
- `/api/balance`: Consulta de saldo

### Exemplo de Uso Programático
```python
# Execute o exemplo
python scripts/trading_example.py
```

## Indicadores Disponíveis

| Indicador | Descrição | Parâmetros |
|-----------|-----------|------------|
| SMA | Média Móvel Simples | Período: 20 |
| EMA | Média Móvel Exponencial | Período: 12 |
| RSI | Índice de Força Relativa | Período: 14, Overbought: 70, Oversold: 30 |
| MACD | Convergence/Divergence | Fast: 12, Slow: 26, Signal: 9 |
| Bollinger Bands | Bandas de Bollinger | Período: 20, Desvio: 2 |
| Stochastic | Oscilador Estocástico | %K: 14, %D: 3 |
| Volume | Volume de negociação | - |
| SAR | Parabólico SAR | Aceleração: 0.02, Máximo: 0.2 |
| Ichimoku | Nuvem Ichimoku | Tenkan: 9, Kijun: 26, Senkou: 52 |
| ADX | Average Directional Index | Período: 14, Threshold: 25 |

## Estratégias de Trading

O sistema inclui estratégias baseadas em:
- **RSI**: Compra quando < 30, vende quando > 70
- **EMA Crossover**: Compra no cruzamento ascendente, vende no descendente
- **MACD Crossover**: Sinais de compra/venda nos cruzamentos
- **Bollinger Bands**: Compra na banda inferior, vende na superior

## Segurança

- Chaves API armazenadas em variáveis de ambiente
- Validação de permissões de trading
- Logs de todas as operações

## Desenvolvimento

### Estrutura do Projeto
```
/
├── backend/          # API FastAPI em Python
├── frontend/         # Interface web com TradingVue.js
├── docker/           # Configurações Docker
├── docs/            # Documentação
└── scripts/         # Scripts de instalação e exemplos
```

### Adicionar Novos Indicadores
1. Implemente o cálculo em `backend/main.py`
2. Adicione configuração em `INDICATORS`
3. Atualize a interface em `frontend/index.html`

### Personalizar Estratégias
Modifique `backend/trading_logic.py` para adicionar novas regras de entrada/saída.

## Suporte

Para questões ou contribuições, consulte a documentação da API em `/docs` ou abra uma issue no repositório.

## Licença

Este projeto é distribuído sob a licença MIT.
