import pandas as pd
import os

def append_to_csv(file_path, data):
	df_new = pd.DataFrame([data])
	if os.path.isfile(file_path):
		df_existing = pd.read_csv(file_path)
		df_combined = pd.concat([df_existing, df_new], ignore_index=True)
	else:
		df_combined = df_new
	df_combined.to_csv(file_path, index=False)