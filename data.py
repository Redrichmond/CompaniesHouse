#!/usr/bin/env python

"""Main.py: Metodo para obtener informacion desde CompaniHouses.gov.uk"""

__author__ = "Victor H. Villalobos B."
__copyright__ = "Copyright 2015"

import urllib

import requests


class CompaniesHouse():
    def __init__(self, apikey):
        self.apikey = apikey
        self.countP = 600  # Petition Counter

    def getCountP(self):
        return self.countP

    # Extraccion de metodos desde hcompanies hose.
    def getCompany(self, number):
        url = "https://api.companieshouse.gov.uk/company/" + number
        r = requests.get(url, auth=(self.apikey, ''), verify = 'cacert.pem')
        return r.json()

    def getRegisteredOffice(self, number):
        url = "https://api.companieshouse.gov.uk/company/" + number + '/registered-office-address'
        r = requests.get(url, auth=(self.apikey, ''), verify = 'cacert.pem')
        r = r.json()
        dictlist = []
        zip_code = 'FAIL'
        locality = 'FAIL'
        Add1 = 'FAIL'
        Add2 = 'FAIL'
        Add3 = 'FAIL'
        for key, value in r.items():
            temp = [key, value]
            dictlist.append(temp)
        for n in range(len(dictlist)):

            if dictlist[n][0] == 'postal_code':
                zip_code = (dictlist[n][1])
                del dictlist[n]
                break
        for n in range(len(dictlist)):
            if dictlist[n][0] == 'locality':
                locality = (dictlist[n][1])
                del dictlist[n]
                break
        for n in range(len(dictlist)):
            if dictlist[n][0] == 'address_line_1':
                Add1 = (dictlist[n][1])
                del dictlist[n]
                break
        for n in range(len(dictlist)):
            if dictlist[n][0] == 'address_line_2':
                Add2 = (dictlist[n][1])
                del dictlist[n]
                break
        for n in range(len(dictlist)):
            if dictlist[n][0] == 'region':
                Add3 = (dictlist[n][1])
                del dictlist[n]
                break
        return [Add1, Add2, Add3, locality, zip_code]

    def getRegisteredOffice2(self, number):
        url = "https://api.companieshouse.gov.uk/company/" + number + '/registered-office-address'
        r = requests.get(url, auth=(self.apikey, ''), verify = 'cacert.pem')
        return r.json()

    def getOfficers(self, number):
        url = "https://api.companieshouse.gov.uk/company/" + number + "/officers"
        r = requests.get(url, auth=(self.apikey, ''), verify = 'cacert.pem')
        j = r.json()
        self.countP = int(r.headers['x-ratelimit-remain'])
        print(r.headers)
        return j['items']

    def getInsolvency(self, number):
        url = "https://api.companieshouse.gov.uk/company/" + number + "/insolvency"
        r = requests.get(url, auth=(self.apikey, ''), verify = 'cacert.pem')
        return r.json()

    def getListFillingHistory(self, number):
        url = "https://api.companieshouse.gov.uk/company/" + number + "/filing-history"
        r = requests.get(url, auth=(self.apikey, ''), verify = 'cacert.pem')
        return r.json()

    def existForm1(self, record):
        # recibe un json desde getListFillingHistory para revisar si existe un documento 4.19
        documents = record['items']
        flag = False
        for doc in documents:
            if 'description_values' in doc.keys():
                if 'form_attached' in doc['description_values'].keys():
                    if doc['description_values']['form_attached'] == '4.19':
                        if 'document_metadata' in doc['links'].keys():
                            flag = True
        return flag

    def existForm2(self, record):
        # recibe un json desde getListFillingHistory para revisar si existe un documento 4.7
        documents = record['items']
        flag = False
        for doc in documents:
            if 'description_values' in doc.keys():
                if 'form_attached' in doc['description_values'].keys():
                    if doc['description_values']['form_attached'] == '4.7':
                        if 'document_metadata' in doc['links'].keys():
                            flag = True
        return flag

    def getUrlForm1(self, record):
        # recibe un json desde getListFillingHistory para revisar si existe un documento 4.19
        documents = record['items']
        for doc in documents:
            if 'description_values' in doc.keys():
                if 'form_attached' in doc['description_values'].keys():
                    if doc['description_values']['form_attached'] == '4.19':
                        return doc['links']['document_metadata']


    def getUrlForm2(self, record):
        # recibe un json desde getListFillingHistory para revisar si existe un documento 4.19
        documents = record['items']
        for doc in documents:
            if 'description_values' in doc.keys():
                if 'form_attached' in doc['description_values'].keys():
                    if doc['description_values']['form_attached'] == '4.7':
                        return doc['links']['document_metadata']


    def getDocumentUrl(self, link):
        url = link + "/content"
        headers = {'Accept': 'application/pdf', 'Authorization': 'Basic ' + self.apikey}
        r = requests.get(url, headers, auth=(self.apikey, ''), verify = 'cacert.pem')
        return r.url

    def downloadDocument(self, url, fileName):
        url = self.getDocumentUrl(url)
        urllib.request.urlretrieve(url, fileName + '.pdf')


    def dict2list(self, dict):
        #Convierte en lista un diccionario
        dictlist = []
        for key, value in dict.items():
            temp = [key, value]
            dictlist.append(temp)
        for n in range(len(dictlist)):
            if dictlist[n][0] == 'postal_code':
                zip_code = (dictlist[n][1])
                del dictlist[n]
                break
        return [dictlist, zip_code]

if __name__ == '__main__':
    obj = CompaniesHouse('fI9ltuY_TeuXVlvgbVl3BGQtRSb9XGucMC4UbPqM')
    registered = obj.getRegisteredOffice('05876280')
    print(registered)

