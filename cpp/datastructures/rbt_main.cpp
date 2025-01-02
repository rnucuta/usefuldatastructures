// Raymond Nucuta Honors Project CSE 310 Fall 2022
// skeleton code sourced from Feng
// red black tree implementation 

// to compile and run:
// g++ -g -Wall rbt_main.cpp RedBlackTree.cpp -o rbt
// ./rbt

#include "RedBlackTree.h"
#include <chrono>

using namespace std;
using namespace std::chrono;


int main()
{
   RedBlackTree* rbt = new RedBlackTree();
   
   srand (time(NULL));
    int count = 1;
    while (count<=1000) {
      //   cout << "insert " << count << endl;
        rbt->treeInsert(count);
        count++;
    }

    int insert_average = 0;
    for (int i=0; i<10; i++){
        auto start = high_resolution_clock::now();
        rbt->treeInsert(rand()%30+1000);
        auto stop = high_resolution_clock::now();
        auto duration = duration_cast<microseconds>(stop - start);
        insert_average += duration.count();
    }
    
    cout << "Time taken by insert: " << insert_average/10 << " microseconds" << endl;

    int deletion_average = 0;
    for (int i=0; i<10; i++){
        auto start = high_resolution_clock::now();
        rbt->deleteNode(rand()%1010+1);
        auto stop = high_resolution_clock::now();
        auto duration = duration_cast<microseconds>(stop - start);
        deletion_average += duration.count();
    }

    cout << "Time taken by deletion: " << deletion_average/10 << " microseconds" << endl;

   int search_average = 0;
    for (int i=0; i<10; i++){
        auto start = high_resolution_clock::now();
        rbt->treeSearch(rand()%1010+1);
        auto stop = high_resolution_clock::now();
        auto duration = duration_cast<microseconds>(stop - start);
        search_average += duration.count();
    }

    cout << "Time taken by search: " << search_average/10 << " microseconds" << endl;
  
   return 0;
}