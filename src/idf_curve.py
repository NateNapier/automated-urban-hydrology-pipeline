"""
IDF Curve Statistical Engine
=============================
Takes daily precipitation data, extracts the Annual Maximum Series (AMS),
fits a Gumbel Extreme Value Distribution, and calculates Intensity-Duration-Frequency
(IDF) relationships for urban drainage design.
"""

import pandas as pd
import numpy as np
from scipy.stats import gumbel_r
import plotly.graph_objects as go
import os

class IDFCurveEngine:
    """Calculates IDF curves using the Gumbel Extreme Value Distribution."""
    
    def __init__(self, data_path='data/raw/synthetic_imd_precipitation.csv'):
        self.data_path = data_path
        self.df = None
        self.ams = None
        self.gumbel_params = {}
        
    def load_and_preprocess(self):
        """Load data and ensure datetime formatting."""
        print("📂 Loading precipitation data...")
        self.df = pd.read_csv(self.data_path)
        self.df['date'] = pd.to_datetime(self.df['date'])
        print(f"✓ Loaded {len(self.df)} records.")
        
    def extract_annual_maximum_series(self):
        """Extract the maximum daily rainfall for each year (AMS)."""
        print("📊 Extracting Annual Maximum Series (AMS)...")
        self.df['year'] = self.df['date'].dt.year
        self.ams = self.df.groupby('year')['precipitation_mm'].max().reset_index()
        self.ams = self.ams.rename(columns={'precipitation_mm': 'max_daily_rainfall_mm'})
        print(f"✓ Extracted {len(self.ams)} annual maximums (Years: {self.ams['year'].min()} - {self.ams['year'].max()})")
        
    def fit_gumbel_distribution(self):
        """Fit the Gumbel (Extreme Value Type I) distribution to the AMS."""
        print("📐 Fitting Gumbel Extreme Value Distribution...")
        data = self.ams['max_daily_rainfall_mm'].values
        
        # Fit the distribution: returns location (mu) and scale (beta) parameters
        loc, scale = gumbel_r.fit(data)
        self.gumbel_params = {'loc': loc, 'scale': scale}
        
        print(f"✓ Gumbel Parameters -> Location (μ): {loc:.2f}, Scale (β): {scale:.2f}")
        
    def calculate_return_periods(self, return_periods=[2, 5, 10, 25, 50, 100]):
        """
        Calculate the expected rainfall depth for specific return periods (T).
        Formula: X_T = μ + β * [-ln(-ln(1 - 1/T))]
        """
        print("🌧️ Calculating return period depths...")
        results = []
        
        for T in return_periods:
            # Gumbel reduced variate
            y_T = -np.log(-np.log(1 - (1 / T)))
            
            # Expected rainfall depth (mm)
            depth_mm = self.gumbel_params['loc'] + (self.gumbel_params['scale'] * y_T)
            
            # Intensity (mm/hr) for a 24-hour duration
            duration_hours = 24
            intensity_mm_hr = depth_mm / duration_hours
            
            results.append({
                'Return_Period_Years': T,
                'Probability_of_Exceedance': f"{(1/T)*100:.1f}%",
                'Expected_Depth_24h_mm': round(depth_mm, 1),
                'Expected_Intensity_24h_mm_hr': round(intensity_mm_hr, 2)
            })
            
        self.idf_table = pd.DataFrame(results)
        print("✓ Return period calculations complete.")
        return self.idf_table
        
    def save_results(self, output_path='data/processed/idf_curve_results.csv'):
        """Save the IDF table to a processed CSV."""
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        self.idf_table.to_csv(output_path, index=False)
        print(f"💾 Saved IDF results to {output_path}")
        
    def plot_idf_curve(self, output_path='outputs/idf_curve_gumbel.html'):
        """Generate an interactive Plotly chart of the IDF curve."""
        print("📈 Generating interactive IDF curve plot...")
        
        fig = go.Figure()
        
        # Add scatter points for the calculated return periods
        fig.add_trace(go.Scatter(
            x=self.idf_table['Return_Period_Years'],
            y=self.idf_table['Expected_Depth_24h_mm'],
            mode='lines+markers',
            name='24-Hour Rainfall Depth',
            line=dict(color='royalblue', width=3),
            marker=dict(size=8, color='royalblue'),
            hovertemplate="<b>Return Period:</b> %{x} Years<br>" +
                          "<b>Expected Depth:</b> %{y} mm<br>" +
                          "<b>Intensity:</b> " + self.idf_table['Expected_Intensity_24h_mm_hr'].astype(str) + " mm/hr<extra></extra>"
        ))
        
        # Format the layout for a professional engineering report
        fig.update_layout(
            title=dict(
                text='Intensity-Duration-Frequency (IDF) Curve - Vadodara, Gujarat<br><sup>Based on 101-Year Synthetic AMS & Gumbel Extreme Value Distribution</sup>',
                x=0.5,
                font=dict(size=16)
            ),
            xaxis_title='Return Period (Years) [Log Scale]',
            yaxis_title='Expected 24-Hour Rainfall Depth (mm)',
            xaxis_type='log',  # Log scale is standard for IDF curves
            xaxis=dict(
                tickmode='array',
                tickvals=[2, 5, 10, 25, 50, 100],
                ticktext=['2-yr', '5-yr', '10-yr', '25-yr', '50-yr', '100-yr']
            ),
            template='plotly_white',
            height=600,
            width=900
        )
        
        # Save as interactive HTML (can be opened in any browser)
        fig.write_html(output_path)
        print(f"💾 Saved interactive plot to {output_path}")
        print("   👉 Open this file in your web browser to interact with the chart!")

if __name__ == "__main__":
    # Initialize the engine
    engine = IDFCurveEngine()
    
    # Run the pipeline
    engine.load_and_preprocess()
    engine.extract_annual_maximum_series()
    engine.fit_gumbel_distribution()
    idf_df = engine.calculate_return_periods()
    
    # Display the final table in the terminal
    print("\n" + "="*70)
    print("FINAL IDF CURVE RESULTS (24-Hour Duration)")
    print("="*70)
    print(idf_df.to_string(index=False))
    print("="*70)
    
    # Save outputs
    engine.save_results()
    engine.plot_idf_curve()