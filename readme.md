# attune.
## (15112 Term Project)
## A space for all your music, all your stats, all for you and you only
### Problem:
Have you ever bought an album from your favorite indie band on Bandcamp to support them, listened to it constantly, and thought, "hey, it'd be nice if I could get some listening analysis for what I listen to locally"? Or, maybe you're frustrated by the Spotify algorithm, the secretive nature of your Spotify wrapped, and how your Spotify and last.fm don't agree on what you listened to. Or, maybe you just want an application that doesn't distract you while you're trying to work.

If you related to any of those statements, well, welcome to attune.

attune is a music application that synchronizes and analyzes the user’s listening history locally. For those whose music libraries span local files as well as streaming services such as Spotify, there is limited support for a centralized platform in which to analyze listening history. While other applications and websites can show certain statistics about a user’s listening, these insights are sometimes shallow and uninteresting, and don’t include local music streaming. attune can stream a user’s local music files, while analyzing listening history.

### Getting Started:
#### You'll need:
- Python 3
- [PyGame Mixer](https://www.pygame.org/docs/ref/mixer.html) (`pip3 install pygame`)
- [Last.fm API key](https://www.last.fm/api/account/create) (if downloading source code from GitHub) (does not apply to 112 TAs)

#### Tips:
- Run the modal.py file **from the terminal (if on Linux/Mac) or cmd (if on Windows)**. Don't use the 'run' button in your IDE.
- If you're on Linux/Mac, PyGame Mixer is unpredictable about mp3 file support. Try using flac, wav, or ogg files.
- Create a last.fm account for the best experience with music synchronization.

### Shortcuts:
- This app can be completely controlled through keyboard shortcuts.
- To navigate through pages and songs, use the left, right, up, and down arrow keys.
- To repeat a song in the player, press 'r'. To repeat a queue in the player, press 'R'.
- To play/pause, press space.
All other shortcuts are listed within the application itself.

### List of APIs and python3 modules used in this application:
- [Last.fm API](https://www.last.fm/api)
- [PyGame Mixer](https://www.pygame.org/docs/ref/mixer.html)