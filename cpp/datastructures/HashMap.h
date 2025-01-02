#include "LinkedList.h"

using namespace std;

class HashMap
{
   private:
      LinkedList* hashTable;
      int m;
	public:
      HashMap(int size);
      ~HashMap();
      bool hashSearch(int key);
      bool hashInsert(int key);
      bool hashDelete(int key);
      void hashDisplay();
      int hashFunction(string key);
      int getHashSize();
  };
