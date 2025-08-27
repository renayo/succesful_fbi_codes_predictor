#!/usr/bin/env python3
"""
Top 10 Astronomical Features per FBI Code Classifier
===================================================
Analysis of feature importance for 50% percentile threshold results
"""

import pandas as pd

# Load feature importance data
feature_importance = pd.read_csv('enhanced_feature_importance_20250827_132115.csv')
performance_results = pd.read_csv('enhanced_temporal_validation_results_20250827_132115.csv')

print("🌟 Top 10 Astronomical Features per FBI Code Classifier")
print("=" * 70)
print("(Based on 50% percentile threshold results)")
print()

# Sort performance results by F1 score
performance_sorted = performance_results.sort_values('f1_score', ascending=False)

# For each FBI code, show top 10 features
for _, perf_row in performance_sorted.iterrows():
    fbi_code = perf_row['fbi_code']
    f1_score = perf_row['f1_score']
    
    # Get features for this FBI code
    code_features = feature_importance[feature_importance['fbi_code'] == fbi_code]
    
    if len(code_features) == 0:
        continue
    
    # Sort by importance and get top 10
    top_features = code_features.sort_values('importance', ascending=False).head(10)
    
    # Performance emoji
    if f1_score > 0.8:
        emoji = "🔥"
    elif f1_score > 0.6:
        emoji = "⭐"
    elif f1_score > 0.4:
        emoji = "📊"
    elif f1_score > 0.2:
        emoji = "📈"
    else:
        emoji = "⚠️"
    
    print(f"{emoji} FBI Code {fbi_code} (F1: {f1_score:.3f})")
    print("-" * 50)
    
    for i, (_, row) in enumerate(top_features.iterrows(), 1):
        feature_name = row['feature']
        importance = row['importance']
        
        # Categorize feature type
        if 'composite' in feature_name:
            feature_type = "🎭 Composite"
        elif any(planet in feature_name for planet in ['sun', 'moon', 'mercury', 'venus', 'mars', 'jupiter', 'saturn', 'uranus', 'neptune', 'pluto']):
            feature_type = "🪐 Major Planet"
        elif 'localization' in feature_name:
            feature_type = "🏙️ Chicago-specific"
        elif any(term in feature_name for term in ['aggression', 'violence', 'mayhem']):
            feature_type = "⚔️ Aggression"
        elif any(term in feature_name for term in ['death', 'victims', 'pain']):
            feature_type = "💀 Violence/Death"
        elif any(term in feature_name for term in ['explosive', 'firearms', 'knives']):
            feature_type = "💥 Weapons"
        elif any(term in feature_name for term in ['drugs', 'prostitution']):
            feature_type = "🚫 Vice"
        elif any(term in feature_name for term in ['money', 'dishonesty']):
            feature_type = "💰 Financial"
        elif any(term in feature_name for term in ['fire', 'obstacles']):
            feature_type = "🔥 Destructive"
        elif any(term in feature_name for term in ['computer', 'law_justice']):
            feature_type = "⚖️ Legal/Tech"
        else:
            feature_type = "🌌 Other"
        
        print(f"  {i:2d}. {feature_type} {feature_name:<35} ({importance:.4f})")
    
    print()

print("📊 Feature Type Legend:")
print("🎭 Composite = Average of multiple related features")
print("🪐 Major Planet = Traditional planetary positions")
print("🏙️ Chicago-specific = Local astronomical bodies")
print("⚔️ Aggression = Violence-related minor planets")
print("💀 Violence/Death = Death/victim-related bodies")
print("💥 Weapons = Weapon/explosive-related bodies")
print("🚫 Vice = Drug/prostitution-related bodies")
print("💰 Financial = Money/fraud-related bodies")
print("🔥 Destructive = Fire/obstacle-related bodies")
print("⚖️ Legal/Tech = Justice/computer-related bodies")
print("🌌 Other = Miscellaneous astronomical features")
