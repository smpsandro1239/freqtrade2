import asyncio
import logging
import os
import threading
import time
from datetime import datetime
from typing import Dict, List, Optional

import pandas as pd
import pandas_ta as ta
from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceOrderException
from dotenv import load_dotenv

load_dotenv()

# Ensure logs directory exists
os.makedirs('logs', exist_ok=True)

# Configurar logging
try:
    logging.basicConfig(
        filename='logs/trading.log',
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('logs/trading.log'),
            logging.StreamHandler()
        ]
    )
except:
    # Fallback para console se não conseguir criar arquivo
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

class TradingBot:
    def __init__(self):
        self.client = Client(os.getenv("BINANCE_API_KEY"), os.getenv("BINANCE_SECRET_KEY"))
        self.symbol = os.getenv("TRADING_SYMBOL", "BTCUSDT")
        self.active = False
        self.paper_trading = os.getenv("PAPER_TRADING", "false").lower() == "true"
        self.max_trade_amount_usdt = float(os.getenv("MAX_TRADE_AMOUNT_USDT", "100"))
        self.stop_loss_percent = float(os.getenv("STOP_LOSS_PERCENT", "5"))
        self.take_profit_percent = float(os.getenv("TAKE_PROFIT_PERCENT", "10"))
        self.use_leverage = os.getenv("USE_LEVERAGE", "false").lower() == "true"
        self.leverage_value = int(os.getenv("LEVERAGE_VALUE", "1"))

        self.rules = {
            "RSI": {"buy_threshold": 30, "sell_threshold": 70},
            "EMA_CROSS": {"fast_period": 12, "slow_period": 26},
            "MACD_CROSS": {},
            "BBANDS": {"period": 20, "deviation": 2}
        }

        self.trade_history = []
        self.current_position = None
        self.trading_thread = None

        # Criar diretório de logs se não existir
        os.makedirs('logs', exist_ok=True)

    async def get_klines(self, symbol: str, interval: str = "1h", limit: int = 100):
        loop = asyncio.get_event_loop()
        klines = await loop.run_in_executor(
            None, lambda: self.client.get_klines(symbol, interval, limit)
        )
        data: List[Dict] = []
        for raw in klines:
            kline = raw or {}          # guard against None
            data.append({
                "timestamp": kline[0],
                "open": float(kline[1]),
                "high": float(kline[2]),
                "low": float(kline[3]),
                "close": float(kline[4]),
                "volume": float(kline[5]),
            })
        return data
    def calculate_indicators(self, df: pd.DataFrame):
        indicators = {}

        # RSI
        indicators["RSI"] = ta.rsi(df['close'], length=14)

        # EMA
        indicators["EMA_fast"] = ta.ema(df['close'], length=12)
        indicators["EMA_slow"] = ta.ema(df['close'], length=26)

        # MACD
        macd_df = ta.macd(df['close'], fast=12, slow=26, signal=9)
        indicators["MACD"] = macd_df['MACD_12_26_9']
        indicators["MACD_signal"] = macd_df['MACDs_12_26_9']
        indicators["MACD_hist"] = macd_df['MACDh_12_26_9']

        # Bollinger Bands
        bb_df = ta.bbands(df['close'], length=20, std=2)
        indicators["BB_upper"] = bb_df['BBU_20_2.0']
        indicators["BB_middle"] = bb_df['BBM_20_2.0']
        indicators["BB_lower"] = bb_df['BBL_20_2.0']

        return indicators

    def evaluate_signals_and_trade(self, symbol: str, indicators: Dict) -> str:
        """
        Avalia sinais dos indicadores e retorna decisão de trading
        """
        signals = {"buy": 0, "sell": 0, "hold": 0}

        # RSI signals
        if indicators.get("RSI") is not None and not indicators["RSI"].empty:
            rsi_value = indicators["RSI"].iloc[-1]
            if rsi_value < self.rules["RSI"]["buy_threshold"]:
                signals["buy"] += 1
            elif rsi_value > self.rules["RSI"]["sell_threshold"]:
                signals["sell"] += 1

        # EMA crossover
        if (indicators.get("EMA_fast") is not None and indicators.get("EMA_slow") is not None and
            not indicators["EMA_fast"].empty and not indicators["EMA_slow"].empty):
            ema_fast_prev = indicators["EMA_fast"].iloc[-2]
            ema_fast_curr = indicators["EMA_fast"].iloc[-1]
            ema_slow_prev = indicators["EMA_slow"].iloc[-2]
            ema_slow_curr = indicators["EMA_slow"].iloc[-1]

            if ema_fast_prev < ema_slow_prev and ema_fast_curr > ema_slow_curr:
                signals["buy"] += 1
            elif ema_fast_prev > ema_slow_prev and ema_fast_curr < ema_slow_curr:
                signals["sell"] += 1

        # MACD crossover
        if (indicators.get("MACD") is not None and indicators.get("MACD_signal") is not None and
            not indicators["MACD"].empty and not indicators["MACD_signal"].empty):
            macd_prev = indicators["MACD"].iloc[-2]
            macd_curr = indicators["MACD"].iloc[-1]
            signal_prev = indicators["MACD_signal"].iloc[-2]
            signal_curr = indicators["MACD_signal"].iloc[-1]

            if macd_prev < signal_prev and macd_curr > signal_curr:
                signals["buy"] += 1
            elif macd_prev > signal_prev and macd_curr < signal_curr:
                signals["sell"] += 1

        # Bollinger Bands
        if (indicators.get("BB_lower") is not None and indicators.get("BB_upper") is not None and
            not indicators["BB_lower"].empty and not indicators["BB_upper"].empty):
            # Este seria passado do df principal, mas por simplicidade vamos assumir que temos o preço
            pass  # Implementar quando necessário

        # Decisão final baseada na maioria dos sinais
        max_signal = max(signals, key=signals.get)
        if signals[max_signal] > 0:
            return max_signal.upper()
        return "HOLD"

    def execute_trade(self, signal: str, symbol: str, amount: float) -> Optional[Dict]:
        """
        Executa uma ordem de trading com validações de risco
        """
        try:
            # Validar saldo disponível
            if not self._validate_balance(signal, amount):
                logging.warning(f"Saldo insuficiente para {signal} {amount} {symbol}")
                return None

            # Aplicar gestão de risco
            amount = self._apply_risk_management(signal, symbol, amount)

            if self.paper_trading:
                # Modo simulação
                order = self._simulate_order(signal, symbol, amount)
                logging.info(f"PAPER TRADE: {signal} {amount} {symbol} at simulated price")
            else:
                # Ordem real na Binance
                if signal.upper() == "BUY":
                    order = self.client.order_market_buy(symbol=symbol, quantity=amount)
                elif signal.upper() == "SELL":
                    order = self.client.order_market_sell(symbol=symbol, quantity=amount)
                else:
                    raise ValueError(f"Sinal inválido: {signal}")

                logging.info(f"TRADE REAL: {signal} {amount} {symbol} - Order ID: {order['orderId']}")

            # Registrar trade no histórico
            self._log_trade(signal, symbol, order)

            return order

        except BinanceAPIException as e:
            logging.error(f"Erro da Binance API: {e}")
            return None
        except BinanceOrderException as e:
            logging.error(f"Erro na ordem: {e}")
            return None
        except Exception as e:
            logging.error(f"Erro geral na execução da ordem: {e}")
            return None

    def _validate_balance(self, signal: str, amount: float) -> bool:
        """Valida se há saldo suficiente para a operação"""
        try:
            account = self.client.get_account()
            if signal.upper() == "BUY":
                # Verificar saldo USDT para compras
                usdt_balance = float(next((b['free'] for b in account['balances'] if b['asset'] == 'USDT'), 0))
                return usdt_balance >= amount * 1.001  # Margem para taxas
            elif signal.upper() == "SELL":
                # Verificar saldo da cripto para vendas
                crypto_asset = self.symbol.replace('USDT', '')
                crypto_balance = float(next((b['free'] for b in account['balances'] if b['asset'] == crypto_asset), 0))
                return crypto_balance >= amount
            return False
        except Exception as e:
            logging.error(f"Erro ao validar saldo: {e}")
            return False

    def _apply_risk_management(self, signal: str, symbol: str, amount: float) -> float:
        """Aplica regras de gestão de risco"""
        # Limitar valor máximo por trade
        if amount > self.max_trade_amount_usdt:
            amount = self.max_trade_amount_usdt
            logging.info(f"Valor ajustado para limite máximo: {amount}")

        return amount

    def _simulate_order(self, signal: str, symbol: str, amount: float) -> Dict:
        """Simula uma ordem para paper trading"""
        # Obter preço atual
        ticker = self.client.get_symbol_ticker(symbol=symbol)
        price = float(ticker['price'])

        return {
            'symbol': symbol,
            'side': signal.upper(),
            'type': 'MARKET',
            'quantity': amount,
            'price': price,
            'status': 'FILLED',
            'orderId': f"paper_{int(time.time())}",
            'transactTime': int(time.time() * 1000),
            'paper_trading': True
        }

    def _log_trade(self, signal: str, symbol: str, order: Dict):
        """Registra trade no histórico"""
        trade_record = {
            'timestamp': datetime.now().isoformat(),
            'signal': signal,
            'symbol': symbol,
            'order': order,
            'paper_trading': self.paper_trading
        }
        self.trade_history.append(trade_record)

        # Manter apenas os últimos 1000 trades
        if len(self.trade_history) > 1000:
            self.trade_history = self.trade_history[-1000:]

    def trading_loop(self):
        """
        Loop principal de trading executado em thread separada
        """
        while self.active:
            try:
                # Obter dados atuais
                klines = asyncio.run(self.get_klines(self.symbol))
                df = pd.DataFrame(klines)
                df['close'] = df['close'].astype(float)
                df['high'] = df['high'].astype(float)
                df['low'] = df['low'].astype(float)

                # Calcular indicadores
                indicators = self.calculate_indicators(df)

                # Avaliar sinais e decidir trade
                signal = self.evaluate_signals_and_trade(self.symbol, indicators)

                # Executar trade se houver sinal
                if signal in ["BUY", "SELL"]:
                    # Calcular quantidade baseada no valor máximo configurado
                    amount = self._calculate_trade_amount(signal, self.symbol)
                    if amount > 0:
                        self.execute_trade(signal, self.symbol, amount)
                        logging.info(f"Sinal {signal} executado para {self.symbol}")

                # Aguardar antes da próxima verificação
                time.sleep(60)  # Verificar a cada minuto

            except Exception as e:
                logging.error(f"Erro no loop de trading: {e}")
                time.sleep(60)

    def _calculate_trade_amount(self, signal: str, symbol: str) -> float:
        """
        Calcula a quantidade a ser negociada baseada no valor máximo em USDT
        """
        try:
            if signal.upper() == "BUY":
                # Para compras, usar valor máximo em USDT
                ticker = self.client.get_symbol_ticker(symbol=symbol)
                price = float(ticker['price'])
                amount = self.max_trade_amount_usdt / price
                return amount
            elif signal.upper() == "SELL":
                # Para vendas, usar todo o saldo disponível (com limite)
                crypto_asset = symbol.replace('USDT', '')
                account = self.client.get_account()
                crypto_balance = float(next((b['free'] for b in account['balances'] if b['asset'] == crypto_asset), 0))
                return min(crypto_balance, self.max_trade_amount_usdt)  # Limitar valor
            return 0
        except Exception as e:
            logging.error(f"Erro ao calcular quantidade: {e}")
            return 0

    def start_trading_loop(self):
        """Inicia o loop de trading em uma thread separada"""
        if not self.active:
            self.active = True
            self.trading_thread = threading.Thread(target=self.trading_loop, daemon=True)
            self.trading_thread.start()
            logging.info("Loop de trading iniciado")

    def stop_trading_loop(self):
        """Para o loop de trading"""
        if self.active:
            self.active = False
            if self.trading_thread and self.trading_thread.is_alive():
                self.trading_thread.join(timeout=5)
            logging.info("Loop de trading parado")

    def get_trade_history(self) -> List[Dict]:
        """Retorna histórico de trades"""
        return self.trade_history.copy()

    def set_strategy_rules(self, rules: Dict):
        """Permite alterar regras de estratégia dinamicamente"""
        self.rules.update(rules)
        logging.info(f"Regras de estratégia atualizadas: {rules}")

bot = TradingBot()
if __name__ == "__main__":
    bot.start_trading_loop()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        bot.stop_trading_loop()
        logging.info("Programa encerrado.")

def safe_to_list(series: pd.Series) -> List[float]:
    """Converte uma Series do pandas para lista, tratando None"""
    if series is None:
        return []
    return series.fillna(0).tolist()

    if INDICATORS["MACD"]["enabled"]:
        macd_df = ta.macd(df['close'], fast=INDICATORS["MACD"]["fast"], slow=INDICATORS["MACD"]["slow"], signal=INDICATORS["MACD"]["signal"])
        if macd_df is not None:
            # Verificar nomes das colunas retornados pelo pandas-ta
            macd_col = [col for col in macd_df.columns if 'MACD' in col and 'hist' not in col and 'signal' not in col]
            signal_col = [col for col in macd_df.columns if 'signal' in col.lower()]
            hist_col = [col for col in macd_df.columns if 'hist' in col.lower()]

            results["MACD"] = {
                "macd": safe_to_list(macd_df[macd_col[0]]) if macd_col else [],
                "signal": safe_to_list(macd_df[signal_col[0]]) if signal_col else [],
                "hist": safe_to_list(macd_df[hist_col[0]]) if hist_col else []
            }
        else:
            results["MACD"] = {"macd": [], "signal": [], "hist": []}
