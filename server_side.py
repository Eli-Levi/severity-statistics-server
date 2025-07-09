import json
import os
import subprocess
import sys
import time

log_path = "/var/log/syslog"

def run_local_command(command):
    try:
        # Run the command
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return result.stdout, result.stderr

    except subprocess.CalledProcessError as e:
        print(f"Command '{command}' returned non-zero exit status {e.returncode}")
        print(f"Error output: {e.stderr}")

def prepJsonFromFiles(files_list: list):
    severities_json = {}
    severities_json["timestamp"] = time.time()
    for file in files_list:
        severity_type = file.strip(".txt").upper()
        absulute_file_path = os.path.join(os.getcwd(), file)
        severity_counter = 0
        with open(absulute_file_path, 'r') as severity_file: 
            content = severity_file.readlines()
            for line in content:  
                severity_counter += 1
        severities_json[severity_type] = severity_counter
    return severities_json

def createSeverityLogs():
    files_list = []
    for severity in ["WARN", "ERROR", "INFO"]:
        file_name = severity.lower() + ".txt"
        files_list.append(file_name)
        run_local_command(f'grep {severity} {log_path} > {file_name}')
    return files_list


def main():
    try:
        files = createSeverityLogs()
        resulting_json = prepJsonFromFiles(files) 
        run_local_command("rm -f error.txt info.txt warn.txt")
        print(json.dumps(resulting_json))
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        # exit()


if __name__ == "__main__":
    main()