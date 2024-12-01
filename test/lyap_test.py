import sys, os
testdir = os.path.dirname(__file__)
srcdir = '../src'
sys.path.insert(0, os.path.abspath(os.path.join(testdir, srcdir)))

import numpy as np
import scipy
import Lqr

lqr = Lqr.Lqr("config/settings.yml")

# Smith method
# S.T * X + X * S + D.T * D = 0
n = 5
hurwitz = False
X = np.zeros([n,n])
while hurwitz == False:
    hurwitz = True
    S = np.random.random_integers(-100, 100, (n, n))
    e, ev = np.linalg.eig(S)
    for eval in e:
        if eval > 0:
            hurwitz = False
D = np.random.rand(n,n)
r = 0.1
Ur = np.matmul(np.linalg.inv(np.eye(n) - r * S), np.eye(n) + r * S)
Yr = 2 * r *  np.matmul(np.linalg.inv(np.eye(n) - r * S.T), \
    np.matmul(D.T, np.matmul(D, np.linalg.inv(np.eye(n) - r * S))))
for i in range(500):
    X = np.matmul(Ur.T, np.matmul(X, Ur)) + Yr
residual = np.matmul(S.T, X) + np.matmul(X,S) + np.matmul(D.T, D)
if abs(residual[0,0]) > 1e-9:
    pause = True 

# Sylvester solver via Bartels-Stewart
n = 5
failures = 0
for k in range(500):
    A = np.random.rand(n,n)
    Q =  np.random.rand(n,n)
    P = lqr.sylv( A.T, A, Q )
    residual = np.matmul(A.T, P) + np.matmul(P, A) - Q
    if(abs(residual[0,0])> 1e-10):
        eigenvaluesA, eigenvectors = np.linalg.eig(A)
        eigenvaluesB, eigenvectors = np.linalg.eig(A.T)
        Aprime, U = scipy.linalg.schur(A)
        Bprime, V = scipy.linalg.schur(A.T)
        failures += 1
    else:
        pause = True

# Test of LQR method per Banks and Ito
n = 5
A = np.zeros([n,n])
Q = np.zeros([n,n])
B = np.zeros([n,1])
C = np.eye(n)
Qprime = np.zeros([1,n])

for i in range(n-1):
    A[i,i+1] = 1
Q[0,0] = 1
Qprime[0,0] = 1
B[n-1] = 1

R = 1
K = lqr.chandrasekhar(A, B, Q, R)

# Choice A, traditional kleinman step
Ktrad = lqr.kleinman(A, B, Q, R, K)

# Choice B, modified smith step
Ksmith = lqr.smith(A, B, Q, R, K)

if abs(Ktrad[0,0] - 1) > 1e-9:
    pause = True

if abs(Ksmith[0,0] - 1) > 1e-9:
    pause = True