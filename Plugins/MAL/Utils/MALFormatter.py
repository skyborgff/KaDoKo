from typing import List
import pycountry
import datetime
import Core.Structures.List as AnimeListsStruct
import Core.Structures.Anime as AnimeStruct
import Core.Structures.Generic as GenericStruct

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

        DefaultCountry = 'Japan'
        DefaultLanguage = "Japanese"
        DefaultScript = 'Latin'
        DefaultLocalization = GenericStruct.Localization(Country=DefaultCountry,
                                                         Language=DefaultLanguage,
                                                         Script=DefaultScript)
        Name = GenericStruct.Text(Text=title, Localization=DefaultLocalization)
        PureAnime.names.list.append(Name)

        Medim_Image = GenericStruct.Image(url=medium_picture)
        Large_Image = GenericStruct.Image(url=large_picture)
        # Todo: save the images as well, need to develop new cache
        PureAnime.images.list.append(Medim_Image)
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