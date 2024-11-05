#include "LinkedList.h"

using namespace std;

class Hash
{
   private:
      LinkedList* hashTable;
      int m;
	public:
      Hash(int size);
      ~Hash();
      bool hashSearch(int key);
      bool hashInsert(int key);
      bool hashDelete(int key);
      void hashDisplay();
      int hashFunction(string key);
      int getHashSize();
  };

Hash::Hash(int size)
{
    m = size;
    hashTable = new LinkedList[m];
}

Hash::~Hash()
{
    for (int i = 0; i < m; i++) {
         hashTable[i].~LinkedList();
    }
    delete[] hashTable;
}

bool Hash::hashSearch(int key)
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

bool Hash::hashInsert(int key)
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

bool Hash::hashDelete(int key)
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

int Hash::getHashSize() {
    return m;
}

void Hash::hashDisplay()
{
    int s;
    for (int i = 0; i < m; ++i) {
        s=hashTable[i].getSize();
        cout << "HashTable["<< i << "]"<< ", " << "size = " << s << endl;
        hashTable[i].displayList();
        cout << "\n";
    } 
}

int Hash::hashFunction(string key)
{
     unsigned p = 0;
       for (int i = 0; i < key.length(); i++) {
	        p = 31*p + key.at(i);
       }
    return p % m;
}