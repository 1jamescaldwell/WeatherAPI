# WeatherAPI
Personal project 11/10/23

I wrote this script to send a notification to my phone every day that the temperature will reach below freezing overnight. Backstory: we had a pipe burst during the winter of 2022, so I want to make sure our faucet is dripping and cabinets are open every night it will be below freezing. This script is set to run automatically every day at 4pm EST. The script calls OpenWeatherMap's API to get the weather forecast in 3hr intervals for the next day. The code finds the lowest temperature from the next day and sends a notification to my phone using the Pushover app if the temperature is below freezing.

To run this code, you will have to setup OpenWeatherMap and Pushover accounts and input your user keys in the blocks of code that say "enter your key here."

Created using nb.anaconda.cloud/jupyterhub.
