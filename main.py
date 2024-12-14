import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
import matplotlib.colors as mcolors
import streamlit as st

# Set Page Configurations
st.set_page_config(
    page_title="Crypto Volume Profile",
    page_icon="📈",
    layout="wide"
)

# Get Data
with open('symbols.txt', 'r') as file:
    content = file.read()
    # Remove square brackets and split by comma
    symbols = [symbol.strip().strip("'") for symbol in content.split(',')]


def get_data(option, period, interval):
    df = yf.download(
                tickers  = option,
                period   = period,
                interval = interval
                )
    return df

col1, col2 = st.columns([2, 1])

col1.title("Cryptocurrencies Volume Profile")

with col2:
    st.write("#")
    option = st.selectbox(
        "Select Cryptocurrency:",
        (symbols))   
     
    period = st.selectbox(
        "Select Period:",
        ('1y','1d','5d','1mo','3mo','6mo','1y','2y','5y','10y'))
    
    interval = st.selectbox(
        "Select Interval:",
        ('1d','1h','1d','5d','1wk','1mo','3mo'))

    threshold = st.number_input("Volume Threshold %:", 1, 100, 94)

progress_text = "Data Loading in progress. Please wait..."
my_bar        = col1.progress(0, text=progress_text)

for percent_complete in range(100):
    df = get_data(option, period, interval)
    
    my_bar.progress(percent_complete + 1, text=progress_text)

my_bar.empty()
st.toast(f'Loaded {option}!', icon="✅")

data       = pd.DataFrame(df)

data['Close'] = data['Close'].fillna(method='ffill')
data['Volume'] = data['Volume'].fillna(0)

price_bins = np.linspace(data['Close'].min(), data['Close'].max(), 100).astype(float)

volume_profile, _ = np.histogram(
    data['Close'], 
    bins=99, 
    range=(float(data['Close'].min()), float(data['Close'].max())), 
    weights=data['Volume']
)

# Calculate bin centers for plotting
bin_centers    = ((price_bins[:-1] + price_bins[1:]) / 2).astype(float)

# Create the plot
fig, (ax2, ax) = plt.subplots(1, 2, figsize=(20, 10), gridspec_kw={'width_ratios': [1, 4]}, dpi=1000)

# Plot Currency chart
ax.plot(data.index, data['Close'], color='black', alpha=0.5)

# Draw horizontal lines where volume profile is bigger than threshold
threshold     = np.percentile(volume_profile, threshold)  # Set threshold to percentile
current_close = float(data['Close'].iloc[-1])  # Get the most recent closing price

for price, volume in zip(bin_centers, volume_profile):
    if volume > threshold:
        if current_close > float(price):
            color = 'aqua'
            linestyle = "-"
        else:
            color = 'red'
            linestyle = "--"
        ax.axhline(y=float(price), color=color, linestyle=linestyle, alpha=0.5, linewidth=4)


# Plot volume profile
cmap = mcolors.LinearSegmentedColormap.from_list("", ["aqua", "red"], gamma=0.7)

ax2.barh(bin_centers, volume_profile, height=price_bins[1]-price_bins[0], color=cmap(volume_profile/volume_profile.max()))
ax2.set_ylim(ax.get_ylim())
ax2.axvline(x=threshold, color='gray', linestyle='--', linewidth=2, label=f'{94}th Percentile')

# Set labels and title
ax.set_xlabel('Date')
ax.set_ylabel('Price (USD)')
ax2.set_ylabel('Volume')
ax2.legend()

plt.title(f'{option} Volume Profile')

col1.pyplot(fig)


col2.info('''A streamlined web application for analyzing cryptocurrency volume profiles.
            
    Users can select from a wide range of cryptocurrencies, 
    time periods, and intervals to visualize price movements 
    and trading volumes.
           
    The app features interactive charts that highlight 
    significant volume thresholds, helping traders and 
    investors identify key price levels and potential 
    support/resistance zones.''', icon="ℹ️")

st.divider()
st.subheader("About")
st.write('''Crypto Volume Profile App 2024\n
This site is for informational purposes only. The information on our website is not financial advice, and you should not consider it to be financial advice.''')

st.write("@VanHes1ng")

st.write('''TradingView: https://www.tradingview.com/u/VanHe1sing/\n 
Telegram: https://t.me/IvanKocherzhat\n 
GitHub: https://github.com/VanHes1ng\n
X: https://x.com/Van_He1sing            
''')


with open('./wave.css') as f:
    css = f.read()

st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)
