import os

import pandas as pd

class Preprocessing:
    
    def __init__(self, path = '../data/Topicos'):
        self.path = path
        self.corpora_path = os.listdir(self.path)
        self.corpora_path = [d for d in self.corpora_path]
    
    def path_news(self, path = '../data/Topicos'):
        xls_news_path = []
        for supervisor in self.corpora_path:
            noticias = os.listdir(path + '/' + supervisor)
            for noticia in noticias:
                xls_news_path.append(path + '/' + supervisor + '/' + noticia)
        return xls_news_path
    
    def extrair_nome(self, path):
        nome = path.replace('../data/Topicos/','')
        nome = nome.replace('.xlsx', '')
        return nome
    
    #retorna um dicionario de dataframe e uma lista com os nomes das noticias repetidas
    def dataFrame_news(self, noticias_xls):
        #dicionario para armazenar o path de cada noticia
        noticias = {}
        #dicionario para armazenar um DF de cada noticia
        notic_indiv = {}
        #noticias repetidas
        notic_rep = []
        for noticia in noticias_xls:
            #cria uma key como a chave de cada noticia
            noticias[noticia] = []
            #le o arquivo do excel
            xlsx = pd.ExcelFile(noticia)
            #para cada key é atribuido um DF referente a planilha com a noticia
            #sheet_name = None, ler todas as folhas de uma planilha
            noticias[noticia] = pd.read_excel(xlsx, sheet_name=None)
            for notic in noticias[noticia].keys():
                #noticias repetidas apenas serão inseridas novas colunas
                if notic in notic_indiv:
                    if notic not in notic_rep: notic_rep.append(notic)
                    #aqui se cria um DataFrame
                    plan_aux = pd.read_excel(xlsx, sheet_name=notic)
                    superv = self.extrair_nome(noticia)
                    #DataFrameName.insert(loc, column, value, allow_duplicates = False)
                    notic_indiv[notic].insert(len(plan_aux.keys()), 'Tópico (Rotule apenas Inicio)', plan_aux['Tópico (Rotule apenas Inicio)'], True)
                    notic_indiv[notic].insert(len(plan_aux.keys()), 'Segmentação', plan_aux['Segmentação'], True)
                else:
                    #aqui se cria uma Serie
                    notic_indiv[notic] = pd.read_excel(xlsx, sheet_name=notic)
                #normalizar a palavra 'inicio' para ficarem todas sem acentos
                notic_indiv[notic] = notic_indiv[notic].replace('Início','Inicio')
                notic_indiv[notic] = notic_indiv[notic].fillna('empty')
        return notic_indiv, notic_rep
    
    def news_match(self, notic_indiv, notic_rep):
        cont = 0;
        matchs = []
        for notic in notic_rep:
            for row in notic_indiv[notic]['Segmentação'].iterrows():
                lista = []
                lista = row[1].tolist()
                for x in range(1, 7):
                    for y in range(x+1,7):
                        if lista[x] != 'nan' and lista[x] == lista[y]:
                            cont+=1
            size = notic_indiv[notic]['Segmentação'].size
            matchs.append((notic, (cont/size)*100))
            cont = 0
        return matchs
    