#include "HashMap.h"

HashMap::HashMap(int size)
{
    m = size;
    hashTable = new LinkedList[m];
}

HashMap::~HashMap()
{
    for (int i = 0; i < m; i++) {
         hashTable[i].~LinkedList();
    }
    delete[] hashTable;
}

bool HashMap::hashSearch(int key)
{
    string str = std::to_string(key);
    bool found = false;
    int ind = hashFunction(str);
    if (hashTable[ind].searchElement(key)) {
        found = true;
    }

   if (found == true)
      cout << "\n" << left
          << setw(8)  << key
          << " is found inside the hash table." << endl;
   else
      cout << "\n" << left
           << setw(8)  << key
           << " is NOT found inside the hash table." << endl;
   return found;
}

bool HashMap::hashInsert(int key)
{
    string str =std::to_string(key);
    int index = hashFunction(str);
   if (hashTable[index].insertElement(key)) {
    return true;
   }
   else {
    return false;
   }
}

bool HashMap::hashDelete(int key)
{
    string str = std::to_string(key);
    int index = hashFunction(str);
    if (hashTable[index].deleteElement(key)) {
      cout << "\n";
      cout << setw(8)  << key
           << " is deleted from hash table." << endl;
           return true;
    }
    else {
      cout << "\n";
      cout << setw(8)  << key
           << " is NOT deleted from hash table." << endl;
       return false;
    }
}

int HashMap::getHashSize() {
    return m;
}

void HashMap::hashDisplay()
{
    int s;
    for (int i = 0; i < m; ++i) {
        s=hashTable[i].getSize();
        cout << "HashTable["<< i << "]"<< ", " << "size = " << s << endl;
        hashTable[i].displayList();
        cout << "\n";
    } 
}

int HashMap::hashFunction(string key)
{
    unsigned p = 0;
       for (int i = 0; i < key.length(); i++) {
	        p = 31*p + key.at(i);
       }
    return p % m;
}