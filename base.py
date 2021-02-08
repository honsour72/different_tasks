from Stars import n
# # import main_app
# import UnAffine
# import Detection
from Orintation_2 import orientation_2
import numpy as np

m = n
print("m = \n", m, "\n")
q = orientation_2()
print("q = \n", q)

a = (m - q).T @ (m - q)
print(a.trace()**0.5)

