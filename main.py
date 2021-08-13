import discord   
import requests   
import os         
import json
from datetime import datetime

client = discord.Client(); # Initialize client

# ANSI colors
class t_colors:
    NAME = '\033[94m'
    INFO = '\033[92m'
    ERROR = '\033[93m'
    NOCOLOR = '\033[0m'

### Command Methods ###

async def getWeatherViaZip(zipcode, countrycode, units):

  # If units of measurement is invalid, return with error
  if units.lower() != 'imperial' and units.lower() != 'metric':
    print(t_colors.ERROR + 'Error: Invalid units.' + t_colors.NOCOLOR)
    return 'Invalid unit of measurement'

  # Request information and store response as json data
  response = requests.get('http://api.openweathermap.org/data/2.5/weather?zip=' + zipcode + ',' + countrycode + '&appid=' +os.environ['API_KEY'] + '&units=' + units)
  data = response.json()

  # If data.cod is 404, something went wrong
  if data['cod'] == '404':
    print(t_colors.ERROR + 'Error: Incorrect information.' + t_colors.NOCOLOR)
    return 'Incorrect information. Use $help for more info.'
 
  # Store data
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

  # Return results
  return str(f"Weather: {weather}\nTemperature: {temp}°{unit}\nFeels like: {feelslike}°{unit}\nHumidity: {humid}%\nRange: {min}°{unit} - {max}°{unit}\nLocation: {location}")

@client.event
async def on_ready(): # When bot is turned on:
  print(f'Bot client started\nLogged in as {client.user}\n')

@client.event
async def on_message(message): # When a message is sent:

  server = message.guild
  user = message.author
  today = datetime.now()
  dateAndTime = today.strftime("%d/%m/%Y %H:%M")

  if message.author == client.user: # If sender is the bot itself
    return

  if message.content.startswith('$'): # Debugging log
      print('Message from: ' + t_colors.NAME + f'"{server}"' + t_colors.NOCOLOR + '\n' + t_colors.NAME + f'{user}:' + t_colors.NOCOLOR + f'"{message.content}"\n' + t_colors.INFO + f'{dateAndTime}' + t_colors.NOCOLOR)
  
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
      print(t_colors.ERROR + 'Error: Invalid number of arguments.' + t_colors.NOCOLOR)
      await message.channel.send('Invalid number of arguments')
      return
    

client.run(os.environ['TOKEN']) # Start bot

