import pandas as pd
import numpy as np
import sys, os

pd.set_option('display.max_rows', 10)
pd.set_option('display.max_columns', 14)
pd.set_option('display.width', 600)
pd.set_option('display.expand_frame_repr', False)




class HistoricalMatchStats():


    def __init__(self, fname):

        fp = os.path.join("/Users/michaelsands/code/vanilla/vanilla/vendors/tennisabstract/tennis_atp/", fname)
        self.df = pd.read_csv(fp)

        self.cols = [ 'winner_hand', 'loser_hand', 'winner_ht', 'surface','w_ace', 'w_df', 'w_svpt', 'w_1stIn', 'w_1stWon', 'w_2ndWon',
       'w_SvGms', 'w_bpSaved', 'w_bpFaced', 'l_ace', 'l_df', 'l_svpt','loser_ht',
       'l_1stIn', 'l_1stWon', 'l_2ndWon', 'l_SvGms', 'l_bpSaved', 'l_bpFaced',
       'winner_rank', 'loser_rank', 'score']

        print(self.df.columns)


    def one_hot_encoding(self, df):
        non_numerics = df.select_dtypes(include=['object']) 
        dummies = pd.get_dummies(non_numerics)                  # one hot encoding
        df.drop(non_numerics.columns, axis=1, inplace=True)
        return pd.merge( left=df, right=dummies, left_index=True,right_index=True,)
    
    def cat_encoding(self, df):
        non_numerics = df.select_dtypes(include=['object']) 
        for c in non_numerics.columns:
            df[c] = df[c].astype('category').cat.codes
        return df

    def pre_process(self, cols):
        df = self.df[cols].dropna(how='any', axis=0).drop(columns = 'score')
        df = self.cat_encoding(df)
        print(df.columns)
        print(df.shape)
        print(df.head())

    def match_rows(self):
        '''
        each row contains data for both players in the match, the winner and looser. Each row describes complete data for both
        players in the match.
        Use projected match stat pobabilities to test which player will wi/how many sets based on fit model.

        Use: knn/clustering for similar matches based upon player stats
        Use: subset data for a specific player id and predict his result against opponents who have similar stats to otheers players p1 has played
        i.e. Hoew like is P1 to win when playing an opponent who wins X% of 1st serves and converts on y% of break point opportunities
        '''
        cols = self.cols
        df = self.pre_process(cols)




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