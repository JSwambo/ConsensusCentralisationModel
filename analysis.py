import pandas as pd
import os
import matplotlib.pyplot as plt
from utils import lengths


class Analysis():
    def __init__(self):

        dir_path = os.path.dirname(os.path.realpath(__file__))
        self.sim_root_path = dir_path + '/SimData'
        if not os.path.exists(self.sim_root_path):
            os.makedirs(self.sim_root_path)

    def get_size_dist_series(self, T, num_miners):
        path = self.sim_root_path + \
            "/size_distribution_series_T-%d_M-%d.txt" % (T, num_miners)
        if not os.path.exists(path):
            print "Could not find file at path: %s" % (path)
        else:
            df = pd.read_csv(path)
            return df

    def clean_data(self, T, num_miners):
        df = self.get_size_dist_series(T, num_miners)

        # relabel dataframe:
        columns = [str(i) for i in range(-1, df.shape[1] - 1)]
        columns[0] = 'Time'
        df.columns = columns

        # starting from the final column, remove all columns without data (whose values are all 0)
        order = range(0, df.shape[1] - 1)
        order.reverse()

        for i in order:
                # if there are 0 counts at each time step, remove the unnecessary data column
            if list(df[str(i)]) == [0.0 for j in range(len(df[str(i)]))]:
                df.drop(labels=[str(i)], axis=1, inplace=True)
            else:
                break

        return df

    def plot_size_dist_series(self, T, num_miners):
        df = self.clean_data(T, num_miners)
        plt.xlabel("Time, $t$")
        plt.ylabel("Number of members in pool, $n$")
        df.drop(labels=['Time'], axis=1, inplace=True)
        for i in range(0, df.shape[1]):
            df[str(i)].plot(label="pool size: %i" % (i))
        plt.legend()
        plt.show()
