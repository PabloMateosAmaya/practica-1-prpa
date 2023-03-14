from multiprocessing import Process,Semaphore,Value,BoundedSemaphore
from random import randint , random
from time import sleep

#definimos la cantidad de procesos y la cantidad de numeros que me va a dar cada proceso
NPROD=10
NVUELTAS=10


def productor(index,lsem,lvalues,semconsumidor):
    #poner en marcha el productor index=[0,1..,NPROD-1]
    for i in range(NVUELTAS):
        #vemos si nos deja pasar el semaforo index
        lsem[index].acquire()
        print(f'vamos a generar el valor {index}')
        
        lvalues[index].value += randint(1 , 10)
        print(f'en nuevo valor es{lvalues[index].value}')
        semconsumidor.release()
        sleep(random())
        
    #haremos todo eso NVUELTAS veces y cuando acabemos
    #miraremos si podemos cambiar el valor a -1 para indicar que ya se acaba
    lsem[index].acquire()
    
    lvalues[index]= -1
        
        

def consumidor(lsem,lvalues,semconsumidor):
    valoresordenados=[]
        #mientras no esté llena la lista de valores ordenados
    while len(valoresordenados)< NPROD*NVUELTAS:
        semconsumidor.acquire()
        print(f'el buffer es ahora{lvalues},vamos a calcular el min')
        minimo=lvalues[0].value
        pmin=0
        proceso=0
        while proceso<len(lvalues):
            if lvalues[proceso].value < minimo and 0<lvalues[proceso].value:
                minimo=lvalues[proceso].value
                pmin=proceso
            proceso+=1
        print(f'el minimo es el{lvalues[pmin].value} generado por el proceso{pmin}')
        valoresordenados+=[minimo]
        lsem[pmin].release()


def main():
    #creamos lista de semaforos, de procesos, y de valores
    lp=[]
    lsem=[]
    lvalues=[]        
    semconsumidor=BoundedSemaphore(1)
    for i in range(NPROD):
        lsem.append(Semaphore(1))
        c=Value('i',0)
        lvalues.append(c)

        
    for i in range(NPROD):    
        p=Process(target=productor, args=(i,lsem,lvalues,semconsumidor))
        lp.append(p)
        
    
    for proceso in lp:
        proceso.start()
    
    q=Process(target=consumidor,args=(lsem,lvalues,semconsumidor))
    q.start()

if __name__=='__main__':
    main()
   
