import streamlit as st
import pandas as pd
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium
import warnings
import os


warnings.filterwarnings('ignore')
st.set_page_config(layout="wide")
st.title("Flood Impact Visualization in Kerala (2018)")


@st.cache_data
def load_data():
	base = os.path.join(os.path.dirname(__file__), '..')
	base = os.path.abspath(base)
	districts_path = os.path.join(base, 'datasets', 'district_wise_details.csv')
	warnings_path = os.path.join(base, 'datasets', 'warnings_actual_predicted.csv')
	df_dist = pd.read_csv(districts_path)
	df_warn = pd.read_csv(warnings_path)
	df_warn['date'] = pd.to_datetime(df_warn['date'], format='%m/%d/%Y')
	return df_dist, df_warn


# Approximate district centroids for Kerala (lat, lon)
DISTRICT_COORDS = {
	'Thiruvananthapuram': (8.5241, 76.9366),
	'Kollam': (8.8932, 76.6141),
	'Pathanamthitta': (9.2643, 76.7878),
	'Alappuzha': (9.4981, 76.3388),
	'Kottayam': (9.5916, 76.5226),
	'Idukki': (9.8786, 77.1596),
	'Ernakulam': (9.9816, 76.2999),
	'Thrissur': (10.5276, 76.2144),
	'Palakkad': (10.7867, 76.6548),
	'Malappuram': (11.0738, 76.0800),
	'Kozhikode': (11.2588, 75.7804),
	'Wayanad': (11.6850, 76.1380),
	'Kannur': (11.8745, 75.3704),
	'Kasaragode': (12.5000, 74.9900)
}


def make_map(df_dist, selected_districts, show_heatmap=True):
	center = [10.5, 76.3]
	m = folium.Map(location=center, zoom_start=7, tiles='CartoDB positron')

	heat_data = []
	for _, row in df_dist.iterrows():
		d = row['district']
		coords = DISTRICT_COORDS.get(d)
		if not coords:
			continue
		lat, lon = coords
		if (selected_districts and d not in selected_districts):
			continue

		popup = (
			f"<b>{d}</b><br>Fatalities: {row.get('fatalities', '')}<br>"
			f"Camps: {row.get('no_of_camps', '')}<br>Damaged houses: {row.get('full_damaged_houses', '')}<br>"
			f"Rainfall (mm): {row.get('actual_rainfall_in_mm', '')}"
		)

		folium.CircleMarker(
			location=(lat, lon),
			radius=max(6, int(min(40, (row.get('full_damaged_houses', 0) or 0) / 50 + 6))),
			color='crimson',
			fill=True,
			fill_opacity=0.7,
			popup=folium.Popup(popup, max_width=300)
		).add_to(m)

		heat_data.append([lat, lon, float(row.get('actual_rainfall_in_mm') or 0)])

	if show_heatmap and heat_data:
		HeatMap(heat_data, radius=25, max_zoom=9).add_to(m)

	return m


def main():
	df_dist, df_warn = load_data()

	st.sidebar.header('Filters')
	all_districts = sorted(df_dist['district'].unique())
	selected = st.sidebar.multiselect('Select district(s)', options=all_districts, default=all_districts)

	dates = sorted(df_warn['date'].dt.date.unique())
	sel_date = st.sidebar.selectbox('Select date (warnings)', options=dates, index=len(dates)-1)

	show_heat = st.sidebar.checkbox('Show rainfall heatmap', value=True)

	# Summary metrics
	filtered_dist = df_dist[df_dist['district'].isin(selected)]
	col1, col2, col3 = st.columns(3)
	col1.metric('Total Fatalities', int(filtered_dist['fatalities'].sum()))
	col2.metric('Total Camps', int(filtered_dist['no_of_camps'].sum()))
	col3.metric('Damaged Houses', int(filtered_dist['full_damaged_houses'].sum()))

	# Show map
	m = make_map(df_dist, selected, show_heatmap=show_heat)
	st.subheader('Flood map')
	st.caption('Circle size ~ damaged houses; heatmap weight ~ rainfall')
	st_data = st_folium(m, width=1200, height=600)

	# Warnings table for the selected date and districts
	sel_date = pd.to_datetime(sel_date)
	warn_filtered = df_warn[df_warn['date'] == sel_date]
	warn_filtered = warn_filtered[warn_filtered['district'].isin(selected)]
	st.subheader(f'Warnings on {sel_date.date()}')
	if warn_filtered.empty:
		st.write('No warning records for selected date/districts.')
	else:
		st.dataframe(warn_filtered.reset_index(drop=True))


if __name__ == '__main__':
	main()

