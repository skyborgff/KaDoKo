import calendar
from cachecontrol.heuristics import BaseHeuristic
from datetime import datetime, timedelta
from email.utils import parsedate, formatdate


#   Todo: Cache images for a month, cache anime for a day, cache user for 10 seconds


class MALHeuristic(BaseHeuristic):

    def update_headers(self, response):
        date = parsedate(response.headers['date'])
        expires = datetime(*date[:6]) + timedelta(weeks=1)
        return {
            'expires' : formatdate(calendar.timegm(expires.timetuple())),
            'cache-control' : 'public',
        }

    def warning(self, response):
        msg = 'Automatically cached! Response is Stale.'
        return '110 - "%s"' % msg