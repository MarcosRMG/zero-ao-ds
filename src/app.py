import streamlit as st
from etl import get_data, get_geofile
from analysis import DataVisualization

# Enviroment config
st.set_page_config(layout='wide')

# Data
data = get_data('./data/kc_house_data.csv')
geofile = get_geofile('https://opendata.arcgis.com/datasets/83fc2e72903343aabff6de8cb445b81c_2.geojson')


def main(data, geofile):
    st.title('House Sales in King County, USA')
    visualization = DataVisualization(data, geofile)
    visualization.data_overview()
    visualization.density_portfolio()
    visualization.histogram()
    

if __name__ == '__main__':
    main(data, geofile)
