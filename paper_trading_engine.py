import asyncio
import json
import websockets
import numpy as np
from collections import deque
from datetime import datetime

BINANCE_WS_URL = "wss://stream.binance.com:9443/ws/btcusdt@depth5@100ms"

# Histórico para métricas
price_history = deque(maxlen=50)

# Estado da Conta Virtual (Paper Trading)
class Portfolio:
    def __init__(self, initial_balance=10000.0):
        self.usdt_balance = initial_balance
        self.btc_balance = 0.0
        self.in_position = False
        self.entry_price = 0.0
        self.total_trades = 0
        self.winning_trades = 0

portfolio = Portfolio()

async def process_orderbook():
    print("Starting Quantitative Paper Trading Engine...")
    
    async with websockets.connect(BINANCE_WS_URL) as websocket:
        print("Connected to Binance. Executing automated paper trades...\n")
        
        while True:
            try:
                response = await websocket.recv()
                data = json.loads(response)
                
                bids = data.get('bids', [])
                asks = data.get('asks', [])
                
                if bids and asks:
                    best_bid_price = float(bids[0][0])
                    best_bid_qty = float(bids[0][1])
                    
                    best_ask_price = float(asks[0][0])
                    best_ask_qty = float(asks[0][1])
                    
                    mid_price = (best_ask_price + best_bid_price) / 2.0
                    price_history.append(mid_price)
                    
                    # Cálculo de Imbalance e Volatilidade
                    total_qty = best_bid_qty + best_ask_qty
                    imbalance = (best_bid_qty - best_ask_qty) / total_qty if total_qty > 0 else 0.0
                    volatility = np.std(price_history) if len(price_history) > 1 else 0.0
                    
                    timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
                    
                    # --- Lógica do Executor de Ordens (Execution Strategy) ---
                    
                    # 1. Sinal de Compra: Imbalance > 0.60 e fora de posição
                    if imbalance > 0.60 and not portfolio.in_position:
                        portfolio.btc_balance = (portfolio.usdt_balance * 0.99) / best_ask_price
                        portfolio.entry_price = best_ask_price
                        portfolio.in_position = True
                        portfolio.usdt_balance = 0.0
                        portfolio.total_trades += 1
                        
                        print(f"\n🚀 [{timestamp}] EXECUTION: BUY ORDER EXECUTED!")
                        print(f"   Bought {portfolio.btc_balance:.4f} BTC @ ${portfolio.entry_price:.2f}")
                        print(f"   Reason: Strong Buy Pressure (Imbalance: {imbalance:+.2f})\n")

                    # 2. Sinal de Venda: Imbalance < -0.40 ou Take-Profit/Stop-Loss
                    elif portfolio.in_position:
                        pnl_pct = ((best_bid_price - portfolio.entry_price) / portfolio.entry_price) * 100
                        
                        # Vender se houver pressão oposta ou se atingir profit (+0.05%) / stop (-0.05%)
                        if imbalance < -0.40 or pnl_pct >= 0.05 or pnl_pct <= -0.05:
                            portfolio.usdt_balance = portfolio.btc_balance * best_bid_price
                            if pnl_pct > 0:
                                portfolio.winning_trades += 1
                                
                            print(f"\n📉 [{timestamp}] EXECUTION: SELL ORDER EXECUTED!")
                            print(f"   Sold BTC @ ${best_bid_price:.2f} | PnL: {pnl_pct:+.3f}%")
                            print(f"   New Balance: ${portfolio.usdt_balance:.2f} USDT\n")
                            
                            portfolio.btc_balance = 0.0
                            portfolio.in_position = False

                    # Monitor no terminal
                    total_portfolio_value = portfolio.usdt_balance if not portfolio.in_position else (portfolio.btc_balance * mid_price)
                    print(f"[{timestamp}] Mid: ${mid_price:.2f} | Imbalance: {imbalance:+.2f} | Portfolio: ${total_portfolio_value:.2f}")
                    
            except websockets.ConnectionClosed:
                print("Connection closed. Reconnecting...")
                break
            except Exception as e:
                print(f"Error: {e}")
                break

if __name__ == "__main__":
    asyncio.run(process_orderbook())