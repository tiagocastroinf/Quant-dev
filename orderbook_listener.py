import asyncio
import json
import websockets
from datetime import datetime

# URL do WebSocket público da Binance para o livro de ordens (Top 5 ordens em tempo real)
BINANCE_WS_URL = "wss://stream.binance.com:9443/ws/btcusdt@depth5@100ms"

async def connect_binance_orderbook():
    print("Connecting to Binance WebSocket...")
    
    async with websockets.connect(BINANCE_WS_URL) as websocket:
        print("Connected successfully! Listening for Order Book updates...\n")
        
        while True:
            try:
                # Receber a mensagem do WebSocket
                response = await websocket.recv()
                data = json.loads(response)
                
                # Extrair os melhores preços de compra (bids) e venda (asks)
                bids = data.get('bids', [])  # [['Preço', 'Quantidade'], ...]
                asks = data.get('asks', [])  # [['Preço', 'Quantidade'], ...]
                
                if bids and asks:
                    best_bid_price = float(bids[0][0])
                    best_bid_qty = float(bids[0][1])
                    
                    best_ask_price = float(asks[0][0])
                    best_ask_qty = float(asks[0][1])
                    
                    # Calcular o Bid-Ask Spread (Diferença entre a melhor venda e melhor compra)
                    spread = best_ask_price - best_bid_price
                    mid_price = (best_ask_price + best_bid_price) / 2.0
                    
                    # Mostrar os dados formatados
                    timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
                    print(f"[{timestamp}] Mid Price: ${mid_price:.2f} | Spread: ${spread:.2f}")
                    print(f"   ---> Top Bid (Compra): ${best_bid_price:.2f} ({best_bid_qty} BTC)")
                    print(f"   <--- Top Ask (Venda):  ${best_ask_price:.2f} ({best_ask_qty} BTC)")
                    print("-" * 60)
                    
            except websockets.ConnectionClosed:
                print("Connection closed. Reconnecting...")
                break
            except Exception as e:
                print(f"Error: {e}")
                break

if __name__ == "__main__":
    # Executar o loop assíncrono
    asyncio.run(connect_binance_orderbook())