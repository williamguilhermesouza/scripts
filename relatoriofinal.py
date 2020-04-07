#!/usr/bin/env python
# coding: UTF-8
#
## @package scripts
#
#   Script that work with two python sets from csv file,
#   s1 file must be a csv file with the names on the 4th
#   column, and spp file must be an csv file with the names
#   on the 3th column
#
#   @author William Souza
#   @since 01/04/2020
#
#
from sys import argv, exit 
from unidecode import unidecode
import getopt
import csv

## Function that prints help list with args
def help():
    print(
        '''Uso: python3 <options> <spp> <s1>
        
        Programa que faz a comparação entre os nomes na 3a coluna
        de um arquivo csv contendo a relação nominal da spp e os 
        nomes na 4a coluna de um arquivo csv contendo a relação de 
        efetivo fornecida pela s1
        
        Opções:
            -o      Imprime para arquivo txt com nome fornecido
            -h      Imprime esta ajuda na tela
        ''')
    
## function that saves the information of the sets
# to a file with the given filename
# @param __arq the filename to save the information
# @param __in_s1_not_spp set to write to file
# @param __in_spp_not_s1 second set to save
def salvar(__arq, __in_s1_not_spp, __in_spp_not_s1):
    try:
        with open(__arq, 'w') as outfile:
            outfile.write('\n')
            outfile.write('Estão na relação Nominal (SPP) e não constam no efetivo (S1):\n')
            outfile.write('-' * 80 + '\n')
            for nome in sorted(__in_spp_not_s1):
                outfile.write(nome + '\n')
            outfile.write('\n')
            outfile.write('Estão na relação do efetivo (S1) e não constam na relação nominal (SPP):\n')
            outfile.write('-' * 90 + '\n')
            for nome in sorted(__in_s1_not_spp):
                outfile.write(nome + '\n')
                
        print(f'arquivo {__arq} salvo com sucesso')
        
    except IOError:
        print('erro na escrita do arquivo')
        
        
## function that prints the information of the sets
# @param __in_s1_not_spp set to print
# @param __in_spp_not_s1 second set to print       
def imprimir(__in_s1_not_spp, __in_spp_not_s1):
    print()
    print('Estão na relação Nominal (SPP) e não constam no efetivo (S1):')
    print('-' * 80)
    for nome in sorted(__in_spp_not_s1):
        print(nome)
    print()
    print('Estão na relação do efetivo (S1) e não constam na relação nominal (SPP):')
    print('-' * 90)
    for nome in sorted(__in_s1_not_spp):
        print(nome)
            
## application main function that open, 
# read the files and parse the args
# @param argv arguments from the program call
def main(argv):
    try:
        opts, args = getopt.getopt(argv[1:],'o:h')
        
    except getopt.GetoptError:
        help()
        return 1

    if len(args) != 2:
        help()
        return 1
        
    for opt, arg in opts:
        if '-h' in opt or '-h' in arg or '-h' in args:
            help()
            return 0
        
        
    spp = args[0]
    s1 = args[1]
    sppnames = set()
    s1names = set()

    try:
        with open(spp, 'r') as sppfile:
            reader = csv.reader(sppfile)
            for value in reader:
                sppnames.add(unidecode(value[2].upper()))
                
    except IOError:
        print('erro de leitura no arquivo spp')
        return 3
        
    try:
        with open(s1, 'r') as s1file:
            reader = csv.reader(s1file)
            for value in reader:
                s1names.add(unidecode(value[3].upper()))
                
    except IOError:
        print('erro de leitura no arquivo s1')
        return 3
        
    in_spp_not_s1 = sppnames - s1names
    in_s1_not_spp = s1names - sppnames
    
    for opt, arg in opts:
        if opt == '-o':
            salvar(arg, in_s1_not_spp, in_spp_not_s1)
            return 0
            
    imprimir(in_s1_not_spp, in_spp_not_s1)
    return 0

if __name__ == '__main__':
    retorno = main(argv)
    if retorno != 0:
        print(f'erro {retorno}')
