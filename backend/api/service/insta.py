import json
import os

import instaloader
from instaloader import Post, Profile

L = instaloader.Instaloader()
L.load_session_from_file("CHANGE_THIS_TO_YOUR_USERNAME - It was `mahasvan.exe` previously")


def clear_folder(username):
    if not os.path.exists(username):
        os.makedirs(username)
    for file in os.listdir(username):
        os.remove(os.path.join("snuc_cc", file))


def get_latest_post(username):
    clear_folder(username=username)
    for post in Profile.from_username(L.context, username).get_posts():
        print(post.caption)
        L.download_post(post, target=username)
        break
    files = os.listdir(username)
    image_file = next(file for file in files if file.endswith("jpg"))
    caption_file = next(file for file in files if file.endswith("txt"))
    caption = open(os.path.join(username, caption_file)).read()
    image = open(os.path.join(username, image_file), "rb").read()
    # image is returned as bytes, kjust save onmto a file and when pittong it to ollama, jist pass in the file patrh where you save in

    return caption, image


# todo: add vision model interfacing
# the get_latest_post endpoint gives binary data for the image, need to encode it into base64 and pass it into ollama via cURL
# https://ollama.com/library/llava - API Usage Section

# SIGN IN TO INSTA
# https://instaloader.github.io/troubleshooting.html#login-error
# you need Firefox in Windows or macOS
# The cookies from firefox are used here
