# coding=utf-8
import requests
from bs4 import BeautifulSoup
import json


class spider(object):
    def prime_time(self):
        '''
        黄金档
        :return: 
        '''
        soup = self.get_soup()
        i = 0
        prime_time_dict = dict()
        prime_time_list = list()
        imgs = soup.select('div#m_86821 div.yk-row div.yk-col4 div.v-thumb img')  # 图片
        Title_Hrefs = soup.select('div#m_86821 div.yk-row div.yk-col4 div.v-link a')  # 播放视频链接+剧名
        infos = soup.select('div#m_86821 div.yk-row div.yk-col4 div.v-meta.va div.v-meta-entry a')  # 简介
        for img in imgs:
            prime_time_dict['img'] = imgs[i]['_src']  # 图片
            prime_time_dict['title'] = Title_Hrefs[i]['title']  # 剧名
            html = requests.get(Title_Hrefs[i]['href'])
            html.encoding = 'utf-8'  # 中文编码
            soup1 = BeautifulSoup(html.text, 'html.parser')  # 解析网页
            links = soup1.select('div.p1 div:nth-of-type(4) input')
            prime_time_dict['link'] = links[0]['value']  # 播放链接
            prime_time_dict['info'] = infos[i].get_text()  # 简介
            prime_time_list.append(prime_time_dict.copy())
            i = i + 1
        return prime_time_list

    def online_teleplay(self):
        '''
        超级网剧
        :return: 
        '''
        soup = soup = self.get_soup()
        i = 0
        online_teleplay_dict = dict()
        online_teleplay_list = list()
        imgs = soup.select(
            'div#m_86869 div.yk-row.yk-tv-index-7 div.yk-w970-col12.yk-w1190-col16 div.v-thumb img')  # 图片
        infos1 = soup.select(
            'div#m_86869 div.yk-row.yk-tv-index-7 div.yk-w970-col12.yk-w1190-col16 div.v-meta.vb div.v-meta-entry span')
        infos2 = soup.select(
            'div#m_86869 div.yk-row.yk-tv-index-7 div.yk-w970-col12.yk-w1190-col16 div.v-meta.vb div.v-meta-entry span.v-num')  # 简介
        for infos in infos2:  # infos1-infos2
            v = infos
            infos1.remove(v)
        Title_Href = soup.select(
            'div#m_86869 div.yk-row.yk-tv-index-7 div.yk-w970-col12.yk-w1190-col16 div.v-link a')  # 播放视频链接+剧名
        for title in Title_Href:
            online_teleplay_dict['img'] = imgs[i]['_src']  # 图片
            online_teleplay_dict['title'] = Title_Href[i]['title']  # 剧名
            html = requests.get(Title_Href[i]['href'])
            html.encoding = 'utf-8'  # 中文编码
            soup1 = BeautifulSoup(html.text, 'html.parser')  # 解析网页
            links = soup1.select('div.p1 div:nth-of-type(4) input')
            online_teleplay_dict['link'] = links[0]['value']  # 播放链接
            online_teleplay_dict['info'] = infos1[i].get_text()  # 简介
            online_teleplay_list.append(online_teleplay_dict.copy())
            i = i + 1
        return online_teleplay_list

    def exclusive_planning(self):
        '''独家策划'''
        soup = self.get_soup()
        i = 0
        exclusive_planning_dict = dict()
        exclusive_planning_list = list()
        imgs = soup.select('div#m_86905 div.yk-w970-col12.yk-w1190-col16 div.v-thumb img')  # 图片
        Title_Hrefs = soup.select('div#m_86905 div.yk-w970-col12.yk-w1190-col16 div.v-link a')  # 播放视频链接+剧名
        infos = soup.select('div#m_86905 div.yk-w970-col12.yk-w1190-col16 div.v-meta-entry span')  # 简介
        for img in imgs:
            exclusive_planning_dict['img'] = imgs[i]['_src']  # 图片
            exclusive_planning_dict['title'] = Title_Hrefs[i]['title']  # 剧名
            html = requests.get(Title_Hrefs[i]['href'])
            html.encoding = 'utf-8'  # 中文编码
            soup1 = BeautifulSoup(html.text, 'html.parser')  # 解析网页
            links = soup1.select('div.p1 div:nth-of-type(4) input')
            exclusive_planning_dict['link'] = links[0]['value']  # 播放链接
            exclusive_planning_dict['info'] = infos[i].get_text()  # 简介
            exclusive_planning_list.append(exclusive_planning_dict.copy())
            i = i + 1
        return exclusive_planning_list

    def get_soup(self, url=u'http://tv.youku.com/'):
        html = requests.get(url)  # 获取网页
        html.encoding = 'utf-8'  # 中文编码
        soup = BeautifulSoup(html.text, 'html.parser')  # 解析网页
        return soup

    def search(self, key_word):
        '''

        :param key_word: 搜索的关键字
        :return: 
        '''
        base_url = u'http://www.soku.com/search_video/q_'
        search_url = base_url + key_word
        soup = self.get_soup(url=search_url)
        posters = soup.select('div.s_poster')  # img,info,href
        informs = soup.select('div.s_inform')  # 剧集信息
        result = []
        for i in range(len(posters)):
            dramas = {}
            dramas['img'] = posters[i].select('div.s_target')[0].img['src']
            dramas['info'] = posters[i].select('div.s_link')[0].a['_log_title']
            dramas['href'] = posters[i].select('div.s_link')[0].a['href']
            dramas['Synopsis'] = informs[i].select('div.s_info p.c_dark span')[0]['data-text']
            links = []
            for link in informs[i].select('div.s_items.all.site14')[0].select('li'):
                if not str(link.a['href']).startswith('java'):
                    links.append(link.a['href'])
            dramas['links'] = links
            result.append(dramas.copy())
            return result

            # for inform in informs:
            #     Synopsis = inform.select('p.c_dark span')[0]['data-text']
            #     leading_role = inform.select('span.s_figure')
            #     print Synopsis
            #     print leading_role

    def get_data(self):
        data = {}
        data[u'黄金档'] = self.prime_time()
        data[u'超级网剧'] = self.online_teleplay()
        data[u'独家策划'] = self.exclusive_planning()
        return data


if __name__ == '__main__':
    a = spider()
    # a.prime_time()
    # a.online_teleplay()
    # a.exclusive_planning()
    # key = raw_input()
    # a.search(key.decode('utf-8'))
    # print json.dumps( a.search(u'人民的名义'), ensure_ascii=False)
    print json.dumps(a.get_data(), ensure_ascii=False)