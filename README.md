# Climate Change Chatbot Analytics

Includes all software necessary for the analysis of the chatbot.

## Code Entry Points

- All code to create an excel-file to analyse from a postgres Tracker Store is at the location [src/climate_change_bot/analytics/import](src/climate_change_bot/analytics/import)
- The script to start the plotly dash application [src/climate_change_bot/analytics/dashboard.py](src/climate_change_bot/analytics/dashboard.py)
- Global Storage of the data as pandas dataframe [src/climate_change_bot/analytics/store.py](src/climate_change_bot/analytics/store.py)
- All pages of the application are defined in [src/climate_change_bot/analytics/pages](src/climate_change_bot/analytics/pages)
- All components for the pages of the application are defined in [src/climate_change_bot/analytics/components](src/climate_change_bot/analytics/components)

## Running the Code

Only described for linux. 

- Install first python 3.10.
- Navigate in console to analytics directory 
- Create a virtual environment and install the packages in the requirements.txt.
- Run the following code if you want to import the data from a postgres tracker store. Be aware that all model_id must be listed in model_versions.csv. Skip this step if you use an already created excel-file.
```bash 
export DB_HOST=url_track_store
export DB_PORT=port_of_the_tracker_store
export DB_USER=user_tracker_store
export DB_PASSWORD=password_of_post
export DB_NAME=database_name
export OUTPUT_FILE_NAME=conversations.xlsx

cd src/climate_change_bot/analytics/import/

python3 import_events.py
```
- Navigate in console to analytics directory if you executed previous step
- Run the following code to start the analytic tool on http://127.0.0.1:8050/
. Set the location to the excel-file to analyse.
```bash 
export PYTHONPATH="${PYTHONPATH}:your_path/analytics/src/climate_change_bot"
export FILE_NAME=../data/conversations_prod.xlsx # Change if your file is at another location

cd src/
python3 climate_change_bot/analytics/dashboard.py
```