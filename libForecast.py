import numpy as np
import statsmodels as sm
from statsmodels import api
from matplotlib import pyplot as plt
import theta as theta
import datetime
import linearregression 
import pandas as pd
import math

zoom = 1

def compute_RMSE(data, result_model):
    return math.sqrt(((pd.DataFrame(data) - pd.DataFrame(result_model.predict(0, len(data)-1))) ** 2).mean()) 

def compose_seasonal(predictions, seasonal_coeffs, start_index):
    
    for idx in range(len(predictions)):
        predictions[idx] *= seasonal_coeffs[start_index % len(seasonal_coeffs)]
        start_index += 1

    return predictions


# TODO: make it threaded

def forecasts(data, methods, season, horizon=1):
    
    results = dict()
    
    # Create a linear regression line for trend analysis
    lrl = linearregression.LRL(data)
    results['LRL'] = lrl.predict(horizon)

    # Get the autocorrelation of the data 
    # to test the seasonality of the data
    acf_mean = api.tsa.acf(data, fft=False, nlags=season).mean()

    if acf_mean >= 0.5:

        # If the time series is seasonal deseasonalize
        decomposed_data = api.tsa.seasonal_decompose(data, model='multiplicative', period=season, two_sided=False)
        seasonal_coeffs = decomposed_data.seasonal[:season]
        seasonal_index = (data.shape[0] // season) % season

        # Holt model predictions
        if 'holt' in methods:
            holt_model = api.tsa.Holt(decomposed_data.trend[season-1:], exponential=False, damped_trend=False, initialization_method='estimated')
            result_model = holt_model.fit()
            predictions = compose_seasonal(result_model.forecast(horizon), seasonal_coeffs, seasonal_index)
            results['holt'] = predictions
            results['holt_RMSE'] = compute_RMSE(data, result_model)

        # Exponential model predictions
        if 'exponential' in methods:
            exp_model = api.tsa.Holt(decomposed_data.trend[season-1:], exponential=True, damped_trend=False, initialization_method='estimated')
            result_model = exp_model.fit()
            predictions = compose_seasonal(result_model.forecast(horizon), seasonal_coeffs, seasonal_index)
            results['exponential'] = predictions
            results['exponential_RMSE'] = compute_RMSE(data, result_model)

        # Damped model predictions
        if 'damped' in methods:
            damped_model = api.tsa.Holt(decomposed_data.trend[season-1:], exponential=False, damped_trend=True, initialization_method='estimated')
            result_model = damped_model.fit()
            predictions = compose_seasonal(result_model.forecast(horizon), seasonal_coeffs, seasonal_index)
            results['damped'] = predictions
            results['damped_RMSE'] = compute_RMSE(data, result_model)

        # Theta model predictions
        if 'theta' in methods:
                theta_model = theta.ThetaModel(data, period=season, deseasonalize=True, method='multiplicative')
                result_model = theta_model.fit()
                results['theta'] = np.array(result_model.forecast(horizon))

        # ARIMA model predictions
        if 'arima' in methods:
                arima = sm.tsa.arima.model.ARIMA(data, seasonal_order=(1, 1, 1, season))
                result_model = arima.fit()
                results['arima'] = result_model.forecast(horizon)
                results['arima_RMSE'] = compute_RMSE(data, result_model)

    # Trend based Data
    else:

        # Holt model predictions
        if 'holt' in methods:
            holt_model = api.tsa.Holt(data, exponential=False, damped_trend=False, initialization_method='estimated')
            result_model = holt_model.fit()
            results['holt'] = result_model.forecast(horizon)
            results['holt_RMSE'] = compute_RMSE(data, result_model)
        
        # Exponential model predictions
        if 'exponential' in methods:
            exp_model = api.tsa.Holt(data, exponential=True, damped_trend=False, initialization_method='estimated')
            result_model = exp_model.fit()
            results['exponential'] = result_model.forecast(horizon)
            results['exponential_RMSE'] = compute_RMSE(data, result_model)

        # Damped model predictions
        if 'damped' in methods:
            damped_model = api.tsa.Holt(data, exponential=False, damped_trend=True, initialization_method='estimated')
            result_model = damped_model.fit()
            results['damped'] = result_model.forecast(horizon)
            results['damped_RMSE'] = compute_RMSE(data, result_model)

        # Theta model predictions
        if 'theta' in methods:
            theta_model = theta.ThetaModel(data, period=season)
            result_model = theta_model.fit()
            results['theta'] = np.array(result_model.forecast(horizon))

        # ARIMA model predictions
        if 'arima' in methods:
                arima = sm.tsa.arima.model.ARIMA(data, order=(1, 0, 1))
                result_model = arima.fit()
                results['arima'] = result_model.forecast(horizon)
                results['arima_RMSE'] = compute_RMSE(data, result_model)

    results['Season'] = season
    results['Horizon'] = horizon
    return results

def fibonacci_retracements(data):

    max_val = max(data[int(3/4 * len(data)) : ])
    min_val = min(data[int(3/4 * len(data)) : ])
    diff = max_val - min_val

    lrl = linearregression.LRL(data[int(3/4 * len(data)) : ])
    beta, _ = lrl.create_coefficients()

    if beta > 0:
        return [max_val, max_val - 0.236 * diff, max_val - 0.382 * diff, max_val - 0.618 * diff, max_val - 0.786 * diff]
    else:
        return [min_val, min_val + 0.236 * diff, min_val + 0.382 * diff, min_val + 0.618 * diff, min_val + 0.786 * diff]

def plot_forecasts(data, forecast, method, confidence_interval, ax, color, colLabels, cellText):

        methods = {
                'holt': 'Holt',
                'exponential': 'Exponential',
                'damped': 'Damped',
                'theta': 'Theta',
                'arima': 'ARIMA'
        }

        # Compute time from the end of the historical data 
        # and the end of the forecasting horizon
        time = [t for t in range(len(data), len(data)+forecast['Horizon'])]

        # Plot the forecasting line
        ax[0].plot(time, forecast[methods[method]], label=methods[method], c=color, linewidth=1)
        # Print the last value forecasted on the plot
        # ax[0].text(len(data) + forecast['Horizon'], forecast[methods[method]][-1], '{:.5f}'.format(forecast[methods[method]][-1]), c=color, fontsize='small')
        # Connect the historical data with the forecasted data
        ax[0].plot([len(data)-1, len(data)], [data[-1], forecast[methods[method]][0]], c=color)

        # Plot the confidence intervals
        if confidence_interval and method != 'theta':
            # Compute confidence intervals
            CIs = [math.sqrt(t - len(data) + 1) * 1.645 * forecast[methods[method] + '_RMSE'] for t in time]
            # Fill the interval to present the confidence in our forecasting power
            ax[0].fill_between([len(data)-1] + time, [data[-1]] + [val + CI for val, CI in list( zip(forecast[methods[method]], CIs) )], 
                                [data[-1]] + [val - CI for val, CI in list( zip(forecast[methods[method]], CIs) )], color=color, alpha=0.2)

        # Add a column for a method
        colLabels.append(methods[method])
        # Add a cell with ast forecasted value
        cellText.append('{:.5f}'.format(forecast[methods[method]][-1]))