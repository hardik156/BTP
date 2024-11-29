import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.utils import shuffle

def train_and_evaluate(file_path):
    data = pd.read_csv(file_path, header=None)
    test_data = pd.read_csv("kismet-features.txt", header=None)
    

    data = shuffle(data, random_state=42)
    test_data = shuffle(test_data)
    
    # X = test_data.iloc[:, :-1]  
    # y = test_data.iloc[:, -1]   
    X = data.iloc[:, :-1]
    y = data.iloc[:,-1]
    X_train = X
    y_train = y
    X_test = test_data.iloc[:,:-1]
    y_test = test_data.iloc[:,-1]

    # X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    clf = RandomForestClassifier(random_state=42)
    

    clf.fit(X_train, y_train)
    

    y_pred = clf.predict(X_test)
    

    print(y_pred)
    print(y_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Accuracy on the test set: {accuracy:.2f}")


file_path = "features.txt"  
train_and_evaluate(file_path)
