# Quantitative Order Book & Paper Trading Engine

A high-frequency market data listener and automated quantitative trading strategy backtester built in Python using WebSockets.

## Features
- **Real-time Order Book Stream:** Connects to Binance WebSockets for live L2 Order Book updates (BTC/USDT).
- **Quantitative Indicators:** Calculates live Bid-Ask Spread, Rolling Volatility, and Order Book Imbalance.
- **Automated Paper Trading:** Simulates order execution based on order book buy/sell pressure signals.

## Project Structure
- `orderbook_listener.py`: Lightweight WebSocket connector for testing feed stability.
- `orderbook_engine.py`: Analytics engine calculating live imbalance and volatility metrics.
- `paper_trading_engine.py`: Full execution engine running paper trading strategies.

## Setup & Run
1. Install dependencies:
   ```bash
   pip install -r requirements.txt