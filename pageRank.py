import numpy as np
from numpy import linalg as la


np.set_printoptions(precision=3)



class DiGraph:
    """A class for representing directed graphs via their adjacency matrices.

    Attributes:
        (fill this out after completing DiGraph.__init__().)
    """
    # Problem 1
    def __init__(self, A, labels=None):
        """Modify A so that there are no sinks in the corresponding graph,
        then calculate Ahat. Save Ahat and the labels as attributes.

        Parameters:
            A ((n,n) ndarray): the adjacency matrix of a directed graph.
                A[i,j] is the weight of the edge from node j to node i.
            labels (list(str)): labels for the n nodes in the graph.
                If None, defaults to [0, 1, ..., n-1].                

        Examples
        ========
        >>> A = np.array([[0, 0, 0, 0],[1, 0, 1, 0],[1, 0, 0, 1],[1, 0, 1, 0]])
        >>> G = DiGraph(A, labels=['a','b','c','d'])
        >>> G.A_hat
        array([[0.   , 0.25 , 0.   , 0.   ],
               [0.333, 0.25 , 0.5  , 0.   ],
               [0.333, 0.25 , 0.   , 1.   ],
               [0.333, 0.25 , 0.5  , 0.   ]])
        >>> steady_state_1 = G.linsolve()
        >>> { k: round(steady_state_1[k],3) for k in steady_state_1}
        {'a': 0.096, 'b': 0.274, 'c': 0.356, 'd': 0.274}
        >>> steady_state_2 = G.eigensolve()
        >>> { k: round(steady_state_2[k],3) for k in steady_state_2}
        {'a': 0.096, 'b': 0.274, 'c': 0.356, 'd': 0.274}
        >>> steady_state_3 = G.itersolve()
        >>> { k: round(steady_state_3[k],3) for k in steady_state_3}
        {'a': 0.096, 'b': 0.274, 'c': 0.356, 'd': 0.274}
        >>> get_ranks(steady_state_3)
        ['c', 'b', 'd', 'a']
        """
        # Checking if A is actually square
        if len(A.shape) == 1:
            raise TypeError("W is not square")
        elif A.shape[0] != A.shape[1]:
            raise TypeError("W is not square")

        # Calculating A_hat by first fixing sinks and then transforming that matrix to A_hat.
        A_tilde = np.where(np.sum(A, axis=0) == 0, 1, A)
        self.A_hat = np.where(A_tilde, A_tilde/np.sum(A_tilde, axis = 0), A_tilde)

        # Raise exception if not enough or too many labels
        # Labels are mapped to strings to assure this property,
        #   this also makes it possible to parse whatever iterable - eg. a set
        if labels:
            if len(labels) != len(A):
                raise ValueError("number of labels is not equal to the number of nodes in the graph")
            self.labels = [*map(str, labels)]
        else:
            self.labels = [*map(str, range(len(A)))]


    def linsolve(self, epsilon=0.85):
        """Compute the PageRank vector using the linear system method.

        Parameters:
            epsilon (float): the damping factor, between 0 and 1.

        Returns:
            dict(str -> float): A dictionary mapping labels to PageRank values.
        """
        # Extract n of nxn matrix
        n = len(self.A_hat)
        # Calculating left side of equation
        A = np.identity(n) - epsilon * self.A_hat
        # Calculating right side of equation
        B = (1 - epsilon)/n * np.array([1 for _ in range(n)])
        # Solving for x (Ax=B)
        return _ret_dict(self.labels, la.solve(A, B))


    def eigensolve(self, epsilon=0.85):
        """Compute the PageRank vector using the eigenvalue method.
        Normalize the resulting eigenvector so its entries sum to 1.

        Parameters:
            epsilon (float): the damping factor, between 0 and 1.

        Return:
            dict(str -> float): A dictionary mapping labels to PageRank values.
        """
        # nxn matrix length extraction
        n = len(self.A_hat)
        # Calculating A_line
        A_line = epsilon * self.A_hat + (1-epsilon)/n * np.ones((n, n))
        # Eigenvalues of A_line
        eig = la.eig(A_line)
        # Picking the eigenvector with eigenvalue 1
        eig_v = np.abs(eig[1][:,np.where(np.isclose(eig[0], 1))[0][0]])
        # Normalizing before returning
        return _ret_dict(self.labels, eig_v/la.norm(eig_v, 1))


    def itersolve(self, epsilon=0.85, maxiter=100, tol=1e-12):
        """Compute the PageRank vector using the iterative method.

        Parameters:
            epsilon (float): the damping factor, between 0 and 1.
            maxiter (int): the maximum number of iterations to compute.
            tol (float): the convergence tolerance.

        Return:
            dict(str -> float): A dictionary mapping labels to PageRank values.
        """
        # Init vector x
        n = len(self.A_hat)
        x = np.array([1/n for _ in range(n)])

        # Do interation until t > maxiter, therefore, range maxiter + 1 -- causes t = maxiter + 1
        for _ in range(maxiter + 1):
            x_t = (epsilon*self.A_hat + (1-epsilon)*1/n*np.ones((n, n))) @ x
            x_t = x_t/la.norm(x_t)
            if la.norm(x_t - x, 1) < tol:
                x=x_t
                break
            x=x_t
        return _ret_dict(self.labels, x/la.norm(x, 1))


def _ret_dict(lab, vec):
        return {k:v for k, v in zip(lab, vec)}

def get_ranks(d):
    """Construct a sorted list of labels based on the PageRank vector.

    Parameters:
        d (dict(str -> float)): a dictionary mapping labels to PageRank values.

    Returns:
        (list) the keys of d, sorted by PageRank value from greatest to least.
    """
    # Sorting on values - rounded to the 8th decimal. Break ties on keys.    
    sort_dict = sorted(d.items(), key=lambda x: (round(-x[1], 8), x[0]))
    # Putting keys in a list
    return [i[0] for i in sort_dict]

# Task 2
def rank_websites(filename="web_stanford.txt", epsilon=0.85):
    """Read the specified file and construct a graph where node j points to
    node i if webpage j has a hyperlink to webpage i. Use the DiGraph class
    and its itersolve() method to compute the PageRank values of the webpages,
    then rank them with get_ranks().

    Each line of the file has the format
        a/b/c/d/e/f...
    meaning the webpage with ID 'a' has hyperlinks to the webpages with IDs
    'b', 'c', 'd', and so on.

    Parameters:
        filename (str): the file to read from.
        epsilon (float): the damping factor, between 0 and 1.

    Returns:
        (list(str)): The ranked list of webpage IDs.

    Examples
    ========
    >>> print(rank_websites()[0:5])
    ['98595', '32791', '28392', '77323', '92715']
    """
    # Read data file
    # Pre: Keys are only listed once
    dictLab = {}
    with open(filename, "r") as input_file:
        for line in input_file.readlines():
            a = line.strip('\n').split('/')
            dictLab[a.pop(0)] = a

    return _do_calc(dictLab, epsilon)

# Task 3
def rank_uefa_teams(filename, epsilon=0.85):
    """Read the specified file and construct a graph where node j points to
    node i with weight w if team j was defeated by team i in w games. Use the
    DiGraph class and its itersolve() method to compute the PageRank values of
    the teams, then rank them with get_ranks().

    Each line of the file has the format
        A,B
    meaning team A defeated team B.

    Parameters:
        filename (str): the name of the data file to read.
        epsilon (float): the damping factor, between 0 and 1.

    Returns:
        (list(str)): The ranked list of team names.

    Examples
    ========
    >>> rank_uefa_teams("psh-uefa-2018-2019.csv",0.85)[0:5]
    ['Liverpool', 'Ath Madrid', 'Paris SG', 'Genk', 'Barcelona']
    """
    # Read data file
    dictLab = {}
    with open(filename, "r") as input_file:
        for line in input_file.readlines():
            home_team, away_team, home_goals, away_goals = line.strip('\n').split(',')
            # Home team lost
            if home_goals < away_goals:
                # Key exists -> append
                if dictLab.get(home_team, 0):
                    dictLab[home_team].append(away_team)
                # Create key with corresponding list
                else:
                    dictLab[home_team] = [away_team]
            # **Symmetric to above ^**
            elif home_goals > away_goals:
                if dictLab.get(away_team, 0):
                    dictLab[away_team].append(home_team)
                else:
                    dictLab[away_team] = [home_team]
    
    return _do_calc(dictLab, epsilon)


def _do_calc(dictLab, epsilon):
    # If not all pages link to others
    allID = set(dictLab).union(*dictLab.values())
    nIDs = len(allID)

    # Dict for looking up index in array
    lookup = {k:v for k, v in zip(allID, range(nIDs))}

    # Making the adjacency matrix
    adj = np.zeros((nIDs, nIDs))
    for k in dictLab:
        for v in dictLab[k]:
            adj[lookup.get(v), lookup.get(k)] += 1

    # Calculate ranking and return 
    g = DiGraph(adj, allID)
    return get_ranks(g.itersolve(epsilon=epsilon))





if __name__ == "__main__":
    import doctest
    doctest.testmod()
