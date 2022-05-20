#include "order.h"
#include "OrderBook.h"
#include <string>
#include <iostream>

using namespace std;

void OrderBook::process_ask(order* new_order)
{
    auto loc = order_list.find(new_order->get_id());
    if (loc != order_list.end()){
        // This is an existing order
        if (new_order->get_quantity() == 0){
            // Remove the order
            bool ret = loc->second->pop();
            if (ret){
                // The price should be removed as well
                ask_tree.erase(price_list[new_order->get_price()]);
                // Delete the tree node
                delete price_list[new_order->get_price()]->second;
            }
            // Remove from map
            order_list.erase(loc);
            // Remove from price list
            price_list.erase(new_order->get_price());
            // Remove the new_order
            delete new_order;
        } else {
            // Update the order info
            loc->second->update(new_order);
        }
    } else {
        // New order
        if (new_order->get_quantity() != 0){
            auto loc = price_list.find(new_order->get_price());

            if (loc != price_list.end()){
                // Current price exists
                loc->second->second->order_tail->push_back(new_order);
            } else {
                // Create a node for the current price
                order_summary* pt = new order_summary(new_order);
                // Insert in the tree
                auto ret = ask_tree.insert({new_order->get_price(), pt});
                // Insert in price list
                price_list[new_order->get_price()] = ret.first;
            }
            // Insert in the order_list
            order_list[new_order->get_id()] = new_order;
        }
    }
}

void OrderBook::process_bid(order* new_order)
{
    auto loc = order_list.find(new_order->get_id());
    if (loc != order_list.end()){
        // This is an existing order
        if (new_order->get_quantity() == 0){
            // Remove the order
            bool ret = loc->second->pop();
            if (ret){
                // The price should be removed as well
                bid_tree.erase(price_list[new_order->get_price()]);
                // Delete the tree node
                delete price_list[new_order->get_price()]->second;
            }
            // Remove from map
            order_list.erase(loc);
            // Remove from price list
            price_list.erase(new_order->get_price());
            // Remove the new_order
            delete new_order;
        } else {
            // Update the order info
            loc->second->update(new_order);
            // Reset the order pointer from order_list
            loc->second = new_order;
        }
    } else {
        // New order
        if (new_order->get_quantity() != 0){
            auto loc = price_list.find(new_order->get_price());

            if (loc != price_list.end()){
                // Current price exists
                loc->second->second->order_tail->push_back(new_order);
            } else {
                // Create a node for the current price
                order_summary* pt = new order_summary(new_order);
                // Insert in the tree
                auto ret = bid_tree.insert({new_order->get_price(), pt});
                // Insert in price list
                price_list[new_order->get_price()] = ret.first;
            }
            // Insert in the order_list
            order_list[new_order->get_id()] = new_order;
        }
    }
}

void OrderBook::process(order* new_order)
{
    if (new_order->get_is_sell()){
        // Sell order
        process_ask(new_order);
    } else{
        // Buy order
        process_bid(new_order);
    }
    // Update the best ask and bid price
    best_ask = ask_tree.begin()->first;
    best_bid = bid_tree.rbegin()->first;
}

ostream& operator<<(ostream& os, const OrderBook& data)
{
    string delm(25, '-');
    os << "Buy order" << delm << endl;
    for (auto it=data.bid_tree.begin();it != data.bid_tree.end();it++){
        os << "Price is " << it->first << ", the quantity is " << it->second->get_quantity() << endl;
    }

    os << "Sell order" << delm << endl;
    for (auto it=data.ask_tree.begin();it != data.ask_tree.end();it++){
        os << "Price is " << it->first << ", the quantity is " << it->second->get_quantity() << endl;
    }

    os << "Summary: the best ask price is " << data.best_ask << " and the best bid price is " << data.best_bid << endl;

    return os;
}
