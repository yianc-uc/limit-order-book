#ifndef __ORDER_H__
#define __ORDER_H__

#include <iostream>

using namespace std;

class order;
class order_summary;

class order {
    unsigned int id;
    double price;
    unsigned int quantity;
    bool is_sell;
public:
    order_summary* wrapper = nullptr;
    order* prev_order = nullptr;
    order* next_order = nullptr;

    order(unsigned int _id, double _price, unsigned int _quantity, bool _is_sell);
    unsigned int get_id() const {return id;};
    double get_price() const {return price;};
    unsigned int get_quantity() const {return quantity;};
    bool get_is_sell() const {return is_sell;};
    void set_wrapper(order_summary* _wrapper);
    void set_quantity(unsigned int _new_quantity);

    // Insert and erase
    void push_back(order* new_order);
    bool pop();
    void update(order* new_order);
};

class order_summary {
    double price;
    unsigned int total_quantity = 0;
public:
    order* order_head;
    order* order_tail;

    void add_quantity(int delta_quant);
    void clear(){total_quantity=0;};
    
    unsigned int get_quantity(){return total_quantity;};
    double get_price(){return price;};

    // Initialize order summary by one new order
    order_summary(order* new_order);
    // Destructor
    ~order_summary();
};
#endif // __ORDER_H__