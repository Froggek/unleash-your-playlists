# Unleash Your Playlists 🚀
## What is that for?
Have you ever felt the *frustration* of of being on vacation, or at a party, with some friends of yours, and chilling out while passively listening to some trendy and appropriate music tracks ... 
And then, as if you wanted to take a bit of that atmosphere and bring it back home, you're asking the DJ: "shoot me your playlist, it's so cool!"

And you get as an answer: "Sure! It's on *Spotify*, my favorite online music service!"

**Sh\*t**! *You're on Deezer/Apple Music/Amazon Music/whatever-not-spotify-music!*

## Technically
Our goal here is to duplicate a given playlist from one online service to another, in a best effort mode. 
It aims at releasing a bit the vendor lock-ins ... in an absolutely legal way, of course ;-) 

The first PoC attempts to do so from **[Spotify](https://www.spotify.com/)** to **[Deezer](https://www.deezer.com/en/)**. 
Ultimately, we want to: 

- Do it the other way other around
- Integrate other music providers 
- Ideally, be music provider-agnostic (?) 

## How to use it?
### Prerequisite
TODO 

### Configuration
TODO

Create a `data/config.yaml` file (based on `data/config.yaml.example`) which contains, at least: 

- A **Spotify** (OAuth 2) access token 
- A **deezer** (OAuth 2) access token.  

### Play! 
Simply execute `src/main.py` using **Python 3** 

## Credits 
- [pydeezer SDK](https://github.com/steinitzu/pydeezer/blob/master/pydeezer/__init__.py) from [steinitzu](https://github.com/steinitzu) - not used, but inspired from :-) 
