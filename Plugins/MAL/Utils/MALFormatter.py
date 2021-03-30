from typing import List
import pycountry
import datetime
import Core.Structures.List as AnimeListsStruct
import Core.Structures.Anime as AnimeStruct
import Core.Structures.Generic as GenericStruct

DefaultCountry = pycountry.countries.get(name='Japan').name
DefaultLanguage = pycountry.languages.get(name='Japanese').name
DefaultScript = pycountry.scripts.get(name='Latin').name
DefaultTag = 'jpn-Latn'
DefaultLocalization = GenericStruct.Localization(Tag=DefaultTag)

def AnimeList(List: list):
    AnimeLists = AnimeListsStruct.AnimeLists()
    size_list = len(List)
    completedList = 0
    for anime in List:
        node: dict = anime.get("node")
        id = node.get("id")
        print(f"Formatting MAL id: {id}")
        title = node.get("title")
        main_picture = node.get("main_picture")
        medium_picture = main_picture.get("medium")
        large_picture = main_picture.get("large")

        list_status: dict = anime.get("list_status")
        status = list_status.get("status")
        score = list_status.get("score")
        num_episodes_watched = list_status.get("num_episodes_watched")
        is_rewatching = list_status.get("is_rewatching")
        updated_at = list_status.get("updated_at")

        PureAnime = AnimeStruct.Anime()
        MetaID = GenericStruct.MetaID(PluginName="MAL", id=str(id))
        PureAnime.id.list.append(MetaID)

        Name = GenericStruct.Text(Text=title, Localization=DefaultLocalization)
        PureAnime.names.list.append(Name)

        Medium_Image = GenericStruct.Image(url=medium_picture)
        Large_Image = GenericStruct.Image(url=large_picture)
        # Todo: save the images as well, need to develop new cache
        PureAnime.images.list.append(Medium_Image)
        PureAnime.images.list.append(Large_Image)

        State_Mapper = {
            'watching': AnimeStruct.LibraryState.Watching,
            'completed': AnimeStruct.LibraryState.Completed,
            'on_hold': AnimeStruct.LibraryState.Hold,
            'dropped': AnimeStruct.LibraryState.Dropped,
            'plan_to_watch': AnimeStruct.LibraryState.PlanToWatch
        }
        updated_at_datetime = datetime.datetime.fromisoformat(updated_at)
        PureAnime.libraryStatus = AnimeStruct.LibraryStatus(state=State_Mapper[status],
                                                            episodesWatched=num_episodes_watched,
                                                            lastUpdated=updated_at_datetime)

        PureAnime.personalRating.rated = score

        AnimeLists.append(anime=PureAnime)
        completedList += 1
        print(f"Formatted {completedList} of {size_list}")

    return AnimeLists

def AnimeMetadata(metadata, oldAnime: AnimeStruct.Anime) -> AnimeStruct.Anime:
    Anime = AnimeStruct.Anime()
    Anime.hash = oldAnime.hash

    id: str = str(metadata.get("id"))
    title: str = metadata.get("title")
    main_picture: dict = metadata.get("main_picture")
    medium_picture: str = main_picture.get("medium")
    large_picture: str = main_picture.get("large")
    alternative_titles: dict = metadata.get("alternative_titles")
    synonyms: List[str] = alternative_titles.pop("synonyms")
    start_date: str = metadata.get("start_date")
    end_date: str = metadata.get("end_date")
    synopsis: str = metadata.get("synopsis")
    mean: float = float(metadata.get("mean", 0))
    rank: int = int(metadata.get("rank", 0))
    popularity: int = int(metadata.get("popularity"))
    num_list_users: str = metadata.get("num_list_users")
    num_scoring_users: str = metadata.get("num_scoring_users")
    nsfw: str = metadata.get("nsfw")
    created_at: str = metadata.get("created_at")
    updated_at: str = metadata.get("updated_at")
    media_type: str = metadata.get("media_type")
    status: str = metadata.get("status")
    genres: List[dict] = metadata.get("genres")
    my_list_status: dict = metadata.get("my_list_status")
    list_status: str = my_list_status.get("status")
    score: float = float(my_list_status.get("score"))
    num_episodes_watched: int = int(my_list_status.get("num_episodes_watched"))
    is_rewatching: bool = bool(my_list_status.get("is_rewatching"))
    updated_at: str = my_list_status.get("updated_at")
    num_episodes: int = int(metadata.get("num_episodes"))
    start_season: dict = metadata.get("start_season")
    if start_season:
        year: int = int(start_season.get("year"))
        season: str = start_season.get("season")
    broadcast: dict = metadata.get("broadcast")
    if broadcast:
        day_of_the_week: str = broadcast.get("day_of_the_week")
        start_time: str = broadcast.get("start_time")
    source: str = metadata.get("source")
    average_episode_duration: str = str(metadata.get("average_episode_duration"))
    rating: str = str(metadata.get("rating"))
    pictures: List[dict] = metadata.get("pictures")
    background: str = metadata.get("background")
    related_anime: List = metadata.get("related_anime")  # Todo: get more info on this
    related_manga: List = metadata.get("related_manga")
    recommendations: List[dict] = metadata.get("recommendations")  # Note To Self: I'm ignoring this for now
    studios: List[dict] = metadata.get("studios")
    statistics: dict = metadata.get("statistics")
    statistics_status: dict = statistics.get("status")
    watching: str = statistics_status.get("watching")
    completed: str = statistics_status.get("completed")
    on_hold: str = statistics_status.get("on_hold")
    dropped: str = statistics_status.get("dropped")
    plan_to_watch: str = statistics_status.get("plan_to_watch")
    num_list_users: str = str(statistics_status.get("num_list_users"))


    if nsfw != "white" and nsfw !="gray" :
        raise Exception("First time seeing Non White, pls help")
    ageRatingDict = {"pg_13": 13}
    Anime.ageRating = AnimeStruct.AgeRating(Age=ageRatingDict["pg_13"], Tag=rating)

    status_dict: AnimeStruct.ReleaseStatus = {"currently_airing": AnimeStruct.ReleaseStatus.ONGOING,
                                              "not_yet_aired": AnimeStruct.ReleaseStatus.SCHEDULED,
                                              "finished_airing": AnimeStruct.ReleaseStatus.COMPLETED}
    Anime.status = status_dict[status]

    Anime.publicRating = AnimeStruct.Rating(rated=mean, rank=rank, popularity=popularity)
    Anime.publicRating.hash = oldAnime.publicRating.hash


    libraryState_dict: AnimeStruct.LibraryState = {"watching": AnimeStruct.LibraryState.Watching,
                                                   "on_hold": AnimeStruct.LibraryState.Hold,
                                                   "dropped": AnimeStruct.LibraryState.Dropped,
                                                   "plan_to_watch": AnimeStruct.LibraryState.PlanToWatch,
                                                   "completed": AnimeStruct.LibraryState.Completed}
    Anime.libraryStatus = AnimeStruct.LibraryStatus(state=libraryState_dict[list_status],
                                                    episodesWatched=num_episodes_watched,
                                                    lastUpdated=datetime.datetime.fromisoformat(updated_at))
    Anime.libraryStatus.hash = oldAnime.libraryStatus.hash


    Anime.personalRating = AnimeStruct.Rating(rated=score)
    Anime.personalRating.hash = oldAnime.personalRating.hash

    # Todo: add new id if the metadata provider differs from the initial id provider
    Anime.id = oldAnime.id

    # Todo: maybe add a script_Dic to map languages to script (Latin, japanese only)
    names = AnimeStruct.Names()
    Name = GenericStruct.Text(Text=title, Localization=DefaultLocalization)
    names.list.append(Name)
    for language in alternative_titles:
        title = alternative_titles[language]
        Country = "Unknown"
        Language = pycountry.languages.get(alpha_2=language).name
        Script = "Unknown"
        Localization = GenericStruct.Localization(Language=Language,
                                                  Script=Script)
        Name = GenericStruct.Text(Text=title, Localization=DefaultLocalization)
        names.list.append(Name)
    for title in synonyms:
        Language = "Unknown"
        Script = "Unknown"
        Localization = GenericStruct.Localization(Language=Language,
                                                  Script=Script)
        Name = GenericStruct.Text(Text=title, Localization=DefaultLocalization)
        names.list.append(Name)
    Anime.names = names
    Anime.names.hash = oldAnime.names.hash

    images = AnimeStruct.Images()
    if medium_picture:
        Medium_Image = GenericStruct.Image(url=medium_picture)
        images.list.append(Medium_Image)
    if large_picture:
        Large_Image = GenericStruct.Image(url=large_picture)
        images.list.append(Large_Image)
    for image_info in pictures:
        Medium_Image = GenericStruct.Image(url=image_info.get("medium"))
        if Medium_Image:
            images.list.append(Medium_Image)
        Large_Image = GenericStruct.Image(url=image_info.get("large"))
        if Large_Image:
            images.list.append(Large_Image)
    Anime.images = images
    Anime.images.hash = oldAnime.images.hash

    tags = AnimeStruct.Tags()
    # Todo: See if exists in database a tag with same name but different aliases
    tags.list = [AnimeStruct.Tag(name=genre.get("name")) for genre in genres]
    Anime.tags = tags
    Anime.tags.hash = oldAnime.tags.hash

    Anime.description = AnimeStruct.Description(synopsis)
    Anime.description.hash = oldAnime.description.hash

    typeDict = {"tv": AnimeStruct.AnimeType.TV,
                "ona": AnimeStruct.AnimeType.ONA,
                "ova": AnimeStruct.AnimeType.OVA,
                "special": AnimeStruct.AnimeType.SPECIAL,
                "unknown": AnimeStruct.AnimeType.UNKNOWN,
                "movie": AnimeStruct.AnimeType.MOVIE}
    Anime.type = typeDict[media_type]

    # episodes = AnimeStruct.Episodes()
    # for episode_number in range(num_episodes):
    #     text = AnimeStruct.Text("Unknown", DefaultLocalization)
    #     names = AnimeStruct.Names()
    #     names.list.append(text)
    #     episode = AnimeStruct.Episode(names=names)
    #     episode.type = AnimeStruct.EpisodeType.UNKNOWN
    #     episodes.list.append(episode)
    # Anime.episodes = episodes
    # Anime.episodes.hash = oldAnime.episodes.hash

    runnings = AnimeStruct.Runnings()
    since = to = None
    strpTypeDict = {1: "%Y", 2: "%Y-%m", 3: "%Y-%m-%d"}
    if start_date:
        strptype = len(start_date.split("-"))
        since = datetime.datetime.strptime(start_date, strpTypeDict[strptype])
    if end_date:
        strptype = len(end_date.split("-"))
        to = datetime.datetime.strptime(end_date, strpTypeDict[strptype])
    runnings.list.append(AnimeStruct.Running(since=since, to=to))
    Anime.runnings = runnings
    Anime.runnings.hash = oldAnime.runnings.hash

    seasonDict = {"winter": AnimeStruct.Seasons.Winter,
                  "spring": AnimeStruct.Seasons.Spring,
                  "summer": AnimeStruct.Seasons.Summer,
                  "fall": AnimeStruct.Seasons.Fall}

    if start_season:
        Anime.season = AnimeStruct.Season(Year=AnimeStruct.Year(year), SeasonName=seasonDict[season])

    studioss = AnimeStruct.Studios()
    for studio in studios:
        name = studio.get("name")
        names = AnimeStruct.Names()
        names.list.append(AnimeStruct.Text(Text=name, Localization=DefaultLocalization))
        studioss.list.append(AnimeStruct.Studio(names))
    Anime.studios = studioss
    Anime.studios.hash = oldAnime.studios.hash

    return Anime
