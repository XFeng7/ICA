import numpy as np
import random
from resourse import ICA, Country, Empire, Colony
import matplotlib.pylab as plt
import time

ica = ICA()

country = ica.createCountries()

ica.createEmpires()

empire = ica.empires

# """
index = 1

plt.ion()
colorList = ['#FFB6C1', '#DC143C', '#483D8B', '#0000FF', '#6495ED', '#00BFFF',
             '#00FF7F', '#FFFF00', '#FFD700', '#FF4500']
while len(empire) != 1:
    empire = ica.empires

    ica.moveAction()
    ica.compare()
    ica.compete()
    ica.weedOut()

    # x_l, y_l = ica.plot()

    plt.clf()

    for ei in range(0, len(empire)):
        currentColor = colorList[ei]
        # print(currentColor)
        plt.scatter(empire[ei].x, empire[ei].y, color=currentColor,s = 400 +abs(empire[ei].cost))
        for colony in empire[ei].colonies:
            plt.scatter(colony.x, colony .y, color=currentColor)

    empiresCost = [e.getSumCost() for e in empire]
    print("第{}伦 -- {}".format(index, empiresCost))
    print("帝国数: {} , 殖民地数: {}".format(len(ica.empires), len(ica.colonies)))
    minEmpiresCost = np.argmin(empiresCost)

    marsEmpire = empire[minEmpiresCost]
    print("第{}伦 -- 战神 ：x:{}, y:{}".format(index, marsEmpire.x, marsEmpire.y))
    index += 1
    print()

    plt.pause(0.05)
    plt.show()
    
print("cost: {} ,最终坐标: {} ".format(empire[0].cost, empire[0].getPosit()))
plt.show()
plt.ioff()

# """
