import csv
import numpy as np
csvRFile		=	open('urlMetrics.csv','r')
reader			=	csv.reader(csvRFile)

met=[]
for row in reader:
	try:
		print(list(map(float,row[2:])))
		met.append([1.0]+list(map(float,row[2:])))
	except:
		pass
csvRFile.close()
X=np.asarray(met)
X1=X-np.mean(X,axis=0)
X2=X1/np.std(X,axis=0)
print(X2)
np.savetxt("data_X.csv", X2, delimiter=",",header='bias,p1,p2,p3,p4,p5,p6,p7,p8,p9,p10,p11,p12,p13',comments='')
