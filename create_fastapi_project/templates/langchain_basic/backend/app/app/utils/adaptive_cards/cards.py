import adaptive_cards.card_types as types
from adaptive_cards.card import AdaptiveCard
from adaptive_cards.elements import TextBlock, Image, Media
from adaptive_cards.containers import Container, ImageSet
from adaptive_cards.actions import ActionSubmit
import re

from app.schemas.adaptive_cards_schema import ICreateMediaAC


def custom_media(anwser):
    regex_http = r'https?://[^\s"]+'
    url_search = re.search(regex_http, anwser)
    url_search_all = re.findall(regex_http, anwser)

    regex_image = r"\b(https?|ftp):\/\/[^\s/$.?#].[^\s]*\.(jpg|jpeg|png|gif|webp)\b"
    url_image_search = re.search(regex_image, anwser)

    if url_image_search:
        url_image = url_search.group()
        if url_image.endswith(")"):
            url_image = url_image[:-1]
        if url_image.endswith(")."):
            url_image = url_image[:-2]
        media = Image(url=url_image)
        return None
        return ICreateMediaAC(media_object=media, media_type="image", url=url_image)

    regex_audio = r"\b(https?|ftp):\/\/[^\s/$.?#].[^\s]*\.(mp3|wav|ogg)\b"
    url_search_audio = re.search(regex_audio, anwser)
    if url_search_audio:
        url_audio = url_search_audio.group()
        media = Media(
            sources=[{"mimeType": "audio/mp3", "url": url_audio}],
            poster="https://adaptivecards.io/content/poster-audio.jpg",
        )
        return ICreateMediaAC(media_object=media, media_type="audio", url=url_audio)

    regex_video = r"\b(https?|ftp):\/\/[^\s/$.?#].[^\s]*\.(mp4|webm|ogg)\b"
    url_search_video = re.search(regex_video, anwser)
    if url_search_video:
        url_video = url_search_video.group()
        media = Media(
            sources=[{"mimeType": "video/mp4", "url": url_video}],
            # poster="https://adaptivecards.io/content/poster-video.png",
            poster="https://douglasgreen.com/wp-content/uploads/2014/03/video-play-btn-featured.png",
        )
        return ICreateMediaAC(media_object=media, media_type="video", url=url_video)

    regex_youtube_video = (
        r"(https?://)?(www\.)?"
        "(youtube|youtu|youtube-nocookie)\\.(com|be)/"
        "(watch\\?v=|embed/|v/|.+\\?v=)?([^&=%\\?]{11})"
    )
    url_search_youtube_video = re.search(regex_youtube_video, anwser)

    if url_search_youtube_video:
        url_youtube_video = url_search_youtube_video.group()
        media = Media(
            sources=[{"mimeType": "video/mp4", "url": url_youtube_video}],
        )
        return ICreateMediaAC(
            media_object=media, media_type="youtube_video", url=url_youtube_video
        )

    if len(url_search_all) > 0:
        list_media_element = []
        for photo in url_search_all:
            if "https://images.unsplash.com" in photo:
                media = Image(url=photo)
                list_media_element.append(media)
        body_container_images = ImageSet(images=list_media_element)
        return None
        return ICreateMediaAC(
            media_object=body_container_images, media_type="image", url=""
        )

    return None


def create_hidden_video_card(url):
    return Media(
        sources=[
            {
                "mimeType": "video/mp4",
                "url": url,
            }
        ],
        is_visible=False,
    )


def create_adaptive_card(answer: str, actions: list[str] = []) -> AdaptiveCard:
    custom_media_element: ICreateMediaAC | None = custom_media(answer)
    custom_media_item = (
        custom_media_element.media_object if custom_media_element else None
    )
    hidden_video_youtube = None
    # if custom_media_element.media_type == "youtube_video":
    #     hidden_video_youtube = create_hidden_video_card(custom_media_element.url)
    if custom_media_element and custom_media_element.media_type == "youtube_video":
        hidden_video_youtube = create_hidden_video_card(custom_media_element.url)

    # if custom_media_element:
    #     answer = answer.replace(custom_media_element.url, "")

    description_text = TextBlock(text=answer, wrap=True)
    items = [
        description_text,
        custom_media_item,
        hidden_video_youtube,
    ]
    body_container = Container(items=items)

    # crear action
    actions = [ActionSubmit(title=action) for action in actions]

    # Crear Adaptive Card
    adaptive_card = AdaptiveCard(body=[body_container], actions=actions, version="1.5")

    return adaptive_card


def create_image_card(image_url: str) -> AdaptiveCard:
    image = Image(url=image_url)
    body_container = Container(items=[image])
    adaptive_card = AdaptiveCard(body=[body_container], version="1.5")

    return adaptive_card


def create_loading_card(image_url: str) -> AdaptiveCard:
    image = Image(
        url=image_url,
        size="small",
        horizontal_alignment=types.HorizontalAlignment.LEFT,
    )
    body_container = Container(items=[image])
    adaptive_card = AdaptiveCard(body=[body_container], version="1.5")

    return adaptive_card
