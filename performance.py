import pandas as pd
from dolar_mep_getter import *
from excel_exporter import export_to_excel
from stock_price_getter import *
import openpyxl

file = './my_current_stock.xlsx'
cedears_df = pd.read_excel(file)

### BUY DATE VALUES
#Add the MEP value at the buy date of each cedear.
cedears_df['Buy Date MEP value'] = cedears_df['Date'].apply(get_dolar_mep)
print("Valor dolar mep al momento de cada compra obtenido")
#Add the stock MEP value at the buy date of each cedear.
cedears_df['Buy Price (U$D)'] = (cedears_df['Buy Price (AR$)'] / cedears_df['Buy Date MEP value']).round(2)
print("Precio de cada compra en dolares obtenido")

### CURRENT VALUES
#Get current MEP value
current_mep_value = get_dolar_mep_now()
#Add current stock pesos value of each cedear
cedears_df['Current Price (AR$)'] = cedears_df['Ticker'].apply(get_current_pesos_stock_value).round(2)
#Add current stock MEP value of each cedear
cedears_df['Current Price (U$D)'] = (cedears_df['Current Price (AR$)'] / current_mep_value).round(2)
print("Precio actual de cada acción obtenido")

### MEP REFERENCE
#Compare buy MEP value with current MEP value
cedears_df['Variacion MEP'] = 100 * (current_mep_value/cedears_df['Buy Date MEP value'] - 1)
cedears_df['Variacion MEP'] = cedears_df['Variacion MEP'].round(2)

### PERFORMANCE
#Add performance in ARS
cedears_df['Performance AR$'] = 100 * ((cedears_df['Current Price (AR$)'] / cedears_df['Buy Price (AR$)']) - 1)
cedears_df['Performance AR$'] = cedears_df['Performance AR$'].round(2)
#Add performance in MEP
cedears_df['Performance U$D'] = 100 * ((cedears_df['Current Price (U$D)'] / cedears_df['Buy Price (U$D)']) - 1)
cedears_df['Performance U$D'] = cedears_df['Performance U$D'].round(2)

print("Calculando performance y ganancias")

### REVENUE
#Add revenue in ARS
cedears_df['Revenue AR$'] = ((cedears_df['Current Price (AR$)'] - cedears_df['Buy Price (AR$)']) * cedears_df['Quantity']).round(2)
#Add revenue in MEP
cedears_df['Revenue U$D'] = ((cedears_df['Current Price (U$D)'] - cedears_df['Buy Price (U$D)']) * cedears_df['Quantity']).round(2)

#Delete unnecessary columns
cedears_df.drop(['Buy Date MEP value'], axis=1, inplace=True)

### TOTALS
#AR$ totals
total_invested_ars = (cedears_df['Buy Price (AR$)'] * cedears_df['Quantity']).sum()
current_value_ars = (cedears_df['Current Price (AR$)'] * cedears_df['Quantity']).sum()
revenue_ars = cedears_df['Revenue AR$'].sum()
performance_ars = 100 * ((current_value_ars / total_invested_ars) - 1).round(2)
#U$D totals
total_invested_usd = (cedears_df['Buy Price (U$D)'] * cedears_df['Quantity']).sum()
current_value_usd = (cedears_df['Current Price (U$D)'] * cedears_df['Quantity']).sum()
revenue_usd = cedears_df['Revenue U$D'].sum()
performance_usd = 100 * ((current_value_usd / total_invested_usd) - 1).round(2)

data_totals = {
    'Total Invested AR$': [total_invested_ars],
    'Current Value AR$': [current_value_ars],
    'Revenue AR$': [revenue_ars],
    'Performance AR$': [performance_ars],
    'Total Invested U$D': [total_invested_usd],
    'Current Value U$D': [current_value_usd],
    'Revenue U$D': [revenue_usd],
    'Performance U$D': [performance_usd]
}

totals_df = pd.DataFrame(data_totals)

print("Valor actual dolar mep: " + str(current_mep_value))

try:
    export_to_excel(cedears_df, totals_df)
    print("Exportado a excel")
except:
    print("Error exporting to excel")
