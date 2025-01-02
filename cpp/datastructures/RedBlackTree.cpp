#include "RedBlackTree.h"
using namespace std;

RedBlackTree::RedBlackTree()
{
    TNULL = new Node;
    TNULL->color = "BLACK";
    TNULL->leftChild = nullptr;
    TNULL->rightChild = nullptr;
    root = TNULL;
}

RedBlackTree::~RedBlackTree()
{
    delete root;
}

Node* RedBlackTree::getRoot()
{
    return root;
}

Node* RedBlackTree::findSuccessorNode(Node *node)
{
    if (node->rightChild != TNULL) {
        return findMinimumNode(node->rightChild);
    }
    Node* y = node->parent;
    while (y != TNULL && node == y->rightChild) {
        node = y;
        y = y->parent;
    }
    return y;
}

void RedBlackTree::rbTransplant(Node* u, Node* v){
    if (u->parent==NULL){
        root = v;
    }
    else if(u==u->parent->leftChild){
        u->parent->leftChild = v;
    }
    else{
        u->parent->rightChild = v;
    }
    v->parent=u->parent;
}

void RedBlackTree::deleteNode(int data) {
    cout << "root " << root->data << endl;
    cout << "deleting " << data << endl;
    deleteNodeHelper(data);
}

void RedBlackTree::deleteNodeHelper(int data){
    Node* z = TNULL;
    Node* x;
    Node* y;
    // while (node != NULL) {
    //   if (node->data == data) {
    //     z = node;
    //   }

    //   if (node->data < data) {
    //     node = node->rightChild;
    //   } else {
    //     node = node->leftChild;
    //   }
    // }
    z = treeSearch(data);

    if (z == TNULL) {
      cout << "Key could not be deleted." << endl;
      return;
    }

    // cout << "hi";
    // cout << z->data;

    y = z;
    string y_original_color = y->color;
    // string y_original_color = "BLACK";
    if (z->leftChild == TNULL) {
      x = z->rightChild;
      rbTransplant(z, z->rightChild);
    } else if (z->rightChild == TNULL) {
      x = z->leftChild;
      rbTransplant(z, z->leftChild);
    } else {
      y = findMinimumNode(z->rightChild);
      y_original_color = y->color;
      x = y->rightChild;
      if (y->parent == z) {
        x->parent = y;
      } else {
        rbTransplant(y, y->rightChild);
        y->rightChild = z->rightChild;
        y->rightChild->parent = y;
      }

      rbTransplant(z, y);
      y->leftChild = z->leftChild;
      y->leftChild->parent = y;
      y->color = z->color;
    }
    delete z;
    if (y_original_color.compare("BLACK") == 0) {
      deleteFix(x);
    }
}


void RedBlackTree::deleteFix(Node *x){
    Node * s;
    while (x != root && x->color.compare("BLACK") == 0) {
      if (x == x->parent->leftChild) {
        s = x->parent->rightChild;
        if (s->color.compare("RED") == 0) {
          s->color = "BLACK";
          x->parent->color = "RED";
          leftRotate(x->parent);
          s = x->parent->rightChild;
        }

        if (s->leftChild->color.compare("BLACK") == 0 && s->rightChild->color.compare("BLACK") == 0) {
          s->color = "RED";
          x = x->parent;
        } else {
          if (s->rightChild->color.compare("BLACK") == 0) {
            s->leftChild->color = "BLACK";
            s->color = 1;
            rightRotate(s);
            s = x->parent->rightChild;
          }

          s->color = x->parent->color;
          x->parent->color = "BLACK";
          s->rightChild->color = "BLACK";
          leftRotate(x->parent);
          x = root;
        }
      } else {
        s = x->parent->leftChild;
        if (s->color.compare("RED") == 0) {
          s->color = "BLACK";
          x->parent->color = "RED";
          rightRotate(x->parent);
          s = x->parent->leftChild;
        }

        if (s->rightChild->color.compare("BLACK") == 0 && s->rightChild->color.compare("BLACK") == 0) {
          s->color = "RED";
          x = x->parent;
        } else {
          if (s->leftChild->color.compare("BLACK") == 0) {
            s->rightChild->color = "BLACK";
            s->color = 1;
            leftRotate(s);
            s = x->parent->leftChild;
          }

          s->color = x->parent->color;
          x->parent->color = "BLACK";
          s->leftChild->color = "BLACK";
          rightRotate(x->parent);
          x = root;
        }
      }
    }
    x->color = "BLACK";
}

void RedBlackTree::insertNode(Node *node)
{
    Node *y = NULL;
    Node *x = root;

    while (x != TNULL) {
        y = x;
        // cout << x->data << endl;
        string x_key = to_string(x->data);
        if (compareNodes(node, x_key) < 0) {
            x = x->leftChild;
        }
        else {
            x = x->rightChild;
        }
    }
    node->parent = y;
    if (y == NULL) {
        root = node;
    }
    else {
        string y_key = to_string(y->data);
        if (compareNodes(node, y_key) < 0) {
            y->leftChild = node;
        }
        else {
            y->rightChild = node;
        }
    }
}

void RedBlackTree::fixUp(Node *z)
{
    while (z->parent != NULL && z->parent->color.compare("RED") == 0) {
        if (z->parent == z->parent->parent->leftChild) {
            Node *y = z->parent->parent->rightChild;
            if (y != NULL && y->color.compare("RED") == 0) {
                z->parent->color = "BLACK";
                y->color = "BLACK";
                z->parent->parent->color = "RED";
                z = z->parent->parent;
            }
            else if (z == z->parent->rightChild) {
                z = z->parent;
                leftRotate(z);
            }
            else {
                z->parent->color = "BLACK";
                z->parent->parent->color = "RED";
                rightRotate(z->parent->parent);
            }
        }
        else {
            Node *y = z->parent->parent->leftChild;
            if (y != NULL && y->color.compare("RED") == 0) {
                z->parent->color = "BLACK";
                y->color = "BLACK";
                z->parent->parent->color = "RED";
                z = z->parent->parent;
            }
            else if (z == z->parent->leftChild) {
                z = z->parent;
                rightRotate(z);
            }
            else {
                z->parent->color = "BLACK";
                z->parent->parent->color = "RED";
                leftRotate(z->parent->parent);
            }
        }
    }
    root->color = "BLACK";
}

void RedBlackTree::preOrderTraversal(Node *node)
{
    if (node != TNULL) {
    print(node);
    preOrderTraversal(node->leftChild);
    preOrderTraversal(node->rightChild);
    }
}

void RedBlackTree::inorderTraversal(Node *node)
{
    if (node != TNULL) {
        inorderTraversal(node->leftChild);
        print(node);
        inorderTraversal(node->rightChild);
    }
}

void RedBlackTree::postOrderTraversal(Node *node)
{
    if (node != TNULL) {
        postOrderTraversal(node->leftChild);
        postOrderTraversal(node->rightChild);
        print(node);
    }
}

Node* RedBlackTree::findMinimumNode(Node *node) {
    if (node->leftChild != TNULL) {
        return findMinimumNode(node->leftChild);
    }
    return node;
}

Node* RedBlackTree::findMaximumNode(Node *node) {
    if (node->rightChild != TNULL) {
        return findMaximumNode(node->rightChild);
    }
    return node;
}

Node* RedBlackTree::treeSearch(int data) {
    string key = to_string(data);
    Node* x = root;
    string x_key = to_string(x->data);
    while (x != TNULL && key != x_key) {
        if (key.compare(x_key) < 0) {
            x = x->leftChild;
        }
        else {
            x = x->rightChild;
        }
        if (x == TNULL) {
            break;
            }
        x_key = to_string(x->data);
    } 
    if (x == TNULL) {
        print_missing(data);
    }
    else {
        printsearch(x);
    }
    return x;
}

void RedBlackTree::leftRotate(Node *node)
{
    Node *x = node;
    Node *y = x->rightChild;
    x->rightChild = y->leftChild;
    if (y->leftChild != TNULL) {
        y->leftChild->parent = x;
    }
    y->parent = x->parent;
    if (x->parent == NULL) {
        root = y;
    }
    else if (x == x->parent->leftChild) {
        x->parent->leftChild = y;
    }
    else {
        x->parent->rightChild = y;
    }
    y->leftChild = x;
    x->parent = y;
}

void RedBlackTree::rightRotate(Node *node)
{
    Node *x = node;
    Node *y = x->leftChild;
    x->leftChild = y->rightChild;
    if (y->rightChild != TNULL) {
        y->rightChild->parent = x;
    }
    y->parent = x->parent;
    if (x->parent == NULL) {
        root = y;
    }
    else if (x == x->parent->rightChild) {
        x->parent->rightChild = y;
    }
    else {
        x->parent->leftChild = y;
    }
    y->rightChild = x;
    x->parent = y;
}

Node* RedBlackTree::findPredecessorNode(Node *node)
{
    if (node->leftChild != TNULL) {
        return findMaximumNode(node->leftChild);
    }
    Node* y = node->parent;
    while (y != TNULL && node == y->leftChild) {
        node = y;
        y = y->parent;
    }
    return y;
}

void RedBlackTree::treeMinimum()
{
    if (root != NULL) {
       Node *x = findMinimumNode(root);
       cout << "the minimum is: " << endl;
       print(x);
    }
    else {
        cout << "Tree is empty. No Minimum." << endl;
    }
}

void RedBlackTree::treeMaximum()
{
    if (root != NULL) {
       cout << "the maximum is: " << findMaximumNode(root) << endl;
    }
    else {
        cout << "Tree is empty. No Maximum." << endl;
    }
}

void RedBlackTree::treePreorder()
{
    preOrderTraversal(root);
}

void RedBlackTree::treeInorder()
{
    inorderTraversal(root);
}

void RedBlackTree::treePostorder() 
{
    postOrderTraversal(root);
}

void RedBlackTree::treePredecessor(int data)
{
    Node* x = treeSearch(data);
    if (x != TNULL) {
        if (x == findMinimumNode(root)) {
            cout << "It's Predecessor does NOT EXIST" << endl;
            return;
        }
        else {
           Node* out = findPredecessorNode(x);
           cout << "It's Predecessor is: " << endl;
           print(out);
           return;
        }
        
    }
    else {
        cout << "the key is not found" << endl;
    }
}

void RedBlackTree::treeSucessor(int data) 
{
    Node* x = treeSearch(data);
    if (x != TNULL) {
        if (x == findMaximumNode(root)) {
            cout << "It's Successor does NOT EXIST" << endl;
            return;
        }
        else {
           Node* out = findSuccessorNode(x);
           cout << "It's Successor is: " << endl;
           print(out);
           return;
        }
        
    }
    else {
        cout << "the key is not found" << endl;
    }
}

void RedBlackTree::treeInsert(int data) {
    Node* n = new Node;
    n->data = data;
    n->color = "RED";
    n->parent = NULL;
    n->leftChild = TNULL;
    n->rightChild = TNULL;
    insertNode(n);
    fixUp(n);
}

void RedBlackTree::print(Node *node)
{
      cout << left;
      cout << setw(8)  << node->data;
      cout << right << setw(7) << node->color << endl;
}


int RedBlackTree::compareNodes(Node *node, string key) 
{
    int val = 0;
    string node_key = to_string(node->data);
    val = node_key.compare(key);
    return val;
}

void RedBlackTree::printsearch(Node *node)
{
      cout << left;
      cout << setw(8)  << node->data;
      cout << right << setw(7) << "is FOUND." << endl;
}

void RedBlackTree::print_missing(int data)
{
      cout << left;
      cout << setw(8) << data;
      cout << right << setw(7) << "is NOT FOUND." << endl;
}