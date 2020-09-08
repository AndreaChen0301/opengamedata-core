from typing import List, Optional
import pandas as pd
from bisect import bisect_left
import numpy as np
import json
from datetime import timedelta
from models.FeatureModel import FeatureModel

_POP_ACHS = "exist group town city".split()
_FARM_ACHS = "farmer farmers farmtown megafarm".split()
_MONEY_ACHS = "paycheck thousandair stability riches".split()
_BLOOM_ACHS = "bloom bigbloom hugebloom massivebloom".split()
_REQ_TUTORIALS = "buy_food build_a_farm timewarp \
successful_harvest sell_food buy_fertilizer buy_livestock \
livestock poop rain".split()  # skip build_a_house - it comes at 0.0


def _get_sess_active_time_to_achievement_list(achs):
    return [f'sess_time_active_to_{a}_achievement' for a in achs]


def _get_sess_active_time_to_tutorial_list(tuts):
    return [f'sess_time_active_to_{t}_tutorial' for t in tuts]


def _get_quantiles(df, feats, filter_debug=True, filter_continue=True):
    filter_strings = []
    if filter_debug:
        filter_strings += ['(debug==0)']
    if filter_continue:
        filter_strings += ['(c==0)']
    if filter_strings:
        df = df.rename({"continue": "c"}, axis=1).query(' & '.join(filter_strings)).rename({"c": "continue"}, axis=1)
    df = df[feats].replace(0.0, pd.NA)
    df = df.quantile(np.arange(0, 1, .01))
    quantiles = df.to_dict('list')
    return quantiles


class _FeatureQuantiles(object):

    def __init__(self, arg, filter_continue=True):
        if type(arg) is str:
            json_path = arg
            with open(json_path) as f:
                self._quantiles = json.load(f)
            return

        df = arg
        cols = df.select_dtypes(include="number").columns
        self._quantiles = _get_quantiles(df, cols, filter_continue=filter_continue)

    @classmethod
    def fromDF(cls, df: pd.DataFrame, filter_continue=True) -> 'FeatureQuantiles':
        return cls(df, filter_continue=filter_continue)

    @classmethod
    def fromCSV(cls, csv_path: str, filter_continue=True) -> 'FeatureQuantiles':
        df = pd.read_csv(csv_path, index_col='sessID')
        return cls(df, filter_continue=filter_continue)

    @classmethod
    def fromJSON(cls, quantile_json_path: str) -> 'FeatureQuantiles':
        return cls(quantile_json_path)

    def get_quantile(self, feat: str, value, verbose: bool = False,
                     lo_to_hi: bool = True) -> int:
        quantile = bisect_left(self._quantiles[feat], value)
        if verbose:
            compare_str = "higher" if lo_to_hi else "lower"
            # print(quantile, len(self._quantiles[feat]))
            high_quant = self._quantiles[feat][quantile] if quantile < len(self._quantiles[feat]) else None
            low_quant = self._quantiles[feat][quantile - 1] if quantile > 0 else None
            quantile = quantile if lo_to_hi else 100 - quantile
            low_quant_offset = -1 if lo_to_hi else +1
            quant_low_str = f'{quantile + low_quant_offset}%={low_quant}'
            quant_high_str = f'{quantile}%={high_quant}'
            quant_str = f"{quant_low_str} and {quant_high_str}" if lo_to_hi else f"{quant_high_str} and {quant_low_str}"
            print(
                f'A {feat} of {value} units is {compare_str} than {quantile}% (between {quant_str}) of sessions.')
        return quantile

    def _export_quantiles(self, path):
        with open(path, 'w+') as f:
            json.dump(self._quantiles, f, indent=4)




class FeatSeqPercentModel(FeatureModel):
    def __init__(self, feature_sequence: List[str], levels: List[int] = [], time_feat: str = 'sess_time_active',
                 quantile_json_path: str = "models/lakeland_data/quantiles_no_continue.json"):
        self._feature_sequence = feature_sequence
        self._time_feat = time_feat
        self._featureQuantiles = _FeatureQuantiles.fromJSON(
            no_continue_json_path=quantile_json_path)

        super().__init__()

    def _eval(self, sess: dict, verbose: bool = False) -> Optional[float]:
        if sess['continue'] or sess['debug']:
            return None
        time_to_vals = [sess[f] for f in self._feature_sequence]
        idx_next = sum(bool(v) for v in time_to_vals)
        if idx_next < len(self._feature_sequence):
            next_feat = self._feature_sequence[idx_next]
            cur_time = sess[self._time_feat]
        else:
            next_feat = self._feature_sequence[-1]
            cur_time = time_to_vals[-1]
        if type(cur_time) is timedelta:  # proc features give float, but cgi might give timedelta
            cur_time = cur_time.seconds

        percentile_if_next_feat_now = self._featureQuantiles.get_quantile(next_feat, cur_time, verbose=verbose)

        return percentile_if_next_feat_now


