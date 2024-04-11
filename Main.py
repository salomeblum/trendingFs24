import pickle as p
import numpy as np
import matplotlib.pyplot as plt


def readPickle(pfad, filename):
    with open(pfad + filename, 'rb') as f:
        data = p.load(f)
    print(len(data))
    return data


def writePickle(data, name):
    with open(name, 'wb') as f:
        p.dump(data, f)


def plotPickle(name):
    with open(name, 'rb') as f:
        data = p.load(f)
    f.close()

    xpoints = np.arange(0, 10000)

    for x in range(6):
        plt.plot(xpoints, data[x])
    plt.show()


if __name__ == '__main__':
    pfad = "K:\\20_TSF\\50_TSF-Proj\\E259_PumpStateDetection\\HSLU_Bachelorarbeit\\Data\\"
    filename = "X.pkl"

    testdata = readPickle(pfad, filename)
    print(len(testdata))

    picklename = "testPickle.pkl"
    writePickle(testdata, picklename)
    plotPickle(picklename)
