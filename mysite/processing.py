__author__ = 'hamdiahmadi'

import xlwt
import xlrd
import copy
import numpy as np

class excel():

    def __init__(self):
        pass

    def dateToString(self,data):
        dates = ''
        for x in range (0,len(data)):
            if x == len(data)-1:
                break
            if int(data[x]) < 10 :
                dates = dates+'0'+str(data[x])
            else :
                dates = dates+''+str(data[x])
        return dates

    def readData(self, file):
        wb = xlrd.open_workbook(filename=file)
        data = wb.sheet_by_index(0)
        list = dict()
        cur = ''
        for x in range(1,data.nrows):
            content = data.row(x)
            if content[0].value != '':
                cur = content[0].value
                list[str(content[0].value)] = []
            tmp = []
            for idx,cell_obj in enumerate(content):
                if idx == 0:
                    continue
                if idx == 2 or idx ==  3:
                    times = self.dateToString(xlrd.xldate_as_tuple(cell_obj.value, wb.datemode))
                    tmp.append(times)
                    continue
                tmp.append(str(cell_obj.value))
            list[cur].append(tmp)
        return list

class heuristic():

    def __init__(self):
        pass

    def getTask(self,rawData):
        listTask = []
        for x in rawData:
            for y in rawData[x]:
                listTask.append(y[0])
        return np.sort(list(set(listTask)))

    def getIndexList(self,lists,where):
        for x in range(0,len(lists)):
            if lists[x] == where:
                return x

    def checkOverLap(self,data1,data2):
        if (data1[0]>data2[0] and data1[0]<data2[1]) or (data1[1]>data2[0] and data1[1]<data2[1]):
            return True
        return False

    def multipleList2D(self,list1,list2):
        return np.multiply(list1,list2)

    def getOverlap(self,rawData):
        listTask = self.getTask(rawData)
        matrix = [[1 for x in range(len(listTask))] for x in range(len(listTask))]
        matrixCountOverlap = [[0 for x in range(len(listTask))] for x in range(len(listTask))]
        tmpMatrixOverlap = [[0 for x in range(len(listTask))] for x in range(len(listTask))]

        for x in rawData:
            for index in range (0,len(rawData[x])-1):
                data1 = []
                data2 = []
                data1.append(rawData[x][index][1])
                data1.append(rawData[x][index][2])
                data2.append(rawData[x][index+1][1])
                data2.append(rawData[x][index+1][2])
                if self.checkOverLap(data1,data2) == True:
                    i = self.getIndexList(listTask,rawData[x][index][0])
                    j = self.getIndexList(listTask,rawData[x][index+1][0])
                    tmpMatrixOverlap[i][j] = 1
                    tmpMatrixOverlap[j][i] = 1
                    matrix[i][j] = 0
                    matrix[j][i] = 0
            matrixCountOverlap = np.add(tmpMatrixOverlap,matrixCountOverlap)
            for y in range(0,len(tmpMatrixOverlap)):
                for x in range(0,len(tmpMatrixOverlap[0])):
                    tmpMatrixOverlap[y][x] = 0
        return matrix,matrixCountOverlap

    def getMatrixDependencyMeasure(self,matrixDependency):
        result = copy.deepcopy(matrixDependency)
        for y in range(0,len(matrixDependency)):
            for x in range(0,len(matrixDependency)):
                if matrixDependency[y][x] == 0:
                    continue
                res = (float(matrixDependency[y][x])-float(matrixDependency[x][y]))/(float(matrixDependency[y][x])+float(matrixDependency[x][y])+1)
                result[y][x] = res
        return result

    def getMatrixDependecy(self, rawData):
        listTask = self.getTask(rawData)
        matrix = [[0 for x in range(len(listTask))] for x in range(len(listTask))]
        for x in rawData :
            for index in range (0,len(rawData[x])-1):
                i = self.getIndexList(listTask,rawData[x][index][0])
                j = self.getIndexList(listTask,rawData[x][index+1][0])
                matrix[i][j]+=1
        return matrix

    def getRBTPOTDT(self,dataDependency, dataMeasureOverlap):
        dataArray = np.array(copy.copy(dataMeasureOverlap))
        resMeasure = np.where(dataArray>0.0)
        listsMeasure = []
        for x in range(0,len(resMeasure[0])):
            coor_y,coor_x = resMeasure[0][x],resMeasure[1][x]
            listsMeasure.append(dataMeasureOverlap[coor_y][coor_x])
        avg = np.average(listsMeasure)
        std = np.std(listsMeasure)

        dataArrayDependency = np.array(copy.copy(dataDependency))
        resDependency = np.where(dataArrayDependency>0.0)
        listsDependency = []
        for x in range(0,len(resDependency[0])):
            coor_y,coor_x = resDependency[0][x],resDependency[1][x]
            listsDependency.append(dataDependency[coor_y][coor_x])
        return float(avg)-(float(std)/float(2)), np.min(listsDependency),float(avg)-float(std)

    def checkOneLoop(self,data1,data2):
        if data1 == data2:
            return True
        return False

    def checkTwoLoop(self,data):
        if data[0] == data[2] and data[1] == data[3]:
            return True
        return False

    def getLoop(self,rawData):
        listTask = self.getTask(rawData)
        matrix1Loop = [[0 for x in range(len(listTask))] for x in range(len(listTask))]
        matrix2Loop = [[0 for x in range(len(listTask))] for x in range(len(listTask))]

        tmpMatrix1Loop = [[0 for x in range(len(listTask))] for x in range(len(listTask))]
        tmpMatrix2Loop = [[0 for x in range(len(listTask))] for x in range(len(listTask))]

        for x in rawData:
            for index in range (0,len(rawData[x])-1):
                if self.checkOneLoop(rawData[x][index][0],rawData[x][index+1][0]) == True :
                    i = self.getIndexList(listTask,rawData[x][index][0])
                    j = self.getIndexList(listTask,rawData[x][index+1][0])
                    tmpMatrix1Loop[i][j] = 1
                elif index+3 <= len(rawData[x])-1:
                    data = []
                    for indexes in range(index,index+4):
                        data.append(rawData[x][indexes][0])
                    if self.checkTwoLoop(data) == True:
                        i = self.getIndexList(listTask,rawData[x][index][0])
                        j = self.getIndexList(listTask,rawData[x][index+1][0])
                        tmpMatrix2Loop[i][j]=1
                        tmpMatrix2Loop[j][i]=1
            matrix1Loop = np.add(matrix1Loop,tmpMatrix1Loop)
            matrix2Loop = np.add(matrix2Loop,tmpMatrix2Loop)
            for y in range(0,len(tmpMatrix1Loop)):
                for x in range(0,len(tmpMatrix1Loop[0])):
                    tmpMatrix1Loop[y][x] = 0
                    tmpMatrix2Loop[y][x] = 0
        return matrix1Loop,matrix2Loop

    def getInitGraph(self,rawData):
        listTask = self.getTask(rawData)
        graph = dict()
        for x in listTask:
            graph[x] = dict()
            graph[x]['input'] = []
            graph[x]['output'] = []
        return graph

    def makeGraph(self,rawData,graph,matrix,threshold):
        lists = self.getTask(rawData)
        for y in range(0,len(matrix)):
            for x in range(0,len(matrix[0])):
                if matrix[y][x] >= threshold:
                    keyFrom = lists[y]
                    keyTo = lists[x]
                    graph[keyFrom]['output'].append(keyTo)
                    graph[keyTo]['input'].append(keyFrom)
                    graph[keyTo]['input'] = list(set(graph[keyTo]['input']))
                    graph[keyFrom]['output'] = list(set(graph[keyFrom]['output']))
        return graph

    def makeGraphLoop(self,rawData,graph,matrix1Loop,matrix2Loop,threshold):
        listTask = self.getTask(rawData)
        for y in range(0,len(matrix1Loop)):
            for x in range(y+1,len(matrix1Loop[0])):
                if matrix2Loop[y][x] == 0:
                    continue
                elif (matrix1Loop[y][y] >= 1 or matrix1Loop[x][x] >= 1) and (matrix2Loop[y][x] > threshold or matrix2Loop[y][x] > threshold):
                    keyFrom = listTask[y]
                    keyTo = listTask[x]
                    if len(graph[keyFrom]['input']) == 0 and len(graph[keyFrom]['output']) == 0:
                        graph[keyTo]['output'].append(keyFrom)
                        graph[keyFrom]['input'].append(keyTo)
                        graph[keyTo]['output'] = list(set(graph[keyTo]['output']))
                        graph[keyFrom]['input'] = list(set(graph[keyFrom]['input']))

                    elif len(graph[keyTo]['input']) == 0 and len(graph[keyTo]['output']) == 0:
                        graph[keyFrom]['output'].append(keyTo)
                        graph[keyTo]['input'].append(keyFrom)
                        graph[keyTo]['input'] = list(set(graph[keyTo]['input']))
                        graph[keyFrom]['output'] = list(set(graph[keyFrom]['output']))

                else :
                    keyFrom = listTask[y]
                    keyTo = listTask[x]
                    graph[keyFrom]['input'].append(keyTo)
                    graph[keyFrom]['output'].append(keyTo)
                    graph[keyTo]['input'].append(keyFrom)
                    graph[keyTo]['output'].append(keyFrom)

                    graph[keyTo]['input'] = list(set(graph[keyTo]['input']))
                    graph[keyFrom]['input'] = list(set(graph[keyFrom]['input']))
                    graph[keyTo]['output'] = list(set(graph[keyTo]['output']))
                    graph[keyFrom]['output'] = list(set(graph[keyFrom]['output']))
        return graph


    def getFirstNode(self,graph):
        lists = []
        for x in graph:
            if len(graph[x]['input']) == 0:
                lists.append(x)
        return lists

    def checkVisit(self,now,list_visit, graph):
        inp = graph[now]['input']
        for x in inp:
            if list_visit[x] == False:
                return False
        return True

    def findCouple(self,rawData,start,graph):
        listTask = self.getTask(rawData)
        res = ''
        queue = []
        is_visit = dict()
        for x in listTask:
            is_visit[x] = False
        is_visit[start] = True
        counter = 2
        for x in graph[start]['output']:
            queue.append(x)
        while counter!=0 and len(queue):
            cur = queue[0]
            res = cur
            queue.pop(0)
            is_visit[cur] = True
            if self.checkVisit(cur, is_visit, graph) == False:
                queue.append(cur)
                continue
            if len(graph[cur]['input']) > 1:
                counter-=len(graph[cur]['input'])
            elif len(graph[cur]['output']) > 1:
                counter+=graph[cur]['output']
                for x in graph[cur]['output']:
                    queue.append(x)
            else :
                for x in graph[cur]['output']:
                    queue.append(x)
        return res

    def getAvgPDMMinPDM(self,matrixMeasure):
        dataArray = np.array(copy.copy(matrixMeasure))
        resMeasure = np.where(dataArray>0.0)
        listsMeasure = []
        for x in range(0,len(resMeasure[0])):
            coor_y,coor_x = resMeasure[0][x],resMeasure[1][x]
            listsMeasure.append(matrixMeasure[coor_y][coor_x])
        return np.average(np.array(listsMeasure)),np.min(np.array(listsMeasure))

    def getRelation(self,rawData,graph,matrix,matrixOverLap,matrixMeasure):
        listTask = self.getTask(rawData)
        avgPDM,minPDM = self.getAvgPDMMinPDM(matrixMeasure)
        for x in graph:
            graph[x]['relation'] = 'sequence'
        for x in graph:
            if len(graph[x]['output']) > 1:
                to1 = self.getIndexList(listTask,graph[x]['output'][0])
                to2 = self.getIndexList(listTask,graph[x]['output'][1])
                fromFrom = self.getIndexList(listTask,x)
                arrMatrix = np.array(matrix)
                PM1 = ( float(matrix[to1][to2])+float(matrix[to2][to1])+ float(2*matrixOverLap[to1][to2]) ) / ( float(matrix[fromFrom][to1]) + float(matrix[fromFrom][to2]) + float(sum(arrMatrix[to1,:])-matrix[to1][to2]) +  float(sum(arrMatrix[to2,:])-matrix[to2][to1]) + float(1))
                couple = self.findCouple(rawData,x,graph)

                from1 = self.getIndexList(listTask,graph[couple]['input'][0])
                from2 = self.getIndexList(listTask,graph[couple]['input'][1])
                toTo = self.getIndexList(listTask,couple)
                PM2 = ( float(matrix[from1][from2])+float(matrix[from2][from1])+ float(2*matrixOverLap[from1][from2]) ) / ( float(matrix[from1][toTo]) + float(matrix[from2][toTo]) + float(sum(arrMatrix[from1,:])-matrix[from1][from2]) +  float(sum(arrMatrix[from2,:])-matrix[from2][from1]) + float(1))
                res = (PM1+PM2)/2

                if res <= minPDM:
                    graph[x]['relation'] = 'xor split'
                    graph[couple]['relation'] = 'xor join'
                elif minPDM <= res and res <= avgPDM:
                    graph[x]['relation'] = 'or split'
                    graph[couple]['relation'] = 'or join'
                elif avgPDM <= res :
                    graph[x]['relation'] = 'and split'
                    graph[couple]['relation'] = 'and join'
        return graph
