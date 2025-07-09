import json
import os
import pandas as pd
import subprocess


log_path = "/var/log/syslog"
severities_json = {"WARN": 0, "INFO": 0, "ERROR": 0}
files_list =["warn.txt", "info.txt", "error.txt"]

def run_local_command(command):
    try:
        # Run the command
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return result.stdout, result.stderr

    except subprocess.CalledProcessError as e:
        print(f"Command '{command}' returned non-zero exit status {e.returncode}")
        print(f"Error output: {e.stderr}")

def prepJsonFromFiles():
    for file in files_list:
        severity_type = file.strip(".txt").upper()
        absulute_file_path = os.getcwd() +"\\"+ file
        severity_counter = 0
        with open(absulute_file_path, 'r') as severity_file: 
            content = severity_file.readlines()
            for line in content:  
                severity_counter += 1
        severities_json[severity_type] = severity_counter
    return severities_json

def createSeverityLogs():
    for severity in severities_json.keys():
        file_name = severity.lower() + ".txt"
        files_list.append(file_name)
        run_local_command(f'grep {severity} {log_path} > {file_name}')


def main():
    res = prepJsonFromFiles()



if __name__ == "__main__":
    main()