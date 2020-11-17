import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np


y = [0.5, 1.5, 2.5, 3.5, 0.5, 1.5, 2.5, 3.5, 0.5, 1.5, 2.5, 3.5, 0.5, 1.5, 2.5, 3.5, 0.5, 1.5, 2.5, 3.5, 0.5]
# x = [0 * 60, 1 * 60, 2 * 60, 3 * 60, 4 * 60, 5 * 60, 6 * 60, 7 * 60, 8 * 60, 9.3 * 60, 10 * 60, 11 * 60, 12 * 60,
#      13 * 60, 14 * 60, 15 * 60, 16 * 60, 17 * 60, 18 * 60, 19 * 60, 20 * 60]
x = [i * 60 for i in np.arange(len(y))]
# x = np.arange(len(y))
y_values = ["", "OFF", "", "SB", "", "D", "", "ON", ""]

fig, ax1 = plt.subplots(figsize=(12, 2))

ax1.step(x, y)
ax1.plot(x, y, 'C0o', alpha=0.5, color='red')
ax1.set_yticks(np.arange(0, 4.1, 0.5))
ax1.xaxis.set_major_locator(ticker.LinearLocator(0))
ax1.set_yticklabels(y_values)
ax1.xaxis.grid(True)
ax1.set_xlim(-60 / 3, 1440 + 60 / 3)

ax2 = ax1.twinx()
ax2.set_yticks(np.arange(0, 4.1, 1))
ax2.set_yticklabels([''] * 5)
ax2.xaxis.set_minor_locator(ticker.MultipleLocator(60 / 3))
ax2.xaxis.set_major_locator(ticker.MultipleLocator(60))
ax2.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: int(x / 60)))

ax2.grid(True, axis='both', which='both')

y3_values = ["24:00", "01:20", "", "01:20", "", "01:20", "", "01:20", ""]
ax3 = ax1.twinx()
ax3.set_yticks(np.arange(0, 4.1, 0.5))
ax3.set_yticklabels(y3_values)

plt.show()
# plt.savefig('main.png')
