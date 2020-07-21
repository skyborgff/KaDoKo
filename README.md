# MAL-torrent-Plex-sync
This program will be the middleman between your MAL account, and your plex. It takes care of downloading, loading plex data, and adding episodes as watched

## Functions
It will load your MAL account, and sync your MAL shows with aniDB ones. It will download any anime marked as "watching" on MAL, as well as download and mark as watching any show marked as "Plan To Watch" as soon as it releases.

Besides that, it will rename shows upon download completion so they get properly named, and they get properly showing on Plex.
It will serve as Plex agent, retrieving data for the animes, as well as mark an episode as watched upon watching it on plex.

## Developing
On main folder:

\>```npm run build```

(Due to eel, you may need to run it twice in a row for it to be successful)
Then

\>```python run app.py```

It should open a browser window

#Useful links:

Bootstrap components:

https://bootstrap-vue.org/docs/components

Json reade:

https://jsonformatter.curiousconcept.com/

Eel and vue together:

https://github.com/samuelhwilliams/Eel#starting-the-app