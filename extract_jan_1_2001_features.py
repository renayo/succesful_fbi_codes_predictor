#!/usr/bin/env python3
"""
Extract all 132 astronomical features for January 1, 2001 at noon Chicago time.
"""

from accurate_astronomical_calculator import AccurateAstronomicalCalculator
from datetime import datetime
import pandas as pd

def get_jan_1_2001_features():
    """Get all 132 astronomical features for Jan 1, 2001 noon Chicago."""
    print("🌌 Extracting 132 Astronomical Features")
    print("Date: January 1, 2001 at noon Chicago time")
    print("=" * 60)
    
    calc = AccurateAstronomicalCalculator()
    target_date = datetime(2001, 1, 1, 12, 0, 0)  # Noon Chicago time
    
    features = calc.calculate_features(target_date)
    
    print(f"Total features calculated: {len(features)}")
    print("\n📊 COMPLETE FEATURE SET WITH VALUES:")
    print("=" * 60)
    
    # Create a structured display
    feature_categories = {
        "🌟 Traditional Planetary Longitudes": [
            'sun_longitude', 'moon_longitude', 'mercury_longitude', 'venus_longitude',
            'mars_longitude', 'jupiter_longitude', 'saturn_longitude', 'uranus_longitude',
            'neptune_longitude', 'pluto_longitude'
        ],
        
        "🏠 Astrological House System": [
            'ascendant', 'midheaven', 'north_node', 'south_node'
        ],
        
        "🌙 Lunar Properties": [
            'moon_phase', 'moon_distance'
        ],
        
        "⚡ Special Astronomical Indicators": [
            'mercury_retrograde', 'eclipse_proximity'
        ],
        
        "📐 Planetary Aspects": [
            'conjunctions', 'oppositions', 'squares'
        ],
        
        "👑 Planetary Dignities": [
            'sun_dignity', 'moon_dignity', 'mercury_dignity'
        ]
    }
    
    # Display categorized features
    feature_count = 0
    for category, feature_list in feature_categories.items():
        print(f"\n{category}:")
        for feature in feature_list:
            if feature in features:
                value = features[feature]
                if feature.endswith('_longitude') or feature in ['ascendant', 'midheaven', 'north_node', 'south_node']:
                    print(f"  {feature}: {value:.3f}°")
                elif feature == 'moon_phase':
                    print(f"  {feature}: {value:.3f}")
                elif feature == 'moon_distance':
                    print(f"  {feature}: {value:.0f} km")
                elif feature == 'eclipse_proximity':
                    print(f"  {feature}: {value:.0f} days")
                else:
                    print(f"  {feature}: {value}")
                feature_count += 1
    
    # Display minor planet categories
    minor_planet_categories = [
        'aggression', 'mayhem', 'explosive', 'victims_pain', 'death',
        'firearms', 'knives', 'prostitution', 'drugs', 'money',
        'fire', 'obstacles', 'dishonesty', 'computer', 'law_justice', 'localization'
    ]
    
    print(f"\n🪨 MINOR PLANET INDIVIDUAL LONGITUDES:")
    for category in minor_planet_categories:
        category_features = [k for k in features.keys() if k.startswith(f"{category}_") and k.endswith("_longitude")]
        if category_features:
            print(f"\n  {category.upper()} Category:")
            for feature in sorted(category_features):
                planet_name = feature.replace(f"{category}_", "").replace("_longitude", "")
                print(f"    {planet_name}: {features[feature]:.3f}°")
                feature_count += 1
    
    print(f"\n🎯 MINOR PLANET COMPOSITE VALUES:")
    for category in minor_planet_categories:
        composite_key = f"{category}_composite"
        if composite_key in features:
            print(f"  {category}_composite: {features[composite_key]:.3f}°")
            feature_count += 1
    
    print(f"\n" + "=" * 60)
    print(f"✅ TOTAL FEATURES DISPLAYED: {feature_count}")
    print(f"📅 Date: {target_date.strftime('%B %d, %Y at %I:%M %p')} Chicago Time")
    
    # Create a DataFrame for easy export
    df = pd.DataFrame([features]).T
    df.columns = ['Value']
    df.index.name = 'Feature'
    
    # Export to CSV
    output_file = "jan_1_2001_astronomical_features.csv"
    df.to_csv(output_file)
    print(f"💾 Exported to: {output_file}")
    
    return features, df

if __name__ == "__main__":
    features, df = get_jan_1_2001_features()
