import io

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np


class StepLineData:

    def __init__(self, events: []) -> None:
        self.events: list = events
        self._ON_time: float = 0.
        self._D_time: float = 0.
        self._SB_time: float = 0.
        self._OFF_time: float = 0.
        self._x = []
        self._y = []


    def prepare_data(self) -> 'StepLineData':
        x = []
        y = []
        _ON_time, _D_time, _SB_time, _OFF_time = 0., 0., 0., 0.
        if not self.events:
            return [1440, 3.5]
        for e in self.events:
            _status = e.event_status.lower()
            if _status == 'sb':
                y.append(2.5)
                _SB_time += e.time_minute
            elif _status == 'd':
                y.append(1.5)
                _D_time += e.time_minute
            elif _status == 'on':
                y.append(0.5)
                _ON_time += e.time_minute
            else:
                y.append(3.5)
                _OFF_time += e.time_minute
            x.append(e.time_minute)
        self._ON_time = _ON_time
        self._D_time = _D_time
        self._SB_time = _SB_time
        self._OFF_time = _OFF_time
        self._x = x
        self._y = y
        return self


    @property
    def x(self):
        return self._x


    @property
    def y(self):
        return self._y


    @property
    def ON_time(self):
        return self.time_fmt(self._ON_time)


    @property
    def D_time(self):
        return self.time_fmt(self._D_time)


    @property
    def SB_time(self):
        return self.time_fmt(self._SB_time)


    @property
    def OFF_time(self):
        return self.time_fmt(self._OFF_time)


    @property
    def total_time(self):
        return self.time_fmt(self._ON_time +
                             self._D_time +
                             self._SB_time +
                             self._OFF_time)


    @staticmethod
    def time_fmt(_time):
        _hours = int(_time / 60)
        _minutes = int(_time % 60)
        return f'{_hours}:{_minutes}'


async def generate_stepline_chart(event_list: []):
    # prepare data
    # y = [0.5, 1.5, 2.5, 3.5, 0.5, 1.5, 2.5, 3.5, 0.5, 1.5, 2.5, 3.5, 0.5, 1.5, 2.5, 3.5, 0.5, 1.5, 2.5, 3.5, 0.5, 1.5,
    #      2.5, 3.5]
    # x = [i * 60 for i in np.arange(len(y))]
    data = StepLineData(event_list).prepare_data()
    x, y = data.x, data.y

    ON_time = "24:00"
    D_time = "24:00"
    SB_time = "24:00"
    OFF_time = "24:00"
    total_time = D_time

    # Plotting
    fig, ax1 = plt.subplots(figsize=(12, 2))

    ax1.step(x, y)
    ax1.plot(x, y, 'C0o', alpha=0.5, color='red')
    ax1.set_yticks(np.arange(0, 4.1, 0.5))
    ax1.xaxis.set_major_locator(ticker.LinearLocator(0))
    ax1.set_yticklabels(["", "OFF", "", "SB", "", "D", "", "ON", ""])
    ax1.xaxis.grid(True)
    ax1.set_xlim(-60 / 3, 1440 + 60 / 3)

    ax2 = ax1.twinx()
    ax2.set_yticks(np.arange(0, 4.1, 1))
    ax2.set_yticklabels([''] * 5)
    ax2.xaxis.set_minor_locator(ticker.MultipleLocator(60 / 3))
    ax2.xaxis.set_major_locator(ticker.MultipleLocator(60))
    ax2.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: int(x / 60)))
    ax2.grid(True, axis='both', which='both')

    ax3 = ax1.twinx()
    ax3.set_yticks(np.arange(0, 4.1, 0.5))
    ax3.set_yticklabels([data.total_time, data.ON_time, "", data.D_time, "", data.SB_time, "", data.OFF_time, ""])

    # plt.show()
    # plt.savefig('main.png')
    img_data = io.BytesIO()
    plt.savefig(img_data, format='png')
    img_data.seek(0)
    return img_data
