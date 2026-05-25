#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Aggressive Driving Analysis Pipeline

This script implements a complete pipeline for analyzing driving behavior data
and detecting aggressive driving events using anomaly detection techniques.

The pipeline consists of three main stages:
1. Data Preprocessing: Clean and prepare driving data for analysis
2. Anomaly Detection: Identify abrupt changes in driving patterns
3. Event Classification: Classify detected anomalies as aggressive driving events

Author: Xingqiang Chen
Created: 2019-03-27
Updated: 2024-09-03
"""

from anomaly_detection.applications.driving.config import first_time, only_evaluation
from anomaly_detection.applications.driving.driving_data_preprocess import apply_preprocess
from anomaly_detection.applications.driving.find_aggressive_driving_event import find_event
from anomaly_detection.applications.driving.parallel_aggressive_driving_detection import apply_detection


def main():
    """
    Main execution function for the aggressive driving analysis pipeline.
    
    This function orchestrates the entire analysis process:
    - Data preprocessing (if running for the first time)
    - Anomaly detection (unless only evaluation is requested)
    - Event classification and analysis
    """
    print("=" * 60)
    print("🚗 AGGRESSIVE DRIVING ANALYSIS PIPELINE")
    print("=" * 60)
    
    # Stage 1: Data Preprocessing
    if first_time:
        print("\n📊 STAGE 1: DATA PREPROCESSING")
        print("-" * 40)
        print("🔄 Running data preprocessing for the first time...")
        apply_preprocess()
        print("✅ Data preprocessing completed successfully!")
    else:
        print("\n📊 STAGE 1: DATA PREPROCESSING")
        print("-" * 40)
        print("⏭️  Skipping data preprocessing (not first time run)")
    
    # Stage 2: Anomaly Detection
    if not only_evaluation:
        print("\n🔍 STAGE 2: ANOMALY DETECTION")
        print("-" * 40)
        print("🚀 Running abrupt-change detection algorithms...")
        apply_detection()
        print("✅ Anomaly detection completed successfully!")
    else:
        print("\n🔍 STAGE 2: ANOMALY DETECTION")
        print("-" * 40)
        print("⏭️  Skipping anomaly detection (evaluation mode only)")
    
    # Stage 3: Event Classification
    print("\n🎯 STAGE 3: EVENT CLASSIFICATION")
    print("-" * 40)
    print("🔍 Analyzing and classifying driving events...")
    find_event()
    print("✅ Event classification completed successfully!")
    
    print("\n" + "=" * 60)
    print("🎉 PIPELINE EXECUTION COMPLETED SUCCESSFULLY!")
    print("=" * 60)
    print("\n📋 Summary of completed stages:")
    if first_time:
        print("   ✅ Data Preprocessing")
    if not only_evaluation:
        print("   ✅ Anomaly Detection")
    print("   ✅ Event Classification")
    print("\n📊 Results are available in the output directories.")
    print("📚 Check the documentation for detailed analysis of results.")


if __name__ == '__main__':
    main()
