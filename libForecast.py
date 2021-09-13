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
            results['Holt'] = predictions
            results['Holt_RMSE'] = compute_RMSE(data, result_model)

        # Exponential model predictions
        if 'exponential' in methods:
            exp_model = api.tsa.Holt(decomposed_data.trend[season-1:], exponential=True, damped_trend=False, initialization_method='estimated')
            result_model = exp_model.fit()
            predictions = compose_seasonal(result_model.forecast(horizon), seasonal_coeffs, seasonal_index)
            results['Exponential'] = predictions
            results['Exponential_RMSE'] = compute_RMSE(data, result_model)

        # Damped model predictions
        if 'damped' in methods:
            damped_model = api.tsa.Holt(decomposed_data.trend[season-1:], exponential=False, damped_trend=True, initialization_method='estimated')
            result_model = damped_model.fit()
            predictions = compose_seasonal(result_model.forecast(horizon), seasonal_coeffs, seasonal_index)
            results['Damped'] = predictions
            results['Damped_RMSE'] = compute_RMSE(data, result_model)

        # Theta model predictions
        if 'theta' in methods:
                theta_model = theta.ThetaModel(data, period=season, deseasonalize=True, method='multiplicative')
                result_model = theta_model.fit()
                results['Theta'] = np.array(result_model.forecast(horizon))

        # ARIMA model predictions
        if 'arima' in methods:
                arima = sm.tsa.arima.model.ARIMA(data, seasonal_order=(1, 1, 1, season))
                result_model = arima.fit()
                results['ARIMA'] = result_model.forecast(horizon)
                results['ARIMA_RMSE'] = compute_RMSE(data, result_model)

    # Trend based Data
    else:

        # Holt model predictions
        if 'holt' in methods:
            holt_model = api.tsa.Holt(data, exponential=False, damped_trend=False, initialization_method='estimated')
            result_model = holt_model.fit()
            results['Holt'] = result_model.forecast(horizon)
            results['Holt_RMSE'] = compute_RMSE(data, result_model)
        
        # Exponential model predictions
        if 'exponential' in methods:
            exp_model = api.tsa.Holt(data, exponential=True, damped_trend=False, initialization_method='estimated')
            result_model = exp_model.fit()
            results['Exponential'] = result_model.forecast(horizon)
            results['Exponential_RMSE'] = compute_RMSE(data, result_model)

        # Damped model predictions
        if 'damped' in methods:
            damped_model = api.tsa.Holt(data, exponential=False, damped_trend=True, initialization_method='estimated')
            result_model = damped_model.fit()
            results['Damped'] = result_model.forecast(horizon)
            results['Damped_RMSE'] = compute_RMSE(data, result_model)

        # Theta model predictions
        if 'theta' in methods:
            theta_model = theta.ThetaModel(data, period=season)
            result_model = theta_model.fit()
            results['Theta'] = np.array(result_model.forecast(horizon))

        # ARIMA model predictions
        if 'arima' in methods:
                arima = sm.tsa.arima.model.ARIMA(data, order=(1, 0, 1))
                result_model = arima.fit()
                results['ARIMA'] = result_model.forecast(horizon)
                results['ARIMA_RMSE'] = compute_RMSE(data, result_model)

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

def produce_plot_and_stats(data, index, methods, forecast, confidence_interval, zoom, fibonacci_enabled=False):

        # Make a black bg styled plot 
        plt.style.use('dark_background')

        # Two figures in one canvas
        # A plot of the historical data and forecasting lines
        # and a plot for a table with the final forecasts
        fig, ax = plt.subplots(2, 1, figsize=(7, 7), gridspec_kw={'height_ratios': [7, 1]})

        # Plot the historical data
        ax[0].plot(data, c='sienna', label='Historical data', linewidth=.7)
        # ax[0].text(len(data) + forecast['Horizon'], data[-1]-0.2, '{:.5f}'.format(data[-1]), c='sienna', fontsize='small')

        ax[0].margins(2, 0)

        # Columns and data cells for the table
        colLabels = ['Last Date']
        cellText = ['{:5f}'.format(data[-1])]

        # Create a color linear space for different iterations
        # of the forecasting methods
        colors = [(1 - b, 0.2 * b, b) for b in np.linspace(0.5, 1, num=len(methods))]
        color_idx = 0

        # If enabled plot fibonacci retracement lines
        if fibonacci_enabled:
            fib_values = fibonacci_retracements(data)
            for fib_val in fib_values:
                ax[0].axhline(fib_val, linewidth=.7, linestyle='-.', color='green')
                ax[0].text(len(data) + forecast['Horizon'], fib_val, '{:.5f}'.format(fib_val), c='green', fontsize='small')

        # Plot the forecasts' lines
        for method in methods:
                if method == 'lrl':
                        ax[0].plot(forecast['LRL'], label='Linear regression', c='red', linewidth=.7)
                else:
                        plot_forecasts(data, forecast, method, confidence_interval, ax, colors[color_idx], colLabels, cellText)
                        color_idx += 1

        # Present the dates as ticks for the graph
        dates = [str(val.date()) for val in index] + [str(index[-1].date() + datetime.timedelta(days=i)) for i in range(1, forecast['Horizon']+1)]
        ticks = [counter for counter in range(0, len(dates), len(dates) // 20)]
        ax[0].set_xticks(ticks)
        ax[0].set_xticklabels([dates[idx] for idx in ticks])
        # Rotate the ticks for better presentation of the dates
        for tick in ax[0].get_xticklabels():
                tick.set_rotation(45)

        if methods != []:
            # Set a limit to the horizontal axis
            ax[0].set_xlim(zoom * len(data) // 100, len(data) + forecast['Horizon'] - 1)
        else:
            ax[0].set_xlim(zoom * len(data) // 100, len(data) - 1)

        # Set a title for the graph about how many days ahead we are speculating
        ax[0].set_title("Forecast for the next {} days".format(forecast['Horizon']))

        # Present the legend to inform about the forecasting lines
        ax[0].legend(loc='upper left')

        # Create a grid for readability purposes
        ax[0].grid(True, linewidth=.2)

        # Create a table with all the forecasting values
        ax[1].axis('off')

        if methods != []:
            cell2Text = [(float(cellText[0]) - float(val)) < 0 for val in cellText]
            cell2Text = ['--'] + cell2Text[1:]
            table = ax[1].table(cellText=[cellText, cell2Text], colLabels=colLabels, rowLabels=['Close', 'Buy?'], cellLoc='center', loc='center')

            for cell in table.properties()['children']:
                if cell.get_text().get_text() == 'False':
                    cell.get_text().set_color('red')
                
                if cell.get_text().get_text() == 'True':
                    cell.get_text().set_color('green')

                if cell.get_text().get_text() == 'Last Date':
                    cell.get_text().set_color('sienna')
        else:
            table = ax[1].table(cellText=[cellText], colLabels=colLabels, rowLabels=['Close'], cellLoc='center', loc='center')
            for cell in table.properties()['children']:
                if cell.get_text().get_text() == 'Last Date':
                    cell.get_text().set_color('sienna')

        # Make the bg color of cells black 
        for cell in table.properties()['children']:
                cell.set_color('black')

        # Tight plot for better readability
        plt.tight_layout()

        return fig

def dummy_plot():

    # Make a black bg styled plot 
    plt.style.use('dark_background')

    fig, ax = plt.subplots(1, 1, figsize=(7, 7))
    ax.plot([1,2,3,4,5], visible=False)
    ax.set_xlim(0, 4)

    plt.grid(False)
    plt.axis('off')

    return fig