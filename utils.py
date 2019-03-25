import math
import random

def Uniforme (a, b):
	## Genera un nombre aleatori seguint distribució uniforme entre els valors donats a i b
	
	return (a+(b-a)*random.random())

def Normal (mu, sigma):
	## Genera un nombre aleatori seguint distribució normal amb mu mitjana i sigma desviació estandard
	## seguint la formula Box-Müller

	z = math.sqrt(-2*math.log(random.random()))*math.cos(2*math.pi*random.random())
	return (mu + z*sigma)

def Exponencial (lamb):
	## Genera un nombre aleatori seguint distribució exponencial amb el parametre lambda proporcionat

	return (-math.log(random.random())/lamb)

def Truncar_normal (a,b, mu, sigma):
	## Genera un nombre aleatori en Normal truncada amb els parametres especificats

	value = Normal(mu, sigma)
	
	while (a > value or b < value):
		value = Normal(mu, sigma)
	
	return value

def nombre_pizzes ():
	## Generador del nombre de pizzes per cada comanda mitjançant la llei especificada

	prob = [(0.05,1),(0.4,2),(0.25,3),(0.20,4), (0.10,5)]
	x = random.random()
	acumulada = 0
	for element in prob:
		acumulada = acumulada + element[0]
		if acumulada > x:
			return element[1]

def test_distribucions (n,a,b,mu,sigma,lamb):
	## Genera un fitxer test_distribucions.csv amb el qual es poden comprovar els generadors de nombres aleatoris amb MiniTab

	with open('test_distribucions.csv', 'w') as f:
		data = "Uniforme ("+str(a)+","+str(b)+");Normal("+str(mu)+","+str(sigma)+");Exponencial ("+str(lamb)+");Discreta ;Normal truncada ("+str(a)+","+str(b)+")\n"
		f.write (data.replace('.',','))
		for i in range(0,n):
			data = str(Uniforme(a,b))+";"+str(Normal(mu,sigma))+";"+str(Exponencial(lamb))+";"+str(nombre_pizzes())+";"+str(Truncar_normal(10,40,25,10))+";\n"
			f.write(data.replace('.',','))
	return

def calcularmu (llista):
	## Funció per calcular mitjanes de llistes

	acumulat = 0
	for element in llista:
		acumulat = acumulat + element
	return acumulat/len(llista)