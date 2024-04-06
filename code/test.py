from flask import Flask, render_template, request
import pandas as pd
import plotly.express as px                                                  
import numpy as np
from prophet import Prophet
import yfinance as yf
from prophet.plot import plot_plotly
import plotly.graph_objects as go
from sklearn.metrics import mean_absolute_error


app = Flask(__name__)

def yahoo_stocks(stock_symbol):
    stock_data = yf.download(stock_symbol, period='5y',interval='1d')
    stock_data = stock_data.reset_index()
    stock_data[['ds','y']] = stock_data[['Date','Adj Close']]                
    return stock_data

def plot_price(df_whole):
    fig = px.line(df_whole, x='Date', y='Close')
    fig.update_xaxes(rangeslider_visible=False)
    return fig.to_html(include_plotlyjs=False, full_html=False)

def prediction_model(df_whole):
    train_data = df_whole.sample(frac=0.8, random_state=0)
    test_data = df_whole.drop(train_data.index)

    model_1 = Prophet(daily_seasonality=True)
    model_1.fit(train_data)
    
    y_actual = test_data['y']
    prediction = model_1.predict(pd.DataFrame({'ds': test_data['ds']}))
    y_predicted = prediction['yhat'].astype(int)
    mae = mean_absolute_error(y_actual, y_predicted)

    trace_predicted = go.Scatter(x=test_data['ds'], y=y_predicted, mode='lines', name='Predicted', line=dict(color='black'))
    trace_actual = go.Scatter(x=test_data['ds'], y=y_actual, mode='lines', name='Actual', line=dict(color='yellow'))
    layout = go.Layout(
        title="Price Action: Predicted vs Actual",
        xaxis=dict(title="Year"),
        yaxis=dict(title="Price Action"),
        showlegend=True)
    fig = go.Figure(data=[trace_predicted, trace_actual], layout=layout)
    return fig.to_html(include_plotlyjs=False, full_html=False), mae

def future_prediction(df_whole):
    model_2 = Prophet()                                                     
    model_2.fit(df_whole)                                                           
    future = model_2.make_future_dataframe(365)                                       
    forecast = model_2.predict(future) 
    fig = plot_plotly(model_2, forecast)
    fig.update_xaxes(rangeslider_visible=False)
    return fig.to_html(include_plotlyjs=False, full_html=False), forecast[['ds','yhat','yhat_lower','yhat_upper']].tail()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        stock = request.form['stock']
        df_whole = yahoo_stocks(stock)
        plot_html = plot_price(df_whole)
        prediction_html, mae = prediction_model(df_whole)
        future_html, forecast_tail = future_prediction(df_whole)
        return render_template('result.html', plot_html=plot_html, prediction_html=prediction_html, future_html=future_html, mae=mae, forecast_tail=forecast_tail)
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
