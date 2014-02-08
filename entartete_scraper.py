import scraperwiki
import lxml.html
import requests
import mechanize
import time

'''currently at https://classic.scraperwiki.com/scrapers/entartete_kunst_datenbank/edit/# because I don't want to have to deal with 
   all the issues of installing mechanize and lxml on my current local env'''

headers = [('User-agent', 'Mozilla/5.0 (compatible; MSIE 9.0; AOL 9.7; AOLBuild 4343.19; Windows NT 6.1; WOW64; Trident/5.0; FunWebProducts)')]

home_url = 'http://emuseum.campus.fu-berlin.de/eMuseumPlus?service=ExternalInterface&lang=en'
base_url = 'http://emuseum.campus.fu-berlin.de'

restart_session='http://emuseum.campus.fu-berlin.de/eMuseumPlus;jsessionid=F14A1EBACD365A9C7C2593B189761791.node1?service=restart'


def get_artwork():
    test_list = [2, 311,312,313]
    data2 = []
    #for i in range(1,627):
    for i in test_list:
        br = mechanize.Browser()
        br.addheaders = headers
        br.open(home_url)
        
        br.select_form(nr=1) #there is a hidden form, we want the visible form at index 1

        br.form["$PropertySelection"] = [str(i)] 

        req = br.submit()

        html = req.read()

        doc = lxml.html.fromstring(html)

        main_selector = 'div#collectionDetailList ul li.titel a'
        
        _scrape_it_look_for_next(doc, main_selector, i, data2, br) #scrape first page after coming from db search
        
    return data2


def get_artists():
    dom = lxml.html.fromstring(requests.get(home_url).content)

    data = []

    for opt in dom.xpath('.//select[@id="field_21"]/option'):
        #print opt.attrib['value'], opt.text_content() #get all possible artists and their db values from db dropdown
        data.append({
            'id': opt.attrib['value'],
            'artist': opt.text_content()
        })
    time.sleep(10)
    return data



#======================== internal use =====================

def _scrape_it_look_for_next(dom_elem, selector, iter, data_repo, br_obj, newer_link = 0):
    '''use this if after the original scrape it appears there is a next link'''


    for a in dom_elem.cssselect(selector): 
        #title = a.text_context() 

        print iter, a.attrib['href']

        data_repo.append({
            "artist_id": iter, 
            #"artwork": title,
            "artwork_url": a.attrib['href']
        })

    for ze in dom_elem.cssselect('li#pageSetEntries-nextSet'): 
        if ze.cssselect('a'):
            newer_link = 1
            
        else:
            newer_link = 0 
        
        if newer_link is 1:
            #print 'link eq TRUE'
            
            for re in ze.cssselect('a'):
                __next = re.attrib['href']
        
                _next_url = base_url+__next
                print 'Now I am going to scrape:  ', _next_url

                #print 'Newer link = ', newer_link
                #next_dom = lxml.html.fromstring(requests.get(next_url).content)


                br_obj.open(_next_url)
                _sub_doc =  lxml.html.fromstring(br_obj.response().read())
                _scrape_it_look_for_next(_sub_doc, selector, iter, data_repo, br_obj)
                '''need to check again if link exists, its not checking'''
        else:
            break
                    


scraperwiki.sqlite.save(unique_keys=["id"], data=get_artists(), table_name="degenerate_artists")
scraperwiki.sqlite.save(unique_keys=["artwork_url"], data=get_artwork(), table_name="degenerate_artists_work")



