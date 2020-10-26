# ScanNetworkEnvironment
Repo to share scripts that help scan Azure network environments and identify all underlying resources

## Network Scan Python Script
1. Install the Python 3 virtual environment - see [here](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments) for more information
2. Start the python3 virtual environment 
   ```
   python3 -m venv .venv
   . ./.venv/bin/activate
   ```
3. Install the required libraries - ```pip3 install -r requirements.txt```
4. Modify env variable and enter the information for each environment variable and then source it:
   ```. ./env```
5. Run the script: ```./net_scan.py```
