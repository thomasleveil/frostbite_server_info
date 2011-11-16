#usage:
`frostbite_server_info.py [-h] [--password PASSWORD] [--format FORMAT] [--timeout SECONDS] [--debug] HOST PORT`

Simple command line tool to query a **Frostbite game server** for basic info.
Result is displayed formatted as json, xml or ini file format.

Optionally can verify RCON password correctness.

##positional arguments:
- **HOST**                 RCON IP address or hostname
- **PORT**                 RCON port

##optional arguments:

###-h, --help
show this help message and exit

###--password PASSWORD, -p PASSWORD
RCON password if you want to check password correctness

###--format FORMAT
output format (json, xml, ini)

###--timeout SECONDS
connection timeout

###--debug
activate debug output

#examples:

`$ frostbite_server_info.py 11.22.33.44 47000 --password=xxxxxxx --timeout=3`

```json
{
    "password_accepted": true,
    "game": "BF3",
    "version": "883971",
    "serverInfo": {
        "targetScore": "100",
        "roundTime": "613627",
        "team4score": null,
        "level": "MP_003",
        "team2score": "0",
        "serverName": "Test server #1",
        "gamemode": "TeamDeathMatch0",
        "numPlayers": "0",
        "maxPlayers": "16",
        "serverUptime": "789299",
        "roundsTotal": "1",
        "hasPunkbuster": "true",
        "numTeams": "2",
        "hasPassword": "false",
        "team1score": "0",
        "team3score": null,
        "onlineState": "",
        "roundsPlayed": "0",
        "isRanked": "true"
    }
}
```

`$ frostbite_server_info.py 11.22.33.44 47200 --password=xxxxxxx --timeout=3 --format=ini`
```ini
[general]
password_accepted = True
game = BF3
version = 883971

[serverInfo]
targetscore = 100
roundtime = 860776
team4score = None
level = MP_003
team2score = 0
servername = Test server #1 (NL)
gamemode = TeamDeathMatch0
numplayers = 0
maxplayers = 16
serveruptime = 1036449
roundstotal = 1
haspunkbuster = true
numteams = 2
haspassword = false
team1score = 0
team3score = None
onlinestate =
roundsplayed = 0
isranked = true
```

`$ frostbite_server_info.py 11.22.33.44 47200 --password=xxxxxxxxxx --timeout=3 --format=xml`

```xml
<?xml version="1.0" encoding="utf-8"?>
<data>
 <game>BF3</game>
 <password_accepted>True</password_accepted>
 <serverInfo>
  <gamemode>TeamDeathMatch0</gamemode>
  <hasPassword>false</hasPassword>
  <hasPunkbuster>true</hasPunkbuster>
  <isRanked>true</isRanked>
  <level>MP_003</level>
  <maxPlayers>16</maxPlayers>
  <numPlayers>0</numPlayers>
  <numTeams>2</numTeams>
  <onlineState />
  <roundTime>860849</roundTime>
  <roundsPlayed>0</roundsPlayed>
  <roundsTotal>1</roundsTotal>
  <serverName>Test server #1 (NL)</serverName>
  <serverUptime>1036521</serverUptime>
  <targetScore>100</targetScore>
  <team1score>0</team1score>
  <team2score>0</team2score>
  <team3score />
  <team4score />
  </serverInfo>
 <version>883971</version>
</data>

```

