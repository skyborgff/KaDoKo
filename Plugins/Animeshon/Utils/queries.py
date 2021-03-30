queryCrossReference = '''
{{
  queryCrossReference(
    filter: {{externalID: {{eq: "{externalID}"}}, 
      namespace: {{eq: "{namespace}"}},
    	kind: {{eq: "Anime"}}}}, 
    first: 1
  )
  {{
    resource{{
      ...on Anime{{
        id
        crossrefs{{
          namespace
          externalID
          partial
        }}
      }}
    }}
  }}
}}
'''

# Note To Self: Soundtracks and canonicals missing query, need examples
# Note To Self: had to remove aliases as AhKlxpHx7Xl_ was giving problems
getAnime = '''
{{
  getAnime(id: "{AnimeshonID}") 
  {{
  id
  restrictions{{
    selfLink
    country{{alpha2}}
    type
    tag
  }}
  releases{{
    languages{{alpha2}}
    releaseDate
    media{{
      type
      quantity
    }}
    censorship
  }}
  ageRatings{{
    age
    tag
  }}
  status
  relations{{
    type
    object{{
      ...on Anime{{
        id
          crossrefs{{
          kind
          externalID
          namespace
          website{{formattedAddress}}
        }}
      }}
    }}
  }}
  partOfCanonicals{{
    id
  }}
  genres{{
    names{{
      text
    }}
    descriptions{{
      text
    }}
  }}
  soundtracks{{
    id
  }}
  voiceActings{{
    voiced{{
      ...on Character{{
        id
        birthday
        hometown{{country{{alpha2}}}}
        gender
        age
        names{{
          text
          localization{{
            tag
          }}
        }}
      }}
    }}
    actor{{
      id
      birthday
      hometown{{country{{alpha2}}}}
      gender
      age
      names{{
        text
        localization{{
          tag
        }}
      }}
    }}
    isPrimary
    localization{{
      tag
    }}
  }}
  staff{{
    id
    collaborator{{
      ...on Person{{
        id
        birthday
        hometown{{country{{alpha2}}}}
        gender
        age
        names{{
          text
          localization{{
            tag
          }}
        }}
      }}
      ...on Circle{{
        id
      }}
      ...on Organization{{
        names{{
          text
            localization{{
            tag
          }}
        }}
      }}
      ...on Magazine{{
          names{{
          text
            localization{{
            tag
          }}
        }}
      }}
    }}
    role{{
      ...on TypedRole{{
        type
      }}
      ...on FreeTextRole{{
        tag
      }}
    }}
    
  }}
  starring{{
    relation
    character{{
      # implement a second call?
      id
      birthday
      hometown{{country{{alpha2}}}}
      gender
      age
      names{{
        text
        localization{{
          tag
        }}
      }}
    }}
  }}
  names{{
    text
    localization{{
      tag
    }}
  }}
  descriptions{{
    text
    localization{{
      tag
    }}
  }}
  images{{
    type
    image{{
      files{{publicUri}}
      # width
      # height
    }}
  }}
  crossrefs{{
    kind
    externalID
    namespace
    website{{formattedAddress}}
  }}
  websites{{
   host{{domain}}
   formattedAddress
  }}
  id
  selfLink
  type
  videos{{
    type
    video{{
      files{{publicUri}}
      # width
      # height
      # duration
    }}
  }}
  episodes{{
    type
    identifier
    releaseDate
    names{{
      text
      localization{{
        tag
      }}
    }}
    ageRatings{{
      age
      tag
    }}
    websites{{
      host{{domain}}
      formattedAddress
    }}
    videos{{
      type
      video{{
        files{{publicUri}}
        # width
        # height
        # duration
      }}
    }}
  }}
  runnings{{
    from
    to
  }}
  }}
}}
'''