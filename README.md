# Kadoko
![alt text](https://raw.githubusercontent.com/skyborgff/KaDoKo/master/Core/images/logo.png "KaDoKo Logo")

Your anime list synchronizer, metadata organizer and media server metadata provider.

##Overview:
- Select what lists are synchonizing.
- Choose what metadata provider populates what info.   
Ex: Description comes from MAL, episode names from AniDB, episode descriptions from Animeshon, etc
- Provide metadata to a media server.

##Lists supported:
| List               | Status      | 
| ------------------ |:-----------:|
| Mal                | Implemented |
| Animeshon          | Planned     |
| AniDB              | Planned     |
| AniList            | Planned     |
| Anime-planet       | Planned     |
| Anime News Network | Planned     |
| Kitsu              | Planned     |

##Metadata Providers supported:
| Metadata provider  | Status      | 
| ------------------ |:-----------:|
| Mal                | Implemented |
| Animeshon          | Implemented |
| AniDB              | Planned     |
| AniList            | Planned     |
| Anime-planet       | Planned     |
| Anime News Network | Planned     |
| Kitsu              | Planned     |

##Media server metadata support:
| Media Server | Status  | 
| ------------ |:-------:|
| Plex         | Planned |
| Jellyfin     | Planned |

##Other planned Plugins:
| Plugin           | Status  |Description |
| ---------------- |:-------:|------------ |
| qBittorrent      | Planned | Downloads new episodes from your watching and custom list |
| webtorrent       | Planned | See episodes from your watching and custom list |
| ListSynchronizer | Planned | Synchronizes your lists |
| PTWReleaseMover  | Planned | Moves animes from PTW to the Watching lists when they release |
| Renamer          | Planned | Renames files to fit a naming scheme |


## Developing
On main folder:

Run UI webserver  
\>```npm run serve```

Run main program  
\>```python run app.py```

#Useful links:

Bootstrap components:  
https://bootstrap-vue.org/docs/components

Json reader:  
https://jsonformatter.curiousconcept.com/