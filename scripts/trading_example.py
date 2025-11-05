#!/usr/bin/env python3
"""
Exemplo de uso da lógica de trading automatizada
Este script demonstra como usar os indicadores para tomar decisões de trading
"""

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio

from backend.trading_logic import TradingBot


async def example_trading_session():
    """
    Exemplo de sessão de trading usando múltiplos indicadores
    """
    bot = TradingBot()

    print("Iniciando exemplo de sessão de trading...")
    print("Regras ativas:")
    print("- RSI: Compra se < 30, Vende se > 70")
    print("- EMA Crossover: Compra na cruzamento ascendente, Vende no descendente")
    print("- MACD Crossover: Compra na cruzamento ascendente, Vende no descendente")
    print("- Bollinger Bands: Compra se preço < banda inferior, Vende se > banda superior")

    # Simular alguns candles para teste
    # Em produção, isso seria feito com dados reais da Binance
    print("\nPara testar com dados reais:")
    print("1. Configure suas chaves da Binance em docker/.env")
    print("2. Execute: docker-compose -f docker/docker-compose.yml up")
    print("3. Acesse http://localhost:3000 para interface web")
    print("4. Use a API em http://localhost:8000 para integração programática")

    # Exemplo de como iniciar o bot (comentado para evitar execução acidental)
    # bot.start()
    # await asyncio.sleep(3600)  # Rodar por 1 hora
    # bot.stop()

def custom_strategy_example():
    """
    Exemplo de como criar uma estratégia personalizada
    """
    print("\nExemplo de estratégia personalizada:")
    print("""
def minha_estrategia(df, indicators):
    signals = {"buy": False, "sell": False}

    # Exemplo: Usar combinação de RSI e Volume
    rsi = indicators["RSI"]
    volume = df["volume"]

    if rsi.iloc[-1] < 30 and volume.iloc[-1] > volume.mean():
        signals["buy"] = True
    elif rsi.iloc[-1] > 70:
        signals["sell"] = True

    return signals
    """)

if __name__ == "__main__":
    print("=== Exemplo de Trading Automatizado ===")
    asyncio.run(example_trading_session())
    custom_strategy_example()

    print("\n=== Configurações dos Indicadores ===")
    print("SMA: Período 20")
    print("EMA: Período 12/26")
    print("RSI: Período 14, Overbought 70, Oversold 30")
    print("MACD: Fast 12, Slow 26, Signal 9")
    print("Bollinger Bands: Período 20, Desvio 2")
    print("Stochastic: %K 14, %D 3")
    print("SAR: Aceleração 0.02, Máximo 0.2")
    print("Ichimoku: Tenkan 9, Kijun 26, Senkou 52")
    print("ADX: Período 14, Threshold 25")
