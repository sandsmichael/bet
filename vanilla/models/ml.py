# run multiple models and return the most accurate model



def learn(df):
    """[Summary]
        Assumes non numeric data is already encodeds

    :param [ParamName]: [ParamDescription], defaults to [DefaultParamVal]
    :type [ParamName]: [ParamType](, optional)
    ...
    :raises [ErrorType]: [ErrorDescription]
    ...
    :return: [ReturnDescription]
    :rtype: [ReturnType]
    """
    df = df.dropna(how='any', axis=0)

    dep_vars = ['p1_result','p2_result', 'score']
    features = [c for c in df.columns if c not in dep_vars]

    _df = df[features]

    # independent variables
    X = _df[features]        # X.drop(dep_vars, axis=1, inplace=True)

    # dependant variable
    y = df['p1_result']


    # match data
    yhat_match_num = X.loc[:0, :'match_num']
    print(yhat_match_num)
    print(X.iloc[:1, :].to_dict())

    from sklearn.linear_model import LogisticRegression
    clf = LogisticRegression(random_state=0).fit(X, y)

    yhat = clf.predict(X.iloc[:1, :])
    print(yhat)

    yhat = clf.predict_proba(X.iloc[:1, :])
    print(yhat)

    acc = clf.score(X, y)
    print(acc)




def find_best_model(df):
    pass