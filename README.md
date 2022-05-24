
# Discord Weather Bot

Application created, documentation written, by Michael Warmbier.<br>
 Last Updated: 5/23/22

## Table of Contents

- [Discord Weather Bot](#discord-weather-bot)
  * [Information](#information)
    + [Description](#description)
    + [Adding to Your Server](#adding-to-your-server)
    + [How It Works](#how-it-works)
    + [Commands](#commands)
    + [[Libraries]](#libraries)
    + [[Classes]](#classes)
    + [[Filesystem]](#filesystem)
    + [[Methods]](#methods)
      - [<u>Utility Methods<u/>](#utility-methods)
      - [<u>Command Methods<u/>](#command-methods)
 

## Information

### Description

This document goes over the structure and logic of the [Discord Weather Bot](https://replit.com/@Kirbout/Discord-Weather-Bot) created by [Michael Warmbier](http://michaelwarmbier.com).

Information retrieved from the bot from the [openweatherapi](https://openweathermap.org/).

The Discord Weather Bot is a free application designed to run within Discord servers, receiving necessary information from users and returning their local weather.

Written originally in Markdown.

### Adding to Your Server

This bot can be invited to a server using [this link](https://discord.com/api/oauth2/authorize?client_id=863074810980073472&permissions=68608&scope=bot). The only permissions required are the ability to send and read messages.

### How It Works

As a bot-application, **Discord Weather Bot** is always running. It awaits messages from the servers that house it, specifically ones that contain its prefix (default '$'). Once a message is noticed, it is then logged on the CLI and the bot will perform actions accordingly.

### Commands

**$help**   <br>
&emsp;&emsp; Lists all commands and their description.

**$ping**   <br>
&emsp;&emsp; Displays bot information and status.

**$updatePrefs** *<preference\> <value\>*  <br>
&emsp;&emsp; Sets-user specific preferences for easier use. <br>
&emsp;&emsp; <u>Valid preferences</u>: *privacy, zipcode, country, units* <br>
&emsp;&emsp; <u>Valid *privacy* values</u>: *public, private* <br>
&emsp;&emsp; <u>Valid *units* values</u>: *metric, imperial* <br>

**$weather** *<zipcode\> <countrycode\>*  <br>
&emsp;&emsp; Retrieves local weather information using parameters. <br>

**$weather** *<zipcode\> <countrycode\> <unit\>* <br>
&emsp;&emsp; Retrieves local weather information using parameters. <br>
&emsp;&emsp; Defaults to 'metric' units. <br>

**$getweather** <br>
&emsp;&emsp; Retrieves local weather information using *saved preferences* as parameters. <br>
&emsp;&emsp; <u>Note</u>: only works if preferences are already set. <br>

---

## Backend

### Libraries

This section highlights each library and their specific use within the application


```py
import discord			# Tools to access Discord through its API
import request			# Function to request information from OpenweatherAPI endpoint
import os			# Used for environmental secrets
import json			# Functions for JSON to Dict conversion
import hashlib			# Functions for hashing strings
import datetime			# Functions for grabbing timestamp information
```

---

---

### Classes

This section highlights the classes specifically defined within the source code. 

```py
class t_colors			
	# Contained information for Strings which display console output with color
```
---
### Filesystem

`main.py`:   	Main script for application<br>
`server.json`:  Storage location for user / guild preferences.

---

### Methods

#### Utility Methods

```py
async def updateServerInfo(what, title, pref, data) 
```
**Description:** Reads current information within `server.json` and stores it as a temporary variable. Updates this temporary variable using the parameters, then writes its information to update `server.json`.<br> <br>
**Parameters:**  <br>
*what*:String['guildPref', 'userPref'] <br> *title*:String[*any*], <br>*pref*:String['privacy', 'zipcode', 'country', 'units'] <br> *data*:String[*any*]
**Returns**: *None*
<br><br>

```py
async def hash(str) 
```
**Description**: Applies md5 hash to provided string.<br> <br>
**Parameters**: *str*:String(*any*) <br>
**Returns**: String
<br><br>
#### Command Methods

```py
async def getWeatherViaZip(zipcode, countrycode, units, privacy)
```

**Description**: Retrieves weather information as String.<br> <br>
**Parameters**:  <br>*zipcode*:String(*any*) <br> *countrycode*:String(*any*) <br>*units*:String('metric', 'imperial') <br> *privacy*:String('public', 'private') <br>
**Returns**: String
<br><br>
#### Event Scripts

```py
@client.event
async def on_ready():
```
**Event**:  Application starts <br>
**Description**: Displays message showing successful bot startup.<br> <br>
**Parameters**: None<br>
**Returns**: None
<br><br>

```py
@client.event
async def on_message(message)
```
**Event**: Message is sent to a Discord server the bot is apart of. <br>
**Description**: Performs various actions based on messages sent (see: [commands]((#commands)))<br> <br>
**Parameters**: *message*:obj(*any*) <br>
**Returns**: None
