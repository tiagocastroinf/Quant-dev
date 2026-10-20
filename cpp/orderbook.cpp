#include <iostream>
#include <map>

class OrderBook {
private:
    std::map<double, double, std::greater<double>> bids;
    std::map<double, double> asks;

public:
    void clear() {
        bids.clear();
        asks.clear();
    }

    void update_bid(double price, double volume) {
        if (volume == 0.0) bids.erase(price);
        else bids[price] = volume;
    }

    void update_ask(double price, double volume) {
        if (volume == 0.0) asks.erase(price);
        else asks[price] = volume;
    }

    double calculate_imbalance() const {
        if (bids.empty() || asks.empty()) return 0.0;

        double top_bid_vol = bids.begin()->second;
        double top_ask_vol = asks.begin()->second;

        double total_vol = top_bid_vol + top_ask_vol;
        if (total_vol == 0.0) return 0.0;

        return (top_bid_vol - top_ask_vol) / total_vol;
    }

    void get_top_of_book(double& best_bid, double& best_ask) const {
        best_bid = bids.empty() ? 0.0 : bids.begin()->first;
        best_ask = asks.empty() ? 0.0 : asks.begin()->first;
    }
};

static OrderBook g_orderbook;

extern "C" {
    __declspec(dllexport) void cpp_clear() {
        g_orderbook.clear();
    }

    __declspec(dllexport) void cpp_update_bid(double price, double volume) {
        g_orderbook.update_bid(price, volume);
    }

    __declspec(dllexport) void cpp_update_ask(double price, double volume) {
        g_orderbook.update_ask(price, volume);
    }

    __declspec(dllexport) double cpp_get_imbalance() {
        return g_orderbook.calculate_imbalance();
    }

    __declspec(dllexport) void cpp_get_top_of_book(double* best_bid, double* best_ask) {
        double bid = 0.0, ask = 0.0;
        g_orderbook.get_top_of_book(bid, ask);
        *best_bid = bid;
        *best_ask = ask;
    }
}