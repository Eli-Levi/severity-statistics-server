import pandas as pd
import os
from SshToServer import SshToServer


def append_to_csv(file_path, data):
	df_new = pd.DataFrame([data])
	if os.path.isfile(file_path):
		df_existing = pd.read_csv(file_path)
		df_combined = pd.concat([df_existing, df_new], ignore_index=True)
	else:
		df_combined = df_new
	df_combined.to_csv(file_path, index=False)


def main():
	user_pem = input("Write the absolute path to your pem file: ")
	my_ssh = SshToServer(user_pem, "13.51.195.198", "ubuntu")
	my_ssh.connect()
	response = my_ssh.runRemoteCommand("python3 server_side.py")



if __name__ == "__main__":
	main()