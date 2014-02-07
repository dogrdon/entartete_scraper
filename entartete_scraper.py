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
    test_list = [1, 2, 3, 311,312,313]
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
        
        _scrape_it(doc, main_selector, i, data2) #scrape first page after coming from db search
        

        for z in doc.cssselect('li#pageSetEntries-nextSet'): 
            if z.cssselect('a'):
                print 'link eq TRUE'
                for r in z.cssselect('a'):
                    _next = r.attrib['href']
                
                    next_url = base_url+_next
                    print next_url
                    #next_dom = lxml.html.fromstring(requests.get(next_url).content)

                    
                    br.open(next_url)
                    sub_doc =  lxml.html.fromstring(br.response().read())
                    _scrape_it(sub_doc, main_selector, i, data2)  #ok, it gets to next page, need to keep checking for link before moving on.
            else:
                print 'link eq FALSE'
            '''
            if zerd == 1: #check if there are multiple pages
                for n in doc.cssselect('li#pageSetEntries-nextSet a'):
                    _next = n.attrib['href']
                
                    next_url = base_url+_next
                
                    next_dom = lxml.html.fromstring(requests.get(next_url).content)
                   
                    if next_dom is not None:        
                        print 'fetching nextpage...' 

                        _scrape_it(next_dom, main_selector, i, data2)

                        for z in next_dom.cssselect('li#pageSetEntries-nextSet'):
                            if z.cssselect('a'):
                                zerd = 1
                            else:
                                zerd = 0
                    else:
                        print ' you fucker there is nothing here '
                 '''   

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
def _scrape_it(dom_elem, selector, iter, data_repo):
    '''This is the scraper, that we need to keep calling
      pass in:
        the active dom element from lxml or requests,
        the selector you wish to use for lxml.cssselect,
        the iterator, or running record, in this case -i- in the main for loop,
        and the list where this is all being stored'''
    for a in dom_elem.cssselect(selector): 
            #title = a.text_context() 

            print iter, a.attrib['href']
            data_repo.append({
                "artist_id": iter, 
                #"artwork": title,
                "artwork_url": a.attrib['href']
            })


scraperwiki.sqlite.save(unique_keys=["id"], data=get_artists(), table_name="degenerate_artists")
scraperwiki.sqlite.save(unique_keys=["artwork_url"], data=get_artwork(), table_name="degenerate_artists_work")



