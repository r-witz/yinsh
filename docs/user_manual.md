# YINSH

!['Yinsh Preview'](../assets/graphics/github/yinsh-game-screenshot.png)

This project is a Python adaptation of the board game Yinsh. Yinsh is an abstract strategy board game for two players designed by Kris Burm and published by Rio Grande Games. The game features simple rules yet complex strategic depth, making it a challenging and engaging experience for players.

# Table of Contents
1. [YINSH](#yinsh)
2. [Getting Started](#getting-started)
	- [Prerequisites](#prerequisites)
	- [Launching the Project](#launching-the-project)
3. [How to use the game](#how-to-use-the-game)
4. [Rules](#yinsh-game-rules)
5. [License](#license)

# Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

## Prerequisites

- Python 3.11+

Once Python installed run the following command to install both dependencies
```sh
pip install -r .\requirements.txt
```

## Launching the Project

1. Clone the repository to your local machine.
```sh
git clone https://github.com/r-witz/yinsh.git
```

2. Navigate to the project directory.
```sh
cd yinsh
```

3. Run the main.py file to launch the project.
```sh
python main.py
```

# How to Use the Game

After launching the game with `python main.py`, you will be presented with the game interface. Here are some basic instructions on how to use the game:

1. **Starting a New Game:**
   - Select "Play" from the main menu.
   - From the "Play" meny you'll then have to choose what mode to play.

2. **Game Interface:**
   - The game board consists of a hexagonal grid where you place and move rings.
   - Each player starts with a set of rings of their respective color.

3. **Placing Rings:**
   - Players take turns placing their rings on the board.

4. **Moving Rings:**
   - Click on a ring to select it, then click on an empty cell to move the ring to that position.
   - As the ring moves, it flips any markers it passes over, changing their color.

5. **Removing Rings and Markers:**
   - When a player forms a row of five markers in their color, they remove these markers and one of their rings from the board.
   - The first player to remove three of their rings wins the game.

6. **Pause Menu:**
	- You can press `ESCAPE` at any stage of the game to make the pause menu pop.
	- From the pause menu you'll be able to resume the game or get back to the menu.

# YINSH Game Rules

Yinsh is a game of strategic movement and marker flipping. Here are the key rules:

1. **Setup:**
   - Each player starts with five rings of their color.
   - Rings are placed on the board during the initial phase.

2. **Gameplay:**
   - Players take turns placing markers within their rings and moving rings to flip markers.
   - When moving a ring, it must be moved in a straight line and cannot jump over other rings.
   - If it jump over markers it must stop at the first empty cell after jumping them.

3. **Flipping Markers:**
   - Moving a ring flips the color of all markers it passes over.

4. **Forming Rows:**
   - Form a continuous row of five markers in your color to score.
   - Remove these markers and one of your rings from the board.

5. **Winning:**
   - The first player to remove three of their rings wins the game.
   - If you're playing Blitz mode the first to remove a ring win.

For detailed rules and strategies, refer to the official Yinsh rulebook or visit the UltraBoardGames [Yinsh rules page](https://ultraboardgames.com/yinsh/game-rules.php).

# License

This project is licensed under the GNU General Public License. For more details, see the [`LICENSE`](../LICENSE) file.