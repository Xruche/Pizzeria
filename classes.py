class llista_esdeveniments:
	##Llista on s'emmagatzemen els esdeveniments
	esdeveniments = []

	def __init__ (self):
		self.esdeveniments = []

	def afegeix (self, temps_esdeveniment, tipus_esdeveniment):
		self.esdeveniments.append((temps_esdeveniment, tipus_esdeveniment))

	def esdeveniments_següents(self):
		self.esdeveniments.sort()			## Ordenem la llista per temps d'execució d'esdeveniments creixent
		t = self.esdeveniments[0][0]		## Obtenim el següent instant de temps	
		
		esdeveniments_següents = []
		provisional = []

		for element in self.esdeveniments:	## Obtenim la llista d'esdevenimnets que ocorreran en el següent instant de temps
			if element[0] == t:
				esdeveniments_següents.append(element[1])
			else:
				provisional.append(element)
		self.esdeveniments = provisional

		## Part de codi per ordenar els esdeveniments en cas de tenir més d'un

		## Llista amb l'ordre dels esdeveniments
		ordre_esdev = ["AC", "FP", "SF", "FR"]  
		ordenats = []

		## Etapa de ordernació dels esdeveniments
		for element in ordre_esdev:
			for esdev in esdeveniments_següents:
				if esdev == element:
					ordenats.append(esdev)

		return ordenats
		
	def next_time(self):
		self.esdeveniments.sort()
		return self.esdeveniments[0][0]

	def buida (self):
		return len(self.esdeveniments) == 0


