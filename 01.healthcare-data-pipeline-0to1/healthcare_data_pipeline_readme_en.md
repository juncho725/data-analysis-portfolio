# 🏥 Healthcare Data Pipeline: Diet Package Analysis System

## 📊 **30-Second Summary**
Built a **complete dataset of 600,000 records** from an **analysis-impossible state** through analyzing 140 SQL files alongside the company's first data team establishment. Achieved 0→1 construction from raw data access to complete analysis system.

---

## 🎯 **Key Achievements**
| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| **Analyzable Data** | 100 patients (manual sampling) | 600,000 records (complete) | **6,000x ↑** |
| **Data Accessibility** | No raw data access | Full raw data utilization | **0→1 Achievement** |
| **KPI Coverage** | Limited sample analysis | One-click analysis for all KPIs | **Complete Automation** |
| **Data Reliability** | Refunds/changes not reflected | Daily change reflection | **100% Accuracy** |

---

## 📖 **Project Background: Solving Healthcare Data Complexity**

### **🎯 Business Challenges**
- **Analysis-impossible state**: No raw data access (SQL-based medical system)
- **Limited sampling**: Only 100 patients manually extracted from charts for analysis
- **Manual data entry**: Daily manual Excel input for package quantities
- **Untracked changes**: Refunds and modifications not reflected in Excel in real-time
- **KPI analysis limitations**: Unable to grasp overall status, only sample-based estimation possible

### **🔍 Technical Challenges**
```sql
-- Problem: Multiple prescriptions linked to one PaymentID
-- Priority logic needed to filter target medications only
ROW_NUMBER() OVER (PARTITION BY PaymentID ORDER BY 
    CASE 
        WHEN MedicineName LIKE '%target_medication%' AND Memo REGEXP '-1' THEN 1  -- Core product + session info
        WHEN MedicineName LIKE '%target_medication%' THEN 2                       -- Core product only
        WHEN Memo REGEXP '-1' THEN 3                                             -- Session info only
        ELSE 4
    END
)
```

---

## 🚨 Core Problems Solved

### 🔎 Solution Strategy Summary

| Problem # | Problem Summary | Domain Cause | Solution Keywords | Technology/Strategy Used |
|-----------|-----------------|--------------|-------------------|--------------------------|
| 1 | Time reference mismatch | Payment date ≠ Prescription date ≠ Start date (diverse treatment flows) | Define treatment start based on latest date (max) | Medical staff consultation, `max(pay_date, consult_date)` |
| 2 | Core medication selection | Multiple medications in one payment | Priority-based medication selection | `SQL ROW_NUMBER + CASE WHEN` |
| 3 | Missing data recovery | Unstable PaymentID-MedicalRecordID connection (prepayment, prescription delays, etc.) | Time-series based similar record matching by same patient | 30-day similar records → 200-day follow-up records |
| 4 | Package classification notation changes | Different memo notation methods by period | Classification logic branching by policy date | `if memo.startswith()` + policy date (`2022-12-13`) conditional branching |
| 5 | Treatment sequence analysis index | Need to analyze multi-dose patients | Generate patient visit order index | `groupby + cumcount` + latest date sorting |

---

### **1. Healthcare Industry Characteristics: Time Reference Mismatch**

```python
# Problem: Payment date ≠ Prescription date
patient_timeline = {
    "payment_date": "2024-01-01",      # Advance deposit payment
    "prescription_date": "2024-01-10",  # Actual consultation and prescription
}

# Solution: Standard definition through medical staff consultation
# Since actual treatment start date is crucial for diet effect analysis,
# 'treatment start point' is defined based on the latest date
def determine_treatment_start_date(pay_date, consult_time):
    """Determine accurate start point for diet effect analysis"""
    return max(pay_date, consult_time)  # Actual treatment confirmation point
```

### **2. Core Product Selection in Complex Table Joins**
```sql
-- Challenge: Complex relationships among 5 core tables out of 140 tables
-- Multiple medications including non-target drugs in one payment

-- Solution: Business priority-based selection algorithm
WITH PriorityRanking AS (
    SELECT *,
        ROW_NUMBER() OVER (PARTITION BY PaymentID ORDER BY 
            CASE 
                -- Priority 1: Target medication + session info complete match
                WHEN MedicineName LIKE '%target_medication%' AND Memo REGEXP '-1' THEN 1
                -- Priority 2: Target medication only confirmed
                WHEN MedicineName LIKE '%target_medication%' THEN 2
                -- Priority 3: Session info only (missing medication name)
                WHEN Memo REGEXP '-1' THEN 3
                ELSE 4
            END,
            PaymentAmt DESC  -- Sort by amount for same conditions
        ) AS priority_rank
    FROM medical_data
)
SELECT * FROM PriorityRanking WHERE priority_rank = 1;
```

### **3. Medical Workflow-Based Missing Data Recovery (35% → 3%)**
```python
def medical_workflow_recovery(df, reference_df):
    """
    Missing data recovery logic defined through medical staff consultation.
    
    💡 Domain-based problem:
    PaymentID and MedicalRecordID are not connected 1:1.
    (e.g., prepayment, post-consultation payment, prescription delays, etc. - non-standard workflows)
    
    ➤ Accurate medication matching is difficult with single-key joins.
    ➤ Therefore, time-based similar matching between treatment points based on 'same patient (PatientID)' is needed.

    🛠️ Solution Strategy:
    1. Prioritize recovery of most similar records within 30 days of same patient's same treatment process
    2. If unavailable, recover based on follow-up revisit records within maximum 200 days of same patient
    
    These criteria are workflow-based logic defined through consultation with actual in-house medical staff.
    """

    for idx in df[df['MedicineName'].isnull()].index:
        patient_id = df.loc[idx, 'PatientID']
        target_date = df.loc[idx, 'ConsultTime']
        
        # Stage 1: Recovery within same treatment process of same patient (within 30 days)
        same_treatment = reference_df[
            (reference_df['PatientID'] == patient_id) &
            (abs(reference_df['ConsultTime'] - target_date) <= pd.Timedelta(days=30)) &
            (reference_df['MedicineName'].str.contains('target_medication', na=False))
        ]
        
        if not same_treatment.empty:
            closest_record = same_treatment.loc[
                abs(same_treatment['ConsultTime'] - target_date).idxmin()
            ]
            df.loc[idx, ['MedicineName', 'Memo', 'ProgressNote']] = \
                closest_record[['MedicineName', 'Memo', 'ProgressNote']].values
            df.loc[idx, 'DataUpdated'] = 1
            continue
        
        # Stage 2: Utilize follow-up revisit records of same patient (within 200 days)
        extended_search = reference_df[
            (reference_df['PatientID'] == patient_id) &
            (reference_df['ConsultTime'] > target_date) &
            (reference_df['ConsultTime'] - target_date <= pd.Timedelta(days=200))
        ]
        
        if not extended_search.empty:
            next_visit = extended_search.sort_values('ConsultTime').iloc[0]
            df.loc[idx, ['MedicineName', 'Memo']] = \
                next_visit[['MedicineName', 'Memo']].values
            df.loc[idx, 'DataUpdated'] = 1

    return df
```

### **4. Period-based Package Classification Algorithm**
```python
def categorize_package(medicine_name, memo, consult_date):
    """
    Package classification algorithm to solve the problem of period-varying notation used in medical settings

    💡 Domain-based problem:
    - For diet medications, **how many months of prescription is very important for analysis**
    - However, in-house system (Raw data) has inconsistent classification due to period-varying input methods
        → Example: Same '1-1' means 1.5 months before 2022, 1 month after

    🛠️ Solution Strategy:
    - Distinguish interpretation methods based on policy change date (2022-12-13) through consultation with medical staff/operations team
    - Create new 'Package Classification' column reflecting policy based on `memo`, `medicine_name`, `consult_date`
    """

    # Data cleaning
    memo = str(memo).strip()
    medicine_name = str(medicine_name).strip().lower()
    consult_date = pd.to_datetime(consult_date)

    # Exclude non-target medications
    if not ('target_medication' in medicine_name or 'target medication' in medicine_name):
        return 'Other'

    # Policy change reference date
    policy_change_date = pd.to_datetime('2022-12-13')

    # First package: '1-1' means different things by period
    if memo.startswith('1-1'):
        return '1.5 months' if consult_date <= policy_change_date else '1 month'

    # Continuous packages: '2-1' ~ '9-1' are all unified as 3-month packages
    elif any(memo.startswith(f"{i}-1") for i in range(2, 10)):
        return '3 months'

    return 'Other'
```

### **5. Patient Journey Indexing**
```python
def create_patient_journey_index(df):
    """
    Regional and patient-specific purchase order indexing

    💡 Domain-based problem:
    - Analyzing which dose a patient is taking is very important for
      effect trends, churn rates, loyalty analysis, etc.
    - Example: Characteristics of 2nd purchase patients / Weight changes at 3rd purchase, etc.
    
    🛠️ Solution Strategy:
    - Sort based on treatment start reference date (latest value between `PayDate` and `ConsultTime`)
    - Assign same patient's visit order as index to create `visit_index` column
    """

    # Sort based on accurate treatment start point
    df['Confirm_date'] = df.apply(
        lambda row: max(row['PayDate'], row['ConsultTime']) 
        if pd.notna(row['PayDate']) and pd.notna(row['ConsultTime'])
        else (row['ConsultTime'] if pd.isna(row['PayDate']) else row['PayDate']),
        axis=1
    )

    # Patient visit order indexing
    df['visit_index'] = (
        df.sort_values(['Region', 'PatientID', 'Confirm_date'])
        .groupby(['Region', 'PatientID'])
        .cumcount() + 1
    )

    return df
```

---

## 🚀 **Organizational Impact**

### **Before: Analysis-Impossible Dark Age**
```
❌ No raw data access (SQL system, no permissions)
❌ Only 100 patients manually extractable from charts
❌ Daily manual Excel input for package quantities
❌ Real-time reflection of refunds/changes impossible
❌ Overall KPI analysis impossible
❌ Only estimation-based decision making possible
```

### **After: Fully Automated Analysis System**
```
✅ Complete raw data access and utilization
✅ Built 600,000 complete dataset
✅ Automatic real-time change reflection
✅ One-click analysis possible for all KPIs
✅ Accurate data-driven decision making
✅ Integrated real-time monitoring across 7 regions
```

### **Built Complete Dataset (600,000 records)**
```python
complete_dataset_columns = [
    "Region",           # 7 regions integrated
    "ChartNumber",      # Patient unique identifier
    "FirstVisitDate",   # Patient acquisition point
    "Prescription",     # Diet package information
    "PhoneNumber",      # Patient contact
    "MedicalNote",      # Patient conditions, weight, muscle mass, fat mass
    "Age",             # Patient age
    "Gender",          # Patient gender
    "ResidentID",      # Patient identification
    "MedicationDate",  # Actual treatment start date
    "PackageType",     # 1month/1.5month/3month automatic classification
    "VisitCount"       # Patient visit order index
]
# → Complete coverage of all existing KPIs in one file
```

---

## 🛠️ **Data Pipeline Architecture**

```
🚫 Analysis-impossible state (No raw data access)
    ↓
🔍 System structure analysis through 140 SQL files
    ↓
🤝 Business logic understanding through medical staff communication
    ↓
🗃️ Raw data access permission acquisition and extraction
    ↓
🔧 Complex joins + business priority filtering
    ↓
🩹 Medical workflow-based missing data recovery (90% success)
    ↓
📅 Time reference standardization (medical staff consultation standard)
    ↓
🏷️ Period-based package classification algorithm implementation
    ↓
🌐 7-region integration + deduplication
    ↓
📊 Patient journey indexing
    ↓
💎 600,000 complete dataset (covers all KPIs)
```

### **Core Technology Stack**
- **SQL**: Complex medical data joins and priority logic
- **Python**: pandas-based large-scale time-series data processing
- **Business Logic**: Medical staff consultation-based domain rule engine

---

## 💡 **Key Success Factors**

### **1. Domain Expertise Development**
```python
stakeholder_collaboration = {
    "Medical Staff": "Diet treatment process and effect measurement standards",
    "Operations Team": "Package policy change history and notation methods",
    "Finance Team": "Complex payment system and settlement logic",
    "Regional Managers": "Regional operation differences and data characteristics"
}
# → Business context understanding more crucial than technical implementation
```

### **2. Reflecting Healthcare Data Characteristics**
```python
medical_data_challenges = {
    "Time Complexity": "Payment ≠ Prescription ≠ Treatment start point",
    "Relationship Complexity": "Core product selection in 1:N payment-prescription relationships",
    "Policy Changes": "Reflecting period-based package notation and policy changes",
    "Workflow": "Data recovery utilizing medical staff treatment patterns"
}
```

### **3. Scalable System Design**
```python
system_design_principles = {
    "Modularization": "Scalability through regional setting separation",
    "Validation": "Medical staff review-based accuracy verification system",
    "Tracking": "Data change history management and recovery success rate monitoring"
}
```

---

## 🎯 **Key Code Snippets**

<details>
<summary><strong>📊 Target Medication Priority Selection Logic</strong></summary>

```sql
-- Priority logic defined through medical staff consultation
WITH PrioritySelection AS (
    SELECT *,
        ROW_NUMBER() OVER (
            PARTITION BY PaymentID 
            ORDER BY 
                CASE 
                    -- Priority 1: Target medication + session info complete
                    WHEN MedicineName LIKE '%target_medication%' AND Memo REGEXP '-1' THEN 1
                    -- Priority 2: Target medication confirmed
                    WHEN MedicineName LIKE '%target_medication%' THEN 2
                    -- Priority 3: Session info only
                    WHEN Memo REGEXP '-1' THEN 3
                    ELSE 4
                END,
                PaymentAmt DESC  -- Amount-based sorting for same conditions
        ) AS priority_rank
    FROM medical_payment_data
)
SELECT * FROM PrioritySelection WHERE priority_rank = 1;
```
</details>

<details>
<summary><strong>🐍 Medical Workflow-Based Missing Data Recovery</strong></summary>

```python
def medical_workflow_recovery(df, reference_df):
    """Recovery logic defined through medical staff consultation"""
    
    updated_count = 0
    
    for idx in df[df['MedicineName'].isnull()].index:
        patient_id = df.loc[idx, 'PatientID']
        target_date = df.loc[idx, 'ConsultTime']
        
        # Data within same treatment process priority (within 30 days)
        same_treatment_window = reference_df[
            (reference_df['PatientID'] == patient_id) &
            (abs(reference_df['ConsultTime'] - target_date) <= pd.Timedelta(days=30)) &
            (reference_df['MedicineName'].str.contains('target_medication', case=False, na=False))
        ]
        
        if not same_treatment_window.empty:
            closest_record = same_treatment_window.loc[
                abs(same_treatment_window['ConsultTime'] - target_date).idxmin()
            ]
            df.loc[idx, ['MedicineName', 'Memo', 'ProgressNote']] = \
                closest_record[['MedicineName', 'Memo', 'ProgressNote']].values
            df.loc[idx, 'DataUpdated'] = 1
            updated_count += 1
    
    print(f"Recovery success rate: {updated_count}/{len(df[df['MedicineName'].isnull()])} ({updated_count/len(df[df['MedicineName'].isnull()])*100:.1f}%)")
    return df
```
</details>

<details>
<summary><strong>🏷️ Period-based Package Classification Algorithm</strong></summary>

```python
def categorize_package_by_period(medicine_name, memo, consult_date):
    """Package classification reflecting period-based policy changes"""
    
    # Data cleaning
    memo = str(memo).strip()
    medicine_name = str(medicine_name).strip().lower()
    
    # Check if target medication
    if not ('target_medication' in medicine_name or 'Target medication' in medicine_name):
        return 'Other'
    
    # Policy change reference date (medical staff consultation result)
    policy_change_date = pd.to_datetime('2022-12-13')
    consult_date = pd.to_datetime(consult_date)
    
    # Package classification logic
    if memo.startswith('1-1'):
        # Different classification before and after policy change
        return '1.5 months' if consult_date <= policy_change_date else '1 month'
    elif any(memo.startswith(f"{i}-1") for i in range(2, 10)):
        return '3 months'
    else:
        return 'Other'
```
</details>

---

## 🔗 **Key Achievement Summary**

**0→1 Innovation**: Analysis-impossible → 600,000 complete dataset  
**Technical Challenge**: Conquered complex medical system through analyzing 140 SQL files  
**Business Impact**: Organizational culture transformation from estimation-based → data-driven decision making

---

*"A 0→1 project that built a complete dataset of 600,000 records from an analysis-impossible state. From raw data access to complete automation, this was the beginning of change that transformed the entire organization's decision-making paradigm."*