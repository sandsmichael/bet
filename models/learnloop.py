import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.linear_model import LogisticRegression
from sklearn import svm
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import cross_val_score
import pydotplus
from sklearn import tree
# from sklearn.exceptions import ConvergenceWarning
# from sklearn.utils.testing import ignore_warnings

# @ignore_warnings(category=ConvergenceWarning)
def learn(df):
    """ Iterate through ml models to find the best one for a given dataset
        Assumes non numeric data is already encodeds
    """
    df = df.dropna(how='any', axis=0)
    dep_vars = ['p1_result','p2_result']
    results = df[dep_vars]

    df = df[[
    'p1_result','p2_result',
    'p1_hand', 'p1_rank','p1_ht', 'p1_ace','p1_svpt', 'p1_1stIn', 'p1_1stWon', 'p1_2ndWon', 'p1_SvGms', 'p1_bpSaved', 'p1_bpFaced', 
    'p2_hand','p2_rank', 'p2_ht', 'p2_ace', 'p2_svpt', 'p2_1stIn', 'p2_1stWon', 'p2_2ndWon', 'p2_SvGms', 'p2_bpSaved', 'p2_bpFaced'
    ]]
    features = [c for c in df.columns if c not in dep_vars]

    X = df[features]        # independent variables  
    y = df['p1_result']     # dependant variable

    X_train, X_test, y_train, y_test = train_test_split(X, df.p1_result, test_size=0.3,random_state=11) # 70% training and 30% test

    models = [LogisticRegression(random_state=100),  svm.SVC(kernel='linear'), KNeighborsClassifier(n_neighbors=3), DecisionTreeClassifier() ]

    
    for model in models:

        print(f'*** {model} ***')

        clf = model.fit(X_train.values, y_train.values)

        yhat = clf.predict(X_test.values)

        print("Accuracy:",metrics.accuracy_score(y_test, yhat)) #  Model Accuracy: how often is the classifier correct?
        print("Precision:",metrics.precision_score(y_test, yhat))  # Model Precision: what percentage of positive tuples are labeled as such?
        print("Recall:",metrics.recall_score(y_test, yhat)) # Model Recall: what percentage of positive tuples are labelled as such?

        # if isinstance(model, DecisionTreeClassifier):
        #     scores = cross_val_score(estimator=clf, X=X_test, y=y_test, cv=10)
        #     # print(scores)
        #     data = tree.export_graphviz(clf, out_file=None, feature_names=X_test.columns)
        #     graph = pydotplus.graph_from_dot_data(data)
        #     # print(graph)
        #     graph.write_png('models/mydecisiontree.png')

        ypred = clf.predict(X_test.iloc[0].values.reshape(1, -1))
        print(f'predit: {ypred}')    

        print('')

    match_data = pd.DataFrame(X_test.iloc[0]).transpose()
    print('actuals:')
    print(match_data)
    print(results.iloc[match_data.index.values[0]])
