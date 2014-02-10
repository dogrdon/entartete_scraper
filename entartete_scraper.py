#!/usr/bin/env python

import scraperwiki
import lxml.html
import requests
import mechanize
import time
import re
import base64
from PIL import Image
import urllib, cStringIO #for opening url images

'''currently at https://scraperwiki.com/dataset/fzmt4qq because I don't want to have to deal with 
   all the issues of installing mechanize and lxml on my current local env'''

#headers = [('User-agent', 'Mozilla/5.0 (compatible; MSIE 9.0; AOL 9.7; AOLBuild 4343.19; Windows NT 6.1; WOW64; Trident/5.0; FunWebProducts)')]
headers = [('User-agent', 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:25.0) Gecko/20100101 Firefox/25.0')]
#headers = [('User-agent', 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36')]


home_url = 'http://emuseum.campus.fu-berlin.de/eMuseumPlus?service=ExternalInterface&lang=en'
base_url = 'http://emuseum.campus.fu-berlin.de'

restart_session='http://emuseum.campus.fu-berlin.de/eMuseumPlus;jsessionid=F14A1EBACD365A9C7C2593B189761791.node1?service=restart'


def get_artwork():
    test_list = [2, 311,312,313]
    
    data2 = []
    
    #for i in range(1,101):
    #for i in range(101, 201):
    #for i in range(201, 301):
    #for i in range(301, 401):
    #for i in range(401, 501):
    #for i in range(501, 601):
    #for i in range(601, 674):
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
        data.append({
            'id': opt.attrib['value'],
            'artist': opt.text_content()
        })
    time.sleep(10)
    return data


#======================== internal use =====================

def _scrape_it_look_for_next(dom_elem, selector, iterator, data_repo, br_obj, newer_link = 0):
    '''use this if after the original scrape it appears there is a next link'''


    for a in dom_elem.cssselect(selector): 
        
        to_details_url = base_url + a.attrib['href']
        
        br_obj.open(to_details_url)
        
        details_page = lxml.html.fromstring(br_obj.response().read())

        '''===============Gather all of the details for putting in the db================'''    
        for b in details_page.cssselect('div.listDescription ul li.ekTitel span.tspValue'):
            
            title = b.text_content()
            
        for c in details_page.cssselect('div.listDescription ul li.ekInventarNr span.tspValue'):
            
            ek_id = c.text_content()
            
        for d in details_page.cssselect('div.listDescription ul li.herkunftsort span.tspValue'):
            
            orig_museum = d.text_content()  
            
        for e in details_page.cssselect('div.listDescription ul li.gattung span.tspValue'):
            
            art_form = e.text_content() 
           
        #this one is a bit tricky because the markup is incorrect, there is a classless li elem after the labelled
        #li element where the object status should be. so currently getting the sibling li where the status is
        if details_page.cssselect('div.listDescription ul li.objektstatus + li span.tspValue'):
            for f in details_page.cssselect('div.listDescription ul li.objektstatus + li span.tspValue'):
                work_status = f.text_content()
                
        else:
            work_status = 'NA'
                
        if details_page.cssselect('div.listDescription ul li.standort span.tspValue'):
            for g in details_page.cssselect('div.listDescription ul li.standort span.tspValue'):
            
                location = g.text_content() 
        else:
            location = 'NA'
            
        if details_page.cssselect('div.listDescription ul li.verlustDurch span.tspValue'):
            for h in details_page.cssselect('div.listDescription ul li.verlustDurch span.tspValue'):
            
                loss_thru = h.text_content() 
        else:
            loss_thru = 'NA'
            
        
        if details_page.cssselect('div.listDescription ul li.datierung span.tspValue'):
            for j in details_page.cssselect('div.listDescription ul li.datierung span.tspValue'):
            
                artwork_date = j.text_content() 
        else:
            artwork_date = 'NA'
            
        if details_page.cssselect('div.listDescription ul li.material span.tspValue'):
            for k in details_page.cssselect('div.listDescription ul li.material span.tspValue'):
                material = k.text_content() 
        else:
            material = 'NA'
        
        #copyright    
        if details_page.cssselect('div.listDescription ul li.copyright span.tspValue'):
            for l in details_page.cssselect('div.listDescription ul li.copyright span.tspValue'):
                copyright = l.text_content() 
        else:
            copyright = 'NA'
            
        #herkunftsinventar - inv of origin
        if details_page.cssselect('div.listDescription ul li.herkunftsinventar span.tspValue'):
            for m in details_page.cssselect('div.listDescription ul li.herkunftsinventar span.tspValue'):
                inv_origin = m.text_content() 
        else:
            inv_origin = 'NA'
        
        #verlustDatum - date lost
        if details_page.cssselect('div.listDescription ul li.verlustDatum span.tspValue'):
            for n in details_page.cssselect('div.listDescription ul li.verlustDatum span.tspValue'):
                date_lost = n.text_content() 
        else:
            date_lost = 'NA'
        
        #werkverzeichnis
        if details_page.cssselect('div.listDescription ul li.werkverzeichnis span.tspValue'):
            for o in details_page.cssselect('div.listDescription ul li.werkverzeichnis span.tspValue'):
                catalog_id = o.text_content() 
        else:
            catalog_id = 'NA'
        
        #konvolut
        if details_page.cssselect('div.listDescription ul li.konvolut span.tspValue'):
            for p in details_page.cssselect('div.listDescription ul li.konvolut span.tspValue'):
                envelope = p.text_content() 
        else:
            envelope = 'NA'
        
        #konvolutTeile
        if details_page.cssselect('div.listDescription ul li.konvolutTeile span.tspValue'):
            for q in details_page.cssselect('div.listDescription ul li.konvolutTeile span.tspValue'):
                env_part = q.text_content() 
        else:
            env_part = 'NA'
            
        
        #======================= END OF GRID ITEMS =============================================      
        
        #IMAGE encoded base64
        #if details_page.cssselect('div.listImg a img'):
        #    for img in details_page.cssselect('div.listImg a img'):
        #        img_url = img.attrib['src']
        #        img_url = base_url+img_url
                
        #        tmp_file = cStringIO.StringIO(urllib.urlopen(img_url).read())
        #        tmp_img_file = Image.open(tmp_file)
                
        #        with open(tmp_img_file, "rb") as image_file:
        #            artwork_image = base64.b64encode(image_file.read())
        #else:
        #    artwork_image = 'NA'
        
        #Bookmark ID
        for bmref in details_page.cssselect('a.bookmarkLink'):
            
            sessionless_uri = bmref.attrib['href']

            db_obj_id = re.search('&objectId=(.+?)&viewType=', sessionless_uri).group(1)
            
        #get image from sessionless url
        br_obj.open(sessionless_uri)
        img_doc = lxml.html.fromstring(br_obj.response().read())

        if img_doc.cssselect('div.listImg a img'):
            for img_a in img_doc.cssselect('div.listImg a img'):
                thmb_url = img_a.attrib['src']
                thmb_url = base_url + thmb_url
                
                #print "thumb url = ", thmb_url
            
            #for img_b in img_doc.cssselect('div.listImg a'):
            #    img_url = img_b.attrib['href']
            #    print 'image url = ', re.search('\(\'(.+?)\'', img_url).group(1)

        else:
            thmb_url = 'NA'
                

        print iterator, title, ek_id, orig_museum, art_form, work_status, location, loss_thru #test print
        
        data_repo.append({
            "artist_id": iterator, 
            "artwork_title": title,
            "ek_inven_id": ek_id,
            "museum_orig": orig_museum, 
            "art_form": art_form, 
            "uri": sessionless_uri,
            "db_id": db_obj_id,
            "work_status": work_status,
            "location": location,
            "loss_thru": loss_thru,
            "date": artwork_date, 
            "material": material, 
            "copyright": copyright,
            "inv_orig": inv_origin,
            "date_lost": date_lost,
            "catalog_id": catalog_id,
            "envelope": envelope,
            "env_part": env_part,
            "thumb_url": thmb_url
        })

    for zef in dom_elem.cssselect('li#pageSetEntries-nextSet'): 
        if zef.cssselect('a'):
            newer_link = 1
            
        else:
            newer_link = 0 
        
        if newer_link is 1:

            for ref in zef.cssselect('a'):
                __next = ref.attrib['href']
        
                _next_url = base_url+__next
                print 'Now I am going to scrape:  ', _next_url


                br_obj.open(_next_url)
                _sub_doc = lxml.html.fromstring(br_obj.response().read())
                _scrape_it_look_for_next(_sub_doc, selector, iterator, data_repo, br_obj)
        else:
            break
                    
def _check_if_val(string):
    if string is not '' or string is not None:
        return string
    else:
        string = 'NA'
        return string

scraperwiki.sql.save(unique_keys=["id"], data=get_artists(), table_name="degenerate_artists")
scraperwiki.sql.save(unique_keys=["ek_inven_id"], data=get_artwork(), table_name="degenerate_artists_work")