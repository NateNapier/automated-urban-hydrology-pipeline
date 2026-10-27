"""
Synthetic IMD Precipitation Data Generator (Vadodara, Gujarat)
================================================================
Generates statistically realistic daily precipitation data for Vadodara 
spanning 100 years, incorporating:
- Semi-arid monsoon seasonality
- Zero-inflation (dry days)
- Gamma-distributed normal rainfall
- Generalized Pareto-distributed extreme cloudburst events
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from scipy import stats
import os

class SyntheticPrecipitationGenerator:
    """Generates synthetic daily precipitation data with realistic statistical properties."""
    
    def __init__(self, start_year=1926, end_year=2026, latitude=22.3072, longitude=73.1812):
        self.start_year = start_year
        self.end_year = end_year
        self.latitude = latitude
        self.longitude = longitude
        
        # CALIBRATED PARAMETERS FOR VADODARA, GUJARAT
        # Target Annual Mean: ~850 mm
        self.seasonal_params = {
            'monsoon': {
                'months': [6, 7, 8, 9],
                'wet_day_probability': 0.50,
                'gamma_shape': 1.8,
                'gamma_scale': 5.5,
                'extreme_threshold': 45.0,
                'extreme_probability': 0.05,
                'pareto_shape': 0.25,
                'pareto_scale': 25.0,
                'pareto_loc': 45.0
            },
            'post_monsoon': {
                'months': [10, 11],
                'wet_day_probability': 0.10,
                'gamma_shape': 1.2,
                'gamma_scale': 4.0,
                'extreme_threshold': 30.0,
                'extreme_probability': 0.01,
                'pareto_shape': 0.3,
                'pareto_scale': 15.0,
                'pareto_loc': 30.0
            },
            'winter': {
                'months': [12, 1, 2],
                'wet_day_probability': 0.02,
                'gamma_shape': 1.0,
                'gamma_scale': 3.0,
                'extreme_threshold': 15.0,
                'extreme_probability': 0.005,
                'pareto_shape': 0.4,
                'pareto_scale': 8.0,
                'pareto_loc': 15.0
            },
            'summer': {
                'months': [3, 4, 5],
                'wet_day_probability': 0.04,
                'gamma_shape': 1.0,
                'gamma_scale': 4.0,
                'extreme_threshold': 25.0,
                'extreme_probability': 0.01,
                'pareto_shape': 0.35,
                'pareto_scale': 12.0,
                'pareto_loc': 25.0
            }
        }
        
        # Physical limit for Vadodara cloudbursts (mm)
        self.max_daily_rainfall_cap = 280.0
        np.random.seed(42)

    def _get_season_for_month(self, month):
        for season, params in self.seasonal_params.items():
            if month in params['months']:
                return season
        return 'monsoon'

    def _generate_daily_precipitation_for_month(self, year, month):
        if month in [1, 3, 5, 7, 8, 10, 12]:
            num_days = 31
        elif month in [4, 6, 9, 11]:
            num_days = 30
        else:
            num_days = 29 if (year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)) else 28
        
        season = self._get_season_for_month(month)
        params = self.seasonal_params[season]
        daily_precip = np.zeros(num_days)
        
        wet_day_mask = np.random.random(num_days) < params['wet_day_probability']
        is_extreme = np.random.random(num_days) < params['extreme_probability']
        
        for day_idx in range(num_days):
            if wet_day_mask[day_idx]:
                if is_extreme[day_idx]:
                    extreme_value = stats.genpareto.rvs(
                        c=params['pareto_shape'],
                        loc=params['pareto_loc'],
                        scale=params['pareto_scale']
                    )
                    daily_precip[day_idx] = extreme_value
                else:
                    normal_value = stats.gamma.rvs(
                        a=params['gamma_shape'],
                        loc=0,
                        scale=params['gamma_scale']
                    )
                    daily_precip[day_idx] = normal_value
            else:
                daily_precip[day_idx] = 0.0
        
        # Apply physical limit
        daily_precip = np.clip(daily_precip, 0, self.max_daily_rainfall_cap)
        return daily_precip

    def generate_full_dataset(self):
        all_dates = []
        all_precip = []
        
        print(f"Generating synthetic precipitation data for Vadodara ({self.start_year}-{self.end_year})...")
        
        for year in range(self.start_year, self.end_year + 1):
            for month in range(1, 13):
                daily_precip = self._generate_daily_precipitation_for_month(year, month)
                
                next_month = 1 if month == 12 else month + 1
                next_year = year + 1 if month == 12 else year
                
                start_date = datetime(year, month, 1)
                end_date = datetime(next_year, next_month, 1) - timedelta(days=1)
                date_range = pd.date_range(start=start_date, end=end_date, freq='D')
                
                all_dates.extend(date_range)
                all_precip.extend(daily_precip)
            
            if (year - self.start_year) % 10 == 0:
                print(f"  Generated data for year {year}")
        
        df = pd.DataFrame({
            'date': all_dates,
            'precipitation_mm': all_precip,
            'latitude': self.latitude,
            'longitude': self.longitude
        })
        
        df['precipitation_mm'] = df['precipitation_mm'].round(1)
        print(f"✓ Generated {len(df)} days of precipitation data")
        print(f"✓ Annual mean precipitation: {df.groupby(df['date'].dt.year)['precipitation_mm'].sum().mean():.1f} mm")
        
        return df

    def save_to_csv(self, df, output_path='data/raw/synthetic_imd_precipitation.csv'):
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        df.to_csv(output_path, index=False)
        print(f"✓ Saved dataset to {output_path}")
        print(f"  File size: {os.path.getsize(output_path) / (1024*1024):.2f} MB")

if __name__ == "__main__":
    generator = SyntheticPrecipitationGenerator()
    df = generator.generate_full_dataset()
    generator.save_to_csv(df)
    
    print("\n" + "="*60)
    print("DATASET SUMMARY STATISTICS")
    print("="*60)
    print(f"Total records: {len(df):,}")
    print(f"Date range: {df['date'].min()} to {df['date'].max()}")
    print(f"\nPrecipitation statistics (mm/day):")
    print(f"  Mean: {df['precipitation_mm'].mean():.2f}")
    print(f"  Max: {df['precipitation_mm'].max():.2f}")
    print(f"  Days with >50mm rain: {(df['precipitation_mm'] > 50).sum():,}")