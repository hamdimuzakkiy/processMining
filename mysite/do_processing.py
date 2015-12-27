__author__ = 'hamdiahmadi'

import processing as pr
import copy

def makeGraph(file):
    file = file
    excel = pr.excel()
    heuristic = pr.heuristic()

    rawData = excel.readData(file)
    dataDependency = heuristic.getMatrixDependecy(copy.deepcopy(rawData))
    dataMeasure = heuristic.getMatrixDependencyMeasure(copy.deepcopy(dataDependency))
    dataOverLap, dataCountOverLap = heuristic.getOverlap(copy.deepcopy(rawData))
    dataMeasureOverlap = heuristic.multipleList2D(copy.deepcopy(dataOverLap),copy.deepcopy(dataMeasure))
    RBT,POT,DT = heuristic.getRBTPOTDT(copy.deepcopy(dataDependency), copy.deepcopy(dataMeasureOverlap))
    data1Loop,data2Loop = heuristic.getLoop(copy.deepcopy(rawData))
    graph = heuristic.getInitGraph(copy.deepcopy(rawData))
    graph = heuristic.makeGraph(rawData,graph,dataMeasure,DT)
    graph = heuristic.getRelation(rawData,graph,dataDependency,dataCountOverLap,dataMeasureOverlap)
    graph = heuristic.makeGraph(rawData,graph,data1Loop,1)
    graph = heuristic.makeGraphLoop(rawData,graph,data1Loop,data2Loop,POT)
    return graph

# if __name__ == '__main__':

