# Tortuga online board game
![Python application](https://github.com/Glyphack/tortuga/workflows/Python%20application/badge.svg)

tortuga is a board game with 2-9 players. Players are divided into teams of British and French pirates. In games with an odd number of players, there will also be a Dutch pirate. You will begin the game on either the Flying Dutchman or the Jolly Roger, but the other players on your ship will not necessarily be on your team.

![tortuga-game](https://github.com/Glyphack/tortuga/blob/master/assets/game_demo.gif)

## How to play
complete rules and how to play for the game is available [here](https://ndsslibraryblog.files.wordpress.com/2017/11/tortuga-1667-pp-rules.pdf).

## Tortugack
this project is a server implementation for this game. It contains a REST Api
to play the game.

#### API Docs
Api documentation is available [here](https://github.com/Glyphack/tortuga/wiki/Api-Documentation)

#### Clients
It currently has clients for these platforms:
- web: https://github.com/Frostack/tortugack-client


### Contributing
This project is just finished and heavily needs testing, So your best contribution would be playing with your friends and giving
feedback.
Also if you are interested you can contact me for creating a client for tortuga.

##### Tests
to run tests install `pytest` and run:
```bash
pytest app
```
