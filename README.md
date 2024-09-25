# Galactic Salvage

## Overview

Galactic Salvage is an exciting game built using Python 3.12.3 and the `pygame` library. In this game, players navigate through space to avoid asteroids, collect extra lives, and manage their resources to achieve high scores. 

## Features

- **Asteroid Evasion**: Navigate your spaceship to dodge incoming asteroids.
- **Extra Lives**: Collect extra lives to prolong your gameplay.
- **Score Keeping**: Keep track of your score with the integrated scoreboard.
- **Dynamic Levels**: Progress through different levels as you advance in the game.
- **Interactive UI**: Start the game using the interactive play button.
- **Sound Effects**: Enjoy immersive sound effects as you play.

## Getting Started

Follow these instructions to get a copy of the Galactic Salvage game up and running on your local machine.

### Prerequisites

- Python 3.12.3
- [Other prerequisites such as a virtual environment, if any]

### Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/your-username/galactic-salvage.git
    ```
2. Navigate to the project directory:
    ```sh
    cd galactic-salvage
    ```
3. (Optional) Create and activate a virtual environment:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```
4. Install the required packages:
    ```sh
    pip install pygame
    ```

### Running the Game

To run the game, execute the following command:
```sh
python main.py
```

## Usage

1. **Start the Game**: Use the play button to start the game.
2. **Control the Ship**: Use the keyboard to control the spaceship and dodge asteroids.
3. **Collect Items**: Gather extra lives and other power-ups to increase your score.
4. **Avoid Collisions**: Make sure to avoid asteroids and other obstacles to keep the game active.

## Core Components

- **Attributes**:
  - `clock`: Manages the game clock.
  - `settings`: Stores game settings.
  - `game_active`: Tracks if the game is active.
  - `asteroids`, `extra_lives`, `bullets`, `broken_ships`: Manage different game objects.
  - `scoreboard`: Displays the player's score.
  - `sounds`: Manages game sounds.
  - and more...

- **Methods**:
  - `__init__`: Initializes the game.
  - `_check_keydown_events`, `_check_keyup_events`: Handle keyboard events.
  - `_fire_bullet`, `_update_bullets`: Manage bullet firing and updating.
  - `_create_asteroids`, `_update_asteroids`: Handle creation and update of asteroids.
  - `_check_collisions`: Various methods to check for object collisions.
  - `run_game`: Main game loop.
  - and more...

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a branch (`git checkout -b feature-branch`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin feature-branch`)
5. Create a new Pull Request

## Acknowledgements


## Contact

For questions or further information, open an issue in this repository.