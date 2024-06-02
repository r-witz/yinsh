# YINSH

!['Yinsh Preview'](../assets/graphics/github/yinsh-game-screenshot.png)

This project is a Python adaptation of the board game Yinsh. Yinsh is an abstract strategy board game for two players designed by Kris Burm and published by Rio Grande Games. The game features simple rules yet complex strategic depth, making it a challenging and engaging experience for players.

# Table of Contents
1. [YINSH](#yinsh)
2. [Technologies Used](#technologies-used)
3. [Getting Started](#getting-started)
	- [Prerequisites](#prerequisites)
	- [Launching the Project](#launching-the-project)
4. [Maintaining the Project](#maintaining-the-project)
	- [File organisations](#file-organisations)
	- [Python Coding Style](#python-coding-style)
	- [Contributing GIT Guidelines](#contributing-git-guidelines)
5. [Code Structure](#code-structure)
	- [Class Diagram](#class-diagram)
	- [Algorithms Used](#algorithms-used)
		- [Hexagonal Grid Management](#hexagonal-grid-management)
		- [Ring Movement](#ring-movement)
		- [Alignement Detection](#alignement-detection)
		- [Alignement Selection](#alignement-selection)
	- [Network](#network)
6. [License](#license)

# Technologies Used

In this project, we have chosen Python as the primary language for the implementation. We had envisaged to choose the C programming language for this project but it has mainly not been used because of the compatibility complexity with multiple platforms as well as the code complexity which was increased compared to Python. The decision to use Python was based on several factors, including:

- **Community Support**: Python has a large and active community, which means there are plenty of resources, libraries, and frameworks available to support our development process.

- **Compatibility**: Python is compatible with the platforms and systems we are targeting, ensuring that our code can run smoothly across different environments.

- **Familiarity**: The development team has extensive experience and expertise in Python, which will facilitate the development process and reduce the learning curve.

Additionally, we have chosen to utilize Pygame as a key library for this project. Pygame provides a wide range of functionalities and features that align with our project requirements, including game development. Its robustness, reliability, and active community support make it an ideal choice for our development needs.

> By selecting **Python** and **Pygame**, we aim to achieve a balance between performance, maintainability, and ease of development, ensuring a successful implementation of our project.

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

# Maintaining the Project

These instructions will give you the basic knowledge about the project organisation, so you can maintain or understand it.

## File organisations

```bash
yinsh/
│
├── assets/                      # Folder for storing game's assets
│   ├── audio/                   # Game audio
│   ├── fonts/                   # Game fonts
│   └── graphics/                # Other assets (i.e. images, video)
├── docs/                        # Folder for documentation files
│   ├── technical_manual.md      # Technical documentation
│   └── user_guide.md            # User manual
├── src/                         # Source code directory
│   ├── board.py                 # Game board logic and operations
│   ├── game.py                  # Controls game flow, rules, and victory.
│   ├── hexagon.py               # Properties and behaviors of hexagons in board.
│   ├── player.py                # Player properties, and methods.
│   ├── server.py                # Sets up and manages the game server.
│   └── client.py                # Sets up and manages the game client.
├── main.py                      # Program used to launch game
├── requirements.txt             # Libraries required
├── .gitignore                   # Files to ignore when commiting
├── LICENSE                      # Project's License
└── README.md                    # Describe the project and how to install
```

> To maintain the project, you should have a basic understanding of Python and Pygame. You should also be familiar with the project structure and the codebase.

## Python Coding Style

**Variable Naming:**

1. **snake_case**: For variable and function names (eg. `player_turn`, `game_state`).
2. **UPPERCASE**: For constants (eg. `BOARD_SIZE`, `MAX_PLAYERS`).
3. **PascalCase**: For classes (eg. `GameLogic`, `BoardRenderer`).

**Docstring Conventions:**

1. **Use triple quotes:** For docstrings, use triple double quotes (`"""`).
2. **Write descriptive docstring:** Describe the purpose and functionality of functions, classes and modules concisely but comprehensively.
3. **Include type information:** Add parameters types, return types (Look at already written code for exemples).

**Type Hinting:**

1. **Use type hints:** Provide type hints for functions parameters, return values, and variables when possible.
2. **Use built-in types:** Perfer built-in types (`int`, `str`, `list`, `dict`, etc.).
3. **Type hints for collections:** For collections, use `list[type]`, `dict[key_type, value_type]`, etc...

**Exemple Docstring with Type Hinting:**

```python
def calculate_score(player_turn: int, game_state: dict[str, list[int]], multiplier: int = 1) -> int:
	"""
	Calculate the score for the current player.
	:param player_turn: int, The index of the current player.
	:param game_state: Dict[str, List[int]], The state of the game. Keys are player identifiers, Values are lists of scores for each player.
	:param multiplier: int(optional), A multiplier to adjust the score calculation. Defaults to 1.
	:return: int, The calculated score for the player.
	"""
	# Function implementation goes here
```

## Contributing GIT Guidelines

Contributors are encouraged to adhere to the following guidelines when contributing to the project.

Use Git for version control, and adhere to the commit message structure and branch naming conventions outlined in the [git conventional commits](https://www.conventionalcommits.org/en/v1.0.0/
). Here are some highlights about it :

**Commit Types:**

1. **feat:** Use for new features implemented.
2. **fix:** Use for bug fixes.
3. **refactor:** Use for code refactoring.
4. **docs:** Use for documentation updates.
5. **test:** Use for adding or modifying tests.
6. **chore:** Use for general maintenance or miscellaneous tasks.

Add "!" at the end of the keyword to denote a breaking change (e.g., `feat!`, `fix!`, etc.).

**Example Commit Messages:**

- feat!(graphics): Add new background image
- fix(network): Fix connection timeout issue
- docs(user): Update user manual for gameplay instructions
- test(utils): Add unit tests for utility function
- refactor(game): Refactor game logic for improved performance
- chore!(deps): Update dependencies to latest versions

# Code Structure

If you wish to know more about data structures used throughout the whole project, you may refer directly to the code. <br>
All the classes, functions and methods are documented using type hinting and docstring, making it as simple as possible to understand the datatypes used.

## Class Diagram

![class diagram](../assets/graphics/github/class-diagram.png)

> This class diagram is representing how the main game logic is made. <br>
It will also help you understand how the classes interact with each others.

## Algorithms Used

### Hexagonal Grid Management:

The hexagonal grid management in the game involves initializing a hexagonal grid structure, placing hexagonal tiles, and managing their properties and interactions. This section explains the process of creating and managing the hexagonal grid on the game board, leveraging the [`Hexagon`](../src/hexagon.py) class to define individual hexagonal tiles and their behaviors. The key aspects of this algorithm include:

- **Hexagons Representation**: Hexagons are represented by a Class, having an x, y position and size to draw them. It then can work out its width, height, and 6 vertexes. It then has a method that check if a given point is in the Hexagon.
<br>For more information go see the [`hexagon.py`](../src/hexagon.py) file and the `init_board` method in the [`board.py`](../src/board.py) file
- **Grid Initialization**: Initializes the grid by creating Hexagonal tiles and positioning them correctly based on their coordinates. Each tile is assigned a unique identifier and positioned using axial or offset coordinates to maintain the hexagonal structure.
- **Tile Adjacency**: Calculates adjacent tiles for any given tile, facilitating movement and interaction within the grid. This is done using predefined direction vectors that represent the six possible neighboring positions in a hexagonal layout.
<br>For more information go see the `get_neighbours` method in the [`board.py`](../src/board.py) file
- **Drawing the Board**: The board is drawn using the tile adjency. We iterate through each tile of the board, get its center, and then for each neighbour got through tile adjency, we draw a line towards that neighbour.
<br>For more information go see the `draw_board` method in the [`board.py`](../src/board.py) file

![yinsh board hexagonal hitboxes backend](../assets/graphics/github/yinsh_board_hitbox_backend.png)
> You can here see how the grid is represented in backend. The red hexagons represented None types in the board, this means the tile is not an Hexagon, it is just here to space the rest of the board tiles. The white hexagons are the one actually clickable and are Hexagon types.

### Ring Movement:

The ring movement algorithm in the game involves several key steps: selecting a ring to move, determining valid destinations for the ring, moving the ring to the selected destination, and flipping markers along the path of movement. Here, we break down these steps to explain how the process is handled.

**Steps Involved in Moving a Player's Ring**

1. **Selecting the Ring to Move:**<br>
        The player selects a ring to move by clicking on it. This interaction is captured through a mouse event in the game interface. The position of the click is then mapped to the corresponding hexagon on the board.
        The method [`get_hexagon`](../src/board.py) in the Board class is used to determine the hexagon corresponding to the click position. It returns the coordinates of the hexagon if the click is within its bounds.

2. **Determining Valid Moves:**<br>
        Once a ring is selected, the game calculates all the valid cells where the ring can be moved. This is achieved using the [`valid_moves`](../src/board.py) method in the Board class.
        The [`valid_moves`](../src/board.py) method relies on the `get_lines` method to identify all potential paths (vertical, horizontal, and diagonal) from the ring's current position. It ensures that rings cannot jump over other rings and must move through empty cells.
        The `get_lines` method generates all possible lines originating from the current position of the ring, considering the hexagonal grid's geometry.
        For each line, the algorithm checks the cells sequentially. If it encounters an empty cell, it is considered a valid move. If it encounters a ring, it stops further checking along that line.

3. **Moving the Ring:**<br>
        The player then selects one of the valid moves. The ring is moved from its initial position to the final position using the move_ring method in the Player class.
        The [`move_ring`](../src/player.py) method first removes the ring from its initial position using the [`remove_ring`](../src/player.py) method and then places it at the new position using the [`place_ring`](../src/player.py) method.
        Both [`remove_ring`](../src/player.py) and [`place_ring`](../src/player.py) methods update the state of the respective hexagons on the board to reflect the ring's movement.

4. **Flipping Markers:**<br>
		After moving the ring, any markers between the initial and final positions are flipped. This is handled by the [`flip_markers`](../src/board.py) method in the Board class.
        The [`flip_markers`](../src/board.py) method first retrieves all the cells between the initial and final positions using the [`get_cells_between`](../src/board.py) method.
        It then iterates through these cells (excluding the starting and ending cells), and flips the markers. The marker is flipped from "MARKER_P1" to "MARKER_P2" and vice versa. If a cell contains no marker, it remains unchanged.

### Alignement Detection:

### Alignement Selection:

## Network

# License

This project is licensed under the GNU General Public License. For more details, see the [`LICENSE`](../LICENSE) file.