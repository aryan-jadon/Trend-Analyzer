from datetime import datetime, timedelta
import pandas as pd
from ModuleFiles.request import TrendReq
from tqdm import tqdm
import plotly.express as px
import plotly.graph_objects as go


def plot_trend(Trend_keyword):
    keywords_to_search = Trend_keyword
    pytrend = TrendReq()
    Keyword = keywords_to_search
    kw_list = [keywords_to_search] 
    pytrend.build_payload(kw_list, cat=0,timeframe = "now 7-d" , gprop='')
    City  = pytrend.interest_by_region(resolution='DMA',inc_low_vol=True, inc_geo_code=True)
    City_Names = City.index
    City["City_Names"] = City_Names
    Records = pd.read_csv("Module-Data/Metro-Cities.csv")
    Results = []

    for city in City["City_Names"]:
        try:

            Frame = City[City["City_Names"]==city]
            Frame.sort_values(keywords_to_search, axis = 0, ascending = False, inplace = True) 
            keywordValue = Frame.iloc[0][keywords_to_search].item()

            Data = Records[Records["City"]== city]
            latitude = Data["lat"].item()
            longitude = Data["lon"].item()

            Results.append((
                city,
                keywordValue,
                latitude,
                longitude
            ))
        except:
            #print(city)
            pass
            
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
    fileName = "Results/"+str(Trend_keyword)+"-1-"+".jpeg"
    print(fileName)
    fig.write_image(fileName)
    
    fig.update_layout(mapbox_style="carto-positron")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    fig.show()
    fileName = "Results/"+str(Trend_keyword)+"-2-"+".jpeg"
    print(fileName)
    fig.write_image(fileName)
    
    
    
plot_trend("australia fire")
