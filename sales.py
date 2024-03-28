#importing dependencies 
import numpy as np, pandas as pd, plotly.express as px, streamlit as st 

#load the data
df = pd.read_csv('superstore_cleaned.csv')

#page confirguration
st.set_page_config('SuperStore Sales Dashboard', page_icon='🏪', layout='wide')
st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)

#page title
st.markdown('# :green[🏪SuperStore] Sales', unsafe_allow_html=True)
st.markdown(':green[SuperStore] is a very large retail establishment that offers a :green[wide variety] of merchandise for sale.Superstores are typically built outside city centres, away from other shops2. They are known for :green[selling goods at lower prices] compared to other stores. These stores are :green[designed to cater to all the shopping needs of consumers] under one roof.', unsafe_allow_html=True)

t1, t2,t3 = st.tabs(['Summary View','Category analysis','Dataset'])


with st.sidebar:
  with st.container(border=True):
    st.write('Filters')
    df["Order Date"] = pd.to_datetime(df["Order Date"])
    startdate = pd.to_datetime(df['Order Date']).min()
    enddate = pd.to_datetime(df['Order Date']).max()
    
    s1,s2 = st.columns([0.5,0.5])
    
    with s1:
      start = pd.to_datetime(st.date_input('Start Date',startdate))
    with s2:
      end = pd.to_datetime(st.date_input('End Date', enddate))
      
    df2 = df[(df['Order Date']>=startdate) & (df['Order Date']<=enddate)].copy()
        
    #----Ship Mode----#
    
    ship = st.multiselect(options=list(df2['Ship Mode'].unique()), label='Select the Ship Modes')
    
    if not ship:
      df3 = df2.copy()
    else:
      df3 = df2[df2['Ship Mode'].isin(ship)]
      
    #----Customer Segment----#
    
    segment = st.multiselect(options=list(df['Segment'].unique()), label='Select the Customer Segment')
    
    if not segment:
      df4 = df3.copy()
    else:
      df4 = df3[df3['Segment'].isin(segment)]
      
    #----City----#
    
    city = st.multiselect(options=list(df['City'].unique()), label='Choose the City')
    
    if not city:
      df5 = df4.copy()
    else:
      df5 = df4[df4['City'].isin(city)]
      
    #----State---
    
    state = st.multiselect(options=list(df['State'].unique()), label='Choose the State')
    
    if not state:
      df6 = df5.copy()
    else:
      df6 = df5[df5['State'].isin(state)]
      
    #----Region
    
    region = st.multiselect(options=list(df['Region'].unique()), label='Choose the Region')
    
    if not region:
      df7 = df6.copy()
    else:
      df7 = df6[df6['Region'].isin(region)]
      
    #----Category----#
    
    category = st.multiselect(options=list(df['Category'].unique()), label='Choose Category')
    
    if not category:
      df8 = df7.copy()
    else:
      df8 = df7[df7['Category'].isin(category)]
      
    #----Sub category----#
    
    sub_category = st.multiselect(options=list(df['Sub-Category'].unique()), label='Choose the Sub Category ')
    
    if not sub_category:
      df9 = df8.copy()
    else:
      df9 = df8[df8['Sub-Category'].isin(sub_category)]
#['Order Date', 'Ship Date', 'Ship Mode', 'Segment', 'Country', 'City',
   #    'State', 'Region', 'Category', 'Sub-Category', 'Product Name', 'Sales',
 #      'Quantity', 'Discount', 'Profit']
 
with t1:
  c1, c2 = st.columns([0.50,0.50])
 
  with c1:
    c3,c4,c5 = st.columns([0.32,0.32,0.25])
  
    def pct(total, last3): #function for deltas
      return "{:.2f}%".format(round(((total-last3)/last3)*100,2))
  
    with c3:
      
      filterdf1 = df9[df9['year'] < df9['year'].max()]
      profit2 = filterdf1['Profit'].sum()
      profit1 = df9['Profit'].sum()
      
      st.metric(value="{:,}".format(round(df9['Profit'].sum(),2)),
                label='Total Profit', delta=f'{pct(profit1,profit2)} last years')
      with c4:
        
        filterdf1 = df9[df9['year'] < df9['year'].max()]
        sales2 = filterdf1['Sales'].sum()
        sales1 = df9['Sales'].sum()
        
        st.metric(value="{:,}".format(round(df9['Sales'].sum(),2)),
                  label='Total Sales', delta=f'{pct(sales1,sales2)} last years')
      with c5:
        
        quan2 = filterdf1['Quantity'].sum()
        quan1 = df9['Quantity'].sum()
        
        st.metric(value = "{:,}".format(df9['Quantity'].sum()), label='Total Quantity Sold', delta=f'{pct(quan1,quan2)} last years')
        
    c6 = st.columns(1)
    color_scale = ["#A6F6AF", "#3DD56D"]
    st.markdown('##### :green[Sales] and :green[Profit] Over the Years')
    filterdf2 = df9.groupby('year').agg({'Profit':'sum','Sales':'sum'}).reset_index()
    fig3 = px.line(filterdf2, x = 'year', y = ['Profit','Sales'], color_discrete_sequence=color_scale)
    st.plotly_chart(fig3, use_container_width=True)
    
  with c2:
    col1,cl1,_ = st.columns([0.40,0.20,0.45])
    
    def format_number(num):
      if num >= 1000:
        return "{:.1f}k".format(num/1000)
      else:
        return str(num)
      
    with cl1:
      option1 = st.selectbox(options=['Sales','Profit'], label='')
    with col1:
      if option1=='Sales':
        st.markdown('##### <br/>Category wise :green[Sales] by year', unsafe_allow_html=True)
      else:
        st.markdown('##### <br/>Category wise :green[Profit] by year', unsafe_allow_html=True)
    
    if option1=='Sales':
      color_scale = ["#A6F6AF", "#7EDD89", "#3DD56D"]
      st.write('This shows the Sales throughout year by category.')    
      catdf = df9.groupby(['Category','year'], as_index=False)['Sales'].sum()
      
# Create a new column for the text to be displayed on the bars
      catdf['text'] = catdf['Sales'].apply(lambda x: format_number(x))

# Create the horizontal bar chart
      fig1 = px.bar(catdf, y="year", x="Sales", color="Category", text='text', orientation='h',color_discrete_sequence=color_scale)
      fig1.update_xaxes(showticklabels=False, title_text='')
      fig1.update_traces(textfont=dict(size=20))
      st.plotly_chart(fig1, use_container_width=True)
      
    else:
      color_scale = ["#A6F6AF", "#7EDD89", "#3DD56D"]
      st.write('This shows the Profit throughout year by category.')
      catdf = df9.groupby(['Category','year'], as_index=False)['Profit'].sum()
      catdf['text'] = catdf['Profit'].apply(lambda x: format_number(x))
      fig1 = px.bar(catdf, y="year", x="Profit", color="Category",orientation='h', text='text',color_discrete_sequence=color_scale)
      fig1.update_xaxes(showticklabels = False, title_text = '')
      fig1.update_traces(textfont=dict(size=20))
      st.plotly_chart(fig1, use_container_width=True)

  c7,c8,c9 = st.columns([0.30,0.30,0.40])

  with c7:
    st.markdown('##### :green[Distribution] of Category of Items')
    st.write('This show the Distribution percentage of Category items ordered by Consumers.')
    green_colors = ["#0D3300", "#265C00", "#3E8500", "#57AE00", "#70D700"]
    filterdf3 = df['Category'].value_counts()
    fig4 = px.pie(filterdf3, values=filterdf3.values, labels=filterdf3.index, names = filterdf3.index, color_discrete_sequence=green_colors)
    fig4.update_traces(textinfo='percent+label')
    fig4.update_traces(textfont=dict(size = 15))
    fig4.update_layout(showlegend=False, margin=dict(l=0, r=0, b=0, t=0), height = 300, width = 300)
    st.plotly_chart(fig4, use_container_width=True)
    
  with c8:
    st.markdown('##### :green[Distribution] of Sub-Category of Category Items')
    st.write("This show the Distribution percentage of each Category's Sub Category itemsordered by Consumers.")
    filterdf4 = df8[df8['Category'].isin(category)]['Sub-Category'].value_counts()
    if not category:
      filterdf4 = df8[df8['Category']=='Furniture']['Sub-Category'].value_counts()
      fig5 = px.pie(filterdf4, labels=filterdf4.index, names = filterdf4.index, color_discrete_sequence=green_colors)
      fig5.update_traces(textinfo = 'percent+label')
      fig5.update_traces(textfont = dict(size=15), hole= 0.4)
      fig5.update_layout(showlegend = False,margin=dict(l=0, r=0, b=0, t=0), height = 300, width = 300)
      st.plotly_chart(fig5, use_container_width=True)
    else:
      filterdf4 = df8[df8['Category'].isin(category)]['Sub-Category'].value_counts()
      fig5 = px.pie(filterdf4, labels=filterdf4.index, names = filterdf4.index, color_discrete_sequence=green_colors)
      fig5.update_traces(textinfo = 'percent+label')
      fig5.update_traces(textfont = dict(size=15), hole = 0.4)
      fig5.update_layout(showlegend = False,margin=dict(l=0, r=0, b=0, t=0), height = 300, width = 300)
      st.plotly_chart(fig5, use_container_width=True)
      
  with c9:
    
    if option1=='Sales':
      
      st.markdown('##### Yearly Distribution of :green[Sales] Across Regions')
      st.write('This visualization allows us to compare sales trends across these areas, revealing which regions are strongest at various points in the year.')
      filterdf6 = df9.groupby(['year','Region'], as_index=False)['Sales'].sum()
      filterdf6['sales'] = filterdf6['Sales'].apply(lambda x: format_number(x))
      
      fig7 = px.bar(filterdf6, x = 'Sales', y = 'year', color='Region', orientation='h',color_discrete_sequence=green_colors, text = 'sales')
      fig7.update_xaxes(showticklabels=False, title_text='')
      fig7.update_traces(textfont=dict(size=20))
      st.plotly_chart(fig7, use_container_width=True)
    else:
      
      st.markdown('##### Yearly Distribution of :green[Profit] Across Regions')
      st.write('This visualization allows us to compare Profit trends across these areas, revealing which regions are strongest at various points in the year.')
      filterdf6 = df9.groupby(['year','Region'], as_index=False)['Profit'].sum()
      filterdf6['profit'] = filterdf6['Profit'].apply(lambda x: format_number(x))
      
      fig7 = px.bar(filterdf6, x = 'Profit', y = 'year', color='Region',orientation='h', color_discrete_sequence=green_colors, text = 'profit')
      fig7.update_xaxes(showticklabels=False, title_text='')
      fig7.update_traces(textfont=dict(size=20))
      st.plotly_chart(fig7, use_container_width=True)
    
    
  c10,c11 = st.columns([0.7,0.3])
  
  with c10:
    st.markdown('##### Sales and Profit by state')
    st.write('This Shows the Choropleth map of USA all states.')
    filterdf5 = df9.groupby('State')['Sales'].sum().reset_index()
    
    import json, urllib.request

    url = 'https://raw.githubusercontent.com/PublicaMundi/MappingAPI/master/data/geojson/us-states.json'

    with urllib.request.urlopen(url) as response:
      geojson = json.load(response)

    fig6 = px.choropleth(filterdf5, geojson=geojson, locations='State', color='Sales',
                     scope='usa', featureidkey='properties.name',
                     color_continuous_scale='Greens')  # Use 'Greens' color scale

    fig6.update_geos(showcountries=False, showcoastlines=True, showland=True, fitbounds="locations")
    fig6.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    st.plotly_chart(fig6, use_container_width=True)
    
  with c11:
    st.markdown('##### Monthly Analysis of :green[Sales-Profit] Relationship')
    st.write('How sales and profits interact & influence. This could involve identifying trends, patterns, or anomalies.')
    filterdf7 = df9.groupby('month', as_index=False).agg({'Profit':'sum','Sales':'sum'})
    color_map = {'January': 'lightgreen', 'February': 'mediumseagreen', 'March': 'seagreen', 
             'April': 'forestgreen', 'May': 'green', 'June': 'darkgreen', 
             'July': 'lightgreen', 'August': 'mediumseagreen', 'September': 'seagreen', 
             'October': 'forestgreen', 'November': 'green', 'December': 'darkgreen'}
    fig8 = px.scatter(filterdf7, x = 'Sales', y = 'Profit', size='Sales',color='month',size_max=21,color_discrete_map=color_map)
    st.plotly_chart(fig8, use_container_width=True)

      
with t2:
  st.markdown('##### :green[Hierarchical] Distribution of All Categories ')
  st.write('This show the distribution of each category to it sub-category by Sales and Profit by Regions.')
  fig9 = px.treemap(df9, path = ['Region','Category','Sub-Category'], values = 'Sales', hover_data='Sales',color = 'Sub-Category', height=700,color_continuous_scale='Greens')
  st.plotly_chart(fig9, use_container_width=True)
  
  st.markdown('##### :green[Sales] & :green[Profit] Performance: Top 10 Sub-Categories')
  import plotly.figure_factory as ff
  col2,col3,_,_=st.columns([0.15,0.35,0.25,0.25])
  with col2:
    option2 = st.selectbox(options=['Sales','Profit'], label='Select the View')
    
  if option2=='Sales':
    show_df = df.groupby(['Region','Sub-Category'], as_index=False).agg({'Sales':'sum','Profit':'sum','Quantity':'sum'}).sort_values(by = 'Sales', ascending=False).head(10)
  
    fig10 = ff.create_table(show_df, colorscale=color_scale)
    fig10.layout.font.size = 21
    st.plotly_chart(fig10, use_container_width=True)
    st.write('Data View by :green[Sales]')
    pivotdf = pd.pivot_table(df, values='Sales',index='Sub-Category',columns = 'month').fillna(0)
    st.dataframe(pivotdf.style.background_gradient(cmap = 'Greens'), use_container_width=True)
    
  else:
    
    show_df = df.groupby(['Region','Sub-Category'], as_index=False).agg({'Sales':'sum','Profit':'sum','Quantity':'sum'}).sort_values(by = 'Profit', ascending=False).head(10)
  
    fig10 = ff.create_table(show_df, colorscale=color_scale)
    fig10.layout.font.size = 21
    
    st.plotly_chart(fig10, use_container_width=True)
    st.write('Data View by :green[Profit]')
    pivotdf = pd.pivot_table(df, values='Profit',index='Sub-Category',columns = 'month').fillna(0)
    st.dataframe(pivotdf.style.background_gradient(cmap = 'Greens'), use_container_width=True)
  
  
with t3:
  st.markdown('###### :green[SuperStore] Dataset')
  st.write('This Data can be sorted by Filter')
  st.dataframe(df9, use_container_width=True)
  
  st.markdown('Original Dataset used in Dashboard Making')
  odf = pd.read_csv('Superstore.csv', encoding='ISO--8859-1')
  st.dataframe(odf, hide_index=True)