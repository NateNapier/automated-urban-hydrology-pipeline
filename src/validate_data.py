"""
Quick validation script to check synthetic data quality for Vadodara
"""
import pandas as pd
import matplotlib.pyplot as plt
import os

print("🚀 Step 1: Script started successfully.")

current_dir = os.getcwd()
print(f"📂 Current working directory: {current_dir}")

data_path = os.path.join(current_dir, 'data', 'raw', 'synthetic_imd_precipitation.csv')
output_path = os.path.join(current_dir, 'outputs', 'validation_annual_precipitation.png')

print(f" Looking for data at: {data_path}")

if not os.path.exists(data_path):
    print(f"❌ ERROR: Could not find the CSV file at {data_path}")
    print("💡 Fix: Make sure you ran the synthetic generator first.")
else:
    print("✅ CSV file found! Loading data...")
    
    df = pd.read_csv(data_path)
    df['date'] = pd.to_datetime(df['date'])
    
    annual_precip = df.groupby(df['date'].dt.year)['precipitation_mm'].sum()
    
    print("\n" + "="*60)
    print("DATA VALIDATION REPORT (VADODARA)")
    print("="*60)
    print(f"\nAnnual Precipitation Statistics:")
    print(f"  Mean: {annual_precip.mean():.1f} mm/year")
    print(f"  Median: {annual_precip.median():.1f} mm/year")
    print(f"  Min: {annual_precip.min():.1f} mm/year")
    print(f"  Max: {annual_precip.max():.1f} mm/year")
    
    print(f"\nExpected for Vadodara: 800-950 mm/year")
    print(f"Your data: {annual_precip.mean():.1f} mm/year")
    
    if 800 <= annual_precip.mean() <= 950:
        print("\n✅ Annual precipitation is perfectly calibrated!")
    else:
        print("\n⚠️  WARNING: Annual precipitation is outside the expected range.")
    
    extreme_events = df[df['precipitation_mm'] > 100]
    print(f"\nExtreme Events (>100mm/day):")
    print(f"  Count: {len(extreme_events)}")
    print(f"  Max: {extreme_events['precipitation_mm'].max():.1f} mm")
    
    print(f"\n Saving plot to: {output_path}")
    plt.figure(figsize=(14, 6))
    plt.plot(annual_precip.index, annual_precip.values, linewidth=1, alpha=0.7, color='steelblue')
    plt.axhline(y=850, color='red', linestyle='--', label='Target Mean (850mm)')
    plt.xlabel('Year')
    plt.ylabel('Annual Precipitation (mm)')
    plt.title('Vadodara Annual Precipitation - Validation Check')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    print("✅ Plot saved successfully!")