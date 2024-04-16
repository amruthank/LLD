"""
    List of classes:
        1. User: name, email
        2. Post: post_id, content: text, author: user_email, create_date, update_date, likes, dislikes
        3. Comment: comment_id, post_id, user_id, content, create_date
        4. NewsFeed
        5. Article: TODO

        Data Structure:
            1. priority queue: get latest 10 posts
            2. map: User objects
            3. map: post_id: [post_obj, comments: [], updated_at]
"""
import collections
from datetime import datetime
import random
import heapq
class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email  # PK

    def getName(self):
        return self.name

    def getEmail(self):
        return self.email

    def __str__(self):
        return f'User {self.name} - {self.email} is created.'

class Post:
    def __init__(self, author_email, title, content):
        self.pid = random.randint(0, 10000)
        self.content = content
        self.author = author_email
        self.created_at = datetime.now()
        self.update_at = datetime.now()
        self.likes = 0
        self.dislikes = 0
        self.title = title

    def getContent(self):
        return self.content
    def getTitle(self):
        return self.title
    def getAuthor(self):
        return self.author
    def getCreateDate(self):
        return self.created_at
    def updateDate(self):
        self.update_at = datetime.now()

    def getUpdateDate(self):
        return self.update_at

    def updateLikes(self, count): #Count can be +1 or -1
        if count == -1 and self.likes <= 0:
            return
        self.likes += count

    def getLikes(self):
        return self.likes

    def updateDisLikes(self, count):
        if count == -1 and self.dislikes <= 0:
            return
        self.dislikes += count

    def getDisLikes(self):
        return self.dislikes

    def __str__(self):
        return f'A new post {self.title} is created by the auther {self.author} at {self.created_at}.'


class Comment:

    def __init__(self, post_id, author, content):
        self.id = random.randint(0, 10000)
        self.post_id = post_id
        self.author = author
        self.content = content
        self.created_at = datetime.now()

    def getCommentID(self):
        return self.id

    def getContent(self):
        return self.content

    def getAuthor(self):
        return self.author

    def getPostID(self):
        return self.post_id

    def getCreatedAt(self):
        return self.created_at

    def __str__(self):
        return f'A new comment is added for the post {self.post_id} by {self.author}.'


class NewsFeed:

    def __init__(self):
        self.news = list()
        self.size = 10
        self.users = collections.defaultdict()
        self.posts = collections.defaultdict()


    def addUser(self, name, email):
        print("Function to add %s to the news feed system."%email)
        if self.users.get(email, None) == None:
            self.users[email] = User(name, email)
        return self.users[email]

    def createPost(self, email, title, content):
        print("Function to create a post.")
        post = Post(email, title, content)
        while self.posts.get(post.pid, None) != None:
            post = Post(email, title, content)
        self.posts[post.pid] = {}
        self.posts[post.pid]["obj"] = post
        self.posts[post.pid]["comments"] = []
        self.posts[post.pid]["updatedAt"] = datetime.now()
        heapq.heappush(self.news, (post.created_at, post.pid)) # Managing the latest posts.
        if len(self.news) > self.size:
            heapq.heappop(self.news)
        print(self.posts)
        return post.pid

    def updatePost(self, pid, email, content):
        print("Function to update the post.")

        if self.posts.get(pid, None) == None:
            return "Invalid post!"
        elif self.posts[pid]["obj"].author != email:
            return "No permission to update this post!"
        else:
            post = self.posts[pid]["obj"]
            post.content = content
            post.updateDate()
            self.posts[post.pid]["updatedAt"]  = post.update_at

    def getPost(self, pid):
        print("Function to get the post ", pid)
        if self.posts.get(pid, None) == None:
            return "Invalid post!"
        response = {}
        response["title"] = self.posts[pid]["obj"].title
        response["email"] = self.posts[pid]["obj"].author
        response["content"] = self.posts[pid]["obj"].content
        response["likes"] = self.posts[pid]["obj"].likes
        response["dislikes"] = self.posts[pid]["obj"].dislikes
        response["comments"] = [(comment.content, comment.created_at) for comment in  self.posts[pid]["comments"]]
        response["createdAt"] = self.posts[pid]["obj"].created_at
        response["updatedAt"] = self.posts[pid]["updatedAt"]
        return response

    def topPosts(self):
        print("Function to get top %s posts.", self.size)
        result = []
        for date, pid in heapq.nlargest(self.size, self.news):
            result.append((self.posts[pid]["obj"].title, self.posts[pid]["obj"].content))
        return result

    def getAllPosts(self):
        print("Function to get all posts.")
        response = []
        for k, v in self.posts.items():
            response.append((v["obj"], v["comments"]))
        return response

    def likes(self, pid, count):
        print("Function to add likes.")
        if self.posts.get(pid, None) == None:
            return "Invalid post!"
        post = self.posts[pid]
        post["obj"].updateLikes(count)

    def dislikes(self, pid, count):
        print("Function to add dislikes.")
        if self.posts.get(pid, None) == None:
            return "Invalid post!"
        post = self.posts[pid]
        post["obj"].updateDisLikes(count)

    def addComment(self, pid, email, content):
        print('Function to add a comment to a post {0} - {1}'.format(pid, email))

        if self.posts.get(pid, None) == None:
            return "Invalid post!"
        elif self.users.get(email, None) == None:
            return "Invalid user!"
        else:
            comment = Comment(pid, email, content)
            self.posts[pid]["comments"].append(comment)
        return


if __name__ == "__main__":
    nf = NewsFeed()
    users = [("Joey", "joey@gmail.com"), ("tina", "tina@gmail.com"), ("mike", "mike@gmail.com")]
    for name, email in users:
        nf.addUser(name, email)

    #Post 1 is created.
    pid1 = nf.createPost(users[0][1], "India", "India is a beautiful country.")
    nf.addComment(pid1, users[1][1], "Good article!")
    nf.addComment(pid1, users[2][1], "Thanks for sharing this content")
    nf.likes(pid1, 1); nf.dislikes(pid1, 1)

    pid2 = nf.createPost(users[1][1], "Travel", "This travel post is about my switzerland trip!")
    nf.addComment(pid2, users[0][1], "Nice")
    nf.likes(pid2, 1); nf.likes(pid2, 1)

    nf.updatePost(pid1,users[0][1], "India is a beautiful and diversed country.")
    print(nf.getPost(pid1))
    print(nf.getPost(pid2))
    print(nf.topPosts())