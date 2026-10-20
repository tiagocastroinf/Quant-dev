import asyncio
import json
import websockets
import ctypes
import os
import time

# 1. Diretorio atual do projeto e do MSYS2 UCRT64 (onde estao as dependencias da DLL)
project_cpp_dir = os.path.abspath("cpp")
msys_bin_dir = r"C:\msys64\ucrt64\bin"

# 2. Registar os diretórios de DLLs no Python
if hasattr(os, 'add_dll_directory'):
    if os.path.exists(project_cpp_dir):
        os.add_dll_directory(project_cpp_dir)
    if os.path.exists(msys_bin_dir):
        os.add_dll_directory(msys_bin_dir)

# 3. Carregar a DLL primeiro
dll_path = os.path.join(project_cpp_dir, "orderbook.dll")
cpp_lib = ctypes.CDLL(dll_path)

# 4. Configurar a assinatura de TODAS as funções da DLL (incluindo o cpp_clear)
cpp_lib.cpp_clear.argtypes = []
cpp_lib.cpp_clear.restype = None

cpp_lib.cpp_update_bid.argtypes = [ctypes.c_double, ctypes.c_double]
cpp_lib.cpp_update_bid.restype = None

cpp_lib.cpp_update_ask.argtypes = [ctypes.c_double, ctypes.c_double]
cpp_lib.cpp_update_ask.restype = None

cpp_lib.cpp_get_imbalance.argtypes = []
cpp_lib.cpp_get_imbalance.restype = ctypes.c_double

cpp_lib.cpp_get_top_of_book.argtypes = [ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double)]
cpp_lib.cpp_get_top_of_book.restype = None

# Stream da Binance em tempo real (depth20)
BINANCE_WEBSOCKET_URL = "wss://stream.binance.com:9443/ws/btcusdt@depth20@100ms"

async def process_live_stream():
    print("A ligar à Binance WebSocket e a alimentar o motor C++20 em tempo real...\n")
    
    async with websockets.connect(BINANCE_WEBSOCKET_URL) as websocket:
        while True:
            message = await websocket.recv()
            data = json.loads(message)
            
            start_time = time.perf_counter_ns()
            
            # Limpar o estado anterior antes de carregar o novo snapshot de 20 niveis
            cpp_lib.cpp_clear()
            
            # Atualizar Bids no C++
            for bid in data.get('bids', []):
                price, volume = float(bid[0]), float(bid[1])
                cpp_lib.cpp_update_bid(price, volume)
                
            # Atualizar Asks no C++
            for ask in data.get('asks', []):
                price, volume = float(ask[0]), float(ask[1])
                cpp_lib.cpp_update_ask(price, volume)
                
            # Obter métricas diretamente da memória do C++
            imbalance = cpp_lib.cpp_get_imbalance()
            
            best_bid = ctypes.c_double()
            best_ask = ctypes.c_double()
            cpp_lib.cpp_get_top_of_book(ctypes.byref(best_bid), ctypes.byref(best_ask))
            
            end_time = time.perf_counter_ns()
            cpp_latency_us = (end_time - start_time) / 1000.0

            print(f"[LIVE C++ ENGINE] Best Bid: ${best_bid.value:.2f} | Best Ask: ${best_ask.value:.2f} "
                  f"| Imbalance: {imbalance:.4f} | Process Latency: {cpp_latency_us:.2f} µs")

if __name__ == "__main__":
    try:
        asyncio.run(process_live_stream())
    except KeyboardInterrupt:
        print("\nMotor encerrado.")