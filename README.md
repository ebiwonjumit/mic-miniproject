# mic-othello

## Description
This is a WebGME Design Studio project. It allows you to play Othello. WebGME is a generic web-based modeling environment that was created by ISIS at Vanderbilt.


## Installation
First, install the miniproject-test following:
- [NodeJS](https://nodejs.org/en/) (LTS recommended)
- [MongoDB](https://www.mongodb.com/)

Second, start mongodb locally by running the `mongod` executable in your mongodb installation (you may need to create a `data` directory or set `--dbpath`).

Then, run `webgme start` from the project root to start . Finally, navigate to `http://localhost:8888` to start using miniproject-test!

### Basic deployment
For a regular deployment, you need to install the following components on top of fetching this repository:
- [NodeJS](https://nodejs.org/en/) (LTS recommended)
- [MongoDB](https://www.mongodb.com/)
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)

After all components in place, you need to install the dependencies, using `npm i` command. After this you need to run `docker compose build` command to build the dependencies. Once that is done, you can run `docker compose up` command to get the server running.

## Development
If you want to make any changes, make sure to run `docker compose build` command once you have finished making changes.

### Seed
There exists one seed created for this design studio named `Othello`. The defaults are also available. 
To create new one, just use the command `webgme new seed -f mySeedFile.webgmex mySeedName`.

### Plugins
All plugins were written in Python.
- othelloPlayerMove: Permits the player to make a move on the selected tile
- othelloAuto: The game automatically makes a random move
- othelloCountPieces: Will return the current number of pieces on the board.
- othelloHighlightMoves: Will return a list of all valid moves
- othelloUndo: The game will undo the current move

Whenever a new game state is created, the game will ensure that the necessary pieces are flipped to their proper color. 

To play the game, please use the plugins in the Game. Shown below:
![alt text](https://github.com/ebiwonjumit/mic-miniproject/blob/main/images/gamePlugins.png)


and the plugin in the Tile:
![alt text](https://github.com/ebiwonjumit/mic-miniproject/blob/main/images/tilePlugins.png)


### Visualization
I tried to create a visualization for the Othello game within the WebGME environment. All I was able to do was create buttons for my plugins within the Play Visualizer. Shown Below:
![alt text](https://github.com/ebiwonjumit/mic-miniproject/blob/main/images/buttons.png)

In the future, I plan to create a full visualization for the Othello game in React.






