from mastodon import Mastodon
from bs4 import BeautifulSoup
import textwrap
import requests


class mastodon_client:
    def __init__(self, **kwargs):
        self.base_url = kwargs.get("base_url", "https://mstdn.science")
        self.mastodon_handle = Mastodon(
            access_token=kwargs.get("access_token"), api_base_url=self.base_url
        )
        self.max_content_length = kwargs.get("max_content_length", 500)

    def create_post(self, content, mentions, hashtags, images):
        media_ids = []
        for image in images[:4]:
            response = requests.get(image["url"])
            filename = image["url"].split("/")[-1]
            if response.status_code == 200:
                with open(filename, "wb") as f:
                    f.write(response.content)
                media_uploaded = self.mastodon_handle.media_post(
                    media_file=filename,
                    description=image["alt_text"] if "alt_text" in image else None,
                )
                media_ids.append(media_uploaded["id"])

        toot_id = None
        status = []
        mentions = " ".join([f"@{v}" for v in mentions])
        hashtags = " ".join([f"#{v}" for v in hashtags])
        for text in textwrap.wrap(
            content + "\n" + mentions + "\n" + hashtags,
            self.max_content_length,
            replace_whitespace=False,
        ):
            toot = self.mastodon_handle.status_post(
                status=text,
                in_reply_to_id=toot_id,
                media_ids=media_ids if (media_ids != [] and toot_id == None) else None,
            )
            
            if not toot_id:
                link = f"{self.base_url}/@{toot['account']['acct']}/{toot['id']}"
            toot_id = toot["id"]
            
            for _ in range(3):
                post = self.mastodon_handle.status(toot_id)
                if post.content:
                    post_content = BeautifulSoup(post.content, "html.parser").get_text(
                        separator=" "
                    )
                    status.append(
                        "".join(post_content.split()) == "".join(text.split())
                    )
                    break

        return all(status), link
