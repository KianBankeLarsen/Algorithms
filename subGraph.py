"""asg3-graphs

The goal of this lab is to let you implement some of the ideas which
are necessary for using graphs in algorithmics and modelling. Such
implementations essentially lie at the very core of the endless
application scenarios. We intentionally will give most of the points for
the easier functions to be implemented. For those who like the
challenge are however also some more complicated tasks. 

If not mentioned otherwise, all adjacency matrices in this assignment
are for unweighted graphs i.e., all elements in the adjacency matrices
integers are 0 or 1. Furthermore, the graphs are undirected, i.e.,
A[i,j] == A[j,i], and furthermore the graphs do not have loops
i.e., A[i,i] == 0.

The functions /docstring/s again contain some examples and usage of the
functions. You can run these examples by executing the script from
command line:

python3 asg3.py

As usual, pushing your solutions to the repository server will trigger
testing of your latest commit (on another set of tests) and you can see
the result as ususal on the server.

Note that the unit tests for the final grading may contain different tests,
and that certain requirements given below are not tested in the testing
period before the final testing. Also the pointing scheme might change. 
Furthermore, the tests might be changed or additional test might be 
introduced during the testing period before the final deadline, to give 
you additional/different feedback.

You may use itertools.

"""

import numpy as np
from math import inf

def isPermutationMatrix(matrix):
    """
    Returns true if matrix is a square permutation matrix.
    matrix is expected to be an instance of np.ndarray 

    Parameters
    ----------
    matrix
        (n,n) np.ndarray : A permutation matrix of integers. Note that numpy uses np.array,
                           which formally is a function that creates an ndarray.
                           Still, the convention is to use np.array when creating
                           arrays (see example below).
    
    Returns
    -------
    bool
        Returns True if A is a permutation matrix.
        Returns False if A is a matrix, but A is not a permutation matrix.

    Raises
    ------
    TypeError
        if A is not a two-dimensional squared np.ndarray 
    ValueError
        if at least one of the entries in A is not integer 0 or 1

    Examples
    --------
    
    >>> A = np.array([[0,1,0],[1,0,0],[0,0,1]])
    >>> isPermutationMatrix(A)
    True
    """
    if len(matrix.shape) == 1:
        raise TypeError("A is not two-dimensional")
    if not all([len(matrix) == len(row) for row in matrix]):
        raise TypeError("A is not square")
    if not all([i == 1 or i == 0 for row in matrix for i in row]):
        raise ValueError("at least one of the entries in A is not integer 0 or 1")

    for sum_row in np.sum(matrix, axis = 1):
        if sum_row != 1:
            return False
    for sum_col in np.sum(matrix, axis = 0):
        if sum_col != 1:
            return False
    return True

def allPermutationMatrices(n):
    """
    Returns a list of all permutation matrices of size n x n. 

    Parameters
    ----------
    n : The size of the resulting permutation matrices should be n x n

    Returns
    -------
    list: A list of all possible permutation matrices of size n x n. 
          Each entry should be an 2-dimesnional np.ndarray of ints

    Raises
    -------
    ValueError: if n<=0 

    Examples
    --------
    >>> allPermutationMatrices(2)
    [array([[1, 0],
           [0, 1]]), array([[0, 1],
           [1, 0]])]
    """
    if n <= 0:
        raise ValueError("n must be larger than 0")

    ## "You may use itertools." ##
    import itertools as it
    return list(map(np.array, it.permutations(np.identity(n).astype(int))))

def isIsomorphicUsingP(A, B, P):
    """
    Returns True if the adjacency matrix B can be changed into the adjaceny matrix A
    by the formula presented in the lecture ( A = P*((P*B)^T ) in mathematical terms,
    where "*" is the matrix-matrix multiplication operator, and "^T" refers to the
    transpose.

    Parameters:
    -----------
    A, B : np.ndarray , two adjacency matrices
    P    : np.ndarray , a permutation matrix

    Returns:
    --------
    bool : see above

    Raises
    -------
    ValueError: if the dimensions of A, B, and P are not identical
    TypeError: if P is not a permutation matrix 

    Examples:
    ---------
    >>> A = np.array([[0, 1, 1], [1, 0, 0], [1, 0, 0]])
    >>> B = np.array([[0, 1, 0], [1, 0, 1], [0, 1, 0]])
    >>> P = np.array([[0, 1, 0], [1, 0, 0], [0, 0, 1]])
    >>> isIsomorphicUsingP(A, B, P)
    True
    
    """
    if not A.shape == B.shape == P.shape:
        raise ValueError("Dimensions of A, B and P are not identical")

    try:
        isPerm = isPermutationMatrix(P)
    except (TypeError, ValueError):
        raise TypeError("P is not a permutation matrix")
    if not isPerm:
        raise TypeError("P is not a permutation matrix")

    return (A == P@(P@B).transpose()).all()

def numIsomorphisms(A, B):
    """
    Returns the number of permutation matrices P, for which A = P*((P*B)^T holds,
    i.e., mathematically speaking, the number of different isomorphisms between
    A and B.

    Parameters:
    -----------
    A, B : np.ndarray, two adjacency matrices

    Returns:
    --------
    int : see above
    
    Examples:
    ---------
    >>> A = np.array([[0, 1, 1], [1, 0, 1], [1, 1, 0]])
    >>> B = np.array([[0, 1, 1], [1, 0, 1], [1, 1, 0]])
    >>> numIsomorphisms(A, B)
    6
    >>> A = np.array([[0, 1, 1], [1, 0, 0], [1, 1, 0]])
    >>> B = np.array([[0, 1, 1], [1, 0, 1], [1, 1, 0]])
    >>> numIsomorphisms(A, B)
    0
    """
    P_0 = perm_mat(A, B, lambda x, y: x == y)

    #return sum([1 for P in allPermutationMatrices(A.shape[0]) if isIsomorphicUsingP(A, B, P)])
    return sum([1 for P in perm_gen(P_0) if isIsomorphicUsingP(A, B, P)])

def moreThanOneSubgraph(A, B):
    """
    NOTE: This methods requires more implementation work and probably a
    careful reading of literature - specifically if you aim to make an
    implementation for graphs A and B having, lets say, more than 20
    vertices. We will only give very few out of the possible 100 points for
    this task, so please think twice before you start. If you like the challenge: go!
    If time allows we will do a comparision and give bonus points to the best solution(s).
    Of course, this assumes that the "best" solution(s) will not "cheat" by using
    existing methods from imported modules. The best solution(s) will be the one(s)
    that can solve the largest of the test instances within 10 seconds and without
    using any imported modules other than numpy. For the testing, the host graph (B) 
    will have approx. twice as many nodes as the potential subgraph (A).

    What you probably learn by trying is: usually it _is_ indeed a very
    good idea to use an existing implementation (assuming it is efficient and correct.)

    Time Limit:
    -----------
    10 seconds 
    
    Returns:
    --------
    True: if A can be found at least twice as a subgraph of B. (Note, A does
    not necessarily need to be an induced subgraph of B. See the lecture
    slides if you are unsure what that means.) See slide 16 on the slideset
    "ullmann.pdf": if you find 2 or more different leaf nodes in the depicted
    search tree for which the property on slide 6 holds, then this method
    return "True".

    Parameters:
    -----------
    A, B : np.ndarray , two adjacency matrices, where the adjacency matrix of
           A represents a graph which has the same number of, or fewer, vertices
           as the graph represented by B. 

    Returns:
    --------
    True or False : see description above
    
    Examples:
    ---------
    >>> A = np.array([[0, 1], [1, 0]])
    >>> B = np.array([[0, 1, 1], [1, 0, 0], [1, 0, 0]])
    >>> moreThanOneSubgraph(A, B)
    True
    """
    def is_subgraph(M):
        C = M@(M@B).transpose()
        return all([A[i, j] == C[i, j] for i in range(A.shape[0]) for j in range(A.shape[1]) if A[i, j] == 1])

    M_0 = perm_mat(A, B, lambda x, y: x >= y)
    subgraph_count = 0
    for M in perm_gen(M_0):
        if is_subgraph(M):
            subgraph_count += 1
        if subgraph_count == 2:
            break
    return subgraph_count == 2

########################## UTILS ###############################
def perm_mat(A, B, comp):
    return np.array([[1 if comp(Bj, Ai) else 0 for Bj in np.sum(B, axis = 0)] for Ai in np.sum(A, axis = 1)])

def do_matrix(M, r, j):
    M_new = M.copy()
    M_new[r] = [1 if i == j else 0 for i in range(M.shape[1])]
    return M_new

def perm_gen(M, i = 0, d = {}): 
        if i == M.shape[0]:
            yield M
        else:
            for j in range(M.shape[1]):
                if M[i, j] == 1 and d.get(j, True):
                    d_new = d.copy()
                    d_new[j] = False
                    yield from perm_gen(do_matrix(M, i, j), i + 1, d_new)
        return
################################################################

if __name__ == "__main__":
    import doctest
    doctest.testmod()