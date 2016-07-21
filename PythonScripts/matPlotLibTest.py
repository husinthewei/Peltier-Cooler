import matplotlib.pyplot as plt

plt.ion()

y = [0,2,4,6,8,10,12,14,16,2000]

for i in range(10):
    plt.axis([0, 10, 0, y[i]])
    plt.scatter(i, y[i])
    plt.pause(0.05)

while True:
    plt.pause(0.05)