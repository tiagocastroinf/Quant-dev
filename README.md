# Quantitative Order Book & Paper Trading Engine

A high-frequency market data listener, quantitative analytics suite, and hybrid execution/analytics engine built in Python and optimized with C++20 dynamic libraries.

## Architecture & Features
- **Real-Time Data Pipeline:** Connects to Binance WebSockets (`wss`) for live L2 Order Book updates (BTC/USDT @ 100ms interval).
- **C++20 Shared Library (`orderbook.dll`):** In-memory L2 Order Book implementation exposed via C-Types for zero-copy high-performance processing.
- **Quantitative Metrics:** Live Bid-Ask Spread and Order Book Imbalance calculations evaluated directly in C++ memory.
- **Hybrid Performance:** Achieves ~50-150 µs end-to-end processing latency for complete 20-level depth snapshots.

## Performance Benchmark
| Component | Implementation | Latency |
| :--- | :--- | :--- |
| Pure C++ Execution | C++20 (`std::map`) | **5.6 µs** |
| Hybrid Live Pipeline | Python WebSocket + C++ DLL | **50 - 150 µs** |

## Project Structure
- `live_cpp_engine.py`: Live WebSocket listener driving the C++20 shared library engine.
- `paper_trading_engine.py`: Simulated execution engine for order book signals.
- `cpp/orderbook.cpp`: C++20 Order Book source code compiled into a DLL.

## Setup & Execution

### Compile C++20 Shared Library
```bash
g++ -std=c++20 -O3 -shared cpp/orderbook.cpp -o cpp/orderbook.dll