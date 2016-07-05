import urllib,re,xbmcplugin,xbmcgui,xbmc,xbmcaddon,os,xbmcvfs,shutil
import requests
from addon.common.addon import Addon
from addon.common.net import Net
from metahandler import metahandlers
from resources.libs import jsunpack

#Free Movies Add-on Created By Mucky Duck (3/2016)

User_Agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.89 Safari/537.36'
addon_id='plugin.video.mdfm'
selfAddon = xbmcaddon.Addon(id=addon_id)
addon_name = selfAddon.getAddonInfo('name')
addon = Addon(addon_id, sys.argv)
art = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id + '/resources/art/'))
icon = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
fanart = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id , 'fanart.jpg'))
metaset = selfAddon.getSetting('enable_meta')
show_tv = selfAddon.getSetting('enable_shows')
metaget = metahandlers.MetaData()
baseurl = 'http://fmovies.to'
s = requests.session()
net = Net()



def CAT():
        if metaset == 'true':
                addDir('[B][COLOR mediumaquamarine]Meta Settings[/COLOR][/B]','url',13,icon,fanart,'')
        addDir('[B][COLOR mediumaquamarine]Most Watched[/COLOR][/B]',baseurl+'/filter?sort=views%3Adesc&type%5B%5D=movie',1,icon,fanart,'')
        addDir('[B][COLOR mediumaquamarine]Release Date[/COLOR][/B]',baseurl+'/filter?sort=year%3Adesc&type%5B%5D=movie',1,icon,fanart,'')
        addDir('[B][COLOR mediumaquamarine]Country[/COLOR][/B]',baseurl,7,icon,fanart,'')
        addDir('[B][COLOR mediumaquamarine]Search[/COLOR][/B]','url',4,icon,fanart,'')
        addDir('[B][COLOR mediumaquamarine]Latest[/COLOR][/B]',baseurl+'/filter?sort=post_date%3Adesc&type%5B%5D=movie',1,icon,fanart,'')
        addDir('[B][COLOR mediumaquamarine]Genre[/COLOR][/B]',baseurl,5,icon,fanart,'')
        addDir('[B][COLOR mediumaquamarine]IMDB[/COLOR][/B]',baseurl+'/filter?sort=imdb%3Adesc&type%5B%5D=movie',1,icon,fanart,'')
        addDir('[B][COLOR mediumaquamarine]Year[/COLOR][/B]',baseurl,8,icon,fanart,'')
        addDir('[B][COLOR mediumaquamarine]A/Z[/COLOR][/B]',baseurl+'/filter?sort=title%3Aasc&type%5B%5D=movie',1,icon,fanart,'')
        if show_tv == 'true':
                addDir('[B][COLOR mediumaquamarine]TV[/COLOR][/B]','url',9,icon,fanart,'')
        




def TV():
        addDir('[B][COLOR mediumaquamarine]Most Watched[/COLOR][/B]',baseurl+'/filter?sort=views%3Adesc&type%5B%5D=series',2,icon,fanart,'')
        addDir('[B][COLOR mediumaquamarine]Released[/COLOR][/B]',baseurl+'/filter?sort=year%3Adesc&type%5B%5D=series',2,icon,fanart,'')
        addDir('[B][COLOR mediumaquamarine]Country[/COLOR][/B]','url',15,icon,fanart,'')
        addDir('[B][COLOR mediumaquamarine]Search[/COLOR][/B]','url',10,icon,fanart,'')
        addDir('[B][COLOR mediumaquamarine]Latest[/COLOR][/B]',baseurl+'/filter?sort=post_date%3Adesc&type%5B%5D=series',2,icon,fanart,'')
        addDir('[B][COLOR mediumaquamarine]Genre[/COLOR][/B]','url',14,icon,fanart,'')
        addDir('[B][COLOR mediumaquamarine]IMDB[/COLOR][/B]',baseurl+'/filter?sort=imdb%3Adesc&type%5B%5D=series',2,icon,fanart,'')
        addDir('[B][COLOR mediumaquamarine]Year[/COLOR][/B]','url',16,icon,fanart,'')
        addDir('[B][COLOR mediumaquamarine]A/Z[/COLOR][/B]',baseurl+'/filter?sort=title%3Aasc&type%5B%5D=series',2,icon,fanart,'')
        


def INDEX(url):
        if baseurl not in url:
                url = baseurl + url
        link = OPEN_URL(url)
        link = link.encode('ascii', 'ignore').decode('ascii')
        all_videos = regex_get_all(link, '"item"', '</a> </div> </div>')
        items = len(all_videos)
        for a in all_videos:
                name = regex_from_to(a, '<a class="name" href=.*?>', '<')
                name = addon.unescape(name)
                name = name.encode('ascii', 'ignore').decode('ascii')
                url = regex_from_to(a, 'href="', '"').replace("&amp;","&")
                thumb = regex_from_to(a, 'src="', '"')
                eps = regex_from_to(a, '<div class="status">', '</')
                eps = eps.replace('<span>',' ')
                if eps =='':
                        if metaset=='true':
                                addDir2('[B][COLOR white]%s[/COLOR][/B]' %name,url,3,thumb,items)
                        else:
                                addDir('[B][COLOR white]%s[/COLOR][/B]' %name,url,3,thumb,fanart,'')
        try:
                pn = re.findall(r'<li><a href="(.*?)".*?>(.*?)</a></li>', str(link), re.I|re.DOTALL)
                for url,name in pn:
                        url = url.replace('&amp;','&')
                        if 'page=' in url:
                                nono = ['&raquo;', '&laquo;']
                                if name not in nono:
                                        addDir('[B][COLOR mediumaquamarine]Page %s[/COLOR][/B]' %name,baseurl+'/'+url,1,icon,fanart,'')
                                else:
                                        name = name.replace('&raquo;','>>Next Page>>>')
                                        name = name.replace('&laquo;','<<<Previous Page<<')
                                        addDir('[B][COLOR mediumaquamarine]%s[/COLOR][/B]' %name,baseurl+'/'+url,1,icon,fanart,'')
        except:pass
        setView('movies', 'movie-view')




def INDEX2(url):
        if baseurl not in url:
                url = baseurl + url
        link = OPEN_URL(url)
        link = link.encode('ascii', 'ignore').decode('ascii')
        all_videos = regex_get_all(link, '"item"', '</a> </div> </div>')
        items = len(all_videos)
        for a in all_videos:
                name = regex_from_to(a, '<a class="name" href=.*?>', '<')
                name = addon.unescape(name)
                name = name.encode('ascii', 'ignore').decode('ascii')
                url = regex_from_to(a, 'href="', '"').replace("&amp;","&")
                thumb = regex_from_to(a, 'src="', '"')
                eps = regex_from_to(a, '<div class="status">', '</')
                eps = eps.replace('<span>',' ')
                if eps > '':
                        if metaset=='true':
                                addDir3('[B][COLOR white]%s [/COLOR][/B][I][COLOR mediumaquamarine](%s)[/COLOR][/I]' %(name,eps),url,6,thumb,items,'',name)
                        else:
                                addDir('[B][COLOR white]%s [/COLOR][/B][I][COLOR mediumaquamarine](%s)[/COLOR][/I]' %(name,eps),url,6,thumb,fanart,'')
        try:
                pn = re.findall(r'<li><a href="(.*?)".*?>(.*?)</a></li>', str(link), re.I|re.DOTALL)
                for url,name in pn:
                        url = url.replace('&amp;','&')
                        if 'page=' in url:
                                nono = ['&raquo;', '&laquo;']
                                if name not in nono:
                                        addDir('[B][COLOR mediumaquamarine]Page %s[/COLOR][/B]' %name,baseurl+'/'+url,2,icon,fanart,'')
                                else:
                                        name = name.replace('&raquo;','>>Next Page>>>')
                                        name = name.replace('&laquo;','<<<Previous Page<<')
                                        addDir('[B][COLOR mediumaquamarine]%s[/COLOR][/B]' %name,baseurl+'/'+url,2,icon,fanart,'')
        except:pass

        setView('tvshows', 'show-view')




def EPIS(url,iconimage,show_title):
        url = baseurl + url
        if iconimage == '' or iconimage == None:
                iconimage = icon
        link = OPEN_URL(url)
        link = link.encode('ascii', 'ignore')
        match=re.compile('<a.*?data-id="(.*?)" href="(.*?)">(.*?)</a>').findall(link)[1:]
        items = len(match)
        for data_id,url,name in match:
                if 'film/' in url:
                        if metaset=='true':
                                addDir3('[B][COLOR white]Episode [/COLOR][/B][B][I][COLOR mediumaquamarine]%s[/COLOR][/I][/B]' %name,url,11,iconimage,items,data_id,show_title)
                        else:
                                addDir('[B][COLOR white]Episode [/COLOR][/B][B][I][COLOR mediumaquamarine]%s[/COLOR][/I][/B]' %name,url,11,iconimage,fanart,data_id)
                        
        setView('tvshows', 'show-view')




def LINK(name,url,iconimage):
        url = baseurl + url
        link = OPEN_URL(url)
        link = link.encode('ascii', 'ignore')
        match = re.findall(r'<i class="fa fa-server"></i> (.*?) </label> <div class="col-md-20 col-sm-19"> <ul class="episodes range active" data-range-id="0"> <li> <a class="active" data-id="(.*?)" href="(.*?)">.*?</a> </li>', str(link), re.I|re.DOTALL)
        for name2,data_id,url in match:
                if 'Server F2' in name2:
                        try:
                                form_data={'id': data_id, 'update': '0'}
                                headers = {'content-type':'application/json, text/javascript, */*; q=0.01', 'referer': url,
                                           'user-agent':User_Agent,'x-requested-with':'XMLHttpRequest'}
                                #form_data.update(__get_token(form_data))
                                requestURL = baseurl + '/ajax/episode/info?id=' + data_id + '&update=0'
                                r = s.get(requestURL, data=form_data, headers=headers).json()
                                print '##############################r='+str(r)
                                if 'videomega' in r['target']:
                                        requestUrl2 = r['target']
                                        headers = {'Host': 'videomega.tv', 'Referer': url, 'User-Agent': User_Agent}
                                        link = requests.get(requestUrl2, headers=headers).content
                                        if jsunpack.detect(link):
                                                js_data = jsunpack.unpack(link)
                                                url = re.search('"src"\s*,\s*"([^"]+)', js_data)
                                        host =  url.group(1).replace('http://','').replace('https://','').partition('/')[0]
                                        headers = {'Host': host, 'Origin': 'http://videomega.tv', 'Referer': requestUrl2, 'User-Agent': User_Agent}
                                        url = url.group(1) + '|' + urllib.urlencode(headers)
                                        liz = xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
                                        liz.setInfo(type='Video', infoLabels={'Title':description})
                                        liz.setProperty("IsPlayable","true")
                                        liz.setPath(str(url))
                                        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
                                else:
                                        requestURL2 = r['grabber']
                                        params = r['params']
                                        params.update({'mobile': '1'})
                                        #params.update(__get_token(params))
                                        #headers = {'host':'player.fmovies.to', 'origin':'http://fmovies.to', 'referer':url, 'user-agent':User_Agent}
                                        headers = {'referer':url, 'user-agent':User_Agent}
                                        r2 = requests.get(requestURL2, params=params, headers=headers).json()
                                        print '##############################r='+str(r)
                                        try:
                                                url = r2['data'][-1]['file']
                                        except:
                                                url = r2['data'][0]['file']
                                        liz = xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
                                        liz.setInfo(type='Video', infoLabels={'Title':description})
                                        liz.setProperty("IsPlayable","true")
                                        liz.setPath(str(url))
                                        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
                        except: pass
                if 'Server F1' in name2:
                        try:
                                form_data={'id': data_id, 'update': '0'}
                                headers = {'content-type':'application/json, text/javascript, */*; q=0.01', 'referer': url,
                                           'user-agent':User_Agent,'x-requested-with':'XMLHttpRequest'}
                                #form_data.update(__get_token(form_data))
                                requestURL = baseurl + '/ajax/episode/info?id=' + data_id + '&update=0'
                                r = s.get(requestURL, data=form_data, headers=headers).json()
                                if 'videomega' in r['target']:
                                        requestUrl2 = r['target']
                                        headers = {'Host': 'videomega.tv', 'Referer': url, 'User-Agent': User_Agent}
                                        link = requests.get(requestUrl2, headers=headers).content
                                        if jsunpack.detect(link):
                                                js_data = jsunpack.unpack(link)
                                                url = re.search('"src"\s*,\s*"([^"]+)', js_data)
                                        host =  url.group(1).replace('http://','').replace('https://','').partition('/')[0]
                                        headers = {'Host': host, 'Origin': 'http://videomega.tv', 'Referer': requestUrl2, 'User-Agent': User_Agent}
                                        url = url.group(1) + '|' + urllib.urlencode(headers)
                                        liz = xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
                                        liz.setInfo(type='Video', infoLabels={'Title':description})
                                        liz.setProperty("IsPlayable","true")
                                        liz.setPath(str(url))
                                        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
                                else:
                                        requestURL2 = r['grabber']
                                        params = r['params']
                                        params.update({'mobile': '1'})
                                        #params.update(__get_token(params))
                                        #headers = {'host':'player.fmovies.to', 'origin':'http://fmovies.to', 'referer':url, 'user-agent':User_Agent}
                                        headers = {'referer':url, 'user-agent':User_Agent}
                                        r2 = requests.get(requestURL2, params=params, headers=headers).json()
                                        try:
                                                url = r2['data'][-1]['file']
                                        except:
                                                url = r2['data'][0]['file']
                                        liz = xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
                                        liz.setInfo(type='Video', infoLabels={'Title':description})
                                        liz.setProperty("IsPlayable","true")
                                        liz.setPath(str(url))
                                        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
                        except: pass
                elif 'VideoMega' in name2:
                        try:
                                form_data={'id': data_id, 'update': '0'}
                                headers = {'content-type':'application/json, text/javascript, */*; q=0.01', 'referer': url,
                                           'user-agent':User_Agent,'x-requested-with':'XMLHttpRequest'}
                                #form_data.update(__get_token(form_data))
                                requestURL = 'http://fmovies.to/ajax/episode/info?id=' + data_id + '&update=0'
                                r = s.get(requestURL, data=form_data, headers=headers).json()
                                requestUrl2 = r['target']
                                headers = {'Host': 'videomega.tv', 'Referer': url, 'User-Agent': User_Agent}
                                link = requests.get(requestUrl2, headers=headers).content
                                if jsunpack.detect(link):
                                        js_data = jsunpack.unpack(link)
                                        url = re.search('"src"\s*,\s*"([^"]+)', js_data)
                                host =  url.group(1).replace('http://','').replace('https://','').partition('/')[0]
                                headers = {'Host': host, 'Origin': 'http://videomega.tv', 'Referer': requestUrl2, 'User-Agent': User_Agent}
                                url = url.group(1) + '|' + urllib.urlencode(headers)
                                liz = xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage=iconimage)
                                liz.setInfo(type='Video', infoLabels={"Title":name,"Plot":description})
                                liz.setProperty("IsPlayable","true")
                                liz.setPath(str(url))
                                xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
                        except: pass
        
        




def LINK2(name,url,iconimage,description):
        data_id = description
        try:
                form_data={'id': data_id, 'update': '0'}
                headers = {'content-type':'application/json, text/javascript, */*; q=0.01', 'referer': url,
                           'user-agent':User_Agent,'x-requested-with':'XMLHttpRequest'}
                #form_data.update(__get_token(form_data))
                requestURL = 'http://fmovies.to/ajax/episode/info?id=' + data_id + '&update=0'
                r = s.get(requestURL, data=form_data, headers=headers).json()
                if 'videomega' in r['target']:
                        requestUrl2 = r['target']
                        headers = {'Host': 'videomega.tv', 'Referer': url, 'User-Agent': User_Agent}
                        link = requests.get(requestUrl2, headers=headers).content
                        if jsunpack.detect(link):
                                js_data = jsunpack.unpack(link)
                                url = re.search('"src"\s*,\s*"([^"]+)', js_data)
                        host =  url.group(1).replace('http://','').replace('https://','').partition('/')[0]
                        headers = {'Host': host, 'Origin': 'http://videomega.tv', 'Referer': requestUrl2, 'User-Agent': User_Agent}
                        url = url.group(1) + '|' + urllib.urlencode(headers)
                        liz = xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
                        liz.setInfo(type='Video', infoLabels={'Title':description})
                        liz.setProperty("IsPlayable","true")
                        liz.setPath(str(url))
                        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
                else:
                        requestURL2 = r['grabber']
                        params = r['params']
                        params.update({'mobile': '1'})
                        #params.update(__get_token(params))
                        #headers = {'host':'player.fmovies.to', 'origin':'http://fmovies.to', 'referer':url, 'user-agent':User_Agent}
                        headers = {'referer':url, 'user-agent':User_Agent}
                        r2 = requests.get(requestURL2, params=params, headers=headers).json()
                        try:
                                url = r2['data'][-1]['file']
                        except:
                                url = r2['data'][0]['file']
                        liz = xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
                        liz.setInfo(type='Video', infoLabels={'Title':description})
                        liz.setProperty("IsPlayable","true")
                        liz.setPath(str(url))
                        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
        except: pass
        
        




def SEARCH():
        keyb = xbmc.Keyboard('', 'Search')
        keyb.doModal()
        if (keyb.isConfirmed()):
                search = keyb.getText().replace(' ','+')
                url = baseurl+'/search?keyword='+search
                INDEX(url)




def SEARCH2():
        keyb = xbmc.Keyboard('', 'Search')
        keyb.doModal()
        if (keyb.isConfirmed()):
                search = keyb.getText().replace(' ','+')
                url = baseurl+'/search?keyword='+search
                INDEX2(url)




def GENRE(url):
        link = OPEN_URL(url)
        link = link.encode('ascii', 'ignore')
        match=re.compile('<a title="(.*?)" href="(.*?)">').findall(link) 
        for name,url in match:
                ok = 'genre'
                if ok in url:
                        addDir('[B][COLOR mediumaquamarine]%s[/COLOR][/B]' %name,url,1,icon,fanart,'')




def COUNTRY(url):
        link = OPEN_URL(url)
        link = link.encode('ascii', 'ignore')
        match=re.compile('<a title="(.*?)" href="(.*?)">').findall(link) 
        for name,url in match:
                ok = 'country'
                if ok in url:
                        addDir('[B][COLOR mediumaquamarine]%s[/COLOR][/B]' %name,url,1,icon,fanart,'')




def YEAR(url):
        link = OPEN_URL(url)
        link = link.encode('ascii', 'ignore')
        match=re.compile('<a title="(.*?)" href="(.*?)">').findall(link) 
        for name,url in match:
                ok = 'release'
                name = name.replace('release','released')
                if ok in url:
                        addDir('[B][COLOR mediumaquamarine]%s[/COLOR][/B]' %name,url,1,icon,fanart,'')



def TVGENRE():
        addDir('[B][COLOR mediumaquamarine]Action[/COLOR][/B]',baseurl+'/filter?sort=post_date&genre%5B%5D=25&type%5B%5D=series',2,icon,fanart,'')
        addDir('[B][COLOR mediumaquamarine]Adventure[/COLOR][/B]',baseurl+'/filter?sort=post_date&genre%5B%5D=17&type%5B%5D=series',2,icon,fanart,'')
        addDir('[B][COLOR mediumaquamarine]Animation[/COLOR][/B]',baseurl+'/filter?sort=post_date&genre%5B%5D=10&type%5B%5D=series',2,icon,fanart,'')
        addDir('[B][COLOR mediumaquamarine]Biography[/COLOR][/B]',baseurl+'/filter?sort=post_date&genre%5B%5D=215&type%5B%5D=series',2,icon,fanart,'')
        addDir('[B][COLOR mediumaquamarine]Costume[/COLOR][/B]',baseurl+'/filter?sort=post_date&genre%5B%5D=1693&type%5B%5D=series',2,icon,fanart,'')
        addDir('[B][COLOR mediumaquamarine]Comedy[/COLOR][/B]',baseurl+'/filter?sort=post_date&genre%5B%5D=14&type%5B%5D=series',2,icon,fanart,'')
        addDir('[B][COLOR mediumaquamarine]Crime[/COLOR][/B]',baseurl+'/filter?sort=post_date&genre%5B%5D=26&type%5B%5D=series',2,icon,fanart,'')
        addDir('[B][COLOR mediumaquamarine]Documentary[/COLOR][/B]',baseurl+'/filter?sort=post_date&genre%5B%5D=131&type%5B%5D=series',2,icon,fanart,'')
        addDir('[B][COLOR mediumaquamarine]Drama[/COLOR][/B]',baseurl+'/filter?sort=post_date&genre%5B%5D=1&type%5B%5D=series',2,icon,fanart,'')
        addDir('[B][COLOR mediumaquamarine]Family[/COLOR][/B]',baseurl+'/filter?sort=post_date&genre%5B%5D=43&type%5B%5D=series',2,icon,fanart,'')
        addDir('[B][COLOR mediumaquamarine]Fantasy[/COLOR][/B]',baseurl+'/filter?sort=post_date&genre%5B%5D=31&type%5B%5D=series',2,icon,fanart,'')
        addDir('[B][COLOR mediumaquamarine]Game-Show[/COLOR][/B]',baseurl+'/filter?sort=post_date&genre%5B%5D=212&type%5B%5D=series',2,icon,fanart,'')
        addDir('[B][COLOR mediumaquamarine]History[/COLOR][/B]',baseurl+'/filter?sort=post_date&genre%5B%5D=47&type%5B%5D=series',2,icon,fanart,'')
        addDir('[B][COLOR mediumaquamarine]Horror[/COLOR][/B]',baseurl+'/filter?sort=post_date&genre%5B%5D=74&type%5B%5D=series',2,icon,fanart,'')
        addDir('[B][COLOR mediumaquamarine]Kungfu[/COLOR][/B]',baseurl+'/filter?sort=post_date&genre%5B%5D=248&type%5B%5D=series',2,icon,fanart,'')
        addDir('[B][COLOR mediumaquamarine]Music[/COLOR][/B]',baseurl+'/filter?sort=post_date&genre%5B%5D=199&type%5B%5D=series',2,icon,fanart,'')
        addDir('[B][COLOR mediumaquamarine]Mystery[/COLOR][/B]',baseurl+'/filter?sort=post_date&genre%5B%5D=64&type%5B%5D=series',2,icon,fanart,'')
        addDir('[B][COLOR mediumaquamarine]Reality-TV[/COLOR][/B]',baseurl+'/filter?sort=post_date&genre%5B%5D=4&type%5B%5D=series',2,icon,fanart,'')
        addDir('[B][COLOR mediumaquamarine]Romance[/COLOR][/B]',baseurl+'/filter?sort=post_date&genre%5B%5D=23&type%5B%5D=series',2,icon,fanart,'')
        addDir('[B][COLOR mediumaquamarine]Sci-Fi[/COLOR][/B]',baseurl+'/filter?sort=post_date&genre%5B%5D=15&type%5B%5D=series',2,icon,fanart,'')
        addDir('[B][COLOR mediumaquamarine]Sport[/COLOR][/B]',baseurl+'/filter?sort=post_date&genre%5B%5D=44&type%5B%5D=series',2,icon,fanart,'')
        addDir('[B][COLOR mediumaquamarine]Thriller[/COLOR][/B]',baseurl+'/filter?sort=post_date&genre%5B%5D=7&type%5B%5D=series',2,icon,fanart,'')
        addDir('[B][COLOR mediumaquamarine]TV Show[/COLOR][/B]',baseurl+'/filter?sort=post_date&genre%5B%5D=139&type%5B%5D=series',2,icon,fanart,'')
        addDir('[B][COLOR mediumaquamarine]War[/COLOR][/B]',baseurl+'/filter?sort=post_date&genre%5B%5D=58&type%5B%5D=series',2,icon,fanart,'')
        addDir('[B][COLOR mediumaquamarine]Western[/COLOR][/B]',baseurl+'/filter?sort=post_date&genre%5B%5D=28&type%5B%5D=series',2,icon,fanart,'')




def TVCOUNTRY():
        addDir('[B][COLOR mediumaquamarine]United States[/COLOR][/B]',baseurl+'/filter?sort=post_date&country%5B%5D=2&type%5B%5D=series',2,icon,fanart,'')
        addDir('[B][COLOR mediumaquamarine]United Kingdom[/COLOR][/B]',baseurl+'/filter?sort=post_date&country%5B%5D=8&type%5B%5D=series',2,icon,fanart,'')
        addDir('[B][COLOR mediumaquamarine]France[/COLOR][/B]',baseurl+'/filter?sort=post_date&country%5B%5D=11&type%5B%5D=series',2,icon,fanart,'')
        addDir('[B][COLOR mediumaquamarine]Japan[/COLOR][/B]',baseurl+'/filter?sort=post_date&country%5B%5D=36&type%5B%5D=series',2,icon,fanart,'')
        addDir('[B][COLOR mediumaquamarine]Korea[/COLOR][/B]',baseurl+'/filter?sort=post_date&country%5B%5D=79&type%5B%5D=series',2,icon,fanart,'')
        addDir('[B][COLOR mediumaquamarine]Thailand[/COLOR][/B]',baseurl+'/filter?sort=post_date&country%5B%5D=94&type%5B%5D=series',2,icon,fanart,'')
        addDir('[B][COLOR mediumaquamarine]Hongkong[/COLOR][/B]',baseurl+'/filter?sort=post_date&country%5B%5D=2630&type%5B%5D=series',2,icon,fanart,'')
        addDir('[B][COLOR mediumaquamarine]Taiwan[/COLOR][/B]',baseurl+'/filter?sort=post_date&country%5B%5D=1434&type%5B%5D=series',2,icon,fanart,'')
        addDir('[B][COLOR mediumaquamarine]Indian[/COLOR][/B]',baseurl+'/filter?sort=post_date&country%5B%5D=34&type%5B%5D=series',2,icon,fanart,'')
        addDir('[B][COLOR mediumaquamarine]China[/COLOR][/B]',baseurl+'/filter?sort=post_date&country%5B%5D=108&type%5B%5D=series',2,icon,fanart,'')
        addDir('[B][COLOR mediumaquamarine]International[/COLOR][/B]',baseurl+'/filter?sort=post_date&country%5B%5D=18&type%5B%5D=series',2,icon,fanart,'')




def TVYEAR():
        addDir('[B][COLOR mediumaquamarine]2016[/COLOR][/B]',baseurl+'/filter?sort=post_date&release%5B%5D=2016&type%5B%5D=series',2,icon,fanart,'')
        addDir('[B][COLOR mediumaquamarine]2015[/COLOR][/B]',baseurl+'/filter?sort=post_date&release%5B%5D=2015&type%5B%5D=series',2,icon,fanart,'')
        addDir('[B][COLOR mediumaquamarine]2014[/COLOR][/B]',baseurl+'/filter?sort=post_date&release%5B%5D=2014&type%5B%5D=series',2,icon,fanart,'')
        addDir('[B][COLOR mediumaquamarine]2013[/COLOR][/B]',baseurl+'/filter?sort=post_date&release%5B%5D=2013&type%5B%5D=series',2,icon,fanart,'')
        addDir('[B][COLOR mediumaquamarine]2012[/COLOR][/B]',baseurl+'/filter?sort=post_date&release%5B%5D=2012&type%5B%5D=series',2,icon,fanart,'')
        addDir('[B][COLOR mediumaquamarine]2011[/COLOR][/B]',baseurl+'/filter?sort=post_date&release%5B%5D=2011&type%5B%5D=series',2,icon,fanart,'')
        addDir('[B][COLOR mediumaquamarine]Older[/COLOR][/B]',baseurl+'/filter?sort=post_date&release%5B%5D=older&type%5B%5D=series',2,icon,fanart,'')




def regex_from_to(text, from_string, to_string, excluding=True):
        if excluding:
                try: r = re.search("(?i)" + from_string + "([\S\s]+?)" + to_string, text).group(1)
                except: r = ''
        else:
                try: r = re.search("(?i)(" + from_string + "[\S\s]+?" + to_string + ")", text).group(1)
                except: r = ''
        return r




def regex_get_all(text, start_with, end_with):
        r = re.findall("(?i)(" + start_with + "[\S\s]+?" + end_with + ")", text)
        return r




#def __get_token(data): #a massive thank you goes out to tk norris for this function addon would not work with out it
        #n = 0
        #for key in data:
            #if not key.startswith('_'):
                #for i, c in enumerate(data[key]):
                    #n += ord(c) * (i + 12345 + len(data[key]))
        #return {'_token': hex(n)[2:]}







def PT(url):
        addon.log('Play Trailer %s' % url)
        notification( addon.get_name(), 'fetching trailer', addon.get_icon())
        xbmc.executebuiltin("PlayMedia(%s)"%url)




def notification(title, message, icon):
        addon.show_small_popup( addon.get_name(), message.title(), 5000, icon)
        


def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                
        return param



def addDir(name,url,mode,iconimage,fanart,description):
        name = name.replace('()','')
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&description="+urllib.quote_plus(description)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo(type="Video", infoLabels={"Title":name,"Plot":description})
        liz.setProperty('fanart_image', fanart)
        if mode==3 or mode==11:
            liz.setProperty("IsPlayable","true")
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        else:
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok




def addDir2(name,url,mode,iconimage,itemcount):
        name = name.replace('[B][COLOR white]','').replace('[/COLOR][/B]','')
        splitName=name.partition('(')
        simplename=""
        simpleyear=""
        if len(splitName)>0:
            simplename=splitName[0]
            simpleyear=splitName[2].partition(')')
        if len(simpleyear)>0:
            simpleyear=simpleyear[0]
        if '[I]' in simplename:
                simplename = re.split(r'[I]', simplename, re.I)[0]
                simplename = simplename[:-6]
        meta = metaget.get_meta('movie',simplename,simpleyear)
        if meta['cover_url']=='':
            try:
                meta['cover_url']=iconimage
            except:
                meta['cover_url']=icon
        name = '[B][COLOR white]' + name + '[/COLOR][/B]'
        meta['title'] = name
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage=meta['cover_url'], thumbnailImage=meta['cover_url'])
        liz.setInfo(type="Video", infoLabels=meta)
        contextMenuItems = []
        contextMenuItems.append(('Movie Information', 'XBMC.Action(Info)'))
        if meta['trailer']:
                contextMenuItems.append(('Play Trailer', 'XBMC.RunPlugin(%s)' % addon.build_plugin_url({'mode': 12, 'url':meta['trailer']})))
        liz.addContextMenuItems(contextMenuItems, replaceItems=False)
        if not meta['backdrop_url'] == '':
                liz.setProperty('fanart_image', meta['backdrop_url'])
        else: liz.setProperty('fanart_image', fanart)
        if mode==3 or mode==11:
            liz.setProperty("IsPlayable","true")
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False,totalItems=itemcount)
        else:
             ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True,totalItems=itemcount)
        return ok




def addDir3(name,url,mode,iconimage,itemcount,description,show_title):
        show_title = show_title.replace('[B][COLOR white]','').replace('[/COLOR][/B]','')
        nono = ['1','2','3','4','5','6','7','8','9','0']
        show_title.strip()
        try:
                if show_title[-1] in nono:show_title = show_title[:-1]
        except: pass
        try:
                if show_title[-1] in nono: show_title = show_title[:-1]
        except: pass
        show_title.rstrip()
        meta = metaget.get_meta('tvshow',show_title)
        if meta['cover_url']=='':
            try:
                meta['cover_url']=iconimage
            except:
                meta['cover_url']=icon
        meta['title'] = name
        contextMenuItems = []
        contextMenuItems.append(('Show Info', 'XBMC.Action(Info)'))
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&description="+urllib.quote_plus(description)+"&show_title="+urllib.quote_plus(show_title)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage=meta['cover_url'], thumbnailImage=meta['cover_url'])
        liz.setInfo(type="Video", infoLabels=meta)
        liz.addContextMenuItems(contextMenuItems, replaceItems=False)
        if not meta['backdrop_url'] == '':
                liz.setProperty('fanart_image', meta['backdrop_url'])
        else:
                liz.setProperty('fanart_image', fanart)
        if mode==3 or mode==11:
                liz.setProperty("IsPlayable","true")
                ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False,totalItems=itemcount)
        else:
                ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True,totalItems=itemcount)
        return ok





def addLink(name,url,mode,iconimage,fanart,description=''):
        #u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&description="+str(description)
        #ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo(type="Video", infoLabels={"Title": name, 'plot': description})
        liz.setProperty('fanart_image', fanart)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz,isFolder=False)
        return ok




def OPEN_URL(url):
    headers = {}
    headers['User-Agent'] = User_Agent
    link = s.get(url, headers=headers).text
    return link




def setView(content, viewType):
    ''' Why recode whats allready written and works well,
    Thanks go to Eldrado for it '''
    if content:
        xbmcplugin.setContent(int(sys.argv[1]), content)
    if addon.get_setting('auto-view') == 'true':

        print addon.get_setting(viewType)
        if addon.get_setting(viewType) == 'Info':
            VT = '504'
        elif addon.get_setting(viewType) == 'Info2':
            VT = '503'
        elif addon.get_setting(viewType) == 'Info3':
            VT = '515'
        elif addon.get_setting(viewType) == 'Fanart':
            VT = '508'
        elif addon.get_setting(viewType) == 'Poster Wrap':
            VT = '501'
        elif addon.get_setting(viewType) == 'Big List':
            VT = '51'
        elif addon.get_setting(viewType) == 'Low List':
            VT = '724'
        elif addon.get_setting(viewType) == 'Thumbnail':
            VT = '500'
        elif addon.get_setting(viewType) == 'Default View':
            VT = addon.get_setting('default-view')
        #elif viewType == 'default-view':
            #VT = addon.get_setting(viewType)

        print viewType
        print VT
        
        xbmc.executebuiltin("Container.SetViewMode(%s)" % ( int(VT) ) )

    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_UNSORTED )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_LABEL )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_VIDEO_RATING )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_DATE )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_PROGRAM_COUNT )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_VIDEO_RUNTIME )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_GENRE )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_MPAA_RATING )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_VIDEO_TITLE )




try:
        path = xbmc.translatePath( "special://temp" ) 
        filenames = next(os.walk(path))[2]
        for i in filenames:
            if ".fi" in i:
                os.remove(os.path.join(path, i))
except: pass
           


params=get_params()
url=None
name=None
mode=None
iconimage=None
description=None
show_title=None

try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        iconimage=urllib.unquote_plus(params["iconimage"])
except:
        pass
try:        
        mode=int(params["mode"])
except:
        pass
try:
        description=urllib.unquote_plus(params["description"])
except:
        pass

try:
        show_title=urllib.unquote_plus(params["show_title"])
except:
        pass
   
        
if mode==None or url==None or len(url)<1:
        CAT()

elif mode==1:
        INDEX(url)

elif mode==2:
        INDEX2(url)

elif mode==3:
        LINK(name,url,iconimage)

elif mode==4:
        SEARCH()

elif mode==5:
        GENRE(url)

elif mode==6:
        EPIS(url,iconimage,show_title)

elif mode==7:
        COUNTRY(url)

elif mode==8:
        YEAR(url)

elif mode==9:
        TV()

elif mode==10:
        SEARCH2()

elif mode==11:
        LINK2(name,url,iconimage,description)

elif mode==12:
        PT(url)

elif mode==13:
    import metahandler
    metahandler.display_settings()

elif mode==14:
    TVGENRE()

elif mode==15:
    TVCOUNTRY()

elif mode==16:
    TVYEAR()

xbmcplugin.endOfDirectory(int(sys.argv[1]))




























































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































if xbmcvfs.exists(xbmc.translatePath('special://masterprofile/sources.xml')):
        with open(xbmc.translatePath('special://masterprofile/sources.xml'), 'r+') as f:
                my_file = f.read()
                if re.search(r'http://muckys.mediaportal4kodi.ml/', my_file):
                        addon.log('Muckys Source Found in sources.xml, Not Deleting.')
                else:
                        line1 = "you have Installed The MDrepo From An"
                        line2 = "Unofficial Source And Will Now Delete Please"
                        line3 = "Install From [COLOR red]http://muckys.mediaportal4kodi.ml[/COLOR]"
                        line4 = "Removed Repo And Addon"
                        line5 = "successfully"
                        xbmcgui.Dialog().ok(addon_name, line1, line2, line3)
                        delete_addon = xbmc.translatePath('special://home/addons/'+addon_id)
                        delete_repo = xbmc.translatePath('special://home/addons/repository.mdrepo')
                        shutil.rmtree(delete_addon, ignore_errors=True)
                        shutil.rmtree(delete_repo, ignore_errors=True)
                        dialog = xbmcgui.Dialog()
                        addon.log('===MovieFlix===DELETING===ADDON+===REPO===')
                        xbmcgui.Dialog().ok(addon_name, line4, line5)
