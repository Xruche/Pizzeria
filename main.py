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
repartidors = 9			## Nombre total de repartidors





def simulacio(nombre_mostres, nombre_mostres_warm_up):

	## Funció encarregada de realitzar una simulació i generar nombre_mostres mostres útils descartant les primeres nombre_mostres_warm_up mostres (règim transitori)

	warm_up = nombre_mostres_warm_up	## Nombre de mostres de warm-up
	mostres = nombre_mostres 			## Nombre de mostres a prendre en règim estacionari

	mostra = 0 							## Mostra actual

	## Les mostres són les dades del temps de processament obtingudes.
	## Es considera que el sistema es troba en estat estacionari quan han passat warm_up mostres (el nombre de mostres corresponent al temps de warm-up).

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
	global Tme
	global t
	global treballadors

	## Bucle de simulació:
	## La simulació s'executa fins que es sobrepassa limit_temps

	pizzes_en_processament = True

	while (mostra < (mostres + warm_up)):			## Condició de finalització, quan s'assoleixi el nombre de mostres adequat

		## Emmagatzemem els esdeveniments a realitzar en el següent instant de temps

		esdev_buffer = llista.esdeveniments_següents()

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

					mostra = mostra + 1					## Contem una mostra més

					if (mostra>warm_up):											## Només si es troba en estacionari.
						Tme.append((t-Pizzes_comanda[0][1])+durada_repartiment/2)	## Guarden la mostra com a dada del temps de processament.
					
					Pizzes_comanda.pop(0)
					llista.afegeix (t + durada_repartiment, "FR")
					rll = rll - 1

		## Esdeveniment de Final de Repartiment

			elif element == "FR":
				if len(Pizzes_comanda) != 0:
					if per > Pizzes_comanda[0][0]:
						per = per - Pizzes_comanda[0][0]
						durada_repartiment =utils.Truncar_normal(10,40,25,10) 

						mostra = mostra + 1					## Contem una mostra més

						if (mostra>warm_up):											## Només si es troba en estacionari.
							Tme.append((t-Pizzes_comanda[0][1])+durada_repartiment/2)	## Guarden la mostra com a dada del temps de processament.
						
						llista.afegeix (t + durada_repartiment, "FR")
						Pizzes_comanda.pop(0)
					else:
						rll = rll + 1
				else:
					rll = rll + 1	

		## S'emmagatzema la quantitat de treballadors lliures en cada instant de simulació en tuples (temps, cuiners lliures, repartidors lliures)

		if (mostra > warm_up): 					## Si la simulació es troba en règim estacionari
			treballadors.append((t,cll,rll))	## Es guarda nombre de treballadors treballant

		## Un cop tenim computades totes les variables d'estat i els nous esdeveniments, obtenim el temps del esdeveniment més proper
		
		t = llista.next_time() 		## Obtenim el temps del següent esdeveniment.


def inicialitzar_variables ():
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
	global Tme
	global t
	global treballadors

							# Inicialitació dels valors de les variables d'estat

	cll = cuiners			## Nombre de cuiners lliures
	pep = 0					## Nombre de pizzes esperant preparació
	pf = 15					## Nombre de places lliures al forn
	pef = 0					## Nombre de pizzes esperant entrar al forn
	rll = repartidors		## Nombre de repartidors lliures
	per = 0 				## Nombre de pizzes esperant repartirment

	Pizzes_comanda = []		##Llista on s'emmagatzema el nombre de pizzes de la comanda i el temps de generació de comanda

		## Variables de control:

	t = 0										## Instant actual de la simulació
	limit_temps = 50*60							## Valor de temps per sobre el qual la simulació no genera noves comandes (minuts)
	llista = classes.llista_esdeveniments() 	## Objecte encarregat de gestionar els esdeveniments

		## Comptadors estadístics:


	ncomandes = 0			## Nombre de comandes realitzades

	Tme = [] 				## Llista on s'emmagatzemen els valors de temps de processament per a cada comanda

	treballadors = []		## LLista on s'emmagatzemen per a cada instant de temps de la simulació (temps, nombre de cuiners lliures, nombre de repartidors lliures) per calcular el temps treballat total


		## Per iniciar la simulació s'introdueix una comanda a l'instant t = 0 que desencadena els esdeveniments següents

	llista.afegeix(0,"AC")


def escriure_a_fitxer (vector_dades):

	## Funció generadora de fitxer resultats.csv amb els temps de processament per a cada comanda per l'anàlisi en MiniTab

	with open('resultats.csv', 'w') as f:
		data = "Nombre de comanda;Temps de processament\n"
		f.write (data)
		for i in range(0,len(Tme)):
			data = str(i)+";"+str(Tme[i])+"\n"
			f.write(data.replace('.',','))


def resultats(vector_dades):

	## Impressió dels resultats per pantalla, dona el temps mitjà de processament (en transitori i permanent conjuntament), el temps d'aturada i la ocupació dels treballadors

	print("Mitjana de temps de processament : "+str(sum(Tme)/len(Tme))+"min")
	print("")
	print("temps d'aturada : "+str(t/60))
	hores_treballades_cuiners = 0;
	hores_treballades_repartidors = 0;
	for i in range (0,len(treballadors)-1):
		hores_treballades_cuiners = hores_treballades_cuiners + (cuiners-treballadors[i][1])*(treballadors[i+1][0]-treballadors[i][0])
		hores_treballades_repartidors = hores_treballades_repartidors + (repartidors-treballadors[i][2])*(treballadors[i+1][0]-treballadors[i][0])

	print("Proporció de temps en treball per als cuiners : "+str(100*hores_treballades_cuiners/(cuiners*(t-treballadors[0][0])))+"%")
	print("Proporció de temps en treball per als repartidors : "+str(100*hores_treballades_repartidors/(repartidors*(t-treballadors[0][0])))+"%")
	escriure_a_fitxer()
	


def simular(nombre_simulacions, nombre_mostres_warm_up, nombre_mostres):
	## Funció que permet realitzar múltiples simulacions amb un determinat nombre de mostres i descartant un cer nombre de mostres de warm_up
	
	dades = [] 		## S'inicialitza el vector on guadarem totes les dades de cada simulació com a una tupla per a cada simulació on la primera dada es el vector de Tme i el segon el vector treballadors.

	for i in range (0,nombre_simulacions):
		inicialitzar_variables()
		simulacio(nombre_mostres, nombre_mostres_warm_up)
		dades.append((Tme, treballadors))

	return dades