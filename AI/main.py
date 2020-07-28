import random as rd
import math as mt

def sig( x): 
	return 1 / (1 + mt.exp(-x))

def RN(m1,m2):
	return sig(m1*w1+m2*w2+b)


def derivata(previsione,obiettivo,n):
	return 2 * (previsione - obiettivo) * previsione*(1 - previsione) *n

def costo(previsione, obiettivo):
	return pow(previsione - obiettivo, 2)

data_set=[
	[1,1,0],
	[1,2,0],
	[2,2,0],
	[3,2,0],
	[3,3,0],
	[10,10,1],
	[10,9,1],
	[9,9,1],
	[9,8,1],
	[8,8,1]
]


rd.seed(1)

w1 = rd.random()
w2 = rd.random()
b = rd.random() 
LR = 0.1

for i in range(10000):
  r = rd.randint(0,len(data_set)-1)
  point=data_set[r]
  m1 = point[0]
  m2 = point[1]

  obiettivo = point[2]
  previsione = RN(m1, m2)

  w1 = w1 - LR * derivata(previsione,obiettivo,m1)
  w2 = w2 - LR * derivata(previsione, obiettivo, m2)
  b = b - LR * derivata(previsione, obiettivo, 1)

print(RN(10,10))