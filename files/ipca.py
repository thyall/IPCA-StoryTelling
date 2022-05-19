"""
Author: Thyall
Data: May 2022
IPCA Storytelling
"""
import logging
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from matplotlib import style


logging.basicConfig(
    filename='./results.log',
    level=logging.INFO,
    filemode='w',
    format='%(name)s - %(levelname)s - %(message)s')


def read_data(file_path):
    '''
    Args:
        file_path: (string) path from the file

    Returns:
            Dataframe
    '''
    try:
        assert isinstance(file_path, str)
        df_func = pd.read_csv(file_path, sep=";")
        shape = df_func.shape[0]
        logging.info(f"SUCCESS: There are {shape} rows in your dataframe")
        return df_func

    except FileNotFoundError:
        logging.error(f"ERROR: we were not able to find {file_path}")
        return None

    except AssertionError:
        logging.error("ERROR: Error type")
        return None


df_ipca = read_data('C:/Users/Pichau/Documents/mlops/ipca/files/ipca.csv')

df_ipca.rename(
    columns={
        'IPCA dessazonalizado - Variação mensal (%)': 'IPCA',
    },
    inplace=True)

df_ipca['IPCA'] = df_ipca['IPCA'].str.replace(',', '.')
df_ipca['IPCA'] = df_ipca['IPCA'].astype(float)

df_ipca['rolling_mean'] = df_ipca['IPCA'].rolling(60).mean()

df_ipca['date'] = df_ipca['Mês'].str.split(' ').str[1]

df_ipca['date'] = pd.to_datetime(df_ipca['date'], format='%Y')

df_ipca_lula = df_ipca.copy()[(df_ipca['date'].dt.year <= 2011)]

df_ipca_dilma = df_ipca.copy()[
    (df_ipca['date'].dt.year >= 2011) & (
        df_ipca['date'].dt.year <= 2016)]

df_ipca_temer = df_ipca.copy()[
    (df_ipca['date'].dt.year >= 2016) & (
        df_ipca['date'].dt.year <= 2019)]

df_ipca_bolsonaro = df_ipca.copy()[(df_ipca['date'].dt.year >= 2019)]

# Adding the FiveThirtyEight style
style.use('fivethirtyeight')

# Adding the subplots
fig = plt.figure(figsize=(16, 8), dpi=300)
ax1 = plt.subplot(2, 4, 1)
ax2 = plt.subplot(2, 4, 2)
ax3 = plt.subplot(2, 4, 3)
ax4 = plt.subplot(2, 4, 4)
ax5 = plt.subplot(2, 1, 2)

axes = [ax1, ax2, ax3, ax4, ax5]

# Changes to all the subplots
for ax in axes:
    ax.set_ylim(0.0, 0.7)
    ax.set_yticks([0.0, 0.2, 0.4, 0.6])
    ax.set_yticklabels(['0.0', '0.2', '0.4', '0.6'],
                       alpha=0.3)
    ax.grid(alpha=0.5)

### Ax1: Lula
ax1.plot(df_ipca_lula['date'], df_ipca_lula['rolling_mean'],
         color='#BF5FFF')
ax1.set_xticklabels(['', '2003', '',
                     '2007', '', '2011', ''],
                    alpha=0.3)

### Ax2: Dilma
ax2.plot(df_ipca_dilma['date'], df_ipca_dilma['rolling_mean'],
         color='#ffa500')
ax2.set_xticklabels(['', '2011', '', '2013', '',
                     '2015', '', '2016'],
                    alpha=0.3)

### Ax3: Temer
ax3.plot(df_ipca_temer['date'], df_ipca_temer['rolling_mean'],
         color='#00B2EE')
ax3.set_xticklabels(['', '2017', '', '2018', '', '2019', '', ],
                    alpha=0.3)

### Ax4: Bolsonaro
ax4.plot(df_ipca_bolsonaro['date'], df_ipca_bolsonaro['rolling_mean'],
         color='#FF0000')
ax4.set_xticklabels(['', '2019', '', '2020', '', '2021', ''],
                    alpha=0.3)


### Ax4: Bush-Obama-Trump
ax5.plot(df_ipca_lula['date'], df_ipca_lula['rolling_mean'],
         color='#BF5FFF')
ax5.plot(df_ipca_dilma['date'], df_ipca_dilma['rolling_mean'],
         color='#ffa500')
ax5.plot(df_ipca_temer['date'], df_ipca_temer['rolling_mean'],
         color='#00B2EE')
ax5.plot(df_ipca_bolsonaro['date'], df_ipca_bolsonaro['rolling_mean'],
         color='#FF0000')
ax5.grid(alpha=0.5)
ax5.set_xticks([])

"""
### IPCA rate averaged under the last four Brazil presidents


###### IPCA exchange rates under Lula (2003 - 2011), Dilma (2011-2016), Temer (2017-2019, Bolsonaro (2019-)
"""

st.pyplot(fig)

if __name__ == "__main__":
    read_data('/ipca.csv')
    read_data('wrong_string')
    read_data(5)