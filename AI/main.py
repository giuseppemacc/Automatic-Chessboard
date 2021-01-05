import random as rd
import math as mt


def RN(m1,m2):
    t=m1*w1+m2*w2+b 
    return sigmoide(t)

def sigmoide(t):
    return 1/(1+mt.exp(-t))

#dataset 
dataset=[
	[1,1,0],
	[2,1,0],
	[1,4,0],
	[2,3,0],
	[4,3,0],
	[9,9,1],
	[7,8,1],
	[6,7,1],
	[9,6,1],
	[9,7,1],
]    
	
def train():

    #pesi inizializzati inizialmente in modo casuale
    w1 = rd.random()
    w2 = rd.random()
    b = rd.random()     

    iterazioni = 10000  #numero di iterazioni 10000
    learning_rate = 0.1 #imposto il learning rate 0.1
    
    for i in range(iterazioni):
       
        point = dataset[rd.randint(0,len(dataset)-1)]
        
        z = point[0] * w1 + point[1] * w2 + b
        pred = sigmoide(point[0] * w1 + point[1] * w2 + b) # previsione della rete
        
        target = point[2] #il mio valore obiettivo
        
        #aggiornamento dei pesi e del bias
        w1 = w1 - learning_rate * 2 * (pred - target) * sigmoide(z)*(1 - sigmoide(z))  * point[0]
        w2 = w2 - learning_rate * 2 * (pred - target) * sigmoide(z)*(1 - sigmoide(z))  * point[1]
        b = b - learning_rate * 2 * (pred - target) * sigmoide(z)*(1 - sigmoide(z))  * 1
        
    return w1, w2, b

#carichiamo i pesi e il bias 
w1, w2, b = train()

pred=[] #array vuoto che conterrà le previsioni

for gatto in dataset:  #per ogni gatto nel dataset
    z = w1 * gatto[0] + w2 * gatto[1] + b
    prediction=sigmoide(z)    #previsione della rete
    if prediction <= 0.5: #se la previsione è minore o uguale a 0.5
        pred.append('0') #aggiungi la stringa "giungla" all'array pred
    else: 
        pred.append('1') #altrimenti aggiungi la stringa "sabbie" all'arrat pred

print(pred) #stampa a schermo l'array pred
print(RN(5,5))