__author__ = 'Programador'

import csv
import os
import time
import datetime
import logging
from PyQt5.QtCore import QThread, pyqtSignal
from data import CompaniesHouse


class Importer(QThread):
    maxSignal = pyqtSignal(int)
    updateSignal = pyqtSignal(int)
    closeSignal = pyqtSignal(bool)

    def __init__(self, parent=None, apikey='', fileImport='', fileOutput=''):
        super(Importer, self).__init__(parent)
        self.apikey = apikey
        self.fileImport = fileImport
        self.fileOutput = fileOutput
        self.pause = False
        logging.basicConfig(filename='import.log',level=logging.DEBUG)

    def setPause(self, pause):
        self.pause = pause


    def run(self, ):
        listaBase = []
        self.lista = []
        self.ch = CompaniesHouse(self.apikey)
        self.getLinesCount()
        with open(self.fileImport, newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
            count = 1  # counter for progress bar signal
            for row in spamreader:
                while True:
                    if not self.pause:
                        try:
                            if self.siHayChance():
                                print(row[0])
                                if len(row[0]) == 7:
                                    CompanyNumber = '0' + row[0]
                                elif len(row[0]) > 8:
                                    print('Error: Very long company number')
                                    self.updateSignal.emit(count)
                                    count = count + 1
                                    break
                                elif len(row[0]) == 8:
                                    CompanyNumber = row[0]

                                company = self.ch.getCompany(CompanyNumber)
                                if 'errors' in company.keys():
                                    print('Error: ' + company['errors'][0]['error'])
                                    break
                                else:
                                    insolvency = self.ch.getInsolvency(CompanyNumber)
                                    fillingHistory = self.ch.getListFillingHistory(CompanyNumber)
                                    #PDFs Download.
                                    if self.ch.existForm1(fillingHistory):
                                            self.ch.downloadDocument(self.ch.getUrlForm1(fillingHistory), os.path.dirname(self.fileOutput)
                                                                + '/pdfs/' + CompanyNumber + '-419')
                                    if self.ch.existForm2(fillingHistory):
                                        self.ch.downloadDocument(self.ch.getUrlForm2(fillingHistory), os.path.dirname(self.fileOutput)
                                                                + '/pdfs/' + CompanyNumber + '-47')
                                    registeredOffice = self.ch.getRegisteredOffice(CompanyNumber)
                                    rOfficeIndex = len(registeredOffice[0])
                                    officers = self.ch.getOfficers(CompanyNumber)
                                    insolvencyNumber = 0
                                    if insolvency is not None:
                                        if 'cases' in insolvency.keys():
                                            insolvencyNumber = len(insolvency['cases'])

                                    listaBase = ([company['company_name'],  # Company Name
                                                  '="' + CompanyNumber + '"',  # Company Number
                                                  insolvencyNumber,    # Insolvency History
                                                  'PRESENT' if self.ch.existForm1(fillingHistory) else 'FAIL',  # Form 4.19
                                                  'PRESENT' if self.ch.existForm2(fillingHistory) else 'FAIL',  # Form 4.7
                                                  insolvencyNumber,    # Insolvency Proceddings Number
                                                  registeredOffice[0],
                                                  registeredOffice[1],
                                                  registeredOffice[2],
                                                  registeredOffice[3],
                                                  registeredOffice[4]
                                                  ])
                                    logging.info(CompanyNumber + '- Added')
                                    for row in officers:
                                        listaBase.append(row['name'])
                                        listaBase.append(row['appointed_on'])
                                        listaBase.append(row['resigned_on'] if 'resigned_on' in row.keys() else 'FAIL')
                                        listaBase.append(str(row['date_of_birth']['month']) + '-' + str(row['date_of_birth']['year'])
                                                                                    if 'date_of_birth' in row.keys() else 'FAIL')
                                        listaBase.append(row['officer_role'])
                                        officerAddress = self.dict2list(row['address'])
                                        for n in range(5):
                                            try:
                                                listaBase.append(officerAddress[n])
                                            except:
                                                listaBase.append('FAIL')
                                        self.lista.append(list(listaBase))

                                        del listaBase[(-10):] #Delete 10 fields.
                                    self.updateSignal.emit(count)
                                    count = count + 1
                                    break
                        except:
                            break
                    else:
                        print('Paused')
                        time.sleep(5)

            self.save(True)
            self.closeSignal.emit(True)


    def save(self, ReiniciarLista):

        def getTime():
            now = datetime.datetime.now()
            return str(datetime.time(now.hour, now.minute, now.second)).replace(":","")

        def saving(filename):
            with open(self.fileOutput.replace(".csv","") + filename, 'w', newline='') as csvfile:
                    spamwriter = csv.writer(csvfile, dialect='excel', delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                    spamwriter.writerow([
                        'Company Name',
                        'Company Number',
                        'Insolvency History',
                        '4,19',
                        '4,7',
                        'Insolvency Proceedings Number',
                        'Registered Office: Address 1',
                        'Registered Office: Address 2',
                        'Registered Office: Address 3 (Region)',
                        'Registered Office: Locality (Locality)',
                        'Registered Office: Postcode',
                        'Officer: Name',
                        'Officer: Appointed Date',
                        'Officer: Resigned Date',
                        'Officer: Year of Birth',
                        'Officer: Position',
                        'Officer: Address 1',
                        'Officer: Address 2',
                        'Officer: Address 3 (Region)',
                        'Officer: Address 4 (Locality)',
                        'Officer: Postcode'
                    ])
                    spamwriter.writerows(self.lista)
        try:
            saving('.csv')
        except:
            print(getTime())
            saving('-' + getTime() + '.csv')

        if ReiniciarLista:
            self.lista = []

    def dict2list(self, dict):
        #Convierte en lista un diccionario
        dictlist = []
        zip_code = 'FAIL'
        Add1 = 'FAIL'
        Add2 = 'FAIL'
        Add3 = 'FAIL'
        Add4 = 'FAIL'

        for key, value in dict.items():
            temp = [key, value]
            dictlist.append(temp)
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
            if dictlist[n][0] == 'locality':
                Add3 = (dictlist[n][1])
                del dictlist[n]
                break
        for n in range(len(dictlist)):
            if dictlist[n][0] == 'region':
                Add4 = (dictlist[n][1])
                del dictlist[n]
                break
        for n in range(len(dictlist)):
            if dictlist[n][0] == 'postal_code':
                zip_code = (dictlist[n][1])
                del dictlist[n]
                break

        return [Add1, Add2, Add3, Add4, zip_code]


    def siHayChance(self):
        #Funcion para verificar si hay chance con las peticiones del server REST
        if self.ch.getCountP() > 9:
            return True
        else:
            return False

    def getLinesCount(self):
        with open(self.fileImport, newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
            count = sum(1 for row in spamreader)
            self.maxSignal.emit(count)

if __name__ == '__main__':
    obj = Importer()
    obj.importar()
