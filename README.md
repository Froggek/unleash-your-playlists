# Unleash Your Playlists 🚀
## What is that for?
Have you ever felt the *frustration* of of being on vacation, or at a party, with some friends of yours, and chilling out while passively listening to some trendy and appropriate music tracks ... 
And then, as if you wanted to take a bit of that atmosphere and bring it back home, you're asking the DJ: "shoot me your playlist, it's so cool!"

And you get as an answer: "Sure! It's on *Spotify*, my favorite online music service!"

**Sh\*t**! *You're on Deezer/Apple Music/Amazon Music/whatever-not-spotify-music!*

Keywords: music streaming service, playlists, synchronization, migration, Spotify, Deezer, YouTube Music

## Technically
Our goal here is to duplicate a given playlist from one online service to another, in a best effort mode. 
It aims at releasing a bit the vendor lock-ins ... in an absolutely legal way, of course ;-) 

The first PoC attempts to do so from **[Spotify](https://www.spotify.com/)** to **[Deezer](https://www.deezer.com/en/)**. 
Ultimately, we want to: 

- Do it the other way other around
- Integrate other music providers ([Youtube](https://www.youtube.com/) is a good candidate)
- Ideally, be music provider-agnostic (?) 

## How to use it?
### Prerequisite
TODO 
- Python 

### Installation
- (Optional) [Create a virtual Python environment (venv)](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/#install-packages-in-a-virtual-environment-using-pip-and-venv), and activate it
- Make sure [you have a recent version `pip` installed](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/#prepare-pip)
- Install the following packages
    > python3 -m pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib

    > python3 -m pip install pyyaml


### Configuration
TODO

Create a `data/config.yaml` file (based on `data/config.yaml.example`) which contains, at least: 

- A **Spotify** (OAuth 2) access token 
- A **deezer** (OAuth 2) access token.  

### Play! 
Simply execute `src/main.py` using **Python 3** 

## Technical Considerations
### Authorization
The application needs to access the music provider API _on behalf of_ the user (to read from the source playlist, and write to the target one). 
For each music provider: 
- If a valid token (access or refresh) is available from the config file, it will be used
- Otherwise, an [OAuth2 flow](https://www.rfc-editor.org/rfc/rfc6749) if triggered. In this case, the user has to grant the application access to the music provider (with the correct scopes).    

## Roadmap

### Bugs

### Feature Requests
- Setup guide (incl. list of dependencies)
- Additional use cases

## Credits 
- [pydeezer SDK](https://github.com/steinitzu/pydeezer/blob/master/pydeezer/__init__.py) from steinitzu - not used, but inspired from :-) 