import random
import time
import numpy as np
from itertools import combinations as combi


ROWS = 10
COLS = 15
if ROWS * COLS < 100:
  NORM = 100
else:
  NORM = 1000

PARTICIPANTS_NUMBER = 20
BUDGET = 40
TRAJ1 = 5
TRAJ2 = 15
COST1 = 1
COST2 = 10
TOP_K = 3

d = [[-1,0],[0,1],[1,0],[0,-1]]



class Traj(object):
  """
  generate a path in map
  """

  def __init__(self,sPoint,length):
    self.sPoint = sPoint
    self.length = length 
    self.cost = random.uniform(COST1, COST2)
    self.trajArray = []
    self.spy = sPoint[0]
    self.spx = sPoint[1]

    for i in range(length):
      while True:
        direct = random.randint(0,3) 
        tempY = self.spy + d[direct][0]
        tempX = self.spx + d[direct][1]
        #print(direct, tempX, tempY)
        if tempX < 0 or tempX > COLS - 1 or tempY < 0 or tempY > ROWS - 1:
          continue
        arrayLen = len(self.trajArray)
        if arrayLen > 0 and tempY == self.trajArray[arrayLen - 1][0] and tempX == self.trajArray[arrayLen - 1][1]:
          continue
        num1 = self.spy * COLS + self.spx
        num2 = tempY * COLS + tempX
        # transform directed graph into undirected graph
        if self.spy <= tempY and self.spx <= tempX:
          edgeNumber = num1 * NORM + num2
        else:
          edgeNumber = num2 * NORM + num1

        tuple = (self.spy, self.spx, tempY, tempX, edgeNumber, self.cost)
        self.trajArray.append(tuple)
        self.spy = tempY
        self.spx = tempX
        break


def traj_generate(trajNumber):
  """
  generate trajectories
  """ 
  trajArr = []
  print("now generate "+str(trajNumber)+" trajs")
  for i in range(trajNumber):
    sPoint = random.randint(0, ROWS - 1), random.randint(0, COLS - 1)
    l = random.randint(TRAJ1, TRAJ2)
    traj = Traj(sPoint, l)
    trajArr.append(traj)
    #print(i,"length=",traj.length)
    #print(len(traj.trajArray))
    #for j in range(len(traj.trajArray)):
    #  print(traj.trajArray[j], '->')
  return trajArr


def select_by_random(trajArr, budget):
  """
  select participants randomly
  """
  participants = []
  trajPool = trajArr[:]
  leftBudget = budget
  count = len(trajArr)
  random.shuffle(trajPool)  
  
  while leftBudget > 0 and count > 0:
    pick = random.randint(0,len(trajPool) - 1)
    count -= 1
    useBudget = trajPool[pick].cost
    if leftBudget - useBudget >= 0:
      participants.append(trajPool[pick])
      #print("pick",pick)
      #for ll in range(len(trajPool[pick].trajArray)):
      #  print(trajPool[pick].trajArray[ll])
      leftBudget -= useBudget
      del(trajPool[pick])
  return participants


def select_by_pureGreedy(trajArr, budget, edgeDic):
  """
  pure greedy: choose participants with maximum (coverate(pre+parp)-coverate(pre))/cost
  the result is unbound
  """
  participants = []
  trajPool = trajArr[:]
  leftBudget = budget

  while leftBudget > 0:
    pick = -1
    maximumRatio = 0
    # find maximum delta_length/cost
    for index in range(len(trajPool)):
      # budget is not enough
      if leftBudget - trajPool[index].cost < 0:
        continue
      # otherwise budget is enough
      tempParticipants = participants[:]
      tempParticipants.append(trajPool[index])
      delta_cover_rate = cover_rate(edgeDic, tempParticipants) - cover_rate(edgeDic, participants)
      ratio = delta_cover_rate / trajPool[index].cost
      #print(index, "ratio", ratio, "cost", trajPool[index].cost, "deltaCover", delta_cover_rate, "len of now cover", len(tempParticipants), cover_rate(edgeDic, tempParticipants), "len of pre cover", len(participants), cover_rate(edgeDic, participants, ratio))
      if ratio > maximumRatio:
        maximumRatio = ratio
        pick = index
    # find the best candidate !
    if pick != -1:
      participants.append(trajPool[pick])
      leftBudget -= trajPool[pick].cost
      #print("this round picks", pick, "with maxRatio=", maximumRatio, "leftBudget=", leftBudget)
      del(trajPool[pick])
    else:
    # can not find a candidate, terminate loop
      return participants
  return participants   
 

def select_by_probablisticGreedy(trajArr, budget, edgeDic):
  """
  probablistic greedy: choose top-k parps and select one by probability
  the result is unbound
  """
  participants = []
  trajPool = trajArr[:]
  leftBudget = budget

  while leftBudget > 0:
    pick = -1
    maximumRatio = 0
    candidatePool = []
    # find maximum delta_length/cost
    for index in range(len(trajPool)):
      # budget is not enough
      if leftBudget - trajPool[index].cost < 0:
        continue
      # otherwise budget is enough
      tempParticipants = participants[:]
      tempParticipants.append(trajPool[index])
      delta_cover_rate = cover_rate(edgeDic, tempParticipants) - cover_rate(edgeDic, participants)
      ratio = delta_cover_rate / trajPool[index].cost
      tuple = (ratio, index)
      candidatePool.append(tuple)
    # pick one candidate by probability!! Add some uncertainty maybe a good thing.
    if len(candidatePool) > 0:
      candidatePool.sort()
      # pick one from top-k
      candidatePool = candidatePool[-min(TOP_K,len(candidatePool)):]
      #print("last candadate", candidatePool)
      randNum = random.randint(0, len(candidatePool) - 1)
      pick = candidatePool[randNum][1]
      leftBudget -= trajPool[pick].cost
      participants.append(trajPool[pick])

      #print("this round picks", pick, "with maxRatio=", candidatePool[randNum][0], "leftBudget=", leftBudget)
      del(trajPool[pick])

    else:
    # can not find a candidate, terminate loop
      return participants
  return participants




def select_by_boundedGreedy(trajArr, budget, edgeDic):
  """
  greedy alg. with worst guarantee of approximate ratio equals 1-1/e
  this is a recursive function
  """
  #print("****************************************")
  #print("visit",len(trajArr))

  if len(trajArr) == 1:
    if trajArr[0].cost <= budget:
      #print(trajArr[0].cost)
      return trajArr[0], trajArr[0].cost
    else:
      return None, 0

  if len(trajArr) == 2:
    t1 = trajArr[0].cost
    t2 = trajArr[1].cost
    t3 = trajArr[0].cost + trajArr[1].cost
    if t3 <= budget:
      return trajArr, t3
    elif t1 <= budget:
      return trajArr[0], t1
    elif t2 <= budget:
      return trajArr[1], t2
    else:
      return None, 0


  if len(trajArr) >= 3:
     # build cursive part
     k = len(trajArr) / 2
     trajPool = random.sample(trajArr, k)  
     cursivePart = [] 
     #print("k=",k)
     for i in range(len(trajPool)):
       cursivePart.append(trajPool[i])
       #print(trajPool[i].cost)
     

     # start to solve

     parp1, parp1Cost = select_by_boundedGreedy(cursivePart, budget, edgeDic)
     H1 = cover_rate(edgeDic, parp1)

     #print("enumerate part started")
     parp2 = []
     H2 = 0

     combiList = list(combi(trajArr, len(trajArr) / 2 + 1))      

     for i in range(len(combiList)):
       #print("now enum combiList",i)
       participants = list(combiList[i])[:]
       tempParp2Cost = 0
 
       # combiList exceed budget
       continueFlag = False
       for j in range(len(participants)):
         tempParp2Cost += participants[j].cost
         if tempParp2Cost > budget:
           #print("combiList", i, "exceeds budget")
           continueFlag = True
           break
           
       if continueFlag == True:
        continue       


       complementaryList = list(set(trajArr).difference(set(participants))) 
 
       #print("previous parp2Cost", tempParp2Cost)
       # a sequence of greedy choice
       while len(complementaryList) > 0:
         maxRatio = -1
         pick = -1

         # find maximum w/c participants
         #print("need to pick from", len(complementaryList))
         for j in range(len(complementaryList)):
           tempParticipants = participants[:]
           tempParticipants.append(complementaryList[j])

           delta_cover_rate = cover_rate(edgeDic, tempParticipants) - cover_rate(edgeDic, participants)
           ratio = delta_cover_rate / complementaryList[j].cost
           if ratio > maxRatio:
             maxRatio = ratio
             pick = j

         # find appropriate traj
         if pick != -1 and tempParp2Cost + complementaryList[pick].cost <= budget:
           tempParp2Cost += complementaryList[pick].cost
           #print("+",complementaryList[pick].cost,"=",tempParp2Cost)
           participants.append(complementaryList[pick])
           
         del(complementaryList[pick])
       # if current cover is a better global cover, replace
       tempCoverRate = cover_rate(edgeDic, participants) 
       #print("tempCoverRate",tempCoverRate,"tempParp2Cost",tempParp2Cost,"H2",H2)
       
       
       if tempCoverRate > H2:
         H2 = tempCoverRate
         parp2 = participants      
         parp2Cost = tempParp2Cost
       
     if H1 > H2:
         return parp1, parp1Cost
     else:
         return parp2, parp2Cost
  return None

















def edge2D_hashing_list(mapRows, mapCols):
  """
  hashing 2D edges into a 1D list
  undirected graph
  """
  edgeDic = {}
  for i in range(mapRows):
    for j in range(mapCols):
      orginNode = i * mapCols + j
      if i + 1 < mapRows:
        linkNode = (i + 1) * mapCols + j
        edgeNumber1 = orginNode * NORM + linkNode
        #edgeNumber2 = linkNode * NORM + orginNode
        edgeDic[edgeNumber1] = True
        #edgeDic[edgeNumber2] = True
        #print(i, j, "->", i + 1, j, "edges",edgeNumber1, edgeNumber2)
      if j + 1 < mapCols:
        linkNode = i * mapCols + j + 1
        edgeNumber1 = orginNode * NORM + linkNode
        #edgeNumber2 = linkNode * NORM + orginNode
        edgeDic[edgeNumber1] = True
        #edgeDic[edgeNumber2] = True
        #print(i, j, "->", i, j + 1, "edges",edgeNumber1, edgeNumber2)
  return edgeDic
  

def cover_rate(edgeDic, participantsList, displayFlag = False):
  """
  compute cover_rate
  """
  tempDic = {}
  for i in range(len(participantsList)):
    for j in range(len(participantsList[i].trajArray)):
      tempEdge = participantsList[i].trajArray[j][4]
      tempDic[tempEdge] = 1
  
  if displayFlag == True:
    cover_display(tempDic, ROWS, COLS)

  return len(tempDic) * 1.0 / len(edgeDic)


def cover_display(edgeDic, rows, cols):
  """
  display the cover
  """
  #print("cover display",rows,cols)   

  # build a empty placeHolder
  placeHolder = []
  for i in range(rows):
    tempArray = []
    for j in range(cols):
      if j == cols - 1:
        tempArray.append(".")
      else:
        tempArray.append(".")
        tempArray.append(" ")
    placeHolder.append(tempArray)
 
  # fill in the covered edge
 
  for tempEdge in edgeDic:
    originNode = tempEdge / NORM
    linkNode = tempEdge % NORM

    p1x = originNode % COLS
    p1y = originNode / COLS

    p2x = linkNode % COLS
    p2y = linkNode / COLS
    #print("find edge",tempEdge,"origin",p1y,p1x,"link",p2y,p2x)

    # assume that p1x<=p2x p1y<=p2y
    if p1y == p2y:
    # at the same row
      #placeHolder[p1y][max(p2x, p1x) * 2 - 1] = "_"
      placeHolder[p1y][p2x * 2 - 1] = "_"
    else:
    # at the same col
      #placeHolder[max(p2y, p1y)][p1x * 2] = "|"
      placeHolder[p2y][p1x * 2] = "|"

  outpic = []
  for i in range(len(placeHolder)):
    tempStr = ""
    for j in range(len(placeHolder[i])):
      tempStr += str(placeHolder[i][j])
    outpic.append(tempStr)
    

  for i in range(len(outpic)):
      print('%s'%outpic[i])
  return outpic





edgeDictionary = edge2D_hashing_list(ROWS, COLS)
print("tot edge number", len(edgeDictionary))  
print("tot potential participants number", PARTICIPANTS_NUMBER)
print("tot budget", BUDGET)
print("average cost", (COST1 + COST2) / 2.0)
print("average length", (TRAJ1 + TRAJ2) / 2.0)
parpTrajs = traj_generate(PARTICIPANTS_NUMBER)


for k in range(1):
  print("********************************************************************************")
  print("********************************************************************************")
  
  totCost = 0 
  participants = select_by_random(parpTrajs, BUDGET)
  for i in range(len(participants)):
    totCost += participants[i].cost
  r1 = cover_rate(edgeDictionary, participants, True)
  print("random", k, "cover rate", r1, "cover cost=", totCost)
 

  totCost2 = 0
  participants2 = select_by_pureGreedy(parpTrajs, BUDGET, edgeDictionary)
  for i in range(len(participants2)):
    totCost2 += participants2[i].cost
  r2 = cover_rate(edgeDictionary, participants2, True)
  print("pure greedy", k, "cover rate=", r2, "cover cost=", totCost2)
 

  totCost3 = 0
  participants3 = select_by_probablisticGreedy(parpTrajs, BUDGET, edgeDictionary)
  for i in range(len(participants3)):
    totCost3 += participants3[i].cost
  r3 = cover_rate(edgeDictionary, participants3, True)
  print("pro greedy", k, "cover rate=", r3, "cover_cost=", totCost3)  
 

  participants4, totCost4 = select_by_boundedGreedy(parpTrajs, BUDGET, edgeDictionary)
  r4 = cover_rate(edgeDictionary, participants4, True)
  print("bounded greedy", k, "cover rate=", r4, "cover_cost=", totCost4)
  



"""
parp, parpCost = select_by_boundedGreedy(parpTrajs, BUDGET, edgeDictionary)
print("cardin", len(parp))
print("totCost", parpCost)
for i in range(len(parp)):
  print(parp[i].cost)
print("cover rate",cover_rate(edgeDictionary, parp))
"""





    

