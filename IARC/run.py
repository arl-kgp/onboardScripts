from collections import deque
import matplotlib.pyplot as plt
from termios import tcflush, TCIFLUSH
import time,sys


class AnalogPlot:
    # constr
    def __init__(self, maxLen):
        # open serial port
        self.ax = deque([0.0] * maxLen)
        self.ay = deque([0.0] * maxLen)
        self.maxLen = maxLen

    # add to buffer
    def addToBuf(self, buf, val):
        if len(buf) < self.maxLen:
            buf.append(val)
        else:
            buf.pop()
            buf.appendleft(val)

    # add data
    def add(self, data):
        assert(len(data) == 2)
        self.addToBuf(self.ax, data[0])
        self.addToBuf(self.ay, data[1])

    # update plot
    def update(self, frameNum, a0, a1, x1, x2):
        try:
            data = [x1, x2]
            # print data
            if(len(data) == 2):
                self.add(data)
                a0.set_data(range(self.maxLen), self.ax)
                a1.set_data(range(self.maxLen), self.ay)
        except KeyboardInterrupt:
            print('exiting')
        return a0,

    # clean up
    def close(self):
        # close serial
        self.ser.flush()
        self.ser.close()


def main():
    # plot parameters
    analogPlot = AnalogPlot(100)
    fig = plt.figure()
    ax = plt.axes(xlim=(0, 100), ylim=(-5, 5))
    a0, = ax.plot([], [])
    a1, = ax.plot([], [])

    x = 1
    fig.show()

    '''proc = subprocess.Popen("./a.out",
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE)
    data = ""
    while True:
        message = proc.stdout.read(1)
        if message != '\n':
            data = data + message
        else:
            data1 = data.split(',')
            if len(data1) == 2:
                x1 = int(data1[0])
                x2 = int(data1[1])
                analogPlot.update(x, a0, a1, x1, x2)
                x = x + 1
                plt.draw()
            data = ""
    proc.wait()'''

    while True:
        data = sys.stdin.readline()

        print data
        data1 = data.split(',')
        if len(data1) >= 2:
            x1 = float(data1[0])
            x2 = float(data1[1])
            analogPlot.update(x, a0, a1, x1, x2)
            x = x + 1
            plt.draw()

    analogPlot.close()
    print('exiting.')

main()