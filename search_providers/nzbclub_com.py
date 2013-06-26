#!/usr/bin/env python

import feedparser
import urllib
import os
from time import mktime
from datetime import datetime
import pprint
from Util import U


class Provider (object):

    provider_url = 'http://www.nzbclub.com/'
    name = 'NZBClub'


    def search(self, search_string):

        '''
        Default Search: Our default is prefix match
        Search 123 will match 123, 1234, 1234abcdefg
        Search 123 will not match 0123, ab123, ab123yz

        AND search:
        -----------
        the words hello and world:
        hello world

        NOT search:
        -----------
        the word hello but NOT the word world:
        hello -world

        We can't do NOT only search
        -world

        OR search:
        ----------
        the words hello or world:
        hello or world

        Each "or" is treated as new query part
        hello abcd or hello efgh != hello abcd or efgh

        grouping:
        ---------
        the exact phrase hello world:
        "hello world"
        '''

        url = 'http://www.nzbclub.com/nzbfeed.aspx?'
        query = {
            'q': search_string
            , 'ig': 2       # hide adult: 1=yes, 2=no
            , 'szs': 15     # min size: 15=75m, 16=100m,
            , 'sze': 24     # max size: 24=2gig
            , 'st': 5       # sort.  5=relevence, 4=size (smallest first)
            , 'ns': 1       # no spam
            , 'sp': 1       # don't show passworded files
            , 'nfo': 0      # has to have nfo  1=yes, 0=no
            }
        full_url = url + urllib.urlencode (query)
        parsed = feedparser.parse(full_url)

        header = [['Name', 'Date', 'Size'],
                  [0, 12, 10],
                  ['<', '<', '>']]

        show_data = []
        for show in parsed['entries']:

            dt = datetime.fromtimestamp(mktime(show['published_parsed']))
            date = dt.strftime('%b %d/%Y')

            size = U.pretty_filesize (show['links'][0]['length'])

            show_data.append([
                show['title'],
                date,
                size,
                show['links'][0]['href'] # id
                ])

        return [header] + [show_data]


    def download (self, chosen_show, destination, final_name):
        '''

        '''

        if not os.path.isdir (destination):
            raise ProviderError ('%s is not a dir' % (dest))

        href = chosen_show
        filename = href.split('/')[-1]
        if final_name:
            # final_name should be a name that SABNzbd can parse
            # if this is being used, it means that this download is
            # a tv show with a season and episode.
            fullname = destination + '/' + final_name
        else:
            # if NOT final_name, then this download came from
            # nondbshow, and is not associated with a tv show.
            # Could be a movie or one off download.
            fullname = destination + '/' + filename

        urllib.urlretrieve(href, fullname)

        return filename

if __name__ == '__main__':

    pass
