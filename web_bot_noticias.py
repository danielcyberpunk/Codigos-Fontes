import requests
import csv
from bs4 import BeautifulSoup

class WebCrawler():
	def __init__(self):
		csv_file = open('noticias.csv', 'w', encoding='utf-8')
		csv_file.write('titulo;noticia;url;data\n')
		csv_file.close()

		url_inicial = 'https://www.noticiasagricolas.com.br/noticias/'

		requisicao = requests.get(url_inicial)

		self.parse_grid(requisicao)

	def parse_grid(self, requisicao):
		while True:
			obj_bs4 = BeautifulSoup(requisicao.content, 'html.parser')
			for urls in obj_bs4.select('li.horizontal.com-hora a'):
				url_noticia = 'https://www.noticiasagricolas.com.br' + str(urls['href']).strip()
				dict_noticia = self.parse_noticias_individuais(url_noticia)

				self.set_in_file(dict_noticia)

			find_next_page = obj_bs4.select_one('li.next a')
			if find_next_page:
				url_next_page = 'https://www.noticiasagricolas.com.br' + str(find_next_page['href']).strip()
				requisicao = requests.get(url_next_page)
				print ('NEXT PAGE')
			else:
				break

	def parse_noticias_individuais(self, url_noticia):
		dict_noticia = {
			'titulo' : None,
			'noticia' : None,
			'url' : url_noticia,
			'data' : None
		}

		requisicao_noticia = requests.get(url_noticia)
		obj_bs4_noticia = BeautifulSoup(requisicao_noticia.content, 'html.parser')

		find_titulo = obj_bs4_noticia.select_one('h1.page-title')
		if find_titulo:
			dict_noticia['titulo'] = str(find_titulo.text).replace(';',',').replace('\n','').replace('\t','').replace('\r','').strip()

		texto_noticia = ''
		for texto_bruto in obj_bs4_noticia.select('div.materia p'):
			texto_parcial = str(texto_bruto.text).strip()

			texto_noticia = str(texto_noticia) + '.' + str(texto_parcial)

		if str(texto_noticia) != '':
			dict_noticia['noticia'] = str(texto_noticia).replace(';',',').replace('\n','').replace('\t','').replace('\r','').strip()

		find_data = obj_bs4_noticia.select_one('div.datas')
		if find_data:
			data_tratamento = str(find_data.text).replace('Publicado em','').strip().split('  ')
			dict_noticia['data'] = str(data_tratamento[0]).strip()

		return dict_noticia

	def set_in_file(self, noticia_dict):
		csv_file = open('noticias.csv', 'a+', encoding='utf-8')

		csv_file.write('{};{};{};{}\n'.format(
			str(noticia_dict['titulo']).replace(';',',').replace('\n','').replace('\t','').replace('\r',''),
			str(noticia_dict['noticia']).replace(';',',').replace('\n','').replace('\t','').replace('\r',''),
			str(noticia_dict['url']).replace(';',',').replace('\n','').replace('\t','').replace('\r',''),
			str(noticia_dict['data']).replace(';',',').replace('\n','').replace('\t','').replace('\r',''),
		))

		csv_file.close()

		print ('COLETADO',noticia_dict['url'])

WebCrawler()