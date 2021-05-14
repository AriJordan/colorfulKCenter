from data.mall.mallConfiguration import mallConfiguration
import random
from instances import instance
from numpy import array, shape
import csv

def getMallInstance(totalPoints):
    points = getMallPoints(totalPoints)
    subset = getSubset(points, totalPoints)
    return instance(subset, mallConfiguration["nCenters"], mallConfiguration["p"])


def getSubset(points, totalPoints):
    allPoints = sum(len(colPoints) for colPoints in points)
    percentages = [len(colPoints)/allPoints for colPoints in points]
    subPoints = [array( random.sample(list(colPoints), round(totalPoints*percentage))) for colPoints, percentage in zip(points,percentages)]
    return subPoints

def getMallPoints(totalPoints):
    with open('./data/mall/Mall_Customers.csv', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        data = list(csv_reader)
    cleanData = clean(data)
    points = createPoints(cleanData)
    return points




def clean(data):
    def cleanup(customer):
        cleanup={}
        cleanup['Gender']=customer['Gender']
        cleanup['Age']=int(customer['Age'])
        cleanup['Income']=int(customer['Annual Income (k$)'])
        cleanup['Spending Score']=int(customer['Spending Score (1-100)'])
        return cleanup

    cleanData = [cleanup(customer) for customer in data]

    return cleanData

def createPoints(cleanData):
    points = [[],[]]
    for customer in cleanData:
        if customer['Gender']=='Male':
            points[0].append( array([customer['Age'], customer['Income']] )  )
        else:
            points[1].append( array([customer['Age'], customer['Income']] )  )
    return array([array(colPoints) for colPoints in points])
