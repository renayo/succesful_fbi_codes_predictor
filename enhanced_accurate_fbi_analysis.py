#!/usr/bin/env python3
"""
Enhanced FBI Crime Analysis with Accurate Astronomical Features
==============================================================

This script provides comprehensive crime analysis using properly calculated astronomical
features at noon Chicago local time for maximum accuracy and consistency.

Key Features:
- Proper ecliptic longitude calculations (not RA)
- Chicago local time zone consistency
- Accurate coordinate system conversions
- Extended temporal validation (2001-2020 vs 2021-2025)
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, f1_score
from sklearn.preprocessing import StandardScaler
import warnings
from accurate_astronomical_calculator import AccurateAstronomicalCalculator
import pytz

warnings.filterwarnings('ignore')

class EnhancedFBICrimeAnalysis:
    """
    Enhanced FBI crime analysis with accurate astronomical calculations.
    """
    
    def __init__(self):
        self.astronomical_calc = AccurateAstronomicalCalculator()
        self.chicago_tz = pytz.timezone('America/Chicago')
        self.fbi_codes = {}
        self.models = {}
        self.scalers = {}
        print("🚔 Enhanced FBI Crime Analysis initialized")
        print("✓ Using accurate astronomical calculations")
        print("✓ Chicago local time zone consistency")
    
    def load_and_process_crime_data(self):
        """
        Load and process Chicago crime data with proper date handling.
        """
        print("\n📊 Loading Chicago crime data...")
        
        # Load the comprehensive crime dataset
        try:
            df = pd.read_csv('chicago_crime_complete_all_months.csv')
            print(f"✓ Loaded {len(df):,} crime records")
        except FileNotFoundError:
            print("❌ Crime data file not found. Please ensure chicago_crime_complete_all_months.csv exists.")
            return None
        
        # Convert date column to datetime
        df['date'] = pd.to_datetime(df['date'])
        
        # For analysis purposes, we'll work with naive datetime and assume Chicago local time
        # This avoids complex DST transition issues while maintaining temporal consistency
        if df['date'].dt.tz is not None:
            df['date'] = df['date'].dt.tz_localize(None)  # Remove timezone info
        
        print(f"✓ Date range: {df['date'].min()} to {df['date'].max()}")
        print(f"✓ FBI codes found: {df['fbi_code'].nunique()}")
        
        return df
    
    def aggregate_daily_crime_data(self, df):
        """
        Aggregate crime data by day and FBI code for daily analysis.
        """
        print("\n📅 Aggregating crime data by day...")
        
        # Create date-only column for daily aggregation
        df['date_only'] = df['date'].dt.date
        
        # Aggregate by date and FBI code
        daily_counts = df.groupby(['date_only', 'fbi_code']).size().reset_index(name='crime_count')
        
        # Pivot to get FBI codes as columns
        daily_pivot = daily_counts.pivot(index='date_only', columns='fbi_code', values='crime_count').fillna(0)
        
        # Reset index and convert date back to datetime
        daily_pivot = daily_pivot.reset_index()
        daily_pivot['date'] = pd.to_datetime(daily_pivot['date_only'])
        daily_pivot = daily_pivot.drop('date_only', axis=1)
        
        print(f"✓ Created daily aggregation: {len(daily_pivot)} days")
        print(f"✓ FBI codes: {[col for col in daily_pivot.columns if col != 'date']}")
        
        return daily_pivot
    
    def calculate_astronomical_features_for_dates(self, dates):
        """
        Calculate accurate astronomical features for all dates.
        """
        print(f"\n🌌 Calculating astronomical features for {len(dates)} dates...")
        
        astronomical_data = []
        
        for i, date in enumerate(dates):
            if i % 500 == 0:
                print(f"  Progress: {i}/{len(dates)} ({100*i/len(dates):.1f}%)")
            
            # Convert to Chicago timezone for consistency (assuming input is already Chicago local time)
            if hasattr(date, 'tzinfo') and date.tzinfo is not None:
                chicago_date = date.astimezone(self.chicago_tz)
            else:
                # Assume naive datetime is already in Chicago local time
                chicago_date = date
            
            # Calculate features at noon Chicago time
            features = self.astronomical_calc.calculate_features(chicago_date)
            # Convert date to match the format from daily_crime_df
            features['date'] = pd.to_datetime(date.date() if hasattr(date, 'date') else date)
            astronomical_data.append(features)
        
        astronomical_df = pd.DataFrame(astronomical_data)
        print(f"✓ Calculated {len(astronomical_df.columns)-1} astronomical features")
        
        return astronomical_df
    
    def perform_temporal_validation(self, daily_crime_df, astronomical_df):
        """
        Perform temporal validation with 2001-2024 training and 2025 testing.
        """
        print("\n🎯 Performing temporal validation...")
        
        # Merge crime and astronomical data
        combined_df = pd.merge(daily_crime_df, astronomical_df, on='date', how='inner')
        combined_df = combined_df.sort_values('date')
        
        print(f"✓ Combined dataset: {len(combined_df)} days")
        
        # Define training and testing periods
        train_end = datetime(2024, 12, 31).date()
        test_start = datetime(2025, 1, 1).date()
        
        train_data = combined_df[combined_df['date'].dt.date <= train_end]
        test_data = combined_df[combined_df['date'].dt.date >= test_start]
        
        print(f"✓ Training period: {len(train_data)} days (2001-2024)")
        print(f"✓ Testing period: {len(test_data)} days (2025)")
        
        # Get FBI codes (excluding date column)
        fbi_codes = [col for col in combined_df.columns if col.startswith('FBI_') or col in [
            '01A', '01B', '02', '03', '04A', '04B', '05', '06', '07', '08A', '08B', 
            '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', 
            '22', '24', '26'
        ]]
        
        # Get astronomical feature columns
        astronomical_features = [col for col in combined_df.columns if col not in fbi_codes + ['date']]
        
        print(f"✓ FBI codes to analyze: {len(fbi_codes)}")
        print(f"✓ Astronomical features: {len(astronomical_features)}")
        print(f"✓ Including all minor planets/asteroids with proper Chicago timezone calculations")
        
        # Prepare feature matrices
        X_train = train_data[astronomical_features]
        X_test = test_data[astronomical_features]
        
        results = {}
        
        for fbi_code in fbi_codes:
            if fbi_code not in train_data.columns:
                continue
                
            # Create binary classification targets (high crime days)
            y_train = train_data[fbi_code]
            y_test = test_data[fbi_code]
            
            # Use 50th percentile as threshold for high crime days
            threshold = np.percentile(y_train[y_train > 0], 50) if np.sum(y_train > 0) > 10 else 1
            
            y_train_binary = (y_train >= threshold).astype(int)
            y_test_binary = (y_test >= threshold).astype(int)
            
            # Skip if not enough positive cases
            if np.sum(y_train_binary) < 10 or np.sum(y_test_binary) < 2:
                continue
            
            # Scale features
            scaler = StandardScaler()
            X_train_scaled = scaler.fit_transform(X_train)
            X_test_scaled = scaler.transform(X_test)
            
            # Train Random Forest
            model = RandomForestClassifier(
                n_estimators=100,
                max_depth=10,
                min_samples_split=10,
                random_state=42,
                class_weight='balanced'
            )
            
            model.fit(X_train_scaled, y_train_binary)
            y_pred = model.predict(X_test_scaled)
            
            # Calculate performance
            f1 = f1_score(y_test_binary, y_pred)
            
            results[fbi_code] = {
                'f1_score': f1,
                'threshold': threshold,
                'train_positive': np.sum(y_train_binary),
                'test_positive': np.sum(y_test_binary),
                'predictions': np.sum(y_pred),
                'model': model,
                'scaler': scaler,
                'feature_importance': dict(zip(astronomical_features, model.feature_importances_))
            }
            
            print(f"  {fbi_code}: F1={f1:.3f}, Threshold={threshold:.1f}, Train+={np.sum(y_train_binary)}, Test+={np.sum(y_test_binary)}")
        
        return results, combined_df
    
    def export_results(self, results, combined_df):
        """
        Export analysis results and data.
        """
        print("\n💾 Exporting results...")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Export performance summary
        performance_data = []
        for fbi_code, result in results.items():
            performance_data.append({
                'fbi_code': fbi_code,
                'f1_score': result['f1_score'],
                'threshold': result['threshold'],
                'train_positive_cases': result['train_positive'],
                'test_positive_cases': result['test_positive'],
                'predicted_positive': result['predictions']
            })
        
        performance_df = pd.DataFrame(performance_data)
        performance_file = f"enhanced_temporal_validation_results_{timestamp}.csv"
        performance_df.to_csv(performance_file, index=False)
        print(f"✓ Performance results: {performance_file}")
        
        # Export feature importance
        feature_importance_data = []
        for fbi_code, result in results.items():
            for feature, importance in result['feature_importance'].items():
                feature_importance_data.append({
                    'fbi_code': fbi_code,
                    'feature': feature,
                    'importance': importance
                })
        
        importance_df = pd.DataFrame(feature_importance_data)
        importance_file = f"enhanced_feature_importance_{timestamp}.csv"
        importance_df.to_csv(importance_file, index=False)
        print(f"✓ Feature importance: {importance_file}")
        
        # Export combined dataset
        combined_file = f"enhanced_combined_crime_astronomy_{timestamp}.csv"
        combined_df.to_csv(combined_file, index=False)
        print(f"✓ Combined dataset: {combined_file}")
        
        # Calculate and display summary statistics
        avg_f1 = np.mean([r['f1_score'] for r in results.values()])
        high_performers = sum(1 for r in results.values() if r['f1_score'] > 0.7)
        
        print(f"\n📈 ENHANCED ANALYSIS SUMMARY:")
        print(f"  Average F1 Score: {avg_f1:.3f}")
        print(f"  High Performers (F1 > 0.7): {high_performers}/{len(results)}")
        print(f"  FBI codes analyzed: {len(results)}")
        print(f"  Using accurate Chicago local time astronomical calculations")
        
        return performance_df, importance_df


def main():
    """
    Main analysis function.
    """
    print("🔍 Enhanced FBI Crime Analysis with Accurate Astronomy")
    print("=" * 60)
    
    analyzer = EnhancedFBICrimeAnalysis()
    
    # Load and process data
    crime_df = analyzer.load_and_process_crime_data()
    if crime_df is None:
        return
    
    # Aggregate to daily data
    daily_crime_df = analyzer.aggregate_daily_crime_data(crime_df)
    
    # Calculate astronomical features
    unique_dates = pd.to_datetime(daily_crime_df['date']).dt.normalize().unique()
    astronomical_df = analyzer.calculate_astronomical_features_for_dates(unique_dates)
    
    # Perform temporal validation
    results, combined_df = analyzer.perform_temporal_validation(daily_crime_df, astronomical_df)
    
    # Export results
    performance_df, importance_df = analyzer.export_results(results, combined_df)
    
    print("\n✅ Enhanced analysis complete!")
    print("🌟 Now using accurate astronomical calculations with Chicago local time")


if __name__ == "__main__":
    main()
