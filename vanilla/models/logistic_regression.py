from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
import pandas as pd 
import datasist


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


y = df['score']


from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
clf = LogisticRegression(random_state=0).fit(X, y)


x = clf.predict(X.iloc[:1, :])
print(x)
# clf.predict_proba(X[:2, :])


x = clf.score(X, y)
print(x)