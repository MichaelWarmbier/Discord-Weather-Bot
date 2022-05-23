import discord   
import requests   
import os
import json
import hashlib
from datetime import datetime

client = discord.Client() # Initialize client 
with open('server.json', 'r') as f:
    server = json.loads(f.read())

# ANSI colors
class t_colors:
    NAME = '\033[94m'
    INFO = '\033[92m'
    ERROR = '\033[93m'
    NOCOLOR = '\033[0m'

### Utility Methods ###

async def updateServerInfo(what, title, pref, data):
  title = await hash(str(title))
  global server
  with open('server.json', 'r') as f:
    server = json.loads(f.read())
    if title in server[what]:
      server[what][title][pref] = data
    else:
      newUser = {
        "privacy": "public",
        "zipcode": 0,
        "country": "us",
        "units": "metric"
      }
      server[what][title] = newUser
      server[what][title][pref] = data
  with open('server.json', 'w') as f:
    json.dump(server, f, indent=4)
  print('Updated preferences successfully.')

async def hash(str):
  return (hashlib.md5(str.encode()).hexdigest());
    
### Command Methods ###

async def getWeatherViaZip(zipcode, countrycode, units, privacy):

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
  if privacy == 'public': location = data['name']
  else: location = '[REDACTED]'
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

  guild = message.guild
  user = message.author
  today = datetime.now()
  dateAndTime = today.strftime("%m/%d/%Y %H:%M")

  if message.author == client.user: # If sender is the bot itself
    return

  if message.content.startswith('$'): # Debugging log
      print('Message from: ' + t_colors.NAME + f'"{guild}"' + t_colors.NOCOLOR + '\n' + t_colors.NAME + f'{user}:' + t_colors.NOCOLOR + f'"{message.content}"\n' + t_colors.INFO + f'{dateAndTime}' + t_colors.NOCOLOR)
  
  # Returns message showing that the bot is currently working
  if message.content.startswith('$ping'):
    await message.channel.send('Discord Weather Bot\nCreated by Michael Warmbier\nSource: https://replit.com/@Kirbout/Discord-Weather-Bot')

  # Returns message showing instructions on how to use each command
  if message.content.startswith('$help'):
      await message.channel.send('```$help```\nInstructions on each command\n\n```$ping```\nShows bot information and status\n\n```$updatePrefs```\nAllows you to set specific preferences for easier use\n\nPreferences: *privacy, zipcode, country, units*\nPrivacy options: *public, private*\nUnit options: *imperial, metric*\n\nDM me to update your settings in private!\n\n```$weather <zipcode> <countrycode> <units>``` \nOR\n ```$weather <zipcode> <countrycode>``` \nOR\n ```$weather // only works with set preferences```\n\nGet current weather data. Default units are metric.\nList of country codes: https://www.iso.org/obp/ui/#search')

  # Retrieves weather based on location
  if message.content.startswith('$weather'):
    
    command = (message.content).split(' ')
    if len(command) == 4:
      result = await getWeatherViaZip(command[1], command[2], command[3], 'public')
      await message.channel.send(result)
    elif len(command) == 3:
      result = await getWeatherViaZip(command[1], command[2], 'metric', 'public')
      await message.channel.send(result)
    elif len(command) == 1:
      global server
      user = await hash(str(user))
      if user in server['userPref']:
        zipcode = server['userPref'][user]['zipcode']
        country = server['userPref'][user]['country']
        privacy = server['userPref'][user]['privacy']
        units = server['userPref'][user]['units']

      result = await getWeatherViaZip(zipcode, country, units, privacy)
      await message.channel.send(result)
      return
    else:
      print(t_colors.ERROR + 'Error: Invalid number of arguments.' + t_colors.NOCOLOR)
      await message.channel.send('Invalid number of arguments')
      return

  if message.content.startswith('$updatePrefs'):
    command = (message.content).split(' ')
    if len(command) == 3:
      if ((str(command[2]) == 'private' or str(command[2]) == 'public') and str(command[1]) == 'privacy') or (str(command[1]) == 'zipcode') or (str(command[1]) == 'country') or (str(command[1]) == 'units' and (str(command[2]) == 'metric' or str(command[2]) == 'imperial')):
        await updateServerInfo('userPref', user, command[1], command[2])
        await message.channel.send('Updated preferences successfully')
      else:
        print(t_colors.ERROR + 'Error: Invalid argument.' + t_colors.NOCOLOR)
        await message.channel.send('Invalid argument')
    else:
      print(t_colors.ERROR + 'Error: Invalid number of arguments.' + t_colors.NOCOLOR)
      await message.channel.send('Invalid number of arguments')
      return
        
      
    

client.run(os.environ['TOKEN']) # Start bot
 