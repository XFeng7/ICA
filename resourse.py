import numpy as np
import random as rn
import math

Constant_countries = 100
Constant_empires = 10
Constant_colony = 90

alpha = 0.5
beta = 1
gamma = math.pi / 10

np.seterr(divide='ignore', invalid='ignore')
"""
20+x^2+y^2-10*cos(2*pi*x)-10*cos(2*pi*y)
"""


class Country:

    def __init__(self, name):
        """
        :param index: 国家的名字编号
        :param x: 参数的横坐标
        :param y: 参数的纵坐标
        """
        self.cost = 0
        # index 是一个国家的名字
        self.name = name
        self.x = np.random.uniform(-6, 6)
        self.y = np.random.uniform(-6, 6)

        self.calcCost()



    def getName(self):
        return self.name

    def updataCost(self, cost):
        self.cost = cost

    def getCost(self):
        return self.cost

    def getPosit(self):
        # print(self.x, self.y)
        return self.x, self.y

    def updataPosit(self, x, y):
        self.x = x
        self.y = y

    def calcCost(self):
        x = self.x
        y = self.y

        cost = 20 + x * x + y * y - 10 * math.cos(2 * math.pi * x) - 10 * math.cos(2 * math.pi * y)

        self.cost = cost

    def moveColony(self, lord_x, lord_y):
        # print("old_x: {}  old_y: {}".format(self.x, self.y))

        distance = math.sqrt((self.x - lord_x) ** 2 + (self.y - lord_y) ** 2)
        np.random.seed(1)
        moveAngle = np.random.uniform(-gamma, gamma)
        moveDistance = np.random.uniform(0, beta * distance)

        posit = np.array([[lord_x - self.x], [lord_y - self.y], [1]])
        R = np.array([[math.cos(moveAngle), -math.sin(moveAngle), 0], [math.sin(moveAngle), math.cos(moveAngle), 0], [0, 0, 1]])
        if distance > 0:
            ratio = moveDistance / distance
        else:
            ratio = 1
        S = np.array([[ratio, 0, 0], [0, ratio, 0], [0, 0, 1]])

        new_posit = np.dot(S, np.dot(R, posit))
        o = np.array([[self.x], [self.y], [0]])

        new_posit = new_posit + o

        self.updataPosit(new_posit[0, 0], new_posit[1, 0])


class Empire(Country):

    def __init__(self, oneImperia):
        # super(Empire, self).__init__(name=oneImperia.name)
        self.x = oneImperia.x
        self.y = oneImperia.y
        self.name = oneImperia.name
        self.cost = oneImperia.cost

        self.colonies = []
        # 帝国的cost function
        self.Cn = 0
        # 帝国的势力标准化
        self.Pn = 0
        # 第n个Emp的初始殖民地个数
        self.NCn = 0
        # 帝国的总价值
        self.TCn = 0

        self.NTCn = 0

    def addColony(self, colony):
        self.colonies.append(colony)

    def getColony(self, index):
        return self.colonies[index]

    def deleteColony(self, index):
        del self.colonies[index]

        return self.colonies

    def getRookieColony(self):
        rookie = np.array([colony.getCost() for colony in self.colonies])
        return np.argmax(rookie)

    def initSetPower(self, maxEmpireCost, totalEmpireCost):
        # 帝国的cost function
        self.Cn = self.getCost() - maxEmpireCost
        # 帝国的势力标准化
        self.Pn = abs(self.Cn / totalEmpireCost)
        # 第n个Emp的初始殖民地个数
        self.NCn = round(self.Pn * 90 - 0.1)

        # 返回每个帝国有的殖民地数量
        return self.NCn

    def getNumColony(self):
        return len(self.colonies)

    def getColonyList(self):
        return self.colonies

    def getSumCost(self):

        colony = self.colonies[:]

        colonyCostList = [c.getCost() for c in colony]
        sumCost = sum(colonyCostList)

        if self.NCn == 0:

            self.TCn = float(self.cost) + alpha
        else:
            self.TCn = float(self.cost) + alpha * (sumCost / self.NCn)

        return self.TCn

    def getColonyPosit(self):

        colonyPosit = [c.getPosit() for c in self.colonies]
        print(colonyPosit)


class Colony(Country):

    def __init__(self, oneImperia):
        # super(Colony, self).__init__(name=oneImperia.name)

        self.x = oneImperia.x
        self.y = oneImperia.y
        self.name = oneImperia.name
        self.cost = oneImperia.cost

        self.lord = 0
        self.state = 'colony'

    def setLord(self, lord):
        self.lord = lord

    def getLord(self):
        return self.lord


class ICA:

    def __init__(self):
        self.countries = []
        self.empires = []
        self.colonies = []

    def getAll(self):

        c_name = []
        c_cost = []

        for e in self.empires:

            c_name = [c.name for c in e.colonies]
            c_cost = [c.cost for c in e.colonies]

        print("帝国: name:{}- cost: {}. 殖民地：{} - {}".format(e.name, e.cost, c_name,c_cost))



    def getCountries(self):

        return self.countries

    def getEmpires(self):
        return self.empires

    def getColonies(self):
        return self.colonies

    # 创建国家
    def createCountries(self):
        # 初始化： 100个国家，每个国家一个编号: 0-99
        count = Constant_countries

        for i in range(count):
            self.countries.append(Country(i))

        return self.countries

    def createEmpires(self):

        """
        初始化：
        1.将前十个国家作为帝国，后面都是殖民地
        """
        countries = self.countries[:]

        CostList = [c.getCost() for c in countries]

        for i in range(Constant_empires):
            minIndex = np.argmin(CostList)
            self.empires.append(Empire(countries[minIndex]))

            del countries[minIndex]
            del CostList[minIndex]

        empireCost = [ec.getCost() for ec in self.empires]
        max_empire_cost = max(empireCost)

        totalEmpireCost = sum(empireCost)

        totalEmpireCost = totalEmpireCost - 10 * max_empire_cost

        for ec in self.empires:
            # 每个帝国的殖民地个数
            self.NCn = ec.initSetPower(max_empire_cost, totalEmpireCost)

            # 给每个帝国分配殖民国，初始化时，随机分一个
            for n in range(self.NCn):
                if len(countries) > 0:
                    l = [num for num in range(0, len(countries))]
                    oneColonyindex = np.random.choice(l)

                    self.colonies.append(Colony(countries[oneColonyindex]))

                    # 给帝国对象添加殖民地
                    ec.addColony(countries[oneColonyindex])

                    del countries[oneColonyindex]

    def compare(self):
        """
        1. 遍历全部的帝国列表，看每一个帝国是否有殖民地
        2. 判断殖民的cost 是否 小于帝国的cost
        3. 如果 帝国的cost 大于 战神殖民地的cost
        4. 战神胜利，战神变成帝国，被灭亡帝国的全部殖民地包括自己都归战神所有


        """
        for ii in range(0, len(self.empires)):

            e = self.empires[ii]    #当前帝国
            if e.getNumColony() > 0:    # 有殖民地
                colonyList = e.getColonyList()[:]

                colonyCostList = [cost.getCost() for cost in colonyList]

                marsIndex, marsCost = np.argmin(colonyCostList), min(colonyCostList)

                if marsCost < e.cost:
                    # 新皇登基
                    del self.empires[ii]
                    self.empires.append(Empire(colonyList[marsIndex]))

                    del colonyList[marsIndex]
                    colonyList.append(e)

                    for t in colonyList:
                        self.empires[-1].colonies.append(t)







    def weedOut(self):
        """
        没有殖民地的帝国将会被淘汰，变成一个殖民地

        """
        deleteList = []  # 没有殖民地的帝国标号
        for e_i in range(0, len(self.empires)):

            e = self.empires[e_i]

            if e.getNumColony() == 0:

                deleteList.append(e_i)

        while len(deleteList) > 0:
            index = np.argmax(deleteList)
            _max = max(deleteList)
            del self.empires[_max]
            del deleteList[index]

    def compete(self):

        """
        1. 计算帝国的总势力大小
        2. 挑出最弱帝国的最弱殖民地：弱鸡
        3. 计算每个帝国占有"弱鸡"的概率
        4. 将弱鸡分配给概率最大的帝国
        """

        # 1.

        empiresTCn = [ec.getSumCost() for ec in self.empires]

        rookieEmpireIndex = np.argmax(empiresTCn)  # 最弱帝国的索引

        if self.empires[rookieEmpireIndex].getNumColony() == 0:
            del empiresTCn[rookieEmpireIndex]

        rookieEmpireIndex = np.argmax(empiresTCn)
        # 最弱帝国
        rookieEmpire = self.empires[rookieEmpireIndex]

        # 取出最弱帝国的最弱殖民地

        rookieColonyCostList = [c.getCost() for c in rookieEmpire.getColonyList()]

        rookieColonyIndex = np.argmax(rookieColonyCostList)

        # 2.
        # 最弱帝国的最弱殖民地 对象
        rookieColony = rookieEmpire.getColonyList()[rookieColonyIndex]

        # 3.
        # 帝国总价值

        empireTotalCost = [e.TCn for e in self.empires]

        max_TCn = max(empireTotalCost)

        for e in self.empires:
            e.NTCn = e.TCn - max_TCn

        GroupTotalCost = [e.NTCn for e in self.empires]
        sumGroupTotalCost = sum(GroupTotalCost)
        # 帝国对弱鸡的占有率
        Pn = abs(np.divide(GroupTotalCost, sumGroupTotalCost))

        R = [np.random.uniform(0, 1) for num in range(0, len(Pn))]

        D = Pn - R

        winner = np.argmax(D)

        rookieEmpire.deleteColony(rookieColonyIndex)
        self.empires[winner].addColony(rookieColony)

    def moveAction(self):

        for e in self.empires:
            colonies = e.getColonyList()
            for c in colonies:
                c.moveColony(e.x, e.y)
                c.calcCost()
















