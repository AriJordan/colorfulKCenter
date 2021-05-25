import itertools
from numpy import array
import random
import csv
from instances import  instance
from data.bank.bankConfiguration import bankConfiguration
import math


def getBankInstance():
    points = getBankPoints(bankConfiguration["colorType"])
    subset, p = getSubset(points, bankConfiguration["totalPoints"], bankConfiguration["percentage"])
    return instance(subset, bankConfiguration["nCenters"], p)


def getSubset(points, totalPoints, percentage):
    if bankConfiguration["fixSeed"]:
        random.seed(42)
    allPoints = sum(len(colPoints) for colPoints in points)
    percentages = [len(colPoints)/allPoints for colPoints in points]
    subPoints = [array( random.sample(list(colPoints), round(totalPoints*percentage))) for colPoints, percentage in zip(points,percentages)]
    p = [math.floor(len(colPoints)*percentage) for colPoints in subPoints]
    return subPoints, p

def getBankPoints(colorType):
    with open('./data/bank/bank-full.csv', mode='r') as csv_file:
        # 45211 entries of phone calls
        csv_reader = csv.DictReader(csv_file, delimiter=';')
        data = list(csv_reader)

    cleanData = clean(data)

    rescale('age', cleanData, scaling=3)
    rescale('balance', cleanData, scaling=20)

    points = createPoints(cleanData, colorType)

    return points



def clean(data):
    def cleanEntry(person):
        entry={}
        # coordinates
        entry['age']=int(person['age'])
        entry['balance']=int(person['balance'])
        entry['personalLoan'] = 1 if person['loan']=='yes' else 0
        entry['housingLoan'] = 1 if person['housing']=='yes' else 0

        # color classes
        entry['job']=person['job']
        entry['education']=person['education']
        return entry

    # remove customers who have been called multiple times
    # 36954 unique customers
    uniqueCustomers = [person for person in data if person['previous']=='0']

    # remove customers with incomplete data
    # 35281 customers with complete information
    completeCustomers = [person for person in uniqueCustomers if person['job']!='unknown' if person['education']!='unknown']

    return [cleanEntry(person) for person in completeCustomers]


def rescale(attribute, entries, scaling=1):
    minVal = min([entry[attribute] for entry in entries])
    maxVal = max([entry[attribute] for entry in entries])
    for entry in entries:
        entry[attribute] = (entry[attribute]-minVal)/(maxVal-minVal)*scaling
    return entries


def createPoints(cleanCustomers, colorType):

    def point(entry):
        return array([entry['age'], entry['balance'], entry['personalLoan'], entry['housingLoan']])

    jobs = ["admin.","unemployed","management","housemaid","entrepreneur","student","blue-collar","self-employed","retired","technician","services"]
    education = ["secondary","primary","tertiary"]

    if colorType == "intersection":
        colors = list(itertools.product(jobs, education))
        points=[ [] for color in colors]
        for entry in cleanCustomers:
            points[colors.index((entry['job'],entry['education']))].append(point(entry))

    if colorType == "overlap":
        colors = jobs + education
        points=[ [] for color in colors]
        for entry in cleanCustomers:
            points[colors.index(entry['job'])].append(point(entry))
            points[colors.index(entry['education'])].append(point(entry))

    return array([array(colPoints) for colPoints in points])
