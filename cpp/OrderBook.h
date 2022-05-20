#ifndef __ORDERBOOK_H__
#define __ORDERBOOK_H__

#include <map>
#include <unordered_map>
#include "order.h"
#include <iostream>

using namespace std;

class OrderBook {
    map<double,order_summary*> ask_tree, bid_tree;
    unordered_map<unsigned int, order*> order_list;
    unordered_map<double, map<double,order_summary*>::iterator> price_list;
    void process_ask(order* new_order);
    void process_bid(order* new_order);
    //void market_order_sell(unsigned int _quantity, double _price);
    //void market_order_buy(unsigned int _quantity, double _price);
public:
    double best_ask, best_bid;

    OrderBook(){};
    void process(order* new_order);
    //void market_order(bool _is_sell, unsigned int _quantity, double _price);
    void remove_price(double _price);
    friend ostream& operator<<(ostream& os, const OrderBook& data);
};

#endif // __ORDERBOOK_H__