"""
Data loading and preprocessing utilities for anomaly detection.

This module provides convenient functions for loading various data formats
and preprocessing data for anomaly detection tasks.
"""

import numpy as np
import pandas as pd
from typing import Union, Tuple, Optional
from pathlib import Path


def load_data(filepath: Union[str, Path], **kwargs) -> Union[np.ndarray, pd.DataFrame]:
    """
    Load data from various file formats.
    
    Parameters
    ----------
    filepath : str or Path
        Path to the data file.
        
    **kwargs : dict
        Additional arguments passed to the loader function.
        
    Returns
    -------
    np.ndarray or pd.DataFrame
        Loaded data.
        
    Examples
    --------
    >>> data = load_data('data.csv')
    >>> data = load_data('data.npy')
    >>> data = load_data('data.parquet')
    """
    filepath = Path(filepath)
    
    if not filepath.exists():
        raise FileNotFoundError(f"File not found: {filepath}")
    
    suffix = filepath.suffix.lower()
    
    if suffix == '.csv':
        return pd.read_csv(filepath, **kwargs)
    elif suffix == '.parquet':
        return pd.read_parquet(filepath, **kwargs)
    elif suffix == '.npy':
        return np.load(filepath, **kwargs)
    elif suffix == '.npz':
        data = np.load(filepath, **kwargs)
        # Return the first array if multiple arrays in npz
        return data[list(data.keys())[0]]
    elif suffix in ['.xlsx', '.xls']:
        return pd.read_excel(filepath, **kwargs)
    elif suffix == '.json':
        return pd.read_json(filepath, **kwargs)
    else:
        raise ValueError(f"Unsupported file format: {suffix}")


def to_numpy(data: Union[np.ndarray, pd.DataFrame, pd.Series]) -> np.ndarray:
    """
    Convert various data formats to numpy array.
    
    Parameters
    ----------
    data : array-like
        Data to convert.
        
    Returns
    -------
    np.ndarray
        Data as numpy array.
        
    Examples
    --------
    >>> df = pd.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]})
    >>> arr = to_numpy(df)
    >>> arr.shape
    (3, 2)
    """
    if isinstance(data, np.ndarray):
        return data
    elif isinstance(data, (pd.DataFrame, pd.Series)):
        return data.values
    else:
        return np.array(data)


def normalize_data(X: np.ndarray, method: str = 'standard') -> Tuple[np.ndarray, dict]:
    """
    Normalize data using various methods.
    
    Parameters
    ----------
    X : np.ndarray
        Data to normalize, shape (n_samples, n_features).
        
    method : str, default='standard'
        Normalization method. Options:
        - 'standard': Standardization (zero mean, unit variance)
        - 'minmax': Min-max scaling to [0, 1]
        - 'robust': Robust scaling using median and IQR
        - 'l2': L2 normalization (unit norm)
        
    Returns
    -------
    X_normalized : np.ndarray
        Normalized data.
        
    params : dict
        Normalization parameters for inverse transform.
        
    Examples
    --------
    >>> X = np.array([[1, 2], [3, 4], [5, 6]])
    >>> X_norm, params = normalize_data(X, method='standard')
    """
    if method == 'standard':
        mean = np.mean(X, axis=0)
        std = np.std(X, axis=0)
        std[std == 0] = 1.0  # Avoid division by zero
        X_normalized = (X - mean) / std
        params = {'method': 'standard', 'mean': mean, 'std': std}
        
    elif method == 'minmax':
        min_val = np.min(X, axis=0)
        max_val = np.max(X, axis=0)
        range_val = max_val - min_val
        range_val[range_val == 0] = 1.0
        X_normalized = (X - min_val) / range_val
        params = {'method': 'minmax', 'min': min_val, 'max': max_val}
        
    elif method == 'robust':
        median = np.median(X, axis=0)
        q75 = np.percentile(X, 75, axis=0)
        q25 = np.percentile(X, 25, axis=0)
        iqr = q75 - q25
        iqr[iqr == 0] = 1.0
        X_normalized = (X - median) / iqr
        params = {'method': 'robust', 'median': median, 'iqr': iqr}
        
    elif method == 'l2':
        norms = np.linalg.norm(X, axis=1, keepdims=True)
        norms[norms == 0] = 1.0
        X_normalized = X / norms
        params = {'method': 'l2'}
        
    else:
        raise ValueError(f"Unknown normalization method: {method}")
    
    return X_normalized, params


def denormalize_data(X_normalized: np.ndarray, params: dict) -> np.ndarray:
    """
    Reverse normalization using saved parameters.
    
    Parameters
    ----------
    X_normalized : np.ndarray
        Normalized data.
        
    params : dict
        Normalization parameters from normalize_data().
        
    Returns
    -------
    np.ndarray
        Original scale data.
        
    Examples
    --------
    >>> X_norm, params = normalize_data(X, method='standard')
    >>> X_recovered = denormalize_data(X_norm, params)
    """
    method = params['method']
    
    if method == 'standard':
        return X_normalized * params['std'] + params['mean']
    elif method == 'minmax':
        range_val = params['max'] - params['min']
        return X_normalized * range_val + params['min']
    elif method == 'robust':
        return X_normalized * params['iqr'] + params['median']
    elif method == 'l2':
        return X_normalized
    else:
        raise ValueError(f"Unknown normalization method: {method}")


def train_test_split_time_series(X: np.ndarray, train_size: float = 0.7,
                                   shuffle: bool = False) -> Tuple[np.ndarray, np.ndarray]:
    """
    Split time series data into train and test sets.
    
    Parameters
    ----------
    X : np.ndarray
        Time series data, shape (n_samples, n_features).
        
    train_size : float, default=0.7
        Proportion of data for training (between 0 and 1).
        
    shuffle : bool, default=False
        Whether to shuffle data before splitting. 
        Usually False for time series to preserve temporal order.
        
    Returns
    -------
    X_train : np.ndarray
        Training data.
        
    X_test : np.ndarray
        Testing data.
        
    Examples
    --------
    >>> X = np.random.randn(1000, 3)
    >>> X_train, X_test = train_test_split_time_series(X, train_size=0.7)
    >>> X_train.shape
    (700, 3)
    """
    if not 0 < train_size < 1:
        raise ValueError("train_size must be between 0 and 1")
    
    n_samples = len(X)
    split_idx = int(n_samples * train_size)
    
    if shuffle:
        indices = np.random.permutation(n_samples)
        X = X[indices]
    
    X_train = X[:split_idx]
    X_test = X[split_idx:]
    
    return X_train, X_test


def create_sliding_windows(X: np.ndarray, window_size: int, 
                           stride: int = 1) -> np.ndarray:
    """
    Create sliding windows from time series data.
    
    Parameters
    ----------
    X : np.ndarray
        Time series data, shape (n_samples, n_features).
        
    window_size : int
        Size of each window.
        
    stride : int, default=1
        Step size between windows.
        
    Returns
    -------
    np.ndarray
        Windows of shape (n_windows, window_size, n_features).
        
    Examples
    --------
    >>> X = np.arange(10).reshape(-1, 1)
    >>> windows = create_sliding_windows(X, window_size=3, stride=1)
    >>> windows.shape
    (8, 3, 1)
    """
    if window_size > len(X):
        raise ValueError(f"window_size ({window_size}) cannot be larger than data length ({len(X)})")
    
    n_samples, n_features = X.shape
    n_windows = (n_samples - window_size) // stride + 1
    
    windows = np.zeros((n_windows, window_size, n_features))
    
    for i in range(n_windows):
        start_idx = i * stride
        end_idx = start_idx + window_size
        windows[i] = X[start_idx:end_idx]
    
    return windows


def handle_missing_values(X: np.ndarray, method: str = 'mean') -> np.ndarray:
    """
    Handle missing values in data.
    
    Parameters
    ----------
    X : np.ndarray
        Data with potential missing values.
        
    method : str, default='mean'
        Imputation method. Options:
        - 'mean': Replace with column mean
        - 'median': Replace with column median
        - 'forward': Forward fill
        - 'backward': Backward fill
        - 'drop': Drop rows with missing values
        
    Returns
    -------
    np.ndarray
        Data with missing values handled.
        
    Examples
    --------
    >>> X = np.array([[1, 2], [np.nan, 4], [5, 6]])
    >>> X_clean = handle_missing_values(X, method='mean')
    """
    X = X.copy()
    
    if method == 'mean':
        col_mean = np.nanmean(X, axis=0)
        inds = np.where(np.isnan(X))
        X[inds] = np.take(col_mean, inds[1])
        
    elif method == 'median':
        col_median = np.nanmedian(X, axis=0)
        inds = np.where(np.isnan(X))
        X[inds] = np.take(col_median, inds[1])
        
    elif method == 'forward':
        mask = np.isnan(X)
        idx = np.where(~mask, np.arange(mask.shape[0])[:, None], 0)
        np.maximum.accumulate(idx, axis=0, out=idx)
        X = X[idx, np.arange(idx.shape[1])]
        
    elif method == 'backward':
        mask = np.isnan(X[::-1])
        idx = np.where(~mask, np.arange(mask.shape[0])[:, None], mask.shape[0] - 1)
        np.maximum.accumulate(idx, axis=0, out=idx)
        X = X[::-1][idx, np.arange(idx.shape[1])][::-1]
        
    elif method == 'drop':
        X = X[~np.isnan(X).any(axis=1)]
        
    else:
        raise ValueError(f"Unknown method: {method}")
    
    return X
