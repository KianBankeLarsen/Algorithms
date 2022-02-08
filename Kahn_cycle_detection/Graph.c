#include "Graph.h"

#include <stddef.h>
#include <stdlib.h>
#include <stdio.h>

// Allocates and constructs a new graph with n vertices.
// Returns a pointer to the new graph, or NULL on error.
// Post: the caller owns the graph.
Graph *Graph_new(int n)
{
    // Allocates memory for graph and vertex array.
    Graph *g = malloc(sizeof(Graph));
    Vertex *v = malloc(sizeof(Vertex) * n);
    if (!g || !v)
    {
        return NULL;
    }

    // Initializes graph struct.
    g->numVertices = n;
    g->numEdges = 0;
    g->vertices = v;

    // Initializes array of vertices.
    for (int i = 0; i < n; i++)
    {
        Vertex *vx = v + i;
        vx->id = i;
        vx->outNeighbours = LinkedList_new();
        vx->inNeighbours = LinkedList_new();
        if (!vx->outNeighbours || !vx->inNeighbours)
        {
            return NULL;
        }
    }
    return g;
}

// Adds an edge from the i'th to the j'th vertex (0-indexed).
void Graph_addEdge(Graph *g, int i, int j)
{
    Vertex *vi = g->vertices + i, *vj = g->vertices + j;
    LinkedList_append(vi->outNeighbours, vj);
    LinkedList_append(vj->inNeighbours, vi);
    ++g->numEdges;
    return;
}

// Reads a graph from the given file and returns a newly
//     constructed Graph representing it.
// Returns a pointer to the read graph, or NULL on error.
// Post: the caller owns the graph.
Graph *Graph_read(const char *filename)
{
    // getline will allocate a buffer for storing the line.
    FILE *stream;
    char *line = NULL;
    size_t len = 0;

    stream = fopen(filename, "r");
    if (!stream)
    {
        return NULL;
    }

    // Interprets the first line as an integer (number of vertices).
    int nVertices;
    if (getline(&line, &len, stream) != -1)
    {
        nVertices = atoi(line);
    }
    else
    {
        free(line);
        return NULL;
    }

    Graph *g = Graph_new(nVertices);
    if (!g)
    {
        free(line);
        return NULL;
    }

    // It is not required to handle input errors,
    //     but this function makes it possible.
    void *Graph_inputError(char *err)
    {
        fprintf(stderr, "Input file: %s\n", err);
        free(line);
        Graph_delete(g);
        return NULL;
    }

    // Creates edges by inspecting the individual chars in string line.
    //     Edge is created if inspected char is '1'.
    // Returns NULL if the given file does not contain a proper adjacency matrix.
    // Matrix is interpreted as i rows, j columns.
    ssize_t nread;
    for (int i = 0; i < nVertices; i++)
    {
        if ((nread = getline(&line, &len, stream)) <= 1)
        {
            return Graph_inputError("Not enough rows");
        }
        else if (nread != nVertices + 1)
        {
            return Graph_inputError("Incorrect amount of columns or missing newline");
        }
        for (int j = 0; j < nVertices; j++)
        {
            if (line[j] == '1')
            {
                Graph_addEdge(g, i, j);
            }
        }
    }
    if (getline(&line, &len, stream) != -1)
    {
        return Graph_inputError("Too many rows");
    }

    free(line);
    fclose(stream);
    return g;
}

// 1. Deletes outNeighbour and inNeighbour linked lists of every vertex.
// 2. Deallocates array of vertices.
// 3. Deallocates graph struct.
void Graph_delete(Graph *g)
{
    for (int i = 0; i < g->numVertices; i++)
    {
        Vertex *v = g->vertices + i;
        LinkedList_delete(v->outNeighbours);
        LinkedList_delete(v->inNeighbours);
    }
    free(g->vertices);
    free(g);
    return;
}

// Prints contents of a linked list: "4, 0, 1, 3, 2\n".
// Prints only newline if the given linked list is empty.
void Graph_printList(LinkedList *ll)
{
    LinkedListNode *node = ll->head;
    while (node)
    {
        Vertex *v = node->data;
        if (node == ll->head)
        {
            printf("%d", v->id);
        }
        else
        {
            printf(", %d", v->id);
        }
        node = node->next;
    }
    printf("\n");
    return;
}

// Prints outNeighbour and inNeighbour edges of every vertex in a graph.
void Graph_print(Graph *g)
{
    for (int i = 0; i < g->numVertices; i++)
    {
        Vertex v = g->vertices[i];
        printf("**NODE %d**\n", i);
        printf("Out: ");
        Graph_printList(v.outNeighbours);
        printf("In: ");
        Graph_printList(v.inNeighbours);
        printf("\n");
    }
    return;
}
