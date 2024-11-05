// Raymond Nucuta Honors Project CSE 310 Fall 2022
//Skeleton code sourcd from Feng

// to compile and run:
// g++ hash_main.cpp -o hash
// ./hash

#include "Hash.h"
#include <sstream>
#include <chrono>
#include <stdio.h> 
#include <stdlib.h>
#include <time.h> 

using namespace std;
using namespace std::chrono;


int main()
{
   srand (time(NULL));
   int size = 0;

   size = 100010;

   Hash* hash = new Hash(size);
   int vin = 1;
   for(int i = 1; i<=100000; i++){
      hash->hashInsert(i);
   } 

   int insert_average = 0;
   for (int i=0; i<10; i++){
      auto start = high_resolution_clock::now();
      hash->hashInsert(rand()%30+100000);
      auto stop = high_resolution_clock::now();
      auto duration = duration_cast<microseconds>(stop - start);
      insert_average += duration.count();
   }
    
   cout << "Time taken by insert: " << insert_average/10 << " microseconds" << endl;

   int deletion_average = 0;
    for (int i=0; i<10; i++){
        auto start = high_resolution_clock::now();
        hash->hashDelete(rand()%100010+1);
        auto stop = high_resolution_clock::now();
        auto duration = duration_cast<microseconds>(stop - start);
        deletion_average += duration.count();
    }

    cout << "Time taken by deletion: " << deletion_average/10 << " microseconds" << endl;

    int search_average = 0;
    for (int i=0; i<10; i++){
        auto start = high_resolution_clock::now();
        hash->hashSearch(rand()%100010+1);
        auto stop = high_resolution_clock::now();
        auto duration = duration_cast<microseconds>(stop - start);
        search_average += duration.count();
    }

    cout << "Time taken by search: " << search_average/10 << " microseconds" << endl;

   return 0;
}