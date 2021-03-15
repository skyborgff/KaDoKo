from typing import List
import pycountry
import datetime
import Core.Structures.List as AnimeListsStruct
import Core.Structures.Anime as AnimeStruct
import Core.Structures.Generic as GenericStruct
import Core.Structures.Other.Person as PersonStruct

DefaultCountry = pycountry.countries.get(name='Japan').name
DefaultLanguage = pycountry.languages.get(name='Japanese').name
DefaultScript = pycountry.scripts.get(name='Latin').name
DefaultLocalization = GenericStruct.Localization(Language=DefaultLanguage,
                                                 Script=DefaultScript)


def AnimeMetadata(metadata, oldAnime: AnimeStruct.Anime) -> AnimeStruct.Anime:
    Anime = AnimeStruct.Anime()
    Anime.hash = oldAnime.hash

    id: str = str(metadata.get("id"))
    # Todo: Add restrictions
    # Todo: Add releases
    ageRatingsList: List[dict] = metadata.get("ageRatings")
    status = metadata.get("status")
    # Todo: Add relations
    # Todo: Add partOfCanonicals
    genresList: List[dict] = metadata.get("genres")
    # Todo: Add soundtracks
    voiceActingsList: List[dict] = metadata.get("voiceActings")
    staffList: List[dict] = metadata.get("staff")
    starringList: List[dict] = metadata.get("starring")
    namesList: List[dict] = metadata.get("names")
    aliasesList: List[dict] = metadata.get("aliases")
    descriptionsList: List[dict] = metadata.get("descriptions")
    imagesList: List[dict] = metadata.get("images")
    crossrefsList: List[dict] = metadata.get("crossrefs")
    websitesList: List[dict] = metadata.get("websites")
    selfLink = metadata.get("selfLink")
    animeType = metadata.get("type")
    videosList: List[dict] = metadata.get("videos")
    episodesList: List[dict] = metadata.get("episodes")
    runningsList: List[dict] = metadata.get("runnings")

    def localizationMetadata(localization: dict):
        language = None
        script = None
        if localization.get('language'):
            language = localization.get('language').get('alpha2')
        if localization.get('script'):
            script = localization.get('script').get('code')
            script = pycountry.scripts.get(alpha_4=script).name
        if language:
            language = pycountry.languages.get(alpha_2=language).name
        return GenericStruct.Localization(language, script)

    def namesMetadata(namesList: List[dict]):
        names = AnimeStruct.Names()
        for name in namesList:
            text = name.get('text')
            localization = localizationMetadata(name.get('localization'))
            Name = GenericStruct.Text(text, localization)
            names.list.append(Name)
        return names

    if ageRatingsList:
        ageRating = ageRatingsList[0]
        Anime.ageRating = AnimeStruct.AgeRating(Age=ageRating.get('age'), Tag=ageRating.get('tag'))
    if status:
        Anime.status = AnimeStruct.ReleaseStatus[status]
    if genresList:
        tags = AnimeStruct.Tags()
        for genre in genresList:
            # Todo: See if exists in database a tag with same name but different aliases
            tag = AnimeStruct.Tag(name=genre.get("names")[0].get("text"))
            tags.list.append(tag)
        Anime.tags = tags
    if voiceActingsList:
        voiceActings = AnimeStruct.VoiceActings()
        voiced = None
        actor = None
        for voiceActing in voiceActingsList:
            Voiced = voiceActing.get('voiced')
            Actor = voiceActing.get('actor')
            if Voiced:
                birthday = Voiced.get('birthday')
                # Note To Self: want example of how it comes out
                country = Voiced.get('hometown')
                gender = PersonStruct.Gender[Voiced.get('gender')]
                age = Voiced.get('age')
                name = None
                for tryname in Voiced.get('names'):
                    if tryname.get('localization').get('script') and tryname.get('localization').get('script').get('code') == 'Latn':
                        name = tryname.get('text')
                if name is None:
                    name = Voiced.get('names')[0].get('text')
                voiced = PersonStruct.Person(name=name,
                                             birthday=birthday,
                                             country=country,
                                             gender=gender,
                                             age=age)
            if Actor:
                birthday = Actor.get('birthday')
                # Note To Self: want example of how it comes out
                country = Actor.get('hometown')
                gender = PersonStruct.Gender[Actor.get('gender')]
                age = Actor.get('age')
                name = None
                for tryname in Actor.get('names'):
                    if tryname.get('localization').get('script'):
                        if tryname.get('localization').get('script').get('code') == 'Latn':
                            name = tryname.get('text')
                            break
                if name is None:
                    name = Actor.get('names')[0].get('text')
                actor = PersonStruct.Person(name=name,
                                             birthday=birthday,
                                             country=country,
                                             gender=gender,
                                             age=age)
                voiceActing = AnimeStruct.VoiceActing(actor=actor, voiced=voiced)
            voiceActings.list.append(voiceActing)
        Anime.voiceActings = voiceActings
    if staffList:
        studios = AnimeStruct.Studios()
        for staff in staffList:
            # Todo: investigate studio tags
            studioNames = AnimeStruct.Names()
            if staff.get('role').get('tag') == 'animation-works':
                Name = namesMetadata(staff.get('collaborator').get('names'))
                studioNames.list.append(Name)
        Anime.status = studios
    if starringList:
        for starring in starringList:
            relation = starring.get('relation')
            Character = starring.get('character')
            birthday = Character.get('birthday')
            # Note To Self: want example of how it comes out
            country = Character.get('hometown')
            gender = PersonStruct.Gender[Character.get('gender')]
            age = Character.get('age')
            name = None
            for tryname in Character.get('names'):
                if tryname.get('localization').get('script'):
                    if tryname.get('localization').get('script').get('code') == 'Latn':
                        name = tryname.get('text')
                        break
            if name is None:
                name = Character.get('names')[0].get('text')
            character = PersonStruct.Person(name=name,
                                        birthday=birthday,
                                        country=country,
                                        gender=gender,
                                        age=age)

    if namesList:
        Anime.names = namesMetadata(namesList)
    if aliasesList:
        names = namesMetadata(aliasesList)
        Anime.names.list.extend(names.list)
    if descriptionsList:
        if len(descriptionsList) > 1:
            raise Exception('Need to add localizations to descriptions')
        Anime.description = AnimeStruct.Description(descriptionsList[0].get('text'))
    if imagesList:
        files_type_priority = {'webp': 0, "png": 1, 'jpg': 2}
        images = GenericStruct.Images()
        for image in imagesList:
            type = image.get('type')
            files: dict = image.get('image').get('files')
            file_list = [file.get('publicUri') for file in files]
            file_list.sort(key=lambda i: files_type_priority.get(i.split('.')[-1], 100))
            images.list.append(GenericStruct.Image(file_list[0]))
        Anime.images = images
    # Note To Self: I'm ignoring crossrefs, may be needed in the future tho
    # Note To Self: I'm ignoring websites, may be needed in the future tho
    # Note To Self: I'm ignoring selflink, may be needed in the future tho
    Anime.type = AnimeStruct.AnimeType[animeType]
    if videosList:
        videos = AnimeStruct.Videos()
        for video in videosList:
            url = video.get('video').get('files')[0].get('publicUri')
            Video = AnimeStruct.Video(url=url, type=AnimeStruct.VideoType[video.get('type')])
            videos.list.append(Video)
        Anime.videos = videos
    if episodesList:
        episodes = AnimeStruct.Episodes()
        for episode in episodesList:
            type = AnimeStruct.EpisodeType[episode.get('type')]
            index = episode.get('identifier')
            releasedate = None
            if episode.get('releaseDate'):
                # '2020-12-04T00:00:00Z'
                releasedate = datetime.datetime.strptime(episode.get('releaseDate')[:-2],
                                                         "%Y-%m-%dT%H:%M:%S")
            names = namesMetadata(episode.get('names'))
            # Ignoring AgeRating, websites and videos
            Episode = AnimeStruct.Episode(names=names, releaseDate=releasedate,
                                          type=type, index=index)
            episodes.list.append(Episode)
        Anime.episodes = episodes
    if runningsList:
        runnings = AnimeStruct.Runnings()
        for running in runningsList:
            since = datetime.datetime.strptime(runningsList[0].get('from')[:-2], "%Y-%m-%dT%H:%M:%S")
            if runningsList[0].get('to'):
                to = datetime.datetime.strptime(runningsList[0].get('to')[:-2], "%Y-%m-%dT%H:%M:%S")
            else:
                to = datetime.datetime.utcfromtimestamp(0)
            Running = AnimeStruct.Running(since=since, to=to)
            runnings.list.append(Running)
        Anime.runnings = runnings

    Anime.libraryStatus = oldAnime.libraryStatus
    Anime.id = oldAnime.id
    Anime.ageRating.hash = oldAnime.ageRating.hash
    Anime.publicRating.hash = oldAnime.publicRating.hash
    Anime.personalRating.hash = oldAnime.personalRating.hash
    Anime.names.hash = oldAnime.names.hash
    Anime.images.hash = oldAnime.images.hash
    Anime.soundtracks.hash = oldAnime.soundtracks.hash
    Anime.voiceActings.hash = oldAnime.voiceActings.hash
    Anime.crossRefs.hash = oldAnime.crossRefs.hash
    Anime.videos.hash = oldAnime.videos.hash
    Anime.tags.hash = oldAnime.tags.hash
    Anime.description.hash = oldAnime.description.hash
    Anime.episodes.hash = oldAnime.episodes.hash
    Anime.runnings.hash = oldAnime.runnings.hash
    Anime.studios.hash = oldAnime.studios.hash

    return Anime
