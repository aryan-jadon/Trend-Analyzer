from datetime import datetime, timedelta
import pandas as pd
from ModuleFiles.request import TrendReq
from tqdm import tqdm
import plotly.express as px
import plotly.graph_objects as go


def find_US_Trend(keywords_to_search):
    country = "US"
    pytrend = TrendReq()
    Keyword = keywords_to_search
    kw_list = [keywords_to_search] 
    pytrend.build_payload(kw_list, cat=0, geo=country,timeframe = "now 7-d" , gprop='')
    City  = pytrend.interest_by_region(inc_low_vol=True, inc_geo_code=True)
    City_Names = City.index
    City["City_Names"] = City_Names
    All_City = list(City["geoCode"])
    country = All_City[0]
    pytrend = TrendReq()
    Keyword = keywords_to_search
    kw_list = [keywords_to_search] 
    pytrend.build_payload(kw_list, cat=0, geo=country,timeframe = "now 7-d" , gprop='')
    City  = pytrend.interest_by_region(resolution='CITY',inc_low_vol=True, inc_geo_code=False)
    City_Names = City.index
    City["City_Names"] = City_Names
    Country_Trend_Frame = City
    
    for city in All_City[1:]:
        country = city
        pytrend = TrendReq()
        Keyword = keywords_to_search
        kw_list = [keywords_to_search] 
        pytrend.build_payload(kw_list, cat=0, geo=country,timeframe = "now 7-d" , gprop='')
        City  = pytrend.interest_by_region(resolution='CITY',inc_low_vol=True, inc_geo_code=False)
        City_Names = City.index
        City["City_Names"] = City_Names
        Country_Trend_Frame = pd.concat([Country_Trend_Frame, City])

    Country_Trend_Frame.drop_duplicates(subset = Country_Trend_Frame.columns ,keep ="first", inplace = True)
    US_Codes = pd.read_csv("Module-Data/US-Codes.csv")

    Results = []

    for city in Country_Trend_Frame["City_Names"]:
        try:
            Frame = Country_Trend_Frame[Country_Trend_Frame["City_Names"]==city]
            Frame.sort_values(keywords_to_search, axis = 0, ascending = False, inplace = True) 
            keywordValue = Frame.iloc[0][keywords_to_search].item()
            Data = US_Codes[US_Codes["City-Name"]== city]
            latitude = Data["Latitude"].item()
            longitude = Data["Longitude"].item()
            Results.append((
                city,
                keywordValue,
                latitude,
                longitude
            ))
        except:
            print(city)

    Results = pd.DataFrame(Results,columns=["City","Score","lat","lon"])
    fig = px.scatter_mapbox(Results, 
                            lat="lat",
                            lon="lon",
                            hover_name="City",
                            hover_data=["Score"],
                            size="Score",
                            zoom=3, 
                            height=300,
                            size_max=10,
                            color_continuous_scale=px.colors.cyclical.IceFire
                            )

    fig.update_layout(mapbox_style="carto-darkmatter")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    fig.show()
    fileName = "Results/"+str(keywords_to_search)+"-1-"+".jpeg"
    print(fileName)
    fig.write_image(fileName)
    
    fig.update_layout(mapbox_style="carto-positron")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    fig.show()
    fileName = "Results/"+str(keywords_to_search)+"-2-"+".jpeg"
    print(fileName)
    fig.write_image(fileName)
    
    
find_US_Trend("australia fire")
        