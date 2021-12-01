from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os, re
import datetime, time
import pandas as pd
from datetime import date, datetime
import clipboard
import shutil
from tika import parser
from gera_txt_STF import Txt_Separados



######  Configurações do Firefox ########


diret = r'PATH PASTA PROVISORIA' # uma pasta provisoria onde o arquivo e baixado
path_default_profile ='PATH MOZILA' #caminho do firefox do computador




firefox_profile = webdriver.FirefoxProfile(path_default_profile) #caminho para a configuração desejada encontrar o firefox com o Webdriver


firefox_profile.set_preference("browser.privatebrowsing.autostart", True)
firefox_profile.set_preference("browser.download.folderList", 2)
firefox_profile.set_preference("browser.download.manager.alertOnEXEOpen", False)
firefox_profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/msword, application/csv, image/jpg, image/p7s, application/ris, text/csv, image/png, application/pdf, text/html, text/plain, application/zip, application/x-zip, application/x-zip-compressed, application/download, application/octet-stream")
firefox_profile.set_preference("browser.download.manager.showWhenStarting", False)
firefox_profile.set_preference("browser.download.manager.focusWhenStarting", False)
firefox_profile.set_preference("browser.download.useDownloadDir", True);
firefox_profile.set_preference("browser.helperApps.alwaysAsk.force", False)
firefox_profile.set_preference("browser.download.manager.closeWhenDone", True)
firefox_profile.set_preference("browser.download.manager.showAlertOnComplete", False)
firefox_profile.set_preference("browser.download.manager.useWindow", False)
firefox_profile.set_preference("services.sync.prefs.sync.browser.download.manager.showWhenStarting", False)
firefox_profile.set_preference("pdfjs.disabled", True)
firefox_profile.set_preference("browser.download.dir", diret)
firefox_profile.set_preference("browser.firefox.marionette", False)
firefox_profile.set_preference("plugin.state.flash", 2)

######## fim das configurações do Firefox ###############


driver = webdriver.Firefox(firefox_profile) # navegador carregado com as configurações
action = webdriver.ActionChains(driver) #habilitação do driver
driver.get("https://jurisprudencia.stf.jus.br/pages/search") #inicia a página
time.sleep(5) #espera carregar
botao_busca = driver.find_element_by_xpath("//*[@id='mat-input-0']") #encontra o campo de busca do termo
termo = input("digite o termo de busca: ")  #termo de busca
botao_busca.send_keys(termo) #coloca o termo no campo
time.sleep(2)
botao_busca.send_keys(Keys.ENTER) # aperta o enter
time.sleep(5) #espera carregar
# driver.find_element_by_xpath("//*[@id='mat-radio-10']/label/div[1]/div[1]").click() #seleciona as decisões monocráticas


### Inicia o procedimento em cada uma das páginas de resultados - descomentar caso queira fazer mais de uma pagina #####

# time.sleep(3)
# driver.find_element_by_xpath("//*[@id='mat-select-17']/div/div[1]/span/span").click()#seleciona o campo na página
# time.sleep(5) #espera carregar 
# driver.find_element_by_xpath("//*[@id='mat-option-609']/span").click() # vai até o link de 100 páginas e clica
# time.sleep(5) #espera carrega



#lista com os nomes das ações sem acórdãos
sem_acordao = []




# parte da extração dos dados

while True:
	a = input("deseja coletar outra pagina? DIGITE s para continuar:") # para permitir o ajuste manual caso dê erro em alguma página
	if a == "s":
		num = int(input("digite a quantidade de links da pagina:"))
		for k in range(num): # 100 pois são os resultados da página
			print("------------------------ link %s ----------------------------"%(k+1)) # mostra em qual link o processo está sendo feito
			driver.find_element_by_xpath("//*[@id='result-index-{}']/a/h4".format(k)).click() # clica no link pra acessar os dados

			time.sleep(6) #espera carregar

			# começa a separar os dados
			acao = driver.find_element_by_xpath("//*[@id='scrollId']/div/div[2]/div/div[1]/div[1]/h4[1]") # número
			cabec = driver.find_element_by_xpath("//*[@id='scrollId']/div/div[2]/div/div[1]/div[1]") #cabeçalho
			partes = driver.find_element_by_xpath("//*[@id='scrollId']/div/div[2]/div/div[3]") 	#partes


			# faz a tentativa etrata os erros pra coletar a decisão e a legislação	
			try:
				decisao = driver.find_element_by_xpath("//*[@id='scrollId']/div/div[2]/div/div[4]")
				text_decisao = str(decisao.text.encode("utf-8").decode("utf-8"))
			except:
				text_decisao = "vazio"
			try:
				legis = driver.find_element_by_xpath("//*[@id='scrollId']/div/div[2]/div/div[6]")
				text_legis = str(legis.text.encode("utf-8").decode("utf-8"))
			except:
				text_legis = "vazio"		
		

			#decodifica os textos da ação, cabeçalho edas partes

			text_acao = str(acao.text.encode("utf-8").decode("utf-8"))
			partic = text_acao.split("\n")
			nome_acao,nada = partic[0].split("/")
			nome_acao = nome_acao.strip()
			text_cabec = str(cabec.text.encode("utf-8").decode("utf-8"))
			text_partes = str(partes.text.encode("utf-8").decode("utf-8"))


			# envia para omódulo que faz a separação e gera o TXT

			Txt_Separados(k,text_cabec,text_partes,text_decisao,text_legis)


			try:
				time.sleep(2)
				driver.find_element_by_xpath("//*[@id='scrollId']/div/div[1]/mat-icon").click() # clica para voltar pra pagina anterior
				WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, "//*[@id='result-index-{}']/a/h4".format(k))))
				driver.find_element_by_xpath("//*[@id='result-index-{}']/a/h4".format(k))
			except:
				x = input("houve um problema, faça manualmente") # se travar por algum problema no site, permite o retorno manualmente
			print(" Dados do link %s produzidos com sucesso"%(k+1)) # avisa se deu tudo certo com os dados desse link

			
			###########  Parte de baixar o documento ##################
			print("***********************************************")
			print("Iniciando o download do link %s "%(k+1))


				# nome da ação
			nome_file, nada = text_acao.split("/") #separa o nome do arquivo
			print("Iniciando tentativa de baixar o arquivo",nome_file) # avisa o usuário
			


			# # tenta clicar pra baixar o documento poque alguns não tem o link
			try:
				driver.find_element_by_xpath("//*[@id='result-index-{}']/div[1]/div/a[3]/mat-icon".format(k)).click() # clica para baixar o acórdão
				time.sleep(10) # espera baixar
				pastas = os.listdir(diret)
				nome_final = str(nome_acao)+".pdf"
				for q in range(len(pastas)):
					nome = os.path.join(diret, pastas[q])
					os.rename(nome, nome_final)
					dir_final = r'C:\Users\Diego\Documents\Pesquisas_Insper\STF_Bianca\acordaos\acordao_pdf'
					shutil.move(nome_final,dir_final)
				print("arquivo do link",k+1,"gerado e movido com sucesso") # informa que terminou
			except:
				sem_acordao.append(nome_file) #inclui na lista dos sem acórdão
				print("Não há link do acórdão",k+1) # avisa que não possui este
			print("---------------------------------------------------------------------")	# indica o encerramento do processo desse link

			##### fim do laço #####


	else:
		print("Fim do procedimento dos dados e download dos acórdãos")			
		break
	#### fim do processo ###	

driver.close()






