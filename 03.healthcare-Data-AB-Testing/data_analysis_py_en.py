"""
Healthcare Product Split Prescription Effectiveness Analysis
Purpose: Measure the effect of 1.5-month split prescription on patient care
KPIs: BMI reduction, repurchase rate, referral rate
"""

import pandas as pd
import numpy as np
from statsmodels.formula.api import mixedlm
from statsmodels.stats.proportion import proportions_ztest
from scipy import stats

class HealthcareAnalyzer:
    """Healthcare product split prescription effectiveness analyzer"""
    
    def __init__(self):
        self.results = {}
    
    def preprocess_bmi_data(self, df, group_name):
        """Preprocess BMI data"""
        # Date and BMI calculation
        df['visit_date'] = pd.to_datetime(df['visit_date'])
        df['height_m'] = df['height'] / 100
        df['initial_bmi'] = df['initial_weight'] / (df['height_m'] ** 2)
        df['current_bmi'] = df['current_weight'] / (df['height_m'] ** 2)
        df['bmi_reduction'] = df['initial_bmi'] - df['current_bmi']
        
        # Create time variables
        df = df.sort_values(['patient_id', 'visit_date'])
        df['first_visit'] = df.groupby('patient_id')['visit_date'].transform('first')
        df['days_since_start'] = (df['visit_date'] - df['first_visit']).dt.days
        
        # Filter analysis subjects
        df_filtered = df[
            (df['days_since_start'].between(30, 105)) &
            (df['initial_bmi'].between(25, 30))
        ].copy()
        
        df_filtered['group'] = group_name
        return df_filtered
    
    def analyze_bmi_effect(self, control_path, treatment_path):
        """BMI reduction effect analysis - Mixed Effects Model"""
        
        # Load and preprocess data
        control_df = self.preprocess_bmi_data(pd.read_excel(control_path), 'control')
        treatment_df = self.preprocess_bmi_data(pd.read_excel(treatment_path), 'treatment')
        combined_df = pd.concat([control_df, treatment_df])
        
        # Remove outliers
        Q1, Q3 = combined_df['bmi_reduction'].quantile([0.25, 0.75])
        IQR = Q3 - Q1
        combined_df = combined_df[
            combined_df['bmi_reduction'].between(Q1 - 1.5*IQR, Q3 + 1.5*IQR)
        ]
        
        # Mixed-Effects Model
        model = mixedlm(
            'bmi_reduction ~ C(group) * days_since_start', 
            combined_df, 
            groups=combined_df['patient_id']
        )
        results = model.fit()
        
        # Store results
        group_effect = results.params['C(group)[T.treatment]']
        p_value = results.pvalues['C(group)[T.treatment]']
        
        self.results['bmi'] = {
            'group_effect': group_effect,
            'p_value': p_value,
            'significant': p_value < 0.05,
            'control_n': len(control_df),
            'treatment_n': len(treatment_df)
        }
        
        return results
    
    def analyze_repurchase_rate(self, purchase_data_paths):
        """Repurchase rate analysis - Z-test"""
        
        results = []
        
        for paths in purchase_data_paths:
            first_df = pd.read_excel(paths['first'])
            second_df = pd.read_excel(paths['second'])
            
            # Merge repurchase data
            merged_df = pd.merge(first_df, second_df, on='patient_id', suffixes=('_1st', '_2nd'))
            merged_df['days_between'] = (
                pd.to_datetime(merged_df['purchase_date_2nd']) - 
                pd.to_datetime(merged_df['purchase_date_1st'])
            ).dt.days
            
            # Repurchase within 150 days
            repurchase_count = len(merged_df[merged_df['days_between'] <= 150])
            total_count = len(first_df)
            
            results.append({
                'group': paths['group'],
                'total': total_count,
                'repurchase': repurchase_count,
                'rate': repurchase_count / total_count * 100
            })
        
        # Z-test
        z_stat, p_value = proportions_ztest(
            [results[0]['repurchase'], results[1]['repurchase']],
            [results[0]['total'], results[1]['total']]
        )
        
        self.results['repurchase'] = {
            'groups': results,
            'z_statistic': z_stat,
            'p_value': p_value,
            'significant': p_value < 0.05
        }
        
        return results
    
    def analyze_referral_rate(self, purchase_paths, incentive_path):
        """Referral rate analysis"""
        
        incentive_df = pd.read_excel(incentive_path)
        incentive_df['region'] = incentive_df['location'].map({
            'loc_a': 'A', 'loc_b': 'B', 'loc_c': 'C', 
            'loc_d': 'D', 'loc_e': 'E', 'loc_f': 'F', 'loc_g': 'G'
        })
        
        results = []
        
        for path_info in purchase_paths:
            purchase_df = pd.read_excel(path_info['path'])
            
            # Match purchase-incentive data
            merged_df = pd.merge(
                purchase_df, incentive_df,
                on=['region', 'patient_chart_no'],
                how='inner'
            )
            
            # Incentive usage within 150 days
            merged_df['days_diff'] = (
                pd.to_datetime(merged_df['incentive_date']) - 
                pd.to_datetime(merged_df['purchase_date'])
            ).dt.days
            
            valid_referrals = len(merged_df[
                (merged_df['days_diff'] >= 0) & 
                (merged_df['days_diff'] <= 150)
            ])
            
            total_customers = len(purchase_df)
            
            results.append({
                'group': path_info['group'],
                'total': total_customers,
                'referral': valid_referrals,
                'rate': valid_referrals / total_customers * 100
            })
        
        self.results['referral'] = results
        return results
    
    def print_summary(self):
        """Analysis results summary"""
        print("=" * 60)
        print("📈 Split Prescription Effectiveness Analysis Results")
        print("=" * 60)
        
        if 'bmi' in self.results:
            bmi = self.results['bmi']
            status = "✅ Significant" if bmi['significant'] else "❌ Not Significant"
            print(f"1️⃣ BMI Reduction Effect: {status}")
            print(f"   → Effect Size: {bmi['group_effect']:+.3f} (p={bmi['p_value']:.4f})")
        
        if 'repurchase' in self.results:
            rep = self.results['repurchase']
            status = "✅ Significant" if rep['significant'] else "❌ Not Significant"
            print(f"2️⃣ Repurchase Rate Difference: {status}")
            for group in rep['groups']:
                print(f"   → {group['group']}: {group['rate']:.1f}%")
        
        if 'referral' in self.results:
            print(f"3️⃣ Referral Rate:")
            for group in self.results['referral']:
                print(f"   → {group['group']}: {group['rate']:.1f}%")
        
        print("\n💡 Conclusion: Quantitative measurement of enhanced patient care effects through split prescription completed")
    
    def run_full_analysis(self):
        """Execute full analysis"""
        
        # Sample file paths (modify when in actual use)
        paths = {
            'bmi_control': "sample_data/control_bmi.xlsx",
            'bmi_treatment': "sample_data/treatment_bmi.xlsx",
            'repurchase': [
                {'first': "sample_data/group1_first.xlsx", 'second': "sample_data/group1_second.xlsx", 'group': 'Group_1'},
                {'first': "sample_data/group2_first.xlsx", 'second': "sample_data/group2_second.xlsx", 'group': 'Group_2'}
            ],
            'referral_purchase': [
                {'path': "sample_data/purchase_jan.xlsx", 'group': 'January'},
                {'path': "sample_data/purchase_feb.xlsx", 'group': 'February'}
            ],
            'referral_incentive': "sample_data/incentive_usage.xlsx"
        }
        
        print("🔍 Healthcare Product Split Prescription Effectiveness Analysis Started")
        
        # 1. BMI analysis
        print("\n1️⃣ BMI Reduction Effect Analysis...")
        self.analyze_bmi_effect(paths['bmi_control'], paths['bmi_treatment'])
        
        # 2. Repurchase rate analysis
        print("2️⃣ Repurchase Rate Analysis...")
        self.analyze_repurchase_rate(paths['repurchase'])
        
        # 3. Referral rate analysis
        print("3️⃣ Referral Rate Analysis...")
        self.analyze_referral_rate(paths['referral_purchase'], paths['referral_incentive'])
        
        # 4. Results summary
        self.print_summary()
        
        return self.results

if __name__ == "__main__":
    analyzer = HealthcareAnalyzer()
    results = analyzer.run_full_analysis()