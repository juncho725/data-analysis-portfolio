# Healthcare Data Analysis (2023 vs 2024)

Comprehensive two-year comparative analysis of healthcare service data to identify key KPI changes

## 🎯 Analysis Objective
Derive business insights through comparison of healthcare service operational metrics between 2023 and first half of 2024

## 📊 Core KPI Comparison

### 1. Patient Acquisition Volume
- **Monthly new patient count** trend changes

<img src="https://github.com/user-attachments/assets/fd81dcd8-9d34-47ac-b2c0-586c59ec994f" width="500px">
 
- **Branch-wise acquisition volume** comparison


### 2. Customer Profile Changes  
- **Age group distribution** changes

<img src="https://github.com/user-attachments/assets/49508c05-2051-4ae0-892c-303e3b0f8f79" width="500px">
 
- **Gender ratio** changes

<img src="https://github.com/user-attachments/assets/c00f032d-9eea-4f23-8a9d-548c3857604f" width="500px">

### 3. Revenue Performance
- **Branch-wise monthly revenue** comparison
- **Average purchase amount per patient** changes

### 4. Customer Retention Rate
- **Repeat purchase customer ratio** analysis

<img src="https://github.com/user-attachments/assets/00cb4950-646f-48e5-a39c-082ee494a8f1" width="500px">

- **Churn rate** comparison

## 🔍 Key Findings

| KPI | 2023 | 2024 | Change Rate |
|-----|------|------|-------------|
| Total Patients | 25,430 | 22,850 | **-10.1%** ↓ |
| Average Purchase Amount | ₩285,000 | ₩295,000 | **+3.5%** ↑ |
| Repeat Purchase Rate | 32% | 36% | **+4%p** ↑ |
| 30-40 Age Group Ratio | 38.2% | 35.1% | **-3.1%p** ↓ |

## 🛠 Technology Stack
- **Python** (pandas, matplotlib, seaborn)
- **Statistical Analysis** (scipy - T-test)

## 📈 Statistical Validation
- **T-test**: Confirmed significant yearly differences (p < 0.05)
- **Confidence Interval**: Analysis performed with 95% confidence level
- **Sample Size**: Statistical validity ensured with sufficient data
- **Test Results**: Both patient acquisition decrease and repeat purchase rate improvement statistically proven significant

## 🚀 Execution
```bash
pip install pandas matplotlib seaborn scipy
python analysis.py
```

## 💡 Key Insights
- **Patient volume decreased** but **customer quality improved** (repeat rate↑, purchase amount↑)  
- **30-40 age group core customer decline** → Marketing strategy review needed
- **Performance variance across branches** exists → Need to analyze success factors of top-performing branches