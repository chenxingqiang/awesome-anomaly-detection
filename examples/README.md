# Examples

This directory contains example scripts and notebooks demonstrating how to use the `awesome-anomaly-detection` package.

## Getting Started

Before running the examples, make sure you have installed the package:

```bash
pip install awesome-anomaly-detection
```

Or install from source:

```bash
git clone https://github.com/chenxingqiang/awesome-anomaly-detection.git
cd awesome-anomaly-detection
pip install -e .
```

## Available Examples

### Basic Examples

- **simple_example.py**: Basic usage of the anomaly detection library with synthetic data
- **simple_data_generator.py**: Generate simple synthetic data for testing
- **time_series_example.py**: Time series anomaly detection examples

### Driving Behavior Analysis

- **aggressive_driving_analysis.py**: Complete pipeline for detecting aggressive driving events
- **aggressive_driving_analysis.md**: Documentation for the aggressive driving analysis
- **Aggressive_Drive_detection.ipynb**: Jupyter notebook with interactive examples

### Data Generation

- **generate_synthetic_driving_data.py**: Generate synthetic driving data for testing
- **generate_original_format_data.py**: Generate data in original format
- **test_synthetic_data.py**: Test scripts for synthetic data
- **test_original_format.py**: Test scripts for original format data

### Integration Examples

- **pyod_integration_example.py**: Integration with PyOD library
- **README_PyOD_Integration.md**: Documentation for PyOD integration

## Data Directories

- **synthetic_driving_data/**: Contains generated synthetic driving data (not included in package)
- **original_format_data/**: Contains original format data (not included in package)

**Note**: The data directories are not included in the package distribution. Use the data generation scripts to create your own datasets.

## Running Examples

To run an example:

```bash
python examples/simple_example.py
```

For Jupyter notebooks:

```bash
jupyter notebook examples/Aggressive_Drive_detection.ipynb
```

## Requirements

Some examples may require additional dependencies. Install them with:

```bash
pip install -r examples/requirements_pyod.txt
```

## Contributing

Feel free to add more examples! Please follow the existing structure and naming conventions.
