### Platformer

A very basic platformer game I made using the pygame library and following 
[this](https://coderslegacy.com/python/pygame-platformer-game-development/) tutorial.

![demo gif](data/gameDemo.gif)

The game is very simple so far:
* Jump higher to earn a higher score
* Every 10th platform passed increases score by 1
* Every glass of milk collected increases score by 10
* As score increases, the game will become more difficult (up to a score of 200):
  * Platforms will get smaller and further apart
  * Some platforms will disappear 3 seconds after the player lands on them. The probability of a platform disappears 
    increases with score from 0% to 90%

And that's it for now!

---

TODO:
- [x] Fix occasional jank when new platforms are generated
- [ ] Add possibility to jump down from a platform using the down arrow key
- [x] Make platforms disappear some time after the player lands on them to make the game a bit harder
  - [ ] Add 1 second to the disappearance timer when the player lands on one
- [ ] Add a start menu and exit screen
  - [ ] Add option to choose character (i.e. have a different picture)
- [ ] Disallow the player to jump up through the bottom of platforms
- [x] Add a double jump (space bar while jumping)
  - [ ] Tweak double jump vertical velocity boost - make velocity boost proportional to how fast the player is falling 
- [x] Add side strafing (left shift + arrow keys while in the air)
- [ ] Add some way of spending accumulated score/money
- [x] Make the game harder as score increases
  - [x] Make platforms smaller as score increases
  - [ ] Make platforms move faster as score increases
- [ ] Revamp player/platform collision detection and logic to determine if the player is resting on a platform
- [ ] Add distinct levels
- [ ] Add sound effects & music
- [x] Collectibles now disappear 3 seconds after generation
  - [x] Add animation to indicate time until disappearing
- [ ] Fix edge-wrapping logic for platforms and the player
 
BUGS:
- [x] If platform threshold is set to 10, occasionally there will be a gap between platforms too big to jump. Setting 
it to 20 solves this but makes the game freeze sometimes due to there not being any suitable positions for platforms - 
Fixed by redoing platform generation logic. Instead of always spawning new platforms at y=0 (the top of the screen), we 
now generate them some random distance above the current highest platform. This also eliminates occasional lag from 
trying to generate the same platform many times until finding a suitable spot
- [ ] Double jumps are not always picked up
- [ ] Sometimes when double jumping just when landing on a platform the resulting jump is disproportionately large
