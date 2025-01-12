#include <iostream>
#include <iomanip>
#include <stdlib.h>
#include <string>

using namespace std;

#ifndef REDBLACKTREE_H_
#define REDBLACKTREE_H_

struct Node
{
   int data;
   Node *parent;
   Node *leftChild;
   Node *rightChild;
   string color;
};

class RedBlackTree
{
    private:
        Node *root;
        Node *TNULL;
    public:
        RedBlackTree();
        ~RedBlackTree();
        Node* getRoot();
        void rbTransplant(Node* u, Node* v);
        Node* findMinimumNode(Node *node);
        void deleteNode(int data);
        // int deleteNode(Node *node);
        void deleteNodeHelper(int data);
        void deleteFix(Node *x);
        void insertNode(Node *node);
        void fixUp(Node *node);


        void preOrderTraversal(Node *node);
        void inorderTraversal(Node *node);
        void postOrderTraversal(Node *node);


        Node* findMaximumNode(Node *node);
        Node* treeSearch(int data);
        void leftRotate(Node *node);
        void rightRotate(Node *node);
        Node* findPredecessorNode(Node *node);
        Node* findSuccessorNode(Node *node);

        void treeMinimum();
        void treeMaximum();
        void treePreorder();
        void treeInorder();
        void treePostorder();
        void treePredecessor(int data);
        void treeSucessor(int data);
        void treeInsert(int data);

        void print(Node *node);
        void printsearch(Node *node);
        void print_missing(int data);
        int compareNodes(Node *node, string key);
};
#endif