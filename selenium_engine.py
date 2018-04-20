import json
import re
import requests
import time
from selenium import webdriver


# ======================================================= #


headers = {'Host': 'www.instagram.com',
           'User-Agent': '''Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:56.0)
           Gecko/20100101 Firefox/56.0''',
           'Accept': '*/*',
           'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
           'Accept-Encoding': 'gzip, deflate, br',
           'X-Requested-With': 'XMLHttpRequest',
           'Connection': 'keep-alive'}


# ======================================================= #


def selenium_driver():
    driver = webdriver.Chrome()
    driver.get('https://instagram.com/accounts/login')
    time.sleep(3)
    credentials = driver.find_elements_by_tag_name('input')
    credentials[0].send_keys('')
    credentials[1].send_keys('')
    login_btn = driver.find_element_by_tag_name('button')
    login_btn.click()
    time.sleep(2)
    return driver
    

# ======================================================= #


def get_username_by_shortcode(driver, shortcode):
    address = 'https://instagram.com/p/' + shortcode
    driver.get(address)
    time.sleep(2)
    username = driver.find_element_by_class_name('_iadoq').get_attribute("href").split("/")[3]
    return username


# ======================================================= #


def get_info_by_username(driver, username):
    address = 'https://instagram.com/' + username
    driver.get(address)
    time.sleep(2)
    engagement = driver.find_elements_by_class_name('_fd86t ')
    post_count = engagement[0].text
    followers = engagement[1].get_attribute('title')
    follows = engagement[2].text
    is_private = False
    is_verified = False
    link = False
    external_url = ''
    email = ''
    bio = ''
    full_name = ''
    phone = ''
    try:
        full_name = driver.find_element_by_class_name('_kc4z2').text
    except Exception:
        pass    
    try:
        bio = driver.find_element_by_class_name('_tb97a').find_elements_by_tag_name('span')[0].text
    except Exception:
        pass
    email = re.search(r'[\w\.-]+@[\w\.-]+', bio)
    if email is None:
        email = ''
    elif email is not None:
        email = email.group(0)    
    phone = re.search(r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})', bio)
    if phone is None:
        phone = ''
    elif phone is not None:
        phone = phone.group(0)    
    try:
        is_private = driver.find_element_by_class_name('_kcrwx')
    except Exception:
        pass
    try:        
        is_verified = driver.find_element_by_class_name('coreSpriteVerifiedBadge ')
    except Exception:
        pass
    try:
        link = bio.find_element_by_class_name('_ng0lj')
    except Exception:
        pass
    if is_private:
        is_private = True
    else:
        pass
    if is_verified:
        is_verified = True
    else:
        pass
    if link:
         external_url = link.text
    else:
        pass
    return username, address, full_name, email, phone, bio, external_url, followers, follows, post_count, is_verified, is_private


# ======================================================= #


def get_top_posts(driver, hashtag):
    topPosts = []
    address = 'https://www.instagram.com/explore/tags/' + hashtag
    driver.get(address)
    for element in driver.find_elements_by_class_name('_tn0ps')[:9]:
            try:
                link = element.find_element_by_tag_name('a')
                shortcode = link.get_attribute("href").split('/')[4]
                if shortcode not in topPosts:
                    print 'Shortcode: ', shortcode
                    topPosts.append(shortcode)
            except Exception as e:
                #print e
                pass
    return topPosts


# ======================================================= #


def get_recent_posts(driver, hashtag, amount):
    recentPosts = []
    elements = []
    address = 'https://www.instagram.com/explore/tags/' + hashtag
    driver.get(address)
    while len(recentPosts) < (amount + 9):
        time.sleep(3)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        for element in driver.find_elements_by_class_name('_tn0ps'):
            try:
                shortcode = element.find_element_by_tag_name('a').get_attribute("href").split('/')[4]
                if shortcode not in recentPosts:
                    print 'Shortcode: ', shortcode
                    recentPosts.append(shortcode)
            except Exception as e:
                #print e
                pass
    return recentPosts[9:(amount + 10)]


# ======================================================= #


def get_top_posts_owners(hashtag):
    allUsers = []    
    driver = selenium_driver()
    topPosts = get_top_posts(driver, hashtag)
    for shortcode in topPosts:
        try:
            username = get_username_by_shortcode(driver, shortcode)
            print 'Username: ', username
            username, url, full_name, email, phone, bio, external_url, followers, follows, post_count, is_verified, is_private = get_info_by_username(driver, username)
            post_url = 'https://instagram.com/p/' + shortcode
            allUsers.append({'username': username,
                             'url': url,
                             'full_name': full_name,
                             'email': email,
                             'phone': phone,
                             'bio': bio,
                             'external_url': external_url,
                             'followers': followers,
                             'follows': follows,
                             'post_count': post_count,
                             'is_verified': is_verified,
                             'is_private': is_private,
                             'post_url': post_url})
        except Exception as e:
            pass
    driver.quit()
    return allUsers


# ======================================================= #


def get_recent_posts_owners(hashtag, amount):
    allUsers = []
    driver = selenium_driver()
    recentPosts = get_recent_posts(driver, hashtag, amount)    
    for shortcode in recentPosts:
        try:
            username = get_username_by_shortcode(driver, shortcode)
            print 'Username: ', username
            username, url, full_name, email, phone, bio, external_url, followers, follows, post_count, is_verified, is_private = get_info_by_username(driver, username)
            post_url = 'https://instagram.com/p/' + shortcode
            allUsers.append({'username': username,
                             'url': url,
                             'full_name': full_name,
                             'email': email,
                             'phone': phone,
                             'bio': bio,
                             'external_url': external_url,
                             'followers': followers,
                             'follows': follows,
                             'post_count': post_count,
                             'is_verified': is_verified,
                             'is_private': is_private,
                             'post_url': post_url})
        except Exception as e:
            #print e
            pass
    driver.quit()
    return allUsers


# ======================================================= #


def get_top_posts_commenters(hashtag, amount):
    driver = selenium_driver()    
    topPosts = get_top_posts(driver, hashtag)
    allUsers = []
    usernames = []
    commenters = []
    for shortcode in topPosts:
        if len(allUsers) >= (amount - 1):
            break
        else:
            address = 'https://www.instagram.com/p/' + shortcode
            driver.get(address)    
            try:
                btn = driver.find_element_by_class_name('_1s3cd')
                while True:
                    time.sleep(3)
                    btn.click()
            except Exception as e:
                pass
            post_owner = driver.find_element_by_class_name('_iadoq').get_attribute("href").split("/")[3]
            elements = driver.find_elements_by_class_name('_ezgzd')
            for element in elements:
                username = element.find_element_by_class_name('_95hvo').get_attribute("href").split('/')[3]
                if username not in usernames and username != post_owner:
                    usernames.append(username)
                    comment = element.find_element_by_tag_name('span').text.encode("utf-8")
                    commenters.append({'username': username,
                                       'comment': comment})
                    #print comment.text.encode("utf-8")
            for commenter in commenters:
                if len(allUsers) >= (amount - 1):
                    break
                else:
                    username = commenter['username']
                    comment = commenter['comment']
                    print 'Username: ', username
                    url = 'https://instagram.com/' + username
                    username, url, full_name, email, phone, bio, external_url, followers, follows, post_count, is_verified, is_private = get_info_by_username(driver, username)
                    allUsers.append({'username': username,
                                     'url': url,
                                     'full_name': full_name,
                                     'email': email,
                                     'phone': phone,
                                     'bio': bio,
                                     'external_url': external_url,
                                     'followers': followers,
                                     'follows': follows,
                                     'post_count': post_count,
                                     'is_verified': is_verified,
                                     'is_private': is_private,
                                     'post_url': address,
                                     'text': comment})
            commenters = []
    driver.quit()
    #print len(allUsers[:amount])
    return allUsers


# ======================================================= #


def get_recent_posts_commenters(hashtag, amount):
    comments_count = 0
    recentPosts = []
    allUsers = []
    usernames = []
    commenters = []
    address = 'https://www.instagram.com/explore/tags/' + hashtag
    driver = selenium_driver()
    driver.get(address)
    topPosts = driver.find_elements_by_class_name('_tn0ps')[:9]
    while comments_count < amount:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        for element in driver.find_elements_by_class_name('_tn0ps'):
            if element in topPosts:
                pass
            elif element not in topPosts:
                try:
                    shortcode = element.find_element_by_tag_name('a').get_attribute("href").split('/')[4]
                    if shortcode not in recentPosts:
                        recentPosts.append(shortcode)
                        print 'Shortcode: ', shortcode
                        address = 'https://www.instagram.com/p/%s/?__a=1' % shortcode
                        req = requests.get(address, headers)
                        data = json.loads(req.text)
                        if data['graphql']['shortcode_media']['edge_media_to_comment']['count'] != 0:
                            comments_count += data['graphql']['shortcode_media']['edge_media_to_comment']['count']                            
                except Exception as e:
                    #print e
                    pass
    for shortcode in recentPosts:
        if len(allUsers) >= (amount - 1):
            break
        else:
            address = 'https://www.instagram.com/p/' + shortcode
            driver.get(address)    
            try:
                btn = driver.find_element_by_class_name('_1s3cd')
                while True:
                    time.sleep(3)
                    btn.click()
            except Exception as e:
                pass
            post_owner = driver.find_element_by_class_name('_iadoq').get_attribute("href").split("/")[3]
            elements = driver.find_elements_by_class_name('_ezgzd')
            for element in elements:
                username = element.find_element_by_class_name('_95hvo').get_attribute("href").split('/')[3]
                if username not in usernames and username != post_owner:
                    usernames.append(username)
                    comment = element.find_element_by_tag_name('span').text.encode("utf-8")
                    commenters.append({'username': username,
                                       'comment': comment})
                    #print comment.text.encode("utf-8")
            for commenter in commenters:
                if len(allUsers) >= (amount - 1):
                    break
                else:
                    username = commenter['username']
                    comment = commenter['comment']
                    print 'Username: ', username
                    usernames.append(username)
                    url = 'https://instagram.com/' + username
                    username, url, full_name, email, phone, bio, external_url, followers, follows, post_count, is_verified, is_private = get_info_by_username(driver, username)
                    allUsers.append({'username': username,
                                     'url': url,
                                     'full_name': full_name,
                                     'email': email,
                                     'phone': phone,
                                     'bio': bio,
                                     'external_url': external_url,
                                     'followers': followers,
                                     'follows': follows,
                                     'post_count': post_count,
                                     'is_verified': is_verified,
                                     'is_private': is_private,
                                     'post_url': address,
                                     'text': comment})
        commenters = []  
    driver.quit()
    #print len(allUsers)
    return allUsers


# ======================================================= #


