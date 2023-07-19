from selenium import webdriver #biblioteca de automação web
import pandas as pd #biblioteca para trabalhar bancos de dados
from removerdorcaracteres import removerAcentosECaracteresEspeciais as removedor #eu coloquei a função em docstring no corpo final do corpo do programa, mas também está num repositório separado
navegador = webdriver.Chrome() #para entender o passo a passo com profundidade, recomendo a leitura da documentação
tabela = pd.read_excel('commodities.xlsx') #tabela inicial das commodities a serem avaliadas

for linha in tabela.index:
    produto = tabela.loc[linha, 'Produto']
    produto = removedor(produto) #precisei realizer um tratamento de caracteres especiais por conta dos acentos nas palavras que estavam retornando erro.
    link = f'https://www.melhorcambio.com/{produto}-hoje' #site real e funcional, mas apenas para do programa
    navegador.get(link)
    cotacao = navegador.find_element('xpath', '//*[@id="comercial"]').get_attribute('value')
    cotacao = cotacao.replace('.', '').replace(',', '.')
    cotacao = float(cotacao)
    tabela.loc[linha, 'Preço Atual'] = cotacao

navegador.quit()

tabela['Comprar'] = tabela['Preço Atual'] < tabela['Preço Ideal'] #o preço ideal foi estabelecido 'humanamente' baseado em análise técnica do mercado financeiro


tabela.to_excel('commodities_atualizado.xlsx', index=False)

print(tabela) #para verificar os resultados no terminal, mas a planilha excel já foi criada



'''
import unicodedata
import re

"""
A remoção de acentos foi baseada em uma resposta no Stack Overflow.
http://stackoverflow.com/a/517974/3464573
"""

def removerAcentosECaracteresEspeciais(palavra):



    # Unicode normalize transforma um caracter em seu equivalente em latin.
    nfkd = unicodedata.normalize('NFKD', palavra)
    palavraSemAcento = u"".join([c for c in nfkd if not unicodedata.combining(c)])

    # Usa expressão regular para retornar a palavra apenas com números, letras e espaço
    return re.sub('[^a-zA-Z0-9 \\\]', '', palavraSemAcento)
'''