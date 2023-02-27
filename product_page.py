
def images_links_extractor(soup):
    Item_img = soup.find('div', attrs={'class': 'image-gallery-slides'})
    elements = Item_img.findAll('img',attrs={'role': 'presentation'})
    images_links = [e.get('src') for e in elements if '.jpeg' in e.get('src')]
    return images_links

def Ad_Id(soup):
    Ind_item=soup.findAll('div', attrs={'class':'_1075545d c6bdd888 _5f872d11'})
    for single_item in Ind_item:
        single_item_des = single_item.find('div' , attrs={'class':'_171225da'})
    return single_item_des.text

def title(soup):
    Ind_item=soup.findAll('div', attrs={'aria-label':'Overview'})
    for single_item in Ind_item:
        single_item_details = single_item.find('h1')
        
        return single_item_details.text
        
def seller(soup):

    Ind_item=soup.findAll('div', attrs={'aria-label':'Seller description'})

    for single_item in Ind_item:
        single_item_link = single_item.find('a')

    return 'https://www.olx.com.pk'+single_item_link.get('href')

def location(soup):
    Ind_item=soup.findAll('div', attrs={'aria-label':'Overview'})
    for single_item in Ind_item:
        single_item_loc = single_item.find('span' , attrs={'aria-label':'Location'})
        return single_item_loc.text
    
def price(soup):
    Ind_item=soup.findAll('div', attrs={'aria-label':'Overview'})
    for single_item in Ind_item:
        single_item_details = single_item.find('span')
        return single_item_details.text
        
def Description_Area_Parser(soup):
    """
    Code for scraping description portion of single olx advertisements.
    input  : soup object of complete page. 
    return : dict of dict.
    """
    Scraped_results={}
    Item_description_tab=soup.find('div', attrs={'aria-label':'Details and description'})

    Description_div = Item_description_tab.findChildren('div', recursive=False)
    for sub_description_div in Description_div:
        category_name = sub_description_div.find('span', recursive=False).text
      
        description_Group_details = sub_description_div.find('div', recursive=False)
        Sub_features = {}
        sub_elementdescription = description_Group_details.findChildren('div', recursive=False)

        # for managing description portion
        if len(sub_elementdescription)==0:
            sub_elementdescription = [description_Group_details]
      
        for sub_element in range(len(sub_elementdescription)):
            sub_element_chld = sub_elementdescription[sub_element].findAll('span')
        
            # For managing key value pair type features
            if len(sub_element_chld)==2:
                Sub_features[sub_element_chld[0].text]=sub_element_chld[1].text
            else:
                Sub_features[category_name] = [sub_element_chld[n_i].text for n_i in range(len(sub_element_chld))]
      
        Scraped_results[category_name]=Sub_features
        
    extracted = {}
    for key in Scraped_results.keys():
        extracted.update(Scraped_results[key])

    return extracted

def category_path(soup):
    return soup.find('div', attrs={'aria-label': 'Breadcrumb'}).text

def olx_add_information_extractor(soup):
    Scraped_advertisement = Description_Area_Parser(soup)
    Scraped_advertisement['Title'] = title(soup)
    Scraped_advertisement['Price'] = price(soup)
    Scraped_advertisement['Location'] = location(soup)
    Scraped_advertisement['Ad_ID'] = Ad_Id(soup)
    Scraped_advertisement['Ad_category'] = category_path(soup)
    Scraped_advertisement['Prof_links'] = seller(soup)
    Scraped_advertisement['Img_Links'] =images_links_extractor(soup)
    return Scraped_advertisement
