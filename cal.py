import cirq
import math as mt

def w(n):
    return n - sum(int(mt.floor(n / (mt.pow(2, i)))) for i in range(1, int(mt.log2(n)) + 1))

n = 10

print(70*n-21*w(n)-21*w(n-1)-21*int(mt.log2(n))-21*int(mt.log2(n-1))-49)
print(10*n-6*int(mt.log2(n))-13)
'''
print(n-w(n))
print(77*n-21*w(n)-12*int(mt.log2(n))-4)
print(44*n-12*w(n)-12*w(n-1)-12*int(mt.log2(n))-12*int(mt.log2(n-1))-28)

print(24*n-12*w(n)-12*int(mt.log2(n))-4)
'''

def l(n, t):
    return int(mt.floor(n / (mt.pow(2, t))))

n = 16
print('ancilla')
ancilla = n - w(n) - mt.floor(mt.log2(n))
print(ancilla)
print(int(mt.log2(2*n/3)))
'''
print(n-w(n)-int(mt.log2(n)))
print(n-w(n))

print(int(mt.log2(n)))

for i in range(1,5):
    print(l(n, i))
for t in range(3,0,-1):
    print('이걸 봐',ancilla-1-(l((n - pow(2, t - 1)), t)+l((n - pow(2, t - 2)), t-1)))
'''

for t in range(int(mt.log2(2 * n / 3)), 0, -1):
    print('t = ', t)

