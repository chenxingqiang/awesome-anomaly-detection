"""
Synthetic data generation utilities for testing anomaly detection algorithms.

This module provides functions to generate synthetic data with controlled
anomalies for testing and benchmarking anomaly detection algorithms.
"""

import numpy as np
from typing import Tuple, Optional, List


def generate_anomaly_data(n_samples: int = 1000, n_features: int = 2,
                          contamination: float = 0.1, 
                          random_state: Optional[int] = None) -> Tuple[np.ndarray, np.ndarray]:
    """
    Generate synthetic data with point anomalies.
    
    Parameters
    ----------
    n_samples : int, default=1000
        Number of samples to generate.
        
    n_features : int, default=2
        Number of features.
        
    contamination : float, default=0.1
        Proportion of anomalies (between 0 and 0.5).
        
    random_state : int, optional
        Random seed for reproducibility.
        
    Returns
    -------
    X : np.ndarray
        Generated data of shape (n_samples, n_features).
        
    y : np.ndarray
        Labels: 0 for normal, 1 for anomaly.
        
    Examples
    --------
    >>> X, y = generate_anomaly_data(n_samples=1000, contamination=0.1)
    >>> X.shape, y.shape
    ((1000, 2), (1000,))
    >>> np.sum(y) / len(y)  # Should be close to contamination
    0.1
    """
    if random_state is not None:
        np.random.seed(random_state)
    
    if not 0 < contamination < 0.5:
        raise ValueError("contamination must be between 0 and 0.5")
    
    n_anomalies = int(n_samples * contamination)
    n_normal = n_samples - n_anomalies
    
    # Generate normal data from standard normal distribution
    X_normal = np.random.randn(n_normal, n_features)
    
    # Generate anomalies from a different distribution
    # Use wider spread and different mean
    X_anomalies = np.random.randn(n_anomalies, n_features) * 3 + 5
    
    # Combine and shuffle
    X = np.vstack([X_normal, X_anomalies])
    y = np.hstack([np.zeros(n_normal), np.ones(n_anomalies)])
    
    # Shuffle
    indices = np.random.permutation(n_samples)
    X = X[indices]
    y = y[indices]
    
    return X, y


def generate_time_series_with_changepoints(n_samples: int = 1000, n_features: int = 1,
                                            n_changepoints: int = 3,
                                            random_state: Optional[int] = None) -> Tuple[np.ndarray, np.ndarray]:
    """
    Generate time series data with change points.
    
    Parameters
    ----------
    n_samples : int, default=1000
        Length of time series.
        
    n_features : int, default=1
        Number of features/dimensions.
        
    n_changepoints : int, default=3
        Number of change points to insert.
        
    random_state : int, optional
        Random seed for reproducibility.
        
    Returns
    -------
    X : np.ndarray
        Time series data of shape (n_samples, n_features).
        
    changepoints : np.ndarray
        Binary array indicating change points (1 at change points, 0 elsewhere).
        
    Examples
    --------
    >>> X, cp = generate_time_series_with_changepoints(n_samples=1000, n_changepoints=3)
    >>> X.shape
    (1000, 1)
    >>> np.sum(cp)
    3
    """
    if random_state is not None:
        np.random.seed(random_state)
    
    # Initialize time series
    X = np.zeros((n_samples, n_features))
    changepoints = np.zeros(n_samples)
    
    # Generate random change point locations
    cp_locations = sorted(np.random.choice(range(100, n_samples - 100), 
                                          size=n_changepoints, replace=False))
    
    # Generate segments between change points
    segments = [0] + cp_locations + [n_samples]
    
    for i in range(len(segments) - 1):
        start = segments[i]
        end = segments[i + 1]
        
        # Each segment has different statistical properties
        mean = np.random.randn(n_features) * 2
        std = np.random.rand(n_features) * 2 + 0.5
        
        # Generate data for this segment
        X[start:end] = np.random.randn(end - start, n_features) * std + mean
        
        # Mark change point
        if i < len(segments) - 2:
            changepoints[end] = 1
    
    return X, changepoints


def generate_seasonal_data(n_samples: int = 1000, n_features: int = 1,
                           period: int = 100, amplitude: float = 1.0,
                           noise_level: float = 0.1,
                           random_state: Optional[int] = None) -> np.ndarray:
    """
    Generate seasonal/periodic time series data.
    
    Parameters
    ----------
    n_samples : int, default=1000
        Length of time series.
        
    n_features : int, default=1
        Number of features.
        
    period : int, default=100
        Period of seasonality.
        
    amplitude : float, default=1.0
        Amplitude of seasonal component.
        
    noise_level : float, default=0.1
        Standard deviation of noise.
        
    random_state : int, optional
        Random seed for reproducibility.
        
    Returns
    -------
    np.ndarray
        Seasonal time series of shape (n_samples, n_features).
        
    Examples
    --------
    >>> X = generate_seasonal_data(n_samples=1000, period=50)
    >>> X.shape
    (1000, 1)
    """
    if random_state is not None:
        np.random.seed(random_state)
    
    t = np.arange(n_samples)
    X = np.zeros((n_samples, n_features))
    
    for i in range(n_features):
        # Seasonal component
        seasonal = amplitude * np.sin(2 * np.pi * t / period + i)
        
        # Noise
        noise = np.random.randn(n_samples) * noise_level
        
        # Combine
        X[:, i] = seasonal + noise
    
    return X


def generate_clustered_data(n_samples: int = 1000, n_features: int = 2,
                            n_clusters: int = 3, cluster_std: float = 1.0,
                            contamination: float = 0.1,
                            random_state: Optional[int] = None) -> Tuple[np.ndarray, np.ndarray]:
    """
    Generate clustered data with anomalies.
    
    Parameters
    ----------
    n_samples : int, default=1000
        Number of samples.
        
    n_features : int, default=2
        Number of features.
        
    n_clusters : int, default=3
        Number of clusters for normal data.
        
    cluster_std : float, default=1.0
        Standard deviation of clusters.
        
    contamination : float, default=0.1
        Proportion of anomalies.
        
    random_state : int, optional
        Random seed for reproducibility.
        
    Returns
    -------
    X : np.ndarray
        Generated data of shape (n_samples, n_features).
        
    y : np.ndarray
        Labels: 0 for normal, 1 for anomaly.
        
    Examples
    --------
    >>> X, y = generate_clustered_data(n_samples=1000, n_clusters=3)
    >>> X.shape
    (1000, 2)
    """
    if random_state is not None:
        np.random.seed(random_state)
    
    n_anomalies = int(n_samples * contamination)
    n_normal = n_samples - n_anomalies
    
    # Generate cluster centers
    centers = np.random.randn(n_clusters, n_features) * 5
    
    # Generate normal data around clusters
    samples_per_cluster = n_normal // n_clusters
    X_normal = []
    
    for i in range(n_clusters):
        if i == n_clusters - 1:
            # Last cluster gets remaining samples
            n_cluster_samples = n_normal - len(X_normal) * samples_per_cluster
        else:
            n_cluster_samples = samples_per_cluster
        
        cluster_data = np.random.randn(n_cluster_samples, n_features) * cluster_std + centers[i]
        X_normal.append(cluster_data)
    
    X_normal = np.vstack(X_normal)
    
    # Generate anomalies uniformly in space
    X_anomalies = np.random.uniform(-10, 10, size=(n_anomalies, n_features))
    
    # Combine
    X = np.vstack([X_normal, X_anomalies])
    y = np.hstack([np.zeros(n_normal), np.ones(n_anomalies)])
    
    # Shuffle
    indices = np.random.permutation(n_samples)
    X = X[indices]
    y = y[indices]
    
    return X, y


def generate_multimodal_distribution(n_samples: int = 1000, n_features: int = 2,
                                    n_modes: int = 2, 
                                    random_state: Optional[int] = None) -> np.ndarray:
    """
    Generate data from a multimodal distribution.
    
    Parameters
    ----------
    n_samples : int, default=1000
        Number of samples.
        
    n_features : int, default=2
        Number of features.
        
    n_modes : int, default=2
        Number of modes in the distribution.
        
    random_state : int, optional
        Random seed for reproducibility.
        
    Returns
    -------
    np.ndarray
        Generated data of shape (n_samples, n_features).
        
    Examples
    --------
    >>> X = generate_multimodal_distribution(n_samples=1000, n_modes=3)
    >>> X.shape
    (1000, 2)
    """
    if random_state is not None:
        np.random.seed(random_state)
    
    # Generate mode centers
    centers = np.random.randn(n_modes, n_features) * 5
    
    # Generate samples for each mode
    samples_per_mode = n_samples // n_modes
    X = []
    
    for i in range(n_modes):
        if i == n_modes - 1:
            n_mode_samples = n_samples - len(X) * samples_per_mode
        else:
            n_mode_samples = samples_per_mode
        
        # Each mode has different covariance
        cov = np.eye(n_features) * (np.random.rand() * 2 + 0.5)
        mode_data = np.random.multivariate_normal(centers[i], cov, n_mode_samples)
        X.append(mode_data)
    
    X = np.vstack(X)
    
    # Shuffle
    indices = np.random.permutation(n_samples)
    X = X[indices]
    
    return X


def add_noise(X: np.ndarray, noise_type: str = 'gaussian', 
              noise_level: float = 0.1) -> np.ndarray:
    """
    Add noise to data.
    
    Parameters
    ----------
    X : np.ndarray
        Original data.
        
    noise_type : str, default='gaussian'
        Type of noise: 'gaussian', 'uniform', 'salt_pepper'.
        
    noise_level : float, default=0.1
        Amount of noise to add.
        
    Returns
    -------
    np.ndarray
        Noisy data.
        
    Examples
    --------
    >>> X = np.ones((100, 2))
    >>> X_noisy = add_noise(X, noise_type='gaussian', noise_level=0.1)
    """
    X_noisy = X.copy()
    
    if noise_type == 'gaussian':
        noise = np.random.randn(*X.shape) * noise_level
        X_noisy += noise
        
    elif noise_type == 'uniform':
        noise = np.random.uniform(-noise_level, noise_level, X.shape)
        X_noisy += noise
        
    elif noise_type == 'salt_pepper':
        # Add salt and pepper noise
        n_salt = int(X.size * noise_level / 2)
        n_pepper = int(X.size * noise_level / 2)
        
        # Salt
        salt_coords = [np.random.randint(0, i, n_salt) for i in X.shape]
        X_noisy[tuple(salt_coords)] = X.max()
        
        # Pepper
        pepper_coords = [np.random.randint(0, i, n_pepper) for i in X.shape]
        X_noisy[tuple(pepper_coords)] = X.min()
        
    else:
        raise ValueError(f"Unknown noise type: {noise_type}")
    
    return X_noisy
