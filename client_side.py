import pandas as pd
import os
from SshToServer import SshToServer
import json

def append_to_csv(file_path, data):
	headers = []
	for header in data:
		headers.append(header)
	json_data = {key: data.get(key, 0) for key in headers}
	df_new = pd.DataFrame([json_data])
	df_new = df_new[headers]
	if os.path.isfile(file_path):
		df_existing = pd.read_csv(file_path)
		df_combined = pd.concat([df_existing, df_new], ignore_index=True)
	else:
		df_combined = df_new
	df_combined.to_csv(file_path, index=False)


def main():
	user_pem = input("Write the absolute path to your pem file: ")
	server_ip = input("Please type in the server's ip: ")
	host_name = input("Please type in the user name: ")
	my_ssh = SshToServer(user_pem, server_ip, host_name)
	my_ssh.connect()
	stdout, stderr = my_ssh.runRemoteCommand("python3 server_side.py")
	if stdout:
		append_to_csv(os.path.join(os.getcwd(), "statistics.csv"), json.loads(stdout))
	else:
		print(stderr)



if __name__ == "__main__":
	main()