// Raymond Nucuta Honors Project CSE 310 Fall 2022
// to compile and run:
// g++ bst_main.cpp -o bst
// ./bst

#include <iostream>
#include <chrono>
#include <stdio.h> 
#include <stdlib.h>
#include <time.h> 
#include <iostream>
#include <iomanip>
#include <string>

using namespace std;
using namespace std::chrono;

class BST {
    struct Node {
        int data;
        Node* left;
        Node* right;
    };

    Node* root;

    Node* makeEmpty(Node* t) {
        if(t == NULL)
            return NULL;
        {
            makeEmpty(t->left);
            makeEmpty(t->right);
            delete t;
        }
        return NULL;
    }

    Node* insert(int x, Node* t)
    {
        if(t == NULL)
        {
            t = new Node;
            t->data = x;
            t->left = t->right = NULL;
        }
        else if(x < t->data)
            t->left = insert(x, t->left);
        else if(x > t->data)
            t->right = insert(x, t->right);
        return t;
    }

    Node* findMin(Node* t)
    {
        if(t == NULL)
            return NULL;
        else if(t->left == NULL)
            return t;
        else
            return findMin(t->left);
    }

    Node* findMax(Node* t) {
        if(t == NULL)
            return NULL;
        else if(t->right == NULL)
            return t;
        else
            return findMax(t->right);
    }

    Node* remove(int x, Node* t) {
        Node* temp;
        if(t == NULL)
            return NULL;
        else if(x < t->data)
            t->left = remove(x, t->left);
        else if(x > t->data)
            t->right = remove(x, t->right);
        else if(t->left && t->right)
        {
            temp = findMin(t->right);
            t->data = temp->data;
            t->right = remove(t->data, t->right);
        }
        else
        {
            temp = t;
            if(t->left == NULL)
                t = t->right;
            else if(t->right == NULL)
                t = t->left;
            cout << "\n" << left
                << setw(8)  << temp->data
                << " is deleted from the bst." << endl;
            delete temp;
            
        }

        return t;
    }

    void inorder(Node* t) {
        if(t == NULL)
            return;
        inorder(t->left);
        cout << t->data << " ";
        inorder(t->right);
    }

    Node* find(Node* t, int x) {
        if(t == NULL)
            return NULL;
        else if(x < t->data)
            return find(t->left, x);
        else if(x > t->data)
            return find(t->right, x);
        else
            return t;
    }

public:
    BST() {
        root = NULL;
    }

    ~BST() {
        root = makeEmpty(root);
    }

    void insert(int x) {
        root = insert(x, root);
    }

    void remove(int x) {
        root = remove(x, root);
    }

    void display() {
        inorder(root);
        cout << endl;
    }

    void search(int x) {
        root = find(root, x);
    }

    void findS(int x) {
        Node* t = root;
        if(t == NULL){
            cout << "\n" << left
            << setw(8)  << x
            << " is NOT found inside BST." << endl;
        }
        else if(x < t->data){
            cout << "\n" << left
            << setw(8)  << find(t->left, x)->data
            << " is found inside BST." << endl;
        }
        else if(x > t->data){
            cout << "\n" << left
            << setw(8)  << find(t->right, x)->data
            << " is found inside BST." << endl;
        }
        else{
            cout << "\n" << left
            << setw(8)  << t->data
            << " is found inside BST and is the root." << endl;
        }
    }
};

int main() {
    srand (time(NULL));
    BST t;
    int count = 1;
    while (count<=1000) {
        t.insert(count);
        count++;
    }

    int insert_average = 0;
    for (int i=0; i<10; i++){
        auto start = high_resolution_clock::now();
        t.insert(rand()%30+1000);
        auto stop = high_resolution_clock::now();
        auto duration = duration_cast<microseconds>(stop - start);
        insert_average += duration.count();
    }
    
    cout << "Time taken by insert: " << insert_average/10 << " microseconds" << endl;


    int deletion_average = 0;
    for (int i=0; i<10; i++){
        auto start = high_resolution_clock::now();
        t.remove(rand()%1010+1);
        auto stop = high_resolution_clock::now();
        auto duration = duration_cast<microseconds>(stop - start);
        deletion_average += duration.count();
    }

    cout << "Time taken by deletion: " << deletion_average/10 << " microseconds" << endl;

    int search_average = 0;
    for (int i=0; i<10; i++){
        auto start = high_resolution_clock::now();
        t.findS(rand()%1010+1);
        auto stop = high_resolution_clock::now();
        auto duration = duration_cast<microseconds>(stop - start);
        search_average += duration.count();
    }

    cout << "Time taken by search: " << search_average/10 << " microseconds" << endl;

    return 0; 
}