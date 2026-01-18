"""
🏆 BREAKTHROUGH INNOVATIONS - WINNING SOLUTION
Aadhaar Life Cycle Intelligence Platform

This module implements 5 breakthrough innovations:
1. Migration Flow Intelligence
2. Life Events Detection Framework
3. Age Cohort Demand Forecasting
4. Service Desert Detection
5. Aadhaar SDG Alignment Score

Run this script to generate all innovation data files.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from glob import glob
import warnings
warnings.filterwarnings('ignore')

# Paths
BASE_PATH = Path('.')
PROCESSED_PATH = BASE_PATH / 'processed_data'

# State populations
INDIA_STATE_POPULATION = {
    'Uttar Pradesh': 241000000, 'Maharashtra': 130000000, 'Bihar': 130000000,
    'West Bengal': 102000000, 'Madhya Pradesh': 87000000, 'Tamil Nadu': 83000000,
    'Rajasthan': 82000000, 'Karnataka': 69000000, 'Gujarat': 71000000,
    'Andhra Pradesh': 54000000, 'Odisha': 47000000, 'Telangana': 39000000,
    'Kerala': 36000000, 'Jharkhand': 40000000, 'Assam': 36000000,
    'Punjab': 31000000, 'Chhattisgarh': 30000000, 'Haryana': 30000000,
    'Delhi': 21000000, 'Jammu And Kashmir': 14000000, 'Uttarakhand': 12000000,
    'Himachal Pradesh': 8000000, 'Tripura': 4500000, 'Meghalaya': 4000000,
    'Manipur': 3500000, 'Nagaland': 2300000, 'Goa': 1600000, 
    'Arunachal Pradesh': 1700000, 'Puducherry': 1700000, 'Mizoram': 1300000,
    'Chandigarh': 1200000, 'Sikkim': 700000, 'Andaman And Nicobar Islands': 450000,
    'Dadra And Nagar Haveli And Daman And Diu': 700000, 'Lakshadweep': 70000,
    'Ladakh': 300000
}


def load_data():
    """Load all datasets."""
    print("📊 Loading datasets...")
    
    if (PROCESSED_PATH / 'enrolment_clean.parquet').exists():
        df_bio = pd.read_parquet(PROCESSED_PATH / 'biometric_clean.parquet')
        df_demo = pd.read_parquet(PROCESSED_PATH / 'demographic_clean.parquet')
        df_enrol = pd.read_parquet(PROCESSED_PATH / 'enrolment_clean.parquet')
    else:
        # Load from CSVs (consolidated raw_data folder)
        bio_files = sorted(glob(str(BASE_PATH / 'raw_data/api_data_aadhar_biometric*.csv')))
        demo_files = sorted(glob(str(BASE_PATH / 'raw_data/api_data_aadhar_demographic*.csv')))
        enrol_files = sorted(glob(str(BASE_PATH / 'raw_data/api_data_aadhar_enrolment*.csv')))
        
        df_bio = pd.concat([pd.read_csv(f) for f in bio_files], ignore_index=True)
        df_demo = pd.concat([pd.read_csv(f) for f in demo_files], ignore_index=True)
        df_enrol = pd.concat([pd.read_csv(f) for f in enrol_files], ignore_index=True)
        
        # Clean data
        for df in [df_bio, df_demo, df_enrol]:
            df['date'] = pd.to_datetime(df['date'], format='%d-%m-%Y')
            df['state'] = df['state'].str.strip().str.title()
            df['district'] = df['district'].str.strip().str.title()
        
        df_bio['total_bio'] = df_bio['bio_age_5_17'] + df_bio['bio_age_17_']
        df_demo['total_demo'] = df_demo['demo_age_5_17'] + df_demo['demo_age_17_']
        df_enrol['total_enrol'] = df_enrol['age_0_5'] + df_enrol['age_5_17'] + df_enrol['age_18_greater']
    
    print(f"   Biometric: {len(df_bio):,} records")
    print(f"   Demographic: {len(df_demo):,} records")
    print(f"   Enrollment: {len(df_enrol):,} records")
    
    return df_bio, df_demo, df_enrol


def calculate_migration_flow(df_enrol, df_demo):
    """
    INNOVATION 1: Migration Flow Intelligence
    
    Analyze demographic updates relative to enrollments to detect migration patterns.
    High demo/enrol ratio = Migration Hub (receiving area)
    Low demo/enrol ratio = Migration Source (sending area)
    """
    print("\n🌊 Calculating Migration Flow Intelligence...")
    
    state_enrol = df_enrol.groupby('state')['total_enrol'].sum().reset_index()
    state_demo = df_demo.groupby('state')['total_demo'].sum().reset_index()
    
    migration_df = state_enrol.merge(state_demo, on='state', how='outer').fillna(0)
    
    # Migration Index
    migration_df['migration_index'] = (
        migration_df['total_demo'] / migration_df['total_enrol'].replace(0, 1)
    ).round(2)
    
    # Classify states
    median_index = migration_df['migration_index'].median()
    migration_df['migration_type'] = migration_df['migration_index'].apply(
        lambda x: 'Migration Hub (Receiving)' if x > median_index * 1.5 
        else ('Migration Source (Sending)' if x < median_index * 0.7 else 'Balanced')
    )
    
    # Migration intensity score (0-100)
    migration_df['migration_intensity'] = (
        migration_df['migration_index'].rank(pct=True) * 100
    ).round(1)
    
    print(f"   Migration Hubs: {(migration_df['migration_type'] == 'Migration Hub (Receiving)').sum()}")
    print(f"   Migration Sources: {(migration_df['migration_type'] == 'Migration Source (Sending)').sum()}")
    
    return migration_df


def calculate_life_events(df_enrol, df_bio, df_demo):
    """
    INNOVATION 2: Life Events Detection Framework
    
    Connect Aadhaar activity to life milestones.
    """
    print("\n🎂 Building Life Events Framework...")
    
    # Monthly patterns by age
    df_enrol['month'] = df_enrol['date'].dt.month
    df_enrol['month_name'] = df_enrol['date'].dt.month_name()
    
    monthly_by_age = df_enrol.groupby('month').agg({
        'age_0_5': 'sum',
        'age_5_17': 'sum',
        'age_18_greater': 'sum',
        'total_enrol': 'sum'
    }).reset_index()
    
    month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                   'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    monthly_by_age['month_name'] = monthly_by_age['month'].apply(
        lambda x: month_names[x-1] if x <= 12 else f'M{x}'
    )
    
    # Life Events Summary
    life_events = pd.DataFrame({
        'life_event': [
            'Birth Registration', 'School Admission', 
            'Board Exam/College', 'Employment/Marriage'
        ],
        'age_group': ['0-5 years', '5-17 years', '15-18 years', '18+ years'],
        'primary_activity': ['New Enrollment', 'New Enrollment', 'Biometric Update', 'Demo Update'],
        'volume': [
            df_enrol['age_0_5'].sum(),
            df_enrol['age_5_17'].sum(),
            df_bio['bio_age_5_17'].sum(),
            df_demo['demo_age_17_'].sum()
        ],
        'policy_action': [
            'Link with birth certificate registration',
            'Partner with schools for enrollment drives',
            'Mandatory biometric update reminders',
            'Address change facilitation services'
        ]
    })
    
    print(f"   Life events identified: {len(life_events)}")
    
    return life_events, monthly_by_age


def calculate_age_cohort_forecast(df_enrol):
    """
    INNOVATION 3: Age Cohort Demand Forecasting
    
    Use current age distribution to predict future service demand.
    """
    print("\n📈 Generating Age Cohort Demand Forecast...")
    
    state_age = df_enrol.groupby('state').agg({
        'age_0_5': 'sum',
        'age_5_17': 'sum',
        'age_18_greater': 'sum',
        'total_enrol': 'sum'
    }).reset_index()
    
    # Calculate percentages
    state_age['pct_infant'] = (state_age['age_0_5'] / state_age['total_enrol'] * 100).round(1)
    state_age['pct_child'] = (state_age['age_5_17'] / state_age['total_enrol'] * 100).round(1)
    state_age['pct_adult'] = (state_age['age_18_greater'] / state_age['total_enrol'] * 100).round(1)
    
    # Future demand predictions
    # Current 0-5 → Need biometric update at age 15 (in ~10 years)
    # Current 5-17 → Need adult services (in ~5 years)
    state_age['bio_demand_2031'] = state_age['age_0_5']
    state_age['bio_demand_2036'] = state_age['age_5_17']
    state_age['demo_demand_2031'] = state_age['age_5_17']
    
    # Growth potential score
    state_age['growth_potential'] = (
        (state_age['age_0_5'] + state_age['age_5_17']) / state_age['total_enrol'] * 100
    ).round(1)
    
    print(f"   States analyzed: {len(state_age)}")
    print(f"   Total future bio demand (2031): {state_age['bio_demand_2031'].sum():,}")
    
    return state_age


def calculate_service_deserts(df_enrol):
    """
    INNOVATION 4: Service Desert Detection
    
    Identify geographic areas that are underserved.
    """
    print("\n🏜️ Detecting Service Deserts...")
    
    # Pincode-level stats
    pincode_stats = df_enrol.groupby(['state', 'district', 'pincode']).agg({
        'total_enrol': 'sum',
        'date': 'nunique'
    }).reset_index()
    pincode_stats.columns = ['state', 'district', 'pincode', 'total_enrol', 'active_days']
    
    # District-level aggregation
    district_stats = pincode_stats.groupby(['state', 'district']).agg({
        'pincode': 'nunique',
        'total_enrol': 'sum',
        'active_days': 'mean'
    }).reset_index()
    district_stats.columns = ['state', 'district', 'unique_pincodes', 'total_enrol', 'avg_active_days']
    
    # Service density
    district_stats['enrol_per_pincode'] = (
        district_stats['total_enrol'] / district_stats['unique_pincodes']
    ).round(0)
    
    # Identify deserts
    median_density = district_stats['enrol_per_pincode'].median()
    district_stats['is_service_desert'] = district_stats['enrol_per_pincode'] < (median_density * 0.3)
    
    # Desert score (0-100, higher = more underserved)
    district_stats['desert_score'] = (
        100 - district_stats['enrol_per_pincode'].rank(pct=True) * 100
    ).round(0)
    
    # Priority level
    district_stats['priority'] = district_stats['desert_score'].apply(
        lambda x: 'Critical' if x >= 80 else ('High' if x >= 60 else ('Medium' if x >= 40 else 'Low'))
    )
    
    print(f"   Districts analyzed: {len(district_stats)}")
    print(f"   Service deserts identified: {district_stats['is_service_desert'].sum()}")
    
    return district_stats


def calculate_sdg_alignment(df_enrol, df_bio, df_demo):
    """
    INNOVATION 5: Aadhaar SDG Alignment Score
    
    Link Aadhaar progress to UN Sustainable Development Goals.
    """
    print("\n🎯 Calculating SDG Alignment Scores...")
    
    sdg_df = df_enrol.groupby('state').agg({
        'total_enrol': 'sum',
        'age_0_5': 'sum',
        'age_5_17': 'sum',
        'age_18_greater': 'sum',
        'pincode': 'nunique',
        'district': 'nunique'
    }).reset_index()
    
    sdg_df['population'] = sdg_df['state'].map(INDIA_STATE_POPULATION).fillna(1000000)
    
    # SDG 16.9: Legal Identity for All
    sdg_df['sdg_16_9_identity'] = (
        (sdg_df['total_enrol'] / sdg_df['population']) * 100
    ).clip(0, 100).round(1)
    
    # SDG 1.3: Social Protection (DBT eligibility via adult enrollment)
    sdg_df['sdg_1_3_protection'] = (
        (sdg_df['age_18_greater'] / (sdg_df['population'] * 0.65)) * 100
    ).clip(0, 100).round(1)
    
    # SDG 4.1: Quality Education (child enrollment)
    sdg_df['sdg_4_1_education'] = (
        (sdg_df['age_5_17'] / (sdg_df['population'] * 0.25)) * 100
    ).clip(0, 100).round(1)
    
    # SDG 10.2: Social Inclusion (geographic spread)
    max_pincodes = sdg_df['pincode'].max()
    sdg_df['sdg_10_2_inclusion'] = (
        (sdg_df['pincode'] / max_pincodes) * 100
    ).round(1)
    
    # Overall SDG Alignment Score (weighted)
    sdg_df['sdg_alignment_score'] = (
        sdg_df['sdg_16_9_identity'].rank(pct=True) * 40 +
        sdg_df['sdg_1_3_protection'].rank(pct=True) * 25 +
        sdg_df['sdg_4_1_education'].rank(pct=True) * 20 +
        sdg_df['sdg_10_2_inclusion'].rank(pct=True) * 15
    ).round(1)
    
    # SDG Achievement Level
    sdg_df['sdg_level'] = sdg_df['sdg_alignment_score'].apply(
        lambda x: 'Leader' if x >= 80 else ('Achiever' if x >= 60 else ('Emerging' if x >= 40 else 'Lagging'))
    )
    
    print(f"   States analyzed: {len(sdg_df)}")
    print(f"   National SDG Score: {sdg_df['sdg_alignment_score'].mean():.1f}/100")
    
    return sdg_df


def main():
    """Generate all breakthrough innovation data."""
    print("="*60)
    print("🏆 BREAKTHROUGH INNOVATIONS - DATA GENERATION")
    print("="*60)
    
    # Load data
    df_bio, df_demo, df_enrol = load_data()
    
    # Generate innovations
    migration_df = calculate_migration_flow(df_enrol, df_demo)
    life_events, monthly_patterns = calculate_life_events(df_enrol, df_bio, df_demo)
    age_forecast = calculate_age_cohort_forecast(df_enrol)
    service_deserts = calculate_service_deserts(df_enrol)
    sdg_scores = calculate_sdg_alignment(df_enrol, df_bio, df_demo)
    
    # Save all outputs
    print("\n💾 Saving innovation data...")
    PROCESSED_PATH.mkdir(exist_ok=True)
    
    migration_df.to_parquet(PROCESSED_PATH / 'migration_flow_analysis.parquet', index=False)
    life_events.to_parquet(PROCESSED_PATH / 'life_events_framework.parquet', index=False)
    monthly_patterns.to_parquet(PROCESSED_PATH / 'life_events_monthly.parquet', index=False)
    age_forecast.to_parquet(PROCESSED_PATH / 'age_cohort_forecast.parquet', index=False)
    service_deserts.to_parquet(PROCESSED_PATH / 'service_desert_analysis.parquet', index=False)
    sdg_scores.to_parquet(PROCESSED_PATH / 'sdg_alignment_scores.parquet', index=False)
    
    print("\n✅ All innovation data generated successfully!")
    print("\n📁 Files created:")
    print("   - migration_flow_analysis.parquet")
    print("   - life_events_framework.parquet")
    print("   - life_events_monthly.parquet")
    print("   - age_cohort_forecast.parquet")
    print("   - service_desert_analysis.parquet")
    print("   - sdg_alignment_scores.parquet")
    
    print("\n" + "="*60)
    print("🎯 INNOVATION SUMMARY")
    print("="*60)
    print(f"   Migration Hubs: {(migration_df['migration_type'] == 'Migration Hub (Receiving)').sum()} states")
    print(f"   Life Events: {len(life_events)} milestones identified")
    print(f"   Future Demand: {age_forecast['bio_demand_2031'].sum():,} biometric updates by 2031")
    print(f"   Service Deserts: {service_deserts['is_service_desert'].sum()} districts need intervention")
    print(f"   National SDG Score: {sdg_scores['sdg_alignment_score'].mean():.1f}/100")
    
    return migration_df, life_events, age_forecast, service_deserts, sdg_scores


if __name__ == "__main__":
    main()
