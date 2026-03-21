from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
import pickle
import os,sys

# Read the file
#trainingData_path1 = "/Users/harris/MLGame/log1"
#trainingData_path2 = "/Users/harris/MLGame/log2"
index = sys.argv[1]
#print(index)

trainingData_path = "/Users/harris/MLGame/log/data" + index
#trainingData_path = "/Users/harris/MLGame/log" + index
#trainingData_path1 = "/Users/harris/MLGame/log1" 
#trainingData_path2 = "/Users/harris/MLGame/log2" 
#trainingData_path3 = "/Users/harris/MLGame/log3" 
#trainingData_path4 = "/Users/harris/MLGame/log4"
#trainingData_path5 = "/Users/harris/MLGame/log/data16"

# x:data, y:action
data = list()
action = list()

for file in os.listdir(trainingData_path):
    with open(os.path.join(trainingData_path, file), "rb") as f:
        loaded_data = pickle.load(f)
        for Data in loaded_data:
            data.append(Data[:7])
            action.append(Data[7]) ##7 is for frame consideration
  
            
# split data
x_train = data
y_train = action

#x_train, x_test, y_train, y_test = train_test_split(
#    data, action, test_size = 0.5
#)

# model train
model = KNeighborsClassifier(n_neighbors = 1)
model.fit(x_train, y_train)

# store model

save_path = "/Users/harris/MLGame/brickgame/K" + index + "model.pickle"
with open(save_path, "wb") as file:
    pickle.dump(model, file)
    
#modle = pickle.load(file)
#y = model.predict(x)

# model test
"""
testData_path = "/Users/harris/MLGame/log3"
for file in os.listdir(testData_path):
    with open(os.path.join(testData_path, file), "rb") as f:
        loaded_data = pickle.load(f)
        for Data in loaded_data:
            data.append(Data[:6])
            action.append(Data[6])
x_test = data
#print(x_test)
y_test = action
print(y_test)
y_predict = model.predict(x_test)

correct = 0
incorrect = 0
total = len(y_test)
for actual, predict in zip(y_test, y_predict):
    if actual == predict:
        correct += 1
    else:
        incorrect += 1
        
print(f"{correct = }")
print(f"{incorrect = }")
print(f"accuracy = {100 * correct / total}%")
"""
