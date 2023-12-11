# mic-othello
This is a design


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



Othello_Game_Design_Studio
CS 6388 Model-Integrated Computing final project.

Introduction
Othello Game Studio is a comprehensive design studio for creating and playing the Othello (Reversi) game. This studio includes a visualizer, game logic plugins, and a meta-model for an immersive gaming experience.

Installation Instructions
Prerequisites
Node.js (version 18 LTS or higher)
Python3 (version 3.11.0 or higher, if applicable)
Steps
Open the terminal and clone the repository
git clone https://github.com/Pingumaniac/Othello_Game_Design_Studio.git
cd [repository directory/myminiproject]
Install dependencies (use Powershell for Windows, Terminal for macOS)
npm install
npm install webgme
npm install zeromq
pip3 install zmq
pip3 install webgme-bindings
npm install webgme-bindings
Install these commands inside ./myminiproject/node_modules/webgme-bindings/python/webgme-bindings

webgme import viz ICore webgme-icore
webgme import plugin PyCoreExecutor webgme-icore
webgme import router BindingsDocs webgme-bindings
pip3 install -e .
Download/Install Docker Desktop from the following url: https://www.docker.com/products/docker-desktop/
Download/Install the latest version of mongo in Docker Image.
Create an image of mongo. For optional settings, please set the Host path as
[repository directory]/DB
and set the Container path as

/data/db
The port number should be 27018 not 27017 (which is default). 6. From the terminal, enter the following command.

node app.js
Open your browser and navigate to [http://localhost:8888].
Implementation Description
Structure
src/: Contains the source code for the studio.
plugins/: Game logic plugins (Highlight valid tiles, Counting pieces, Flipping, Undo, Auto).
visualizers/: Visualization components for the game.
meta/: Meta-model for the game.
Technologies Used
React.js for front-end visualization.
Node.js for back-end services.
WebGME for model integration.
Python for creating the plugins.
Usage Description
Playing the Game
Start a New Game:
Click on 'New Game' to initialize a new Othello board.
Making Moves:
Click on a valid tile to place your piece.
The valid tiles are highlighted based on the current game state.
Game Progression:
The game automatically counts and displays the number of pieces for each color.
After each move, the board updates to reflect the new state.
Undo Functionality:
Click 'Undo' to revert to the previous state.
Auto Play (Optional):
Click 'Auto' to let the computer make a move.
End of the Game
The game concludes when no valid moves are available.
The final score is displayed, indicating the winner.
Repository Contents
README.md: This documentation file.
src/: Source code directory.
Deployment
Follow the installation instructions to deploy the Othello Game Studio on your local machine. Ensure all dependencies are installed for a smooth setup.
You can create a new seed by typing the following command on terminal:
webgme new seed [seed_name]
