import requests
import os
import aiofiles.os
import magic
from PIL import Image
from nio import AsyncClient, UploadResponse
import asyncio

class matrix_social_client:

    def __init__(self, access_token=None, user_id=None, device_id=None, room_id=None, homeserver="https://matrix.org"):
        self.client = AsyncClient(homeserver)
        self.client.access_token = access_token
        self.client.user_id = user_id
        self.client.device_id = device_id
        self.room_id = room_id


    async def sync_create_post(self, text, mentions, images):
        if images:
            for image in images:
                response = requests.get(image)
                filename = image.split('/')[-1]
                if response.status_code == 200:
                    with open(filename, 'wb') as f:
                        f.write(response.content)
                mime_type = magic.from_file(filename, mime=True)
                if not mime_type.startswith("image/"): return

                (width, height) = Image.open(filename).size
                file_stat = await aiofiles.os.stat(filename)
                async with aiofiles.open(filename, "r+b") as f:
                    resp, maybe_keys = await self.client.upload(
                        f,
                        content_type=mime_type,
                        filename=os.path.basename(filename),
                        filesize=file_stat.st_size,
                    )

                if not isinstance(resp, UploadResponse):
                    return False

                content = {
                    "body": os.path.basename(filename),
                    "info": {
                        "size": file_stat.st_size,
                        "mimetype": mime_type,
                        "thumbnail_info": None,
                        "w": width,
                        "h": height,
                        "thumbnail_url": None,
                    },
                    "msgtype": "m.image",
                    "url": resp.content_uri,
                }


                try:
                    await self.client.room_send(self.room_id, message_type="m.room.message", content=content)
                except:
                    return False
                
        if mentions:
            text = text + "\n\n" + " ".join([f"https://matrix.to/#/@{mention}" for mention in mentions])
        content = {
            "msgtype": "m.text",
            "format": "org.matrix.custom.html",
            "body": text,
        }
        try:
            await self.client.room_send(self.room_id, message_type="m.room.message", content=content)
            await self.client.close()
            return True
        except:
            return False
    
    def create_post(self, content, mentions, images):
        result = asyncio.run(self.sync_create_post(content, mentions, images))
        return result
        

    