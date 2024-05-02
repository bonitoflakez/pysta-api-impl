from flask import Flask, jsonify
from instaloader import Instaloader, Profile

app = Flask(__name__)

@app.route('/fetch_reels/<username>', methods=['GET'])
def fetch_reels(username):
    try:
        # Initialize Instaloader
        L = Instaloader()
        print("[!] Loaded loader class")

        # Retrieve profile info
        profile = Profile.from_username(L.context, username)
        print("[+] Loading " + username + " profile")

        # Fetch reels
        reels = []
        for post in profile.get_posts():
            print("[!] Post found")
            if post.is_video and post.typename == 'GraphVideo':
                print("[+] Is a reel")
                reels.append({
                    'id': post.mediaid,
                    'caption': post.caption,
                    'video_url': post.video_url,
                    'thumbnail_url': post.url,
                    'likes': post.likes,
                    'comments': post.comments,
                    'timestamp': post.date.strftime('%Y-%m-%d %H:%M:%S')
                })

        return jsonify({'reels': reels}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
