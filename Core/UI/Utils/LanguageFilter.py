import Core.Structures.Anime as Anime

def LanguageFilter(settings: dict, list) -> list:
    ordered = []
    for local in settings:
        for text in list:
            if local.get('tag', '') == text.Localization.Tag:
                ordered.append(text.Text)
    return ordered