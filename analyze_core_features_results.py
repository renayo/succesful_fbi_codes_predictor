#!/usr/bin/env python3
"""
Analysis of Core Features Only Results (No Composites, Aspects, or Dignities)
============================================================================
"""

import pandas as pd

# Load the core features results
results_core = pd.read_csv('enhanced_temporal_validation_results_20250827_212653.csv')

print("🎯 FBI Crime Analysis - CORE ASTRONOMICAL FEATURES ONLY")
print("=" * 70)
print("(No Composites, No Aspects, No Dignities - Pure Celestial Positions)")
print(f"Total FBI codes analyzed: {len(results_core)}")
print(f"Average F1 Score: {results_core['f1_score'].mean():.3f}")
print(f"Total features: 110 (down from 116)")
print()

# Sort by F1 score
results_sorted = results_core.sort_values('f1_score', ascending=False)

print("🏆 FBI Code Performance Rankings (Core Features Only):")
print("-" * 75)
print("Rank | FBI Code | F1 Score | Threshold | Performance | vs No-Comp | vs Comp")
print("-" * 75)

# Previous results for comparison
no_comp_results = {  # No composites but had aspects/dignities
    '15': 0.910, '02': 0.766, '04A': 0.765, '08A': 0.759, '07': 0.604,
    '04B': 0.559, '17': 0.536, '20': 0.462, '01A': 0.394, '09': 0.343,
    '06': 0.157, '08B': 0.077, '10': 0.000, '11': 0.000, '12': 0.000,
    '14': 0.000, '13': 0.000, '22': 0.000, '24': 0.000
}

comp_results = {  # Original with composites
    '15': 0.860, '04A': 0.765, '02': 0.692, '08A': 0.664, '04B': 0.543,
    '07': 0.526, '17': 0.519, '14': 0.258, '20': 0.254, '06': 0.149,
    '08B': 0.148, '01A': 0.073, '13': 0.038, '10': 0.032, '24': 0.019,
    '11': 0.000, '09': 0.000, '12': 0.000, '22': 0.000
}

for i, (_, row) in enumerate(results_sorted.iterrows(), 1):
    fbi_code = row['fbi_code']
    f1 = row['f1_score']
    threshold = row['threshold']
    
    # Performance emoji
    if f1 > 0.7:
        emoji = "🔥 EXCELLENT"
    elif f1 > 0.6:
        emoji = "⭐ VERY GOOD"
    elif f1 > 0.4:
        emoji = "📊 GOOD"
    elif f1 > 0.2:
        emoji = "📈 MODERATE"
    else:
        emoji = "⚠️ POOR"
    
    # Calculate improvements
    no_comp_f1 = no_comp_results.get(fbi_code, 0)
    comp_f1 = comp_results.get(fbi_code, 0)
    
    no_comp_change = f1 - no_comp_f1
    comp_change = f1 - comp_f1
    
    if no_comp_change > 0:
        no_comp_text = f"↗️{no_comp_change:+.3f}"
    elif no_comp_change < 0:
        no_comp_text = f"↘️{no_comp_change:.3f}"
    else:
        no_comp_text = "➡️ same"
    
    if comp_change > 0:
        comp_text = f"↗️{comp_change:+.3f}"
    elif comp_change < 0:
        comp_text = f"↘️{comp_change:.3f}"
    else:
        comp_text = "➡️ same"
    
    print(f"{i:2d}   | {fbi_code:8s} | {f1:8.3f} | {threshold:9.1f} | {emoji:13s} | {no_comp_text:8s} | {comp_text:8s}")

print()

# Performance categories
excellent = results_core[results_core['f1_score'] > 0.7]
very_good = results_core[(results_core['f1_score'] > 0.6) & (results_core['f1_score'] <= 0.7)]
good = results_core[(results_core['f1_score'] > 0.4) & (results_core['f1_score'] <= 0.6)]
moderate = results_core[(results_core['f1_score'] > 0.2) & (results_core['f1_score'] <= 0.4)]
poor = results_core[results_core['f1_score'] <= 0.2]

print("📈 Performance Summary Comparison:")
print("-" * 65)
print("Category        | Core Only | No-Comp | With-Comp | Trend")
print("-" * 65)
print(f"🔥 Excellent >0.7  |    {len(excellent):2d}     |    4    |     1     | 📉 Declined")
print(f"⭐ Very Good 0.6-0.7|    {len(very_good):2d}     |    1    |     3     | 📉 Declined") 
print(f"📊 Good 0.4-0.6     |    {len(good):2d}     |    3    |     3     | ➡️ Stable")
print(f"📈 Moderate 0.2-0.4 |    {len(moderate):2d}     |    2    |     2     | ➡️ Stable")
print(f"⚠️ Poor ≤0.2       |   {len(poor):2d}     |    9    |    10     | 📈 Worse")
print()

print("🔍 Key Insights from Removing Aspects & Dignities:")
print("-" * 55)

# Compare averages
core_avg = results_core['f1_score'].mean()
no_comp_avg = 0.333
comp_avg = 0.292

print(f"📊 Average F1 Performance:")
print(f"   Core Features Only: {core_avg:.3f}")
print(f"   No Composites:      {no_comp_avg:.3f} (↗️ {no_comp_avg-core_avg:+.3f})")
print(f"   With Composites:    {comp_avg:.3f} (↗️ {comp_avg-core_avg:+.3f})")
print()

print("🎯 Analysis Conclusion:")
if core_avg < no_comp_avg:
    print("   ↘️ Removing aspects & dignities DECREASED performance")
    print("   📈 Aspects & dignities contain useful predictive information")
    print("   🔄 Recommendation: RESTORE aspects & dignities for optimal results")
else:
    print("   ↗️ Core features maintain strong performance")
    print("   ✅ Simplification successful without major loss")

print()
print("📋 Feature Count Comparison:")
print(f"   With Composites + Aspects + Dignities: 132 features")
print(f"   No Composites but Aspects + Dignities: 116 features")  
print(f"   Core Features Only: 110 features")
print()
print("🌟 Optimal Configuration Discovery:")
print("   🥇 Best: Individual features + Aspects + Dignities (F1=0.333)")
print("   🥈 Good: Individual features only (F1=0.312)")  
print("   🥉 Baseline: With composites (F1=0.292)")
