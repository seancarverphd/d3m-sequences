import itertools
import numpy as np
import pandas as pd
import pickle
import statsmodels.api as sm
import statsmodels.formula.api as smf

with open("single_problem_data.pickle", "rb") as f:
    single_problems = pickle.load(f)

def define_sp(inp=None):
    if inp is not None:
        with open(inp, "rb") as f:
            sp = pickle.load(f)
    else:
        sp = single_problems
    return sp

def lpnorm(prob=0, p=1, normalize=False, inp=None):  # None loads: single_problem_data.pickle
    sp = define_sp(inp)
    df = sp[prob]['pairs']
    repeated_performers = df[df.performers0 == df.performers1]
    if len(repeated_performers) == 0:
        print("lp_norm: No performer had more than one pipeline.")
        return None
    grouped_performers = repeated_performers.groupby('performers0')
    if p == 0 and normalize:
        return grouped_performers.apply(lambda dfr: (sum(dfr.distance!=0)/len(dfr.distance))).sort_values(ascending=False)
    elif p == np.Inf and normalize:
        return grouped_performers.apply(lambda dfr: (max(dfr.distance)/len(dfr.distance))).sort_values(ascending=False)
    elif normalize and p!=0:
        return grouped_performers.apply(lambda dfr: (sum(dfr.distance**p))**(1/p)/len(dfr.distance)).sort_values(ascending=False)
    elif p == np.Inf:
        return grouped_performers.apply(lambda dfr: (max(dfr.distance))).sort_values(ascending=False)
    elif p == 0:
        return grouped_performers.apply(lambda dfr: (sum(dfr.distance!=0))).sort_values(ascending=False) 
    else:
        return grouped_performers.apply(lambda dfr: (sum(dfr.distance**p))**(1/p)).sort_values(ascending=False)

def count_pipelines(prob=0, inp="single_problem_data.pickle"):
    sp = define_sp(inp)
    df = pd.DataFrame({'performer': sp[prob]['performers']})
    return df.groupby('performer').size()

def count_problems(inp="single_problem_data.pickle"):
    sp = define_sp(inp)
    return len(sp)

def max_score(prob=0):
    sp = define_sp(None)
    df = pd.DataFrame({"performer": sp[prob]['performers'], "adjusted_score": sp[prob]['adjusted_scores']})
    return df.groupby('performer').max().sort_values('adjusted_score', ascending=False)

def multimeasure(prob=0):
    common_index = set()
    l1 = pd.DataFrame(lpnorm(prob=prob, p=1))
    if len(l1) == 0:
        return None
    l1.columns = ['l1']
    l2 = pd.DataFrame(lpnorm(prob=prob, p=2))
    if len(l2) == 0:
        return None
    l2.columns = ['l2']
    linf = pd.DataFrame(lpnorm(prob=prob, p=np.inf))
    if len(linf) == 0:
        return None
    linf.columns = ['linf']
    maxs = pd.DataFrame(max_score(prob=prob))
    if len(maxs) == 0:
        return None
    maxs.columns = ['max_score']
    count = pd.DataFrame(count_pipelines(prob=prob, inp=None))
    if len(count) == 0:
        return None
    count.columns = ['count']
    multi = pd.DataFrame(l1).join(pd.DataFrame(l2),how='inner').join(pd.DataFrame(linf),how='inner').join(pd.DataFrame(maxs),how='inner').join(pd.DataFrame(count),how='inner')
    multi = multi.assign(prob_num=prob)
    multi = multi.assign(prob_name=problem_name(prob=prob))
    multi = multi.assign(keywords=problem_keywords(prob=prob))
    multi = multi.assign(ranking=multi.max_score.rank(method='dense', ascending=False))
    multi = multi.assign(best=multi.ranking==1)
    return multi

def multizscore(prob=0):
    df = multimeasure(prob=prob)
    if df is None:
        return None
    cols = list(df.columns)
    cols.remove('prob_num')  # These statements remove from list for creating z-scores.  Columns stay in dataframe df.
    cols.remove('prob_name')
    cols.remove('keywords')
    cols.remove('ranking')
    cols.remove('best')
    for col in cols:
        col_zscore = col + '_zscore'
        df[col_zscore] = (df[col] - df[col].mean())/df[col].std(ddof=0)
    return df

def problem_name(prob=0):
    return single_problems[prob]['type']

def problem_keywords(prob=0):
    return single_problems[prob]['keywords']

def problem_performers(prob=0):
    return list(set(single_problems[prob]['performers']))

def all_keywords():
    all_kw = [problem_keywords(prob) for prob in range(count_problems())]
    unique_kw = list(set(all_kw))
    return unique_kw

def adjusted_metric(prob=0):
    return single_problems[prob]['adjusted_metric'][0]

def problem_has_keywords(prob, desired_keywords_string, default_if_none=True):  # returns logical; elsewhere summing/counting True's
    if desired_keywords_string is None:
        return default_if_none
    actual_keywords_set = set(problem_keywords(prob=prob).split(sep=','))
    desired_keywords_set = set(desired_keywords_string.split(sep=','))
    return desired_keywords_set.issubset(actual_keywords_set)

def all_performers():
    all_perf = [problem_performers(prob) for prob in range(count_problems())]
    return list(set(list(itertools.chain.from_iterable(all_perf))))

def had_success(performer, prob):
    return performer in set(problem_performers(prob=prob))

def df_performer_succeeded():
    all_perf = all_performers()
    performer_successes = {}
    for performer in all_perf:
        performer_successes[performer] = [had_success(performer, prob) for prob in range(count_problems())]
    return pd.DataFrame(performer_successes)

original_categories = ['binary_classification', 'clustering', 'collaborative_filtering', 'community_detection', 'graph_matching', 'link_prediction',
        'binary_semisupervised_classification', 'multiclass_semisupervised_classification', 'multiclass_classification',
        'multilabel_classification', 'multivariate_regression', 'object_detection', 'regression', 'time_series',
        'vertex_nomination', 'vertex_classification']

def category_to_keywords():
    return {'binary_classification': 'classification,binary',
            'clustering': None,
            'collaborative_filtering': 'collaborativeFiltering',
            'community_detection': 'communityDetection',
            'graph_matching': 'graphMatching',
            'link_prediction': 'linkPrediction',
            'binary_semisupervised_classification': 'semiSupervised,classification,binary',
            'multiclass_semisupervised_classification': 'semiSupervised,classification,multiClass',
            'multiclass_classification': 'classification,multiClass',
            'multilabel_classification': None,
            'multivariate_regression': 'regression,multivariate',
            'object_detection': 'objectDetection',
            'regression': 'regression,univariate',
            'time_series': 'timeSeries',
            'vertex_nomination': None,
            'vertex_classification': 'vertexClassification'}

def categories():
    return [*category_to_keywords()]

def categories_to_problems():
    prob_in_cat = {}
    for cat, kws in category_to_keywords().items():
        prob_in_cat[cat] = [problem_has_keywords(prob, kws, default_if_none=False) for prob in range(count_problems())]
    return pd.DataFrame(prob_in_cat)

def count_problems_for_each_category():
    return categories_to_problems().sum(axis=0)

def measures_all_probs(min_performers=5, multi=multizscore, keywords=None):
    dfs = []
    for prob in range(count_problems()):
        if problem_has_keywords(prob, keywords, default_if_none=False):
            df = pd.DataFrame(multi(prob)).reset_index()
        else:
            continue
        if len(df) < min_performers:
            continue
        else:
            colnames = list(df.columns)
            colnames[0] = 'performer'
            df.columns = colnames
            dfs.append(df)
    if len(dfs) > 0:
        return pd.concat(dfs).reset_index(drop=True)
    else:
        return None

def bigdf(min_performers=5):
    dfs = []
    for cat, kws in category_to_keywords().items():
        df = measures_all_probs(min_performers=min_performers, multi=multizscore, keywords=kws)
        if df is not None:
            df = df.assign(category=cat)
            dfs.append(df)
    return pd.concat(dfs).reset_index(drop=True)

def meandf(min_performers=5):
    df = bigdf(min_performers=min_performers)
    return df.groupby(['category','performer']).mean()

def rep(n):
    return '*'*int(n)

def sumdf(min_performers=5):
    df = bigdf(min_performers=min_performers)
    dg = df.groupby(['category','performer']).sum()
    return dg.assign(best_string=dg.best.apply(rep))

def kw_regression(min_performers=5, keywords=None):
    df = measures_all_probs(min_performers, multizscore, keywords)
    if df is not None:
        mod = smf.ols(formula = 'max_score_zscore ~ l1_zscore + linf_zscore + count_zscore', data=df)
        res = mod.fit()
        return res
        # return res.summary()
    else:
        return None

def cat_regression(min_performers=5, category=None):
    return kw_regression(min_performers=5, keywords=category_to_keywords()[category])

