# Quantitative Order Book & Paper Trading Engine

A high-frequency market data listener, quantitative analytics suite, and paper trading engine built in Python and optimized in C++20.

## Features
- **Real-time Order Book Stream:** Connects to Binance WebSockets for live L2 Order Book updates (BTC/USDT).
- **Quantitative Indicators:** Calculates live Bid-Ask Spread, Rolling Volatility, and Order Book Imbalance.
- **Ultra-Low Latency Engine (C++20):** In-memory L2 Order Book implementation achieving sub-10 microsecond processing latency.
- **Automated Paper Trading:** Simulates order execution based on order book buy/sell pressure signals.

## Performance Benchmark
| Engine | Language | Latency |
| :--- | :--- | :--- |
| Data Stream & Backtester | Python 3.14 | ~200 µs |
| L2 Order Book Analytics | C++20 (-O3) | **5.6 µs** |

## Project Structure
- `orderbook_listener.py`: Lightweight WebSocket connector for testing feed stability.
- `orderbook_engine.py`: Python analytics engine calculating live imbalance and volatility.
- `paper_trading_engine.py`: Full execution engine running paper trading strategies.
- `cpp/orderbook.cpp`: C++20 high-performance Order Book implementation.

## Setup & Run

### Python Engine
```bash
pip install -r requirements.txt
python paper_trading_engine.py