#include <iostream>
#include <iomanip>
#include <string>

using namespace std;

#ifndef LINKEDLIST_H_
#define LINKEDLIST_H_

struct Element
{
    int key;
    struct Element* next;
};

class LinkedList
{
    private:
        struct Element* head;
        int size;
    public:
        LinkedList();
        ~LinkedList();
        Element* getHead();
        int getSize();
        bool searchElement(int key);
        bool insertElement(int key);
        bool deleteElement(int key);
        void displayList();
};

#endif