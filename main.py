import discord   
import requests   
import os         
import json

client = discord.Client(); # Initialize client

### Command Methods ###

async def getWeatherViaZip(zipcode, countrycode, units):

  if units.lower() != 'imperial' and units.lower() != 'metric':
    return 'Invalid unit of measurement'

  response = requests.get('http://api.openweathermap.org/data/2.5/weather?zip=' + zipcode + ',' + countrycode + '&appid=' +os.environ['API_KEY'] + '&units=' + units)
  data = response.json()

  if data['cod'] == '404':
    return 'Incorrect information. Use $help for more info.'

  weather = data['weather'][0]['main']
  temp = data['main']['temp']
  feelslike = data['main']['feels_like']
  humid = data['main']['humidity']
  min = data['main']['temp_min']
  max = data['main']['temp_max']
  location = data['name']
  unit = ''
  if units == 'imperial':
    unit = 'f'
  else:
    unit = 'c'

  return str(f"Weather: {weather}\nTemperature: {temp}°{unit}\nFeels like: {feelslike}\nHumidity: {humid}\nRange: {min}°{unit} - {max}°{unit}\nLocation: {location}")

@client.event
async def on_ready(): # When bot is turned on:
  print(f'Bot client started\nLogged in as {client.user}')

@client.event
async def on_message(message): # When a message is sent:

  if message.author == client.user: # If sender is the bot itself
    return
  
  # Returns message showing that the bot is currently working
  if message.content.startswith('$ping'):
    await message.channel.send('Discord Weather Bot\nCreated by Michael Warmbier\nSource: https://replit.com/@Kirbout/Discord-Weather-Bot')

  # Returns message showing instructions on how to use each command
  if message.content.startswith('$help'):
      await message.channel.send('**$help**\nInstructions on each command\n\n**$ping**\nShows bot information and status\n\n**$getweather <zipcode> <countrycode> <units>** *OR* **$getweather <zipcode> <countrycode>**\nGet current weather data. Default units are metric.\nList of country codes: https://en.wikipedia.org/wiki/List_of_ISO_3166_country_codes')

  # Retrieves weather based on location
  if message.content.startswith('$getweather'):
    command = (message.content).split(' ')
    if len(command) == 4:
      result = await getWeatherViaZip(command[1], command[2], command[3])
      await message.channel.send(result)
    elif len(command) == 3:
      result = await getWeatherViaZip(command[1], command[2], 'metric')
      await message.channel.send(result)
    else:
      await message.channel.send('Invalid number of arguments')
      return
    

client.run(os.environ['TOKEN']) # Start bot

