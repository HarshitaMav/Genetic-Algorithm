import os
import sklearn
from sklearn.tree import _tree
from warnings import warn
from sklearn import tree
import pydotplus
from sklearn.externals.six import StringIO
import numpy as np
import pandas as pd

from rule import Rule

# 2018.10.14 Created by Eamon.Zhang
# 2018.10.15 Add rule filtering function, which allows future functions such as prediction based on selected sets of rules
# 2018.10.15 Issue: DataFrame.Query has a max length limit of 32 to the query string, see https://github.com/PyTables/PyTables/issues/286. 
#            will raise error if rules have >32 conditiions. Unsovlebale yet.
# 2018.10.28 Add tree visualize function. Output the tree structure to images.
# 2018.12.15 fix bug on calculating precision on class 0
# 2018.12.15 add rule voting


# 2018.10.28  Visualize a decision tree or trees from ensembles
def draw_tree(model,outdir,feature_names=None,proportion=True,class_names=['0','1']):

    # if input model is a single decision tree/classifier
    if isinstance(model,(sklearn.tree.tree.DecisionTreeClassifier,sklearn.tree.tree.DecisionTreeRegressor)):
        dot_data = StringIO()
        tree.export_graphviz(decision_tree=model,
                             out_file=dot_data,
                             filled=True,
                             rounded=True,
                             special_characters=True,
                             feature_names=feature_names,
                             proportion=proportion,
                             class_names=class_names)
    
        graph = pydotplus.graph_from_dot_data(dot_data.getvalue())
        # print(graph)
        outfile = os.path.join(outdir,'DecisionTree.jpeg')
        graph.write_jpeg(outfile)
    
    # if input model is a tree ensemble
    elif isinstance(model,(sklearn.ensemble.bagging.BaggingClassifier,
                           sklearn.ensemble.bagging.BaggingRegressor,
                           sklearn.ensemble.forest.RandomForestClassifier,
                           sklearn.ensemble.forest.RandomForestRegressor,
                           sklearn.ensemble.forest.ExtraTreesClassifier,
                           sklearn.ensemble.forest.ExtraTreeRegressor)):
        i = 0
        # visulaize each tree from the whole ensemble
        for estimator in model.estimators_:
            i += 1
            dot_data = StringIO()
            tree.export_graphviz(decision_tree=estimator,
                             out_file=dot_data,
                             filled=True,
                             rounded=True,
                             special_characters=True,
                             feature_names=feature_names,
                             proportion=proportion,
                             class_names=class_names)
    
            graph = pydotplus.graph_from_dot_data(dot_data.getvalue())
            #print(graph)
            outfile = os.path.join(outdir,'EnsembleTrees_No%s.jpeg' % str(i))
            graph.write_jpeg(outfile)
    else:
        raise ValueError('Unsupported model type!')
        return
        

# 2018.10.15 rule extraction from a tree model with filtering criterions based on recall/precision on a given dataset
# 2018.10.30 allow extract all paths of a tree with no filtering
def rule_extract(model, feature_names, x_test=None, y_test=None, sort_key=0, recall_min_c1=0., precision_min_c1=0., recall_min_c0=0., precision_min_c0=0.):    
    rules_dict = {}
    rules_ = []  
    #feature_names = feature_names if feature_names is not None
    #                      else ['X' + x for x in np.arange(X.shape[1]).astype(str)]
    
    # if input model is a single decision tree/classifier
    if isinstance(model,(sklearn.tree.tree.DecisionTreeClassifier,sklearn.tree.tree.DecisionTreeRegressor)):
        rules_from_tree = _tree_to_rules(model,feature_names)
    
        # if no test data is given, return the rules
        if x_test is None:          
            rules_ = [(r) for r in set(rules_from_tree)]
            return rules_, rules_dict
        # if test data is given, filter the rules based on precision/recall
        else:
            rules_from_tree = [(r, _eval_rule_perf(r, x_test, y_test)) for r in set(rules_from_tree)]
            rules_ = rules_from_tree
            
            rules_dict = _rule_filter(rules_,rules_dict, recall_min_c1, precision_min_c1, recall_min_c0, precision_min_c0)
                
            rules_dict = sorted(rules_dict.items(),
                                key=lambda x: (x[1][sort_key]), reverse=True)   
            rules_= [i[0] for i in rules_dict]
            return rules_, rules_dict
        
    elif isinstance(model,(sklearn.ensemble.bagging.BaggingClassifier,
                           sklearn.ensemble.bagging.BaggingRegressor,
                           sklearn.ensemble.forest.RandomForestClassifier,
                           sklearn.ensemble.forest.RandomForestRegressor,
                           sklearn.ensemble.forest.ExtraTreesClassifier,
                           sklearn.ensemble.forest.ExtraTreeRegressor)):
        if x_test is None: 
            for estimator in model.estimators_:
                rules_from_tree = _tree_to_rules(estimator,feature_names)
                rules_from_tree = [(r) for r in set(rules_from_tree)]
                rules_ += rules_from_tree
            return rules_, rules_dict
        else:
            for estimator in model.estimators_:
                rules_from_tree = _tree_to_rules(estimator,feature_names)
                rules_from_tree = [(r, _eval_rule_perf(r, x_test, y_test)) for r in set(rules_from_tree)]
                rules_ += rules_from_tree
               
            rules_dict = _rule_filter(rules_, rules_dict, recall_min_c1, precision_min_c1, recall_min_c0, precision_min_c0)
                
            rules_dict = sorted(rules_dict.items(),
                                 key=lambda x: (x[1][sort_key]), reverse=True)  
            rules_= [i[0] for i in rules_dict]
            return rules_, rules_dict 
    
    else:
        raise ValueError('Unsupported model type!')
        return


def _rule_filter(rules_,rules_dict,recall_min_c1,precision_min_c1,recall_min_c0,precision_min_c0):
    # Factorize rules before semantic tree filtering
    rules_ = [
        tuple(rule)
        for rule in
        [Rule(r, args=args) for r, args in rules_]]
    
    for rule, score in rules_:
        if score[0] >= recall_min_c1 and score[1] >= precision_min_c1 and score[2]>=recall_min_c0 and score[3]>=precision_min_c0:

            if rule in rules_dict:
                # update the score to the new mean
                # Moving Average Calculation
                e = rules_dict[rule][4] + 1  # counter
                d = rules_dict[rule][3] + 1. / e * (
                    score[3] - rules_dict[rule][3])
                c = rules_dict[rule][2] + 1. / e * (
                    score[2] - rules_dict[rule][2])          
                b = rules_dict[rule][1] + 1. / e * (
                    score[1] - rules_dict[rule][1])
                a = rules_dict[rule][0] + 1. / e * (
                    score[0] - rules_dict[rule][0])

                rules_dict[rule] = (a, b, c, d, e)
            else:
                rules_dict[rule] = (score[0], score[1], score[2], score[3], 1)
                
    return rules_dict

def _eval_rule_perf(rule, X, y):
    detected_index = list(X.query(rule).index)
    if len(detected_index) <= 0:
        warn("rule %s reach no samples" % str(rule))
        return (0.,0.,0.,0.)
    
    y_detected = y[detected_index]
    true_pos = y_detected[y_detected > 0].count()
    false_pos = y_detected[y_detected == 0].count()

    pos = y[y > 0].count()
    neg = y[y == 0].count()
    recall_0 = (1- (float(false_pos) /neg))
    prec_0 = ((neg-false_pos) / (len(y)-y_detected.sum()-false_pos))
    recall_1 = (float(true_pos) / pos)
    prec_1 = (y_detected.mean())
    return recall_1, prec_1, recall_0, prec_0
  
def _tree_to_rules(tree, feature_names):
    tree_ = tree.tree_
    feature_name = [
        feature_names[i] if i != _tree.TREE_UNDEFINED else "undefined!"
        for i in tree_.feature]
    rules = []

    def recurse(node, base_name):
        if tree_.feature[node] != _tree.TREE_UNDEFINED:
            name = feature_name[node]
            symbol = '<='
            symbol2 = '>'
            threshold = tree_.threshold[node]
            text = base_name + ["{} {} {}".format(name, symbol, threshold)]
            recurse(tree_.children_left[node], text)

            text = base_name + ["{} {} {}".format(name, symbol2,
                                                  threshold)]
            recurse(tree_.children_right[node], text)
        else:
            rule = str.join(' and ', base_name)
            rule = (rule if rule != ''
                    else ' == '.join([feature_names[0]] * 2))
            rules.append(rule)

    recurse(0, [])

    return rules if len(rules) > 0 else 'True'

def rules_vote(X,rules):
    scores = np.zeros(X.shape[0])
    for r in rules:
        scores[list(X.query(r).index)] +=1
    scores=pd.DataFrame(scores)

    return scores