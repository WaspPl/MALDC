
# Matrix And LCD Display Controller
 **MALDC for short** </br>
 *<sub>yes, i know D in LCD already stands for display, just treat it like chai tea.</sub>* </br>
## Short Description
This project contains a display controller that allows you to add displays to Your personal assistant making it just a little bit more friendly.
<img src="https://github.com/WaspPl/MALDC/blob/main/readmeImages/IMG_20260420_183051.jpg" width="300">

It's built to work on a Raspberry Pi with these connections in mind, but it can all be configured at will.

<img src="https://github.com/WaspPl/MALDC/blob/main/readmeImages/circuit_image.png">

# It's functions include:
1. [API activation method](#api-activation-method)
2. [LED Matrix, LCD and Buzzer synchronization](#led-matrix-lcd-and-buzzer-synchronization)
3. [Sleep states with message queueing](#sleep-states-with-message-queueing)
4. [Custom idle animations support](#custom-idle-animations-support)
5. [Full customization through a .yaml config file](#full-customization-through-a-yaml-config-file)

# API Activation Method
The system is controlled through API request. </br>
The API itself is hosted using FastAPI and listens to one endpoint.
| Method| URL |Description  |
|--|--|--|
| `Post` | `/display`  | Displays text and sprites provided in the request body  |

The `/display` route takes following arguments
| Argument | Description  |
|--|--|
| `message` | String representing the message that will be displayed using the LCD panel. |
| `spriteBase64` | String representing a base64 converted sprite to be displayed to the LED Matrix. It should be the a horizontal sprite sheet (or a single sprite) of size specified in your yaml config file.  |
| `spriteReplayTimes` | Integer telling the display how many times the specified sprite should be replayed. |
## LED Matrix, LCD and Buzzer synchronization
This project synchronizes  the LED display, LCD and a buzzer to make the assistant seem more "alive". </br>
The text sent is split into suitable chunks and displayed in screens one letter at a time  *<sub>(undertale style)</sub>* making a buzzer sound after each character *<sub>(except for " ")</sub>* . If the text is too big to fit on one screen the last character becomes an arrow that indicates the next screen is available and the screen gets changed after a specified time. </br>
<img src="https://github.com/WaspPl/MALDC/blob/main/readmeImages/IMG_20260420_200954.jpg" width="300">

While printing the characters the matrix either displays the provided sprite, or if one was not provided or has already ended tries to match it's mouth shape to the character displayed to mimic talking.

# Sleep states with message queueing

If the system receives multiple display requests in a quick succession it will queue them up in the order they were received. </br>
After getting a message it will play a "Wake Up" animation turning on the matrix display, display the message and enter a "waiting" phase after which it'll play a "Sleep" animation and disappear. </br>
During the "waiting" phase random animations with varying rarity will play until the system receives another message which will be displayed without triggering the "Wake Up" animation, or it reaches a limit of consecutive animations and falls asleep. </br>
The limits, animation rarities and timings can all be configured in the .yaml file.
## Custom idle animations support
The system is built around customizability and thus it's possible to add your own sprites and animations.</br>
There are three rarities idle animations can be assigned to:

 - common
 - uncommon
 - rare
 
Each rarity corresponds to a folder located at `/src/sprites/random/`  and can be assigned a weight that influences it's rarity. </br>
When an animation is played a rarity is chosen first and then a random image from within it's folder gets displayed. This gives user the ability to add animations to the system without editing any code.

# Full customization through a .yaml config file
This project features a cohesive config file allowing you to customize many features
| Category | Config | Type | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| **Api** | `use_uds` | Bool | `True` | Toggle to use Unix Domain Sockets instead of TCP. |
| **Api** | `linux.socket` | String | `/tmp/moris/maldc.sock` | Path to the socket file for Linux systems.|
| **Api** | `windows.host` | String | `127.0.0.1` | Host address for the API if not using uds |
| **Api** | `windows.port` | Int | `8000` | Port number for the API if not using uds |
| **Matrix** | `rows` | Int | `8` | Number of rows in the LED matrix. |
| **Matrix** | `columns` | Int | `8` | Number of columns in the LED matrix. |
| **Matrix** | `random_sprites_before_sleep` | Int | `3` | Count of random sprites to cycle through before sleep. |
| **Matrix** | `random_sprite_interval_sec` | Int | `5` | Time interval in seconds between idle sprites play. |
| **Matrix** | `random_sprites_weights.common` | Int | `4` | Weight for selecting "common" rarity sprites. |
| **Matrix** | `random_sprites_weights.uncommon` | Int | `3` | Weight for selecting "uncommon" rarity sprites. |
| **Matrix** | `random_sprites_weights.rare` | Int | `1` | Weight for selecting "rare" rarity sprites. |
| **Matrix** | `flip_every_other_row` | Bool | `True` | Whether to reverse direction on alternate rows (for zigzag wiring). |
| **Matrix** | `spritesheet_framerate` | Float | `0.1` | Delay between frames in a spritesheet animation. |
| **Matrix** | `brightness` | Float | `0.2` | Brightness level of the matrix (0.0 to 1.0). |
| **Matrix** | `sprites_folder` | String | `storage/sprites` | Directory path where sprite files are stored. |
| **Buzzer** | `pin` | Int | `23` | GPIO pin number assigned to the buzzer. |
| **LCD** | `line_count` | Int | `2` | Number of lines supported by the LCD. |
| **LCD** | `line_length` | Int | `16` | Character width of each LCD line. |
| **LCD** | `backlight_enabled_by_default` | Bool | `False` | Sets the initial state of the LCD backlight. |
| **LCD** | `long_wait_list` | List[Str] | `[",", ".", "?", "!", ":", "\n"]` | Characters that trigger a longer pause during text rendering. |
| **LCD** | `wait_time` | Float | `0.05` | Standard delay between characters. |
| **LCD** | `long_wait_time` | Float | `0.1` | Extended delay for characters defined in `long_wait_list`. |
| **LCD** | `next_screen_wait_time` | Float | `1` | Delay before transitioning to a new screen of text. |
