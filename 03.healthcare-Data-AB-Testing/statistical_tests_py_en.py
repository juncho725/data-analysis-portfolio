"""
Statistical Testing Utilities
Core statistical functions for healthcare analysis
"""

import pandas as pd
import numpy as np
from scipy import stats
from statsmodels.formula.api import mixedlm
from statsmodels.stats.proportion import proportions_ztest

def mixed_effects_test(data, outcome, group_var, time_var, subject_id):
    """Mixed-Effects Model analysis"""
    formula = f'{outcome} ~ C({group_var}) * {time_var}'
    model = mixedlm(formula, data, groups=data[subject_id])
    results = model.fit()
    
    # Extract key results
    group_params = [p for p in results.params.index if 'C(' in p and ')[T.' in p]
    if group_params:
        coef = results.params[group_params[0]]
        p_val = results.pvalues[group_params[0]]
    else:
        coef, p_val = 0, 1
    
    return {
        'coefficient': coef,
        'p_value': p_val,
        'significant': p_val < 0.05,
        'model': results
    }

def proportion_test(successes, totals):
    """Z-test between two proportions"""
    z_stat, p_val = proportions_ztest(successes, totals)
    
    rates = [s/t for s, t in zip(successes, totals)]
    
    return {
        'z_statistic': z_stat,
        'p_value': p_val,
        'significant': p_val < 0.05,
        'rates': rates,
        'difference': rates[0] - rates[1]
    }

def variance_test(group1, group2):
    """Compare variances using F-test"""
    var1, var2 = np.var(group1, ddof=1), np.var(group2, ddof=1)
    f_stat = var1 / var2 if var1 > var2 else var2 / var1
    
    df1, df2 = len(group1)-1, len(group2)-1
    p_val = 2 * min(stats.f.cdf(f_stat, df1, df2), 1 - stats.f.cdf(f_stat, df1, df2))
    
    return {
        'f_statistic': f_stat,
        'p_value': p_val,
        'significant': p_val < 0.05,
        'variances': [var1, var2]
    }

def welch_ttest(group1, group2):
    """Welch's t-test (no equal variance assumption)"""
    t_stat, p_val = stats.ttest_ind(group1, group2, equal_var=False)
    
    mean1, mean2 = np.mean(group1), np.mean(group2)
    
    return {
        't_statistic': t_stat,
        'p_value': p_val,
        'significant': p_val < 0.05,
        'means': [mean1, mean2],
        'difference': mean1 - mean2
    }

def remove_outliers(data, column, method='iqr', multiplier=1.5):
    """Remove outliers"""
    if method == 'iqr':
        Q1, Q3 = data[column].quantile([0.25, 0.75])
        IQR = Q3 - Q1
        lower, upper = Q1 - multiplier * IQR, Q3 + multiplier * IQR
        return data[data[column].between(lower, upper)]
    else:
        # Z-score method
        z_scores = np.abs(stats.zscore(data[column]))
        return data[z_scores < multiplier]

def cohens_d(group1, group2):
    """Calculate Cohen's d effect size"""
    n1, n2 = len(group1), len(group2)
    pooled_std = np.sqrt(((n1-1)*np.var(group1, ddof=1) + (n2-1)*np.var(group2, ddof=1)) / (n1+n2-2))
    return (np.mean(group1) - np.mean(group2)) / pooled_std

def quick_summary(test_results, test_name):
    """Summary of test results"""
    print(f"\n📊 {test_name} Results:")
    
    if 'coefficient' in test_results:
        print(f"   Effect Size: {test_results['coefficient']:.4f}")
    elif 'difference' in test_results:
        print(f"   Difference: {test_results['difference']:.4f}")
    
    print(f"   p-value: {test_results['p_value']:.4f}")
    print(f"   Significance: {'Significant' if test_results['significant'] else 'Not Significant'}")

# Convenience functions
def analyze_groups(control, treatment, outcome_col, test_type='ttest'):
    """Group comparison analysis"""
    
    if test_type == 'ttest':
        result = welch_ttest(treatment[outcome_col], control[outcome_col])
        result['effect_size'] = cohens_d(treatment[outcome_col], control[outcome_col])
    elif test_type == 'variance':
        result = variance_test(control[outcome_col], treatment[outcome_col])
    
    return result

def preprocess_data(df, date_cols=None, numeric_cols=None):
    """Data preprocessing"""
    if date_cols:
        for col in date_cols:
            df[col] = pd.to_datetime(df[col])
    
    if numeric_cols:
        for col in numeric_cols:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    return df.dropna()

if __name__ == "__main__":
    print("Statistical testing utilities loaded successfully")
    print("Main functions:")
    print("- mixed_effects_test(): Mixed-Effects Model")
    print("- proportion_test(): Proportion test")
    print("- variance_test(): Variance test")
    print("- welch_ttest(): t-test")
    print("- analyze_groups(): Group comparison")