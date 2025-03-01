import pandas as pd
import numpy as np
from pathlib import Path

def load_and_preprocess_data():
    """
    Load and preprocess the nutrition dataset
    """
    # Get the data path
    data_path = Path(__file__).parents[1] / "data" / "nutrition.csv"
    
    # Load the data
    df = pd.read_csv(data_path)
    
    # Basic cleaning
    df = df.dropna()  # Remove any null values
    
    # Create derived features
    df['protein_ratio'] = df['protein'] / df['calories']
    df['fat_ratio'] = df['fat'] / df['calories']
    df['carb_ratio'] = df['carbohydrates'] / df['calories']
    
    # Create nutrient density score (higher is better)
    df['nutrient_density'] = (
        (df['protein'] * 4) +  # 4 calories per gram of protein
        (df['carbohydrates'] * 4) +  # 4 calories per gram of carbs
        (df['fat'] * 9)  # 9 calories per gram of fat
    ) / df['calories']
    
    return df

def get_food_category_stats(df):
    """
    Calculate statistics for each food category
    """
    stats = df.groupby('category').agg({
        'calories': ['mean', 'std'],
        'protein': ['mean', 'std'],
        'fat': ['mean', 'std'],
        'carbohydrates': ['mean', 'std']
    }).round(2)
    
    return stats

def get_healthy_foods(df, criteria='balanced'):
    """
    Get list of healthy foods based on different criteria
    
    Parameters:
    -----------
    criteria : str
        'balanced' - foods with good balance of nutrients
        'high_protein' - foods with high protein content
        'low_calorie' - foods with low calories
    """
    if criteria == 'balanced':
        return df[
            (df['protein_ratio'] >= 0.15) &  # At least 15% protein
            (df['fat_ratio'] <= 0.30) &      # No more than 30% fat
            (df['carb_ratio'] <= 0.55)       # No more than 55% carbs
        ]
    elif criteria == 'high_protein':
        return df[df['protein_ratio'] >= 0.25]  # At least 25% protein
    elif criteria == 'low_calorie':
        return df[df['calories'] <= df['calories'].quantile(0.25)]  # Bottom 25% calories
    
    return df
