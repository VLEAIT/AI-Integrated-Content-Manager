from services.social.base import BaseSocialPublisher
from services.social.meta import MetaPublisher
from services.social.stub import StubPublisher
from schemas import platform_opt

class SocialDispatcher:
    @staticmethod
    def get_publisher(platform:platform_opt,is_dev_mode:bool=True)->BaseSocialPublisher:
        if is_dev_mode:
            return StubPublisher()
        if platform in [platform_opt.facebook,platform_opt.instagram]:
            return MetaPublisher()
        else:
            ValueError(f"Unsupported platform:{platform}")