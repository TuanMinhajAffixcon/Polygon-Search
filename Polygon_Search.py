import  pandas as pd
import streamlit as st
from shapely.geometry import Point, Polygon
from collections import Counter
import folium
from streamlit_folium import folium_static


def download_csv(df, filename):
    csv = df.to_csv(index=False)
    st.download_button(
        label="Download CSV",
        data=csv,
        file_name=filename,
        mime='text/csv'
    )
    
new_coordinates = [
(-37.875064933155514, 145.03708825418542),
(-37.874998743191306, 145.03655848187904),
(-37.8755119779044, 145.03646120385565),
(-37.87544854897898, 145.03583302336966),
(-37.876234908041546, 145.03568424051093),
(-37.876315788419774, 145.0362646956954),
(-37.876427077693435, 145.0362324636629),
(-37.87642453677239, 145.03609872020147),
(-37.876762317651654, 145.0360307194947),
(-37.87689377196801, 145.03676204269914)]

formatted_locations = [f"{coord[0]}, {coord[1]}" for coord in new_coordinates]
formatted_locations_str = "\n".join(formatted_locations)
locations = st.text_area("Coordinates:", value=formatted_locations_str)
user_coordinates = [tuple(map(float, location.split(','))) for location in locations.split('\n') if location]

if user_coordinates:
    total_lat = sum(coord[0] for coord in user_coordinates)
    total_lon = sum(coord[1] for coord in user_coordinates)
    center_lat = total_lat / len(user_coordinates)
    center_lon = total_lon / len(user_coordinates)
    m = folium.Map(location=[center_lat, center_lon], zoom_start=12)
    if len(user_coordinates) >= 3:
        folium.Polygon(locations=user_coordinates, color='green', fill=True, fill_color='green', fill_opacity=0.4).add_to(m)


    folium_static(m)

uploaded_file = st.file_uploader("Choose a file",type=['csv'])

def main():
    df_movement=pd.read_csv(uploaded_file)
    st.write('All URN counts uploaded: ',len(df_movement.URN))
    
    polygon_shapely = Polygon(user_coordinates)

    maid_counts = Counter()
    matching_records=[]
    for index, row in df_movement.iterrows():
        lat = row['latitude']
        lon = row['longitude']
        # datetimestamp=row['new_timestamp']
        
        point = Point(lat, lon)
        if point.within(polygon_shapely):
            maid = row['URN']
            maid_counts[maid] += 1
            matching_records.append([maid,lat,lon])

    filtered_df=pd.DataFrame(matching_records,columns=["URN","latitude","longitude"])

    st.write(filtered_df.head())
    st.write('unique URN count',len(filtered_df.URN.unique()))
    
    download_csv(filtered_df[['URN']], filename='witin polygon '+file_name)

if __name__ == "__main__":
    if uploaded_file is not None:
        file_name = uploaded_file.name
        main()