################# Functions ############################
import requests
import os
import pandas as pd
import json

# OPen the data using a URL API Address and save it
response = requests.get(
    "https://opendata.arcgis.com/datasets/d1877e350fad45d192d233d2b2600156_6.geojson"
)

data = response.json()

justFeatures = data[
    'features']  # We only need the features section on the data
df = pd.json_normalize(justFeatures)

df = df.rename(
    columns={
        'properties.RecordID': 'RecordID',
        'properties.Offense': 'Offense',
        'properties.IncidentID': 'IncidentID',
        'properties.BlockNumber': 'BlockNumber',
        'properties.StreetName': 'StreetName',
        'properties.Agency': 'Agency',
        'properties.DateReported': 'DateRep',
        'properties.HourReported': 'HoursRep',
        'properties.ReportingOfficer': 'Officer'
    })

##################################################################
############### Discord Bot ######################################
##################################################################

import discord
import os
import random

client = discord.Client()
TOKEN = os.getenv(
    'DISCORD_TOKEN',
    'OTY2MzU2MTI1NjYwMzUyNTQy.YmAjRg.L3FfmQJtgcQ0cMO1i7WTTiabLAs')

GUILD = os.getenv('DISCORD_GUILD', 'DS3200')

@client.event
async def on_ready(): ## Log into Discord
    print('We have logged in as {0.user}.format(client)')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

  # Help and Welcome message to explain what happens
    if message.content.startswith('Help') or message.content.startswith('Hello'):
        await message.channel.send(
            'Hello! I am a bit that tells you about crime data in Charlottesville! You can ask me for 3 things. They are... ')
        await message.channel.send('Record - to get a random crime record from the area')
        await message.channel.send('Street - to see the streets with the most recorded crime')
        await message.channel.send('Offense - to see the most recorded offenses')

  # Record Message which finds a random record to show
    if message.content.startswith('Record'):
        await message.channel.send(
            df[df['RecordID'] == random.randrange(1, 10, 1)].iloc[:, 3:8])

  # Street message which shows which streets are most dangerous
    if message.content.startswith('Street'):
        await message.channel.send(
            df['StreetName'].value_counts().head())

  # Offense Message which shows the most popular Offenses
    if message.content.startswith('Offense'):
        await message.channel.send(
            df['Offense'].value_counts().head())

  # If you type anything else 
    else:
      await message.channel.send(
            'Please type Record, Street or Offense to see information about crime')
      
client.run(TOKEN)
