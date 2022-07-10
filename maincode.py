#importing dependencies

import pandas as pd
import numpy as np
import plotly
import chart_studio
import .graph_objs as go
import warnings
import plotly.express as px
#writing message of step execution 
def msg(i):
    print("STEP [",i,"] Executed with no ERRORS.    :-)")
    print(60*'=')

#signing in plotly

chart_studio.tools.get_credentials_file('hariviratmuthyam','9A5xwENqvyTkWE7wosmp')
chart_studio.tools.set_config_file(world_readable=True, sharing='public')
chart_studio.plotly.sign_in('hariviratmuthyam','9A5xwENqvyTkWE7wosmp')
msg(1)

#setting data to 2 decimals
pd.set_option('display.float.format',lambda x: "%.2f"% x)

#ignoring warnings
warnings.filterwarnings('ignore')

#reading data from excel
inbound_tourists = pd.read_excel("D://virat//travel_data.xls", sheet_name="number_of_arrival")
country_list = pd.read_excel("D://virat//travel_data.xls", sheet_name="country code")
msg(2)
#defining  a function to select rows and columns

def data_selection(df,cname):
    #merge the data frame with country list data frame by county Code, so we can drop irrelevant rows
    df = pd.merge(country_list, df, left_on = "Country Code", right_on = "Country Code", how="left")
    df = df.set_index(cname)
    #select columns from year 2007 to 2017
    df_new = pd.concat([df["Country Code"],df.loc[:,"2007":"2017"]], axis=1)
    #replace missing value by 0
    df_new = df_new.fillna(0)
    return df_new

cname='Country Name_x'
inbound_tourists_clean = data_selection(inbound_tourists,cname)
msg(3)

#Reshaping Data using stack
def reshape_data(df):
    df_new = df[:] 
    df_new.set_index(["Country Code"], inplace = True, append = True)
    #use stack to change the data frame shape
    df_new = df_new.stack()
    df_new = pd.DataFrame(df_new)
    df_new = df_new.reset_index()
    #rename column names
    df_new = df_new.rename(columns = {"level_2":"Year",0:"Amount"})
    return df_new

inbound_tourists_stack = reshape_data(inbound_tourists_clean)
msg(4)
# Map Plot using plotly_express 
inbound_map = px.choropleth(inbound_tourists_stack, 
                            locations="Country Code", 
                            color="Amount", 
                            hover_name="Country Name_x",
                            #set the animation slide bar
                            animation_frame="Year",
                            color_continuous_scale=px.colors.sequential.BuGn,
                            #set the map type
                            projection="natural earth")

plotly.offline.plot(inbound_map, filename="D://virat//inbound_map")
msg(5)


#finding top countries that attract Tourists
top_country_inbound = inbound_tourists_clean.sort_values("2017", ascending=False).head(10)
top_inbound_country_list = list(top_country_inbound.index)
msg(6)

#selecting top countries data
top_inbound_data = inbound_tourists_stack.loc[inbound_tourists_stack["Country Name_x"].isin(top_inbound_country_list)]
msg(7)
#make the line plot for top countries

inbound_top = px.line(top_inbound_data, 
                      x="Year", 
                      y="Amount", 
                      color="Country Name_x", 
                      line_group="Country Name_x",  
                      line_shape="linear", 
                      title="Top countries that attract tourists")

plotly.offline.plot(inbound_top, filename="D://virat//inbound_top")
msg(8)

#define function to calculate yearly military spending growth
def growth_inbound(df):
    for year in range(2007, 2017,1):
        # add growth columns 
        df["growth"+ str(year+1)] = (df[str(year+1)] - df[str(year)])/df[str(year)]*100
        df_new = df.iloc[:, -10:]
    return df_new

growth_inbound_data = growth_inbound(top_country_inbound)
growth_inbound_data = growth_inbound_data.stack()
growth_inbound_data = growth_inbound_data.reset_index()
growth_inbound_data = growth_inbound_data.rename(columns = {"level_1":"Year",0:"Amount"})
msg(9)

#make the bar plot of countrys inbound tourists growth
growth_bar = px.bar(growth_inbound_data, 
                         x="Year", 
                         y="Amount", 
                         color="Country Name_x", 
                         hover_name="Country Name_x",
                         #make grouped bar code
                         barmode="group",
                         title="Top attractive countries inbound tourists yearly growth rate")
plotly.offline.plot(growth_bar, filename="D://virat//growth_bar")
msg(10)
#top countries with highest receipts from tourists

receipts = pd.read_excel("D://virat//travel_data.xls", sheet_name="receipts for travel items", header=0, index_col=0)
msg(11)
#using data selection function to select inbound tourists data
cname="Country Name"
receipts_clean = data_selection(receipts,cname)

msg(12)

#find the top countries with the attract tourists most
top_country_receipts = receipts_clean.sort_values("2017", ascending=False).head(10)
top_receipts_country_list = list(top_country_receipts.index)
msg(13)

#select top countries data
top_receipts_data = receipts_clean.loc[receipts_clean.index.isin(top_receipts_country_list)]
msg(14)

#use "reshape_data" function to reshape the inbound_touists_clean data frame
receipts_clean_stack = reshape_data(top_receipts_data)
msg(15)

#make the bar plot of the top countries with highest receipts from trouism
receipts_bar = px.bar(receipts_clean_stack, 
                      x="Year", 
                      y="Amount", 
                      color="Country Name", 
                      hover_name="Country Name",
                      title="Top countries with highest receipts")

#barplotting of the top countries with highest receipts
plotly.offline.plot(receipts_bar, filename="D://virat//receipts_bar")    
msg(16)
#import receipts count percentage of export data set
percent_export = pd.read_excel("D://virat//travel_data.xls", sheet_name="receipts (% of total exports)", header=3, index_col=0)
msg(17)
#use "data_selection" function to select receipts export data
cname='Country Name'
percent_export_clean = data_selection(percent_export,cname)
msg(18)
#find the top countries with the attract tourists most
top_country_export = percent_export_clean.sort_values("2017", ascending=False).head(10)
top_export_country_list = list(top_country_export.index)
msg(19)
#use "reshape_data" function to reshape the percent_export_clean data frame
percent_export_stack = reshape_data(percent_export_clean)
msg(20)
#select the top countries' data 
top_country_export = percent_export_stack.loc[percent_export_stack['Country Name'].isin(top_export_country_list)]
msg(21)

#make the polar bar plot for the top countries tourism are export oriented
export_polar = px.bar_polar(top_country_export,
                            #radius column
                            r="Amount",
                            #angle column
                            theta="Country Name",
                            color="Country Name", 
                            #slider animation column
                            animation_frame="Year", 
                            title="Top countries ranked by tourism share of exports")

plotly.offline.plot(export_polar, filename="D://virat//export_polar")
msg(22)
# GDP and tourists number correlation

gdp = pd.read_excel("d://virat//travel_data.xls", sheet_name="GDP", header=3, index_col=0)
msg(23)
#select relevant years data
gdp = gdp.loc[:,"2007":"2017"]
#reshape the data frame
gdp_data = pd.DataFrame(gdp.stack()).reset_index()
#rename the column name
gdp_data = gdp_data.rename(columns = {"level_1":"Year", 0:"GDP"})
msg(24)

#merge the inbound tourists data and gdp data by Country name and year
gdp_inbound = inbound_tourists_stack.merge(gdp_data, left_on=("Country Name_x","Year"), right_on=("Country Name","Year"))
msg(25)
#make the scatter plot check the relation between GDP and inbound tourists number
gdp_inbound_plot = px.scatter(gdp_inbound, 
                              x="Amount", 
                              y="GDP",
                              #set the color of the plot
                              color_discrete_sequence = px.colors.qualitative.Vivid,
                              hover_name="Country Name",
                              #use log data to plot
                              log_x=True, 
                              log_y=True, 
                              labels="Amount(number of people)",
                              title="Correlation between GDP and number of inbound tourists")
plotly.offline.plot(gdp_inbound_plot, filename="D://virat//gdp_inbound_plot")
msg(26)

# world tourists travel outbound

#import tourists outbound data set
outbound_tourists = pd.read_excel("D://virat//travel_data.xls", sheet_name="number_of_departure", header=3, index_col=0)
msg(27)
#use "data_selection" function to select inbound tourists data
cname='Country Name'
outbound_tourists_clean = data_selection(outbound_tourists,cname)
msg(28)
#use "reshape_data" function to reshape the outbound_tourists_clean data frame
outbound_tourists_stack = reshape_data(outbound_tourists_clean)
msg(29)
#make the map plot of world outbound tourist
outbound_map = px.scatter_geo(outbound_tourists_stack, 
                              locations="Country Code", 
                              color="Amount", 
                              hover_name="Country Name", 
                              size="Amount",
                              #set animation column
                              animation_frame="Year",
                              color_continuous_scale=px.colors.sequential.Aggrnyl,
                              projection="natural earth")
#outbound map of tourists
plotly.offline.plot(outbound_map, filename="D://virat//outbound_map")
msg(30)

#find the top countries with the attract tourists most
top_country_outbound = outbound_tourists_clean.sort_values("2017", ascending=False).head(10)
top_outbound_country_list = list(top_country_outbound.index)
msg(31)
top_outbound_data = outbound_tourists_stack.loc[outbound_tourists_stack['Country Name'].isin(top_outbound_country_list)]
msg(32)
#make the line plot for top outbound countries
outbound_top = px.line(top_outbound_data,
                       #x axis column
                       x="Year",
                       #y axis column
                       y="Amount", 
                       color="Country Name", 
                       line_group="Country Name", 
                       hover_name="Country Name",
                       #line type
                       line_shape="linear",
                       title="Top countries where people like to travel")

plotly.offline.plot(outbound_top, filename="D://virat//outbound_top")
msg(33)

# Relationship between population and the number of outbound tourists

#import the population data set
population = pd.read_excel("D://virat//travel_data.xls", sheet_name="population", header=3, index_col=0)
msg(34)
#use "data_selection" function to select population data set
cname='Country Name'
population_clean = data_selection(population,cname)
msg(35)
#def a function concate the population data with outbound tourists data
def population_outbound(year):
    df1 = population_clean.loc[population_clean.index.isin(top_outbound_country_list)].loc[:,year]
    df2 = outbound_tourists_clean.loc[outbound_tourists_clean.index.isin(top_outbound_country_list)].loc[:,year]
    df = pd.concat([df1, df2], axis=1)
    return df

msg(36)

#make the line-bar plot
#make the scatter plot
trace1=go.Scatter(
    x=population_outbound("2017").index,
    y=population_outbound("2017").iloc[:,0],
    name="population")
#make the bar plot
trace2=go.Bar(
    x=population_outbound("2017").index,
    y=population_outbound("2017").iloc[:,1],
    name="tourists",
    yaxis="y2",
    #transparent level
    opacity=0.6,
    #bar wide
    width=[0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5])
data=[trace1,trace2]
layout=go.Layout(
    title="Outbound tourists number vs country's population",
    yaxis=dict(title="population"),
    yaxis2=dict(title="number of people", 
                titlefont=dict(color="rgb(148, 103, 189)"),
                tickfont=dict(color="rgb(148, 103, 189)"),
                overlaying="y",
                side="right"))

outbound_population_compare=go.Figure(data=data, layout=layout)
plotly.offline.plot(outbound_population_compare, filename="D://virat//outbound_population_compare")
msg(37)
#merge the outbound tourists data and gdp data
gdp_outbound = outbound_tourists_stack.merge(gdp_data, left_on=("Country Name","Year"), right_on=("Country Name","Year"))
msg(38)
#make the scatter plot to check the relationship between tourists number and GDP
gdp_outbound_plot = px.scatter(gdp_outbound, 
                               x="Amount", 
                               y="GDP",  
                               hover_name="Country Name",
                               #use log data to make the plot
                               log_x=True, 
                               log_y=True,
                               title="Correlation between GDP and outbound tourists")

plotly.offline.plot(gdp_outbound_plot, filename="D://virat//gdp_outbound_plot")
msg(39)

#import expenditure data set
expenditure = pd.read_excel("D://virat//travel_data.xls", sheet_name="expenditure for travel item", header=3, index_col=0)
cname='Country Name'
expenditure_clean = data_selection(expenditure,cname)
msg(40)
#calculate the per capita data 
expenditure_p = expenditure_clean.iloc[:,1:12]/outbound_tourists_clean.iloc[:,1:12]
#drop nan, inf rows
expenditure_p = expenditure_p[~expenditure_p.isin([np.nan, np.inf, -np.inf]).any(1)]
msg(41)
#select the top countries' data 
top_expenditure_p_data = expenditure_p.loc[expenditure_p.index.isin(top_outbound_country_list)].sort_values("2017", ascending=False)
msg(42)
#reshape the top_expenditure_p_data data frame
top_expenditure_p_stack = top_expenditure_p_data.stack().reset_index()
top_expenditure_p_stack = top_expenditure_p_stack.rename(columns = {"level_1":"Year",0:"Per capita expenditure"})
msg(43)
#make the bar plot of the top countries' people with highest spending in the travel
expenditure_bar = px.bar(top_expenditure_p_stack, 
                         x="Year", 
                         y="Per capita expenditure", 
                         color="Country Name", 
                         hover_name="Country Name",
                         title="Top countries per capita expenditure in travel(exclude international transportation)")

plotly.offline.plot(expenditure_bar, filename="D://virat//expenditure_bar")
msg(44)
