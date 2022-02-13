
#decision tree

import pandas as pd
from sklearn import tree
import pydotplus
from sklearn.tree import DecisionTreeClassifier
import matplotlib.pyplot as plt
import matplotlib.image as pltimg


df = pd.read_csv("/Users/michaelsands/code/vanilla/vanilla/vendors/tennisabstract/atp_matches_2021.csv")
# print(df.columns)
# print(df.head())

features = ['surface', 'winner_hand','winner_ht','winner_age', 'loser_hand',
       'loser_ht', 'loser_age', 'w_ace', 'w_df', 'w_svpt', 'w_1stIn', 'w_1stWon', 'w_2ndWon',
       'w_SvGms', 'w_bpSaved', 'w_bpFaced', 'l_ace', 'l_df', 'l_svpt',
       'l_1stIn', 'l_1stWon', 'l_2ndWon', 'l_SvGms', 'l_bpSaved', 'l_bpFaced',
       'winner_rank','loser_rank', 'score']

df = df[features].dropna(how='any', axis=0)


X = df[features]
X.drop('score', axis=1, inplace=True)
nonnumerics = X.select_dtypes(include=['object']) 
dummies = pd.get_dummies(nonnumerics)
X.drop(nonnumerics.columns, axis=1, inplace=True)
xx = pd.merge(
    left=X,
    right=dummies,
    left_index=True,
    right_index=True,
)

xxcols = X.columns

y = df['score']

dtree = DecisionTreeClassifier()
dtree = dtree.fit(X, y)
data = tree.export_graphviz(dtree, out_file=None, feature_names=xxcols)
graph = pydotplus.graph_from_dot_data(data)
print(graph)
graph.write_png('mydecisiontree.png')

img=pltimg.imread('mydecisiontree.png')
imgplot = plt.imshow(img)
plt.show()



