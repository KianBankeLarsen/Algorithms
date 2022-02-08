#include "cycleDetection.h"

#include <stdio.h>
#include <stdlib.h>

// Runs Kahn's algorithm on the graph, and outputs 'CYCLE DETECTED!\n'
//     if a DAG cannot be created, or the vertices as a list e.g. '4, 0, 1, 3, 2\n'
//     representing an ordering in the DAG.
// Generates a topological sort in asymptotic time O(|V| + |E|).
// The output is printed to stdout.
// The input is altered in the process - still a valid graph even though edges are deleted.
//     i.e. edges are deleted correctly. If an outgoing edge is deleted,
//     the corresponding ingoing edge is deleted as well.
void cycleDetection(Graph *g)
{
    LinkedList *L = LinkedList_new();
    LinkedList *S = LinkedList_new();

    // Appends all vertices of G with no incoming edges to S.
    for (int i = 0; i < g->numVertices; i++)
    {
        Vertex *v = g->vertices + i;
        if (!v->inNeighbours->head)
        {
            LinkedList_append(S, v);
        }
    }

    while (S->head)
    {
        Vertex *u = LinkedList_popFront(S);
        LinkedList_append(L, u);

        // Loops over all outgoing edges, v, of u.
        LinkedListNode *next;
        for (LinkedListNode *nv = u->outNeighbours->head; nv; nv = next)
        {
            next = nv->next;
            Vertex *v = nv->data;

            // Append edge v to S if edge e is the only incoming edge.
            if (v->inNeighbours->size == 1)
            {
                LinkedList_append(S, v);
            }

            // Removes edge e from G.
            LinkedListNode *nu = LinkedList_find(v->inNeighbours, u);
            LinkedList_remove(v->inNeighbours, nu);
            LinkedList_remove(u->outNeighbours, nv);
            --g->numEdges;
        }
    }

    // Cycle is detected if numEdges is not 0.
    // Prints topological sort if no cycle was encountered.
    if (g->numEdges)
    {
        printf("CYCLE DETECTED!\n");
    }
    else
    {
        Graph_printList(L);
    }

    LinkedList_delete(L);
    LinkedList_delete(S);
}
