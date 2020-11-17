import numpy as np
import matplotlib.pyplot as plt


fig, axs =plt.subplots(2,1)
clust_data = np.random.random((10,3))
collabel=("col 1", "col 2", "col 3")
axs[0].axis('tight')
axs[0].axis('off')
the_table = axs[0].table(cellText=clust_data,colLabels=collabel,loc='center')

axs[1].plot(clust_data[:,0],clust_data[:,1])
# fig.tight_layout()
# fig.show()

plt.suptitle("Subtitle", fontsize=18)
axs[0].set_title('subplot 1', pad=20)

plt.subplots_adjust(left=1, bottom=1, right=1)
# plt.autoscale(enable=True)
plt.show()
# plt.savefig("image.png",bbox_inches='tight',dpi=100)