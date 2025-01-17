# -*- coding: utf-8 -*-

'''
    Genesis XBMC Addon
    Copyright (C) 2014 lambda

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import urllib,urllib2,re,os,threading,datetime,time,base64,xbmc,xbmcplugin,xbmcgui,xbmcaddon,xbmcvfs
from operator import itemgetter
try:    import json
except: import simplejson as json
try:    from sqlite3 import dbapi2 as database
except: from pysqlite2 import dbapi2 as database
try:    import CommonFunctions
except: import commonfunctionsdummy as CommonFunctions
try:    import StorageServer
except: import storageserverdummy as StorageServer
from metahandler import metahandlers


action              = None
common              = CommonFunctions
metaget             = metahandlers.MetaData(preparezip=False)
language            = xbmcaddon.Addon().getLocalizedString
setSetting          = xbmcaddon.Addon().setSetting
getSetting          = xbmcaddon.Addon().getSetting
addonName           = xbmcaddon.Addon().getAddonInfo("name")
addonVersion        = xbmcaddon.Addon().getAddonInfo("version")
addonId             = xbmcaddon.Addon().getAddonInfo("id")
addonPath           = xbmcaddon.Addon().getAddonInfo("path")
addonFullId         = addonName + addonVersion
addonDesc           = language(30450).encode("utf-8")
dataPath            = xbmc.translatePath(xbmcaddon.Addon().getAddonInfo("profile")).decode("utf-8")
cache               = StorageServer.StorageServer(addonFullId,1).cacheFunction
cache2              = StorageServer.StorageServer(addonFullId,24).cacheFunction
cache3              = StorageServer.StorageServer(addonFullId,720).cacheFunction
movieLibrary        = os.path.join(xbmc.translatePath(getSetting("movie_library")),'')
tvLibrary           = os.path.join(xbmc.translatePath(getSetting("tv_library")),'')
PseudoTV            = xbmcgui.Window(10000).getProperty('PseudoTVRunning')
addonLogos          = os.path.join(addonPath,'resources/logos')
addonSettings       = os.path.join(dataPath,'settings.db')
addonCache          = os.path.join(dataPath,'cache.db')


class main:
    def __init__(self):
        global action
        index().container_data()
        index().settings_reset()
        params = {}
        splitparams = sys.argv[2][sys.argv[2].find('?') + 1:].split('&')
        for param in splitparams:
            if (len(param) > 0):
                splitparam = param.split('=')
                key = splitparam[0]
                try:    value = splitparam[1].encode("utf-8")
                except: value = splitparam[1]
                params[key] = value

        try:        action = urllib.unquote_plus(params["action"])
        except:     action = None
        try:        name = urllib.unquote_plus(params["name"])
        except:     name = None
        try:        title = urllib.unquote_plus(params["title"])
        except:     title = None
        try:        year = urllib.unquote_plus(params["year"])
        except:     year = None
        try:        imdb = urllib.unquote_plus(params["imdb"])
        except:     imdb = None
        try:        tvdb = urllib.unquote_plus(params["tvdb"])
        except:     tvdb = None
        try:        season = urllib.unquote_plus(params["season"])
        except:     season = None
        try:        episode = urllib.unquote_plus(params["episode"])
        except:     episode = None
        try:        show = urllib.unquote_plus(params["show"])
        except:     show = None
        try:        show_alt = urllib.unquote_plus(params["show_alt"])
        except:     show_alt = None
        try:        date = urllib.unquote_plus(params["date"])
        except:     date = None
        try:        genre = urllib.unquote_plus(params["genre"])
        except:     genre = None
        try:        url = urllib.unquote_plus(params["url"])
        except:     url = None
        try:        image = urllib.unquote_plus(params["image"])
        except:     image = None
        try:        meta = urllib.unquote_plus(params["meta"])
        except:     meta = None
        try:        query = urllib.unquote_plus(params["query"])
        except:     query = None
        try:        source = urllib.unquote_plus(params["source"])
        except:     source = None
        try:        provider = urllib.unquote_plus(params["provider"])
        except:     provider = None

        if action == None:                            root().get()
        elif action == 'root_movies':                 root().movies()
        elif action == 'root_shows':                  root().shows()
        elif action == 'root_genesis':                root().genesis()
        elif action == 'root_tools':                  root().tools()
        elif action == 'root_search':                 root().search()
        elif action == 'item_queue':                  contextMenu().item_queue()
        elif action == 'view_movies':                 contextMenu().view('movies')
        elif action == 'view_tvshows':                contextMenu().view('tvshows')
        elif action == 'view_seasons':                contextMenu().view('seasons')
        elif action == 'view_episodes':               contextMenu().view('episodes')
        elif action == 'cache_clear':                 contextMenu().cache_clear()
        elif action == 'playlist_open':               contextMenu().playlist_open()
        elif action == 'settings_open':               contextMenu().settings_open()
        elif action == 'settings_urlresolver':        contextMenu().settings_open('script.module.urlresolver')
        elif action == 'settings_metahandler':        contextMenu().settings_open('script.module.metahandler')
        elif action == 'favourite_movie_add':         contextMenu().favourite_add('Movie', imdb, name, year, image, refresh=True)
        elif action == 'favourite_movie_from_search': contextMenu().favourite_add('Movie', imdb, name, year, image)
        elif action == 'favourite_tv_add':            contextMenu().favourite_add('TV Show', imdb, name, year, image, refresh=True)
        elif action == 'favourite_tv_from_search':    contextMenu().favourite_add('TV Show', imdb, name, year, image)
        elif action == 'favourite_delete':            contextMenu().favourite_delete(imdb)
        elif action == 'indicator_service':           contextMenu().trakt_indicator()
        elif action == 'trakt_manager':               contextMenu().trakt_manager('movie', name, imdb)
        elif action == 'trakt_tv_manager':            contextMenu().trakt_manager('show', name, imdb)
        elif action == 'watched_movies':              contextMenu().playcount_movies(title, year, imdb, 7)
        elif action == 'unwatched_movies':            contextMenu().playcount_movies(title, year, imdb, 6)
        elif action == 'watched_episodes':            contextMenu().playcount_episodes(imdb, season, episode, 7)
        elif action == 'unwatched_episodes':          contextMenu().playcount_episodes(imdb, season, episode, 6)
        elif action == 'watched_shows':               contextMenu().playcount_shows(name, year, imdb, tvdb, '', 7)
        elif action == 'unwatched_shows':             contextMenu().playcount_shows(name, year, imdb, tvdb, '', 6)
        elif action == 'watched_seasons':             contextMenu().playcount_shows(name, year, imdb, tvdb, season, 7)
        elif action == 'unwatched_seasons':           contextMenu().playcount_shows(name, year, imdb, tvdb, season, 6)
        elif action == 'library_movie_add':           contextMenu().library_movie_add(name, title, year, imdb, url)
        elif action == 'library_movie_list':          contextMenu().library_movie_list(url)
        elif action == 'library_tv_add':              contextMenu().library_tv_add(name, year, imdb, tvdb)
        elif action == 'library_tv_list':             contextMenu().library_tv_list(url)
        elif action == 'library_update':              contextMenu().library_update()
        elif action == 'library_service':             contextMenu().library_update(silent=True)
        elif action == 'library_trakt_collection':    contextMenu().library_movie_list('trakt_collection')
        elif action == 'library_trakt_watchlist':     contextMenu().library_movie_list('trakt_watchlist')
        elif action == 'library_imdb_watchlist':      contextMenu().library_movie_list('imdb_watchlist')
        elif action == 'library_tv_trakt_collection': contextMenu().library_tv_list('trakt_tv_collection')
        elif action == 'library_tv_trakt_watchlist':  contextMenu().library_tv_list('trakt_tv_watchlist')
        elif action == 'library_tv_imdb_watchlist':   contextMenu().library_tv_list('imdb_tv_watchlist')
        elif action == 'toggle_movie_playback':       contextMenu().toggle_playback('movie', name, title, year, imdb, '', '', '', '', '', '', '')
        elif action == 'toggle_episode_playback':     contextMenu().toggle_playback('episode', name, title, year, imdb, tvdb, season, episode, show, show_alt, date, genre)
        elif action == 'download':                    contextMenu().download(name, url, provider)
        elif action == 'trailer':                     contextMenu().trailer(name, url)
        elif action == 'movies':                      movies().get(url)
        elif action == 'movies_userlist':             movies().get(url)
        elif action == 'movies_popular':              movies().popular()
        elif action == 'movies_boxoffice':            movies().boxoffice()
        elif action == 'movies_views':                movies().views()
        elif action == 'movies_oscars':               movies().oscars()
        elif action == 'movies_added':                movies().added()
        elif action == 'movies_theaters':             movies().theaters()
        elif action == 'movies_trending':             movies().trending()
        elif action == 'movies_trakt_collection':     movies().trakt_collection()
        elif action == 'movies_trakt_watchlist':      movies().trakt_watchlist()
        elif action == 'movies_imdb_watchlist':       movies().imdb_watchlist()
        elif action == 'movies_search':               movies().search(query)
        elif action == 'movies_favourites':           movies().favourites()
        elif action == 'shows':                       shows().get(url)
        elif action == 'shows_userlist':              shows().get(url)
        elif action == 'shows_popular':               shows().popular()
        elif action == 'shows_rating':                shows().rating()
        elif action == 'shows_views':                 shows().views()
        elif action == 'shows_active':                shows().active()
        elif action == 'shows_trending':              shows().trending()
        elif action == 'shows_trakt_collection':      shows().trakt_collection()
        elif action == 'shows_trakt_watchlist':       shows().trakt_watchlist()
        elif action == 'shows_imdb_watchlist':        shows().imdb_watchlist()
        elif action == 'shows_search':                shows().search(query)
        elif action == 'shows_favourites':            shows().favourites()
        elif action == 'seasons':                     seasons().get(show, year, imdb, tvdb)
        elif action == 'episodes':                    episodes().get(show, year, imdb, tvdb, season)
        elif action == 'episodes_added':              episodes().added()
        elif action == 'episodes_calendar':           episodes().calendar(url)
        elif action == 'actors_movies':               actors().movies(query)
        elif action == 'actors_shows':                actors().shows(query)
        elif action == 'genres_movies':               genres().movies()
        elif action == 'genres_shows':                genres().shows()
        elif action == 'languages_movies':            languages().movies()
        elif action == 'years_movies':                years().movies()
        elif action == 'calendar_episodes':           calendar().episodes()
        elif action == 'channels_movies':             channels().movies()
        elif action == 'userlists_movies':            userlists().movies()
        elif action == 'userlists_shows':             userlists().shows()
        elif action == 'get_host':                    resolver().get_host(name, title, year, imdb, tvdb, season, episode, show, show_alt, date, genre, url, meta)
        elif action == 'play_moviehost':              resolver().play_host('movie', name, imdb, url, source, provider)
        elif action == 'play_tvhost':                 resolver().play_host('episode', name, imdb, url, source, provider)
        elif action == 'play':                        resolver().run(name, title, year, imdb, tvdb, season, episode, show, show_alt, date, genre, url)

class getUrl(object):
    def __init__(self, url, close=True, proxy=None, post=None, mobile=False, referer=None, cookie=None, output='', timeout='5'):
        if not proxy == None:
            proxy_handler = urllib2.ProxyHandler({'http':'%s' % (proxy)})
            opener = urllib2.build_opener(proxy_handler, urllib2.HTTPHandler)
            opener = urllib2.install_opener(opener)
        if output == 'cookie' or not close == True:
            import cookielib
            cookie_handler = urllib2.HTTPCookieProcessor(cookielib.LWPCookieJar())
            opener = urllib2.build_opener(cookie_handler, urllib2.HTTPBasicAuthHandler(), urllib2.HTTPHandler())
            opener = urllib2.install_opener(opener)
        if not post == None:
            request = urllib2.Request(url, post)
        else:
            request = urllib2.Request(url,None)
        if mobile == True:
            request.add_header('User-Agent', 'Mozilla/5.0 (iPhone; CPU; CPU iPhone OS 4_0 like Mac OS X; en-us) AppleWebKit/532.9 (KHTML, like Gecko) Version/4.0.5 Mobile/8A293 Safari/6531.22.7')
        else:
            request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.57 Safari/537.36')
        if not referer == None:
            request.add_header('Referer', referer)
        if not cookie == None:
            request.add_header('cookie', cookie)
        response = urllib2.urlopen(request, timeout=int(timeout))
        if output == 'cookie':
            result = str(response.headers.get('Set-Cookie'))
        elif output == 'geturl':
            result = response.geturl()
        else:
            result = response.read()
        if close == True:
            response.close()
        self.result = result

class uniqueList(object):
    def __init__(self, list):
        uniqueSet = set()
        uniqueList = []
        for n in list:
            if n not in uniqueSet:
                uniqueSet.add(n)
                uniqueList.append(n)
        self.list = uniqueList

class Thread(threading.Thread):
    def __init__(self, target, *args):
        self._target = target
        self._args = args
        threading.Thread.__init__(self)
    def run(self):
        self._target(*self._args)

class player(xbmc.Player):
    def __init__ (self):
        self.folderPath = xbmc.getInfoLabel('Container.FolderPath')
        self.loadingStarting = time.time()
        xbmc.Player.__init__(self)

    def run(self, content, name, url, imdb='0'):
        self.video_info(content, name, imdb)

        if self.folderPath.startswith(sys.argv[0]) or PseudoTV == 'True':
            item = xbmcgui.ListItem(path=url)
            xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)
        else:
            try:
                if self.content == 'movie':
                    meta = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.GetMovies", "params": {"filter":{"or": [{"field": "year", "operator": "is", "value": "%s"}, {"field": "year", "operator": "is", "value": "%s"}, {"field": "year", "operator": "is", "value": "%s"}]}, "properties" : ["title", "originaltitle", "year", "genre", "studio", "country", "runtime", "rating", "votes", "mpaa", "director", "writer", "plot", "plotoutline", "tagline", "thumbnail", "file"]}, "id": 1}' % (self.year, str(int(self.year)+1), str(int(self.year)-1)))
                    meta = unicode(meta, 'utf-8', errors='ignore')
                    meta = json.loads(meta)['result']['movies']
                    self.meta = [i for i in meta if i['file'].endswith(self.file)][0]

                    meta = {'title': self.meta['title'], 'originaltitle': self.meta['originaltitle'], 'year': self.meta['year'], 'genre': str(" / ".join(self.meta['genre'])), 'studio' : str(" / ".join(self.meta['studio'])), 'country' : str(" / ".join(self.meta['country'])), 'duration' : self.meta['runtime'], 'rating': self.meta['rating'], 'votes': self.meta['votes'], 'mpaa': self.meta['mpaa'], 'director': str(" / ".join(self.meta['director'])), 'writer': str(" / ".join(self.meta['writer'])), 'plot': self.meta['plot'], 'plotoutline': self.meta['plotoutline'], 'tagline': self.meta['tagline']}

                    thumb = self.meta['thumbnail']
                    poster = thumb

                elif self.content == 'episode':
                    meta = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.GetEpisodes", "params": {"filter":{"and": [{"field": "season", "operator": "is", "value": "%s"}, {"field": "episode", "operator": "is", "value": "%s"}]}, "properties": ["title", "season", "episode", "showtitle", "firstaired", "runtime", "rating", "director", "writer", "plot", "thumbnail", "file"]}, "id": 1}' % (self.season, self.episode))
                    meta = unicode(meta, 'utf-8', errors='ignore')
                    meta = json.loads(meta)['result']['episodes']
                    self.meta = [i for i in meta if i['file'].endswith(self.file)][0]

                    meta = {'title': self.meta['title'], 'season' : self.meta['season'], 'episode': self.meta['episode'], 'tvshowtitle': self.meta['showtitle'], 'premiered' : self.meta['firstaired'], 'duration' : self.meta['runtime'], 'rating': self.meta['rating'], 'director': str(" / ".join(self.meta['director'])), 'writer': str(" / ".join(self.meta['writer'])), 'plot': self.meta['plot']}

                    thumb = self.meta['thumbnail']

                    poster = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.GetTVShows", "params": {"filter": {"field": "title", "operator": "is", "value": "%s"}, "properties": ["thumbnail"]}, "id": 1}' % self.meta['showtitle'])
                    poster = unicode(poster, 'utf-8', errors='ignore')
                    poster = json.loads(poster)['result']['tvshows'][0]['thumbnail']

            except:
                poster, thumb, meta = '', '', {'title': self.name}

            item = xbmcgui.ListItem(path=url, iconImage="DefaultVideo.png", thumbnailImage=thumb)
            try: item.setArt({'poster': poster, 'tvshow.poster': poster, 'season.poster': poster})
            except: pass
            item.setInfo(type="Video", infoLabels = meta)
            xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)

        for i in range(0, 250):
            try: self.totalTime = self.getTotalTime()
            except: self.totalTime = 0
            if not self.totalTime == 0: continue
            xbmc.sleep(1000)
        if self.totalTime == 0: return

        while True:
            try: self.currentTime = self.getTime()
            except: break
            xbmc.sleep(1000)

    def video_info(self, content, name, imdb):
        self.name = name
        self.content = content
        self.file = self.name + '.strm'
        self.file = self.file.translate(None, '\/:*?"<>|').strip('.')

        if self.content == 'movie':
            self.title = self.name.rsplit(' (', 1)[0].strip()
            self.year = '%04d' % int(self.name.rsplit(' (', 1)[-1].split(')')[0])
            if imdb == '0': imdb = metaget.get_meta('movie', self.title ,year=str(self.year))['imdb_id']
            self.imdb = re.sub('[^0-9]', '', imdb)
            self.subtitle = subtitles().get(self.name, self.imdb, '', '')

        elif self.content == 'episode':
            self.show = self.name.rsplit(' ', 1)[0]
            if imdb == '0': imdb = metaget.get_meta('tvshow', self.show)['imdb_id']
            self.imdb = re.sub('[^0-9]', '', imdb)
            self.season = '%01d' % int(name.rsplit(' ', 1)[-1].split('S')[-1].split('E')[0])
            self.episode = '%01d' % int(name.rsplit(' ', 1)[-1].split('E')[-1])
            self.subtitle = subtitles().get(self.name, self.imdb, self.season, self.episode)

    def resume_add(self):
        try:
            record = (self.name, 'tt' + self.imdb, str(self.currentTime))
            if not xbmcvfs.exists(dataPath): xbmcvfs.mkdir(dataPath)
            dbcon = database.connect(addonSettings)
            dbcur = dbcon.cursor()
            dbcur.execute("CREATE TABLE IF NOT EXISTS points (""name TEXT, ""imdb_id TEXT, ""resume_point TEXT, ""UNIQUE(name, imdb_id)"");")
            dbcur.execute("DELETE FROM points WHERE name = '%s' AND imdb_id = '%s'" % (record[0], record[1]))
            dbcur.execute("INSERT INTO points Values (?, ?, ?)", record)
            dbcon.commit()
        except:
            return

    def resume_delete(self):
        try:
            record = (self.name, 'tt' + self.imdb)
            if not xbmcvfs.exists(dataPath): xbmcvfs.mkdir(dataPath)
            dbcon = database.connect(addonSettings)
            dbcur = dbcon.cursor()
            dbcur.execute("DELETE FROM points WHERE name = '%s' AND imdb_id = '%s'" % (record[0], record[1]))
            dbcon.commit()
        except:
            return

    def resume_read(self):
        try:
            self.offset = '0'
            record = (self.name, 'tt' + self.imdb)
            dbcon = database.connect(addonSettings)
            dbcur = dbcon.cursor()
            dbcur.execute("SELECT * FROM points WHERE name = '%s' AND imdb_id = '%s'" % (record[0], record[1]))
            offset = dbcur.fetchone()
            self.offset = offset[2]
        except:
            return

    def resume_play(self):
        offset = float(self.offset)
        if not offset > 0: return
        minutes, seconds = divmod(offset, 60)
        hours, minutes = divmod(minutes, 60)
        offset_time = '%02d:%02d:%02d' % (hours, minutes, seconds)
        yes = index().yesnoDialog('%s %s' % (language(30348).encode("utf-8"), offset_time), '', self.name, language(30349).encode("utf-8"), language(30350).encode("utf-8"))
        if yes: self.seekTime(offset)

    def change_watched(self):
        if self.content == 'movie':
            try:
                metaget.get_meta('movie', self.title ,year=self.year)
                metaget.change_watched(self.content, '', self.imdb, season='', episode='', year='', watched=7)
            except:
                pass

            try:
                if not getSetting("watched_trakt") == 'true': raise Exception()
                if (link().trakt_user == '' or link().trakt_password == ''): raise Exception()
                imdb = self.imdb
                if not imdb.startswith('tt'): imdb = 'tt' + imdb
                url = 'http://api.trakt.tv/movie/seen/%s' % link().trakt_key
                post = {"movies": [{"imdb_id": imdb}], "username": link().trakt_user, "password": link().trakt_password}
                result = getUrl(url, post=json.dumps(post), timeout='30').result
            except:
                pass

            try:
                if not getSetting("watched_library") == 'true': raise Exception()
                try: movieid = self.meta['movieid']
                except: movieid = ''

                if movieid == '':
                    movieid = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.GetMovies", "params": {"filter":{"or": [{"field": "year", "operator": "is", "value": "%s"}, {"field": "year", "operator": "is", "value": "%s"}, {"field": "year", "operator": "is", "value": "%s"}]}, "properties" : ["file"]}, "id": 1}' % (self.year, str(int(self.year)+1), str(int(self.year)-1)))
                    movieid = unicode(movieid, 'utf-8', errors='ignore')
                    movieid = json.loads(movieid)['result']['movies']
                    movieid = [i for i in movieid if i['file'].endswith(self.file)][0]
                    movieid = movieid['movieid']

                while xbmc.getInfoLabel('Container.FolderPath').startswith(sys.argv[0]) or xbmc.getInfoLabel('Container.FolderPath') == '': xbmc.sleep(1000)
                xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.SetMovieDetails", "params": {"movieid" : %s, "playcount" : 1 }, "id": 1 }' % str(movieid))
            except:
                pass

        elif self.content == 'episode':
            try:
                metaget.get_meta('tvshow', self.show, imdb_id=self.imdb)
                metaget.get_episode_meta(self.show, self.imdb, self.season, self.episode)
                metaget.change_watched(self.content, '', self.imdb, season=self.season, episode=self.episode, year='', watched=7)
            except:
                pass

            try:
                if not getSetting("watched_trakt") == 'true': raise Exception()
                if (link().trakt_user == '' or link().trakt_password == ''): raise Exception()
                imdb = self.imdb
                if not imdb.startswith('tt'): imdb = 'tt' + imdb
                season, episode = int('%01d' % int(self.season)), int('%01d' % int(self.episode))
                url = 'http://api.trakt.tv/show/episode/seen/%s' % link().trakt_key
                post = {"imdb_id": imdb, "episodes": [{"season": season, "episode": episode}], "username": link().trakt_user, "password": link().trakt_password}
                result = getUrl(url, post=json.dumps(post), timeout='30').result
            except:
                pass

            try:
                if not getSetting("watched_library") == 'true': raise Exception()
                try: episodeid = self.meta['episodeid']
                except: episodeid = ''

                if episodeid == '':
                    episodeid = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.GetEpisodes", "params": {"filter":{"and": [{"field": "season", "operator": "is", "value": "%s"}, {"field": "episode", "operator": "is", "value": "%s"}]}, "properties": ["file"]}, "id": 1}' % (self.season, self.episode))
                    episodeid = unicode(episodeid, 'utf-8', errors='ignore')
                    episodeid = json.loads(episodeid)['result']['episodes']
                    episodeid = [i for i in episodeid if i['file'].endswith(self.file)][0]
                    episodeid = episodeid['episodeid']

                while xbmc.getInfoLabel('Container.FolderPath').startswith(sys.argv[0]) or xbmc.getInfoLabel('Container.FolderPath') == '': xbmc.sleep(1000)
                xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.SetEpisodeDetails", "params": {"episodeid" : %s, "playcount" : 1 }, "id": 1 }' % str(episodeid))
            except:
                pass

    def onPlayBackStarted(self):
        try: self.setSubtitles(self.subtitle)
        except: pass

        if PseudoTV == 'True': return

        if getSetting("playback_info") == 'true':
            elapsedTime = '%s %.2f seconds' % (language(30315).encode("utf-8"), (time.time() - self.loadingStarting))     
            index().infoDialog(elapsedTime, header=self.name)

        if getSetting("resume_playback") == 'true':
            self.resume_read()
            self.resume_play()

    def onPlayBackEnded(self):
        if PseudoTV == 'True': return
        self.resume_delete()
        self.change_watched()

    def onPlayBackStopped(self):
        if PseudoTV == 'True': return
        self.resume_delete()
        self.resume_add()
        if self.currentTime / self.totalTime >= .9:
            self.change_watched()

class subtitles:
    def get(self, name, imdb, season, episode):
        if not getSetting("subtitles") == 'true': return
        quality = ['bluray', 'hdrip', 'brrip', 'bdrip', 'dvdrip', 'webrip', 'hdtv']
        langDict = {'Afrikaans': 'afr', 'Albanian': 'alb', 'Arabic': 'ara', 'Armenian': 'arm', 'Basque': 'baq', 'Bengali': 'ben', 'Bosnian': 'bos', 'Breton': 'bre', 'Bulgarian': 'bul', 'Burmese': 'bur', 'Catalan': 'cat', 'Chinese': 'chi', 'Croatian': 'hrv', 'Czech': 'cze', 'Danish': 'dan', 'Dutch': 'dut', 'English': 'eng', 'Esperanto': 'epo', 'Estonian': 'est', 'Finnish': 'fin', 'French': 'fre', 'Galician': 'glg', 'Georgian': 'geo', 'German': 'ger', 'Greek': 'ell', 'Hebrew': 'heb', 'Hindi': 'hin', 'Hungarian': 'hun', 'Icelandic': 'ice', 'Indonesian': 'ind', 'Italian': 'ita', 'Japanese': 'jpn', 'Kazakh': 'kaz', 'Khmer': 'khm', 'Korean': 'kor', 'Latvian': 'lav', 'Lithuanian': 'lit', 'Luxembourgish': 'ltz', 'Macedonian': 'mac', 'Malay': 'may', 'Malayalam': 'mal', 'Manipuri': 'mni', 'Mongolian': 'mon', 'Montenegrin': 'mne', 'Norwegian': 'nor', 'Occitan': 'oci', 'Persian': 'per', 'Polish': 'pol', 'Portuguese': 'por,pob', 'Portuguese(Brazil)': 'pob,por', 'Romanian': 'rum', 'Russian': 'rus', 'Serbian': 'scc', 'Sinhalese': 'sin', 'Slovak': 'slo', 'Slovenian': 'slv', 'Spanish': 'spa', 'Swahili': 'swa', 'Swedish': 'swe', 'Syriac': 'syr', 'Tagalog': 'tgl', 'Tamil': 'tam', 'Telugu': 'tel', 'Thai': 'tha', 'Turkish': 'tur', 'Ukrainian': 'ukr', 'Urdu': 'urd'}

        langs = []
        try: langs.append(langDict[getSetting("sublang1")])
        except: pass
        try: langs.append(langDict[getSetting("sublang2")])
        except: pass
        langs = ','.join(langs)

        try:
            import xmlrpclib
            server = xmlrpclib.Server('http://api.opensubtitles.org/xml-rpc', verbose=0)
            token = server.LogIn('', '', 'en', 'XBMC_Subtitles_v1')['token']
            if not (season == '' or episode == ''): result = server.SearchSubtitles(token, [{'sublanguageid': langs, 'imdbid': imdb, 'season': season, 'episode': episode}])['data']
            else: result = server.SearchSubtitles(token, [{'sublanguageid': langs, 'imdbid': imdb}])['data']
            result = [i for i in result if i['SubSumCD'] == '1']
        except:
            return

        subtitles = []
        for lang in langs.split(','):
            filter = [i for i in result if lang == i['SubLanguageID']]
            if filter == []: continue
            for q in quality: subtitles += [i for i in filter if q in i['MovieReleaseName'].lower()]
            subtitles += [i for i in filter if not any(x in i['MovieReleaseName'].lower() for x in quality)]
            try: lang = xbmc.convertLanguage(lang, xbmc.ISO_639_1)
            except: pass
            break

        try:
            import zlib, base64
            content = [subtitles[0]["IDSubtitleFile"],]
            content = server.DownloadSubtitles(token, content)
            content = base64.b64decode(content['data'][0]['data'])
            content = zlib.decompressobj(16+zlib.MAX_WBITS).decompress(content)

            subtitle = xbmc.translatePath('special://temp/')
            subtitle = os.path.join(subtitle, 'TemporarySubs.%s.srt' % lang)
            file = open(subtitle, 'wb')
            file.write(content)
            file.close()

            return subtitle
        except:
            index().infoDialog(language(30313).encode("utf-8"), name)
            return

class index:
    def infoDialog(self, str, header=addonName):
        try: xbmcgui.Dialog().notification(header, str, self.addonArt('icon.png'), 3000, sound=False)
        except: xbmc.executebuiltin("Notification(%s,%s, 3000, %s)" % (header, str, self.addonArt('icon.png')))

    def okDialog(self, str1, str2, header=addonName):
        xbmcgui.Dialog().ok(header, str1, str2)

    def selectDialog(self, list, header=addonName):
        select = xbmcgui.Dialog().select(header, list)
        return select

    def yesnoDialog(self, str1, str2, header=addonName, str3='', str4=''):
        answer = xbmcgui.Dialog().yesno(header, str1, str2, '', str4, str3)
        return answer

    def getProperty(self, str):
        property = xbmcgui.Window(10000).getProperty(str)
        return property

    def setProperty(self, str1, str2):
        xbmcgui.Window(10000).setProperty(str1, str2)

    def clearProperty(self, str):
        xbmcgui.Window(10000).clearProperty(str)

    def addon_status(self, id):
        check = xbmcaddon.Addon(id=id).getAddonInfo("name")
        if not check == addonName: return True

    def container_refresh(self):
        xbmc.executebuiltin('Container.Refresh')

    def container_data(self):
        favData, favData2, viewData, offData, watchData = os.path.join(dataPath,'favourite_movies.list'), os.path.join(dataPath,'favourite_tv.list'), os.path.join(dataPath,'views.list'), os.path.join(dataPath,'offset.list'), os.path.join(dataPath,'watched.list')
        if xbmcvfs.exists(favData) == 0 or xbmcvfs.exists(favData2) == 0 or xbmcvfs.exists(viewData) == 0 or xbmcvfs.exists(offData) == 0: return

        try: xbmcvfs.delete(watchData)
        except: pass

        try:
            dbcon = database.connect(addonSettings)
            dbcur = dbcon.cursor()
            dbcur.execute("CREATE TABLE IF NOT EXISTS favourites (""imdb_id TEXT, ""video_type TEXT, ""title TEXT, ""year TEXT, ""tvdb_id TEXT, ""genre TEXT, ""poster TEXT, ""banner TEXT, ""fanart TEXT, ""studio TEXT, ""premiered TEXT, ""duration TEXT, ""rating TEXT, ""votes TEXT, ""mpaa TEXT, ""director TEXT, ""writer TEXT, ""plot TEXT, ""plotoutline TEXT, ""tagline TEXT, ""UNIQUE(imdb_id)"");")
            dbcur.execute("CREATE TABLE IF NOT EXISTS views (""skin TEXT, ""view_type TEXT, ""view_id TEXT, ""UNIQUE(skin, view_type)"");")
            dbcur.execute("CREATE TABLE IF NOT EXISTS points (""name TEXT, ""imdb_id TEXT, ""resume_point TEXT, ""UNIQUE(name, imdb_id)"");")
        except:
            pass
        try:
            file = xbmcvfs.File(offData)
            read = file.read()
            file.close()
            try: xbmcvfs.delete(offData)
            except: pass
            read = re.compile('"(.+?)"[|]"(.+?)"[|]"(.+?)"').findall(read)
            read = [(i[0], 'tt' + i[1], i[2]) for i in read]
            for a in read:
                try:
                    dbcur.execute("DELETE FROM points WHERE name = '%s'" % (a[0]))
                    dbcur.execute("INSERT INTO points Values (?, ?, ?)", a)
                except:
                    pass
        except:
            pass
        try:
            file = xbmcvfs.File(viewData)
            read = file.read()
            file.close()
            try: xbmcvfs.delete(viewData)
            except: pass
            read = re.compile('"(.+?)"[|]"(.+?)"[|]"(.+?)"').findall(read)
            for b in read:
                try:
                    dbcur.execute("DELETE FROM views WHERE skin = '%s' AND view_type = '%s'" % (b[0], b[1]))
                    dbcur.execute("INSERT INTO views Values (?, ?, ?)", b)
                except:
                    pass
        except:
            pass
        try:
            file = xbmcvfs.File(favData)
            read = file.read()
            file.close()
            try: xbmcvfs.delete(favData)
            except: pass
            read = re.compile('"(.+?)"[|]"(.+?)"[|]"(.+?)"[|]".+?"[|]"(.+?)"').findall(read)
            read = [('tt' + i[2], 'Movie', i[0], i[1], '', '', i[3], '', '', '', '', '', '', '', '', '', '', '', '', '') for i in read]
            for c in read:
                try:
                    dbcur.execute("DELETE FROM favourites WHERE imdb_id = '%s'" % (c[0]))
                    dbcur.execute("INSERT INTO favourites Values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", c)
                except:
                    pass
        except:
            pass
        try:
            file = xbmcvfs.File(favData2)
            read = file.read()
            file.close()
            try: xbmcvfs.delete(favData2)
            except: pass
            read = re.compile('"(.+?)"[|]"(.+?)"[|]"(.+?)"[|]".+?"[|]"(.+?)"').findall(read)
            read = [('tt' + i[2], 'TV Show', i[0], i[1], '', '', i[3], '', '', '', '', '', '', '', '', '', '', '', '', '') for i in read]
            for d in read:
                try:
                    dbcur.execute("DELETE FROM favourites WHERE imdb_id = '%s'" % (d[0]))
                    dbcur.execute("INSERT INTO favourites Values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", d)
                except:
                    pass
        except:
            pass
        try:
            dbcon.commit()
        except:
            pass

    def container_view(self, content, viewDict):
        try:
            skin = xbmc.getSkinDir()
            record = (skin, content)
            dbcon = database.connect(addonSettings)
            dbcur = dbcon.cursor()
            dbcur.execute("SELECT * FROM views WHERE skin = '%s' AND view_type = '%s'" % (record[0], record[1]))
            view = dbcur.fetchone()
            view = view[2]
            if view == None: raise Exception()
            xbmc.executebuiltin('Container.SetViewMode(%s)' % str(view))
        except:
            try:
                id = str(viewDict[skin])
                xbmc.executebuiltin('Container.SetViewMode(%s)' % id)
            except:
                pass

    def settings_reset(self):
        try:
            if getSetting("settings_version") == '2.0.6': return
            settings = os.path.join(addonPath,'resources/settings.xml')
            file = xbmcvfs.File(settings)
            read = file.read()
            file.close()
            #setSetting('appearance', common.parseDOM(read, "setting", ret="default", attrs = {"id": 'appearance'})[0])
            #for i in range (1,14): setSetting('hosthd' + str(i), common.parseDOM(read, "setting", ret="default", attrs = {"id": 'hosthd' + str(i)})[0])
            for i in range (1,21): setSetting('host' + str(i), common.parseDOM(read, "setting", ret="default", attrs = {"id": 'host' + str(i)})[0])
            setSetting('settings_version', '2.0.6')
        except:
            return

    def addonArt(self, image, root=''):
        if image.startswith('http://'):
            pass
        elif getSetting("appearance") == '-':
            if image == 'fanart.jpg': image = '-'
            elif image == 'icon.png': image = os.path.join(addonPath,'icon.png')
            elif root == 'episodes_added': image = 'DefaultRecentlyAddedEpisodes.png'
            elif root == 'movies_added': image = 'DefaultRecentlyAddedMovies.png'
            elif root == 'root_genesis': image = 'DefaultVideoPlaylists.png'
            elif root == 'root_tools': image = 'DefaultAddonProgram.png'
            elif root.startswith('movies') or root.endswith('_movies'): image = 'DefaultMovies.png'
            elif root.startswith('episodes') or root.endswith('_episodes'): image = 'DefaultTVShows.png'
            elif root.startswith('shows') or root.endswith('_shows'): image = 'DefaultTVShows.png'
            else: image = 'DefaultFolder.png'
        else:
            art = os.path.join(addonPath, 'resources/art')
            art = os.path.join(art, getSetting("appearance").lower().replace(' ', ''))
            image = os.path.join(art, image)

        return image

    def rootList(self, rootList):
        if rootList == None or len(rootList) == 0: return

        addonFanart = self.addonArt('fanart.jpg')

        total = len(rootList)

        for i in rootList:
            try:
                try: name = language(i['name']).encode("utf-8")
                except: name = i['name']

                root = i['action']

                image = self.addonArt(i['image'], root)

                u = '%s?action=%s' % (sys.argv[0], root)
                try: u += '&url=%s' % urllib.quote_plus(i['url'])
                except: pass
                if root == 'folder_downloads':
                    u = xbmc.translatePath(getSetting("downloads"))
                elif root == 'folder_movie':
                    u = movieLibrary
                elif root == 'folder_tv':
                    u = tvLibrary
                if u == '': raise Exception()

                cm = []
                replaceItems = False
                if root == 'movies_userlist':
                    cm.append((language(30408).encode("utf-8"), 'RunPlugin(%s?action=library_movie_list&url=%s)' % (sys.argv[0], urllib.quote_plus(i['url']))))
                elif root == 'shows_userlist':
                    cm.append((language(30408).encode("utf-8"), 'RunPlugin(%s?action=library_tv_list&url=%s)' % (sys.argv[0], urllib.quote_plus(i['url']))))
                elif root == 'movies_trakt_collection':
                    cm.append((language(30408).encode("utf-8"), 'RunPlugin(%s?action=library_trakt_collection)' % (sys.argv[0])))
                elif root == 'movies_trakt_watchlist':
                    cm.append((language(30408).encode("utf-8"), 'RunPlugin(%s?action=library_trakt_watchlist)' % (sys.argv[0])))
                elif root == 'movies_imdb_watchlist':
                    cm.append((language(30408).encode("utf-8"), 'RunPlugin(%s?action=library_imdb_watchlist)' % (sys.argv[0])))
                elif root == 'shows_trakt_collection':
                    cm.append((language(30408).encode("utf-8"), 'RunPlugin(%s?action=library_tv_trakt_collection)' % (sys.argv[0])))
                elif root == 'shows_trakt_watchlist':
                    cm.append((language(30408).encode("utf-8"), 'RunPlugin(%s?action=library_tv_trakt_watchlist)' % (sys.argv[0])))
                elif root == 'shows_imdb_watchlist':
                    cm.append((language(30408).encode("utf-8"), 'RunPlugin(%s?action=library_tv_imdb_watchlist)' % (sys.argv[0])))
                if root == 'movies_search' or root == 'shows_search' or root == 'actors_movies' or root == 'actors_shows':
                    cm.append((language(30411).encode("utf-8"), 'RunPlugin(%s?action=settings_open)' % (sys.argv[0])))
                    cm.append((language(30412).encode("utf-8"), 'RunPlugin(%s?action=playlist_open)' % (sys.argv[0])))
                    replaceItems = True

                item = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=image)
                item.setInfo(type="Video", infoLabels={"Label": name, "Title": name, "Plot": addonDesc})
                item.setProperty("Fanart_Image", addonFanart)
                item.addContextMenuItems(cm, replaceItems=replaceItems)
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,totalItems=total,isFolder=True)
            except:
                pass

        xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc=True)

    def channelList(self, channelList):
        if channelList == None or len(channelList) == 0: return

        addonFanart = self.addonArt('fanart.jpg')

        autoplay = getSetting("autoplay")
        if PseudoTV == 'True': autoplay = 'true'

        playbackMenu = language(30409).encode("utf-8")
        if autoplay == 'true': playbackMenu = language(30410).encode("utf-8")

        total = len(channelList)
        for i in channelList:
            try:
                channel, title, year, imdb, genre, url, poster, fanart, studio, duration, rating, votes, mpaa, director, plot, plotoutline, tagline = i['name'], i['title'], i['year'], i['imdb'], i['genre'], i['url'], i['poster'], i['fanart'], i['studio'], i['duration'], i['rating'], i['votes'], i['mpaa'], i['director'], i['plot'], i['plotoutline'], i['tagline']

                if fanart == '0' or not getSetting("fanart") == 'true': fanart = addonFanart
                if duration == '0': duration == '120'

                thumb = '%s/%s.png' % (addonLogos, channel)
                name = '%s (%s)' % (title, year)
                label = "[B]%s[/B] : %s" % (channel.upper(), name)

                sysname, systitle, sysyear, sysimdb, sysurl = urllib.quote_plus(name), urllib.quote_plus(title), urllib.quote_plus(year), urllib.quote_plus(imdb), urllib.quote_plus(url)

                meta = {'title': title, 'year': year, 'imdb_id' : 'tt' + imdb, 'genre' : genre, 'poster' : poster, 'fanart' : fanart, 'studio' : studio, 'duration' : duration, 'rating': rating, 'votes': votes, 'mpaa': mpaa, 'director': director, 'plot': plot, 'plotoutline': plotoutline, 'tagline': tagline}
                meta = dict((k,v) for k, v in meta.iteritems() if not v == '0')
                sysmeta = urllib.quote_plus(json.dumps(meta))

                if not autoplay == 'false':
                    u = '%s?action=play&name=%s&title=%s&year=%s&imdb=%s&url=%s&t=%s' % (sys.argv[0], sysname, systitle, sysyear, sysimdb, sysurl, datetime.datetime.now().strftime("%Y%m%d%H%M%S%f"))
                    isFolder = False
                else:
                    u = '%s?action=get_host&name=%s&title=%s&year=%s&imdb=%s&url=%s&meta=%s' % (sys.argv[0], sysname, systitle, sysyear, sysimdb, sysurl, sysmeta)
                    isFolder = True

                cm = []
                cm.append((playbackMenu, 'RunPlugin(%s?action=toggle_movie_playback&name=%s&title=%s&imdb=%s&year=%s)' % (sys.argv[0], sysname, systitle, sysimdb, sysyear)))
                cm.append((language(30405).encode("utf-8"), 'RunPlugin(%s?action=trailer&name=%s)' % (sys.argv[0], sysname)))

                item = xbmcgui.ListItem(label, iconImage=thumb, thumbnailImage=thumb)
                try: item.setArt({'poster': thumb, 'banner': thumb})
                except: pass
                item.setProperty("Fanart_Image", fanart)
                item.setInfo(type="Video", infoLabels = meta)
                item.setProperty("Video", "true")
                item.setProperty("IsPlayable", "true")
                item.addContextMenuItems(cm, replaceItems=True)
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,totalItems=total,isFolder=isFolder)
            except:
                pass

        xbmcplugin.setContent(int(sys.argv[1]), 'episodes')
        xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc=False)

    def movieList(self, movieList):
        if movieList == None or len(movieList) == 0: return

        addonFanart = self.addonArt('fanart.jpg')

        autoplay = getSetting("autoplay")
        if PseudoTV == 'True': autoplay = 'true'

        playbackMenu = language(30409).encode("utf-8")
        if autoplay == 'true': playbackMenu = language(30410).encode("utf-8")

        cacheToDisc = False
        if action == 'movies_search': cacheToDisc = True

        try:
            favourites = []
            dbcon = database.connect(addonSettings)
            dbcur = dbcon.cursor()
            dbcur.execute("SELECT * FROM favourites WHERE video_type ='Movie'")
            favourites = dbcur.fetchall()
            favourites = [i[0] for i in favourites]
            favourites = [re.sub('[^0-9]', '', i) for i in favourites]
        except:
            pass

        try:
            record = ('movies', getSetting("trakt_user"))
            dbcon = database.connect(addonCache)
            dbcur = dbcon.cursor()
            dbcur.execute("SELECT * FROM trakt WHERE info = '%s' AND user = '%s'" % (record[0], record[1]))
            indicators = dbcur.fetchone()
            indicators = indicators[2]
            indicators = json.loads(indicators)
        except:
            pass

        total = len(movieList)
        for i in movieList:
            try:
                name, title, year, imdb, genre, url, poster, fanart, studio, duration, rating, votes, mpaa, director, plot, plotoutline, tagline = i['name'], i['title'], i['year'], i['imdb'], i['genre'], i['url'], i['poster'], i['fanart'], i['studio'], i['duration'], i['rating'], i['votes'], i['mpaa'], i['director'], i['plot'], i['plotoutline'], i['tagline']

                if fanart == '0' or not getSetting("fanart") == 'true': fanart = addonFanart
                if duration == '0': duration == '120'

                sysname, systitle, sysyear, sysimdb, sysurl, sysimage = urllib.quote_plus(name), urllib.quote_plus(title), urllib.quote_plus(year), urllib.quote_plus(imdb), urllib.quote_plus(url), urllib.quote_plus(poster)

                meta = {'title': title, 'year': year, 'imdb_id' : 'tt' + imdb, 'genre' : genre, 'poster' : poster, 'fanart' : fanart, 'studio' : studio, 'duration' : duration, 'rating': rating, 'votes': votes, 'mpaa': mpaa, 'director': director, 'plot': plot, 'plotoutline': plotoutline, 'tagline': tagline}
                meta = dict((k,v) for k, v in meta.iteritems() if not v == '0')
                sysmeta = urllib.quote_plus(json.dumps(meta))

                if not autoplay == 'false':
                    u = '%s?action=play&name=%s&title=%s&year=%s&imdb=%s&url=%s&t=%s' % (sys.argv[0], sysname, systitle, sysyear, sysimdb, sysurl, datetime.datetime.now().strftime("%Y%m%d%H%M%S%f"))
                    isFolder = False
                else:
                    u = '%s?action=get_host&name=%s&title=%s&year=%s&imdb=%s&url=%s&meta=%s' % (sys.argv[0], sysname, systitle, sysyear, sysimdb, sysurl, sysmeta)
                    isFolder = True

                try:
                    playcount = metaget._get_watched('movie', 'tt' + imdb, '', '')
                    if playcount == 7: meta.update({'playcount': 1, 'overlay': 7})
                    else: meta.update({'playcount': 0, 'overlay': 6})
                except:
                    pass
                try:
                    playcount = [i for i in indicators if i['imdb_id'] == 'tt' + imdb][0]
                    meta.update({'playcount': 1, 'overlay': 7})
                except:
                    pass

                cm = []
                cm.append((playbackMenu, 'RunPlugin(%s?action=toggle_movie_playback&name=%s&title=%s&year=%s&imdb=%s)' % (sys.argv[0], sysname, systitle, sysyear, sysimdb)))
                cm.append((language(30405).encode("utf-8"), 'RunPlugin(%s?action=trailer&name=%s)' % (sys.argv[0], sysname)))
                if not (getSetting("trakt_user") == '' or getSetting("trakt_password") == ''):
                    cm.append((language(30420).encode("utf-8"), 'RunPlugin(%s?action=trakt_manager&name=%s&imdb=%s)' % (sys.argv[0], sysname, sysimdb)))
                if action == 'movies_favourites':
                    cm.append((language(30407).encode("utf-8"), 'RunPlugin(%s?action=favourite_delete&imdb=%s)' % (sys.argv[0], sysimdb)))
                elif action == 'movies_search':
                    cm.append((language(30406).encode("utf-8"), 'RunPlugin(%s?action=favourite_movie_from_search&imdb=%s&name=%s&year=%s&image=%s)' % (sys.argv[0], sysimdb, systitle, sysyear, sysimage)))
                else:
                    if not imdb in favourites: cm.append((language(30406).encode("utf-8"), 'RunPlugin(%s?action=favourite_movie_add&imdb=%s&name=%s&year=%s&image=%s)' % (sys.argv[0], sysimdb, systitle, sysyear, sysimage)))
                    else: cm.append((language(30407).encode("utf-8"), 'RunPlugin(%s?action=favourite_delete&imdb=%s)' % (sys.argv[0], sysimdb)))
                cm.append((language(30408).encode("utf-8"), 'RunPlugin(%s?action=library_movie_add&name=%s&title=%s&year=%s&imdb=%s&url=%s)' % (sys.argv[0], sysname, systitle, sysyear, sysimdb, sysurl)))
                cm.append((language(30413).encode("utf-8"), 'Action(Info)'))
                if not imdb == '0' and not action == 'movies_search':
                    cm.append((language(30403).encode("utf-8"), 'RunPlugin(%s?action=unwatched_movies&title=%s&year=%s&imdb=%s)' % (sys.argv[0], systitle, sysyear, sysimdb)))
                if not imdb == '0' and not action == 'movies_search':
                    cm.append((language(30404).encode("utf-8"), 'RunPlugin(%s?action=watched_movies&title=%s&year=%s&imdb=%s)' % (sys.argv[0], systitle, sysyear, sysimdb)))
                cm.append((language(30416).encode("utf-8"), 'RunPlugin(%s?action=view_movies)' % (sys.argv[0])))

                item = xbmcgui.ListItem(label=name, iconImage="DefaultVideo.png", thumbnailImage=poster)
                try: item.setArt({'poster': poster, 'banner': poster})
                except: pass
                item.setProperty("Fanart_Image", fanart)
                item.setInfo(type="Video", infoLabels = meta)
                item.setProperty("Video", "true")
                item.setProperty("IsPlayable", "true")
                item.addContextMenuItems(cm, replaceItems=True)
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,totalItems=total,isFolder=isFolder)
            except:
                pass

        try:
            next = movieList[0]['next']
            if next == '': raise Exception()
            name, url, image = language(30381).encode("utf-8"), next, self.addonArt('item_next.jpg')
            if getSetting("appearance") == '-': image = 'DefaultFolder.png'
            u = '%s?action=movies&url=%s' % (sys.argv[0], urllib.quote_plus(url))
            item = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=image)
            item.setInfo( type="Video", infoLabels={ "Label": name, "Title": name, "Plot": addonDesc } )
            item.setProperty("Fanart_Image", addonFanart)
            item.addContextMenuItems([], replaceItems=False)
            xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,isFolder=True)
        except:
            pass

        xbmcplugin.setContent(int(sys.argv[1]), 'movies')
        xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc=cacheToDisc)
        for i in range(0, 200):
            if xbmc.getCondVisibility('Container.Content(movies)'):
                return index().container_view('movies', {'skin.confluence' : 500})
            xbmc.sleep(100)

    def showList(self, showList):
        if showList == None or len(showList) == 0: return

        addonFanart = self.addonArt('fanart.jpg')

        try:
            favourites = []
            dbcon = database.connect(addonSettings)
            dbcur = dbcon.cursor()
            dbcur.execute("SELECT * FROM favourites WHERE video_type ='TV Show'")
            favourites = dbcur.fetchall()
            favourites = [i[0] for i in favourites]
            favourites = [re.sub('[^0-9]', '', i) for i in favourites]
        except:
            pass

        total = len(showList)
        for i in showList:
            try:
                name, title, year, imdb, tvdb, genre, url, poster, banner, fanart, studio, premiered, duration, rating, mpaa, plot = i['title'],  i['title'], i['year'], i['imdb'], i['tvdb'], i['genre'], i['url'], i['poster'], i['banner'], i['fanart'], i['studio'], i['premiered'], i['duration'], i['rating'], i['mpaa'], i['plot']

                if fanart == '0' or not getSetting("fanart") == 'true': fanart = addonFanart
                if duration == '0': duration == '60'

                systitle, sysyear, sysimdb, systvdb, sysurl, sysimage = urllib.quote_plus(title), urllib.quote_plus(year), urllib.quote_plus(imdb), urllib.quote_plus(tvdb), urllib.quote_plus(url), urllib.quote_plus(poster)

                meta = {'title': title, 'tvshowtitle': title, 'year': year, 'imdb_id' : 'tt' + imdb, 'tvdb_id': tvdb, 'genre' : genre, 'studio': studio, 'premiered': premiered, 'duration' : duration, 'rating' : rating, 'mpaa' : mpaa, 'plot': plot}
                meta = dict((k,v) for k, v in meta.iteritems() if not v == '0')

                u = '%s?action=seasons&show=%s&year=%s&imdb=%s&tvdb=%s' % (sys.argv[0], systitle, sysyear, sysimdb, systvdb)

                try:
                    raise Exception()
                    playcount = metaget._get_watched('tvshow', 'tt' + imdb, '', '')
                    if playcount == 7: meta.update({'playcount': 1, 'overlay': 7})
                    else: meta.update({'playcount': 0, 'overlay': 6})
                except:
                    pass

                cm = []
                cm.append((language(30405).encode("utf-8"), 'RunPlugin(%s?action=trailer&name=%s)' % (sys.argv[0], systitle)))
                if not (getSetting("trakt_user") == '' or getSetting("trakt_password") == ''):
                    cm.append((language(30420).encode("utf-8"), 'RunPlugin(%s?action=trakt_tv_manager&name=%s&imdb=%s)' % (sys.argv[0], systitle, sysimdb)))
                if action == 'shows_favourites':
                    cm.append((language(30407).encode("utf-8"), 'RunPlugin(%s?action=favourite_delete&imdb=%s)' % (sys.argv[0], sysimdb))) 
                elif action.startswith('shows_search'):
                    cm.append((language(30406).encode("utf-8"), 'RunPlugin(%s?action=favourite_tv_from_search&imdb=%s&name=%s&year=%s&image=%s)' % (sys.argv[0], sysimdb, systitle, sysyear, sysimage)))
                else:
                    if not imdb in favourites: cm.append((language(30406).encode("utf-8"), 'RunPlugin(%s?action=favourite_tv_add&imdb=%s&name=%s&year=%s&image=%s)' % (sys.argv[0], sysimdb, systitle, sysyear, sysimage)))
                    else: cm.append((language(30407).encode("utf-8"), 'RunPlugin(%s?action=favourite_delete&imdb=%s)' % (sys.argv[0], sysimdb)))
                cm.append((language(30408).encode("utf-8"), 'RunPlugin(%s?action=library_tv_add&name=%s&year=%s&imdb=%s&tvdb=%s)' % (sys.argv[0], systitle, sysyear, sysimdb, systvdb)))
                cm.append((language(30414).encode("utf-8"), 'Action(Info)'))
                if not imdb == '0' and not action == 'shows_search':
                    cm.append((language(30403).encode("utf-8"), 'RunPlugin(%s?action=unwatched_shows&name=%s&year=%s&imdb=%s&tvdb=%s)' % (sys.argv[0], systitle, sysyear, sysimdb, systvdb)))
                if not imdb == '0' and not action == 'shows_search':
                    cm.append((language(30404).encode("utf-8"), 'RunPlugin(%s?action=watched_shows&name=%s&year=%s&imdb=%s&tvdb=%s)' % (sys.argv[0], systitle, sysyear, sysimdb, systvdb)))
                cm.append((language(30417).encode("utf-8"), 'RunPlugin(%s?action=view_tvshows)' % (sys.argv[0])))

                item = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=poster)
                try: item.setArt({'poster': poster, 'tvshow.poster': poster, 'season.poster': poster, 'banner': banner, 'tvshow.banner': banner, 'season.banner': banner})
                except: pass
                item.setProperty("Fanart_Image", fanart)
                item.setInfo(type="Video", infoLabels = meta)
                item.addContextMenuItems(cm, replaceItems=True)
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,totalItems=total,isFolder=True)
            except:
                pass

        try:
            next = showList[0]['next']
            if next == '': raise Exception()
            name, url, image = language(30381).encode("utf-8"), next, self.addonArt('item_next.jpg')
            if getSetting("appearance") == '-': image = 'DefaultFolder.png'
            u = '%s?action=shows&url=%s' % (sys.argv[0], urllib.quote_plus(url))
            item = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=image)
            item.setInfo( type="Video", infoLabels={ "Label": name, "Title": name, "Plot": addonDesc } )
            item.setProperty("Fanart_Image", addonFanart)
            item.addContextMenuItems([], replaceItems=False)
            xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,isFolder=True)
        except:
            pass

        xbmcplugin.setContent(int(sys.argv[1]), 'tvshows')
        xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc=True)
        for i in range(0, 200):
            if xbmc.getCondVisibility('Container.Content(tvshows)'):
                return index().container_view('tvshows', {'skin.confluence' : 500})
            xbmc.sleep(100)

    def seasonList(self, seasonList):
        if seasonList == None or len(seasonList) == 0: return

        addonFanart = self.addonArt('fanart.jpg')

        try:
            favourites = []
            dbcon = database.connect(addonSettings)
            dbcur = dbcon.cursor()
            dbcur.execute("SELECT * FROM favourites WHERE video_type ='TV Show'")
            favourites = dbcur.fetchall()
            favourites = [i[0] for i in favourites]
            favourites = [re.sub('[^0-9]', '', i) for i in favourites]
        except:
            pass

        total = len(seasonList)
        for i in seasonList:
            try:
                title, year, imdb, tvdb, season, show, show_alt, genre, url, poster, banner, thumb, fanart, studio, status, premiered, duration, rating, mpaa, plot = 'Season ' + i['title'], i['year'], i['imdb'], i['tvdb'], i['season'], i['show'], i['show_alt'], i['genre'], i['url'], i['poster'], i['banner'], i['thumb'], i['fanart'], i['studio'], i['status'], i['date'], i['duration'], i['rating'], i['mpaa'], i['plot']

                if fanart == '0' or not getSetting("fanart") == 'true': fanart = addonFanart
                if duration == '0': duration == '60'

                sysyear, sysimdb, systvdb, sysseason, sysshow, sysurl, sysimage = urllib.quote_plus(year), urllib.quote_plus(imdb), urllib.quote_plus(tvdb), urllib.quote_plus(season), urllib.quote_plus(show), urllib.quote_plus(url), urllib.quote_plus(poster)

                meta = {'title': title, 'year': year, 'imdb_id' : 'tt' + imdb, 'tvdb_id' : tvdb, 'season' : season, 'tvshowtitle': show, 'genre' : genre, 'studio': studio, 'status': status, 'premiered' : premiered, 'duration' : duration, 'rating': rating, 'mpaa' : mpaa, 'plot': plot}
                meta = dict((k,v) for k, v in meta.iteritems() if not v == '0')

                u = '%s?action=episodes&show=%s&year=%s&imdb=%s&tvdb=%s&season=%s' % (sys.argv[0], sysshow, sysyear, sysimdb, systvdb, sysseason)

                try:
                    raise Exception()
                    playcount = metaget._get_watched('tvshow', 'tt' + imdb, '', season)
                    if playcount == 7: meta.update({'playcount': 1, 'overlay': 7})
                    else: meta.update({'playcount': 0, 'overlay': 6})
                except:
                    pass

                cm = []
                cm.append((language(30405).encode("utf-8"), 'RunPlugin(%s?action=trailer&name=%s)' % (sys.argv[0], sysshow)))
                if not (getSetting("trakt_user") == '' or getSetting("trakt_password") == ''):
                    cm.append((language(30420).encode("utf-8"), 'RunPlugin(%s?action=trakt_tv_manager&name=%s&imdb=%s)' % (sys.argv[0], sysshow, sysimdb)))
                if not imdb in favourites: cm.append((language(30406).encode("utf-8"), 'RunPlugin(%s?action=favourite_tv_add&imdb=%s&name=%s&year=%s&image=%s)' % (sys.argv[0], sysimdb, sysshow, sysyear, sysimage)))
                else: cm.append((language(30407).encode("utf-8"), 'RunPlugin(%s?action=favourite_delete&imdb=%s)' % (sys.argv[0], sysimdb)))
                cm.append((language(30408).encode("utf-8"), 'RunPlugin(%s?action=library_tv_add&name=%s&year=%s&imdb=%s&tvdb=%s)' % (sys.argv[0], sysshow, sysyear, sysimdb, systvdb)))
                cm.append((language(30414).encode("utf-8"), 'Action(Info)'))
                if not imdb == '0':
                    cm.append((language(30403).encode("utf-8"), 'RunPlugin(%s?action=unwatched_seasons&name=%s&year=%s&imdb=%s&tvdb=%s&season=%s)' % (sys.argv[0], sysshow, sysyear, sysimdb, systvdb, sysseason)))
                if not imdb == '0':
                    cm.append((language(30404).encode("utf-8"), 'RunPlugin(%s?action=watched_seasons&name=%s&year=%s&imdb=%s&tvdb=%s&season=%s)' % (sys.argv[0], sysshow, sysyear, sysimdb, systvdb, sysseason)))
                cm.append((language(30418).encode("utf-8"), 'RunPlugin(%s?action=view_seasons)' % (sys.argv[0])))

                item = xbmcgui.ListItem(title, iconImage="DefaultVideo.png", thumbnailImage=thumb)
                try: item.setArt({'poster': thumb, 'tvshow.poster': poster, 'season.poster': thumb, 'banner': banner, 'tvshow.banner': banner, 'season.banner': banner})
                except: pass
                item.setProperty("Fanart_Image", fanart)
                item.setInfo(type="Video", infoLabels = meta)
                item.addContextMenuItems(cm, replaceItems=True)
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,totalItems=total,isFolder=True)
            except:
                pass

        xbmcplugin.setProperty(int(sys.argv[1]), 'showplot', plot)

        xbmcplugin.setContent(int(sys.argv[1]), 'seasons')
        xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc=True)
        for i in range(0, 200):
            if xbmc.getCondVisibility('Container.Content(seasons)'):
                return index().container_view('seasons', {'skin.confluence' : 500})
            xbmc.sleep(100)

    def episodeList(self, episodeList):
        if episodeList == None or len(episodeList) == 0: return

        addonFanart = self.addonArt('fanart.jpg')

        autoplay = getSetting("autoplay")
        if PseudoTV == 'True': autoplay = 'true'

        playbackMenu = language(30409).encode("utf-8")
        if autoplay == 'true': playbackMenu = language(30410).encode("utf-8")

        try:
            favourites = []
            dbcon = database.connect(addonSettings)
            dbcur = dbcon.cursor()
            dbcur.execute("SELECT * FROM favourites WHERE video_type ='TV Show'")
            favourites = dbcur.fetchall()
            favourites = [i[0] for i in favourites]
            favourites = [re.sub('[^0-9]', '', i) for i in favourites]
        except:
            pass

        try:
            record = ('shows', getSetting("trakt_user"))
            dbcon = database.connect(addonCache)
            dbcur = dbcon.cursor()
            dbcur.execute("SELECT * FROM trakt WHERE info = '%s' AND user = '%s'" % (record[0], record[1]))
            indicators = dbcur.fetchone()
            indicators = indicators[2]
            indicators = json.loads(indicators)
        except:
            pass

        total = len(episodeList)
        for i in episodeList:
            try:
                name, title, year, imdb, tvdb, season, episode, show, show_alt, genre, url, poster, banner, thumb, fanart, studio, status, premiered, duration, rating, mpaa, director, writer, plot = i['name'], i['title'], i['year'], i['imdb'], i['tvdb'], i['season'], i['episode'], i['show'], i['show_alt'], i['genre'], i['url'], i['poster'], i['banner'], i['thumb'], i['fanart'], i['studio'], i['status'], i['date'], i['duration'], i['rating'], i['mpaa'], i['director'], i['writer'], i['plot']

                label = season + 'x' + '%02d' % int(episode) + ' . ' + title
                if action == 'episodes_added' or action == 'episodes_calendar': label = show + ' - ' + label

                if fanart == '0' or not getSetting("fanart") == 'true': fanart = addonFanart
                if duration == '0': duration == '60'

                sysname, systitle, sysyear, sysimdb, systvdb, sysseason, sysepisode, sysshow, sysshow_alt, sysurl, sysimage, sysdate, sysgenre = urllib.quote_plus(name), urllib.quote_plus(title), urllib.quote_plus(year), urllib.quote_plus(imdb), urllib.quote_plus(tvdb), urllib.quote_plus(season), urllib.quote_plus(episode), urllib.quote_plus(show), urllib.quote_plus(show_alt), urllib.quote_plus(url), urllib.quote_plus(poster), urllib.quote_plus(premiered), urllib.quote_plus(genre)

                meta = {'title': title, 'year': year, 'imdb_id' : 'tt' + imdb, 'tvdb_id' : tvdb, 'season' : season, 'episode': episode, 'tvshowtitle': show, 'genre' : genre, 'poster' : poster, 'banner' : banner, 'thumb' : thumb, 'fanart' : fanart, 'studio': studio, 'status': status, 'premiered' : premiered, 'duration' : duration, 'rating': rating, 'mpaa' : mpaa, 'director': director, 'writer': writer, 'plot': plot}
                sysmeta = urllib.quote_plus(json.dumps(meta))

                if not autoplay == 'false':
                    u = '%s?action=play&name=%s&title=%s&year=%s&imdb=%s&tvdb=%s&season=%s&episode=%s&show=%s&show_alt=%s&date=%s&genre=%s&url=%s&t=%s' % (sys.argv[0], sysname, systitle, sysyear, sysimdb, systvdb, sysseason, sysepisode, sysshow, sysshow_alt, sysdate, sysgenre, sysurl, datetime.datetime.now().strftime("%Y%m%d%H%M%S%f"))
                    isFolder = False
                else:
                    u = '%s?action=get_host&name=%s&title=%s&year=%s&imdb=%s&tvdb=%s&season=%s&episode=%s&show=%s&show_alt=%s&date=%s&genre=%s&url=%s&meta=%s' % (sys.argv[0], sysname, systitle, sysyear, sysimdb, systvdb, sysseason, sysepisode, sysshow, sysshow_alt, sysdate, sysgenre, sysurl, sysmeta)
                    isFolder = True

                try:
                    playcount = metaget._get_watched_episode({'imdb_id' : 'tt' + imdb, 'season' : season, 'episode': episode, 'premiered' : ''})
                    if playcount == 7: meta.update({'playcount': 1, 'overlay': 7})
                    else: meta.update({'playcount': 0, 'overlay': 6})
                except:
                    pass
                try:
                    playcount = [i for i in indicators if i['imdb_id'] == 'tt' + imdb][0]['seasons']
                    playcount = [i for i in playcount if i['season'] == int(season)][0]['episodes']
                    playcount = [i for i in playcount if i == int(episode)][0]
                    meta.update({'playcount': 1, 'overlay': 7})
                except:
                    pass

                cm = []
                cm.append((playbackMenu, 'RunPlugin(%s?action=toggle_episode_playback&name=%s&title=%s&year=%s&imdb=%s&tvdb=%s&season=%s&episode=%s&show=%s&show_alt=%s&date=%s&genre=%s)' % (sys.argv[0], sysname, systitle, sysyear, sysimdb, systvdb, sysseason, sysepisode, sysshow, sysshow_alt, sysdate, sysgenre)))
                if not imdb == '0':
                    cm.append((language(30420).encode("utf-8"), 'RunPlugin(%s?action=trakt_tv_manager&name=%s&imdb=%s)' % (sys.argv[0], sysshow, sysimdb)))
                if not imdb in favourites: cm.append((language(30406).encode("utf-8"), 'RunPlugin(%s?action=favourite_tv_add&imdb=%s&name=%s&year=%s&image=%s)' % (sys.argv[0], sysimdb, sysshow, sysyear, sysimage)))
                else: cm.append((language(30407).encode("utf-8"), 'RunPlugin(%s?action=favourite_delete&imdb=%s)' % (sys.argv[0], sysimdb)))
                cm.append((language(30408).encode("utf-8"), 'RunPlugin(%s?action=library_tv_add&name=%s&year=%s&imdb=%s&tvdb=%s)' % (sys.argv[0], sysshow, sysyear, sysimdb, systvdb)))
                cm.append((language(30415).encode("utf-8"), 'Action(Info)'))
                if not imdb == '0':
                    cm.append((language(30403).encode("utf-8"), 'RunPlugin(%s?action=unwatched_episodes&imdb=%s&season=%s&episode=%s)' % (sys.argv[0], sysimdb, sysseason, sysepisode)))
                if not imdb == '0':
                    cm.append((language(30404).encode("utf-8"), 'RunPlugin(%s?action=watched_episodes&imdb=%s&season=%s&episode=%s)' % (sys.argv[0], sysimdb, sysseason, sysepisode)))
                cm.append((language(30419).encode("utf-8"), 'RunPlugin(%s?action=view_episodes)' % (sys.argv[0])))

                item = xbmcgui.ListItem(label, iconImage="DefaultVideo.png", thumbnailImage=thumb)
                try: item.setArt({'poster': poster, 'tvshow.poster': poster, 'season.poster': poster, 'banner': banner, 'tvshow.banner': banner, 'season.banner': banner})
                except: pass
                item.setProperty("Fanart_Image", fanart)
                item.setInfo(type="Video", infoLabels = meta)
                item.setProperty("Video", "true")
                item.setProperty("IsPlayable", "true")
                item.addContextMenuItems(cm, replaceItems=True)
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,totalItems=total,isFolder=isFolder)
            except:
                pass

        xbmcplugin.setContent(int(sys.argv[1]), 'episodes')
        xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc=False)
        for i in range(0, 200):
            if xbmc.getCondVisibility('Container.Content(episodes)'):
                return index().container_view('episodes', {'skin.confluence' : 504})
            xbmc.sleep(100)

    def moviesourceList(self, sourceList, name, imdb, meta):
        if sourceList == None or len(sourceList) == 0: return

        total = len(sourceList)
        for i in sourceList:
            try:
                url, source, provider = i['url'], i['source'], i['provider']
                poster, fanart = meta['poster'], meta['fanart']

                sysname, sysimdb, sysurl, syssource, sysprovider = urllib.quote_plus(name), urllib.quote_plus(imdb), urllib.quote_plus(url), urllib.quote_plus(source), urllib.quote_plus(provider)

                u = '%s?action=play_moviehost&name=%s&imdb=%s&url=%s&source=%s&provider=%s' % (sys.argv[0], sysname, sysimdb, sysurl, syssource, sysprovider)

                cm = []
                cm.append((language(30401).encode("utf-8"), 'RunPlugin(%s?action=item_queue)' % (sys.argv[0])))
                cm.append((language(30402).encode("utf-8"), 'RunPlugin(%s?action=download&name=%s&url=%s&provider=%s)' % (sys.argv[0], sysname, sysurl, sysprovider)))
                cm.append((language(30405).encode("utf-8"), 'RunPlugin(%s?action=trailer&name=%s)' % (sys.argv[0], sysname)))
                cm.append((language(30413).encode("utf-8"), 'Action(Info)'))
                cm.append((language(30411).encode("utf-8"), 'RunPlugin(%s?action=settings_open)' % (sys.argv[0])))
                cm.append((language(30412).encode("utf-8"), 'RunPlugin(%s?action=playlist_open)' % (sys.argv[0])))

                item = xbmcgui.ListItem(source, iconImage="DefaultVideo.png", thumbnailImage=poster)
                try: item.setArt({'poster': poster, 'banner': poster})
                except: pass
                item.setProperty("Fanart_Image", fanart)
                item.setInfo(type="Video", infoLabels = meta)
                item.setProperty("Video", "true")
                item.setProperty("IsPlayable", "true")
                item.addContextMenuItems(cm, replaceItems=True)
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,totalItems=total,isFolder=False)
            except:
                pass

        xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc=True)

    def tvsourceList(self, sourceList, name, imdb, meta):
        if sourceList == None or len(sourceList) == 0: return

        total = len(sourceList)
        for i in sourceList:
            try:
                url, source, provider = i['url'], i['source'], i['provider']
                poster, banner, thumb, fanart = meta['poster'], meta['banner'], meta['thumb'], meta['fanart']

                sysname, sysimdb, sysurl, syssource, sysprovider = urllib.quote_plus(name), urllib.quote_plus(imdb), urllib.quote_plus(url), urllib.quote_plus(source), urllib.quote_plus(provider)

                u = '%s?action=play_tvhost&name=%s&imdb=%s&url=%s&source=%s&provider=%s' % (sys.argv[0], sysname, sysimdb, sysurl, syssource, sysprovider)

                cm = []
                cm.append((language(30401).encode("utf-8"), 'RunPlugin(%s?action=item_queue)' % (sys.argv[0])))
                cm.append((language(30402).encode("utf-8"), 'RunPlugin(%s?action=download&name=%s&url=%s&provider=%s)' % (sys.argv[0], sysname, sysurl, sysprovider)))
                cm.append((language(30415).encode("utf-8"), 'Action(Info)'))
                cm.append((language(30411).encode("utf-8"), 'RunPlugin(%s?action=settings_open)' % (sys.argv[0])))
                cm.append((language(30412).encode("utf-8"), 'RunPlugin(%s?action=playlist_open)' % (sys.argv[0])))

                item = xbmcgui.ListItem(source, iconImage="DefaultVideo.png", thumbnailImage=thumb)
                try: item.setArt({'poster': poster, 'tvshow.poster': poster, 'season.poster': poster, 'banner': banner, 'tvshow.banner': banner, 'season.banner': banner})
                except: pass
                item.setProperty("Fanart_Image", fanart)
                item.setInfo(type="Video", infoLabels = meta)
                item.setProperty("Video", "true")
                item.setProperty("IsPlayable", "true")
                item.addContextMenuItems(cm, replaceItems=True)
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,totalItems=total,isFolder=False)
            except:
                pass

        xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc=True)

class contextMenu:
    def item_queue(self):
        xbmc.executebuiltin('Action(Queue)')

    def cache_clear(self):
        try: StorageServer.StorageServer(addonFullId,1).delete('%')
        except: pass
        try: StorageServer.StorageServer(addonFullId,24).delete('%')
        except: pass
        try: StorageServer.StorageServer(addonFullId,720).delete('%')
        except: pass
        index().infoDialog(language(30312).encode("utf-8"))

    def playlist_open(self):
        xbmc.executebuiltin('ActivateWindow(VideoPlaylist)')

    def settings_open(self, id=addonId):
        xbmc.executebuiltin('Addon.OpenSettings(%s)' % id)

    def view(self, content):
        try:
            skin = xbmc.getSkinDir()
            skinPath = xbmc.translatePath('special://skin/')
            xml = os.path.join(skinPath,'addon.xml')
            file = xbmcvfs.File(xml)
            read = file.read().replace('\n','')
            file.close()
            try: src = re.compile('defaultresolution="(.+?)"').findall(read)[0]
            except: src = re.compile('<res.+?folder="(.+?)"').findall(read)[0]
            src = os.path.join(skinPath, src)
            src = os.path.join(src, 'MyVideoNav.xml')
            file = xbmcvfs.File(src)
            read = file.read().replace('\n','')
            file.close()
            views = re.compile('<views>(.+?)</views>').findall(read)[0]
            views = [int(x) for x in views.split(',')]
            for view in views:
                label = xbmc.getInfoLabel('Control.GetLabel(%s)' % (view))
                if not (label == '' or label == None): break
            record = (skin, content, str(view))
            if not xbmcvfs.exists(dataPath): xbmcvfs.mkdir(dataPath)
            dbcon = database.connect(addonSettings)
            dbcur = dbcon.cursor()
            dbcur.execute("CREATE TABLE IF NOT EXISTS views (""skin TEXT, ""view_type TEXT, ""view_id TEXT, ""UNIQUE(skin, view_type)"");")
            dbcur.execute("DELETE FROM views WHERE skin = '%s' AND view_type = '%s'" % (record[0], record[1]))
            dbcur.execute("INSERT INTO views Values (?, ?, ?)", record)
            dbcon.commit()
            viewName = xbmc.getInfoLabel('Container.Viewmode')
            index().infoDialog('%s%s%s' % (language(30301).encode("utf-8"), viewName, language(30302).encode("utf-8")))
        except:
            return

    def favourite_add(self, type, imdb, name, year, image, refresh=False):
        try:
            record = ('tt' + imdb, type, name, year, '', '', image, '', '', '', '', '', '', '', '', '', '', '', '', '')

            if not xbmcvfs.exists(dataPath): xbmcvfs.mkdir(dataPath)
            dbcon = database.connect(addonSettings)
            dbcur = dbcon.cursor()
            dbcur.execute("CREATE TABLE IF NOT EXISTS favourites (""imdb_id TEXT, ""video_type TEXT, ""title TEXT, ""year TEXT, ""tvdb_id TEXT, ""genre TEXT, ""poster TEXT, ""banner TEXT, ""fanart TEXT, ""studio TEXT, ""premiered TEXT, ""duration TEXT, ""rating TEXT, ""votes TEXT, ""mpaa TEXT, ""director TEXT, ""writer TEXT, ""plot TEXT, ""plotoutline TEXT, ""tagline TEXT, ""UNIQUE(imdb_id)"");")
            dbcur.execute("DELETE FROM favourites WHERE imdb_id = '%s'" % (record[0]))
            dbcur.execute("INSERT INTO favourites Values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", record)
            dbcon.commit()

            if refresh == True: index().container_refresh()
            index().infoDialog(language(30303).encode("utf-8"), name)
        except:
            return

    def favourite_delete(self, imdb):
        try:
            record = ['tt' + imdb]

            if not xbmcvfs.exists(dataPath): xbmcvfs.mkdir(dataPath)
            dbcon = database.connect(addonSettings)
            dbcur = dbcon.cursor()
            dbcur.execute("DELETE FROM favourites WHERE imdb_id = '%s'" % (record[0]))
            dbcon.commit()

            index().container_refresh()
            index().infoDialog(language(30304).encode("utf-8"), name)
        except:
            return

    def trakt_manager(self, content, name, imdb):
        try:
            if not imdb.startswith('tt'): imdb = 'tt' + imdb

            userList = userlists().trakt_list()

            nameList = [i['name'] for i in userList]
            nameList = [nameList[i//2] for i in range(len(nameList)*2)]
            for i in range(0, len(nameList), 2): nameList[i] = (language(30426) + ' ' + nameList[i]).encode('utf-8')
            for i in range(1, len(nameList), 2): nameList[i] = (language(30427) + ' ' + nameList[i]).encode('utf-8')
            nameList = [language(30421).encode("utf-8"), language(30422).encode("utf-8"), language(30423).encode("utf-8"), language(30424).encode("utf-8"), language(30425).encode("utf-8")] + nameList

            slugList = [[x for x in i['url'].split('/') if not x == ''][-1] for i in userList]
            slugList = [slugList[i//2] for i in range(len(slugList)*2)]
            slugList = ['', '', '', '', ''] + slugList

            select = index().selectDialog(nameList, language(30420).encode("utf-8"))
            post = {"imdb_id": imdb, "movies": [{"imdb_id": imdb}], "shows": [{"imdb_id": imdb}]}

            if select == -1:
                return
            elif select == 0:
                url = 'http://api.trakt.tv/%s/library/%s' % (content, link().trakt_key)
            elif select == 1:
                url = 'http://api.trakt.tv/%s/unlibrary/%s' % (content, link().trakt_key)
            elif select == 2:
                url = 'http://api.trakt.tv/%s/watchlist/%s' % (content, link().trakt_key)
            elif select == 3:
                url = 'http://api.trakt.tv/%s/unwatchlist/%s' % (content, link().trakt_key)
            else:
                if select == 4:
                    new = common.getUserInput(language(30425).encode("utf-8"), '')
                    if (new == None or new == ''): return
                    url = 'http://api.trakt.tv/lists/add/%s' % link().trakt_key
                    post = {"name": new, "privacy": "private", "description": ""}
                    post.update({"username": link().trakt_user, "password": link().trakt_password})
                    result = getUrl(url, post=json.dumps(post), timeout='30').result
                    result = json.loads(result)
                    if result['status'] == 'failure':
                        return index().infoDialog(result['error'].encode("utf-8"), name)
                    slug = result['slug']
                else:
                    slug = slugList[select]

                if select == 4 or not select % 2 == 0:
                    url = 'http://api.trakt.tv/lists/items/add/%s' % link().trakt_key
                else:
                    url = 'http://api.trakt.tv/lists/items/delete/%s' % link().trakt_key

                post = {"slug": slug, "items": [{"type": "movie", "imdb_id": imdb}, {"type": "show", "imdb_id": imdb}]}


            post.update({"username": link().trakt_user, "password": link().trakt_password})
            result = getUrl(url, post=json.dumps(post), timeout='30').result
            result = json.loads(result)

            try: info = result['status'].encode("utf-8")
            except: pass
            try: info = result['message'].encode("utf-8")
            except: pass
            try:
                if result['already_exist'] == 1: info = 'already added'
            except: pass
            try:
                if result['inserted'] == 1: info = 'added successfully'
            except: pass

            index().infoDialog(info, name)
        except:
            return

    def trakt_indicator(self, content=''):
        try:
            if content == 'shows': raise Exception()
            post = urllib.urlencode({'username': link().trakt_user, 'password': link().trakt_password})
            url = link().trakt_watched % (link().trakt_key, link().trakt_user)
            result = getUrl(url, post=post, timeout='30').result
            updated = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
            record = ('movies', link().trakt_user, result, updated)
            if not xbmcvfs.exists(dataPath): xbmcvfs.mkdir(dataPath)
            dbcon = database.connect(addonCache)
            dbcur = dbcon.cursor()
            dbcur.execute("CREATE TABLE IF NOT EXISTS trakt (""info TEXT, ""user TEXT, ""result TEXT, ""updated TEXT, ""UNIQUE(info, user)"");")
            dbcur.execute("DELETE FROM trakt WHERE info = '%s' AND user = '%s'" % (record[0], record[1]))
            dbcur.execute("INSERT INTO trakt Values (?, ?, ?, ?)", record)
            dbcon.commit()
        except:
            pass

        try:
            if content == 'movies': raise Exception()
            post = urllib.urlencode({'username': link().trakt_user, 'password': link().trakt_password})
            url = link().trakt_tv_watched % (link().trakt_key, link().trakt_user)
            result = getUrl(url, post=post, timeout='30').result
            updated = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
            record = ('shows', link().trakt_user, result, updated)
            if not xbmcvfs.exists(dataPath): xbmcvfs.mkdir(dataPath)
            dbcon = database.connect(addonCache)
            dbcur = dbcon.cursor()
            dbcur.execute("CREATE TABLE IF NOT EXISTS trakt (""info TEXT, ""user TEXT, ""result TEXT, ""updated TEXT, ""UNIQUE(info, user)"");")
            dbcur.execute("DELETE FROM trakt WHERE info = '%s' AND user = '%s'" % (record[0], record[1]))
            dbcur.execute("INSERT INTO trakt Values (?, ?, ?, ?)", record)
            dbcon.commit()
        except:
            pass

    def playcount_movies(self, title, year, imdb, watched):
        try:
            metaget.get_meta('movie', title ,year=year)
            metaget.change_watched('movie', '', imdb, season='', episode='', year='', watched=watched)
        except:
            pass

        try:
            if (link().trakt_user == '' or link().trakt_password == ''): raise Exception()
            if not imdb.startswith('tt'): imdb = 'tt' + imdb
            if watched == 7: url = 'http://api.trakt.tv/movie/seen/%s' % link().trakt_key
            else: url = 'http://api.trakt.tv/movie/unseen/%s' % link().trakt_key
            post = {"movies": [{"imdb_id": imdb}], "username": link().trakt_user, "password": link().trakt_password}
            result = getUrl(url, post=json.dumps(post), timeout='30').result
            self.trakt_indicator('movies')
        except:
            pass

        index().container_refresh()

    def playcount_episodes(self, imdb, season, episode, watched):
        try:
            metaget.get_meta('tvshow', '', imdb_id=imdb)
            metaget.get_episode_meta('', imdb, season, episode)
            metaget.change_watched('episode', '', imdb, season=season, episode=episode, year='', watched=watched)
        except:
            pass

        try:
            if (link().trakt_user == '' or link().trakt_password == ''): raise Exception()
            if not imdb.startswith('tt'): imdb = 'tt' + imdb
            season, episode = int('%01d' % int(season)), int('%01d' % int(episode))
            if watched == 7: url = 'http://api.trakt.tv/show/episode/seen/%s' % link().trakt_key
            else: url = 'http://api.trakt.tv/show/episode/unseen/%s' % link().trakt_key
            post = {"imdb_id": imdb, "episodes": [{"season": season, "episode": episode}], "username": link().trakt_user, "password": link().trakt_password}
            result = getUrl(url, post=json.dumps(post), timeout='30').result
            self.trakt_indicator('shows')
        except:
            pass

        index().container_refresh()

    def playcount_shows(self, name, year, imdb, tvdb, season, watched):
        dialog = xbmcgui.DialogProgress()
        dialog.create(addonName.encode("utf-8"), str(name))
        dialog.update(0, str(name), language(30361).encode("utf-8") + '...')

        try:
            match = episodes().get(name, year, imdb, tvdb, season, idx=False)
            match = match[1]['episodes']
            match = [{'name': i['name'], 'season': int('%01d' % int(i['season'])), 'episode': int('%01d' % int(i['episode']))} for i in match]
        except:
            pass

        try:
            metaget.get_meta('tvshow', '', imdb_id=imdb)

            for i in range(len(match)):
                if xbmc.abortRequested == True: return sys.exit()
                if dialog.iscanceled(): return dialog.close()

                dialog.update(int((100 / float(len(match))) * i), str(name), str(match[i]['name']))

                season, episode = match[i]['season'], match[i]['episode']
                metaget.get_episode_meta('', imdb, season, episode)
                metaget.change_watched('episode', '', imdb, season=season, episode=episode, year='', watched=watched)
        except:
            pass

        try:
            if (link().trakt_user == '' or link().trakt_password == ''): raise Exception()
            if not imdb.startswith('tt'): imdb = 'tt' + imdb
            if watched == 7: url = 'http://api.trakt.tv/show/episode/seen/%s' % link().trakt_key
            else: url = 'http://api.trakt.tv/show/episode/unseen/%s' % link().trakt_key
            post = {"imdb_id": imdb, "episodes": match, "username": link().trakt_user, "password": link().trakt_password}
            result = getUrl(url, post=json.dumps(post), timeout='30').result
        except:
            pass

        dialog.close()

    def library_movie_add(self, name, title, year, imdb, url):
        self.library_movie_processor(name, title, year, imdb, url)

        index().infoDialog(language(30309).encode("utf-8"), name)
        if getSetting("update_library") == 'true' and not xbmc.getCondVisibility('Library.IsScanningVideo'):
            xbmc.executebuiltin('UpdateLibrary(video)')

    def library_movie_list(self, url):
        if xbmc.getInfoLabel('Container.FolderPath').endswith('root_tools'):
            yes = index().yesnoDialog(language(30347).encode("utf-8"), '')
            if not yes: return

        if url == 'trakt_collection':
            url = link().trakt_collection % (link().trakt_key, link().trakt_user)
        elif url == 'trakt_watchlist':
            url = link().trakt_watchlist % (link().trakt_key, link().trakt_user)
        elif url == 'imdb_watchlist':
            url = link().imdb_watchlist % link().imdb_user

        try:
            dialog = xbmcgui.DialogProgress()
            dialog.create(addonName.encode("utf-8"), language(30408).encode("utf-8"))
            dialog.update(0, language(30408).encode("utf-8"), language(30361).encode("utf-8") + '...')

            match = movies().get(url, idx=False)
            if match == None: return dialog.close()

            dialog.update(50, language(30408).encode("utf-8"), str(len(match)) + ' ' + language(30362).encode("utf-8"))
            xbmc.sleep(1000)

            for i in range(len(match)):
                if xbmc.abortRequested == True: return sys.exit()
                if dialog.iscanceled(): return dialog.close()
                self.library_movie_processor(match[i]['name'], match[i]['title'], match[i]['year'], match[i]['imdb'], match[i]['url'])

            dialog.close()
        except:
            return

        index().infoDialog(language(30309).encode("utf-8"))
        if getSetting("update_library") == 'true' and not xbmc.getCondVisibility('Library.IsScanningVideo'):
            xbmc.executebuiltin('UpdateLibrary(video)')

    def library_movie_processor(self, name, title, year, imdb, url):
        try:
            if getSetting("check_library") == 'true': filter = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.GetMovies", "params": {"filter":{"or": [{"field": "year", "operator": "is", "value": "%s"}, {"field": "year", "operator": "is", "value": "%s"}, {"field": "year", "operator": "is", "value": "%s"}]}, "properties" : ["imdbnumber"]}, "id": 1}' % (year, str(int(year)+1), str(int(year)-1)))
            filter = unicode(filter, 'utf-8', errors='ignore')
            filter = json.loads(filter)['result']['movies']
            filter = [i for i in filter if imdb in i['imdbnumber']][0]
        except:
            filter = []

        try:
            if not filter == []: return
            if not xbmcvfs.exists(dataPath): xbmcvfs.mkdir(dataPath)
            if not xbmcvfs.exists(movieLibrary): xbmcvfs.mkdir(movieLibrary)

            sysname, systitle, sysyear, sysimdb, sysurl = urllib.quote_plus(name), urllib.quote_plus(title), urllib.quote_plus(year), urllib.quote_plus(imdb), urllib.quote_plus(url)
            content = '%s?action=play&name=%s&title=%s&year=%s&imdb=%s&url=%s' % (sys.argv[0], sysname, systitle, sysyear, sysimdb, sysurl)

            enc_name = name.translate(None, '\/:*?"<>|').strip('.')
            folder = os.path.join(movieLibrary, enc_name)
            if not xbmcvfs.exists(folder): xbmcvfs.mkdir(folder)

            stream = os.path.join(folder, enc_name + '.strm')
            file = xbmcvfs.File(stream, 'w')
            file.write(str(content))
            file.close()
        except:
            return

    def library_tv_add(self, name, year, imdb, tvdb):
        self.library_tv_processor(name, year, imdb, tvdb)

        index().infoDialog(language(30310).encode("utf-8"), name)
        if getSetting("update_library") == 'true' and not xbmc.getCondVisibility('Library.IsScanningVideo'):
            xbmc.executebuiltin('UpdateLibrary(video)')

    def library_tv_list(self, url):
        if xbmc.getInfoLabel('Container.FolderPath').endswith('root_tools'):
            yes = index().yesnoDialog(language(30347).encode("utf-8"), '')
            if not yes: return

        if url == 'trakt_tv_collection':
            url = link().trakt_tv_collection % (link().trakt_key, link().trakt_user)
        elif url == 'trakt_tv_watchlist':
            url = link().trakt_tv_watchlist % (link().trakt_key, link().trakt_user)
        elif url == 'imdb_tv_watchlist':
            url = link().imdb_watchlist % link().imdb_user

        try:
            dialog = xbmcgui.DialogProgress()
            dialog.create(addonName.encode("utf-8"), language(30408).encode("utf-8"))
            dialog.update(0, language(30408).encode("utf-8"), language(30361).encode("utf-8") + '...')

            match = shows().get(url, idx=False)
            if match == None: return dialog.close()

            dialog.update(0, language(30408).encode("utf-8"), str(len(match)) + ' ' + language(30362).encode("utf-8"))
            xbmc.sleep(1000)

            for i in range(len(match)):
                if xbmc.abortRequested == True: return sys.exit()
                if dialog.iscanceled(): return dialog.close()
                dialog.update(int((100 / float(len(match))) * i), language(30408).encode("utf-8"), str(match[i]['title']))
                self.library_tv_processor(match[i]['title'], match[i]['year'], match[i]['imdb'], match[i]['tvdb'])

            dialog.close()
        except:
            return

        index().infoDialog(language(30310).encode("utf-8"))
        if getSetting("update_library") == 'true' and not xbmc.getCondVisibility('Library.IsScanningVideo'):
            xbmc.executebuiltin('UpdateLibrary(video)')

    def library_update(self, silent=False):
        try:
            match = []

            seasons, episodes = [], []
            shows = [os.path.join(tvLibrary, i) for i in xbmcvfs.listdir(tvLibrary)[0]]
            for show in shows: seasons += [os.path.join(show, i) for i in xbmcvfs.listdir(show)[0]]
            for season in seasons: episodes += [os.path.join(season, i) for i in xbmcvfs.listdir(season)[1] if i.endswith('.strm')]

            for episode in episodes:
                try:
                    file = xbmcvfs.File(episode)
                    read = file.read()
                    read = read.encode("utf-8")
                    file.close()
                    if not read.startswith(sys.argv[0]): raise Exception()
                    params = {}
                    query = read[read.find('?') + 1:].split('&')
                    for i in query: params[i.split('=')[0]] = i.split('=')[1]
                    show, year, imdb, tvdb = urllib.unquote_plus(params["show"]), urllib.unquote_plus(params["year"]), urllib.unquote_plus(params["imdb"]), urllib.unquote_plus(params["tvdb"])
                    match.append({'show': show, 'year': year, 'imdb': imdb, 'tvdb': tvdb})
                except:
                    pass

            match = [i for x, i in enumerate(match) if i not in match[x + 1:]]
            if len(match) == 0: return
        except:
            return

        try:
            if silent == False:
                dialog = xbmcgui.DialogProgress()
                dialog.create(addonName.encode("utf-8"), language(30363).encode("utf-8"))

            for i in range(len(match)):
                if xbmc.abortRequested == True: return sys.exit()
                if silent == False:
                    if dialog.iscanceled(): return dialog.close()
                    dialog.update(int((100 / float(len(match))) * i), language(30363).encode("utf-8"), str(match[i]['show']))
                self.library_tv_processor(match[i]['show'], match[i]['year'], match[i]['imdb'], match[i]['tvdb'], limit=True)

            if silent == False: dialog.close()
        except:
            return

        if silent == False:
            index().infoDialog(language(30311).encode("utf-8"))
        if getSetting("update_library") == 'true' and not xbmc.getCondVisibility('Library.IsScanningVideo'):
            xbmc.executebuiltin('UpdateLibrary(video)')

    def library_tv_processor(self, name, year, imdb, tvdb, limit=False):
        try:
            match = episodes().get(name, year, imdb, tvdb, idx=False)
            match = match[1]['episodes']
        except:
            return

        try:
            filter = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.GetTVShows", "params": {"properties" : ["title", "imdbnumber"]}, "id": 1}')
            filter = unicode(filter, 'utf-8', errors='ignore')
            filter = json.loads(filter)['result']['tvshows']
            filter = [i['title'].encode("utf-8") for i in filter if match[0]['tvdb'] in i['imdbnumber']][0]
            filter = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.GetEpisodes", "params": {"filter":{"and": [{"field": "tvshow", "operator": "is", "value": "%s"}]}, "properties": ["season", "episode"]}, "id": 1}' % filter)
            filter = unicode(filter, 'utf-8', errors='ignore')
            filter = json.loads(filter)['result']['episodes']
            filter = ['S%02dE%02d' % (int(i['season']), int(i['episode'])) for i in filter]
        except:
            filter = []

        try:
            match = [{'name': i['name'], 'title': i['title'], 'year': i['year'], 'imdb': i['imdb'], 'tvdb': i['tvdb'], 'season': i['season'], 'episode': i['episode'], 'show': i['show'], 'show_alt': i['show_alt'], 'date': i['date'], 'genre': i['genre'], 'url': i['url'], 'filter': 'S%02dE%02d' % (int(i['season']), int(i['episode']))} for i in match]
            if getSetting("service_limit") == 'true' and limit == True:
                match = [i for i in match if i['season'] == match[-1]['season']]
            if getSetting("check_library") == 'true':
                match = [i for i in match if not i['filter'] in filter]
        except:
            return

        for i in match:
            try:
                if not xbmcvfs.exists(dataPath): xbmcvfs.mkdir(dataPath)
                if not xbmcvfs.exists(tvLibrary): xbmcvfs.mkdir(tvLibrary)

                name, title, year, imdb, tvdb, season, episode, show, show_alt, date, genre, url = i['name'], i['title'], i['year'], i['imdb'], i['tvdb'], i['season'], i['episode'], i['show'], i['show_alt'], i['date'], i['genre'], i['url']
                sysname, systitle, sysyear, sysimdb, systvdb, sysseason, sysepisode, sysshow, sysshow_alt, sysdate, sysgenre, sysurl = urllib.quote_plus(name), urllib.quote_plus(title), urllib.quote_plus(year), urllib.quote_plus(imdb), urllib.quote_plus(tvdb), urllib.quote_plus(season), urllib.quote_plus(episode), urllib.quote_plus(show), urllib.quote_plus(show_alt), urllib.quote_plus(date), urllib.quote_plus(genre), urllib.quote_plus(url)
                content = '%s?action=play&name=%s&title=%s&year=%s&imdb=%s&tvdb=%s&season=%s&episode=%s&show=%s&show_alt=%s&date=%s&genre=%s&url=%s' % (sys.argv[0], sysname, systitle, sysyear, sysimdb, systvdb, sysseason, sysepisode, sysshow, sysshow_alt, sysdate, sysgenre, sysurl)

                enc_show = show_alt.translate(None, '\/:*?"<>|').strip('.')
                folder = os.path.join(tvLibrary, enc_show)
                if not xbmcvfs.exists(folder): xbmcvfs.mkdir(folder)

                enc_season = 'Season %s' % season.translate(None, '\/:*?"<>|').strip('.')
                folder = os.path.join(folder, enc_season)
                if not xbmcvfs.exists(folder): xbmcvfs.mkdir(folder)

                enc_name = name.translate(None, '\/:*?"<>|').strip('.')
                stream = os.path.join(folder, enc_name + '.strm')
                file = xbmcvfs.File(stream, 'w')
                file.write(str(content))
                file.close()
            except:
                pass

    def download(self, name, url, provider):
        try:
            property = (addonName+name)+'download'
            download = xbmc.translatePath(getSetting("downloads"))
            enc_name = name.translate(None, '\/:*?"<>|').strip('.')
            xbmcvfs.mkdir(dataPath)
            xbmcvfs.mkdir(download)

            file = [i for i in xbmcvfs.listdir(download)[1] if i.startswith(enc_name + '.')]
            if not file == []: file = os.path.join(download, file[0])
            else: file = None

            if download == '':
            	yes = index().yesnoDialog(language(30341).encode("utf-8"), language(30342).encode("utf-8"))
            	if yes: contextMenu().settings_open()
            	return

            if file == None:
            	pass
            elif not file.endswith('.tmp'):
            	yes = index().yesnoDialog(language(30343).encode("utf-8"), language(30344).encode("utf-8"), name)
            	if yes:
            	    xbmcvfs.delete(file)
            	else:
            	    return
            elif file.endswith('.tmp'):
            	if index().getProperty(property) == 'open':
            	    yes = index().yesnoDialog(language(30345).encode("utf-8"), language(30346).encode("utf-8"), name)
            	    if yes: index().setProperty(property, 'cancel')
            	    return
            	else:
            	    xbmcvfs.delete(file)

            url = resolver().sources_resolve(url, provider)
            if url == None: return
            url = url.rsplit('|', 1)[0]
            ext = url.rsplit('/', 1)[-1].rsplit('?', 1)[0].rsplit('|', 1)[0].strip().lower()
            ext = os.path.splitext(ext)[1][1:]
            if ext == '' or ext == 'php': ext = 'mp4'
            stream = os.path.join(download, enc_name + '.' + ext)
            temp = stream + '.tmp'

            count = 0
            CHUNK = 16 * 1024
            request = urllib2.Request(url)
            request.add_header('User-Agent', 'Mozilla/5.0 (iPhone; CPU; CPU iPhone OS 4_0 like Mac OS X; en-us) AppleWebKit/532.9 (KHTML, like Gecko) Version/4.0.5 Mobile/8A293 Safari/6531.22.7')
            request.add_header('Cookie', 'video=true')
            response = urllib2.urlopen(request, timeout=5)
            size = response.info()["Content-Length"]

            file = xbmcvfs.File(temp, 'w')
            index().setProperty(property, 'open')
            index().infoDialog(language(30306).encode("utf-8"), name)
            while True:
            	chunk = response.read(CHUNK)
            	if not chunk: break
            	if index().getProperty(property) == 'cancel': raise Exception()
            	if xbmc.abortRequested == True: raise Exception()
            	part = xbmcvfs.File(temp)
            	quota = int(100 * float(part.size())/float(size))
            	part.close()
            	if not count == quota and count in [0,10,20,30,40,50,60,70,80,90]:
            		index().infoDialog(language(30307).encode("utf-8") + str(count) + '%', name)
            	file.write(chunk)
            	count = quota
            response.close()
            file.close()

            index().clearProperty(property)
            xbmcvfs.rename(temp, stream)
            index().infoDialog(language(30308).encode("utf-8"), name)
        except:
            file.close()
            index().clearProperty(property)
            xbmcvfs.delete(temp)
            sys.exit()
            return

    def toggle_playback(self, content, name, title, year, imdb, tvdb, season, episode, show, show_alt, date, genre):
        if content == 'movie':
            meta = {'title': xbmc.getInfoLabel('ListItem.title'), 'originaltitle': xbmc.getInfoLabel('ListItem.originaltitle'), 'year': xbmc.getInfoLabel('ListItem.year'), 'genre': xbmc.getInfoLabel('ListItem.genre'), 'studio' : xbmc.getInfoLabel('ListItem.studio'), 'country' : xbmc.getInfoLabel('ListItem.country'), 'duration' : xbmc.getInfoLabel('ListItem.duration'), 'rating': xbmc.getInfoLabel('ListItem.rating'), 'votes': xbmc.getInfoLabel('ListItem.votes'), 'mpaa': xbmc.getInfoLabel('ListItem.mpaa'), 'director': xbmc.getInfoLabel('ListItem.director'), 'writer': xbmc.getInfoLabel('ListItem.writer'), 'plot': xbmc.getInfoLabel('ListItem.plot'), 'plotoutline': xbmc.getInfoLabel('ListItem.plotoutline'), 'tagline': xbmc.getInfoLabel('ListItem.tagline')}
            label, poster, thumb, fanart = xbmc.getInfoLabel('ListItem.label'), xbmc.getInfoLabel('ListItem.icon'), xbmc.getInfoLabel('ListItem.icon'), xbmc.getInfoLabel('ListItem.Property(Fanart_Image)')
            sysname, systitle, sysyear, sysimdb = urllib.quote_plus(name), urllib.quote_plus(title), urllib.quote_plus(year), urllib.quote_plus(imdb)
            u = '%s?action=play&name=%s&title=%s&year=%s&imdb=%s' % (sys.argv[0], sysname, systitle, sysyear, sysimdb)

        elif content == 'episode':
            meta = {'title': xbmc.getInfoLabel('ListItem.title'), 'season' : xbmc.getInfoLabel('ListItem.season'), 'episode': xbmc.getInfoLabel('ListItem.episode'), 'tvshowtitle': xbmc.getInfoLabel('ListItem.tvshowtitle'), 'studio': xbmc.getInfoLabel('ListItem.studio'), 'premiered' : xbmc.getInfoLabel('ListItem.premiered'), 'duration' : xbmc.getInfoLabel('ListItem.duration'), 'rating': xbmc.getInfoLabel('ListItem.rating'), 'mpaa' : xbmc.getInfoLabel('ListItem.mpaa'), 'director': xbmc.getInfoLabel('ListItem.director'), 'writer': xbmc.getInfoLabel('ListItem.writer'), 'plot': xbmc.getInfoLabel('ListItem.plot')}
            label, poster, thumb, fanart = xbmc.getInfoLabel('ListItem.label'), xbmc.getInfoLabel('ListItem.Art(tvshow.poster)'), xbmc.getInfoLabel('ListItem.icon'), xbmc.getInfoLabel('ListItem.Property(Fanart_Image)')
            sysname, systitle, sysyear, sysimdb, systvdb, sysseason, sysepisode, sysshow, sysshow_alt, sysdate, sysgenre = urllib.quote_plus(name), urllib.quote_plus(title), urllib.quote_plus(year), urllib.quote_plus(imdb), urllib.quote_plus(tvdb), urllib.quote_plus(season), urllib.quote_plus(episode), urllib.quote_plus(show), urllib.quote_plus(show_alt), urllib.quote_plus(date), urllib.quote_plus(genre)
            u = '%s?action=play&name=%s&title=%s&year=%s&imdb=%s&tvdb=%s&season=%s&episode=%s&show=%s&show_alt=%s&date=%s&genre=%s' % (sys.argv[0], sysname, systitle, sysyear, sysimdb, systvdb, sysseason, sysepisode, sysshow, sysshow_alt, sysdate, sysgenre)

        autoplay = getSetting("autoplay")
        if not xbmc.getInfoLabel('Container.FolderPath').startswith(sys.argv[0]):
            autoplay = getSetting("autoplay_library")
        if autoplay == 'false': u += '&url=direct://'
        else: u += '&url=dialog://'

        playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playlist.clear()
        item = xbmcgui.ListItem(label, iconImage="DefaultVideo.png", thumbnailImage=thumb)
        try: item.setArt({'poster': poster, 'tvshow.poster': poster, 'season.poster': poster})
        except: pass
        item.setProperty("Fanart_Image", fanart)
        item.setInfo(type="Video", infoLabels = meta)
        item.setProperty("Video", "true")
        item.setProperty("IsPlayable", "true")
        xbmc.Player().play(u, item)

    def trailer(self, name, url):
        url = trailer().run(name, url)
        if url == None: return
        item = xbmcgui.ListItem(path=url)
        item.setProperty("IsPlayable", "true")
        xbmc.Player().play(url, item)

class root:
    def get(self):
        rootList = []
        rootList.append({'name': 30501, 'image': 'root_movies.jpg', 'action': 'root_movies'})
        rootList.append({'name': 30502, 'image': 'root_shows.jpg', 'action': 'root_shows'})
        rootList.append({'name': 30503, 'image': 'channels_movies.jpg', 'action': 'channels_movies'})
        rootList.append({'name': 30504, 'image': 'root_genesis.jpg', 'action': 'root_genesis'})
        rootList.append({'name': 30505, 'image': 'movies_added.jpg', 'action': 'movies_added'})
        rootList.append({'name': 30506, 'image': 'episodes_added.jpg', 'action': 'episodes_added'})
        rootList.append({'name': 30507, 'image': 'calendar_episodes.jpg', 'action': 'calendar_episodes'})
        rootList.append({'name': 30508, 'image': 'root_tools.jpg', 'action': 'root_tools'})
        rootList.append({'name': 30509, 'image': 'root_search.jpg', 'action': 'root_search'})
        index().rootList(rootList)

    def movies(self):
        rootList = []
        rootList.append({'name': 30521, 'image': 'genres_movies.jpg', 'action': 'genres_movies'})
        rootList.append({'name': 30522, 'image': 'languages_movies.jpg', 'action': 'languages_movies'})
        rootList.append({'name': 30523, 'image': 'movies_boxoffice.jpg', 'action': 'movies_boxoffice'})
        rootList.append({'name': 30524, 'image': 'years_movies.jpg', 'action': 'years_movies'})
        rootList.append({'name': 30525, 'image': 'movies_trending.jpg', 'action': 'movies_trending'})
        rootList.append({'name': 30526, 'image': 'movies_popular.jpg', 'action': 'movies_popular'})
        rootList.append({'name': 30527, 'image': 'movies_views.jpg', 'action': 'movies_views'})
        rootList.append({'name': 30528, 'image': 'movies_oscars.jpg', 'action': 'movies_oscars'})
        rootList.append({'name': 30529, 'image': 'movies_theaters.jpg', 'action': 'movies_theaters'})
        rootList.append({'name': 30530, 'image': 'actors_movies.jpg', 'action': 'actors_movies'})
        rootList.append({'name': 30531, 'image': 'movies_search.jpg', 'action': 'movies_search'})
        index().rootList(rootList)

    def shows(self):
        rootList = []
        rootList.append({'name': 30541, 'image': 'genres_shows.jpg', 'action': 'genres_shows'})
        rootList.append({'name': 30542, 'image': 'shows_popular.jpg', 'action': 'shows_popular'})
        rootList.append({'name': 30543, 'image': 'shows_active.jpg', 'action': 'shows_active'})
        rootList.append({'name': 30544, 'image': 'shows_trending.jpg', 'action': 'shows_trending'})
        rootList.append({'name': 30545, 'image': 'shows_rating.jpg', 'action': 'shows_rating'})
        rootList.append({'name': 30546, 'image': 'shows_views.jpg', 'action': 'shows_views'})
        rootList.append({'name': 30547, 'image': 'actors_shows.jpg', 'action': 'actors_shows'})
        rootList.append({'name': 30548, 'image': 'shows_search.jpg', 'action': 'shows_search'})
        index().rootList(rootList)

    def genesis(self):
        rootList = []
        if not (link().trakt_user == '' or link().trakt_password == ''):
            rootList.append({'name': 30561, 'image': 'movies_trakt_collection.jpg', 'action': 'movies_trakt_collection'})
            rootList.append({'name': 30562, 'image': 'shows_trakt_collection.jpg', 'action': 'shows_trakt_collection'})
            rootList.append({'name': 30563, 'image': 'movies_trakt_watchlist.jpg', 'action': 'movies_trakt_watchlist'})
            rootList.append({'name': 30564, 'image': 'shows_trakt_watchlist.jpg', 'action': 'shows_trakt_watchlist'})
        if not (link().imdb_user == ''):
            rootList.append({'name': 30565, 'image': 'movies_imdb_watchlist.jpg', 'action': 'movies_imdb_watchlist'})
            rootList.append({'name': 30566, 'image': 'shows_imdb_watchlist.jpg', 'action': 'shows_imdb_watchlist'})
        if not (link().trakt_user == '' or link().trakt_password == '') or not (link().imdb_user == ''):
            rootList.append({'name': 30567, 'image': 'userlists_movies.jpg', 'action': 'userlists_movies'})
            rootList.append({'name': 30568, 'image': 'userlists_shows.jpg', 'action': 'userlists_shows'})
        rootList.append({'name': 30569, 'image': 'movies_favourites.jpg', 'action': 'movies_favourites'})
        rootList.append({'name': 30570, 'image': 'shows_favourites.jpg', 'action': 'shows_favourites'})
        rootList.append({'name': 30571, 'image': 'folder_downloads.jpg', 'action': 'folder_downloads'})
        index().rootList(rootList)

    def search(self):
        rootList = []
        rootList.append({'name': 30581, 'image': 'movies_search.jpg', 'action': 'movies_search'})
        rootList.append({'name': 30582, 'image': 'shows_search.jpg', 'action': 'shows_search'})
        rootList.append({'name': 30583, 'image': 'actors_movies.jpg', 'action': 'actors_movies'})
        rootList.append({'name': 30584, 'image': 'actors_shows.jpg', 'action': 'actors_shows'})
        index().rootList(rootList)

    def tools(self):
        rootList = []
        rootList.append({'name': 30601, 'image': 'settings_open.jpg', 'action': 'settings_open'})
        rootList.append({'name': 30602, 'image': 'settings_metahandler.jpg', 'action': 'settings_metahandler'})
        rootList.append({'name': 30603, 'image': 'settings_urlresolver.jpg', 'action': 'settings_urlresolver'})
        rootList.append({'name': 30604, 'image': 'cache_clear.jpg', 'action': 'cache_clear'})
        rootList.append({'name': 30605, 'image': 'library_update.jpg', 'action': 'library_update'})
        if not (link().trakt_user == '' or link().trakt_password == ''):
            rootList.append({'name': 30606, 'image': 'movies_trakt_collection.jpg', 'action': 'library_trakt_collection'})
            rootList.append({'name': 30607, 'image': 'shows_trakt_collection.jpg', 'action': 'library_tv_trakt_collection'})
            rootList.append({'name': 30608, 'image': 'movies_trakt_watchlist.jpg', 'action': 'library_trakt_watchlist'})
            rootList.append({'name': 30609, 'image': 'shows_trakt_watchlist.jpg', 'action': 'library_tv_trakt_watchlist'})
        if not (link().imdb_user == ''):
            rootList.append({'name': 30610, 'image': 'movies_imdb_watchlist.jpg', 'action': 'library_imdb_watchlist'})
            rootList.append({'name': 30611, 'image': 'shows_imdb_watchlist.jpg', 'action': 'library_tv_imdb_watchlist'})
        rootList.append({'name': 30612, 'image': 'folder_movie.jpg', 'action': 'folder_movie'})
        rootList.append({'name': 30613, 'image': 'folder_tv.jpg', 'action': 'folder_tv'})
        index().rootList(rootList)


class link:
    def __init__(self):
        self.imdb_base = 'http://www.imdb.com'
        self.imdb_akas = 'http://akas.imdb.com'
        self.imdb_mobile = 'http://m.imdb.com'
        self.imdb_genre = 'http://akas.imdb.com/genre/'
        self.imdb_language = 'http://akas.imdb.com/language/'
        self.imdb_title = 'http://www.imdb.com/title/tt%s/'
        self.imdb_media = 'http://ia.media-imdb.com'
        self.imdb_seasons = 'http://akas.imdb.com/title/tt%s/episodes'
        self.imdb_episodes = 'http://www.imdb.com/title/tt%s/episodes?season=%s'
        self.imdb_image = 'http://i.media-imdb.com/images/SFaa265aa19162c9e4f3781fbae59f856d/nopicture/medium/film.png'
        self.imdb_tv_image = 'http://i.media-imdb.com/images/SF1b61b592d2fa1b9cfb8336f160e1efcf/nopicture/medium/tv.png'
        self.imdb_genres = 'http://akas.imdb.com/search/title?title_type=feature,tv_movie&sort=boxoffice_gross_us&count=25&start=1&genres=%s'
        self.imdb_languages = 'http://akas.imdb.com/search/title?languages=%s|1&title_type=feature,tv_movie&sort=moviemeter,asc&count=25&start=1'
        self.imdb_years = 'http://akas.imdb.com/search/title?title_type=feature,tv_movie&sort=boxoffice_gross_us&count=25&start=1&year=%s,%s'
        self.imdb_popular = 'http://akas.imdb.com/search/title?title_type=feature,tv_movie&sort=moviemeter,asc&count=25&start=1'
        self.imdb_boxoffice = 'http://akas.imdb.com/search/title?title_type=feature,tv_movie&sort=boxoffice_gross_us,desc&count=25&start=1'
        self.imdb_views = 'http://akas.imdb.com/search/title?title_type=feature,tv_movie&sort=num_votes,desc&count=25&start=1'
        self.imdb_oscars = 'http://akas.imdb.com/search/title?title_type=feature,tv_movie&groups=oscar_best_picture_winners&sort=year,desc&count=25&start=1'
        self.imdb_search = 'http://akas.imdb.com/search/title?title_type=feature,short,tv_movie,tv_special,video&sort=moviemeter,asc&count=25&start=1&title=%s'
        self.imdb_tv_genres = 'http://akas.imdb.com/search/title?title_type=tv_series,mini_series&sort=moviemeter,asc&count=25&start=1&genres=%s'
        self.imdb_tv_popular = 'http://akas.imdb.com/search/title?title_type=tv_series,mini_series&sort=moviemeter,asc&count=25&start=1'
        self.imdb_tv_rating = 'http://akas.imdb.com/search/title?title_type=tv_series,mini_series&num_votes=5000,&sort=user_rating,desc&count=25&start=1'
        self.imdb_tv_views = 'http://akas.imdb.com/search/title?title_type=tv_series,mini_series&sort=num_votes,desc&count=25&start=1'
        self.imdb_tv_active = 'http://akas.imdb.com/search/title?title_type=tv_series,mini_series&production_status=active&sort=moviemeter,asc&count=25&start=1'
        self.imdb_tv_search = 'http://akas.imdb.com/search/title?title_type=tv_series,mini_series&sort=moviemeter,asc&count=25&start=1&title=%s'
        self.imdb_api_search = 'http://www.imdb.com/xml/find?json=1&nr=1&tt=on&q=%s'
        self.imdb_actors_search = 'http://www.imdb.com/search/name?count=100&name=%s'
        self.imdb_actors = 'http://akas.imdb.com/search/title?count=25&sort=year,desc&title_type=feature,tv_movie&start=1&role=nm%s'
        self.imdb_tv_actors = 'http://akas.imdb.com/search/title?count=25&sort=year,desc&title_type=tv_series,mini_series&start=1&role=nm%s'
        self.imdb_userlists = 'http://akas.imdb.com/user/ur%s/lists?tab=all&sort=modified:desc&filter=titles'
        self.imdb_watchlist ='http://akas.imdb.com/user/ur%s/watchlist'
        self.imdb_list = 'http://akas.imdb.com/list/%s/?view=detail&sort=title:asc&title_type=feature,short,tv_movie,tv_special,video,documentary,game&start=1'
        self.imdb_tv_list = 'http://akas.imdb.com/list/%s/?view=detail&sort=title:asc&title_type=tv_series,mini_series&start=1'
        self.imdb_user = getSetting("imdb_user").replace('ur', '')

        self.tmdb_base = 'http://api.themoviedb.org'
        self.tmdb_key = base64.urlsafe_b64decode('NTc5ODNlMzFmYjQzNWRmNGRmNzdhZmI4NTQ3NDBlYTk=')
        self.tmdb_info = 'http://api.themoviedb.org/3/movie/tt%s?language=en&api_key=%s'
        self.tmdb_info2 = 'http://api.themoviedb.org/3/movie/%s?language=en&api_key=%s'
        self.tmdb_theaters = 'http://api.themoviedb.org/3/movie/now_playing?api_key=%s&page=1'
        self.tmdb_image = 'http://image.tmdb.org/t/p/original'
        self.tmdb_image2 = 'http://image.tmdb.org/t/p/w500'

        self.tvdb_base = 'http://thetvdb.com'
        self.tvdb_key = base64.urlsafe_b64decode('MUQ2MkYyRjkwMDMwQzQ0NA==')
        self.tvdb_search = 'http://thetvdb.com/api/GetSeriesByRemoteID.php?imdbid=tt%s&language=en'
        self.tvdb_search2 = 'http://thetvdb.com/api/GetSeries.php?seriesname=%s&language=en'
        self.tvdb_info = 'http://thetvdb.com/api/%s/series/%s/all/en.zip'
        self.tvdb_info2 = 'http://thetvdb.com/api/%s/series/%s/en.xml'
        self.tvdb_image = 'http://thetvdb.com/banners/'
        self.tvdb_image2 = 'http://thetvdb.com/banners/_cache/'

        self.trakt_base = 'http://api.trakt.tv'
        self.trakt_key = base64.urlsafe_b64decode('YmU2NDI5MWFhZmJiYmU2MmZkYzRmM2FhMGVkYjQwNzM=')
        self.trakt_user, self.trakt_password = getSetting("trakt_user"), getSetting("trakt_password")
        self.trakt_trending = 'http://api.trakt.tv/movies/trending.json/%s'
        self.trakt_watchlist = 'http://api.trakt.tv/user/watchlist/movies.json/%s/%s'
        self.trakt_collection = 'http://api.trakt.tv/user/library/movies/collection.json/%s/%s/extended'
        self.trakt_watched = 'http://api.trakt.tv/user/library/movies/watched.json/%s/%s/min'
        self.trakt_info = 'http://api.trakt.tv/movie/summaries.json/%s/%s/full'
        self.trakt_tv_search = 'http://api.trakt.tv/show/summary.json/%s/%s'
        self.trakt_tv_trending = 'http://api.trakt.tv/shows/trending.json/%s'
        self.trakt_tv_calendar = 'http://api.trakt.tv/calendar/shows.json/%s/%s/%s'
        self.trakt_tv_user_calendar = 'http://api.trakt.tv/user/calendar/shows.json/%s/%s/%s/%s'
        self.trakt_tv_watchlist = 'http://api.trakt.tv/user/watchlist/shows.json/%s/%s'
        self.trakt_tv_collection = 'http://api.trakt.tv/user/library/shows/collection.json/%s/%s/extended'
        self.trakt_tv_watched = 'http://api.trakt.tv/user/library/shows/watched.json/%s/%s/min'
        self.trakt_tv_info = 'http://api.trakt.tv/show/summaries.json/%s/%s/full'
        self.trakt_lists = 'http://api.trakt.tv/user/lists.json/%s/%s'
        self.trakt_list= 'http://api.trakt.tv/user/list.json/%s/%s'

        self.tvrage_base = 'http://services.tvrage.com'
        self.tvrage_search = 'http://services.tvrage.com/feeds/search.php?show=%s'
        self.tvrage_info = 'http://www.tvrage.com/shows/id-%s/episode_list/all'
        self.epguides_info = 'http://epguides.com/common/exportToCSV.asp?rage=%s'

        self.scn_base = 'http://rapidmoviez.com'
        self.scn_added = 'http://rapidmoviez.com/feature/hd/m/1'
        self.scn_tv_added = 'http://m2v.ru/?func=part&Part=11'

class actors:
    def __init__(self):
        self.list = []

    def movies(self, query=None):
        if query == None:
            self.query = common.getUserInput(language(30382).encode("utf-8"), '')
        else:
            self.query = query
        if not (self.query == None or self.query == ''):
            self.query = link().imdb_actors_search % urllib.quote_plus(self.query)
            self.imdb_list(self.query)
            for i in range(0, len(self.list)): self.list[i].update({'action': 'movies', 'url': link().imdb_actors % self.list[i]['url']})
            index().rootList(self.list)

    def shows(self, query=None):
        if query == None:
            self.query = common.getUserInput(language(30382).encode("utf-8"), '')
        else:
            self.query = query
        if not (self.query == None or self.query == ''):
            self.query = link().imdb_actors_search % urllib.quote_plus(self.query)
            self.imdb_list(self.query)
            for i in range(0, len(self.list)): self.list[i].update({'action': 'shows', 'url': link().imdb_tv_actors % self.list[i]['url']})
            index().rootList(self.list)

    def imdb_list(self, url):
        try:
            result = getUrl(url, timeout='10').result
            result = result.decode('iso-8859-1').encode('utf-8')
            actors = common.parseDOM(result, "tr", attrs = { "class": ".+? detailed" })
        except:
            return
        for actor in actors:
            try:
                name = common.parseDOM(actor, "a", ret="title")[0]
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                url = common.parseDOM(actor, "a", ret="href")[0]
                url = re.findall('nm(\d*)', url, re.I)[0]
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                image = common.parseDOM(actor, "img", ret="src")[0]
                if not ('._SX' in image or '._SY' in image): raise Exception()
                image = image.rsplit('._SX', 1)[0].rsplit('._SY', 1)[0] + '._SX500.' + image.rsplit('.', 1)[-1]
                image = common.replaceHTMLCodes(image)
                image = image.encode('utf-8')

                self.list.append({'name': name, 'url': url, 'image': image})
            except:
                pass

        return self.list

class genres:
    def __init__(self):
        self.list = []

    def movies(self):
        #self.list = self.imdb_list()
        try: self.list = cache3(self.imdb_list)
        except: return
        for i in range(0, len(self.list)): self.list[i].update({'image': 'genres_movies.jpg', 'action': 'movies'})
        index().rootList(self.list)

    def shows(self):
        #self.list = self.imdb_list2()
        try: self.list = cache3(self.imdb_list2)
        except: return
        for i in range(0, len(self.list)): self.list[i].update({'image': 'genres_shows.jpg', 'action': 'shows'})
        index().rootList(self.list)

    def imdb_list(self):
        try:
            result = getUrl(link().imdb_genre, timeout='10').result
            result = common.parseDOM(result, "table", attrs = { "class": "genre-table" })[0]
            genres = common.parseDOM(result, "h3")
        except:
            return

        for genre in genres:
            try:
                name = common.parseDOM(genre, "a")[0]
                name = name.split('<', 1)[0].rsplit('>', 1)[0].strip()
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                url = common.parseDOM(genre, "a", ret="href")[0]
                url = re.compile('/genre/(.+?)/').findall(url)[0]
                if url == 'documentary': raise Exception()
                url = link().imdb_genres % url
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                self.list.append({'name': name, 'url': url})
            except:
                pass

        return self.list

    def imdb_list2(self):
        try:
            result = getUrl(link().imdb_genre, timeout='10').result
            result = common.parseDOM(result, "div", attrs = { "class": "article" })
            result = [i for i in result if str('"tv_genres"') in i][0]
            genres = common.parseDOM(result, "td")
        except:
            return

        for genre in genres:
            try:
                name = common.parseDOM(genre, "a")[0]
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                url = common.parseDOM(genre, "a", ret="href")[0]
                try: url = re.compile('genres=(.+?)&').findall(url)[0]
                except: url = re.compile('/genre/(.+?)/').findall(url)[0]
                url = link().imdb_tv_genres % url
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                self.list.append({'name': name, 'url': url})
            except:
                pass

        return self.list

class languages:
    def __init__(self):
        self.list = []

    def movies(self):
        #self.list = self.imdb_list()
        try: self.list = cache3(self.imdb_list)
        except: return
        for i in range(0, len(self.list)): self.list[i].update({'image': 'languages_movies.jpg', 'action': 'movies'})
        index().rootList(self.list)

    def imdb_list(self):
        try:
            result = getUrl(link().imdb_language, timeout='10').result
            result = common.parseDOM(result, "table", attrs = { "class": "splash" })[0]
            languages = common.parseDOM(result, "td")
        except:
            return

        for language in languages:
            try:
                name = common.parseDOM(language, "a")[0]
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                url = common.parseDOM(language, "a", ret="href")[0]
                url = re.compile('/language/(.+)').findall(url)[0]
                url = link().imdb_languages % url
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                self.list.append({'name': name, 'url': url})
            except:
                pass

        return self.list

class years:
    def __init__(self):
        self.list = []

    def movies(self):
        self.list = self.imdb_list()
        for i in range(0, len(self.list)): self.list[i].update({'image': 'years_movies.jpg', 'action': 'movies'})
        index().rootList(self.list)

    def imdb_list(self):
        year = (datetime.datetime.utcnow() - datetime.timedelta(hours = 5)).strftime("%Y")

        for i in range(int(year)-0, int(year)-50, -1):
            name = str(i).encode('utf-8')
            url = link().imdb_years % (str(i), str(i))
            url = url.encode('utf-8')
            self.list.append({'name': name, 'url': url})

        return self.list

class calendar:
    def __init__(self):
        self.list = []

    def episodes(self):
        self.list = self.trakt_list()
        for i in range(0, len(self.list)): self.list[i].update({'image': 'calendar_episodes.jpg', 'action': 'episodes_calendar'})
        index().rootList(self.list)

    def trakt_list(self):
        now = datetime.datetime.utcnow() - datetime.timedelta(hours = 5)
        today = datetime.date(now.year, now.month, now.day)

        for i in range(0, 14):
            date = today - datetime.timedelta(days=i)
            date = str(date)
            date = date.encode('utf-8')
            self.list.append({'name': date, 'url': date})

        return self.list

class userlists:
    def __init__(self):
        self.list = []

    def movies(self):
        if not (link().trakt_user == '' or link().trakt_password == ''): self.trakt_list()
        if not (link().imdb_user == ''): self.imdb_list()
        for i in range(0, len(self.list)): self.list[i].update({'image': 'userlists_movies.jpg', 'action': 'movies_userlist'})
        index().rootList(self.list)

    def shows(self):
        if not (link().trakt_user == '' or link().trakt_password == ''): self.trakt_list()
        if not (link().imdb_user == ''): self.imdb_list()
        for i in range(0, len(self.list)): self.list[i].update({'image': 'userlists_movies.jpg', 'action': 'shows_userlist', 'url': self.list[i]['url'].replace(link().imdb_list.split('?', 1)[-1], link().imdb_tv_list.split('?', 1)[-1])})
        index().rootList(self.list)

    def trakt_list(self):
        post = urllib.urlencode({'username': link().trakt_user, 'password': link().trakt_password})
        info = (link().trakt_key, link().trakt_user)

        try:
            userlists = []
            result = getUrl(link().trakt_lists % info, post=post, timeout='30').result
            userlists = json.loads(result)
        except:
            pass

        for userlist in userlists:
            try:
                name = userlist['name']
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                url = userlist['slug']
                url = '%s/%s' % (link().trakt_list % info, url)
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                self.list.append({'name': name, 'url': url})
            except:
                pass

        return self.list

    def imdb_list(self):
        try:
            userlists = []
            result = getUrl(link().imdb_userlists % link().imdb_user, timeout='30').result
            result = result.decode('iso-8859-1').encode('utf-8')
            userlists = common.parseDOM(result, "div", attrs = { "class": "list_name" })
        except:
            pass

        for userlist in userlists:
            try:
                name = common.parseDOM(userlist, "a")[0]
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                url = common.parseDOM(userlist, "a", ret="href")[0]
                url = url.split('/list/', 1)[-1].replace('/', '')
                url = link().imdb_list % url
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                self.list.append({'name': name, 'url': url})
            except:
                pass

        return self.list

class channels:
    def __init__(self):
        self.list = []
        self.sky_now_link = 'http://epgservices.sky.com/5.1.1/api/2.0/channel/json/%s/now/nn/0'
        self.sky_programme_link = 'http://tv.sky.com/programme/channel/%s/%s/%s.json'

    def movies(self):
        threads = []

        threads.append(Thread(self.sky_list, '01', 'Sky Premiere', '1409'))
        threads.append(Thread(self.sky_list, '02', 'Sky Premiere +1', '1823'))
        threads.append(Thread(self.sky_list, '03', 'Sky Showcase', '1814'))
        threads.append(Thread(self.sky_list, '04', 'Sky Greats', '1815'))
        threads.append(Thread(self.sky_list, '05', 'Sky Disney', '1838'))
        threads.append(Thread(self.sky_list, '06', 'Sky Family', '1808'))
        threads.append(Thread(self.sky_list, '07', 'Sky Action', '1001'))
        threads.append(Thread(self.sky_list, '08', 'Sky Comedy', '1002'))
        threads.append(Thread(self.sky_list, '09', 'Sky Crime', '1818'))
        threads.append(Thread(self.sky_list, '10', 'Sky Drama', '1816'))
        threads.append(Thread(self.sky_list, '11', 'Sky Sci Fi', '1807'))
        threads.append(Thread(self.sky_list, '12', 'Sky Select', '1811'))

        [i.start() for i in threads]
        [i.join() for i in threads]

        threads = []
        for i in range(0, len(self.list)): threads.append(Thread(self.imdb_search, i))
        [i.start() for i in threads]
        [i.join() for i in threads]

        self.list = [i for i in self.list if not i['imdb'] == '0']
        self.list = sorted(self.list, key=itemgetter('num'))

        threads = []
        for i in range(0, len(self.list)): threads.append(Thread(self.tmdb_info, i))
        [i.start() for i in threads]
        [i.join() for i in threads]

        index().channelList(self.list)

    def sky_list(self, num, channel, id):
        try:
            url = self.sky_now_link % id
            result = getUrl(url, timeout='10').result
            result = json.loads(result)
            match = result['listings'][id][0]['url']

            dt = self.uk_datetime()
            dt1 = '%04d' % dt.year + '-' + '%02d' % dt.month + '-' + '%02d' % dt.day
            dt2 = int(dt.hour)
            if (dt2 < 6): dt2 = 0
            elif (dt2 >= 6 and dt2 < 12): dt2 = 1
            elif (dt2 >= 12 and dt2 < 18): dt2 = 2
            elif (dt2 >= 18): dt2 = 3
            url = self.sky_programme_link % (id, str(dt1), str(dt2))

            result = getUrl(url, timeout='10').result
            result = json.loads(result)
            result = result['listings'][id]
            result = [i for i in result if i['url'] == match][0]

            year = result['d']
            year = re.findall('.+?[(](\d{4})[)]', year)[0].strip()
            year = year.encode('utf-8')

            title = result['t']
            title = title.replace('(%s)' % year, '').strip()
            title = common.replaceHTMLCodes(title)
            title = title.encode('utf-8')

            self.list.append({'name': channel, 'title': title, 'year': year, 'imdb': '0', 'tvdb': '0', 'season': '0', 'episode': '0', 'show': '0', 'show_alt': '0', 'date': '0', 'genre': '0', 'url': '0', 'poster': '0', 'fanart': '0', 'studio': '0', 'duration': '0', 'rating': '0', 'votes': '0', 'mpaa': '0', 'director': '0', 'plot': '0', 'plotoutline': '0', 'tagline': '0', 'num': num})
        except:
            return

    def imdb_search(self, i):
        try:
            match = []
            title = self.list[i]['title']
            year = self.list[i]['year']
            search = link().imdb_api_search % urllib.quote_plus(title)
            result = getUrl(search, timeout='10').result
            result = json.loads(result)
            for x in result.keys(): match += result[x]
            clean = '\n|([[].+?[]])|([(].+?[)])|\s(vs|v[.])\s|(:|;|-|"|,|\'|\.|\?)|\s'
            match = [x for x in match if re.sub(clean, '', title).lower() == re.sub(clean, '', x['title']).lower() and any(x['title_description'].startswith(y) for y in [str(year), str(int(year)+1), str(int(year)-1)])][0]

            title = match['title']
            title = common.replaceHTMLCodes(title)
            title = title.encode('utf-8')

            imdb = match['id']
            imdb = re.sub('[^0-9]', '', str(imdb))
            imdb = imdb.encode('utf-8')

            url = link().imdb_title % imdb
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            self.list[i].update({'title': title, 'imdb': imdb, 'url': url})
        except:
            pass

    def tmdb_info(self, i):
        try:
            url = link().tmdb_info % (self.list[i]['imdb'], link().tmdb_key)
            result = getUrl(url, timeout='10').result
            result = json.loads(result)

            poster = result['poster_path']
            if poster == '' or poster == None: poster = '0'
            if not poster == '0': poster = '%s%s' % (link().tmdb_image2, poster)
            poster = common.replaceHTMLCodes(poster)
            poster = poster.encode('utf-8')
            if not poster == '0': self.list[i].update({'poster': poster})

            fanart = result['backdrop_path']
            if fanart == '' or fanart == None: fanart = '0'
            if not fanart == '0': fanart = '%s%s' % (link().tmdb_image, fanart)
            fanart = common.replaceHTMLCodes(fanart)
            fanart = fanart.encode('utf-8')
            if not fanart == '0': self.list[i].update({'fanart': fanart})

            genre = result['genres']
            try: genre = [x['name'] for x in genre]
            except: genre = '0'
            if genre == '' or genre == None or genre == []: genre = '0'
            genre = " / ".join(genre)
            genre = common.replaceHTMLCodes(genre)
            genre = genre.encode('utf-8')
            if not genre == '0': self.list[i].update({'genre': genre})

            studio = result['production_companies']
            try: studio = [x['name'] for x in studio][0]
            except: studio = '0'
            if studio == '' or studio == None: studio = '0'
            studio = common.replaceHTMLCodes(studio)
            studio = studio.encode('utf-8')
            if not studio == '0': self.list[i].update({'studio': studio})

            try: duration = str(result['runtime'])
            except: duration = '0'
            if duration == '' or duration == None or not self.list[i]['duration'] == '0': duration = '0'
            duration = common.replaceHTMLCodes(duration)
            duration = duration.encode('utf-8')
            if not duration == '0': self.list[i].update({'duration': duration})

            rating = str(result['vote_average'])
            if rating == '' or rating == None or not self.list[i]['rating'] == '0': rating = '0'
            rating = common.replaceHTMLCodes(rating)
            rating = rating.encode('utf-8')
            if not rating == '0': self.list[i].update({'rating': rating})

            votes = str(result['vote_count'])
            try: votes = str(format(int(votes),',d'))
            except: pass
            if votes == '' or votes == None or not self.list[i]['votes'] == '0': votes = '0'
            votes = common.replaceHTMLCodes(votes)
            votes = votes.encode('utf-8')
            if not votes == '0': self.list[i].update({'votes': votes})

            plot = result['overview']
            if plot == '' or plot == None: plot = '0'
            plot = common.replaceHTMLCodes(plot)
            plot = plot.encode('utf-8')
            if not plot == '0': self.list[i].update({'plot': plot})

            tagline = result['tagline']
            if (tagline == '' or tagline == None) and not plot == '0': tagline = plot.split('.', 1)[0]
            elif tagline == '' or tagline == None: tagline = '0'
            tagline = common.replaceHTMLCodes(tagline)
            tagline = tagline.encode('utf-8')
            if not tagline == '0': self.list[i].update({'tagline': tagline})
        except:
            pass

    def uk_datetime(self):
        dt = datetime.datetime.utcnow() + datetime.timedelta(hours = 0)
        d = datetime.datetime(dt.year, 4, 1)
        dston = d - datetime.timedelta(days=d.weekday() + 1)
        d = datetime.datetime(dt.year, 11, 1)
        dstoff = d - datetime.timedelta(days=d.weekday() + 1)
        if dston <=  dt < dstoff:
            return dt + datetime.timedelta(hours = 1)
        else:
            return dt

class movies:
    def __init__(self):
        self.list = []

    def get(self, url, idx=True):
        if (url.startswith(link().imdb_base) or url.startswith(link().imdb_akas)) and not ('/user/' in url or '/list/' in url):
            #self.list = self.imdb_list(url)
            try: self.list = cache2(self.imdb_list, url)
            except: return
        elif url.startswith(link().imdb_base) or url.startswith(link().imdb_akas):
            self.list = self.imdb_list2(url, idx=idx)
        elif url.startswith(link().tmdb_base):
            #self.list = self.tmdb_list(url)
            try: self.list = cache2(self.tmdb_list, url)
            except: return
        elif url.startswith(link().trakt_base):
            self.list = self.trakt_list(url)
        elif url.startswith(link().scn_base):
            #self.list = self.scn_list(url)
            try: self.list = cache2(self.scn_list, url)
            except: return

        if idx == False: return self.list
        index().movieList(self.list)

    def popular(self):
        #self.list = self.imdb_list(link().imdb_popular)
        try: self.list = cache2(self.imdb_list, link().imdb_popular)
        except: return
        index().movieList(self.list)

    def boxoffice(self):
        #self.list = self.imdb_list(link().imdb_boxoffice)
        try: self.list = cache2(self.imdb_list, link().imdb_boxoffice)
        except: return
        index().movieList(self.list)

    def views(self):
        #self.list = self.imdb_list(link().imdb_views)
        try: self.list = cache2(self.imdb_list, link().imdb_views)
        except: return
        index().movieList(self.list)

    def oscars(self):
        #self.list = self.imdb_list(link().imdb_oscars)
        try: self.list = cache2(self.imdb_list, link().imdb_oscars)
        except: return
        index().movieList(self.list)

    def added(self):
        #self.list = self.scn_list(link().scn_added)
        try: self.list = cache2(self.scn_list, link().scn_added)
        except: return
        index().movieList(self.list)

    def theaters(self):
        #self.list = self.tmdb_list(link().tmdb_theaters % link().tmdb_key)
        try: self.list = cache2(self.tmdb_list, link().tmdb_theaters % link().tmdb_key)
        except: return
        index().movieList(self.list)

    def trending(self):
        #self.list = self.trakt_list(link().trakt_trending % link().trakt_key)
        try: self.list = cache2(self.trakt_list, link().trakt_trending % link().trakt_key)
        except: return
        index().movieList(self.list[:100])

    def trakt_collection(self):
        self.list = self.trakt_list(link().trakt_collection % (link().trakt_key, link().trakt_user))
        index().movieList(self.list)

    def trakt_watchlist(self):
        self.list = self.trakt_list(link().trakt_watchlist % (link().trakt_key, link().trakt_user))
        index().movieList(self.list)

    def imdb_watchlist(self):
        self.list = self.imdb_list2(link().imdb_watchlist % link().imdb_user)
        index().movieList(self.list)

    def search(self, query=None):
        if query == None:
            self.query = common.getUserInput(language(30382).encode("utf-8"), '')
        else:
            self.query = query
        if not (self.query == None or self.query == ''):
            self.query = link().imdb_search % urllib.quote_plus(self.query)
            self.list = self.imdb_list(self.query)
            index().movieList(self.list)

    def favourites(self):
        try:
            dbcon = database.connect(addonSettings)
            dbcur = dbcon.cursor()
            dbcur.execute("SELECT * FROM favourites WHERE video_type ='Movie'")
            match = dbcur.fetchall()
            match = [(i[0], i[2], i[3], i[6]) for i in match]

            for imdb, title, year, poster in match:
                name = '%s (%s)' % (title, year)
                imdb = re.sub('[^0-9]', '', imdb)
                self.list.append({'name': name, 'title': title, 'year': year, 'imdb': imdb, 'tvdb': '0', 'season': '0', 'episode': '0', 'show': '0', 'show_alt': '0', 'date': '0', 'genre': '0', 'url': '0', 'poster': poster, 'fanart': '0', 'studio': '0', 'duration': '0', 'rating': '0', 'votes': '0', 'mpaa': '0', 'director': '0', 'plot': '0', 'plotoutline': '0', 'tagline': '0'})

            threads = []
            for i in range(0, len(self.list)): threads.append(Thread(self.tmdb_info, i))
            [i.start() for i in threads]
            [i.join() for i in threads]

            self.list = sorted(self.list, key=itemgetter('title'))
            index().movieList(self.list)
        except:
            return

    def imdb_list(self, url):
        try:
            url = url.replace(link().imdb_base, link().imdb_akas)
            result = getUrl(url, timeout='10').result
            result = result.decode('iso-8859-1').encode('utf-8')
            movies = common.parseDOM(result, "tr", attrs = { "class": ".+?" })
        except:
            return

        try:
            next = common.parseDOM(result, "span", attrs = { "class": "pagination" })[0]
            name = common.parseDOM(next, "a")[-1]
            if 'laquo' in name: raise Exception()
            next = common.parseDOM(next, "a", ret="href")[-1]
            next = '%s%s' % (link().imdb_akas, next)
            next = common.replaceHTMLCodes(next)
            next = next.encode('utf-8')
        except:
            next = ''

        for movie in movies:
            try:
                title = common.parseDOM(movie, "a")[1]
                title = common.replaceHTMLCodes(title)
                title = title.encode('utf-8')

                year = common.parseDOM(movie, "span", attrs = { "class": "year_type" })[0]
                year = re.compile('(\d{4})').findall(year)[-1]
                year = year.encode('utf-8')

                if int(year) > int((datetime.datetime.utcnow() - datetime.timedelta(hours = 5)).strftime("%Y")): raise Exception()

                name = '%s (%s)' % (title, year)
                try: name = name.encode('utf-8')
                except: pass

                url = common.parseDOM(movie, "a", ret="href")[0]
                url = '%s%s' % (link().imdb_base, url)
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                imdb = re.sub('[^0-9]', '', url.rsplit('tt', 1)[-1])
                imdb = imdb.encode('utf-8')

                poster = link().imdb_image
                try: poster = common.parseDOM(movie, "img", ret="src")[0]
                except: pass
                if not ('_SX' in poster or '_SY' in poster): poster = link().imdb_image
                poster = re.sub('_SX\d*|_SY\d*|_CR\d+?,\d+?,\d+?,\d*','_SX500', poster)
                poster = common.replaceHTMLCodes(poster)
                poster = poster.encode('utf-8')

                genre = common.parseDOM(movie, "span", attrs = { "class": "genre" })
                genre = common.parseDOM(genre, "a")
                genre = " / ".join(genre)
                if genre == '': genre = '0'
                genre = common.replaceHTMLCodes(genre)
                genre = genre.encode('utf-8')

                try: duration = common.parseDOM(movie, "span", attrs = { "class": "runtime" })[0]
                except: duration = '0'
                duration = re.sub('[^0-9]', '', duration)
                if duration == '': duration = '0'
                duration = common.replaceHTMLCodes(duration)
                duration = duration.encode('utf-8')

                try: rating = common.parseDOM(movie, "span", attrs = { "class": "rating-rating" })[0]
                except: rating = '0'
                try: rating = common.parseDOM(movie, "span", attrs = { "class": "value" })[0]
                except: rating = '0'
                if rating == '': rating = '0'
                rating = common.replaceHTMLCodes(rating)
                rating = rating.encode('utf-8')

                try: votes = common.parseDOM(movie, "div", ret="title", attrs = { "class": "rating rating-list" })[0]
                except: votes = '0'
                try: votes = votes = re.compile('[(](.+?) votes[)]').findall(votes)[0]
                except: votes = '0'
                if votes == '': votes = '0'
                votes = common.replaceHTMLCodes(votes)
                votes = votes.encode('utf-8')

                try: mpaa = common.parseDOM(movie, "span", attrs = { "class": "certificate" })[0]
                except: mpaa = '0'
                try: mpaa = common.parseDOM(mpaa, "span", ret="title")[0]
                except: mpaa = '0'
                if mpaa == '' or mpaa == 'NOT_RATED': mpaa = '0'
                mpaa = mpaa.replace('_', '-')
                mpaa = common.replaceHTMLCodes(mpaa)
                mpaa = mpaa.encode('utf-8')

                director = common.parseDOM(movie, "span", attrs = { "class": "credit" })
                try: director = director[0].split('With:', 1)[0].strip()
                except: director = '0'
                director = common.parseDOM(director, "a")
                director = " / ".join(director)
                if director == '': director = '0'
                director = common.replaceHTMLCodes(director)
                director = director.encode('utf-8')

                try: plot = common.parseDOM(movie, "span", attrs = { "class": "outline" })[0]
                except: plot = '0'
                plot = plot.rsplit('<span>', 1)[0].strip()
                if plot == '': plot = '0'
                plot = common.replaceHTMLCodes(plot)
                plot = plot.encode('utf-8')

                tagline = re.compile('[.!?][\s]{1,2}(?=[A-Z])').split(plot)[0]
                try: tagline = tagline.encode('utf-8')
                except: pass

                self.list.append({'name': name, 'title': title, 'year': year, 'imdb': imdb, 'tvdb': '0', 'season': '0', 'episode': '0', 'show': '0', 'show_alt': '0', 'date': '0', 'genre': genre, 'url': url, 'poster': poster, 'fanart': '0', 'studio': '0', 'duration': duration, 'rating': rating, 'votes': votes, 'mpaa': mpaa, 'director': director, 'plot': plot, 'plotoutline': tagline, 'tagline': tagline, 'next': next})
            except:
                pass

        threads = []
        for i in range(0, len(self.list)): threads.append(Thread(self.tmdb_info, i))
        [i.start() for i in threads]
        [i.join() for i in threads]

        return self.list

    def imdb_list2(self, url, idx=True):
        try:
            if url == link().imdb_watchlist % link().imdb_user:
                result = getUrl(url, timeout='10').result
                url = common.parseDOM(result, "div", attrs = { "class": "export" })[0]
                url = re.compile('=(ls\d*)').findall(url)[0]
                url = link().imdb_list % url

            url = url.replace(link().imdb_base, link().imdb_akas)
            result = getUrl(url, timeout='10').result

            try:
                if idx == True: raise Exception()
                pages = common.parseDOM(result, "div", attrs = { "class": "desc" })[0]
                pages = re.compile('Page \d+? of (\d*)').findall(pages)[0]
                for i in range(1, int(pages)):
                    u = url.replace('&start=1', '&start=%s' % str(i*100+1))
                    try: result += getUrl(u, timeout='10').result
                    except: pass
            except:
                pass

            result = result.replace('\n','')
            result = result.decode('iso-8859-1').encode('utf-8')
            movies = common.parseDOM(result, "div", attrs = { "class": "list_item.+?" })
        except:
            return

        try:
            next = common.parseDOM(result, "div", attrs = { "class": "pagination" })[-1]
            name = common.parseDOM(next, "a")[-1]
            if 'laquo' in name: raise Exception()
            next = common.parseDOM(next, "a", ret="href")[-1]
            next = '%s%s' % (url.split('?', 1)[0], next)
            next = common.replaceHTMLCodes(next)
            next = next.encode('utf-8')
        except:
            next = ''

        for movie in movies:
            try:
                title = common.parseDOM(movie, "a", attrs = { "onclick": ".+?" })[-1]
                title = common.replaceHTMLCodes(title)
                title = title.encode('utf-8')

                year = common.parseDOM(movie, "span", attrs = { "class": "year_type" })[0]
                year = re.compile('(\d{4})').findall(year)[-1]
                year = year.encode('utf-8')

                if int(year) > int((datetime.datetime.utcnow() - datetime.timedelta(hours = 5)).strftime("%Y")): raise Exception()

                name = '%s (%s)' % (title, year)
                try: name = name.encode('utf-8')
                except: pass

                url = common.parseDOM(movie, "a", ret="href")[0]
                url = '%s%s' % (link().imdb_base, url)
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                imdb = re.sub('[^0-9]', '', url.rsplit('tt', 1)[-1])
                imdb = imdb.encode('utf-8')

                poster = link().imdb_image
                try: poster = common.parseDOM(movie, "img", ret="src")[0]
                except: pass
                try: poster = common.parseDOM(movie, "img", ret="loadlate")[0]
                except: pass
                if not ('_SX' in poster or '_SY' in poster): poster = link().imdb_image
                poster = re.sub('_SX\d*|_SY\d*|_CR\d+?,\d+?,\d+?,\d*','_SX500', poster)
                poster = common.replaceHTMLCodes(poster)
                poster = poster.encode('utf-8')

                try: duration = common.parseDOM(movie, "div", attrs = { "class": "item_description" })[0]
                except: duration = '0'
                try: duration = common.parseDOM(duration, "span")[-1]
                except: duration = '0'
                duration = re.sub('[^0-9]', '', duration)
                if duration == '': duration = '0'
                duration = common.replaceHTMLCodes(duration)
                duration = duration.encode('utf-8')

                try: rating = common.parseDOM(movie, "span", attrs = { "class": "rating-rating" })[0]
                except: rating = '0'
                try: rating = common.parseDOM(movie, "span", attrs = { "class": "value" })[0]
                except: rating = '0'
                if rating == '' or rating == '-': rating = '0'
                rating = common.replaceHTMLCodes(rating)
                rating = rating.encode('utf-8')

                try: votes = common.parseDOM(movie, "div", ret="title", attrs = { "class": "rating rating-list" })[0]
                except: votes = '0'
                try: votes = votes = re.compile('[(](.+?) votes[)]').findall(votes)[0]
                except: votes = '0'
                if votes == '': votes = '0'
                votes = common.replaceHTMLCodes(votes)
                votes = votes.encode('utf-8')

                director = common.parseDOM(movie, "div", attrs = { "class": "secondary" })
                director = [i for i in director if i.startswith('Director:')]
                try: director = common.parseDOM(director[0], "a")
                except: director = '0'
                director = " / ".join(director)
                if director == '': director = '0'
                director = common.replaceHTMLCodes(director)
                director = director.encode('utf-8')

                try: plot = common.parseDOM(movie, "div", attrs = { "class": "item_description" })[0]
                except: plot = '0'
                plot = plot.rsplit('<span>', 1)[0].strip()
                if plot == '': plot = '0'
                plot = common.replaceHTMLCodes(plot)
                plot = plot.encode('utf-8')

                tagline = re.compile('[.!?][\s]{1,2}(?=[A-Z])').split(plot)[0]
                try: tagline = tagline.encode('utf-8')
                except: pass

                self.list.append({'name': name, 'title': title, 'year': year, 'imdb': imdb, 'tvdb': '0', 'season': '0', 'episode': '0', 'show': '0', 'show_alt': '0', 'date': '0', 'genre': '0', 'url': url, 'poster': poster, 'fanart': '0', 'studio': '0', 'duration': duration, 'rating': rating, 'votes': votes, 'mpaa': '0', 'director': director, 'plot': plot, 'plotoutline': tagline, 'tagline': tagline, 'next': next})
            except:
                pass

        if idx == True: self.trakt_info()

        return self.list

    def tmdb_list(self, url):
        try:
            result = getUrl(url, timeout='10').result
            result = json.loads(result)
            movies = result['results']
        except:
            return

        try:
            next = str(result['page'])
            if next == '5': raise Exception()
            next = '%s&page=%s' % (url.split('&page=', 1)[0], str(int(next)+1))
            next = common.replaceHTMLCodes(next)
            next = next.encode('utf-8')
        except:
            next = ''

        for movie in movies:
            try:
                title = movie['title']
                title = common.replaceHTMLCodes(title)
                title = title.encode('utf-8')

                year = movie['release_date']
                year = re.compile('(\d{4})').findall(year)[-1]
                year = year.encode('utf-8')

                if int(year) > int((datetime.datetime.utcnow() - datetime.timedelta(hours = 5)).strftime("%Y")): raise Exception()

                name = '%s (%s)' % (title, year)
                try: name = name.encode('utf-8')
                except: pass

                tmdb = movie['id']
                tmdb = re.sub('[^0-9]', '', str(tmdb))
                tmdb = tmdb.encode('utf-8')

                poster = movie['poster_path']
                if poster == '' or poster == None: raise Exception()
                else: poster = '%s%s' % (link().tmdb_image2, poster)
                poster = common.replaceHTMLCodes(poster)
                poster = poster.encode('utf-8')

                fanart = movie['backdrop_path']
                if fanart == '' or fanart == None: fanart = '0'
                if not fanart == '0': fanart = '%s%s' % (link().tmdb_image, fanart)
                fanart = common.replaceHTMLCodes(fanart)
                fanart = fanart.encode('utf-8')

                rating = str(movie['vote_average'])
                if rating == '' or rating == None: rating = '0'
                rating = common.replaceHTMLCodes(rating)
                rating = rating.encode('utf-8')

                votes = str(movie['vote_count'])
                try: votes = str(format(int(votes),',d'))
                except: pass
                if votes == '' or votes == None: votes = '0'
                votes = common.replaceHTMLCodes(votes)
                votes = votes.encode('utf-8')

                self.list.append({'name': name, 'title': title, 'year': year, 'imdb': '0', 'tvdb': '0', 'season': '0', 'episode': '0', 'show': '0', 'show_alt': '0', 'date': '0', 'genre': '0', 'url': '0', 'poster': poster, 'fanart': fanart, 'studio': '0', 'duration': '0', 'rating': rating, 'votes': votes, 'mpaa': '0', 'director': '0', 'plot': '0', 'plotoutline': '0', 'tagline': '0', 'tmdb': tmdb, 'next': next})
            except:
                pass

        threads = []
        for i in range(0, len(self.list)): threads.append(Thread(self.tmdb_info2, i))
        [i.start() for i in threads]
        [i.join() for i in threads]

        return self.list

    def trakt_list(self, url):
        try:
            post = urllib.urlencode({'username': link().trakt_user, 'password': link().trakt_password})

            result = getUrl(url, post=post, timeout='30').result
            result = json.loads(result)

            movies = []
            try: result = result['items']
            except: pass
            for i in result:
                try: movies.append(i['movie'])
                except: pass
            if movies == []: 
                movies = result
        except:
            return

        for movie in movies:
            try:
                title = movie['title']
                title = common.replaceHTMLCodes(title)
                title = title.encode('utf-8')

                year = movie['year']
                year = re.sub('[^0-9]', '', str(year))
                year = year.encode('utf-8')

                if int(year) > int((datetime.datetime.utcnow() - datetime.timedelta(hours = 5)).strftime("%Y")): raise Exception()

                name = '%s (%s)' % (title, year)
                try: name = name.encode('utf-8')
                except: pass

                imdb = movie['imdb_id']
                imdb = re.sub('[^0-9]', '', str(imdb))
                imdb = imdb.encode('utf-8')

                url = link().imdb_title % imdb
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                genre = movie['genres']
                if genre == []: genre = '0'
                genre = " / ".join(genre)
                genre = common.replaceHTMLCodes(genre)
                genre = genre.encode('utf-8')

                try: poster = movie['images']['poster']
                except: poster = movie['poster']
                poster = poster.rsplit('?', 1)[0]
                poster = poster.replace('zapp.trakt','slurm.trakt')
                if poster.endswith('poster-dark.jpg'): poster = link().imdb_image
                poster = common.replaceHTMLCodes(poster)
                poster = poster.encode('utf-8')

                try: fanart = movie['images']['fanart']
                except: fanart = movie['fanart']
                fanart = fanart.rsplit('?', 1)[0]
                if fanart == '' or fanart.endswith('fanart-dark.jpg'): fanart = '0'
                fanart = common.replaceHTMLCodes(fanart)
                fanart = fanart.encode('utf-8')

                try: duration = str(movie['runtime'])
                except: duration = '0'
                if duration == '': duration = '0'
                duration = common.replaceHTMLCodes(duration)
                duration = duration.encode('utf-8')

                try: rating = str(movie['ratings']['percentage'])
                except: rating = '0'
                rating = str(int(rating) / 10.0)
                if rating == '' or rating == '0.0': rating = '0'
                rating = common.replaceHTMLCodes(rating)
                rating = rating.encode('utf-8')

                try: votes = str(movie['ratings']['votes'])
                except: votes = '0'
                try: votes = str(format(int(votes),',d'))
                except: pass
                if votes == '': votes = '0'
                votes = common.replaceHTMLCodes(votes)
                votes = votes.encode('utf-8')

                mpaa = movie['certification']
                if mpaa == '': mpaa = '0'
                mpaa = common.replaceHTMLCodes(mpaa)
                mpaa = mpaa.encode('utf-8')

                plot = movie['overview']
                if plot == '': plot = '0'
                plot = common.replaceHTMLCodes(plot)
                plot = plot.encode('utf-8')

                plotoutline = re.compile('[.!?][\s]{1,2}(?=[A-Z])').split(plot)[0]
                try: plotoutline = plotoutline.encode('utf-8')
                except: pass

                tagline = movie['tagline']
                if tagline == '' and not plot == '0': tagline = plotoutline
                elif tagline == '': tagline = '0'
                tagline = common.replaceHTMLCodes(tagline)
                tagline = tagline.encode('utf-8')

                self.list.append({'name': name, 'title': title, 'year': year, 'imdb': imdb, 'tvdb': '0', 'season': '0', 'episode': '0', 'show': '0', 'show_alt': '0', 'date': '0', 'genre': genre, 'url': url, 'poster': poster, 'fanart': fanart, 'studio': '0', 'duration': duration, 'rating': rating, 'votes': votes, 'mpaa': mpaa, 'director': '0', 'plot': plot, 'plotoutline': plotoutline, 'tagline': tagline})
            except:
                pass

        return self.list

    def scn_list(self, url):
        try:
            result = getUrl(url, timeout='10').result
            result = result.replace('\n','')
            result = result.decode('iso-8859-1').encode('utf-8')

            url = common.parseDOM(result, "span", ret="data-title", attrs = { "class": "imdbRatingPlugin" })
            url = [i.encode('utf-8') for i in url]
            url = uniqueList(url).list
            url = link().trakt_info % (link().trakt_key, ",".join(url))

            movies = getUrl(url, timeout='30').result
            movies = json.loads(movies)
        except:
            return

        try:
            next = common.parseDOM(result, "a", attrs = { "class": "page" })
            i = [x[0] for x in list(enumerate(next)) if x[1] == '&gt;'][0]
            next = common.parseDOM(result, "a", ret="href", attrs = { "class": "page" })[int(i)]
            next = '%s%s' % (link().scn_base, next)
            next = common.replaceHTMLCodes(next)
            next = next.encode('utf-8')
        except:
            next = ''

        for movie in movies:
            try:
                title = movie['title']
                title = common.replaceHTMLCodes(title)
                title = title.encode('utf-8')

                year = movie['year']
                year = re.sub('[^0-9]', '', str(year))
                year = year.encode('utf-8')

                if int(year) > int((datetime.datetime.utcnow() - datetime.timedelta(hours = 5)).strftime("%Y")): raise Exception()

                name = '%s (%s)' % (title, year)
                try: name = name.encode('utf-8')
                except: pass

                imdb = movie['imdb_id']
                imdb = re.sub('[^0-9]', '', str(imdb))
                imdb = imdb.encode('utf-8')

                url = link().imdb_title % imdb
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                try: poster = movie['images']['poster']
                except: poster = movie['poster']
                poster = poster.rsplit('?', 1)[0]
                poster = poster.replace('zapp.trakt','slurm.trakt')
                if poster.endswith('poster-dark.jpg'): poster = link().imdb_image
                poster = common.replaceHTMLCodes(poster)
                poster = poster.encode('utf-8')

                try: fanart = movie['images']['fanart']
                except: fanart = movie['fanart']
                fanart = fanart.rsplit('?', 1)[0]
                if fanart == '' or fanart.endswith('fanart-dark.jpg'): fanart = '0'
                fanart = common.replaceHTMLCodes(fanart)
                fanart = fanart.encode('utf-8')

                genre = movie['genres']
                if genre == []: genre = '0'
                genre = " / ".join(genre)
                genre = common.replaceHTMLCodes(genre)
                genre = genre.encode('utf-8')

                try: duration = str(movie['runtime'])
                except: duration = '0'
                if duration == '': duration = '0'
                duration = common.replaceHTMLCodes(duration)
                duration = duration.encode('utf-8')

                mpaa = movie['certification']
                if mpaa == '': mpaa = '0'
                mpaa = common.replaceHTMLCodes(mpaa)
                mpaa = mpaa.encode('utf-8')

                plot = movie['overview']
                if plot == '': plot = '0'
                plot = common.replaceHTMLCodes(plot)
                plot = plot.encode('utf-8')

                plotoutline = re.compile('[.!?][\s]{1,2}(?=[A-Z])').split(plot)[0]
                try: plotoutline = plotoutline.encode('utf-8')
                except: pass

                tagline = movie['tagline']
                if tagline == '' and not plot == '0': tagline = plotoutline
                elif tagline == '': tagline = '0'
                tagline = common.replaceHTMLCodes(tagline)
                tagline = tagline.encode('utf-8')

                self.list.append({'name': name, 'title': title, 'year': year, 'imdb': imdb, 'tvdb': '0', 'season': '0', 'episode': '0', 'show': '0', 'show_alt': '0', 'date': '0', 'genre': genre, 'url': url, 'poster': poster, 'fanart': fanart, 'studio': '0', 'duration': duration, 'rating': '0', 'votes': '0', 'mpaa': mpaa, 'director': '0', 'plot': plot, 'plotoutline': plotoutline, 'tagline': tagline, 'next': next})
            except:
                pass

        return self.list

    def tmdb_info(self, i):
        try:
            url = link().tmdb_info % (self.list[i]['imdb'], link().tmdb_key)
            result = getUrl(url, timeout='10').result
            result = json.loads(result)

            poster = result['poster_path']
            if poster == '' or poster == None: poster = '0'
            if not poster == '0': poster = '%s%s' % (link().tmdb_image2, poster)
            poster = common.replaceHTMLCodes(poster)
            poster = poster.encode('utf-8')
            if not poster == '0': self.list[i].update({'poster': poster})

            fanart = result['backdrop_path']
            if fanart == '' or fanart == None: fanart = '0'
            if not fanart == '0': fanart = '%s%s' % (link().tmdb_image, fanart)
            fanart = common.replaceHTMLCodes(fanart)
            fanart = fanart.encode('utf-8')
            if not fanart == '0': self.list[i].update({'fanart': fanart})

            genre = result['genres']
            try: genre = [x['name'] for x in genre]
            except: genre = '0'
            if genre == '' or genre == None or genre == []: genre = '0'
            genre = " / ".join(genre)
            genre = common.replaceHTMLCodes(genre)
            genre = genre.encode('utf-8')
            if not genre == '0': self.list[i].update({'genre': genre})

            studio = result['production_companies']
            try: studio = [x['name'] for x in studio][0]
            except: studio = '0'
            if studio == '' or studio == None: studio = '0'
            studio = common.replaceHTMLCodes(studio)
            studio = studio.encode('utf-8')
            if not studio == '0': self.list[i].update({'studio': studio})

            try: duration = str(result['runtime'])
            except: duration = '0'
            if duration == '' or duration == None or not self.list[i]['duration'] == '0': duration = '0'
            duration = common.replaceHTMLCodes(duration)
            duration = duration.encode('utf-8')
            if not duration == '0': self.list[i].update({'duration': duration})

            rating = str(result['vote_average'])
            if rating == '' or rating == None or not self.list[i]['rating'] == '0': rating = '0'
            rating = common.replaceHTMLCodes(rating)
            rating = rating.encode('utf-8')
            if not rating == '0': self.list[i].update({'rating': rating})

            votes = str(result['vote_count'])
            try: votes = str(format(int(votes),',d'))
            except: pass
            if votes == '' or votes == None or not self.list[i]['votes'] == '0': votes = '0'
            votes = common.replaceHTMLCodes(votes)
            votes = votes.encode('utf-8')
            if not votes == '0': self.list[i].update({'votes': votes})

            plot = result['overview']
            if plot == '' or plot == None: plot = '0'
            plot = common.replaceHTMLCodes(plot)
            plot = plot.encode('utf-8')
            if not plot == '0': self.list[i].update({'plot': plot})

            tagline = result['tagline']
            if (tagline == '' or tagline == None) and not plot == '0': tagline = plot.split('.', 1)[0]
            elif tagline == '' or tagline == None: tagline = '0'
            tagline = common.replaceHTMLCodes(tagline)
            tagline = tagline.encode('utf-8')
            if not tagline == '0': self.list[i].update({'tagline': tagline})
        except:
            pass

    def tmdb_info2(self, i):
        try:
            url = link().tmdb_info2 % (self.list[i]['tmdb'], link().tmdb_key)
            result = getUrl(url, timeout='10').result
            result = json.loads(result)

            imdb = result['imdb_id']
            imdb = re.sub('[^0-9]', '', str(imdb))
            imdb = imdb.encode('utf-8')
            self.list[i].update({'imdb': imdb})

            url = link().imdb_title % imdb
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            self.list[i].update({'url': url})

            genre = result['genres']
            try: genre = [x['name'] for x in genre]
            except: genre = '0'
            if genre == '' or genre == None or genre == []: genre = '0'
            genre = " / ".join(genre)
            genre = common.replaceHTMLCodes(genre)
            genre = genre.encode('utf-8')
            if not genre == '0': self.list[i].update({'genre': genre})

            studio = result['production_companies']
            try: studio = [x['name'] for x in studio][0]
            except: studio = '0'
            if studio == '' or studio == None: studio = '0'
            studio = common.replaceHTMLCodes(studio)
            studio = studio.encode('utf-8')
            if not studio == '0': self.list[i].update({'studio': studio})

            try: duration = str(result['runtime'])
            except: duration = '0'
            if duration == '' or duration == None: fanart = '0'
            duration = common.replaceHTMLCodes(duration)
            duration = duration.encode('utf-8')
            if not duration == '0': self.list[i].update({'duration': duration})

            plot = result['overview']
            if plot == '' or plot == None: plot = '0'
            plot = common.replaceHTMLCodes(plot)
            plot = plot.encode('utf-8')
            if not plot == '0': self.list[i].update({'plot': plot})

            tagline = result['tagline']
            if (tagline == '' or tagline == None) and not plot == '0': tagline = plot.split('.', 1)[0]
            elif tagline == '' or tagline == None: tagline = '0'
            tagline = common.replaceHTMLCodes(tagline)
            tagline = tagline.encode('utf-8')
            if not tagline == '0': self.list[i].update({'tagline': tagline})
        except:
            pass

    def trakt_info(self):
        try:
            url = ['tt' + i['imdb'] for i in self.list]
            url = uniqueList(url).list
            url = link().trakt_info % (link().trakt_key, ",".join(url))
            movies = getUrl(url, timeout='30').result
            movies = json.loads(movies)
        except:
            return

        for i in range(0, len(self.list)):
            try:
                movie = [x for x in movies if x['imdb_id'] == 'tt' + self.list[i]['imdb']][0]

                try: poster = movie['images']['poster']
                except: poster = movie['poster']
                poster = poster.rsplit('?', 1)[0]
                poster = poster.replace('zapp.trakt','slurm.trakt')
                poster = common.replaceHTMLCodes(poster)
                poster = poster.encode('utf-8')
                if not poster.endswith('poster-dark.jpg'): self.list[i].update({'poster': poster})

                try: fanart = movie['images']['fanart']
                except: fanart = movie['fanart']
                fanart = fanart.rsplit('?', 1)[0]
                if fanart == '' or fanart.endswith('fanart-dark.jpg'): fanart = '0'
                fanart = common.replaceHTMLCodes(fanart)
                fanart = fanart.encode('utf-8')
                if not fanart == '0': self.list[i].update({'fanart': fanart})

                try: duration = str(movie['runtime'])
                except: duration = '0'
                if duration == '' or not self.list[i]['duration'] == '0': duration = '0'
                duration = common.replaceHTMLCodes(duration)
                duration = duration.encode('utf-8')
                if not duration == '0': self.list[i].update({'duration': duration})

                genre = movie['genres']
                if genre == []: genre = '0'
                genre = " / ".join(genre)
                genre = common.replaceHTMLCodes(genre)
                genre = genre.encode('utf-8')
                if not genre == '0': self.list[i].update({'genre': genre})

                mpaa = movie['certification']
                if mpaa == '': mpaa = '0'
                mpaa = common.replaceHTMLCodes(mpaa)
                mpaa = mpaa.encode('utf-8')
                if not mpaa == '0': self.list[i].update({'mpaa': mpaa})

                plot = movie['overview']
                if plot == '': plot = '0'
                plot = common.replaceHTMLCodes(plot)
                plot = plot.encode('utf-8')
                if not plot == '0': self.list[i].update({'plot': plot})

                tagline = movie['tagline']
                if tagline == '' and not plot == '0': tagline = plot.split('.', 1)[0]
                elif tagline == '': tagline = '0'
                tagline = common.replaceHTMLCodes(tagline)
                tagline = tagline.encode('utf-8')
                if not tagline == '0': self.list[i].update({'tagline': tagline})
            except:
                pass

class shows:
    def __init__(self):
        self.list = []

    def get(self, url, idx=True):
        if (url.startswith(link().imdb_base) or url.startswith(link().imdb_akas)) and not ('/user/' in url or '/list/' in url):
            #self.list = self.imdb_list(url)
            try: self.list = cache2(self.imdb_list, url)
            except: return
        elif url.startswith(link().imdb_base) or url.startswith(link().imdb_akas):
            self.list = self.imdb_list2(url, idx=idx)
        elif url.startswith(link().trakt_base):
            self.list = self.trakt_list(url)

        if idx == False: return self.list
        index().showList(self.list)

    def popular(self):
        #self.list = self.imdb_list(link().imdb_tv_popular)
        try: self.list = cache2(self.imdb_list, link().imdb_tv_popular)
        except: return
        index().showList(self.list)

    def rating(self):
        #self.list = self.imdb_list(link().imdb_tv_rating)
        try: self.list = cache2(self.imdb_list, link().imdb_tv_rating)
        except: return
        index().showList(self.list)

    def views(self):
        #self.list = self.imdb_list(link().imdb_tv_views)
        try: self.list = cache2(self.imdb_list, link().imdb_tv_views)
        except: return
        index().showList(self.list)

    def active(self):
        #self.list = self.imdb_list(link().imdb_tv_active)
        try: self.list = cache2(self.imdb_list, link().imdb_tv_active)
        except: return
        index().showList(self.list)

    def trending(self):
        #self.list = self.trakt_list(link().trakt_tv_trending % link().trakt_key)
        try: self.list = cache2(self.trakt_list, link().trakt_tv_trending % link().trakt_key)
        except: return
        index().showList(self.list[:100])

    def trakt_collection(self):
        self.list = self.trakt_list(link().trakt_tv_collection % (link().trakt_key, link().trakt_user))
        index().showList(self.list)

    def trakt_watchlist(self):
        self.list = self.trakt_list(link().trakt_tv_watchlist % (link().trakt_key, link().trakt_user))
        index().showList(self.list)

    def imdb_watchlist(self):
        self.list = self.imdb_list2(link().imdb_watchlist % link().imdb_user)
        index().showList(self.list)

    def search(self, query=None):
        if query == None:
            self.query = common.getUserInput(language(30382).encode("utf-8"), '')
        else:
            self.query = query
        if not (self.query == None or self.query == ''):
            self.query = link().imdb_tv_search % urllib.quote_plus(self.query)
            self.list = self.imdb_list(self.query)
            index().showList(self.list)


    def favourites(self):
        try:
            dbcon = database.connect(addonSettings)
            dbcur = dbcon.cursor()
            dbcur.execute("SELECT * FROM favourites WHERE video_type ='TV Show'")
            match = dbcur.fetchall()
            match = [(i[0], i[2], i[3], i[6]) for i in match]

            for imdb, title, year, poster in match:
                imdb = re.sub('[^0-9]', '', imdb)
                self.list.append({'title': title, 'year': year, 'imdb': imdb, 'tvdb': '0', 'genre': '0', 'url': '0', 'poster': poster, 'banner': poster, 'fanart': '0', 'studio': '0', 'premiered': '0', 'duration': '0', 'rating': '0', 'mpaa': '0', 'plot': '0'})

            threads = []
            for i in range(0, len(self.list)): threads.append(Thread(self.tvdb_info, i))
            [i.start() for i in threads]
            [i.join() for i in threads]

            self.list = sorted(self.list, key=itemgetter('title'))
            index().showList(self.list)
        except:
            return

    def imdb_list(self, url):
        try:
            url = url.replace(link().imdb_base, link().imdb_akas)
            result = getUrl(url, timeout='10').result
            result = result.decode('iso-8859-1').encode('utf-8')
            shows = common.parseDOM(result, "tr", attrs = { "class": ".+?" })
        except:
            return

        try:
            next = common.parseDOM(result, "span", attrs = { "class": "pagination" })[0]
            name = common.parseDOM(next, "a")[-1]
            if 'laquo' in name: raise Exception()
            next = common.parseDOM(next, "a", ret="href")[-1]
            next = '%s%s' % (link().imdb_akas, next)
            next = common.replaceHTMLCodes(next)
            next = next.encode('utf-8')
        except:
            next = ''

        for show in shows:
            try:
                title = common.parseDOM(show, "a")[1]
                title = common.replaceHTMLCodes(title)
                title = title.encode('utf-8')

                year = common.parseDOM(show, "span", attrs = { "class": "year_type" })[0]
                year = re.compile('(\d{4})').findall(year)[-1]
                year = year.encode('utf-8')

                if int(year) > int((datetime.datetime.utcnow() - datetime.timedelta(hours = 5)).strftime("%Y")): raise Exception()

                url = common.parseDOM(show, "a", ret="href")[0]
                url = '%s%s' % (link().imdb_base, url)
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                imdb = re.sub('[^0-9]', '', url.rsplit('tt', 1)[-1])
                imdb = imdb.encode('utf-8')

                poster = link().imdb_tv_image
                try: poster = common.parseDOM(show, "img", ret="src")[0]
                except: pass
                if not ('_SX' in poster or '_SY' in poster): poster = link().imdb_tv_image
                poster = re.sub('_SX\d*|_SY\d*|_CR\d+?,\d+?,\d+?,\d*','_SX500', poster)
                poster = common.replaceHTMLCodes(poster)
                poster = poster.encode('utf-8')

                genre = common.parseDOM(show, "span", attrs = { "class": "genre" })
                genre = common.parseDOM(genre, "a")
                genre = " / ".join(genre)
                if genre == '': genre = '0'
                genre = common.replaceHTMLCodes(genre)
                genre = genre.encode('utf-8')

                try: rating = common.parseDOM(show, "span", attrs = { "class": "rating-rating" })[0]
                except: rating = '0'
                try: rating = common.parseDOM(show, "span", attrs = { "class": "value" })[0]
                except: rating = '0'
                if rating == '': rating = '0'
                rating = common.replaceHTMLCodes(rating)
                rating = rating.encode('utf-8')

                try: mpaa = common.parseDOM(show, "span", attrs = { "class": "certificate" })[0]
                except: mpaa = '0'
                try: mpaa = common.parseDOM(mpaa, "span", ret="title")[0]
                except: mpaa = '0'
                if mpaa == '' or mpaa == 'NOT_RATED': mpaa = '0'
                mpaa = mpaa.replace('_', '-')
                mpaa = common.replaceHTMLCodes(mpaa)
                mpaa = mpaa.encode('utf-8')

                try: plot = common.parseDOM(show, "span", attrs = { "class": "outline" })[0]
                except: plot = '0'
                plot = plot.rsplit('<span>', 1)[0].strip()
                if plot == '': plot = '0'
                plot = common.replaceHTMLCodes(plot)
                plot = plot.encode('utf-8')

                self.list.append({'title': title, 'year': year, 'imdb': imdb, 'tvdb': '0', 'genre': genre, 'url': url, 'poster': poster, 'banner': poster, 'fanart': '0', 'studio': '0', 'premiered': '0', 'duration': '0', 'rating': rating, 'mpaa': mpaa, 'plot': plot, 'next': next})
            except:
                pass

        threads = []
        for i in range(0, len(self.list)): threads.append(Thread(self.tvdb_info, i))
        [i.start() for i in threads]
        [i.join() for i in threads]

        return self.list

    def imdb_list2(self, url, idx=True):
        try:
            if url == link().imdb_watchlist % link().imdb_user:
                result = getUrl(url, timeout='10').result
                url = common.parseDOM(result, "div", attrs = { "class": "export" })[0]
                url = re.compile('=(ls\d*)').findall(url)[0]
                url = link().imdb_tv_list % url

            url = url.replace(link().imdb_base, link().imdb_akas)
            result = getUrl(url, timeout='10').result

            try:
                if idx == True: raise Exception()
                pages = common.parseDOM(result, "div", attrs = { "class": "desc" })[0]
                pages = re.compile('Page \d+? of (\d*)').findall(pages)[0]
                for i in range(1, int(pages)):
                    u = url.replace('&start=1', '&start=%s' % str(i*100+1))
                    try: result += getUrl(u, timeout='10').result
                    except: pass
            except:
                pass

            result = result.replace('\n','')
            result = result.decode('iso-8859-1').encode('utf-8')
            shows = common.parseDOM(result, "div", attrs = { "class": "list_item.+?" })
        except:
            return

        try:
            next = common.parseDOM(result, "div", attrs = { "class": "pagination" })[-1]
            name = common.parseDOM(next, "a")[-1]
            if 'laquo' in name: raise Exception()
            next = common.parseDOM(next, "a", ret="href")[-1]
            next = '%s%s' % (url.split('?', 1)[0], next)
            next = common.replaceHTMLCodes(next)
            next = next.encode('utf-8')
        except:
            next = ''

        for show in shows:
            try:
                title = common.parseDOM(show, "a", attrs = { "onclick": ".+?" })[-1]
                title = common.replaceHTMLCodes(title)
                title = title.encode('utf-8')

                year = common.parseDOM(show, "span", attrs = { "class": "year_type" })[0]
                year = re.compile('(\d{4})').findall(year)[-1]
                year = year.encode('utf-8')

                if int(year) > int((datetime.datetime.utcnow() - datetime.timedelta(hours = 5)).strftime("%Y")): raise Exception()

                url = common.parseDOM(show, "a", ret="href")[0]
                url = '%s%s' % (link().imdb_base, url)
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                imdb = re.sub('[^0-9]', '', url.rsplit('tt', 1)[-1])
                imdb = imdb.encode('utf-8')

                poster = link().imdb_tv_image
                try: poster = common.parseDOM(show, "img", ret="src")[0]
                except: pass
                try: poster = common.parseDOM(show, "img", ret="loadlate")[0]
                except: pass
                if not ('_SX' in poster or '_SY' in poster): poster = link().imdb_tv_image
                poster = re.sub('_SX\d*|_SY\d*|_CR\d+?,\d+?,\d+?,\d*','_SX500', poster)
                poster = common.replaceHTMLCodes(poster)
                poster = poster.encode('utf-8')

                try: rating = common.parseDOM(show, "span", attrs = { "class": "rating-rating" })[0]
                except: rating = '0'
                try: rating = common.parseDOM(show, "span", attrs = { "class": "value" })[0]
                except: rating = '0'
                if rating == '' or rating == '-': rating = '0'
                rating = common.replaceHTMLCodes(rating)
                rating = rating.encode('utf-8')

                try: plot = common.parseDOM(show, "div", attrs = { "class": "item_description" })[0]
                except: plot = '0'
                plot = plot.rsplit('<span>', 1)[0].strip()
                if plot == '': plot = '0'
                plot = common.replaceHTMLCodes(plot)
                plot = plot.encode('utf-8')

                self.list.append({'title': title, 'year': year, 'imdb': imdb, 'tvdb': '0', 'genre': '0', 'url': url, 'poster': poster, 'banner': poster, 'fanart': '0', 'studio': '0', 'premiered': '0', 'duration': '0', 'rating': rating, 'mpaa': '0', 'plot': plot, 'next': next})
            except:
                pass

        if idx == True: self.trakt_info()

        return self.list

    def trakt_list(self, url):
        try:
            post = urllib.urlencode({'username': link().trakt_user, 'password': link().trakt_password})

            result = getUrl(url, post=post, timeout='30').result
            result = json.loads(result)

            shows = []
            try: result = result['items']
            except: pass
            for i in result:
                try: shows.append(i['show'])
                except: pass
            if shows == []: 
                shows = result
        except:
            return

        for show in shows:
            try:
                title = show['title']
                title = re.sub('\s(|[(])(UK|US|AU|\d{4})(|[)])$', '', title)
                title = common.replaceHTMLCodes(title)
                title = title.encode('utf-8')

                year = show['year']
                year = re.sub('[^0-9]', '', str(year))
                year = year.encode('utf-8')

                if int(year) > int((datetime.datetime.utcnow() - datetime.timedelta(hours = 5)).strftime("%Y")): raise Exception()

                imdb = show['imdb_id']
                imdb = re.sub('[^0-9]', '', str(imdb))
                imdb = imdb.encode('utf-8')

                tvdb = str(show['tvdb_id'])
                if tvdb == '': tvdb = '0'
                tvdb = common.replaceHTMLCodes(tvdb)
                tvdb = tvdb.encode('utf-8')

                url = link().imdb_title % imdb
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                try: poster = show['images']['poster']
                except: poster = show['poster']
                poster = poster.rsplit('?', 1)[0]
                poster = poster.replace('zapp.trakt','slurm.trakt')
                if poster.endswith('poster-dark.jpg'): poster = link().imdb_tv_image
                poster = common.replaceHTMLCodes(poster)
                poster = poster.encode('utf-8')

                try: banner = show['images']['banner']
                except: banner = show['banner']
                banner = banner.rsplit('?', 1)[0]
                banner = banner.replace('zapp.trakt','slurm.trakt')
                if banner == '' or banner.endswith('banner-dark.jpg'): banner = poster
                banner = common.replaceHTMLCodes(banner)
                banner = banner.encode('utf-8')

                try: fanart = show['images']['fanart']
                except: fanart = show['fanart']
                fanart = fanart.rsplit('?', 1)[0]
                if fanart == '' or fanart.endswith('fanart-dark.jpg'): fanart = '0'
                fanart = common.replaceHTMLCodes(fanart)
                fanart = fanart.encode('utf-8')

                genre = show['genres']
                if genre == []: genre = '0'
                genre = " / ".join(genre)
                genre = common.replaceHTMLCodes(genre)
                genre = genre.encode('utf-8')

                studio = show['network']
                if studio == '': studio = '0'
                studio = common.replaceHTMLCodes(studio)
                studio = studio.encode('utf-8')

                premiered = show['first_aired']
                try: premiered = (datetime.datetime.fromtimestamp(0) + datetime.timedelta(seconds = premiered)).strftime("%Y-%m-%d")
                except: premiered = '0'
                premiered = common.replaceHTMLCodes(premiered)
                premiered = premiered.encode('utf-8')

                try: duration = str(show['runtime'])
                except: duration = '0'
                if duration == '': duration = '0'
                duration = common.replaceHTMLCodes(duration)
                duration = duration.encode('utf-8')

                try: rating = str(show['ratings']['percentage'])
                except: rating = '0'
                rating = str(int(rating) / 10.0)
                if rating == '' or rating == '0.0': rating = '0'
                rating = common.replaceHTMLCodes(rating)
                rating = rating.encode('utf-8')

                mpaa = show['certification']
                if mpaa == '': mpaa = '0'
                mpaa = common.replaceHTMLCodes(mpaa)
                mpaa = mpaa.encode('utf-8')

                plot = show['overview']
                if plot == '': plot = '0'
                plot = common.replaceHTMLCodes(plot)
                plot = plot.encode('utf-8')

                self.list.append({'title': title, 'year': year, 'imdb': imdb, 'tvdb': tvdb, 'genre': genre, 'url': url, 'poster': poster, 'banner': banner, 'fanart': fanart, 'studio': studio, 'premiered': premiered, 'duration': duration, 'rating': rating, 'mpaa': mpaa, 'plot': plot})
            except:
                pass

        return self.list

    def tvdb_info(self, i):
        try:
            url = link().tvdb_search % self.list[i]['imdb']
            result = getUrl(url, timeout='10').result

            url = common.parseDOM(result, "seriesid")[0]
            url = link().tvdb_info2 % (link().tvdb_key, url)
            result = getUrl(url, timeout='10').result

            tvdb = common.parseDOM(result, "id")[0]
            if tvdb == '': tvdb = '0'
            tvdb = common.replaceHTMLCodes(tvdb)
            tvdb = tvdb.encode('utf-8')
            if not tvdb == '0': self.list[i].update({'tvdb': tvdb})

            poster = common.parseDOM(result, "poster")[0]
            if not poster == '': poster = link().tvdb_image + poster
            else: poster = '0'
            poster = common.replaceHTMLCodes(poster)
            poster = poster.encode('utf-8')
            if not poster == '0': self.list[i].update({'poster': poster})

            banner = common.parseDOM(result, "banner")[0]
            if not banner == '': banner = link().tvdb_image + banner
            else: banner = poster
            banner = common.replaceHTMLCodes(banner)
            banner = banner.encode('utf-8')
            if not banner == '0': self.list[i].update({'banner': banner})

            fanart = common.parseDOM(result, "fanart")[0]
            if not fanart == '': fanart = link().tvdb_image + fanart
            else: fanart = '0'
            fanart = common.replaceHTMLCodes(fanart)
            fanart = fanart.encode('utf-8')
            if not fanart == '0': self.list[i].update({'fanart': fanart})

            genre = common.parseDOM(result, "Genre")[0]
            genre = [x for x in genre.split('|') if not x == '']
            genre = " / ".join(genre)
            if genre == '': genre = '0'
            genre = common.replaceHTMLCodes(genre)
            genre = genre.encode('utf-8')
            if not genre == '0': self.list[i].update({'genre': genre})

            studio = common.parseDOM(result, "Network")[0]
            if studio == '': studio = '0'
            studio = common.replaceHTMLCodes(studio)
            studio = studio.encode('utf-8')
            if not studio == '0': self.list[i].update({'studio': studio})

            premiered = common.parseDOM(result, "FirstAired")[0]
            if premiered == '': premiered = '0'
            premiered = common.replaceHTMLCodes(premiered)
            premiered = premiered.encode('utf-8')
            if not premiered == '0': self.list[i].update({'premiered': premiered})

            duration = common.parseDOM(result, "Runtime")[0]
            if duration == '': duration = '0'
            duration = common.replaceHTMLCodes(duration)
            duration = duration.encode('utf-8')
            if not duration == '0': self.list[i].update({'duration': duration})

            rating = common.parseDOM(result, "Rating")[0]
            if rating == '' or not self.list[i]['rating'] == '0': rating = '0'
            rating = common.replaceHTMLCodes(rating)
            rating = rating.encode('utf-8')
            if not rating == '0': self.list[i].update({'rating': rating})

            mpaa = common.parseDOM(result, "ContentRating")[0]
            if mpaa == '': mpaa = '0'
            mpaa = common.replaceHTMLCodes(mpaa)
            mpaa = mpaa.encode('utf-8')
            if not mpaa == '0': self.list[i].update({'mpaa': mpaa})

            plot = common.parseDOM(result, "Overview")[0]
            if plot == '': plot = '0'
            plot = common.replaceHTMLCodes(plot)
            plot = plot.encode('utf-8')
            if not plot == '0': self.list[i].update({'plot': plot})
        except:
            pass

    def trakt_info(self):
        try:
            url = ['tt' + i['imdb'] for i in self.list]
            url = uniqueList(url).list
            url = link().trakt_tv_info % (link().trakt_key, ",".join(url))
            shows = getUrl(url, timeout='30').result
            shows = json.loads(shows)
        except:
            return

        for i in range(0, len(self.list)):
            try:
                show = [x for x in shows if x['imdb_id'] == 'tt' + self.list[i]['imdb']][0]

                tvdb = str(show['tvdb_id'])
                if tvdb == '': tvdb = '0'
                tvdb = common.replaceHTMLCodes(tvdb)
                tvdb = tvdb.encode('utf-8')
                if not tvdb == '0': self.list[i].update({'tvdb': tvdb})

                try: poster = show['images']['poster']
                except: poster = show['poster']
                poster = poster.rsplit('?', 1)[0]
                poster = poster.replace('zapp.trakt','slurm.trakt')
                if poster == '' or poster.endswith('poster-dark.jpg'): poster = '0'
                poster = common.replaceHTMLCodes(poster)
                poster = poster.encode('utf-8')
                if not poster == '0': self.list[i].update({'poster': poster})

                try: banner = show['images']['banner']
                except: banner = show['banner']
                banner = banner.rsplit('?', 1)[0]
                banner = banner.replace('zapp.trakt','slurm.trakt')
                if banner == '' or banner.endswith('banner-dark.jpg'): banner = poster
                banner = common.replaceHTMLCodes(banner)
                banner = banner.encode('utf-8')
                if not banner == '0': self.list[i].update({'banner': banner})

                try: fanart = show['images']['fanart']
                except: fanart = show['fanart']
                fanart = fanart.rsplit('?', 1)[0]
                if fanart == '' or fanart.endswith('fanart-dark.jpg'): fanart = '0'
                fanart = common.replaceHTMLCodes(fanart)
                fanart = fanart.encode('utf-8')
                if not fanart == '0': self.list[i].update({'fanart': fanart})

                genre = show['genres']
                if genre == []: genre = '0'
                genre = " / ".join(genre)
                genre = common.replaceHTMLCodes(genre)
                genre = genre.encode('utf-8')
                if not genre == '0': self.list[i].update({'genre': genre})

                studio = show['network']
                if studio == '': studio = '0'
                studio = common.replaceHTMLCodes(studio)
                studio = studio.encode('utf-8')
                if not studio == '0': self.list[i].update({'studio': studio})

                premiered = show['first_aired']
                if premiered == '': premiered = '0'
                try: premiered = (datetime.datetime.fromtimestamp(0) + datetime.timedelta(seconds = premiered)).strftime("%Y-%m-%d")
                except: premiered = '0'
                premiered = common.replaceHTMLCodes(premiered)
                premiered = premiered.encode('utf-8')
                if not premiered == '0': self.list[i].update({'premiered': premiered})

                try: duration = str(show['runtime'])
                except: duration = '0'
                if duration == '': duration = '0'
                duration = common.replaceHTMLCodes(duration)
                duration = duration.encode('utf-8')
                if not duration == '0': self.list[i].update({'duration': duration})

                mpaa = show['certification']
                if mpaa == '': mpaa = '0'
                mpaa = common.replaceHTMLCodes(mpaa)
                mpaa = mpaa.encode('utf-8')
                if not mpaa == '0': self.list[i].update({'mpaa': mpaa})

                plot = show['overview']
                if plot == '': plot = '0'
                plot = common.replaceHTMLCodes(plot)
                plot = plot.encode('utf-8')
                if not plot == '0': self.list[i].update({'plot': plot})
            except:
                pass

class seasons:
    def __init__(self):
        self.list = []

    def get(self, show, year, imdb, tvdb, idx=True):
        if idx == True:
            #self.list = self.tvdb_list(show, year, imdb, tvdb, '-1')
            try: self.list = cache2(self.tvdb_list, show, year, imdb, tvdb, '-1')
            except: return
            self.list = self.list[0]['seasons']
            index().seasonList(self.list)
        else:
            self.list = self.tvdb_list(show, year, imdb, tvdb, '-1')
            return self.list

    def tvdb_list(self, show, year, imdb, tvdb, limit=''):
        try:
            if not tvdb == '0': raise Exception()

            url = link().tvdb_search % imdb
            result = getUrl(url, timeout='10').result
            result = common.parseDOM(result, "Series")

            if len(result) == 0:
                url = link().tvdb_search2 % urllib.quote_plus(show)
                clean = '\n|\s(|[(])(UK|US|AU|\d{4})(|[)])$|\s(vs|v[.])\s|(:|;|-|"|,|\'|\.|\?)|\s'
                result = getUrl(url, timeout='10').result
                result = common.parseDOM(result, "Series")
                result = [i for i in result if re.sub(clean, '', show).lower() == re.sub(clean, '', common.replaceHTMLCodes(common.parseDOM(i, "SeriesName")[0])).lower() and any(x in common.parseDOM(i, "FirstAired")[0] for x in [str(year), str(int(year)+1), str(int(year)-1)])][0]

            tvdb = common.parseDOM(result, "seriesid")[0]
            tvdb = tvdb.encode('utf-8')
        except:
            pass

        try:
            if tvdb == '0': raise Exception()

            import zipfile, StringIO
            tvdbUrl = link().tvdb_info % (link().tvdb_key, tvdb)
            data = urllib2.urlopen(tvdbUrl, timeout=10).read()
            zip = zipfile.ZipFile(StringIO.StringIO(data))
            art = zip.read('banners.xml')
            result = zip.read('en.xml')
            zip.close()

            art = common.parseDOM(art, "Banner")
            art = [i for i in art if common.parseDOM(i, "Language")[0] == 'en']
            art = [i for i in art if common.parseDOM(i, "BannerType")[0] == 'season']
            art = [i for i in art if not 'seasonswide' in common.parseDOM(i, "BannerPath")[0]]

            show_alt = common.parseDOM(result, "SeriesName")[0]
            if show_alt == '': show_alt = show
            show_alt = common.replaceHTMLCodes(show_alt)
            show_alt = show_alt.encode('utf-8')

            url = link().imdb_title % imdb
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            poster = common.parseDOM(result, "poster")[0]
            poster = link().tvdb_image + poster
            poster = common.replaceHTMLCodes(poster)
            poster = poster.encode('utf-8')

            banner = common.parseDOM(result, "banner")[0]
            if not banner == '': banner = link().tvdb_image + banner
            else: banner = poster
            banner = common.replaceHTMLCodes(banner)
            banner = banner.encode('utf-8')

            fanart = common.parseDOM(result, "fanart")[0]
            if not fanart == '': fanart = link().tvdb_image + fanart
            else: fanart = '0'
            fanart = common.replaceHTMLCodes(fanart)
            fanart = fanart.encode('utf-8')

            genre = common.parseDOM(result, "Genre")[0]
            genre = [i for i in genre.split('|') if not i == '']
            genre = " / ".join(genre)
            if genre == '': genre = '0'
            genre = common.replaceHTMLCodes(genre)
            genre = genre.encode('utf-8')

            studio = common.parseDOM(result, "Network")[0]
            if studio == '': studio = '0'
            studio = common.replaceHTMLCodes(studio)
            studio = studio.encode('utf-8')

            status = common.parseDOM(result, "Status")[0]
            if status == '': status = 'Ended'
            status = common.replaceHTMLCodes(status)
            status = status.encode('utf-8')

            duration = common.parseDOM(result, "Runtime")[0]
            if duration == '': duration = '0'
            duration = common.replaceHTMLCodes(duration)
            duration = duration.encode('utf-8')

            rating = common.parseDOM(result, "Rating")[0]
            if rating == '': rating = '0'
            rating = common.replaceHTMLCodes(rating)
            rating = rating.encode('utf-8')

            mpaa = common.parseDOM(result, "ContentRating")[0]
            if mpaa == '': mpaa = '0'
            mpaa = common.replaceHTMLCodes(mpaa)
            mpaa = mpaa.encode('utf-8')

            plot = common.parseDOM(result, "Overview")[0]
            if plot == '': plot = '0'
            plot = common.replaceHTMLCodes(plot)
            plot = plot.encode('utf-8')

            networks = ['BBC One', 'BBC Two', 'BBC Three', 'BBC Four', 'CBBC', 'CBeebies', 'ITV', 'ITV1', 'ITV2', 'ITV3', 'ITV4', 'Channel 4', 'E4', 'More4', 'Channel 5', 'Sky1']
            if studio in networks: country = 'UK'
            else: country = 'US'
            dt = datetime.datetime.utcnow() - datetime.timedelta(hours = 5)
            if country == 'UK': dt = datetime.datetime.utcnow() - datetime.timedelta(hours = 0)
        except:
            return

        self.list = [{'seasons': []}, {'episodes': []}]

        try:
            seasons = common.parseDOM(result, "Episode")
            seasons = [i for i in seasons if common.parseDOM(i, "EpisodeNumber")[0] == '1']
            seasons = [i for i in seasons if not common.parseDOM(i, "SeasonNumber")[0] == '0']
        except:
            return

        for season in seasons:
            try:
                date = common.parseDOM(season, "FirstAired")[0]
                date = common.replaceHTMLCodes(date)
                date = date.encode('utf-8')

                if date == '' or '-00' in date: raise Exception()
                if int(re.sub('[^0-9]', '', str(date)) + '0000') + 10500 > int(dt.strftime("%Y%m%d%H%M")): raise Exception()

                num = common.parseDOM(season, "SeasonNumber")[0]
                num = '%01d' % int(num)
                num = num.encode('utf-8')

                thumb = [i for i in art if common.parseDOM(i, "Season")[0] == num]
                try: thumb = link().tvdb_image + common.parseDOM(thumb[0], "BannerPath")[0]
                except: thumb = poster
                thumb = common.replaceHTMLCodes(thumb)
                thumb = thumb.encode('utf-8')

                self.list[0]['seasons'].append({'title': num, 'year': year, 'imdb': imdb, 'tvdb': tvdb, 'season': num, 'show': show, 'show_alt': show_alt, 'genre': genre, 'url': url, 'poster': poster, 'banner': banner, 'thumb': thumb, 'fanart': fanart, 'studio': studio, 'status': status, 'date': date, 'duration': duration, 'rating': rating, 'mpaa': mpaa, 'plot': plot})
            except:
                pass

        try:
            match = [i['season'] for i in self.list[0]['seasons']]
            episodes = common.parseDOM(result, "Episode")
            if limit == '':
                episodes = [i for i in episodes if '%01d' % int(common.parseDOM(i, "SeasonNumber")[0]) in match]
            else:
                episodes = [i for i in episodes if '%01d' % int(common.parseDOM(i, "SeasonNumber")[0]) == limit]

            episodes = [i for i in episodes if not common.parseDOM(i, "EpisodeNumber")[0] == '0']
        except:
            return

        for episode in episodes:
            try:
                date = common.parseDOM(episode, "FirstAired")[0]
                date = common.replaceHTMLCodes(date)
                date = date.encode('utf-8')

                if date == '' or '-00' in date: raise Exception()
                if int(re.sub('[^0-9]', '', str(date)) + '0000') + 10500 > int(dt.strftime("%Y%m%d%H%M")): raise Exception()

                season = common.parseDOM(episode, "SeasonNumber")[0]
                season = '%01d' % int(season)
                season = season.encode('utf-8')

                num = common.parseDOM(episode, "EpisodeNumber")[0]
                num = re.sub('[^0-9]', '', '%01d' % int(num))
                num = num.encode('utf-8')

                title = common.parseDOM(episode, "EpisodeName")[0]
                title = common.replaceHTMLCodes(title)
                title = title.encode('utf-8')

                name = show_alt + ' S' + '%02d' % int(season) + 'E' + '%02d' % int(num)
                try: name = name.encode('utf-8')
                except: pass

                thumb = common.parseDOM(episode, "filename")[0]
                if not thumb == '': thumb = link().tvdb_image + thumb
                elif not fanart == '0': thumb = fanart.replace(link().tvdb_image, link().tvdb_image2)
                else: thumb = poster
                thumb = common.replaceHTMLCodes(thumb)
                thumb = thumb.encode('utf-8')

                rating = common.parseDOM(episode, "Rating")[0]
                if rating == '': rating = '0'
                rating = common.replaceHTMLCodes(rating)
                rating = rating.encode('utf-8')

                director = common.parseDOM(episode, "Director")[0]
                director = [i for i in director.split('|') if not i == '']
                director = " / ".join(director)
                if director == '': director = '0'
                director = common.replaceHTMLCodes(director)
                director = director.encode('utf-8')

                writer = common.parseDOM(episode, "Writer")[0]
                writer = [i for i in writer.split('|') if not i == '']
                writer = " / ".join(writer)
                if writer == '': writer = '0'
                writer = common.replaceHTMLCodes(writer)
                writer = writer.encode('utf-8')

                try: desc = common.parseDOM(episode, "Overview")[0]
                except: desc = plot
                if desc == '': desc = plot
                desc = common.replaceHTMLCodes(desc)
                desc = desc.encode('utf-8')

                self.list[1]['episodes'].append({'name': name, 'title': title, 'year': year, 'imdb': imdb, 'tvdb': tvdb, 'season': season, 'episode': num, 'show': show, 'show_alt': show_alt, 'genre': genre, 'url': url, 'poster': poster, 'banner': banner, 'thumb': thumb, 'fanart': fanart, 'studio': studio, 'status': status, 'date': date, 'duration': duration, 'rating': rating, 'mpaa': mpaa, 'director': director, 'writer': writer, 'plot': desc})
            except:
                pass

        return self.list

class episodes:
    def __init__(self):
        self.list = []

    def get(self, show, year, imdb, tvdb, season='', idx=True):
        if idx == True:
            #self.list = seasons().tvdb_list(show, year, imdb, tvdb, season)
            try: self.list = cache(seasons().tvdb_list, show, year, imdb, tvdb, season)
            except: return
            self.list = self.list[1]['episodes']
            index().episodeList(self.list)
        else:
            self.list = seasons().tvdb_list(show, year, imdb, tvdb, season)
            return self.list

    def calendar(self, url):
        date = url
        url = link().trakt_tv_calendar % (link().trakt_key, re.sub('[^0-9]', '', str(date)), '1')
        #self.list = self.trakt_list(url)
        try: self.list = cache2(self.trakt_list, url)
        except: return
        self.list = sorted(self.list, key=itemgetter('name'))
        index().episodeList(self.list)

    def added(self):
        if not (link().trakt_user == '' or link().trakt_password == '') and getSetting("trakt_episodes") == 'true':
            now = datetime.datetime.utcnow() - datetime.timedelta(hours = 5)
            date = datetime.date(now.year, now.month, now.day) - datetime.timedelta(days=30)
            url = link().trakt_tv_user_calendar % (link().trakt_key, link().trakt_user, re.sub('[^0-9]', '', str(date)), '31')
            #self.list = self.trakt_list(url)
            try: self.list = cache(self.trakt_list, url)
            except: return
            try: self.list = self.list[::-1]
            except: return
            index().episodeList(self.list)
        else:
            #self.list = self.scn_list()
            try: self.list = cache(self.scn_list)
            except: return
            index().episodeList(self.list)

    def tvrage_redirect(self, title, year, tvdb, season, episode, show, date, genre):
        try:
            exception = True
            if len(season) > 3: exception = False
            genre = [i.strip() for i in genre.split('/')]
            genre = [i for i in genre if any(x == i for x in ['Reality', 'Game Show', 'Talk Show'])]
            if not len(genre) == 0: exception = False
            blocks = ['73141']
            if tvdb in blocks: exception = False
            if exception == True: raise Exception()
        except:
            return (season, episode)

        try:
            tvrage = '0'
            url = link().trakt_tv_search % (link().trakt_key, tvdb)
            result = getUrl(url, timeout='10').result
            result = json.loads(result)
            tvrage = result['tvrage_id']
            tvrage = str(tvrage)
        except:
            pass

        def cleantitle_tv(title):
            title = re.sub('\n|\s(|[(])(UK|US|AU|\d{4})(|[)])$|\s(vs|v[.])\s|(:|;|-|"|,|\'|\.|\?)|\s', '', title).lower()
            return title

        try:
            if not tvrage == '0': raise Exception()
            url = link().tvrage_search % urllib.quote_plus(show)
            result = getUrl(url, timeout='10').result
            result = common.parseDOM(result, "show")
            result = [i for i in result if cleantitle_tv(show) == cleantitle_tv(common.replaceHTMLCodes(common.parseDOM(i, "name")[0])) and any(x in common.parseDOM(i, "started")[0] for x in [str(year), str(int(year)+1), str(int(year)-1)])][0]
            tvrage = common.parseDOM(result, "showid")[0]
            tvrage = str(tvrage)
        except:
            pass

        try:
            if tvrage == '0': raise Exception()
            url = link().epguides_info % tvrage
            result = getUrl(url, timeout='10').result
            search = re.compile('\d+?,(\d+?),(\d+?),.+?,(\d+?/.+?/\d+?),"(.+?)",.+?,".+?"').findall(result)
            d = '%02d/%s/%s' % (int(date.split('-')[2]), {'01':'Jan', '02':'Feb', '03':'Mar', '04':'Apr', '05':'May', '06':'Jun', '07':'Jul', '08':'Aug', '09':'Sep', '10':'Oct', '11':'Nov', '12':'Dec'}[date.split('-')[1]], date.split('-')[0][-2:])
            match = [i for i in search if d == i[2]]
            match += [i for i in search if cleantitle_tv(title) == cleantitle_tv(i[3])]
            season = str('%01d' % int(match[0][0]))
            episode = str('%01d' % int(match[0][1]))
            return (season, episode)
        except:
            pass

        try:
            if tvrage == '0': raise Exception()
            url = link().tvrage_info % tvrage
            result = getUrl(url, timeout='10').result
            search = re.compile('<td.+?><a.+?title=.+?season.+?episode.+?>(\d+?)x(\d+?)<.+?<td.+?>(\d+?/.+?/\d+?)<.+?<td.+?>.+?href=.+?>(.+?)<').findall(result.replace('\n',''))
            d = '%02d/%s/%s' % (int(date.split('-')[2]), {'01':'Jan', '02':'Feb', '03':'Mar', '04':'Apr', '05':'May', '06':'Jun', '07':'Jul', '08':'Aug', '09':'Sep', '10':'Oct', '11':'Nov', '12':'Dec'}[date.split('-')[1]], date.split('-')[0])
            match = [i for i in search if d == i[2]]
            match += [i for i in search if cleantitle_tv(title) == cleantitle_tv(i[3])]
            season = str('%01d' % int(match[0][0]))
            episode = str('%01d' % int(match[0][1]))
            return (season, episode)
        except:
            pass

        return (season, episode)

    def trakt_list(self, url):
        try:
            post = urllib.urlencode({'username': link().trakt_user, 'password': link().trakt_password})

            result = getUrl(url, post=post, timeout='30').result
            episodes = json.loads(result)
        except:
            return

        for i in episodes:
            try:
                date = i['date']
                date = common.replaceHTMLCodes(date)
                date = date.encode('utf-8')

                for episode in i['episodes']:
                    try:
                        title = episode['episode']['title']
                        if title == '': raise Exception()
                        title = common.replaceHTMLCodes(title)
                        title = title.encode('utf-8')

                        year = episode['show']['year']
                        year = re.sub('[^0-9]', '', str(year))
                        year = year.encode('utf-8')

                        imdb = episode['show']['imdb_id']
                        imdb = re.sub('[^0-9]', '', str(imdb))
                        if imdb == '': raise Exception()
                        imdb = imdb.encode('utf-8')

                        tvdb = episode['show']['tvdb_id']
                        tvdb = re.sub('[^0-9]', '', str(tvdb))
                        if tvdb == '': tvdb = '0'
                        tvdb = tvdb.encode('utf-8')

                        season = episode['episode']['season']
                        season = re.sub('[^0-9]', '', '%01d' % int(season))
                        if season == '0': raise Exception()
                        season = season.encode('utf-8')

                        num = episode['episode']['number']
                        num = re.sub('[^0-9]', '', '%01d' % int(num))
                        if num == '0': raise Exception()
                        num = num.encode('utf-8')

                        show_alt = episode['show']['title']
                        if show_alt == '': raise Exception()
                        show_alt = common.replaceHTMLCodes(show_alt)
                        show_alt = show_alt.encode('utf-8')

                        show = re.sub('\s(|[(])(UK|US|AU|\d{4})(|[)])$', '', show_alt)
                        show = common.replaceHTMLCodes(show)
                        show = show.encode('utf-8')

                        name = show_alt + ' S' + '%02d' % int(season) + 'E' + '%02d' % int(num)
                        try: name = name.encode('utf-8')
                        except: pass

                        url = link().imdb_title % imdb
                        url = common.replaceHTMLCodes(url)
                        url = url.encode('utf-8')

                        poster = episode['show']['images']['poster']
                        poster = poster.rsplit('?', 1)[0]
                        poster = poster.replace('zapp.trakt','slurm.trakt')
                        if poster.endswith('poster-dark.jpg'): poster = link().imdb_tv_image
                        poster = common.replaceHTMLCodes(poster)
                        poster = poster.encode('utf-8')

                        banner = episode['show']['images']['banner']
                        banner = banner.rsplit('?', 1)[0]
                        banner = banner.replace('zapp.trakt','slurm.trakt')
                        if banner == '' or banner.endswith('banner-dark.jpg'): banner = poster
                        banner = common.replaceHTMLCodes(banner)
                        banner = banner.encode('utf-8')

                        thumb = episode['episode']['images']['screen']
                        if thumb == '': thumb = poster
                        thumb = common.replaceHTMLCodes(thumb)
                        thumb = thumb.encode('utf-8')

                        fanart = episode['show']['images']['fanart']
                        fanart = fanart.rsplit('?', 1)[0]
                        if fanart == '' or fanart.endswith('fanart-dark.jpg'): fanart = '0'
                        fanart = common.replaceHTMLCodes(fanart)
                        fanart = fanart.encode('utf-8')

                        genre = episode['show']['genres']
                        if genre == []: genre = '0'
                        genre = " / ".join(genre)
                        genre = common.replaceHTMLCodes(genre)
                        genre = genre.encode('utf-8')

                        studio = episode['show']['network']
                        if studio == '': studio = '0'
                        studio = common.replaceHTMLCodes(studio)
                        studio = studio.encode('utf-8')

                        try: duration = str(episode['show']['runtime'])
                        except: duration = '0'
                        if duration == '': duration = '0'
                        duration = common.replaceHTMLCodes(duration)
                        duration = duration.encode('utf-8')

                        rating = str(episode['episode']['ratings']['percentage'])
                        if rating == '': rating = str(episode['show']['ratings']['percentage'])
                        if rating == '': rating = '0'
                        rating = str(int(rating) / 10.0)
                        if rating == '' or rating == '0.0': rating = '0'
                        rating = common.replaceHTMLCodes(rating)
                        rating = rating.encode('utf-8')

                        mpaa = episode['show']['certification']
                        if mpaa == '': mpaa = '0'
                        mpaa = common.replaceHTMLCodes(mpaa)
                        mpaa = mpaa.encode('utf-8')

                        desc = episode['episode']['overview']
                        if desc == '': desc = episode['show']['overview']
                        if desc == '': desc = '0'
                        desc = common.replaceHTMLCodes(desc)
                        desc = desc.encode('utf-8')

                        self.list.append({'name': name, 'title': title, 'year': year, 'imdb': imdb, 'tvdb': tvdb, 'season': season, 'episode': num, 'show': show, 'show_alt': show_alt, 'genre': genre, 'url': url, 'poster': poster, 'banner': banner, 'thumb': thumb, 'fanart': fanart, 'studio': studio, 'status': 'Continuing', 'date': date, 'duration': duration, 'rating': rating, 'mpaa': mpaa, 'director': '0', 'writer': '0', 'plot': desc})
                    except:
                        pass
            except:
                pass

        return self.list

    def scn_list(self):
        try:
            result = getUrl(link().scn_tv_added, timeout='10').result
            result = result.decode('iso-8859-1').encode('utf-8')

            dates = common.parseDOM(result, "tr", attrs = { "class": "MainTable" })
            dates = [re.compile('(\d{4}-\d{2}-\d{2})').findall(i) for i in dates]
            dates = [i[0] for i in dates if not len(i) == 0]
            dates = [i.encode('utf-8') for i in dates]
            dates = uniqueList(dates).list
            dates = dates[:4]

            shows = common.parseDOM(result, "tr", attrs = { "class": "MainTable" })
            shows = [common.parseDOM(i, "a")[0] for i in shows]
            shows = [re.compile('(.*)[.]S\d+?E\d+?[.]').findall(i) for i in shows]
            shows = [i[0] for i in shows if not len(i) == 0]
            shows = [re.sub('\n|\.(UK|US|AU|\d{4})$|\s(vs|v[.])\s|(:|;|-|"|,|\'|\.|\?)|\s', '', i).lower() for i in shows]
            shows = [i.encode('utf-8') for i in shows]
            shows = uniqueList(shows).list

            date = datetime.date(int(dates[-1].split('-')[0]), int(dates[-1].split('-')[1]), int(dates[-1].split('-')[2]))
            url = link().trakt_tv_calendar % (link().trakt_key, re.sub('[^0-9]', '', str(date)), str(len(dates)))
            self.list = self.trakt_list(url)
            self.list = [i for i in self.list if re.sub('\n|\s(|[(])(UK|US|AU|\d{4})(|[)])$|\s(vs|v[.])\s|(:|;|-|"|,|\'|\.|\?)|\s', '', i['show']).lower() in shows]

            self.list = self.list[::-1]
            return self.list
        except:
            return

class trailer:
    def __init__(self):
        self.youtube_base = 'http://www.youtube.com'
        self.youtube_query = 'http://gdata.youtube.com/feeds/api/videos?q='
        self.youtube_watch = 'http://www.youtube.com/watch?v=%s'
        self.youtube_info = 'http://gdata.youtube.com/feeds/api/videos/%s?v=2'

    def run(self, name, url):
        try:
            if url.startswith(self.youtube_base):
                url = self.youtube(url)
                if url == None: raise Exception()
                return url
            elif not url.startswith('http://'):
                url = self.youtube_watch % url
                url = self.youtube(url)
                if url == None: raise Exception()
                return url
            else:
                raise Exception()
        except:
            url = self.youtube_query + name + ' trailer'
            url = self.youtube_search(url)
            if url == None: return
            return url

    def youtube_search(self, url):
        try:
            query = url.split("?q=")[-1].split("/")[-1].split("?")[0]
            url = url.replace(query, urllib.quote_plus(query))
            result = getUrl(url, timeout='10').result
            result = common.parseDOM(result, "entry")
            result = common.parseDOM(result, "id")

            for url in result[:5]:
                url = url.split("/")[-1]
                url = self.youtube_watch % url
                url = self.youtube(url)
                if not url == None: return url
        except:
            return

    def youtube(self, url):
        try:
            id = url.split("?v=")[-1].split("/")[-1].split("?")[0].split("&")[0]
            state, reason = None, None
            result = getUrl(self.youtube_info % id, timeout='10').result
            try:
                state = common.parseDOM(result, "yt:state", ret="name")[0]
                reason = common.parseDOM(result, "yt:state", ret="reasonCode")[0]
            except:
                pass
            if state == 'deleted' or state == 'rejected' or state == 'failed' or reason == 'requesterRegion' : return
            try:
                result = getUrl(self.youtube_watch % id, timeout='10').result
                alert = common.parseDOM(result, "div", attrs = { "id": "watch7-notification-area" })[0]
                return
            except:
                pass
            url = 'plugin://plugin.video.youtube/?action=play_video&videoid=%s' % id
            return url
        except:
            return


class resolver:
    def __init__(self):
        self.sources_dict()
        self.sources = []

    def get_host(self, name, title, year, imdb, tvdb, season, episode, show, show_alt, date, genre, url, meta):
        try:
            if show == None: content = 'movie'
            else: content = 'episode'

            if content == 'movie':
                self.sources = self.sources_movie(name, title, year, imdb, self.hostDict)
            else:
                season, episode = episodes().tvrage_redirect(title, year, tvdb, season, episode, show, date, genre)
                self.sources = self.sources_tv(name, title, year, imdb, tvdb, season, episode, show, show_alt, self.hostDict)

            self.sources = self.sources_filter()
            if self.sources == []: raise Exception()

            meta = json.loads(meta)

            if content == 'movie': 
                index().moviesourceList(self.sources, name, imdb, meta)
            else:
                index().tvsourceList(self.sources, name, imdb, meta)
        except:
            index().infoDialog(language(30314).encode("utf-8"))
            return

    def play_host(self, content, name, imdb, url, source, provider):
        try:
            url = self.sources_resolve(url, provider)
            if url == None: raise Exception()

            if getSetting("playback_info") == 'true':
                index().infoDialog(source, header=name)

            player().run(content, name, url, imdb)
            return url
        except:
            index().infoDialog(language(30314).encode("utf-8"))
            return

    def run(self, name, title, year, imdb, tvdb, season, episode, show, show_alt, date, genre, url):
        try:
            if show == None: content = 'movie'
            else: content = 'episode'

            if content == 'movie':
                self.sources = self.sources_movie(name, title, year, imdb, self.hostDict)
            else:
                season, episode = episodes().tvrage_redirect(title, year, tvdb, season, episode, show, date, genre)
                self.sources = self.sources_tv(name, title, year, imdb, tvdb, season, episode, show, show_alt, self.hostDict)

            self.sources = self.sources_filter()
            if self.sources == []: raise Exception()

            autoplay = getSetting("autoplay")
            if PseudoTV == 'True': autoplay = 'true'
            elif not xbmc.getInfoLabel('Container.FolderPath').startswith(sys.argv[0]):
                autoplay = getSetting("autoplay_library")

            if url == 'dialog://':
                url = self.sources_dialog()
            elif url == 'direct://':
                url = self.sources_direct()
            elif not autoplay == 'true':
                url = self.sources_dialog()
            else:
                url = self.sources_direct()

            if url == None: raise Exception()
            if url == 'close://': return

            if getSetting("playback_info") == 'true':
                index().infoDialog(self.selectedSource, header=name)

            player().run(content, name, url, imdb)
            return url
        except:
            if not PseudoTV == 'True': return
            index().infoDialog(language(30314).encode("utf-8"))
            return

    def cleantitle_movie(self, title):
        title = re.sub('\n|([[].+?[]])|([(].+?[)])|\s(vs|v[.])\s|(:|;|-|"|,|\'|\.|\?)|\s', '', title).lower()
        return title

    def cleantitle_tv(self, title):
        title = re.sub('\n|\s(|[(])(UK|US|AU|\d{4})(|[)])$|\s(vs|v[.])\s|(:|;|-|"|,|\'|\.|\?)|\s', '', title).lower()
        return title

    def sources_movie(self, name, title, year, imdb, hostDict):
        threads = []

        global icefilms_sources
        icefilms_sources = []
        if getSetting("icefilms") == 'true':
            threads.append(Thread(icefilms().mv, name, title, year, imdb, hostDict))

        global primewire_sources
        primewire_sources = []
        if getSetting("primewire") == 'true':
            threads.append(Thread(primewire().mv, name, title, year, imdb, hostDict))

        global movie25_sources
        movie25_sources = []
        if getSetting("movie25") == 'true':
            threads.append(Thread(movie25().mv, name, title, year, imdb, hostDict))

        global flixanity_sources
        flixanity_sources = []
        if getSetting("flixanity") == 'true':
            threads.append(Thread(flixanity().mv, name, title, year, imdb, hostDict))

        global movieshd_sources
        movieshd_sources = []
        if getSetting("movieshd") == 'true':
            threads.append(Thread(movieshd().mv, name, title, year, imdb, hostDict))

        global popcornered_sources
        popcornered_sources = []
        if getSetting("popcornered") == 'true':
            threads.append(Thread(popcornered().mv, name, title, year, imdb, hostDict))

        global muchmovies_sources
        muchmovies_sources = []
        if getSetting("muchmovies") == 'true':
            threads.append(Thread(muchmovies().mv, name, title, year, imdb, hostDict))

        global yify_sources
        yify_sources = []
        if getSetting("yify") == 'true':
            threads.append(Thread(yify().mv, name, title, year, imdb, hostDict))

        global vkbox_sources
        vkbox_sources = []
        if getSetting("vkbox") == 'true':
            threads.append(Thread(vkbox().mv, name, title, year, imdb, hostDict))

        global istreamhd_sources
        istreamhd_sources = []
        if getSetting("istreamhd") == 'true':
            threads.append(Thread(istreamhd().mv, name, title, year, imdb, hostDict))

        global simplymovies_sources
        simplymovies_sources = []
        if getSetting("simplymovies") == 'true':
            threads.append(Thread(simplymovies().mv, name, title, year, imdb, hostDict))

        global moviestorm_sources
        moviestorm_sources = []
        if getSetting("moviestorm") == 'true':
            threads.append(Thread(moviestorm().mv, name, title, year, imdb, hostDict))

        global noobroom_sources
        noobroom_sources = []
        if getSetting("noobroom") == 'true':
            threads.append(Thread(noobroom().mv, name, title, year, imdb, hostDict))

        global einthusan_sources
        einthusan_sources = []
        if getSetting("einthusan") == 'true':
            threads.append(Thread(einthusan().mv, name, title, year, imdb, hostDict))

        [i.start() for i in threads]
        [i.join() for i in threads]

        self.sources = icefilms_sources + primewire_sources + movie25_sources + flixanity_sources + movieshd_sources + popcornered_sources + muchmovies_sources + yify_sources + vkbox_sources + istreamhd_sources + simplymovies_sources + moviestorm_sources + noobroom_sources + einthusan_sources

        return self.sources

    def sources_tv(self, name, title, year, imdb, tvdb, season, episode, show, show_alt, hostDict):
        threads = []

        global icefilms_sources
        icefilms_sources = []
        if getSetting("icefilms_tv") == 'true':
            threads.append(Thread(icefilms().tv, name, title, year, imdb, tvdb, season, episode, show, show_alt, hostDict))

        global primewire_sources
        primewire_sources = []
        if getSetting("primewire_tv") == 'true':
            threads.append(Thread(primewire().tv, name, title, year, imdb, tvdb, season, episode, show, show_alt, hostDict))

        global watchseries_sources
        watchseries_sources = []
        if getSetting("watchseries_tv") == 'true':
            threads.append(Thread(watchseries().tv, name, title, year, imdb, tvdb, season, episode, show, show_alt, hostDict))

        global flixanity_sources
        flixanity_sources = []
        if getSetting("flixanity_tv") == 'true':
            threads.append(Thread(flixanity().tv, name, title, year, imdb, tvdb, season, episode, show, show_alt, hostDict))

        global shush_sources
        shush_sources = []
        if getSetting("shush_tv") == 'true':
            threads.append(Thread(shush().tv, name, title, year, imdb, tvdb, season, episode, show, show_alt, hostDict))

        global ororo_sources
        ororo_sources = []
        if getSetting("ororo_tv") == 'true':
            threads.append(Thread(ororo().tv, name, title, year, imdb, tvdb, season, episode, show, show_alt, hostDict))

        global putlockertv_sources
        putlockertv_sources = []
        if getSetting("putlocker_tv") == 'true':
            threads.append(Thread(putlockertv().tv, name, title, year, imdb, tvdb, season, episode, show, show_alt, hostDict))

        global clickplay_sources
        clickplay_sources = []
        if getSetting("clickplay_tv") == 'true':
            threads.append(Thread(clickplay().tv, name, title, year, imdb, tvdb, season, episode, show, show_alt, hostDict))

        global vkbox_sources
        vkbox_sources = []
        if getSetting("vkbox_tv") == 'true':
            threads.append(Thread(vkbox().tv, name, title, year, imdb, tvdb, season, episode, show, show_alt, hostDict))

        global istreamhd_sources
        istreamhd_sources = []
        if getSetting("istreamhd_tv") == 'true':
            threads.append(Thread(istreamhd().tv, name, title, year, imdb, tvdb, season, episode, show, show_alt, hostDict))

        global simplymovies_sources
        simplymovies_sources = []
        if getSetting("simplymovies_tv") == 'true':
            threads.append(Thread(simplymovies().tv, name, title, year, imdb, tvdb, season, episode, show, show_alt, hostDict))

        global moviestorm_sources
        moviestorm_sources = []
        if getSetting("moviestorm_tv") == 'true':
            threads.append(Thread(moviestorm().tv, name, title, year, imdb, tvdb, season, episode, show, show_alt, hostDict))

        global noobroom_sources
        noobroom_sources = []
        if getSetting("noobroom_tv") == 'true':
            threads.append(Thread(noobroom().tv, name, title, year, imdb, tvdb, season, episode, show, show_alt, hostDict))

        [i.start() for i in threads]
        [i.join() for i in threads]

        self.sources = icefilms_sources + primewire_sources + watchseries_sources + flixanity_sources + shush_sources + ororo_sources + putlockertv_sources + vkbox_sources + clickplay_sources + istreamhd_sources + simplymovies_sources + moviestorm_sources + noobroom_sources

        return self.sources

    def sources_resolve(self, url, provider):
        try:
            if provider == 'Icefilms': url = icefilms().resolve(url)
            elif provider == 'Primewire': url = primewire().resolve(url)
            elif provider == 'Movie25': url = movie25().resolve(url)
            elif provider == 'Watchseries': url = watchseries().resolve(url)
            elif provider == 'Flixanity': url = flixanity().resolve(url)
            elif provider == 'MoviesHD': url = movieshd().resolve(url)
            elif provider == 'Popcornered': url = popcornered().resolve(url)
            elif provider == 'Muchmovies': url = muchmovies().resolve(url)
            elif provider == 'YIFY': url = yify().resolve(url)
            elif provider == 'Shush': url = shush().resolve(url)
            elif provider == 'Ororo': url = ororo().resolve(url)
            elif provider == 'PutlockerTV': url = putlockertv().resolve(url)
            elif provider == 'Clickplay': url = clickplay().resolve(url)
            elif provider == 'VKBox': url = vkbox().resolve(url)
            elif provider == 'iStreamHD': url = istreamhd().resolve(url)
            elif provider == 'Simplymovies': url = simplymovies().resolve(url)
            elif provider == 'Moviestorm': url = moviestorm().resolve(url)
            elif provider == 'Noobroom': url = noobroom().resolve(url)
            elif provider == 'Einthusan': url = einthusan().resolve(url)
            return url
        except:
            return

    def sources_filter(self):
        #hd_rank = ['VK', 'Videomega', 'Popcornered', 'Muchmovies', 'Shush', 'YIFY', 'Noobroom', 'Firedrive', 'Movreel', 'Billionuploads', '180upload', 'Hugefiles', 'Einthusan']
        #sd_rank = ['Ororo', 'Firedrive', 'Putlocker', 'Sockshare', 'Streamin', 'Noobroom', 'iShared', 'Movreel', 'Mightyupload', 'VK', 'Mailru', 'Movshare', 'Promptfile', 'Vodlocker', 'Played', 'Gorillavid', 'Bestreams', 'Daclips', 'Divxstage', 'Vidbull']
        hd_rank = [getSetting("hosthd1"), getSetting("hosthd2"), getSetting("hosthd3"), getSetting("hosthd4"), getSetting("hosthd5"), getSetting("hosthd6"), getSetting("hosthd7"), getSetting("hosthd8"), getSetting("hosthd9"), getSetting("hosthd10"), getSetting("hosthd11"), getSetting("hosthd12"), getSetting("hosthd13")]
        sd_rank = [getSetting("host1"), getSetting("host2"), getSetting("host3"), getSetting("host4"), getSetting("host5"), getSetting("host6"), getSetting("host7"), getSetting("host8"), getSetting("host9"), getSetting("host10"), getSetting("host11"), getSetting("host12"), getSetting("host13"), getSetting("host14"), getSetting("host15"), getSetting("host16"), getSetting("host17"), getSetting("host18"), getSetting("host19"), getSetting("host20")]

        for i in range(len(self.sources)): self.sources[i]['source'] = self.sources[i]['source'].lower()
        self.sources = sorted(self.sources, key=itemgetter('source'))

        filter = []
        for host in hd_rank: filter += [i for i in self.sources if i['quality'] == 'HD' and i['source'].lower() == host.lower()]
        for host in sd_rank: filter += [i for i in self.sources if not i['quality'] == 'HD' and i['source'].lower() == host.lower()]
        filter += [i for i in self.sources if not i['quality'] == 'HD' and not any(x == i['source'].lower() for x in [r.lower() for r in sd_rank])]
        self.sources = filter

        filter = []
        filter += [i for i in self.sources if i['quality'] == 'HD']
        filter += [i for i in self.sources if i['quality'] == 'SD']
        filter += [i for i in self.sources if i['quality'] == 'SCR']
        filter += [i for i in self.sources if i['quality'] == 'CAM']
        self.sources = filter

        if getSetting("play_hd") == 'false':
            self.sources = [i for i in self.sources if not i['quality'] == 'HD']

        count = 1
        for i in range(len(self.sources)):
            self.sources[i]['host'] = self.sources[i]['source']
            self.sources[i]['source'] = str('%02d' % count) + ' | [B]' + self.sources[i]['provider'].upper() + '[/B] | ' + self.sources[i]['source'].upper() + ' | ' + self.sources[i]['quality']
            count = count + 1

        return self.sources

    def sources_dialog(self):
        try:
            sourceList, urlList, providerList = [], [], []

            for i in self.sources:
                sourceList.append(i['source'])
                urlList.append(i['url'])
                providerList.append(i['provider'])

            select = index().selectDialog(sourceList)
            if select == -1: return 'close://'

            url = self.sources_resolve(urlList[select], providerList[select])
            self.selectedSource = self.sources[select]['source']
            return url
        except:
            return

    def sources_direct(self):
        hd_blocks = ['Muchmovies', 'Firedrive', 'Movreel', 'Billionuploads', '180upload', 'Hugefiles']
        hd_blocks = [i.lower() for i in hd_blocks]

        if not (getSetting("realdedrid_user") == '' or getSetting("realdedrid_password") == ''):
            try:
                filter = []
                rd_hosts = getUrl('https://real-debrid.com/api/hosters.php').result
                rd_hosts = [i.split('.')[0].replace('"', '').lower() for i in rd_hosts.split(',')]
                filter += [i for i in self.sources if i['quality'] == 'HD' and i['host'] in rd_hosts]
                filter += [i for i in self.sources if i['quality'] == 'HD' and not i['host'] in hd_blocks]
                filter += [i for i in self.sources if not i['quality'] == 'HD' and i['host'] in rd_hosts]
                filter += [i for i in self.sources if not i['quality'] == 'HD' and not i['host'] in rd_hosts]
                self.sources = filter
            except:
                pass
        else:
            self.sources = [i for i in self.sources if not i['host'] in hd_blocks]

        if getSetting("autoplay_hd") == 'false':
            self.sources = [i for i in self.sources if not i['quality'] == 'HD']

        u = None

        for i in self.sources:
            try:
                url = self.sources_resolve(i['url'], i['provider'])
                xbmc.sleep(1000)
                if url == None: raise Exception()
                if u == None: u = url

                if url.startswith('http://'):
                    request = urllib2.Request(url.rsplit('|', 1)[0])
                    request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.57 Safari/537.36')
                    request.add_header('Cookie', 'video=true')
                    response = urllib2.urlopen(request, timeout=20)
                    chunk = response.read(16 * 1024)
                    response.close()
                    if 'text/html' in str(response.info()["Content-Type"]): raise Exception()

                self.selectedSource = i['source']
                return url
            except:
                pass

        return u

    def sources_dict(self):
        self.hostDict = [
        '2gb-hosting',
        'allmyvideos',
        #'180upload',
        'bayfiles',
        'bestreams',
        #'billionuploads',
        'castamp',
        #'clicktoview',
        'daclips',
        'divxstage',
        'donevideo',
        'ecostream',
        'filenuke',
        'firedrive',
        'gorillavid',
        'hostingbulk',
        #'hugefiles',
        'ishared',
        'jumbofiles',
        'lemuploads',
        'limevideo',
        #'megarelease',
        'mightyupload',
        'movdivx',
        'movpod',
        'movreel',
        'movshare',
        'movzap',
        'muchshare',
        'nosvideo',
        'novamov',
        'nowvideo',
        'played',
        'playwire',
        'primeshare',
        'promptfile',
        'purevid',
        'putlocker',
        'sharerepo',
        'sharesix',
        'sockshare',
        'stagevu',
        'streamcloud',
        'streamin',
        'thefile',
        'uploadc',
        'vidbull',
        'videobb',
        'videoweed',
        'videozed',
        #'vidhog',
        #'vidplay',
        'vidto',
        'vidx',
        #'vidxden',
        'vodlocker',
        #'watchfreeinhd',
        'xvidstage',
        'youtube',
        'yourupload',
        'youwatch',
        'zalaa'
        ]


class icefilms:
    def __init__(self):
        global icefilms_sources
        icefilms_sources = []
        self.base_link = 'http://www.icefilms.info'
        self.moviesearch_link = 'http://www.icefilms.info/movies/a-z/%s'
        self.tvsearch_link = 'http://www.icefilms.info/tv/a-z/%s'
        self.video_link = 'http://www.icefilms.info/membersonly/components/com_iceplayer/video.php?vid=%s'
        self.post_link = 'http://www.icefilms.info/membersonly/components/com_iceplayer/video.phpAjaxResp.php'

    def mv(self, name, title, year, imdb, hostDict):
        try:
            query = title.upper()
            if query.startswith('THE '): query = query.replace('THE ', '')
            elif query.startswith('A '): query = query.replace('A ', '')
            if not query[0].isalpha(): query = '1'
            query = self.moviesearch_link % query[0]

            result = getUrl(query).result
            result = result.decode('iso-8859-1').encode('utf-8')
            id = re.compile('id=%s>.+?href=/ip.php[?]v=(.+?)&' % imdb).findall(result)[0]
            url = self.video_link % id
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            result = getUrl(url).result
            result = result.decode('iso-8859-1').encode('utf-8')
            sec = re.compile('lastChild[.]value="(.+?)"').findall(result)[0]
            links = common.parseDOM(result, "div", attrs = { "class": "ripdiv" })

            import random

            try:
                hd_links = ''
                hd_links = [i for i in links if '>HD 720p<' in i][0]
                hd_links = re.compile("onclick='go[(](.+?)[)]'>Source(.+?)</a>").findall(hd_links)
            except:
                pass

            for url, host in hd_links:
                try:
                    hosts = ['movreel', 'billionuploads', '180upload', 'hugefiles']
                    host = re.sub('<span\s.+?>|</span>|#\d*:','', host)
                    host = host.strip().lower()
                    if not host in hosts: raise Exception()
                    url = 'id=%s&t=%s&sec=%s&s=%s&m=%s&cap=&iqs=&url=' % (url, id, sec, random.randrange(5, 50), random.randrange(100, 300) * -1)
                    icefilms_sources.append({'source': host, 'quality': 'HD', 'provider': 'Icefilms', 'url': url})
                except:
                    pass

            try:
                sd_links = ''
                sd_links = [i for i in links if '>DVDRip / Standard Def<' in i]
                if len(sd_links) == 0: sd_links = [i for i in links if '>DVD Screener<' in i]
                if len(sd_links) == 0: sd_links = [i for i in links if '>R5/R6 DVDRip<' in i]
                sd_links = sd_links[0]
                sd_links = re.compile("onclick='go[(](.+?)[)]'>Source(.+?)</a>").findall(sd_links)
            except:
                pass

            for url, host in sd_links:
                try:
                    hosts = ['movreel']
                    host = re.sub('<span\s.+?>|</span>|#\d*:','', host)
                    host = host.strip().lower()
                    if not host in hosts: raise Exception()
                    url = 'id=%s&t=%s&sec=%s&s=%s&m=%s&cap=&iqs=&url=' % (url, id, sec, random.randrange(5, 50), random.randrange(100, 300) * -1)
                    icefilms_sources.append({'source': host, 'quality': 'SD', 'provider': 'Icefilms', 'url': url})
                except:
                    pass
        except:
            return

    def tv(self, name, title, year, imdb, tvdb, season, episode, show, show_alt, hostDict):
        try:
            query = show.upper()
            if query.startswith('THE '): query = query.replace('THE ', '')
            elif query.startswith('A '): query = query.replace('A ', '')
            if not query[0].isalpha(): query = '1'
            query = self.tvsearch_link % query[0]

            result = getUrl(query).result
            result = result.decode('iso-8859-1').encode('utf-8')
            url = re.compile('id=%s>.+?href=(.+?)>' % imdb).findall(result)[0]
            url = '%s%s' % (self.base_link, url)
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            result = getUrl(url).result
            result = result.decode('iso-8859-1').encode('utf-8')
            id = re.compile('href=/ip.php[?]v=(.+?)&>%01dx%02d' % (int(season), int(episode))).findall(result)[0]
            id = id.split('v=')[-1]
            url = self.video_link % id
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            result = getUrl(url).result
            result = result.decode('iso-8859-1').encode('utf-8')
            sec = re.compile('lastChild[.]value="(.+?)"').findall(result)[0]
            links = common.parseDOM(result, "div", attrs = { "class": "ripdiv" })

            import random

            try:
                hd_links = ''
                hd_links = [i for i in links if '>HD 720p<' in i][0]
                hd_links = re.compile("onclick='go[(](.+?)[)]'>Source(.+?)</a>").findall(hd_links)
            except:
                pass

            for url, host in hd_links:
                try:
                    hosts = ['movreel', 'billionuploads', '180upload', 'hugefiles']
                    host = re.sub('<span\s.+?>|</span>|#\d*:','', host)
                    host = host.strip().lower()
                    if not host in hosts: raise Exception()
                    url = 'id=%s&t=%s&sec=%s&s=%s&m=%s&cap=&iqs=&url=' % (url, id, sec, random.randrange(5, 50), random.randrange(100, 300) * -1)
                    icefilms_sources.append({'source': host, 'quality': 'HD', 'provider': 'Icefilms', 'url': url})
                except:
                    pass

            try:
                sd_links = ''
                sd_links = [i for i in links if '>DVDRip / Standard Def<' in i][0]
                sd_links = re.compile("onclick='go[(](.+?)[)]'>Source(.+?)</a>").findall(sd_links)
            except:
                pass

            for url, host in sd_links:
                try:
                    hosts = ['movreel']
                    host = re.sub('<span\s.+?>|</span>|#\d*:','', host)
                    host = host.strip().lower()
                    if not host in hosts: raise Exception()
                    url = 'id=%s&t=%s&sec=%s&s=%s&m=%s&cap=&iqs=&url=' % (url, id, sec, random.randrange(5, 50), random.randrange(100, 300) * -1)
                    icefilms_sources.append({'source': host, 'quality': 'SD', 'provider': 'Icefilms', 'url': url})
                except:
                    pass
        except:
            return

    def resolve(self, url):
        try:
            result = getUrl(self.post_link, post=url).result
            url = result.split("?url=", 1)[-1]
            url = urllib.unquote_plus(url)

            import commonresolvers
            url = commonresolvers.resolvers().get(url)
            return url
        except:
            return

class primewire:
    def __init__(self):
        global primewire_sources
        primewire_sources = []
        self.base_link = 'http://www.primewire.ag'
        self.key_link = 'http://www.primewire.ag/index.php?search'
        self.moviesearch_link = 'http://www.primewire.ag/index.php?search_keywords=%s&key=%s&search_section=1'
        self.tvsearch_link = 'http://www.primewire.ag/index.php?search_keywords=%s&key=%s&search_section=2'
        self.proxy_link = 'http://unblocked.ws'

    def mv(self, name, title, year, imdb, hostDict):
        try:
            try:
                result = getUrl(self.key_link, mobile=True).result
                key = common.parseDOM(result, "input", ret="value", attrs = { "name": "key" })[0]
                query = self.moviesearch_link % (urllib.quote_plus(re.sub('\'', '', title)), key)
            except:
                result = getUrl(self.proxy_link, mobile=True).result
                proxy = common.parseDOM(result, "a", ret="href")
                proxy = [i.lower() for i in proxy if 'primewire' in i.lower()][0]
                self.key_link = self.key_link.replace(self.base_link, proxy)
                self.moviesearch_link = self.moviesearch_link.replace(self.base_link, proxy)
                self.base_link = proxy

                result = getUrl(self.key_link, mobile=True).result
                key = common.parseDOM(result, "input", ret="value", attrs = { "name": "key" })[0]
                query = self.moviesearch_link % (urllib.quote_plus(re.sub('\'', '', title)), key)

            result = getUrl(query, mobile=True).result
            result = result.decode('iso-8859-1').encode('utf-8')
            result = common.parseDOM(result, "div", attrs = { "class": "index_item.+?" })
            result = [i for i in result if any(x in re.compile('title="Watch (.+?)"').findall(i)[0] for x in ['(%s)' % str(year), '(%s)' % str(int(year)+1), '(%s)' % str(int(year)-1)])]
            result = uniqueList(result).list

            match = [common.parseDOM(i, "a", ret="href")[0] for i in result]
            if match == []: return
            for i in match[:5]:
                try:
                    if not i.startswith('http://'): i = '%s%s' % (self.base_link, i)
                    result = getUrl(i, mobile=True).result
                    if any(x in resolver().cleantitle_movie(result) for x in [str('>' + resolver().cleantitle_movie(title) + '(%s)' % str(year) + '<')]):
                        match2 = i
                    if any(x in resolver().cleantitle_movie(result) for x in [str('>' + resolver().cleantitle_movie(title) + '<')]):
                        match2 = i
                    if str('tt' + imdb) in result:
                        match2 = i
                        break
                except:
                    pass

            url = match2
            result = getUrl(url, mobile=True).result
            result = result.decode('iso-8859-1').encode('utf-8')
            links = common.parseDOM(result, "tbody")

            for i in links:
                try:
                    url = common.parseDOM(i, "a", ret="href")[0]
                    url = re.compile('url=(.+?)&').findall(url)[0]
                    url = base64.urlsafe_b64decode(url.encode('utf-8'))
                    url = common.replaceHTMLCodes(url)
                    url = url.encode('utf-8')

                    host = common.parseDOM(i, "a", ret="href")[0]
                    host = re.compile('domain=(.+?)&').findall(host)[0]
                    host = base64.urlsafe_b64decode(host.encode('utf-8'))
                    host = host.rsplit('.', 1)[0]
                    host = [x for x in hostDict if host.lower() == x.lower()][0]
                    host = host.encode('utf-8')

                    quality = common.parseDOM(i, "span", ret="class")[0]
                    if quality == 'quality_cam' or quality == 'quality_ts': quality = 'CAM'
                    elif quality == 'quality_dvd': quality = 'SD'
                    else:  raise Exception()
                    quality = quality.encode('utf-8')

                    primewire_sources.append({'source': host, 'quality': quality, 'provider': 'Primewire', 'url': url})
                except:
                    pass
        except:
            return

    def tv(self, name, title, year, imdb, tvdb, season, episode, show, show_alt, hostDict):
        try:
            try:
                result = getUrl(self.key_link, mobile=True).result
                key = common.parseDOM(result, "input", ret="value", attrs = { "name": "key" })[0]
                query = self.tvsearch_link % (urllib.quote_plus(re.sub('\'', '', show)), key)
            except:
                result = getUrl(self.proxy_link, mobile=True).result
                proxy = common.parseDOM(result, "a", ret="href")
                proxy = [i.lower() for i in proxy if 'primewire' in i.lower()][0]
                self.key_link = self.key_link.replace(self.base_link, proxy)
                self.tvsearch_link = self.tvsearch_link.replace(self.base_link, proxy)
                self.base_link = proxy

                result = getUrl(self.key_link, mobile=True).result
                key = common.parseDOM(result, "input", ret="value", attrs = { "name": "key" })[0]
                query = self.tvsearch_link % (urllib.quote_plus(re.sub('\'', '', show)), key)

            result = getUrl(query, mobile=True).result
            result = result.decode('iso-8859-1').encode('utf-8')
            result = common.parseDOM(result, "div", attrs = { "class": "index_item.+?" })
            result = [i for i in result if any(x in re.compile('title="Watch (.+?)"').findall(i)[0] for x in ['(%s)' % str(year), '(%s)' % str(int(year)+1), '(%s)' % str(int(year)-1)])]
            result = uniqueList(result).list

            match = [common.parseDOM(i, "a", ret="href")[0] for i in result]
            if match == []: return
            for i in match[:5]:
                try:
                    if not i.startswith('http://'): i = '%s%s' % (self.base_link, i)
                    result = getUrl(i, mobile=True).result
                    if any(x in resolver().cleantitle_tv(result) for x in [str('>' + resolver().cleantitle_tv(show) + '(%s)' % str(year) + '<'), str('>' + resolver().cleantitle_tv(show_alt) + '(%s)' % str(year) + '<')]):
                        match2 = i
                    if any(x in resolver().cleantitle_tv(result) for x in [str('>' + resolver().cleantitle_tv(show) + '<'), str('>' + resolver().cleantitle_tv(show_alt) + '<')]):
                        match2 = i
                    if str('tt' + imdb) in result:
                        match2 = i
                        break
                except:
                    pass

            url = match2.replace('/watch-','/tv-')
            url += '/season-%01d-episode-%01d' % (int(season), int(episode))

            result = getUrl(url, mobile=True).result
            result = result.decode('iso-8859-1').encode('utf-8')
            links = common.parseDOM(result, "tbody")

            for i in links:
                try:
                    url = common.parseDOM(i, "a", ret="href")[0]
                    url = re.compile('url=(.+?)&').findall(url)[0]
                    url = base64.urlsafe_b64decode(url.encode('utf-8'))
                    url = common.replaceHTMLCodes(url)
                    url = url.encode('utf-8')

                    host = common.parseDOM(i, "a", ret="href")[0]
                    host = re.compile('domain=(.+?)&').findall(host)[0]
                    host = base64.urlsafe_b64decode(host.encode('utf-8'))
                    host = host.rsplit('.', 1)[0]
                    host = [x for x in hostDict if host.lower() == x.lower()][0]
                    host = host.encode('utf-8')

                    quality = common.parseDOM(i, "span", ret="class")[0]
                    if quality == 'quality_dvd': quality = 'SD'
                    else:  raise Exception()
                    quality = quality.encode('utf-8')

                    primewire_sources.append({'source': host, 'quality': quality, 'provider': 'Primewire', 'url': url})
                except:
                    pass
        except:
            return

    def resolve(self, url):
        try:
            import commonresolvers
            url = commonresolvers.resolvers().get(url)
            return url
        except:
            return

class movie25:
    def __init__(self):
        global movie25_sources
        movie25_sources = []
        self.base_link = 'http://www.movie25.so'
        self.search_link = 'http://www.movie25.so/search.php?key=%s'

    def mv(self, name, title, year, imdb, hostDict):
        try:
            query = self.search_link % urllib.quote_plus(title)

            result = getUrl(query).result
            result = result.decode('iso-8859-1').encode('utf-8')
            result = common.parseDOM(result, "div", attrs = { "class": "movie_table" })[0]
            result = common.parseDOM(result, "li")

            match = [i for i in result if any(x in i for x in [' (%s)' % str(year), ' (%s)' % str(int(year)+1), ' (%s)' % str(int(year)-1)])]
            match2 = [self.base_link + common.parseDOM(i, "a", ret="href")[0] for i in match]
            if match2 == []: return
            for i in match2[:10]:
                try:
                    result = getUrl(i).result
                    result = result.decode('iso-8859-1').encode('utf-8')
                    if str('tt' + imdb) in result:
                        match3 = result
                        break
                except:
                    pass

            result = common.parseDOM(match3, "div", attrs = { "class": "links_quality" })[0]

            quality = common.parseDOM(result, "h1")[0]
            quality = quality.replace('\n','').rsplit(' ', 1)[-1]
            if quality == 'CAM' or quality == 'TS': quality = 'CAM'
            elif quality == 'SCREENER': quality = 'SCR'
            else: quality = 'SD'

            links = common.parseDOM(result, "ul")
            for i in links:
                try:
                    name = common.parseDOM(i, "a")[0]
                    name = common.replaceHTMLCodes(name)
                    if name.isdigit(): raise Exception()
                    host = common.parseDOM(i, "li", attrs = { "class": "link_name" })[0]
                    host = common.replaceHTMLCodes(host)
                    host = host.encode('utf-8')
                    host = [x for x in hostDict if host.lower() == x.lower()][0]
                    url = common.parseDOM(i, "a", ret="href")[0]
                    url = '%s%s' % (self.base_link, url)
                    url = common.replaceHTMLCodes(url)
                    url = url.encode('utf-8')
                    movie25_sources.append({'source': host, 'quality': quality, 'provider': 'Movie25', 'url': url})
                except:
                    pass
        except:
            return

    def resolve(self, url):
        try:
            result = getUrl(url).result
            result = result.decode('iso-8859-1').encode('utf-8')
            url = common.parseDOM(result, "input", ret="onclick")
            url = [i for i in url if 'location.href' in i and 'http://' in i][0]
            url = url.split("'", 1)[-1].rsplit("'", 1)[0]

            import commonresolvers
            url = commonresolvers.resolvers().get(url)
            return url
        except:
            return

class watchseries:
    def __init__(self):
        global watchseries_sources
        watchseries_sources = []
        self.base_link = 'http://watchseries.ag'
        self.search_link = 'http://watchseries.ag/search/%s'
        self.episode_link = 'http://watchseries.ag/episode/%s_s%s_e%s.html'

    def tv(self, name, title, year, imdb, tvdb, season, episode, show, show_alt, hostDict):
        try:
            query = self.search_link % urllib.quote_plus(show)

            result = getUrl(query, referer=query).result
            result = result.decode('iso-8859-1').encode('utf-8')
            result = result.replace(' (%s)' % str(int(year) - 1), ' (%s)' % year)
            result = re.compile('href="(/serie/.+?)".+?[(]%s[)]' % year).findall(result)
            result = uniqueList(result).list

            match = [self.base_link + i for i in result]
            if match == []: return
            for i in match[:5]:
                try:
                    result = getUrl(i, referer=i).result
                    if any(x in resolver().cleantitle_tv(result) for x in [str('>' + resolver().cleantitle_tv(show) + '<'), str('>' + resolver().cleantitle_tv(show_alt) + '<')]):
                        match2 = i
                    if str('tt' + imdb) in result:
                        match2 = i
                        break
                except:
                    pass

            url = match2.rsplit('/', 1)[-1]
            url = self.episode_link % (url, season, episode)
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            result = getUrl(url, referer=url).result
            result = common.parseDOM(result, "div", attrs = { "id": "lang_1" })[0]

            for host in hostDict:
                try:
                    links = re.compile('<span>%s</span>.+?href="(.+?)"' % host.lower()).findall(result)
                    for url in links:
                        url = '%s%s' % (self.base_link, url)
                        watchseries_sources.append({'source': host, 'quality': 'SD', 'provider': 'Watchseries', 'url': url})
                except:
                    pass
        except:
            return

    def resolve(self, url):
        try:
            result = getUrl(url, referer=url).result
            url = common.parseDOM(result, "a", ret="href", attrs = { "class": "myButton" })[0]
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            import commonresolvers
            url = commonresolvers.resolvers().get(url)
            return url
        except:
            return

class flixanity:
    def __init__(self):
        global flixanity_sources
        flixanity_sources = []
        self.base_link = 'http://www.flixanity.com'
        self.moviesearch_link = 'http://www.flixanity.com/ajax/search.php?q=%s&limit=5'
        self.tvsearch_link = 'http://www.flixanity.com/ajax/search.php?q=%s&limit=5'

    def mv(self, name, title, year, imdb, hostDict):
        try:
            query = self.moviesearch_link % urllib.quote_plus(title)

            result = getUrl(query).result
            result = json.loads(result)
            result = [i for i in result if 'Movie' in i['meta']]

            url = [i for i in result if any(x in resolver().cleantitle_movie(i['title']) for x in [resolver().cleantitle_movie(title)]) and any(x in i['title'] for x in [' (%s)' % str(year), ' (%s)' % str(int(year)+1), ' (%s)' % str(int(year)-1)])]
            if len(url) == 0:
                url = [i for i in result if any(x == resolver().cleantitle_movie(i['title']) for x in [resolver().cleantitle_movie(title)])]
            url = url[0]['permalink']
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            result = getUrl(url).result
            if not str('tt' + imdb) in result: raise Exception()

            result = common.parseDOM(result, "script")
            result = [i for i in result if 'var embeds' in i][0]
            result = result.replace('IFRAME', 'iframe').replace('SRC=', 'src=')
            links = common.parseDOM(result, "iframe", ret="src")
            links = [i.split('player.php?', 1)[-1] for i in links]

            for url in links:
                try:
                    host = re.compile('://(.+?)/').findall(url)[0]
                    host = host.rsplit('.', 1)[0].split('w.', 1)[-1]
                    host = [x for x in hostDict if host.lower() == x.lower()][0]

                    flixanity_sources.append({'source': host, 'quality': 'SD', 'provider': 'Flixanity', 'url': url})
                except:
                    pass
        except:
            return

    def tv(self, name, title, year, imdb, tvdb, season, episode, show, show_alt, hostDict):
        try:
            query = self.tvsearch_link % urllib.quote_plus(show)

            result = getUrl(query).result
            result = json.loads(result)
            result = [i for i in result if 'TV' in i['meta']]

            url = [i for i in result if any(x in resolver().cleantitle_tv(i['title']) for x in [resolver().cleantitle_tv(show), resolver().cleantitle_tv(show_alt)]) and any(x in i['title'] for x in [' (%s)' % str(year), ' (%s)' % str(int(year)+1), ' (%s)' % str(int(year)-1)])]
            if len(url) == 0:
                url = [i for i in result if any(x == resolver().cleantitle_tv(i['title']) for x in [resolver().cleantitle_tv(show), resolver().cleantitle_tv(show_alt)])]
            url = url[0]['permalink']
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            result = getUrl(url).result
            if not str('tt' + imdb) in result: raise Exception()

            url = common.parseDOM(result, "a", ret="href", attrs = { "class": "item" })
            url = [i for i in url if i.endswith('season/%01d/episode/%01d' % (int(season), int(episode)))][0]
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            result = getUrl(url).result
            result = common.parseDOM(result, "script")
            result = [i for i in result if 'var embeds' in i][0]
            result = result.replace('IFRAME', 'iframe').replace('SRC=', 'src=')
            links = common.parseDOM(result, "iframe", ret="src")
            links = [i.split('player.php?', 1)[-1] for i in links]

            for url in links:
                try:
                    host = re.compile('://(.+?)/').findall(url)[0]
                    host = host.rsplit('.', 1)[0].split('w.', 1)[-1]
                    host = [x for x in hostDict if host.lower() == x.lower()][0]

                    flixanity_sources.append({'source': host, 'quality': 'SD', 'provider': 'Flixanity', 'url': url})
                except:
                    pass
        except:
            return

    def resolve(self, url):
        try:
            import commonresolvers
            url = commonresolvers.resolvers().get(url)
            return url
        except:
            return

class movieshd:
    def __init__(self):
        global movieshd_sources
        movieshd_sources = []
        self.base_link = 'http://movieshd.co'
        self.search_link = 'http://movieshd.co/?s=%s'
        self.player_link = 'http://videomega.tv/iframe.php?ref=%s'

    def mv(self, name, title, year, imdb, hostDict):
        try:
            query = self.search_link % (urllib.quote_plus(title))

            result = getUrl(query).result
            url = common.parseDOM(result, "ul", attrs = { "class": "listing-videos.+?" })[0]
            url = common.parseDOM(url, "li", attrs = { "class": ".+?" })
            url = [i for i in url if any(x in resolver().cleantitle_movie(re.sub('[(]\d{4}[)]', '<', i)) for x in [str('>' + resolver().cleantitle_movie(title) + '<')]) and any(x in i for x in [' (%s)' % str(year), ' (%s)' % str(int(year)+1), ' (%s)' % str(int(year)-1)])][0]
            url = common.parseDOM(url, "a", ret="href")[0]
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            result = getUrl(url).result
            url = common.parseDOM(result, "div", attrs = { "class": "video-embed" })[0]
            url = re.compile("ref='(.+?)'").findall(url)[0]
            url = self.player_link % url
            url = url.encode('utf-8')

            import commonresolvers
            url = commonresolvers.resolvers().videomega(url)
            if url == None: return

            movieshd_sources.append({'source': 'Videomega', 'quality': 'HD', 'provider': 'MoviesHD', 'url': url})
        except:
            return

    def resolve(self, url):
        return url

class popcornered:
    def __init__(self):
        global popcornered_sources
        popcornered_sources = []
        self.base_link = 'http://popcornered.com'
        self.search_link = 'http://popcornered.com/search.php'

    def mv(self, name, title, year, imdb, hostDict):
        try:
            post = urllib.urlencode({'query': title})
            result = getUrl(self.search_link, post=post).result

            url = common.parseDOM(result, "li")
            url = [i for i in url if any(x in resolver().cleantitle_movie(common.parseDOM(i, "b")[0]) for x in [resolver().cleantitle_movie(title)]) and any(x == common.parseDOM(i, "h3")[0] for x in [str(year), str(int(year)+1), str(int(year)-1)])][0]
            url = common.parseDOM(url, "a", ret="href")[0]
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            popcornered_sources.append({'source': 'Popcornered', 'quality': 'HD', 'provider': 'Popcornered', 'url': url})
        except:
            return

    def resolve(self, url):
        try:
            result = getUrl(url, mobile=True).result
            url = common.parseDOM(result, "iframe", ret="data-video", attrs = { "onload": ".+?" })[0]
            url = '%s/%s' % (self.base_link, url)
            return url
        except:
            return

class muchmovies:
    def __init__(self):
        global muchmovies_sources
        muchmovies_sources = []
        self.base_link = 'http://www.buzzfilms.co'
        self.search_link = 'http://www.buzzfilms.co/search'

    def mv(self, name, title, year, imdb, hostDict):
        try:
            query = self.search_link + '/' + urllib.quote_plus(title.replace(' ', '-'))

            result = getUrl(query, mobile=True).result
            url = common.parseDOM(result, "li", attrs = { "data-icon": "false" })
            url = [i for i in url if any(x in resolver().cleantitle_movie(i) for x in [str('>' + resolver().cleantitle_movie(title) + '<')]) and any(x in i for x in [' (%s)' % str(year), ' (%s)' % str(int(year)+1), ' (%s)' % str(int(year)-1)])][0]
            url = common.parseDOM(url, "a", ret="href")[0]
            url = '%s%s' % (self.base_link, url)
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            muchmovies_sources.append({'source': 'Muchmovies', 'quality': 'HD', 'provider': 'Muchmovies', 'url': url})
        except:
            return

    def resolve(self, url):
        try:
            result = getUrl(url, mobile=True).result
            url = common.parseDOM(result, "a", ret="href", attrs = { "data-role": "button" })
            url = [i for i in url if str('.mp4') in i][0]
            return url
        except:
            return

class yify:
    def __init__(self):
        global yify_sources
        yify_sources = []
        self.base_link = 'http://yify.tv'
        self.ajax_link = 'http://yify.tv/wp-admin/admin-ajax.php'
        self.post_link = 'action=ajaxy_sf&sf_value=%s'
        self.player_link = 'http://yify.tv/reproductor2/pk/pk/plugins/player_p2.php?url=%s'

    def mv(self, name, title, year, imdb, hostDict):
        try:
            query = self.post_link % (urllib.quote_plus(title))

            result = getUrl(self.ajax_link, post=query).result
            result = result.replace('&#8211;','-')
            url = json.loads(result)
            url = url['post']['all']
            url = [i['post_link'] for i in url if any(x == resolver().cleantitle_movie(i['post_title']) for x in [resolver().cleantitle_movie(title), resolver().cleantitle_movie(title)])][0]
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            result = getUrl(url).result
            if not str('tt' + imdb) in result: raise Exception()

            url = re.compile('showPkPlayer[(]"(.+?)"[)]').findall(result)[0]
            url = self.player_link % url

            result = getUrl(url, referer=url).result
            result = json.loads(result)

            url = [i['url'] for i in result if 'x-shockwave-flash' in i['type']]
            url += [i['url'] for i in result if 'video/mpeg4' in i['type']]
            url = url[-1]

            yify_sources.append({'source': 'YIFY', 'quality': 'HD', 'provider': 'YIFY', 'url': url})
        except:
            return

    def resolve(self, url):
        try:
            url = getUrl(url, output='geturl').result
            if 'requiressl=yes' in url: url = url.replace('http://', 'https://')
            else: url = url.replace('https://', 'http://')
            return url
        except:
            return

class shush:
    def __init__(self):
        global shush_sources
        shush_sources = []
        self.base_link = 'http://www.shush.se'
        self.search_link = 'http://www.shush.se/index.php?shows'
        self.show_link = 'http://www.shush.se/index.php?showlist=%s'

    def tv(self, name, title, year, imdb, tvdb, season, episode, show, show_alt, hostDict):
        try:
            result = getUrl(self.search_link).result
            url = common.parseDOM(result, "a", ret="href")
            url = [i.split('showlist=')[-1] for i in url if 'showlist=' in i]
            url = [i for i in url if any(x == resolver().cleantitle_tv(i) for x in [resolver().cleantitle_tv(show), resolver().cleantitle_tv(show_alt)])][0]
            url = self.show_link % url
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            result = getUrl(url).result
            url = common.parseDOM(result, "div")
            url += common.parseDOM(result, "div", attrs = { "class": ".+?" })
            url = [i for i in url if ' Season %01d Episode: %01d '% (int(season), int(episode)) in i][0]
            url = common.parseDOM(url, "a", ret="href")[0]
            url = '%s/%s' % (self.base_link, url)
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            result = getUrl(url).result
            url = re.compile('proxy[.]link=(.+?)&').findall(result)[-1]

            if url.startswith('http'):
                player = 'http://player.shush.tv/p/plugins_player.php'
                post = urllib.urlencode({'url': url})
                result = getUrl(player, post=post).result
                url = re.compile('"url":"(.+?)"').findall(result)
                url = [i for i in url if 'videoplayback?' in i][-1]
                url = getUrl(url, output='geturl').result
            else:
                import GKDecrypter
                url = url.split('*', 1)[-1]
                url = GKDecrypter.decrypter(198,128).decrypt(url,base64.urlsafe_b64decode('djRBdVhhalplRm83akFNZ1VOWkI='),'ECB').split('\0')[0]

            import commonresolvers
            if 'docs.google.com' in url:
                url = commonresolvers.resolvers().googledocs(url)
            elif 'picasaweb.google.com' in url:
                url = commonresolvers.resolvers().picasaweb(url)

            if not any(x in url for x in ['&itag=22&', '&itag=37&', '&itag=38&', '&itag=45&', '&itag=84&', '&itag=102&', '&itag=120&', '&itag=121&']): return

            shush_sources.append({'source': 'Shush', 'quality': 'HD', 'provider': 'Shush', 'url': url})
        except:
            return

    def resolve(self, url):
        try:
            url = getUrl(url, output='geturl').result
            if 'requiressl=yes' in url: url = url.replace('http://', 'https://')
            else: url = url.replace('https://', 'http://')
            return url
        except:
            return

class ororo:
    def __init__(self):
        global ororo_sources
        ororo_sources = []
        self.base_link = 'http://ororo.tv'
        self.key_link = base64.urlsafe_b64decode('dXNlciU1QnBhc3N3b3JkJTVEPWMyNjUxMzU2JnVzZXIlNUJlbWFpbCU1RD1jMjY1MTM1NiU0MGRyZHJiLmNvbQ==')
        self.sign_link = 'http://ororo.tv/users/sign_in'

    def tv(self, name, title, year, imdb, tvdb, season, episode, show, show_alt, hostDict):
        try:
            result = getUrl(self.base_link).result

            if not "'index show'" in result:
                result = getUrl(self.sign_link, post=self.key_link, close=False).result
                result = getUrl(self.base_link).result
            result = common.parseDOM(result, "div", attrs = { "class": "index show" })

            match = [i for i in result if any(x == resolver().cleantitle_tv(common.parseDOM(i, "a", attrs = { "class": "name" })[0]) for x in [resolver().cleantitle_tv(show), resolver().cleantitle_tv(show_alt)])]
            match2 = [i for i in match if any(x in i for x in ['>%s<' % str(year), '>%s<' % str(int(year)+1), '>%s<' % str(int(year)-1)])][0]
            url = common.parseDOM(match2, "a", ret="href")[0]
            url = '%s%s' % (self.base_link, url)
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            result = getUrl(url).result
            url = common.parseDOM(result, "a", ret="data-href", attrs = { "href": "#%01d-%01d" % (int(season), int(episode)) })[0]
            url = '%s%s' % (self.base_link, url)
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            ororo_sources.append({'source': 'Ororo', 'quality': 'SD', 'provider': 'Ororo', 'url': url})
        except:
            return

    def resolve(self, url):
        try:
            result = getUrl(url).result

            if not "my_video" in result:
                result = getUrl(self.sign_link, post=self.key_link, close=False).result
                result = getUrl(url).result

            url = None
            try: url = common.parseDOM(result, "source", ret="src", attrs = { "type": "video/webm" })[0]
            except: pass
            try: url = url = common.parseDOM(result, "source", ret="src", attrs = { "type": "video/mp4" })[0]
            except: pass

            if url == None: return
            if not url.startswith('http://'): url = '%s%s' % (self.base_link, url)
            url = '%s|Cookie=%s' % (url, urllib.quote_plus('video=true'))

            return url
        except:
            return

class putlockertv:
    def __init__(self):
        global putlockertv_sources
        putlockertv_sources = []
        self.base_link = 'http://putlockertvshows.me'

    def tv(self, name, title, year, imdb, tvdb, season, episode, show, show_alt, hostDict):
        try:
            search = 'http://www.imdbapi.com/?i=tt%s' % imdb
            search = getUrl(search).result
            search = json.loads(search)
            country = [i.strip() for i in search['Country'].split(',')]
            if 'UK' in country and not 'USA' in country: return

            result = getUrl(self.base_link).result
            result = common.parseDOM(result, "tr", attrs = { "class": "fc" })

            match = [i for i in result if any(x == resolver().cleantitle_tv(common.parseDOM(i, "a")[0]) for x in [resolver().cleantitle_tv(show), resolver().cleantitle_tv(show_alt)])][0]
            url = common.parseDOM(match, "a", ret="href")[0]
            url = '%s%s/ifr/s%02de%02d.html' % (self.base_link, url, int(season), int(episode))
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            result = getUrl(url).result
            url = common.parseDOM(result, "div", ret="onclick", attrs = { "class": "badsvideo" })
            if url == []:
                url = common.parseDOM(result, "iframe", ret="src")[-1]
                url = '%s%s' % (self.base_link, url)
                result = getUrl(url).result
                url = common.parseDOM(result, "div", ret="onclick", attrs = { "class": "badsvideo" })
            url = re.compile(".*'(.+?)'").findall(url[0])[0]
            url = '%s%s' % (self.base_link, url)
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            result = getUrl(url).result
            url = common.parseDOM(result, "iframe", ret="src")[0]
            url = url.replace('putlocker', 'firedrive')
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            if 'firedrive' in url: source = 'Firedrive'
            elif 'mail.ru' in url: source = 'Mailru'
            else: return

            putlockertv_sources.append({'source': source, 'quality': 'SD', 'provider': 'PutlockerTV', 'url': url})
        except:
            return

    def resolve(self, url):
        try:
            import commonresolvers
            url = commonresolvers.resolvers().get(url)
            return url
        except:
            return

class clickplay:
    def __init__(self):
        global clickplay_sources
        clickplay_sources = []
        self.base_link = 'http://clickplay.to'
        self.search_link = 'http://clickplay.to/search/%s'

    def tv(self, name, title, year, imdb, tvdb, season, episode, show, show_alt, hostDict):
        try:
            query = self.search_link % urllib.quote_plus(' '.join([i for i in show.split() if i not in ['The','the','A','a']]))
            result = getUrl(query).result
            result = common.parseDOM(result, "div", attrs = { "id": "video_list" })[0]
            result = result.split('</a>')

            match = [i for i in result if any(x in resolver().cleantitle_tv(i) for x in [str('>' + resolver().cleantitle_tv(show) + '(%s)' % str(year) + '<'), str('>' + resolver().cleantitle_tv(show) + '(%s)' % str(int(year)+1) + '<'), str('>' + resolver().cleantitle_tv(show) + '(%s)' % str(int(year)-1) + '<'), str('>' + resolver().cleantitle_tv(show_alt) + '(%s)' % str(year) + '<'), str('>' + resolver().cleantitle_tv(show_alt) + '(%s)' % str(int(year)+1) + '<'), str('>' + resolver().cleantitle_tv(show_alt) + '(%s)' % str(int(year)-1) + '<')])][0]
            url = common.parseDOM(match, "a", ret="href")[0]
            url = '%sseason-%01d/episode-%01d' % (url, int(season), int(episode))
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            import GKDecrypter
            result = getUrl(url).result
            links = re.compile('<a href="([?]link_id=.+?)".+?rel="noindex, nofollow".+?\[720p\].+?</a>').findall(result)
            u = re.compile('content="(%s.+?)"' % url).findall(result)[0]

            for i in links[:5]:
                try:
                    result = getUrl(u + i).result
                    url = re.compile('proxy[.]link=clickplay[*](.+?)"').findall(result)[-1]
                    url = GKDecrypter.decrypter(198,128).decrypt(url,base64.urlsafe_b64decode('bW5pcUpUcUJVOFozS1FVZWpTb00='),'ECB').split('\0')[0]
                    if 'vk.com' in url:
                        import commonresolvers
                        vk = commonresolvers.resolvers().vk(url)
                        for i in vk: clickplay_sources.append({'source': 'VK', 'quality': i['quality'], 'provider': 'Clickplay', 'url': i['url']})
                    elif 'firedrive' in url:
                        clickplay_sources.append({'source': 'Firedrive', 'quality': 'HD', 'provider': 'Clickplay', 'url': url})
                    elif 'mail.ru' in url:
                        clickplay_sources.append({'source': 'Mailru', 'quality': 'SD', 'provider': 'Clickplay', 'url': url})
                except:
                    pass
        except:
            return

    def resolve(self, url):
        try:
            import commonresolvers
            url = commonresolvers.resolvers().get(url)
            return url
        except:
            return

class vkbox:
    def __init__(self):
        global vkbox_sources
        vkbox_sources = []
        self.base_link = 'http://mobapps.cc'
        self.data_link = 'http://mobapps.cc/data/data_en.zip'
        self.moviedata_link = 'movies_lite.json'
        self.tvdata_link = 'tv_lite.json'
        self.moviesearch_link = 'http://mobapps.cc/api/serials/get_movie_data/?id=%s'
        self.tvsearch_link = 'http://mobapps.cc/api/serials/e/?h=%s&u=%s&y=%s'

    def mv(self, name, title, year, imdb, hostDict):
        try:
            #result = self.getdata(self.moviedata_link)
            result = cache2(self.getdata, self.moviedata_link)
            result = json.loads(result)

            match = [i['id'] for i in result if any(x == resolver().cleantitle_movie(i['title']) for x in [resolver().cleantitle_movie(title), resolver().cleantitle_movie(title)]) and any(x == i['year'] for x in [str(year), str(int(year)+1), str(int(year)-1)])][0]
            url = self.moviesearch_link % match
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            request = urllib2.Request(url,None)
            request.add_header('User-Agent', 'android-async-http/1.4.1 (http://loopj.com/android-async-http)')
            response = urllib2.urlopen(request, timeout=5)
            result = response.read()
            response.close()

            param = re.findall('"lang":"en","apple":(\d+?),"google":(\d+?),"microsoft":"(.+?)"', result, re.I)
            num = int(match) + 537
            url = 'https://vk.com/video_ext.php?oid=%s&id=%s&hash=%s' % (str(int(param[0][0]) + num), str(int(param[0][1]) + num), param[0][2])

            import commonresolvers
            url = commonresolvers.resolvers().vk(url)
            for i in url: vkbox_sources.append({'source': 'VK', 'quality': i['quality'], 'provider': 'VKBox', 'url': i['url']})
        except:
            return

    def tv(self, name, title, year, imdb, tvdb, season, episode, show, show_alt, hostDict):
        try:
            search = 'http://www.imdbapi.com/?i=tt%s' % imdb
            search = getUrl(search).result
            search = json.loads(search)
            country = [i.strip() for i in search['Country'].split(',')]
            if 'UK' in country and not 'USA' in country: return

            #result = self.getdata(self.tvdata_link)
            result = cache2(self.getdata, self.tvdata_link)
            result = json.loads(result)

            match = [i['id'] for i in result if any(x == resolver().cleantitle_tv(i['title']) for x in [resolver().cleantitle_tv(show), resolver().cleantitle_tv(show_alt)])][0]
            url = self.tvsearch_link % (match, season, episode)
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            request = urllib2.Request(url,None)
            request.add_header('User-Agent', 'android-async-http/1.4.1 (http://loopj.com/android-async-http)')
            response = urllib2.urlopen(request, timeout=5)
            result = response.read()
            response.close()

            param = re.findall('"lang":"en","apple":(\d+?),"google":(\d+?),"microsoft":"(.+?)"', result, re.I)
            num = int(match) + int(season) + int(episode)
            url = 'https://vk.com/video_ext.php?oid=%s&id=%s&hash=%s' % (str(int(param[0][0]) + num), str(int(param[0][1]) + num), param[0][2])

            import commonresolvers
            url = commonresolvers.resolvers().vk(url)
            for i in url: vkbox_sources.append({'source': 'VK', 'quality': i['quality'], 'provider': 'VKBox', 'url': i['url']})
        except:
            return

    def getdata(self, file):
        try:
            import zipfile, StringIO
            data = urllib2.urlopen(self.data_link, timeout=5).read()
            zip = zipfile.ZipFile(StringIO.StringIO(data))
            result = zip.read(file)
            zip.close()
            return result
        except:
            return

    def resolve(self, url):
        return url

class istreamhd:
    def __init__(self):
        global istreamhd_sources
        istreamhd_sources = []
        self.base_link = 'http://istreamhd.org'
        self.login_link = 'aHR0cDovL2lzdHJlYW1oZC5vcmcvYXBpL2F1dGhlbnRpY2F0ZS5waHA='
        self.search_link = 'aHR0cDovL2lzdHJlYW1oZC5vcmcvYXBpL3NlYXJjaC5waHA='
        self.show_link = 'aHR0cDovL2lzdHJlYW1oZC5vcmcvYXBpL2dldF9zaG93LnBocA=='
        self.get_link = 'aHR0cDovL2lzdHJlYW1oZC5vcmcvYXBpL2dldF92aWRlby5waHA='
        self.mail, self.password = getSetting("istreamhd_mail"), getSetting("istreamhd_password")

    def mv(self, name, title, year, imdb, hostDict):
        try:
            if (self.mail == '' or self.password == ''): raise Exception()

            post = urllib.urlencode({'e-mail': self.mail, 'password': self.password})
            result = getUrl(base64.urlsafe_b64decode(self.login_link), post=post).result
            result = json.loads(result)
            token = result['auth']['token']

            post = urllib.urlencode({'token': token, 'query': title})
            result = getUrl(base64.urlsafe_b64decode(self.search_link), post=post).result
            result = json.loads(result)
            url = result['result']['items']
            url = [i for i in url if str('tt' + imdb) in i['imdb_id']][0]
            url = url['id']

            post = urllib.urlencode({'token': token, 'vid_id': url})
            result = getUrl(base64.urlsafe_b64decode(self.get_link), post=post).result
            result = json.loads(result)
            url = result['video']['url']
            url = url.replace('http://', 'https://')
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            import commonresolvers
            url = commonresolvers.resolvers().vk(url)
            for i in url: istreamhd_sources.append({'source': 'VK', 'quality': i['quality'], 'provider': 'iStreamHD', 'url': i['url']})
        except:
            return

    def tv(self, name, title, year, imdb, tvdb, season, episode, show, show_alt, hostDict):
        try:
            if (self.mail == '' or self.password == ''): raise Exception()

            post = urllib.urlencode({'e-mail': self.mail, 'password': self.password})
            result = getUrl(base64.urlsafe_b64decode(self.login_link), post=post).result
            result = json.loads(result)
            token = result['auth']['token']

            post = urllib.urlencode({'token': token, 'query': show})
            result = getUrl(base64.urlsafe_b64decode(self.search_link), post=post).result
            result = json.loads(result)
            url = result['result']['items']
            url = [i for i in url if str('tt' + imdb) in i['poster']][0]

            post = urllib.urlencode({'token': token, 'show': url['title'], 'cat_id': url['cat_id']})
            result = getUrl(base64.urlsafe_b64decode(self.show_link), post=post).result
            result = json.loads(result)
            url = result['result']['items']
            url = [i for i in url if i['season'] == str('%01d' % int(season)) and  i['episode'] == str('%01d' % int(episode))][0]
            url = url['vid_id']

            post = urllib.urlencode({'token': token, 'vid_id': url})
            result = getUrl(base64.urlsafe_b64decode(self.get_link), post=post).result
            result = json.loads(result)
            url = result['video']['url']
            url = url.replace('http://', 'https://')
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            import commonresolvers
            url = commonresolvers.resolvers().vk(url)
            for i in url: istreamhd_sources.append({'source': 'VK', 'quality': i['quality'], 'provider': 'iStreamHD', 'url': i['url']})
        except:
            return

    def resolve(self, url):
        return url

class simplymovies:
    def __init__(self):
        global simplymovies_sources
        simplymovies_sources = []
        self.base_link = 'http://simplymovies.net'
        self.moviesearch_link = 'http://simplymovies.net/index.php?searchTerm='
        self.tvsearch_link = 'http://simplymovies.net/tv_shows.php?searchTerm='

    def mv(self, name, title, year, imdb, hostDict):
        try:
            query = self.moviesearch_link + urllib.quote_plus(title.replace(' ', '-'))

            result = getUrl(query).result
            url = common.parseDOM(result, "div", attrs = { "class": "movieInfoHolder" })
            try: match = [i for i in url if any(x in resolver().cleantitle_movie(i) for x in [str('>' + resolver().cleantitle_movie(title) + '<')]) and any(x in i for x in [', %s<' % str(year), ', %s<' % str(int(year)+1), ', %s<' % str(int(year)-1)])][0]
            except: pass
            try: match = [i for i in url if str('tt' + imdb) in i][0]
            except: pass
            url = common.parseDOM(match, "a", ret="href")[0]
            url = '%s/%s' % (self.base_link, url)
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            result = getUrl(url).result
            url = common.parseDOM(result, "iframe", ret="src", attrs = { "class": "videoPlayerIframe" })[0]
            url = common.replaceHTMLCodes(url)
            url = url.replace('http://', 'https://')
            url = url.encode('utf-8')

            import commonresolvers
            url = commonresolvers.resolvers().vk(url)
            for i in url: simplymovies_sources.append({'source': 'VK', 'quality': i['quality'], 'provider': 'Simplymovies', 'url': i['url']})
        except:
            return

    def tv(self, name, title, year, imdb, tvdb, season, episode, show, show_alt, hostDict):
        try:
            query = self.tvsearch_link + urllib.quote_plus(show.replace(' ', '-'))

            result = getUrl(query).result
            url = common.parseDOM(result, "div", attrs = { "class": "movieInfoHolder" })
            try: match = [i for i in url if any(x in resolver().cleantitle_tv(i) for x in [str('>' + resolver().cleantitle_tv(show) + '<'), str('>' + resolver().cleantitle_tv(show_alt) + '<')])][0]
            except: pass
            try: match = [i for i in url if str('tt' + imdb) in i][0]
            except: pass
            url = common.parseDOM(match, "a", ret="href")[0]
            url = '%s/%s' % (self.base_link, url)
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            result = getUrl(url).result
            url = result.split('<h3>')
            url = [i for i in url if str('Season %01d</h3>' % int(season)) in i][-1]
            url = url.replace(':','<')
            url = re.compile('.*href="(.+?)">Episode %01d<' % int(episode)).findall(url)[0]
            url = '%s/%s' % (self.base_link, url)
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            result = getUrl(url).result
            url = common.parseDOM(result, "iframe", ret="src", attrs = { "class": "videoPlayerIframe" })[0]
            url = common.replaceHTMLCodes(url)
            url = url.replace('http://', 'https://')
            url = url.encode('utf-8')

            import commonresolvers
            url = commonresolvers.resolvers().vk(url)
            for i in url: simplymovies_sources.append({'source': 'VK', 'quality': i['quality'], 'provider': 'Simplymovies', 'url': i['url']})
        except:
            return

    def resolve(self, url):
        return url

class moviestorm:
    def __init__(self):
        global moviestorm_sources
        moviestorm_sources = []
        self.base_link = 'http://moviestorm.eu'
        self.search_link = 'http://moviestorm.eu/search?q=%s'

    def mv(self, name, title, year, imdb, hostDict):
        try:
            query = self.search_link % (urllib.quote_plus(title))

            result = getUrl(query).result
            url = common.parseDOM(result, "div", attrs = { "class": "movie_box" })
            url = [i for i in url if str('tt' + imdb) in i][0]
            url = common.parseDOM(url, "a", ret="href")[0]
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            result = getUrl(url).result
            result = common.parseDOM(result, "div", attrs = { "class": "links" })[0]
            links = common.parseDOM(result, "tr")
            links = [i for i in links if 'http://ishared.eu/' in i]

            sd_links = [re.compile('"(http://ishared.eu/.+?)"').findall(i)[0] for i in links if not any(x in common.parseDOM(i, "td", attrs = { "class": "quality_td" })[0] for x in ['CAM', 'TS'])]
            ts_links = [re.compile('"(http://ishared.eu/.+?)"').findall(i)[0] for i in links if any(x in common.parseDOM(i, "td", attrs = { "class": "quality_td" })[0] for x in ['CAM', 'TS'])]

            if (len(sd_links) == 1):
                moviestorm_sources.append({'source': 'iShared', 'quality': 'SD', 'provider': 'Moviestorm', 'url': sd_links[0]})
            if (len(ts_links) == 1):
                moviestorm_sources.append({'source': 'iShared', 'quality': 'CAM', 'provider': 'Moviestorm', 'url': ts_links[0]})
        except:
            return

    def tv(self, name, title, year, imdb, tvdb, season, episode, show, show_alt, hostDict):
        try:
            query = self.search_link % (urllib.quote_plus(show))

            result = getUrl(query).result
            url = common.parseDOM(result, "div", attrs = { "class": "movie_box" })
            url = [i for i in url if str('tt' + imdb) in i][0]
            url = common.parseDOM(url, "a", ret="href")[0]
            url = '%s?season=%01d&episode=%01d' % (url, int(season), int(episode))
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            result = getUrl(url).result
            result = common.parseDOM(result, "div", attrs = { "id": "searialinks" })[0]
            links = re.compile('"(http://ishared.eu/.+?)"').findall(result)

            for url in links:
                moviestorm_sources.append({'source': 'iShared', 'quality': 'SD', 'provider': 'Moviestorm', 'url': url})
        except:
            return

    def resolve(self, url):
        try:
            import commonresolvers
            url = commonresolvers.resolvers().get(url)
            return url
        except:
            return

class noobroom:
    def __init__(self):
        global noobroom_sources
        noobroom_sources = []
        self.base_link = 'http://superchillin.com'
        self.search_link = 'http://superchillin.com/search.php?q=%s'
        self.login_link = 'http://superchillin.com/login.php'
        self.login2_link = 'http://superchillin.com/login2.php'
        self.mail, self.password = getSetting("noobroom_mail"), getSetting("noobroom_password")

    def mv(self, name, title, year, imdb, hostDict):
        try:
            if (self.mail == '' or self.password == ''): raise Exception()

            query = self.search_link % (urllib.quote_plus(title))

            result = self.login()
            result = getUrl(query).result

            url = re.compile('(<i>Movies</i>.+)').findall(result)[0]
            url = url.split("'tippable'")
            url = [i for i in url if any(x in resolver().cleantitle_movie(i) for x in [str('>' + resolver().cleantitle_movie(title) + '<')]) and any(x in i for x in [' (%s)' % str(year), ' (%s)' % str(int(year)+1), ' (%s)' % str(int(year)-1)])][0]
            url = re.compile("href='(.+?)'").findall(url)[0]
            url = '%s%s' % (self.base_link, url)
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            result = getUrl(url).result

            if not str('tt' + imdb) in result: raise Exception()

            links = re.compile('"file": "(.+?)"').findall(result)
            try: u = [i for i in links if 'type=flv' in i][0]
            except: pass
            try: u = [i for i in links if 'type=mp4' in i][0]
            except: pass
            url = '%s%s' % (self.base_link, u)
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            try:
                quality = 'SD'
                q = re.compile('"width": "(.+?)"').findall(result)[0]
                if int(q) > 720: quality = 'HD'
            except:
                pass

            noobroom_sources.append({'source': 'Noobroom', 'quality': quality, 'provider': 'Noobroom', 'url': url})
        except:
            return

    def tv(self, name, title, year, imdb, tvdb, season, episode, show, show_alt, hostDict):
        try:
            if (self.mail == '' or self.password == ''): raise Exception()

            search = 'http://www.imdbapi.com/?i=tt%s' % imdb
            search = getUrl(search).result
            search = json.loads(search)
            country = [i.strip() for i in search['Country'].split(',')]
            if 'UK' in country and not 'USA' in country: return

            query = self.search_link % (urllib.quote_plus(show))

            result = self.login()
            result = getUrl(query).result

            url = re.compile('(<i>TV Series</i>.+)').findall(result)[0]
            url = url.split("><a ")
            url = [i for i in url if any(x in resolver().cleantitle_tv(i) for x in [str('>' + resolver().cleantitle_tv(show) + '<'), str('>' + resolver().cleantitle_tv(show_alt) + '<')])][0]
            url = re.compile("href='(.+?)'").findall(url)[0]
            url = '%s%s' % (self.base_link, url)
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            result = getUrl(url).result
            url = re.compile("<b>%01dx%02d .+?style=.+? href='(.+?)'" % (int(season), int(episode))).findall(result)[0]
            url = '%s%s' % (self.base_link, url)
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            result = getUrl(url).result
            links = re.compile('"file": "(.+?)"').findall(result)
            try: u = [i for i in links if 'type=flv' in i][0]
            except: pass
            try: u = [i for i in links if 'type=mp4' in i][0]
            except: pass
            url = '%s%s' % (self.base_link, u)
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            try:
                quality = 'SD'
                q = re.compile('"width": "(.+?)"').findall(result)[0]
                if int(q) > 720: quality = 'HD'
            except:
                pass

            noobroom_sources.append({'source': 'Noobroom', 'quality': quality, 'provider': 'Noobroom', 'url': url})
        except:
            return

    def login(self):
        try:
            post = urllib.urlencode({'email': self.mail, 'password': self.password})
            result = getUrl(self.login_link, close=False).result
            cookie = getUrl(self.login_link, output='cookie').result
            result = urllib2.Request(self.login2_link, post)
            result = urllib2.urlopen(result, timeout=5)
        except:
            return

    def resolve(self, url):
        try:
            result = self.login()
            try: u = getUrl(url, output='geturl').result
            except: pass
            try: u = getUrl(url.replace('&hd=0', '&hd=1'), output='geturl').result
            except: pass
            return u
        except:
            return

class einthusan:
    def __init__(self):
        global einthusan_sources
        einthusan_sources = []
        self.base_link = 'http://www.einthusan.com'
        self.search_link = 'http://www.einthusan.com/search/?search_query=%s&lang=%s'

    def mv(self, name, title, year, imdb, hostDict):
        try:
            search = 'http://www.imdbapi.com/?i=tt%s' % imdb
            search = getUrl(search).result
            search = json.loads(search)
            country = [i.strip() for i in search['Country'].split(',')]
            if not 'India' in country: return

            language = [i.strip().lower() for i in search['Language'].split(',')]
            language = [i for i in language if any(x == i for x in ['hindi', 'tamil', 'telugu', 'malayalam'])][0]

            query = self.search_link % (urllib.quote_plus(title), language)

            result = getUrl(query).result
            result = common.parseDOM(result, "div", attrs = { "class": "search-category" })
            result = [i for i in result if 'Movies' in common.parseDOM(i, "p")[0]][0]
            result = common.parseDOM(result, "li")

            url = [i for i in result if any(x in resolver().cleantitle_movie(common.parseDOM(i, "a")[0]) for x in [resolver().cleantitle_movie(title)]) and any(x in common.parseDOM(i, "a")[0] for x in [' (%s)' % str(year), ' (%s)' % str(int(year)+1), ' (%s)' % str(int(year)-1)])]
            if len(url) == 0:
                url = [i for i in result if any(x == resolver().cleantitle_movie(common.parseDOM(i, "a")[0]) for x in [resolver().cleantitle_movie(title)])]
            url = common.parseDOM(url, "a", ret="href")[0]
            url = url.replace('../', '%s/' % self.base_link)
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            result = getUrl(url).result

            y = common.parseDOM(result, "div", attrs = { "class": "movie-description" })[0]
            if not any(x in y for x in [str(year), str(int(year)+1), str(int(year)-1)]): return

            url = re.compile("'file': '(.+?)'").findall(result)[0]

            einthusan_sources.append({'source': 'Einthusan', 'quality': 'HD', 'provider': 'Einthusan', 'url': url})
        except:
            return

    def resolve(self, url):
        return url


main()