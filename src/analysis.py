import pandas as pd
import streamlit as st
import folium
from streamlit_folium import folium_static
from folium.plugins import MarkerCluster
from datetime import datetime
import plotly.express as px


class DataVisualization:
    '''
    --> Shows control options and graphical views   
    '''
    def __init__(self, data, geofile):
        '''
        param data: DataFrame Pandas with informations to visualize
        param geofile: URL with regions of Seattle city  
        '''
        self._data = data
        self._geofile = geofile


    def data_overview(self):
        '''
        --> General informations
        '''
        standard_columns = ['date', 'id', 'zipcode', 'price', 'price_m2', 'sqft_living', 'bedrooms', 'bathrooms', 'floors', 
                            'waterfront', 'yr_built', 'lat', 'long']
        f_attributes = st.sidebar.multiselect('Enter columns', self._data.columns)
        
        # Include standard_columns if f_attribues was defined
        if f_attributes:
            not_selected = list(set(standard_columns).difference(set(f_attributes)))
            for columns in standard_columns:
                if columns not in f_attributes: 
                    f_attributes.append(columns)
            
        f_zipcode = st.sidebar.multiselect('Enter zipcode', self._data['zipcode'].unique())

        if f_attributes != [] and f_zipcode != []:
            self._data = self._data.loc[self._data['zipcode'].isin(f_zipcode), f_attributes]
        elif f_attributes == [] and f_zipcode != []:
            self._data = self._data.loc[self._data['zipcode'].isin(f_zipcode), :]
        elif f_attributes != [] and f_zipcode == []:
            self._data = self._data.loc[:, f_attributes]
        else:
            self._data = self._data.copy()
        
        st.header('Data Overview')
        if f_attributes:
            st.dataframe(self._data.drop(not_selected, axis=1))
        else:
            st.dataframe(self._data)

        c1, c2 = st.columns((1, 1))
        # Metrics
        df1 = self._data[['id', 'zipcode']].groupby('zipcode').count().reset_index()
        df2 = self._data[['price', 'zipcode']].groupby('zipcode').mean().reset_index()
        df3 = self._data[['sqft_living', 'zipcode']].groupby('zipcode').mean().reset_index()
        df4 = self._data[['price_m2', 'zipcode']].groupby('zipcode').mean().reset_index()

        # Merge
        m1 = pd.merge(df1, df2, on='zipcode', how='inner')
        m2 = pd.merge(m1, df3, on='zipcode', how='inner')
        df = pd.merge(m2, df4, on='zipcode', how='inner')
        df.columns = ['ZIPCODE', 'ID', 'PRICE', 'SQFT_LIVING', 'PRICE M²']

        c1.subheader('Metrics')
        c1.dataframe(df)

        # Statistic Descriptive
        num_attributes = self._data.select_dtypes(include=['int64', 'float64'])
        mean = pd.DataFrame(num_attributes.mean())
        median = pd.DataFrame(num_attributes.median())
        std = pd.DataFrame(num_attributes.std())

        min = pd.DataFrame(num_attributes.min())
        max = pd.DataFrame(num_attributes.max())

        df1 = pd.concat([min, max, mean, median, std], axis=1).reset_index()
        df1.columns = ['Attributes', 'Min', 'Max', 'Mean', 'Median', 'Std']

        c2.subheader('Descriptive Analysis')
        c2.dataframe(df1)


    def density_portfolio(self):
        '''
        --> Maps visualizations
        '''
        st.header('Region Overview')

        c1, c2 = st.columns((1, 1))
        c1.subheader('Portfolio Density')

        df = self._data.sample(100)
        # Base mape - folium
        density_map = folium.Map(location=[self._data['lat'].mean(), self._data['long'].mean()], default_zoom_start=5)

        marker_cluster = MarkerCluster().add_to(density_map)
        for name, row in df.iterrows():
            folium.Marker([row['lat'], row['long']], popup=f'Sold R$ {row["price"]}, Date: {row["date"]}, bedrooms {row["bedrooms"]} bathrooms {row["bathrooms"]} year build {row["yr_built"]}').add_to(marker_cluster)
        with c1:
            folium_static(density_map)


        # Region Price Map
        c2.subheader('Price Density')
        df = self._data[['price', 'zipcode']].groupby('zipcode').mean().reset_index()
        df.columns = ['ZIP', 'PRICE']

        #df = df.sample(10)

        geofile = self._geofile[self._geofile['ZIP'].isin(df['ZIP'].tolist())]

        region_price_map = folium.Map(location=[self._data['lat'].mean(), self._data['long'].mean()], default_zoom_start=5)
        folium.Choropleth(data = df, geo_data = geofile, columns = ['ZIP', 'PRICE'], key_on='feature.properties.ZIP',
                                    fill_color='YlOrRd', fill_opacity=0.7, line_opacity=0.2, legend_name='AVG PRICE').add_to(region_price_map)

        with c2:
            folium_static(region_price_map)


    def distribution(self):
        '''
        --> Distribution plots
        '''
        st.sidebar.title('Commercial Options')
        st.header('Commercial Attributes')

        self._data['date'] = pd.to_datetime(self._data['date']).dt.strftime('%Y-%m-%d')

        # Average price per year
        # Filters
        min_year_built = int(self._data['yr_built'].min())
        max_year_built = int(self._data['yr_built'].max())

        st.sidebar.subheader('Select Max Year Built')
        f_year_built = st.sidebar.slider('Year Built', min_year_built, max_year_built, min_year_built)

        # Data Selection
        df = self._data[['yr_built', 'price']].groupby('yr_built').mean().reset_index()
        df = df[df['yr_built'] < f_year_built]
        fig = px.line(df, 'yr_built', 'price')

        st.subheader('Average Price per Year Built')
        st.plotly_chart(fig, use_container_width=True)

        # Average price per day
        st.subheader('Average Price per Day')
        st.sidebar.subheader('Select Max Date')

        # filter 
        min_date = datetime.strptime(self._data['date'].min(), '%Y-%m-%d')
        max_date = datetime.strptime(self._data['date'].max(), '%Y-%m-%d')

        f_date = st.sidebar.slider('Date', min_date, max_date, min_date)

        # Data filtering
        self._data['date'] = pd.to_datetime(self._data['date'])
        df = self._data.loc[self._data['date'] < f_date]
        df = df[['date', 'price']].groupby('date').mean().reset_index()

        fig = px.line(df, 'date', 'price')
        st.plotly_chart(fig, use_container_width=True)


    def histogram(self):
        '''
        --> Histograms views
        '''
        st.header('Price Distribution')
        st.sidebar.subheader('Select Max Price')

        # filter
        min_price = int(self._data['price'].min())
        max_price = int(self._data['price'].max())
        avg_price = int(self._data['price'].mean())

        # Data filtering
        f_price = st.sidebar.slider('Price', min_price, max_price, avg_price)
        df = self._data.loc[self._data['price'] < f_price]

        # data plot
        fig = px.histogram(df, x='price', nbins=50)
        st.plotly_chart(fig, use_container_width=True)

        # =======================
        # Feature distribution
        # =======================
        st.sidebar.title('Attributes Options')
        st.header('House Attributes')

        # filters
        f_bedrooms = st.sidebar.selectbox('Max number of bedrooms', sorted(set(self._data['bedrooms'].unique())))
        f_bathrooms = st.sidebar.selectbox('Max number of bathrooms', sorted(set(self._data['bathrooms'].unique())))

        c1, c2 = st.columns(2)

        # House per bedrooms
        c1.subheader('House per bedrooms')
        df = self._data[self._data['bedrooms'] < f_bedrooms]
        fig = px.histogram(df, x='bedrooms', nbins=19)
        c1.plotly_chart(fig, use_container_width=True)

        # House per bathrooms
        c2.subheader('House per bathrooms')
        df = self._data[self._data['bathrooms'] < f_bathrooms]
        fig = px.histogram(df, x='bathrooms', nbins=19)
        c2.plotly_chart(fig, use_container_width=True)

        # House per floors
        # filters
        c1, c2 = st.columns(2)

        c1.subheader('House per floors')
        f_floors = st.sidebar.selectbox('Max number of floors', sorted(set(self._data['floors'].unique())))
        df = self._data[self._data['floors'] < f_floors]
        fig = px.histogram(df, x='floors', nbins=19)
        c1.plotly_chart(fig, use_container_width=True)

        # House per water views
        # Filters
        f_waterview = st.sidebar.checkbox('Only Houses with Water View')

        if f_waterview:
            df = self._data[self._data['waterfront'] == 1]
        else:
            df = self._data.copy()

        c2.subheader('House per water view')
        fig = px.histogram(df, x='waterfront', nbins=10)
        c2.plotly_chart(fig, use_container_width=True)
