#importing libraries
import requests, urllib

#This is for analyzing the sentiments of the comments.
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer

# This is to print the input/output in color
from termcolor import colored

#This is the token for accessing the instagram API.
APP_ACCESS_TOKEN = '5688075466.5f069c7.4c2feb78d6954dcb9f70c12def066748'
#Token owner = instabotmriutest0

#Sandbox users = insta.bot.test.0

#This is the base url of instagram.
BASE_URL = 'http://api.instagram.com/v1/'


# 1. Function declaration to get your own info

def self_info():
    request_url = (BASE_URL + 'users/self/?access_token=%s') % (APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            print 'Username: %s' % (user_info['data']['username'])
            print 'No. of followers: %s' % (user_info['data']['counts']['followed_by'])
            print 'No. of people you are following: %s' % (user_info['data']['counts']['follows'])
            print 'No. of posts: %s' % (user_info['data']['counts']['media'])
        else:
            print 'User does not exist!'
    else:
        print 'Status code other than 200 received!'


# Function declaration to get the ID of a user by username

def get_user_id(insta_username):
    request_url = (BASE_URL + 'users/search?q=%s&access_token=%s') % (insta_username, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            return user_info['data'][0]['id']
        else:
            return None
    else:
        print 'Status code other than 200 received!'
        exit()


# 2. Function declaration to get the info of a user by username

def get_user_info(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = (BASE_URL + 'users/%s?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            print 'Username: %s' % (user_info['data']['username'])
            print 'No. of followers: %s' % (user_info['data']['counts']['followed_by'])
            print 'No. of people you are following: %s' % (user_info['data']['counts']['follows'])
            print 'No. of posts: %s' % (user_info['data']['counts']['media'])
        else:
            print 'There is no data for this user!'
    else:
        print 'Status code other than 200 received!'


# 3. Function declaration to get your recent post

def get_own_post():
    request_url = (BASE_URL + 'users/self/media/recent/?access_token=%s') % (APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    own_media = requests.get(request_url).json()

    if own_media['meta']['code'] == 200:
        if len(own_media['data']):
            image_name = own_media['data'][0]['id'] + '.jpeg'
            image_url = own_media['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url, image_name)
            print 'Your image has been downloaded!'
        else:
            print 'Post does not exist!'
    else:
            print 'Status code other than 200 received!'



#  Function to get a post id of a user.

def get_post_id(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()

    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_media = requests.get(request_url).json()

    if user_media['meta']['code'] == 200:

        if len(user_media['data']):
            return user_media['data'][0]['id']
        else:
            print 'There is no recent post of the user!'
            exit()

    else:
        print 'Status code other than 200 received!'
        exit()


# 4. Function declaration to get the recent post of a user by username

def get_user_post(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_media = requests.get(request_url).json()

    if user_media['meta']['code'] == 200:
        if len(user_media['data']):
            image_name = user_media['data'][0]['id'] + '.jpeg'
            image_url = user_media['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url, image_name)
            print 'Your image has been downloaded!'
        else:
            print 'Post does not exist!'
    else:
        print 'Status code other than 200 received!'

# 5. Function declaration to get the list of likes on a particular media.

def fetch_like_list(insta_username):
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + 'media/%s/likes?access_token= %s') % (media_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    list_of_likes_info = requests.get(request_url).json()

    if list_of_likes_info['meta']['code'] == 200:

        if len(list_of_likes_info['data']):
            for x in range(len(list_of_likes_info['data'])):
                print 'list of likes is %s' % (list_of_likes_info['data'][x]['username'])
        else:
            print colored('likes does not exist.', 'red')

    else:
        print colored('status code other than 200 received.', 'red')


# 6. Function to post a like on user's picture.

def post_a_like(insta_username):
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + 'media/%s/likes') % (media_id)
    payload = {"access_token": APP_ACCESS_TOKEN}
    print 'POST request url : %s' % (request_url)
    post_a_like = requests.post(request_url, payload).json()

    if post_a_like['meta']['code'] == 200:
        print 'Like was successful!'
    else:
        print 'Your like was unsuccessful. Try again!'

# 7. Function declaration to get the list of comments on a particular post.

def get_comments_list(insta_username):
    media_id = get_post_id(insta_username)
    if media_id is None:
        print colored("There is no media", 'red')
    else:
        request_url = BASE_URL + "media/%s/comments/?access_token=%s" % (media_id, APP_ACCESS_TOKEN)
        print "Get request url:%s" % request_url
        comment_list = requests.get(request_url).json()

    # check the status code, if comes 200 then show the list of comments
    if comment_list['meta']['code'] == 200:
        if len(comment_list['data']):
            print "The comments on the post :"
            for x in range(len(comment_list['data'])):
                comment_text = comment_list['data'][x]['text']
                print "comment: %s" % (comment_text)

        else:
            print colored("No comments on this post", 'red')
    else:
        print colored("Status code other than 200", 'red')



# 8. Function to post a comment on user's picture.

def post_a_comment(insta_username):
    media_id = get_post_id(insta_username)
    comment_text = raw_input("Your comment: ")
    payload = {"access_token": APP_ACCESS_TOKEN, "text": comment_text}
    request_url = (BASE_URL + 'media/%s/comments') % (media_id)
    print 'POST request url : %s' % (request_url)
    make_comment = requests.post(request_url, payload).json()

    if make_comment['meta']['code'] == 200:
        print "Successfully added a new comment!"
    else:
        print "Unable to add comment. Try again!"


# 9. Function to delete the negative comments.

def delete_negative_comment(insta_username):
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + 'media/%s/comments/?access_token=%s') % (media_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    comment_info = requests.get(request_url).json()

    if comment_info['meta']['code'] == 200:

        if len(comment_info['data']):

            for x in range(0, len(comment_info['data'])):
                comment_id = comment_info['data'][x]['id']
                comment_text = comment_info['data'][x]['text']
                blob = TextBlob(comment_text, analyzer=NaiveBayesAnalyzer())

                if (blob.sentiment.p_neg > blob.sentiment.p_pos):
                    print 'Negative comment : %s' % (comment_text)
                    delete_url = (BASE_URL + 'media/%s/comments/%s/?access_token=%s') % (
                        media_id, comment_id, APP_ACCESS_TOKEN)

                    print 'DELETE request url : %s' % (delete_url)
                    delete_info = requests.delete(delete_url).json()

                    if delete_info['meta']['code'] == 200:
                        print 'Comment successfully deleted!\n'
                    else:
                        print 'Unable to delete comment!'

                else:
                    print 'Positive comment: %s\n' % (comment_info)

        else:
            print "There are no comments on this post."

    else:
        print 'Status code other than 200 received!'


# 10. Function declaratio to perform sentiment analysis of comments on a post.

def sentiment_analysis(insta_username):



    post_id = get_post_id(insta_username)
    print "Fetching data..."
    req_url = BASE_URL + "media/" + post_id + "/comments/?access_token=" + APP_ACCESS_TOKEN

    comments = requests.get(req_url).json()
    data = ""
    if not comments['data']:
        print "No comments found."
    else:
        for temp in comments['data']:
            temp['text'] += " " + temp['text']
            data = temp['text']

        blob = TextBlob(data, analyzer=NaiveBayesAnalyzer())
        if blob.sentiment.classification == "neg":
            print "Overall negative content found."
        else:
            print "Overall Positive content found."
        print blob.sentiment.classification


# 11. Function to get the recent media liked by the user.

def recently_liked():

    request_url = (BASE_URL + 'users/self/media/liked?access_token=%s') % (APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    recent_liked_media = requests.get(request_url).json()

    if recent_liked_media['meta']['code'] == 200 :
        if len(recent_liked_media):
            image_name = recent_liked_media['data'][0]['id'] + '.jpeg'
            image_url = recent_liked_media['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url, image_name)
            print colored('Your image has been downloaded','green')
        else:
            print colored('No media found.','red')
    else:
        print colored('Status code other than 200 received.','red')


#Function declaration to start the bot.

def start_bot():
    while True:
        print '\n'
        print 'Hey! Welcome to instaBot!'
        print 'Here are your menu options:'
        print "1.Get your own details\n"
        print "2.Get details of a user by username\n"
        print "3.Get your own recent post\n"
        print "4.Get the recent post of a user by username\n"
        print "5.Get a list of people who have liked the recent post of a user\n"
        print "6.Like the recent post of a user\n"
        print "7.Get a list of comments on the recent post of a user\n"
        print "8.Make a comment on the recent post of a user\n"
        print "9.Delete negative comments from the recent post of a user\n"
        print "10.Sentiment Analysis\n"
        print "11.Get recent media liked by the user\n."
        print "12.Exit.\n"

        choice=raw_input("Enter you choice: ")
        if choice=="1":
            self_info()
        elif choice=="2":
            insta_username = raw_input("Enter the username of the user: ")
            get_user_info(insta_username)
        elif choice=="3":
            get_own_post()
        elif choice=="4":
            insta_username = raw_input("Enter the username of the user: ")
            get_user_post(insta_username)
        elif choice=="5":
           insta_username = raw_input("Enter the username of the user: ")
           fetch_like_list(insta_username)
        elif choice=="6":
           insta_username = raw_input("Enter the username of the user: ")
           post_a_like(insta_username)
        elif choice=="7":
           insta_username = raw_input("Enter the username of the user: ")
           get_comments_list(insta_username)
        elif choice=="8":
           insta_username = raw_input("Enter the username of the user: ")
           post_a_comment(insta_username)
        elif choice=="9":
           insta_username = raw_input("Enter the username of the user: ")
           delete_negative_comment(insta_username)
        elif choice=="10":
            sentiment_analysis(insta_username)

        elif choice == "11" :
            recently_liked()

        elif choice == "12":
            exit()

        else:
            print "Wrong choice"
start_bot()
