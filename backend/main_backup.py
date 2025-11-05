import asyncio
import os
from datetime import datetime
from typing import Dict, List, Optional

import numpy as np
import pandas as pd
import pandas_ta as ta
from binance.client import Client
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from trading_logic import TradingBot

load_dotenv()

app = FastAPI(title="TradingView-like Charts with Indicators and Binance Automation")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Binance client
binance_api_key = os.getenv("BINANCE_API_KEY")
binance_secret_key = os.getenv("BINANCE_SECRET_KEY")
client = Client(binance_api_key, binance_secret_key)

# Initialize trading bot
bot = TradingBot()

# Indicator configurations
INDICATORS = {
    "SMA": {"enabled": True, "period": 20},
    "EMA": {"enabled": True, "period": 12},
    "RSI": {"enabled": True, "period": 14, "overbought": 70, "oversold": 30},
    "MACD": {"enabled": True, "fast": 12, "slow": 26, "signal": 9},
    "BBANDS": {"enabled": True, "period": 20, "deviation": 2},
    "STOCH": {"enabled": True, "k_period": 14, "d_period": 3, "overbought": 80, "oversold": 20},
    "VOLUME": {"enabled": True},
    "SAR": {"enabled": True, "acceleration": 0.02, "maximum": 0.2},
    "ICHIMOKU": {"enabled": True, "tenkan": 9, "kijun": 26, "senkou": 52},
    "ADX": {"enabled": True, "period": 14, "threshold": 25}
}

@app.get("/api/indicators")
async def get_indicators():
    return INDICATORS

@app.put("/api/indicators/{indicator}")
async def update_indicator(indicator: str, config: Dict):
    if indicator not in INDICATORS:
        raise HTTPException(status_code=404, detail="Indicator not found")
    INDICATORS[indicator].update(config)
    return INDICATORS[indicator]

@app.get("/api/klines/{symbol}")
async def get_klines(symbol: str, interval: str = "1h", limit: int = 500):
    try:
        # Tentar usar API da Binance primeiro
        if binance_api_key and binance_secret_key:
            klines = client.get_klines(symbol=symbol, interval=interval, limit=limit)
            data = []
            for kline in klines:
                data.append({
                    "timestamp": kline[0],
                    "open": float(kline[1]),
                    "high": float(kline[2]),
                    "low": float(kline[3]),
                    "close": float(kline[4]),
                    "volume": float(kline[5])
                })
            return data
        else:
            # Fallback: dados simulados para demonstração
            import random
            import time
            data = []
            base_price = 50000  # Preço base para BTC
            current_time = int(time.time() * 1000)

            for i in range(limit):
                # Simular movimento de preço realista
                change = random.uniform(-0.02, 0.02)  # -2% a +2%
                open_price = base_price * (1 + change)
                high_price = open_price * (1 + random.uniform(0, 0.01))
                low_price = open_price * (1 - random.uniform(0, 0.01))
                close_price = random.uniform(low_price, high_price)
                volume = random.uniform(100, 1000)

                data.append({
                    "timestamp": current_time - (limit - i) * 3600000,  # 1 hora em ms
                    "open": round(open_price, 2),
                    "high": round(high_price, 2),
                    "low": round(low_price, 2),
                    "close": round(close_price, 2),
                    "volume": round(volume, 2)
                })

                base_price = close_price  # Próximo candle começa onde o anterior terminou

            return data
    except Exception as e:
        # Fallback para dados simulados em caso de erro
        import random
        import time
        data = []
        base_price = 50000
        current_time = int(time.time() * 1000)

        for i in range(limit):
            change = random.uniform(-0.02, 0.02)
            open_price = base_price * (1 + change)
            high_price = open_price * (1 + random.uniform(0, 0.01))
            low_price = open_price * (1 - random.uniform(0, 0.01))
            close_price = random.uniform(low_price, high_price)
            volume = random.uniform(100, 1000)

            data.append({
                "timestamp": current_time - (limit - i) * 3600000,
                "open": round(open_price, 2),
                "high": round(high_price, 2),
                "low": round(low_price, 2),
                "close": round(close_price, 2),
                "volume": round(volume, 2)
            })

            base_price = close_price

        return data

@app.get("/api/indicators/{symbol}")
async def calculate_indicators(symbol: str, interval: str = "1h", limit: int = 500):
    klines = await get_klines(symbol, interval, limit)
    df = pd.DataFrame(klines)
    df['close'] = df['close'].astype(float)
    df['high'] = df['high'].astype(float)
    df['low'] = df['low'].astype(float)
    df['volume'] = df['volume'].astype(float)

    results = {}

    if INDICATORS["SMA"]["enabled"]:
        results["SMA"] = ta.sma(df['close'], length=INDICATORS["SMA"]["period"]).tolist()

    if INDICATORS["EMA"]["enabled"]:
        results["EMA"] = ta.ema(df['close'], length=INDICATORS["EMA"]["period"]).tolist()

    if INDICATORS["RSI"]["enabled"]:
        results["RSI"] = ta.rsi(df['close'], length=INDICATORS["RSI"]["period"]).tolist()

    if INDICATORS["MACD"]["enabled"]:
        macd_df = ta.macd(df['close'], fast=INDICATORS["MACD"]["fast"], slow=INDICATORS["MACD"]["slow"], signal=INDICATORS["MACD"]["signal"])
        results["MACD"] = {"macd": macd_df['MACD_12_26_9'].tolist(), "signal": macd_df['MACDs_12_26_9'].tolist(), "hist": macd_df['MACDh_12_26_9'].tolist()}

    if INDICATORS["BBANDS"]["enabled"]:
        bb_df = ta.bbands(df['close'], length=INDICATORS["BBANDS"]["period"], std=INDICATORS["BBANDS"]["deviation"])
        results["BBANDS"] = {"upper": bb_df['BBU_20_2.0'].tolist(), "middle": bb_df['BBM_20_2.0'].tolist(), "lower": bb_df['BBL_20_2.0'].tolist()}

    if INDICATORS["STOCH"]["enabled"]:
        stoch_df = ta.stoch(df['high'], df['low'], df['close'], k=INDICATORS["STOCH"]["k_period"], d=INDICATORS["STOCH"]["d_period"])
        results["STOCH"] = {"k": stoch_df['STOCHk_14_3_3'].tolist(), "d": stoch_df['STOCHd_14_3_3'].tolist()}

    if INDICATORS["VOLUME"]["enabled"]:
        results["VOLUME"] = df['volume'].tolist()

    if INDICATORS["SAR"]["enabled"]:
        results["SAR"] = ta.psar(df['high'], df['low'], af=INDICATORS["SAR"]["acceleration"], max_af=INDICATORS["SAR"]["maximum"])['PSARl_0.02_0.02_0.2'].tolist()

    if INDICATORS["ICHIMOKU"]["enabled"]:
        ichimoku_df = ta.ichimoku(df['high'], df['low'], df['close'], tenkan=INDICATORS["ICHIMOKU"]["tenkan"], kijun=INDICATORS["ICHIMOKU"]["kijun"], senkou=INDICATORS["ICHIMOKU"]["senkou"])
        results["ICHIMOKU"] = {
            "tenkan": ichimoku_df['ITS_9'].tolist(),
            "kijun": ichimoku_df['IKS_26'].tolist(),
            "senkou_a": ichimoku_df['ISA_9'].tolist(),
            "senkou_b": ichimoku_df['ISB_26'].tolist()
        }

    if INDICATORS["ADX"]["enabled"]:
        results["ADX"] = ta.adx(df['high'], df['low'], df['close'], length=INDICATORS["ADX"]["period"])['ADX_14'].tolist()

    return results

@app.post("/api/trade")
async def execute_trade(symbol: str, side: str, quantity: float, price: Optional[float] = None):
    try:
        if side.upper() == "BUY":
            order = client.order_market_buy(symbol=symbol, quantity=quantity)
        elif side.upper() == "SELL":
            order = client.order_market_sell(symbol=symbol, quantity=quantity)
        else:
            raise HTTPException(status_code=400, detail="Invalid side")
        return order
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/balance")
async def get_balance():
    try:
        account = client.get_account()
        balances = {balance['asset']: float(balance['free']) for balance in account['balances'] if float(balance['free']) > 0}
        return balances
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/trading/start")
async def start_trading():
    try:
        if not bot.active:
            bot.start_trading_loop()
            return {"message": "Trading iniciado com sucesso", "status": "running"}
        else:
            return {"message": "Trading já está ativo", "status": "already_running"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/trading/stop")
async def stop_trading():
    try:
        if bot.active:
            bot.stop_trading_loop()
            return {"message": "Trading parado com sucesso", "status": "stopped"}
        else:
            return {"message": "Trading já está parado", "status": "already_stopped"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/trading/status")
async def get_trading_status():
    return {
        "active": bot.active,
        "symbol": bot.symbol,
        "paper_trading": bot.paper_trading,
        "max_trade_amount": bot.max_trade_amount_usdt
    }

@app.get("/api/trade_history")
async def get_trade_history():
    try:
        history = bot.get_trade_history()
        return {"trades": history[-50:]}  # Últimos 50 trades
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/set_strategy")
async def set_strategy(rules: Dict):
    try:
        bot.set_strategy_rules(rules)
        return {"message": "Estratégia atualizada com sucesso"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
