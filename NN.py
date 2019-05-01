from keras.models import Sequential
from keras.layers import Dense
from sklearn.model_selection import train_test_split
import numpy as np
from numpy import genfromtxt

# fix random seed for reproducibility
np.random.seed(7)
# load pima indians dataset
X 	= genfromtxt('data_X.csv', delimiter=',',skip_header=1)
Y	= genfromtxt('data_Y.csv', delimiter=',',skip_header=1)
# create model
X_train,X_test,Y_train,Y_test = train_test_split(X,Y,test_size=0.33)

model = Sequential()
model.add(Dense(16, input_dim=12, activation='relu'))
model.add(Dense(12, activation='relu'))
model.add(Dense(1, activation='sigmoid'))
# Compile model
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
# Fit the model
model.fit(X_train, Y_train, epochs=5, batch_size=10, verbose=2)
# evaluate the model
scores = model.evaluate(X_test, Y_test)
print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))

predictions=model.predict(X_test)
dev=0.0
n=33
for i in range(n):
	dev+=abs(Y_test[i]-predictions[i])
	print(Y[i],predictions[i])
print("average deviation",dev/n)
print(X_test)
model.predict([])
