from data.mall.mallConfiguration import mallConfiguration

from instances import instance
from numpy import array, shape
import csv

def getMallInstance(totalPoints):
    points = getMallPoints(totalPoints)
    return instance(points, mallConfiguration["nCenters"], mallConfiguration["p"])


def getMallPoints(totalPoints):
    with open('./data/mall/Mall_Customers.csv', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        data = list(csv_reader)
    cleanData = clean(data)
    points = createPoints(cleanData)

    # TODO: implement only choosing subset of points
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
