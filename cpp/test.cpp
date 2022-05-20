#include <iostream>
#include "order.h"
#include "OrderBook.h"
#include <vector>
#include <string>

using namespace std;

// Memory tracker
struct AllocationMetrics {
    uint32_t TotalAllocated = 0;
    uint32_t TotalFreed = 0;

    uint32_t CurrentUsage(){return (TotalAllocated - TotalFreed);}
};

static AllocationMetrics myAllocationMetrics;

void* operator new(size_t size){
    myAllocationMetrics.TotalAllocated += size;

    return malloc(size);
}

void operator delete(void* memory, size_t size) {
    myAllocationMetrics.TotalFreed += size;

    return free(memory);
}

static void PrintMemoryUsage(){
    cout << "Current usage: " << myAllocationMetrics.CurrentUsage() << endl;
}

int main(){
    OrderBook book;
    vector <order*> order_list;

    cout << "start" << endl;

    order_list.push_back(new order(1,100,5,false));
    order_list.push_back(new order(2,95,5,false));
    order_list.push_back(new order(3,90,5,false));
    order_list.push_back(new order(4,200,5,true));
    order_list.push_back(new order(5,205,5,true));
    order_list.push_back(new order(6,210,5,true));

    string delim(30,'-');

    // (1) Test with adding new orders
    for (auto it=order_list.begin();it != order_list.end();it++){
        book.process(*it);
    }

    cout << book << endl << delim << endl;

    // (2) Test with updating orders
    PrintMemoryUsage();
    order* tmp = new order(1,100,20,false);
    book.process(tmp);
    delete tmp; tmp = nullptr;
    PrintMemoryUsage();

    cout << book << endl << delim << endl;

    // (3) Test with deleting orders
    book.process(new order(1,100,0,false));

    cout << book << endl << delim << endl;

    // (4) Test with market orders  

    // book.market_order(true, 8, 80);

    cout << book << endl << delim << endl;

    return 0;
}