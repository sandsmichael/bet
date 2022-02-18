import pandas as pd
import numpy as np
import sys, os
import random

# pd.set_option('display.max_rows', 8)
pd.set_option('display.max_columns', 12)
pd.set_option('display.width', 1000)
# pd.set_option('display.expand_frame_repr', False)




class HistoricalMatchStats():

    def __init__(self, fname):

        fp = os.path.join("/Users/michaelsands/code/vanilla/vanilla/vendors/tennisabstract/tennis_atp/", fname)
        self.df = pd.read_csv(fp)

        self.cols = [ 
            'winner_hand', 'winner_rank',  'winner_ht','w_ace', 'w_df', 'w_svpt', 'w_1stIn', 'w_1stWon', 'w_2ndWon','w_SvGms', 'w_bpSaved', 'w_bpFaced', 
            'loser_hand','loser_rank', 'loser_ht', 'l_ace', 'l_df', 'l_svpt', 'l_1stIn', 'l_1stWon', 'l_2ndWon', 'l_SvGms', 'l_bpSaved', 'l_bpFaced',
            'surface', 'score', 'match_num', 'tourney_name'
             ]   

        print(self.df.columns)

    def one_hot_encoding(self, df):
        non_numerics = df.select_dtypes(include=['object']) 
        dummies = pd.get_dummies(non_numerics)    # one hot encoding
        df.drop(non_numerics.columns, axis=1, inplace=True)
        return pd.merge( left=df, right=dummies, left_index=True,right_index=True,)
    
    def cat_encoding(self, df):
        non_numerics = df.select_dtypes(include=['object']) 
        for c in non_numerics.columns:
            df[c] = df[c].astype('category').cat.codes
        return df

    def winner_loser_split(self, df):
        winner = df.loc[:, 'winner_hand':'w_bpFaced'].merge(df[['match_num', 'tourney_name']], left_index=True, right_index=True) 
        winner['result'] = 1
        loser = df.loc[:, 'loser_hand':'l_bpFaced'].merge(df[['match_num', 'tourney_name']], left_index=True, right_index=True) 
        loser['result'] = 0 
        idcols = df[['surface', 'score', 'match_num', 'tourney_name']]
        return winner, loser

    def winner_loser_rename(self, dfx, dfy):
        wl_cols = ['hand', 'rank',  'ht','ace', 'df', 'svpt', '1stIn', '1stWon', '2ndWon','SvGms', 'bpSaved', 'bpFaced', 'match_num', 'tourney_name','result']
        dfs = [dfx, dfy]
        for i, df in enumerate(dfs):
            df.columns = ['p' + str(i+1) +'_' + c for c in   wl_cols]
            df.rename(columns={'p1_match_num':'match_num', 'p2_match_num':'match_num', 'p1_tourney_name':'tourney_name', 'p2_tourney_name':'tourney_name'}, inplace=True)
            df.set_index('match_num', inplace=True)
        df = pd.merge(dfx, dfy, on=['tourney_name', 'match_num'], how = 'inner')
        df.reset_index(inplace=True)
        return df
    
    def winner_loser_shuffle(self, df):
        '''
        swap player 1 and player 2 stats for a given match to interchange the winner and looser stats
            in the raw data, player 1 is the winner and player 2 is the looser.
            take a random sample of rows and swap all p1 data with p2 data in each column
        '''
        _df = df.copy()
        randomlist = random.sample(range(0, len(df)),  int(0.5*len(df))) # random sample of row numbers

        p1cols = [c for c in df.columns if c.startswith('p1_')]
        p2cols = [c for c in df.columns if c.startswith('p2_')]
        for  c1,c2 in zip(p1cols, p2cols):
            _df[c1].loc[_df.index.isin(randomlist)] = df[c1.replace('p1_', 'p2_')].loc[_df.index.isin(randomlist)]
            _df[c2].loc[_df.index.isin(randomlist)] = df[c2.replace('p2_', 'p1_')].loc[_df.index.isin(randomlist)]

        # print(_df[['p1_result', 'p2_result']].value_counts())
        return _df[ ['match_num', 'tourney_name',  'p1_result', 'p2_result'] + [ col for col in _df.columns if col not in ['match_num', 'tourney_name',  'p1_result', 'p2_result'] ] ]

    def pre_process(self, cols):
        df = self.df[cols].dropna(how='any', axis=0)#.drop(columns = 'score')
        df = self.cat_encoding(df)
        return df

    def player_match_rows(self):
        '''
        each row contains data for both players in the match, the winner and looser. 
            winner and looser stats columns are renamed to player 1 and player 2 and shuffled
            a result column is appended for use as a dependent variable
        Use projected match stat pobabilities to test which player will wi/how many sets based on fit model.

        Use: knn/clustering for similar matches based upon player stats
        Use: subset data for a specific player id and predict his result against opponents who have similar stats to otheers players p1 has played
        i.e. Hoew like is P1 to win when playing an opponent who wins X% of 1st serves and converts on y% of break point opportunities
        '''
        cols = self.cols
        df = self.pre_process(cols)
        winner, loser = self.winner_loser_split(df)
        return self.winner_loser_shuffle(self.winner_loser_rename(winner, loser))


    def result_rows(self):
        '''
        transform the dataframe to show individual rows for winner and looser with an additional field called 'Result'
        for binary classification problems (result = win or loss)

        Use: logistic regression / prediction of win/loss
        Use win_probabilities to project p1 and p2 stats for a giveen match and predict if those stats will result in a win or loss
        '''
        pass


    def player_subset(self):
        '''
        subseet the data file to include only rows for a specific pla
        '''
        cols = self.cols + ['winner_name', 'loser_name', 'winner_id', 'loser_id']

        pass