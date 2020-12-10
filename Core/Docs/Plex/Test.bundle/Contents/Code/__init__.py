import re  #import time def Log(dbgline): Log("\n\n\n----------\n\n" + time.strftime("%H:%M:%S - ") + dbgline + "\n\n---------\n\n\n")

def Start():
  HTTP.CacheTime             = CACHE_1DAY
  HTTP.Headers['User-Agent'] = 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.2; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0)'

class TestAgent(Agent.TV_Shows):
  name, primary_provider, fallback_agent, contributes_to, languages, accepts_from = ('Test', True, False, None, [Locale.Language.English,], ['com.plexapp.agents.localmedia'] )  #, 'com.plexapp.agents.opensubtitles'
  
  def search(self, results, media, lang, manual=False):
    Log("".ljust(157, '-'))
    Log("search() - Title: '%s'  -> '%s'" % (media.title, media.episode))
    if media.title:  shootSite = media.title
    else:            Log('ERROR: No Site for ' + media.episode)
    if shootSite:
      results.Append( MetadataSearchResult(
            id=str(shootSite),
            name=shootSite,
            year=None,
            lang=lang,
            score=100
      ) )
    results.Sort('score', descending=True)

  def update(self, metadata, media, lang):
    Log("".ljust(157, '='))
    Log("update() - metadata.id: '%s', metadata.title: '%s'" % (metadata.id, metadata.title))
    metadata.title                   = "title updated"
    metadata.summary                 = 'Summary updated'
    metadata.studio                  = 'Studio updated'
    metadata.originally_available_at = Datetime.ParseDate('1981-12-03').date()
    Log('update() ended')
    @parallelize
    def UpdateEpisodes():
      for year in media.seasons:
        for shootID in media.seasons[year].episodes:
          episode = metadata.seasons[year].episodes[shootID]
          @task  # Create a task for updating this episode
          def UpdateEpisode(episode=episode, shootID=shootID):
            episode.title = 'AGENT: ' + shootID
    