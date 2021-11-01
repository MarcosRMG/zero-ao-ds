import streamlit as st
import folium
from streamlit_folium import folium_static
from folium.plugins import MarkerCluster
import plotly.express as px


class DataVisualization:
    '''
    --> Shows control options and graphical views   
    '''
    def __init__(self, data, geofile, attributes=None, zipcode=None, columns_not_selected=None, min_price=None, max_price=None, avg_price=None, bedrooms=None, 
                bathrooms=None, floors=None, waterview=None):
        '''
        --> Apply filters and show visualizations about the data

        :param data: DataFrame Pandas with informations to visualize
        :param geofile: URL with regions of Seattle city  
        :param attributes: The attributes filters of a house
        :param zipcode: The zipcode of house location
        :param columns_not_selected: Columns not filtered for the use
        :param min_price: Min price filter of a house
        :param max_price: Max price filter of a house
        :param avg_price: Average price fiter of a house
        :param bedrooms: Max number of bedrooms to filter
        :param bathrooms: Max number of bathrooms to filter
        :param floors: Max number of floors to filter
        :para waterview: Filter only houses with waterview 
        '''
        self._data = data
        self._geofile = geofile
        self._attributes = attributes
        self._zipcode = zipcode
        self._columns_not_selected = columns_not_selected
        self._min_price = min_price
        self._max_price = max_price
        self._avg_price = avg_price
        self._bedrooms = bedrooms
        self._bathrooms = bathrooms
        self._floors = floors
        self._waterview = waterview


    def columns_filter(self):
        '''
        --> Options to filter the columns display
        '''
        # Columns that can't be excluded from DataFrame
        standard_columns = ['date', 'id', 'zipcode', 'price', 'price_m2', 'sqft_living', 'bedrooms', 'bathrooms', 'floors', 
                            'waterfront', 'yr_built', 'lat', 'long']

        # Column filter
        self._attributes = st.sidebar.multiselect('Enter columns', self._data.columns, default=['id', 'price', 'bedrooms', 'bathrooms', 'floors', 
                                                                                                'recommendation'])
        
        # Include standard_columns if f_attribues was defined
        if self._attributes:
            self._not_selected = list(set(standard_columns).difference(set(self._attributes)))
            for columns in standard_columns:
                if columns not in self._attributes: 
                    self._attributes.append(columns)

        # Zipcode filter    
        f_zipcode = st.sidebar.multiselect('Enter zipcode', self._data['zipcode'].unique())

        # DataFrame attribution
        if self._attributes != [] and f_zipcode != []:
            self._data = self._data.loc[self._data['zipcode'].isin(f_zipcode), self._attributes]
        elif self._attributes == [] and f_zipcode != []:
            self._data = self._data.loc[self._data['zipcode'].isin(f_zipcode), :]
        elif self._attributes != [] and f_zipcode == []:
            self._data = self._data.loc[:, self._attributes]
        else:
            self._data
        

    def price_filter(self):
        '''
        --> Filter the max price of house to display portfolio options
        '''    
        # Selector
        st.sidebar.subheader('Select Max Price')
        # Range definiiton
        self._min_price = int(self._data['price'].min())
        self._max_price = int(self._data['price'].max())
        # Set price
        f_price = st.sidebar.slider('Price', self._min_price, self._max_price, self._max_price)
        # DataFrame reassignment
        self._data = self._data.loc[self._data['price'] <= f_price]


    def feature_options(self):
        '''
        --> Filter the caracteristics of the house
        '''
        # filters
        st.sidebar.title('Attributes Options')
        self._bedrooms = st.sidebar.selectbox('Max number of bedrooms', sorted(set(self._data['bedrooms'].unique()), reverse=True))
        self._bathrooms = st.sidebar.selectbox('Max number of bathrooms', sorted(set(self._data['bathrooms'].unique()), reverse=True))
        self._floors = st.sidebar.selectbox('Max number of floors', sorted(set(self._data['floors'].unique()), reverse=True))
        self._waterview = st.sidebar.checkbox('Only Houses with Water View')

        # DataFrame slice
        self._data = self._data[(self._data['bedrooms'] <= self._bedrooms) & (self._data['bathrooms'] <= self._bathrooms) & (self._data['floors'] <= self._floors)]

        if self._waterview:
            self._data = self._data[self._data['waterfront'] == 1]
    
    
    def data_overview(self):
        '''
        --> General informations in tables with all columns or selected columns
        '''       
        if self._data.empty:
            st.header('No Houses Available')      
        else:
            st.header('Data Overview')
            if self._attributes:
                st.dataframe(self._data.drop(self._not_selected, axis=1).reset_index(drop=True))
                st.subheader('Descriptive Analysis')
                st.dataframe(self._data.drop(columns=['zipcode', 'waterfront', 'lat', 'long']).describe().T[['mean', '50%', 'std', 'min', 'max']].rename(columns={'50%': 'median'}))
            else:
                st.dataframe(self._data.reset_index(drop=True))
                st.subheader('Descriptive Analysis')
                st.dataframe(self._data.drop(columns=['zipcode', 'waterfront', 'lat', 'long']).describe().T[['mean', '50%', 'std', 'min', 'max']].rename(columns={'50%': 'median'}))


    def density_portfolio(self):
        '''
        --> Maps visualizations
        '''
        

        if self._data.empty:
           st.write('')

        else:
            st.header('Region Overview')

            c1, c2 = st.columns((1, 1))
            c1.subheader('Portfolio Density')
            # Base mape - folium
            density_map = folium.Map(location=[self._data['lat'].mean(), self._data['long'].mean()], default_zoom_start=5)

            marker_cluster = MarkerCluster().add_to(density_map)
            for name, row in self._data.iterrows():
                folium.Marker([row['lat'], row['long']], popup=f'Sold R$ {row["price"]}, Date: {row["date"]}, bedrooms {row["bedrooms"]} bathrooms {row["bathrooms"]} year build {row["yr_built"]}').add_to(marker_cluster)
            with c1:
                folium_static(density_map)


            # Region Price Map
            c2.subheader('Price Density')
            df = self._data[['price', 'zipcode']].groupby('zipcode').mean().reset_index()
            df.columns = ['ZIP', 'PRICE']

            geofile = self._geofile[self._geofile['ZIP'].isin(df['ZIP'].tolist())]

            region_price_map = folium.Map(location=[self._data['lat'].mean(), self._data['long'].mean()], default_zoom_start=5)
            folium.Choropleth(data = df, geo_data = geofile, columns = ['ZIP', 'PRICE'], key_on='feature.properties.ZIP',
                                        fill_color='YlOrRd', fill_opacity=0.7, line_opacity=0.2, legend_name='AVG PRICE').add_to(region_price_map)

            with c2:
                folium_static(region_price_map)


    def price_distribuition(self):
        '''
        --> Histograms views
        '''
        if self._data.empty:
            st.write('')
        else:
            st.header('Price Distribution')
            fig = px.histogram(self._data, x='price', nbins=50)
            st.plotly_chart(fig, use_container_width=True)
        

    def feature_distribution(self):   
        '''
        --> Show houses attributes counts
        '''
        if self._data.empty:
            st.write('')
        else:   
            st.header('House Attributes')
            c1, c2 = st.columns(2) 

            # House per bedrooms
            c1.subheader('House per bedrooms')
            _ = self._data['bedrooms'].value_counts()
            fig = px.bar(_, x=_.index, y=_.values, labels={'index': 'Bedrooms', 'y': 'Count'})
            c1.plotly_chart(fig, use_container_width=True)

            # House per bathrooms
            c2.subheader('House per bathrooms')
            _ = self._data['bathrooms'].value_counts()
            fig = px.bar(_, x=_.index, y=_.values, labels={'index': 'Bathrooms', 'y': 'Count'})
            c2.plotly_chart(fig, use_container_width=True)

            # House per floors
            c3, c4 = st.columns(2)

            c3.subheader('House per floors')
            _ = self._data['floors'].value_counts()
            fig = px.bar(_, x=_.index, y=_.values, labels={'index': 'Floors', 'y': 'Count'})
            c3.plotly_chart(fig, use_container_width=True)

            # Waterfront
            c4.subheader('House per water view')
            _ = self._data['waterfront'].replace({0: 'No', 1: 'Yes'}).value_counts()
            fig = px.bar(_, x=_.index, y=_.values, labels={'index': 'Water Front', 'y': 'Count'})
            c4.plotly_chart(fig, use_container_width=True)
