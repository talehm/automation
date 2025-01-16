from .social_media_service import SocialMediaService


def run(post_type: str, post_id: str, social_platform: str, count: int):
    service = SocialMediaService(social_platform)
    return service.process_post(post_type, post_id, count)
