# Galaxy Social

To create a post, follow these steps:

1. Create a pull request to the "posts" folder.
2. Inside the pull request, create a new file with the extension ".md".
3. Use the following template for the post content:

```
---
media:
  - bluesky
  - mastodon
  - matrix
  - slack

images:
  - url: https://exampla.com/a.jpg
    alt_text: A
  - url: https://example.org/b.png
    alt_text: B

mentions:
  bluesky:
    - a.bsky.social
  mastodon:
    - a
  matrix:
    - a:matrix.org

hashtags:
  bluesky:
    - a
    - b
  mastodon:
    - c
    - d
---
Text
```

After each pull request, an action will run, and the results of it will be added to `processed_files.json` in processed_files brach.

# Add a new social media

To create a new plugin, you have to add a Python file to the plugins folder with the function `create_post(content, mentions, hashtags, images, alt_texts)` inside a class to handle sending announcements to the social media, and then add it to `plugins.yml` following this template:

```
  - name: name_of_the_media
    class: file_name.class_name
    enabled: true
    config:
      token: TOKEN_SAVED_IN_PUBLISH_CONTENT
```

The `name` is then used in the `media` tag in the post file (posts/*.md) to determine the social media.

Just with `enabled: true`, the social media will be implemented.

In the config, you have to add all the variables needed for the class inside your plugin to initialize.

You have to then add tokens and variables needed to start the client to [GitHub secrets](https://docs.github.com/en/actions/security-guides/using-secrets-in-github-actions#creating-secrets-for-a-repository) and in `publish_content.yml` add an env variable like this template:


```
TOKEN_SAVED_IN_PUBLISH_CONTENT: ${{ secrets.TOKEN_SAVED_IN_GITHUB_SECRETS }}
```

# Social media implemented
- Bluesky
- Mastodon
- Matrix: hashtags and alt_text for image are not working!
- Slack: mentions and hashtags are not working!
