#include <iostream>
#include <map>
#include <chrono>
#include <numeric>

// Livro de Ordens L2 otimizado
// Asks: menor preço primeiro (std::less)
// Bids: maior preço primeiro (std::greater)
class OrderBook {
private:
    std::map<double, double, std::greater<double>> bids; // Price -> Volume
    std::map<double, double> asks;                       // Price -> Volume

public:
    void update_bid(double price, double volume) {
        if (volume == 0.0) bids.erase(price);
        else bids[price] = volume;
    }

    void update_ask(double price, double volume) {
        if (volume == 0.0) asks.erase(price);
        else asks[price] = volume;
    }

    // Cálculo da métrica de Imbalance: (Vol_Bid - Vol_Ask) / (Vol_Bid + Vol_Ask)
    double calculate_imbalance() const {
        if (bids.empty() || asks.empty()) return 0.0;

        double top_bid_vol = bids.begin()->second;
        double top_ask_vol = asks.begin()->second;

        double total_vol = top_bid_vol + top_ask_vol;
        if (total_vol == 0.0) return 0.0;

        return (top_bid_vol - top_ask_vol) / total_vol;
    }

    void print_top_of_book() const {
        if (!bids.empty() && !asks.empty()) {
            std::cout << "[CPP Engine] Best Bid: $" << bids.begin()->first 
                      << " | Best Ask: $" << asks.begin()->first 
                      << " | Imbalance: " << calculate_imbalance() << "\n";
        }
    }
};

int main() {
    OrderBook book;

    // Medição de latência com std::chrono (alta precisão)
    auto start = std::chrono::high_resolution_clock::now();

    // Simulação de atualizações de alta frequência
    book.update_bid(82050.0, 1.5);
    book.update_bid(82049.5, 2.0);
    book.update_ask(82051.0, 0.8);
    book.update_ask(82051.5, 3.1);

    auto end = std::chrono::high_resolution_clock::now();
    auto elapsed_nanos = std::chrono::duration_cast<std::chrono::nanoseconds>(end - start).count();

    book.print_top_of_book();
    std::cout << "[Benchmark] Processing Latency: " << elapsed_nanos << " ns (" 
              << elapsed_nanos / 1000.0 << " us)\n";

    return 0;
}