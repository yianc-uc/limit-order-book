#include "order.h"
#include <cassert>

order::order(unsigned int _id, double _price, unsigned int _quantity, bool _is_sell)
{
    id = _id; price = _price; quantity = _quantity; is_sell = _is_sell;
}

void order::set_wrapper(order_summary* _wrapper)
{
    wrapper = _wrapper;
}

void order::set_quantity(unsigned int _new_quantity)
{
    quantity = _new_quantity;
}

void order::push_back(order* new_order)
{
    if (next_order){
        // There is an order following, we are iserting an order
        next_order->prev_order = new_order;
        new_order->next_order = next_order;
        new_order->prev_order = this;
        next_order = new_order;
        // Modify the wrapper
        wrapper->add_quantity(new_order->get_quantity());
    } else {
        // This is the end of the order chain
        next_order = new_order;
        new_order->prev_order = this;
        // Modify the wrapper
        wrapper->add_quantity(new_order->get_quantity());
        wrapper->order_tail = new_order;
    }
    // Set the wrapper of the new order
    new_order->set_wrapper(this->wrapper);
}

bool order::pop()
{
    // Pop the current node from the linked list
    if (!prev_order && !next_order){
        // This is the only order for the price
        wrapper->clear();
        return true;
    } else if (!prev_order && next_order) {
        // This is the first order for the price
        wrapper->add_quantity(-quantity);
        wrapper->order_head = next_order;
        next_order->prev_order = nullptr;
        return false;
    } else if (prev_order && !next_order) {
        // This is the last order for the price
        wrapper->add_quantity(-quantity);
        wrapper->order_tail = prev_order;
        prev_order->next_order = nullptr;
        return false;
    } else {
        // This is in the middle
        wrapper->add_quantity(-quantity);
        prev_order->next_order = next_order;
        next_order->prev_order = prev_order;
        return false;
    }

    // Reclaim the memory for the order
    delete this;
}

void order::update(order* new_order)
{
    // Update the order information
    assert(new_order->get_id()==id && "The id doesn't match!");
    // Push back to the tail of the linked list then pop the current
    wrapper->order_tail->push_back(new_order);
    pop();
}

void order_summary::add_quantity(int delta_quant)
{
    total_quantity += delta_quant;
}

order_summary::order_summary(order* new_order)
{
    price = new_order->get_price();
    total_quantity = new_order->get_quantity();
    order_head = new_order;
    order_tail = new_order;
    new_order->set_wrapper(this);
}

order_summary::~order_summary()
{
    order* tmp = order_head;
    while (tmp){
        order* tp = tmp->next_order;
        delete tmp;
        tmp = tp;
    }
}
