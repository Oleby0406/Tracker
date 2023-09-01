from matplotlib import pyplot as plt
import itertools as it

#calculate average
def averageOfOneTime(input):
    input = [i for i in input if i != -1]
    return sum(input) / len(input)

data = open("libraryCollectedData.txt", "r")
content = data.readlines()

timeList = ['12:00', '12:30', ' 13:00', ' 13:30', ' 14:00', ' 14:30', ' 15:00', ' 15:30', ' 16:00', ' 16:30', 
            ' 17:00', ' 17:30', ' 18:00', ' 18:30', ' 19:00', ' 19:30', ' 20:00', ' 20:30', ' 21:00']
datalist = []
numLists = 0
for i in range (1, len(content), 4):
    datalist.append(content[i][:-1].strip('][').split(','))
    datalist[numLists] = [float(k) for k in datalist[numLists]]
    numLists += 1

average = list(map(averageOfOneTime, it.zip_longest(*datalist)))
minimumFullness = min(average)
maximumFullness = max(average)

minimumFullnessTime = timeList[average.index(minimumFullness)]
maximumFullnessTime = timeList[average.index(maximumFullness)]

earliestDate = content[0][:-1]
latestDate = content[len(content) - 4][:-1]

data.close()

sharedVars = open("sharedVars.txt", "w")
sharedVars.write("[" + ', '.join(str(x) for x in timeList) + "]" + "\n")
sharedVars.write("[" + ', '.join(str(round(x, 2)) for x in average) + "]" + "\n")
sharedVars.write("Minimum is: " + str(round(minimumFullness * 100, 2)) + "% at " + minimumFullnessTime + "\n")
sharedVars.write("Maximum is: " + str(round(maximumFullness * 100, 2)) + "% at " + maximumFullnessTime + "\n")
sharedVars.write("Based on data collected between " + earliestDate + " and " + latestDate + ", total of " + str(numLists) + " entries.")

sharedVars.close()

#graph
plt.plot(timeList, average)
plt.xlabel("Time")
plt.ylabel("Fullness")
plt.xticks(rotation=60)
plt.ylim([0, 1])
plt.savefig("main/static/graph.png")
#plt.show()