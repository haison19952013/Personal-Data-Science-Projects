# Stock Volatility Forecasting In Vietnam

## Overview
This project forecasts stock price volatility for Vietnamese stocks using historical price data retrieved via the EODHD API. The models are trained to predict future volatility and help inform investment decisions.

## Files
- `main.ipynb` — Main Jupyter notebook for data retrieval, modelling, and evaluation
- `config.py` — Configuration and API key settings (requires a `.env` file with `eodhd_api_key`, `db_name`, and `regressor_directory`)
- `data.py` — Module for fetching and processing stock data from the API
- `model.py` — Module for training and evaluating volatility forecasting models
- `my_api.py` — Helper module for API interactions
- `stocks.sqlite` — Local SQLite database storing historical stock data

## Requirements
- An [EODHD](https://eodhd.com/) API key
- A `.env` file in the project directory with the following variables:
  ```
  eodhd_api_key=<your_api_key>
  db_name=stocks.sqlite
  regressor_directory=<path_to_save_models>
  ```

## Procedure
1. Configure the `.env` file with your API key and settings
2. Run `main.ipynb` to fetch data, train models, and evaluate results
3. Review volatility forecasts and model performance metrics
