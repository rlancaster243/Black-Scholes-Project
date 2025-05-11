# Black–Scholes Pricing Model

This repository hosts an interactive Black–Scholes pricing dashboard, letting you see how option values react to different market inputs. With an intuitive interface, you can quickly tweak parameters and watch call and put prices update in real time.

## 🚀 Features

1. **Option Price Visualization**  
   - Renders both Call and Put prices on an interactive heatmap  
   - Instantly refreshes as you modify Spot Price, Volatility, or Time to Maturity  

2. **Real-Time Parameter Controls**  
   - Adjust Spot Price, Volatility, Strike Price, Time to Maturity, and Risk-Free Rate on the fly  
   - Calculates and displays Call vs. Put values side-by-side for easy comparison  

3. **Customizable Ranges**  
   - Define your own Spot Price and Volatility intervals  
   - Explore option prices over any market scenario you choose  

## 🔧 Dependencies

- **`yfinance`** – fetches up-to-date asset prices  
- **`numpy`** – powers the numerical calculations  
- **`matplotlib`** – generates the heatmap visualizations  
