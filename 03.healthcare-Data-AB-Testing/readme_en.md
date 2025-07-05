# Healthcare Product Split Prescription Effectiveness Analysis

## 📋 Project Overview

### Business Problem
- **Current Method**: Prescribing 3-month healthcare products all at once
- **Issues**: Difficulty monitoring patient compliance and treatment effectiveness
- **Solution**: Split prescription into two 1.5-month periods with medical staff check-ins

### Analysis Purpose
**Validate through A/B testing whether enhanced patient care through split prescription improves treatment outcomes**

## 🎯 Key Performance Indicators (KPI)

### 1️⃣ Weight Loss Effectiveness (BMI Changes)
- **Measurement**: Weight/height data directly measured at medical facility
- **Comparison**: BMI changes before vs after product consumption
- **Expected Effect**: Better weight loss through intermediate monitoring

### 2️⃣ Repurchase Rate
- **Measurement**: Repurchase ratio within 150 days
- **Meaning**: Patient satisfaction and treatment continuity
- **Expected Effect**: Increased repurchases due to enhanced care

### 3️⃣ Referral Rate (Customer Satisfaction)
- **Measurement**: Participation rate in referral incentive program
- **Meaning**: Patient product satisfaction and referral intention
- **Expected Effect**: Increased referrals due to improved care

## 📊 Data Structure

### Experimental Design
- **Control Group (2023)**: 3-month batch prescription
- **Treatment Group (2024)**: 1.5-month split prescription

### Data Characteristics
- **BMI Data**: Patient time-series data (weekly analysis due to irregular visit timing)
- **Purchase Data**: First purchase date, repurchase date information
- **Referral Data**: Incentive program participation records

## 🔬 Analysis Methodology

### 1. BMI Reduction Analysis
- **Model**: Mixed-Effects Model (accounting for individual patient differences)
- **Statistical Test**: F-test (variance homogeneity test)
- **Period Analysis**: Effect measurement across 30-105 day intervals

### 2. Repurchase Rate Analysis
- **Statistical Test**: Z-test (difference between two proportions)
- **Detailed Analysis**: Period-based repurchase pattern analysis

### 3. Referral Rate Analysis
- **Matching**: Incentive program participation within 150 days after first purchase per patient
- **Statistical Test**: Z-test (monthly referral rate comparison)

## 📈 Expected Results

**Enhanced medical care through split prescription** is expected to produce the following effects:

1. **Better BMI Reduction**: Compliance guidance effects through intermediate monitoring
2. **Higher Repurchase Rate**: Continued treatment due to increased patient satisfaction
3. **Increased Referral Rate**: Enhanced referral intention due to improved care quality

## 🛠 Technology Stack

- **Python**: Data analysis and statistical testing
- **pandas**: Data preprocessing
- **statsmodels**: Mixed-Effects Model, ANOVA
- **scipy**: Statistical testing (F-test, Z-test)
- **matplotlib**: Visualization

## 📁 File Structure

```
├── README.md
├── healthcare_analysis.py        # Core analysis code
├── statistical_utils.py          # Statistical testing utilities
└── sample_data/
    ├── bmi_measurements/         # BMI measurement data
    ├── purchase_records/         # Purchase/repurchase data
    └── referral_data/           # Referral/incentive data
```

## 🚀 Execution Method

```python
from healthcare_analysis import HealthcareAnalyzer

# Run analysis
analyzer = HealthcareAnalyzer()
results = analyzer.run_full_analysis()

# Print summary
analyzer.print_summary()
```

## 💡 Business Impact

Through this analysis, we quantitatively measure the **ROI of split prescription** and provide data-driven evidence for future prescription policy decisions.

### Key Insights
- Quantitative measurement of enhanced patient care effects
- Analysis of correlation between healthcare service quality and business performance
- Scientific decision-making support through A/B testing

---

*This project is a case study of A/B test analysis using healthcare data.*