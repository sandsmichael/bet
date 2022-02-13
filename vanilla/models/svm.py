# svm classification of win or loss

from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np



    # df = pd.read_csv("/Users/michaelsands/code/vanilla/vanilla/vendors/tennisabstract/tennis_atp/atp_matches_2021.csv")
    # # print(df.columns)
    # # print(df.head())

    # features = ['surface', 'winner_hand','winner_ht','winner_age', 'loser_hand',
    #        'loser_ht', 'loser_age', 'w_ace', 'w_df', 'w_svpt', 'w_1stIn', 'w_1stWon', 'w_2ndWon',
    #        'w_SvGms', 'w_bpSaved', 'w_bpFaced', 'l_ace', 'l_df', 'l_svpt',
    #        'l_1stIn', 'l_1stWon', 'l_2ndWon', 'l_SvGms', 'l_bpSaved', 'l_bpFaced',
    #        'winner_rank','loser_rank', 'score']

    # df = df[features].dropna(how='any', axis=0)


    # X = df[features]
    # X.drop('score', axis=1, inplace=True)
    # nonnumerics = X.select_dtypes(include=['object']) 
    # dummies = pd.get_dummies(nonnumerics)
    # X.drop(nonnumerics.columns, axis=1, inplace=True)
    # xx = pd.merge(
    #     left=X,
    #     right=dummies,
    #     left_index=True,
    #     right_index=True,
    # )


    # y = df['score']





# X_train, X_test, y_train, y_test = train_test_split(xx, df.score, test_size=0.3,random_state=109) # 70% training and 30% test


# #Import svm model
# from sklearn import svm

# #Create a svm Classifier
# clf = svm.SVC(kernel='linear') # Linear Kernel

# #Train the model using the training sets
# clf.fit(X_train, y_train)

# #Predict the response for test dataset
# y_pred = clf.predict(X_test)

# #Import scikit-learn metrics module for accuracy calculation
# from sklearn import metrics

# # Model Accuracy: how often is the classifier correct?
# print("Accuracy:",metrics.accuracy_score(y_test, y_pred))

# # Model Precision: what percentage of positive tuples are labeled as such?
# print("Precision:",metrics.precision_score(y_test, y_pred))

# # Model Recall: what percentage of positive tuples are labelled as such?
# print("Recall:",metrics.recall_score(y_test, y_pred))