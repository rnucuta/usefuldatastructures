#include <iostream>
#include <iomanip>
#include <string>

using namespace std;
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

LinkedList::LinkedList()
{
    head = NULL;
}

LinkedList::~LinkedList()
{
    Element* curr = head;
    Element* prev = NULL;
    int ElementCount = 0;
    
    while (curr != NULL) {
        prev = curr;
        curr = curr->next;
        delete prev;
        ElementCount++;
    }
}

Element* LinkedList::getHead()
{
    return head;
}

int LinkedList::getSize()
{
    size = 0;
    Element* curr = head;
    while (curr != NULL) {
        size++;
        curr = curr->next;
    }
    return size;
}

bool LinkedList::searchElement(int key)
{
    Element* ptr = head;
    while (ptr != NULL) {
        if (ptr->key == key) {
            return true;
        }
        ptr = ptr->next;
    }
    return false;
}

bool LinkedList::insertElement(int key)
{
    //----
    if (searchElement(key) == true) {
        return false;
    }
    else if (head == NULL) {
        Element* c = new Element;
        c->key = key;
        head = c;
    }
    else {
        Element* c = new Element;
        c->key = key;

        c->next = head;
        head = c;
    }
    return true;
}

bool LinkedList::deleteElement(int key)
{
     Element* curr = head;
     Element* prev = NULL;
    
    if (head->key == key) {
        head = head->next;
        return true;
    }

    while (curr != NULL) {
        if (key == curr->key) {
            prev->next = curr->next;
            delete curr;
            return true;
        }
        prev = curr;
        curr = curr->next;
    }
    return false;
}

void LinkedList::displayList()
{
   struct Element *temp = head;
   if(head == NULL)
   {
        cout << "Empty list.\n";
   }
   else
   {
      while(temp != NULL)
      {
         cout << right   << setw(8)  << temp->key << "\n";
         temp = temp->next;
      }
   }
}