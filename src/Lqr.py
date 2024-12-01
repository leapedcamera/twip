import Control
import yaml
import scipy
import numpy as np
import copy
import control as ct

# Implementation of LQR using:
#  (1986). Ito and Banks. A NUMERICAL ALGORITHM FOR OPTIMAL FEEDBACK GAINS IN HIGH DIMENSIONAL LQR PROBLEMS
#
#  with support from:
#  (1991). Mehrmann, V.L. (eds) The Autonomous Linear Quadratic Control Problem
#  (2019). Schwarz et al. Robust Task-Parallel Solution of the Triangular Sylvester Equation
#  (1968). Kleinman. On an Iterative Technique for Riccati Equation Computation
#  (1970). Bartels and Stewart. Solution of the Matrix Equation AX + XB = C 

class Lqr(Control.Control):
    def __init__(self, paramFile):
        Control.Control.__init__(self, paramFile)
        with open(paramFile, 'r') as file:       
            data = yaml.safe_load(file)
            if "Q" in data:
                self.Q = np.diag(data["Q"])
            if "R" in data:
                self.R =data["R"]

    
    def getInput(self, x, dt):
        error =  x - self.xDes
        u = np.matmul(-self.K, error)
        return u
    
    def setGain(self, A, B):
        K = self.chandrasekhar(A, B, self.Q, self.R)
        self.K = self.kleinman(A, B, self.Q, self.R, K)     
        eval, evec = np.linalg.eig(A - np.matmul(B, K))
        pause = True 
       
    
    def sylv(self, A, B, C ):
        Aprime, U = scipy.linalg.schur(A, output='complex')
        Bprime, V = scipy.linalg.schur(B, output='complex')
        Cprime = np.matmul(U.conj().T, np.matmul(C, V))
        q = np.shape(Bprime)[0]
        p = np.shape(Aprime)[0]

        Y = Cprime
        for l in range(q):
            for k in range(p-1, -1, -1):
                Y[k,l] = Y[k,l] / (Aprime[k,k] + Bprime[l,l])
                Y[:k,l] = Y[:k,l] - Aprime[:k, k] * Y[k,l]
                Y[k,l+1:q] = Y[k,l+1:q] - Y[k,l] * Bprime[l, l + 1:q]
        X = np.matmul(U, np.matmul(Y, V.conj().T)).real
        return X
    
    def chandrasekhar(self, A, B, Q, R):
        n = np.size(B)
        Li = Q
        Lii = Q
        Ki = np.zeros([1,n])
        h = .1
        iterations = int(10 / h)

        for i in range(iterations):
            K = Ki + h * (3/2 * np.matmul( B.T, np.matmul( Li.T, Li ) ) \
                    - 1/2 * np.matmul( B.T, np.matmul(Lii.T, Lii) ) )
            
            K = ( K + Ki ) / 2

            L = 2 * np.matmul( Li, np.linalg.inv(  \
                np.eye(n) - h/2 * ( A - np.matmul(B, K) ) ) ) - Li
            
            K = Ki + h/2 * ( np.matmul(B.T, np.matmul(L.T, L)) + \
                            np.matmul(B.T, np.matmul(Li.T, Li)) )
            
            Ki = K
            Lii = Li
            Li = L

        return K
    
    def kleinman(self, A, B, Q, R, Ki):
        eval, evec = np.linalg.eig(A - np.matmul(B, Ki))
        for iVal in eval:
            if iVal >= 0:
                pause = True
        K = Ki
        for i in range(50):
            S = A - np.matmul(B, K)
            V = np.matmul(K.T, K) * R  + Q
            P = self.sylv(S.T, S, -V)
            K = 1 / R * np.matmul(B.T, P)
        return K

    def simpleSmith(self, r, S, D):
        n = np.shape(S)[0]
        X = np.zeros([n,n])
        Ur = np.matmul(np.linalg.inv(np.eye(n) - r * S), np.eye(n) + r * S)
        Yr = 2 * r *  np.matmul(np.linalg.inv(np.eye(n) - r * S.T), \
            np.matmul(D.T, np.matmul(D, np.linalg.inv(np.eye(n) - r * S))))
        for i in range(500):
            X = np.matmul(Ur.T, np.matmul(X, Ur)) + Yr
        return X
            
    def smith(self, A, B, Q, R, Ki):
        n = np.size(Ki)
        # Solve for K1
        S = A - np.matmul(B, Ki)
        r = 0.1

        # First Half
        D = Ki
        X1 = self.simpleSmith(r, S, D)

        # Second Half
        D = Q
        X2 = self.simpleSmith(r, S, D)

        # Combine
        K = np.matmul(B.T, X1) + np.matmul(B.T, X2)

        D = K - Ki

        Ur = np.matmul( np.linalg.inv( np.eye(n) - r * S ), \
            np.eye(n) + r * S  )
        M = np.matmul( D, np.linalg.inv( np.eye(n) - r * S ) )
        J = 2 * r * np.matmul(B.T, np.matmul(M.T, M))
        F = 0
        for k in range(500):
            M = np.matmul( M, Ur )
            J = J + 2 * r * np.matmul(B.T, np.matmul(M.T, M))
            F = np.append(F, J)
        return J
