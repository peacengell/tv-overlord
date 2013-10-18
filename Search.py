#!/usr/bin/env python

import sys
from Util import U
from subprocess import call
from subprocess import Popen
import os
import platform

from tv_config import config


class SearchError (Exception):

    def __init__ (self, value):
        self.value = value

    def __str__ (self):
        return repr(self.value)


class Search (object):

    def __init__(self, provider):

        mod_name = 'search_providers.' + provider
        mod = __import__(mod_name, fromlist=["Provider"])
        engine = getattr (mod, 'Provider')
        self.engine = engine()

        self.season = ''
        self.episode = ''
        self.show_name = ''


    def search(self, search_string, season=False,
               episode=False):
        '''
        Return an array of values:

        [
          [
            [head1, head2, head3, id],
            [head1-width, head2-width, head3-width],
            [head1-alignment, head1-alignment, head1-alignment]
          ],
          [data from search...]
        ]
        '''

        self.season = season
        self.episode = episode
        self.show_name = search_string

        msg = 'Searching for: %s...' % (search_string)
        msg = U.hi_color (msg, foreground=16, background=184)
        sys.stdout.write (msg)
        sys.stdout.flush()
        backspace = '\b' * len (msg)
        overwrite = ' ' * len (msg)

        search_results = self.engine.search(search_string, season, episode)

        print '%s%s' % (backspace, overwrite)

        return search_results


    def download(self, chosen_show, destination):
        '''
        Pass the chosen show's data and destination to the providers
        download method and return the name of the file downloaded
        back to get-nzb.v2.py
        '''

        downloaded_filename = ''
        if chosen_show.startswith("magnet:"):

            if platform.system() == 'Linux':
                # gvfs-... are the Gnome tools for interacting with
                # the file system.  Use KIO for kde.
                # gvfs-open will open whatever application is associated
                # with magnet links.
                desktop = os.environ.get('DESKTOP_SESSION')
                if desktop == "gnome":
                    Popen (["gvfs-open", chosen_show])
                elif desktop == 'kde':
                    Popen (["kioclient", chosen_show])
                elif desktop == 'ubuntu':
                    Popen (['xdg-open', chosen_show])
                else:
                    unknown_enviroment = os.environ.get('DESKTOP_SESSION')
                    print 'Unknown enviroment:', unknown_enviroment
            elif platform.system() == 'Darwin':
                Popen (["open", chosen_show])
            else:
                unknown_system = platform.platform()
                print 'Unknown system:', unknown_system
                exit()


        else:       # is a nzb file
            final_name = ''
            # only cleans name for tv show downloads
            if self.season and self.episode:
                final_name = '%s.%s.nzb' % (
                    self.show_name.replace(' ', '.'),
                    "S%sE%s" % (self.season.rjust(2, '0'), self.episode.rjust(2, '0'))
                )
                print final_name
            downloaded_filename = self.engine.download (
                chosen_show, destination, final_name)

        return downloaded_filename


if __name__ == '__main__':

    test = Search ('nzbindex')
    test = Search ('NZBIndex')
    test = Search('x')