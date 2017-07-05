import sys
import pandas as pd
import numpy as np
import json
from sklearn.cluster import MeanShift, estimate_bandwidth

def get_support_and_resistance(df, period):
	# group by day and drop NA values (usually weekends)
	grouped_data = df.dropna()

	ticks_data = grouped_data['RateBid'].resample(period)

	# use 'ask'
	sell_data = pd.DataFrame(ticks_data.values)
	sell_data.dropna(inplace=True)
	sell_data = sell_data.as_matrix();

	
	# calculate bandwidth (expirement with quantile and samples)
	bandwidth = estimate_bandwidth(sell_data, quantile=0.1, n_samples=100)
	ms = MeanShift(bandwidth=bandwidth, bin_seeding=True)

	# fit the data
	ms.fit(sell_data)
	
	ml_results = []
	for k in range(len(np.unique(ms.labels_))):
		my_members = ms.labels_ == k
		values = sell_data[my_members, 0]    

		# find the edges
		ml_results.append(min(values))
		ml_results.append(max(values))

	# export the data for the visualizations
	ticks_data.to_json('ticks.json', date_format='iso', orient='index')

	# export ml support resisistance
	with open('ml_results.json', 'w') as f:
		f.write(json.dumps(ml_results))
		