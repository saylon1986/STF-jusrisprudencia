import os, re
import pandas as pd
import datetime, time




def Separador_dados(nome_dir):




#	print(len(path_files))

	df_stf_final = pd.DataFrame()

	while True:
		a = input("deseja rodar uma nova leva de dados?")
		if a == "s":
			num = str(input("digite o numero da pagina: "))
			path = nome_dir+num
			path_files = os.listdir(path)
			# print("temos",len(path_files))
			for x in range(len(path_files)):
				numer_acao = []
				tipo_de_acao = []
				relatores = []
				dat_julgamento = []
				decisoes = []
				legislacoes =[]
				partes_separ = []
				funcao = []
				path_arq = os.path.join(path,path_files[x])
				
				# print(path_arq)
				# print("---------------------------")
				arq_list_1 = os.listdir(path_arq)

		#		print(arq_list_1)


				arq_0_0 = os.path.join(path_arq,arq_list_1[0])
				

				arq_0 = open(arq_0_0, "r")
				line_0 = arq_0.readlines()

		#		print(line_0)


				############ arquivo cabecalho  #################

				# nome acao
				num_acao = line_0[0]
			#	print(num_acao)
				numer_acao.append(num_acao)
				del(line_0[0]) #deleta esse elemento da lista



				# tipo de acao
				tipo_acao = line_0[0]
				tipo_de_acao.append(tipo_acao)
				del(line_0[0]) #deleta esse 

				# print(path_arq)
				# print(tipo_acao)
				# print("---------------------------")

				# relator
				for n in range(len(line_0)):
					if re.search(r'relator', line_0[n], re.IGNORECASE) != None:
						rest, relator = line_0[n].split(":")
				#			print(relator)
						relatores.append(relator)
						del(line_0[n])
						break
					else:
						relator = "vazio"
						relatores.append(relator)
				
				# julgamento		
				for n in range(len(line_0)):
					if re.search(r'julgamento', line_0[n], re.IGNORECASE) != None:
						rest, julgamento = line_0[n].split(":")
				#			print(relator)
						dat_julgamento.append(julgamento)
						del(line_0[n])
						break
					else:
						julgamento = "vazio"
						dat_julgamento.append(julgamento)

				################  arquivo decisao #######################		

				arq_list_0_1 = os.path.join(path_arq,arq_list_1[1])


				arq_1 = open(arq_list_0_1, "r")

				line_1 = arq_1.readlines()

				decisao = " ".join(line_1)
				decisao = re.sub(r"\n"," ",decisao)
				decisoes.append(decisao)

				############# arquivo legis ##########################

				arq_list_2 = os.path.join(path_arq,arq_list_1[2])

				arq_2 = open(arq_list_2, "r")

				line_2 = arq_2.readlines()

				try:	
					legis = " ".join(line_2)
				#	legis = re.sub(r"\s+",",",legis)
					legislacoes.append(legis)
				except:
					legislacoes.append(line_2)
					

				############# arquivo partes ##########################	

				arq_list_3 = os.path.join(path_arq,arq_list_1[3])

				arq_3 = open(arq_list_3, "r")

				line_3 = arq_3.readlines()

				partes_separ = []
				funcao = []
				for z in range(len(line_3)):
					parti = line_3 [z]
					if len(parti) > 8:
						try:	
					 		part = parti.split(":")
				#	 		print(part)
					 		funcao.append(part[0])
					 		partes_separ.append(part[1])
						except:
				 #		pass
				 			erro = ["erro"]
				 			funcao.append(erro[0])
				 			partes_separ.append(erro[0])


			# for k in range(len(decisoes)):
			# 	print(decisoes[k])
			# 	print("________________________________________________________________________________________")


			#gera os objetos do DataFrame

				x = pd.Series(numer_acao)
				y = pd.Series(tipo_de_acao)
				w = pd.Series(relatores)
				t = pd.Series(dat_julgamento)
				q = pd.Series(decisoes)
				r = pd.Series(legislacoes)
				#	u = pd.Series([legis])

				df_stf = pd.DataFrame()

				# 	# concatena os objetos
				df_stf = pd.concat([x,y,w,t,q,r], axis=1,keys=["Número do Processo","Tipo de acao","Relator","Julgamento","Decisão","legislacao"])
		 	
				for m in range(len(partes_separ)):
					df_stf["Função_processual_"+str(m+1)] = funcao[m]
					df_stf["Parte_"+str(m+1)] = partes_separ[m]

				# print(df_stf_final)	
				df_stf_final = df_stf_final.append(df_stf,ignore_index=True, sort=False)	

		else:
			break		

	# print(df_stf_final)			
	return df_stf_final


	################################################## fim da funcao ##################################################################



nome_dir = r'C:\Users\saylo\Desktop\STF-jusrisprudencia-main\txt_separados\pagina_'

df_stf_final = pd.DataFrame()


# for f in nome_dir:
df_stf_final = Separador_dados(nome_dir)
#	print(dado_stf)
	# df_stf_final = df_stf_final.append(dado_stf,ignore_index=True, sort=False)
#	time.sleep(6)


df_stf_final.to_excel("STF_final.xlsx",index=False)
