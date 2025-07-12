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

def prepJsonFromFiles():
    severities_json = {"timestamp": time.time()}
    with open(log_path, 'r') as severities_log:
        content = severities_log.readline()
        severity_occurance = { "WARN": 0, "INFO": 0, "ERROR": 0}
        while content:
            for key in severity_occurance.keys():
                returned_value = content.find(key)
                if returned_value > 0:
                    severity_occurance[key] += 1
            content = severities_log.readline()      
    severities_json.update(severity_occurance)
    return severities_json


def main():
    try:
        resulting_json = prepJsonFromFiles() 
        print(json.dumps(resulting_json))
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        # exit()


if __name__ == "__main__":
    main()