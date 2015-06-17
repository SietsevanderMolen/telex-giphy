import tgl
from telex import plugin
import giphypop
import random
import os


class GiphyPlugin(plugin.TelexPlugin):
    """
    Get gifs from giphy.com
    """

    patterns = {
        "^{prefix}giphy$": "giphy_random",
        "^{prefix}giphy (.+)$": "giphy_search"
    }

    usage = [
        "{prefix}giphy: return random giphy",
        "{prefix}giphy (keyword): do a giphy search for keyword and return random giphy"
    ]

    def __init__(self):
        super().__init__()
        self.giphy = giphypop.Giphy()

    def giphy_random(self, msg, matches):
        gif = self.giphy.random_gif()
        self.send_gif(msg, gif)

    def giphy_search(self, msg, matches):
        gif = random.choice(self.giphy.search_list(matches.group(1)))
        self.send_gif(msg, gif)

    def send_gif(self, msg, gif):
        filename = self.bot.download_to_file(gif.media_url, "gif")
        peer = self.bot.get_peer_to_send(msg)

        def cleanup_cb(success, msg):
            if success:
                os.remove(filename)
            else:
                peer.send_msg("Giphy: something went wrong")
            
        tgl.send_document(peer, filename, cleanup_cb)

