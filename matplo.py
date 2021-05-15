import matplotlib.pyplot as plt
import numpy as np
print("hi")
x=np.array([1,2,3,4])
y=np.array([1,4,9,16])
plt.plot(x,y)
plt.xlabel('x')
plt.ylabel('x square')
plt.title('square function')
plt.grid(True)
plt.savefig("test.png")
print(type(plt))
plt.show()