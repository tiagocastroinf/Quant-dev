import asyncio
import json
import websockets
import numpy as np
from collections import deque
from datetime import datetime

BINANCE_WS_URL = "wss://stream.binance.com:9443/ws/btcusdt@depth5@100ms"

# Guardar os últimos 50 preços para calcular a volatilidade em tempo real
price_history = deque(maxlen=50)

async def process_orderbook():
    print("Starting Quantitative Order Book Engine...")
    
    async with websockets.connect(BINANCE_WS_URL) as websocket:
        print("Connected to Binance. Processing live quantitative signals...\n")
        
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
                    
                    # 1. Cálculos Base
                    spread = best_ask_price - best_bid_price
                    mid_price = (best_ask_price + best_bid_price) / 2.0
                    price_history.append(mid_price)
                    
                    # 2. Order Book Imbalance (-1.0 a +1.0)
                    total_qty = best_bid_qty + best_ask_qty
                    imbalance = (best_bid_qty - best_ask_qty) / total_qty if total_qty > 0 else 0.0
                    
                    # 3. Volatilidade (Desvio Padrão dos últimos preços)
                    volatility = np.std(price_history) if len(price_history) > 1 else 0.0
                    
                    # Determinar o sinal de pressão do mercado
                    if imbalance > 0.35:
                        signal = "BUY PRESSURE 🟢"
                    elif imbalance < -0.35:
                        signal = "SELL PRESSURE 🔴"
                    else:
                        signal = "NEUTRAL ⚪"
                    
                    timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
                    
                    # Output limpo com métricas quantitativas
                    print(f"[{timestamp}] Mid: ${mid_price:.2f} | Spread: ${spread:.2f} | Volatility: {volatility:.4f}")
                    print(f"   Pressure Signal: {signal} (Imbalance: {imbalance:+.2f})")
                    print(f"   Bids: {best_bid_qty:.4f} BTC @ ${best_bid_price:.2f} | Asks: {best_ask_qty:.4f} BTC @ ${best_ask_price:.2f}")
                    print("-" * 70)
                    
            except websockets.ConnectionClosed:
                print("Connection closed. Reconnecting...")
                break
            except Exception as e:
                print(f"Error: {e}")
                break

if __name__ == "__main__":
    asyncio.run(process_orderbook())