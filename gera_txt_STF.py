import os


def Txt_Separados(k,text_cabec,text_partes,text_decisao,text_legis):
	

	# cria o direitorio para cada pasta

	try:
		dir = "txt_separados"   
		os.mkdir(dir)
	except:
		pass


	try:
		dir = "txt_separados/STF_txt_"+str(k)   
		os.mkdir(dir)
	except:
		pass


	
	# arq_acao = open("txt_separados/STF_txt_"+str(k)+"/acao.txt","w")
	# arq_acao.write(text_acao)
	# arq_acao.close()	

	arq_cabec = open("txt_separados/STF_txt_"+str(k)+"/cabec.txt","w")
	arq_cabec.write(text_cabec)
	arq_cabec.close()	

	arq_partes = open("txt_separados/STF_txt_"+str(k)+"/partes.txt","w")
	arq_partes.write(text_partes)
	arq_partes.close()

	arq_decisao = open("txt_separados/STF_txt_"+str(k)+"/decisao.txt","w")
	arq_decisao.write(text_decisao)
	arq_decisao.close()


	arq_legis = open("txt_separados/STF_txt_"+str(k)+"/legis.txt","w")
	arq_legis.write(text_legis)
	arq_legis.close()