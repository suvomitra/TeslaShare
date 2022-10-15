import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
import plotly.graph_objects as go
from plotly.subplots import make_subplots
def make_graph(stock_data, revenue_data, stock):    #making a function to use later
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Historical Share Price", "Historical Revenue"), vertical_spacing = .3)
    stock_data_specific = stock_data[stock_data.Date <= '2021--06-14']
    revenue_data_specific = revenue_data[revenue_data.Date <= '2021-04-30']
    fig.add_trace(go.Scatter(x=pd.to_datetime(stock_data_specific.Date, infer_datetime_format=True), y=stock_data_specific.Close.astype("float"), name="Share Price"), row=1, col=1)
    fig.add_trace(go.Scatter(x=pd.to_datetime(revenue_data_specific.Date, infer_datetime_format=True), y=revenue_data_specific.Revenue.astype("float"), name="Revenue"), row=2, col=1)
    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Price ($US)", row=1, col=1)
    fig.update_yaxes(title_text="Revenue ($US Millions)", row=2, col=1)
    fig.update_layout(showlegend=False,
    height=900,
    title=stock,
    xaxis_rangeslider_visible=True)
    fig.show()
tesla=  yf.Ticker('TSLA')
tesla_data=tesla.history(period='max')
tesla_data.reset_index(inplace=True)
# print(tesla_data.head()) #printing the first five values of tesla data

html_data=requests.get('https://www.macrotrends.net/stocks/charts/TSLA/tesla/revenue').text
soup=BeautifulSoup(html_data,'html.parser')

tesla_revenue = pd.DataFrame(columns=["Date", "Revenue"])  # defining a dataframe with 2 columns
dafa = soup.find_all("tbody")[1]      # finding the table from html file

for row in dafa.find_all("tr"):     # adding values to the table by running a loop
    col = row.find_all("td")
    date = col[0]
    value = col[1]
    tesla_revenue = tesla_revenue.append({"Date":date,"Revenue":value},ignore_index=True)
#print(tesla_revenue)

tesla_revenue["Revenue"] = tesla_revenue['Revenue'].str.replace(',|\$',"")
print(tesla_revenue)