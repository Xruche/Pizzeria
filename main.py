## Treball de simulació
## Optimització i simulació, GETI, ETSEIB, Barcelona, QPrimavera 2018-2019
##
## Simulació Enunciat 9 : Pizzeria
## Autors:
## 			Francesc Xavier Ruché ALvarez
##			Anna Cinta Bel Ferreres
## 			Clara Sellés Hontoria
##			Alejandro Sànchez Gil

import utils
import math
import classes
import os



	# Inicialitació dels valors de les variables

cuiners = 5				## Nombre total de cuiners
repartidors = 5			## Nombre total de repartidors


cll = cuiners			## Nombre de cuiners lliures
pep = 0					## Nombre de pizzes esperant preparació
pf = 15					## Nombre de places lliures al forn
pef = 0					## Nombre de pizzes esperant entrar al forn
rll = repartidors		## Nombre de repartidors lliures
per = 0 				## Nombre de pizzes esperant repartirment

Pizzes_comanda = []

	## Variables de control:

t = 0										## Instant actual de la simulació
limit_temps = 12*60							## Valor de temps per sobre el qual la simulació no genera noves comandes (minuts)
llista = classes.llista_esdeveniments() 	## Objecte encarregat de gestionar els esdeveniments

	## Comptadors estadístics:


ncomandes = 0			## Nombre de comandes realitzades

temps_espera = [] 		## Llista on s'emmagatzemen els valors de temps de processament per a cada comanda

treballadors = []		## LLista on s'emmagatzemen per a cada instant de temps de la simulació (temps, nombre de cuiners lliures, nombre de repartidors lliures) per calcular el temps treballat total

temps_warm_up = 0

	## Per iniciar la simulació s'introdueix una comanda a l'instant t = 0 que desencadena els esdeveniments següents

llista.afegeix(0,"AC")


def simular():	

	global nc
	global nf
	global nr 
	global cll
	global pep
	global pf
	global pef
	global rll
	global per
	global Pizzes_comanda
	global t
	global limit_temps
	global llista
	global Time
	global tot
	global ncomandes
	global temps_espera_accumulat
	global t
	global treballadors

	## Bucle de simulació:
	## La simulació s'executa fins que es sobrepassa limit_temps

	pizzes_en_processament = True

	while (t < limit_temps):

		esdev_buffer = llista.esdeveniments_següents()  ## Emmagatzemem els esdeveniments a realitzar en el següent instant de temps

		## Processem els esdeveniments al buffer

		for element in esdev_buffer:

		## Esdeveniment de Arribada de Comanda

			if   element == "AC":
				ncomandes = ncomandes + 1
				temps_nova_comanda = t+utils.Exponencial(1/3) 
				llista.afegeix(temps_nova_comanda, "AC")
				npizzes = utils.nombre_pizzes()
				pep = pep + npizzes
				Pizzes_comanda.append((npizzes, t))

				if cll > 0 and pep > cll:
					for cuiner in range (0,cll):
						llista.afegeix(t+utils.Uniforme(3,7), "FP")
					pep = pep - cll
					cll = 0
				elif cll > 0 and pep <= cll:
					for element in range (0, pep):
						llista.afegeix(t+utils.Uniforme(3,7), "FP")
					cll = cll-pep
					pep = 0

		## Esdeveniment de Fi de Preparació

			elif element == "FP":
				if pep > 0:
					llista.afegeix(t+utils.Uniforme(3,7), "FP")
					pep = pep - 1
				else :
					cll = cll + 1

				if pf > 0:
					llista.afegeix(t+5 , "SF")
					pf = pf - 1
				else : 
					pef = pef + 1

		## Esdeveniment de Sortida del Forn

			elif element == "SF":
				if pef > 0:
					llista.afegeix(t+5 , "SF")
					pef = pef - 1
				else:
					pf = pf + 1
				per = per + 1

				if rll > 0 and per >= Pizzes_comanda[0][0]:
					per = per - Pizzes_comanda[0][0]
					durada_repartiment =utils.Truncar_normal(10,40,25,10)
					temps_espera.append((t-Pizzes_comanda[0][1])+durada_repartiment/2)
					Pizzes_comanda.pop(0)
					llista.afegeix (t + durada_repartiment, "FR")
					rll = rll - 1

		## Esdeveniment de Final de Repartiment

			elif element == "FR":
				if len(Pizzes_comanda) != 0:
					if per > Pizzes_comanda[0][0]:
						per = per - Pizzes_comanda[0][0]
						durada_repartiment =utils.Truncar_normal(10,40,25,10) 
						temps_espera.append((t-Pizzes_comanda[0][1])+durada_repartiment/2)
						llista.afegeix (t + durada_repartiment, "FR")
						Pizzes_comanda.pop(0)
					else:
						rll = rll + 1
				else:
					rll = rll + 1	

		treballadors.append((t,cll,rll))
		## Un cop tenim computades totes les variables d'estat i els nous esdeveniments, obtenim el temps del esdeveniment més proper
		t = llista.next_time()

def calcularmu (llista):
	acumulat = 0
	for element in llista:
		acumulat = acumulat + element
	return acumulat/len(llista)


def resultats():
	global ncomandes
	print("Mitjana de temps de processament : "+str(sum(temps_espera)/len(temps_espera))+"h")
	print("")
	print("temps d'aturada : "+str(t/60))
	hores_treballades_cuiners = 0;
	hores_treballades_repartidors = 0;
	for i in range (0,len(treballadors)-1):
		hores_treballades_cuiners = hores_treballades_cuiners + (cuiners-treballadors[i][1])*(treballadors[i+1][0]-treballadors[i][0])
		hores_treballades_repartidors = hores_treballades_repartidors + (repartidors-treballadors[i][2])*(treballadors[i+1][0]-treballadors[i][0])
	print("Proporció de temps en treball per als cuiners : "+str(hores_treballades_cuiners/(cuiners*t))+"%")
	print("Proporció de temps en treball per als repartidors : "+str(hores_treballades_repartidors/(repartidors*t))+"%")
	

simular()
resultats()
			