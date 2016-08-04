"""

    Temporary python file to document ideas on class framework

"""
import pandas as pd
import numpy as np


class Strategy:
    """
    A framework for evaluating betting decisions given the observed data and the outcomes.
    """
    def __init__(self):
        pass

    def score(self, features):
        """
        Score bet(s) given a set of features.

        :param features: pd.DataFrame, indexed by bet name
        :return: two pandas objects indexed by the name of the bet
            pd.Series(str)  (e.g. 'Home' where 'Home' is what side of the bet)
            pd.DataFrame(str, float)  (e.g. ('Home', 100), where 100 is a wager)
        """
        # insert decisioning logic off of features here
        pass

    def backtest(self, features, outcomes, retro_fit=None):
        """
        Backtest bet(s) with a given set of features vs a given set of outcomes.

        :param features: pd.DataFrame, indexed by bet name
        :param outcomes: pd.DataFrame, indexed by bet name with columns
            outcome, a str of what actually happened  (e.g. 'Over')
            return, a float for the return on correctly guessing the outcome
            bet_date, a pd.Datetime64 for when the bet took place
        :param retro_fit: pd.Datetime64, default None, which if a fit function needs to be called, will be called
            starting at retro_fit, and fit will be called every day thereafter (may want to add param to change freq);
            requires that the features and outcomes are indexed by the same index
        :return: pd.DataFrame, indexed by bet name with columns
            amount, a float for amount won / lost
            bet_date, a pd.Datetime64 for when the bet took place
        """
        # PSEUDO-CODE
        #
        # if retro_fit is not None:
        #   self.fit(features.loc[outcomes['bet_date'] < retro_fit], outcomes.loc[outcomes['bet_date'] < retro_fit])
        #   for retro_fit to max(outcomes['bet_date']:
        #       bets, wagers = score(features.loc[outcomes['bet_date'] == retro_fit])
        #       winnings = self._get_winnings(outcomes.loc[outcomes['bet_date'] == retro_fit, 'outcome'],
        #                                     bets, wagers)
        #
        # else:
        #   bets, wagers = self.score(features)
        #   winnings = self._get_winnings(outcomes['outcome'], bets, wagers)
        #
        # return winnings
        pass

    def _get_winnings(self, outcomes, bets, wagers):
        """
        For a set of bets and wagers, check them against the outcome and return earnings.

        :param outcomes: pd.Series
        :param bets: pd.Series
        :param wagers: pd.Series
        :return: pd.Series
        """
        # PSEUDO-CODE
        #
        #   for i in range(len(bets)):
        #       if bets[i] is the same as outcomes['outcome'].iloc[i],
        #       then win wagers[i] * outcomes['return'].iloc[i]
        #       else loss wagers[i]
        pass

    def fit(self, features, outcomes=None):
        """
        Used if score method requires a fitted model.
        Fitted model could be
            - a set of rules that need to be updated based on _features only_
            - a classifier that needs features and outcomes to be fit

        :param features: pd.DataFrame
        :param outcomes: pd.DataFrame, default None
        """
        # self.decisioner_ = SomeDecisionObject
        # self.decisioner_.fit(features, outcomes) if outcomes is not None else self.decisioner_.fit(features)
        pass


class MajorityRules(Strategy):
    """
    Strategy specific for betting against where the majority of bets are taken on moneylines.
    """
    def __init__(self):
        self.decisioner_ = object()  # should be something like SplitWagersEvenly
        super(MajorityRules, self).__init__()

    def score(self, features):
        """

        :param features:
        :return:
        """
        home_diff = features['home_wagers'].subtract(features['away_wagers'])
        bets = pd.Series(['Home' if x == 1 else 'Away' for x in home_diff > 0],
                         index=features.index)

        if self.decisioner_ is None:
            wagers = pd.Series([1] * len(bets), index=features.index)
        else:
            # for example, MajorityRules could determine wager based on date and total
            # number of bets taken that day
            wagers = self.decisioner_.place_wagers(features['bet_date'])
