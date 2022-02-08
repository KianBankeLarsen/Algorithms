#include "LinkedList.h"

#include <stddef.h>
#include <stdlib.h>

// Allocates and initializes an empty linked list.
// Returns: a pointer to the new linked list, or NULL on error.
// Post: the caller owns the linked list.
LinkedList *LinkedList_new()
{
    LinkedList *ll = malloc(sizeof(LinkedList));
    if (!ll)
    {
        return NULL;
    }
    ll->head = NULL;
    ll->tail = NULL;
    ll->size = 0;
    return ll;
}

// Deallocates the given linked list, including all nodes and their data.
void LinkedList_delete(LinkedList *ll)
{
    LinkedListNode *next;
    for (LinkedListNode *node = ll->head; node; node = next)
    {
        next = node->next;
        free(node);
    }
    free(ll);
}

// Appends the given element to the list.
// The linked list does _not_ take ownership over the element
// (only the linked list node).
// Returns: a pointer to the node with the new element, or NULL on error.
LinkedListNode *LinkedList_append(LinkedList *ll, void *elem)
{
    LinkedListNode *node = malloc(sizeof(LinkedListNode));
    if (!node)
    {
        return NULL;
    }
    node->data = elem;
    node->next = NULL;
    if (ll->tail)
    { // If ll is not empty.
        ll->tail->next = node;
        node->prev = ll->tail;
        ll->tail = node;
    }
    else
    { // else ll is empty.
        ll->head = ll->tail = node;
        node->prev = NULL;
    }
    ++ll->size;
    return node;
}

// Removes and returns the first element from the given list
// Actually just a wrapper for calling LinkedList_remove on head.
// Pre: ll->size != 0
void *LinkedList_popFront(LinkedList *ll)
{
    return LinkedList_remove(ll, ll->head);
}

// Finds the linked list node containing the given element.
// Returns: a pointer to the found node, or NULL if the element was not found.
LinkedListNode *LinkedList_find(LinkedList *ll, void *elem)
{
    LinkedListNode *node = ll->head;
    while (node)
    {
        if (node->data == elem)
        {
            return node;
        }
        node = node->next;
    }
    return NULL;
}

// Removes the given node from the given linked list (and deallocates it).
// Pre: node must belong to ll
// Returns: node->data
void *LinkedList_remove(LinkedList *ll, LinkedListNode *node)
{
    void *nodeData = node->data;
    if (node == ll->head)
    {
        if (node == ll->tail)
        { // if node is the only vertex in the list.
            ll->head = ll->tail = NULL;
        }
        else
        { // else it is just head.
            ll->head = node->next;
            ll->head->prev = NULL;
        }
    }
    else if (node == ll->tail)
    { // Else if node is tail.
        ll->tail = node->prev;
        ll->tail->next = NULL;
    }
    else
    { // Else node must be elsewhere.
        node->next->prev = node->prev;
        node->prev->next = node->next;
    }
    --ll->size;
    free(node);
    return nodeData;
}
