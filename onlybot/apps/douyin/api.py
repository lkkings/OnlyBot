class DouyinAPIEndpoints:
    """
    API Endpoints for Douyin
    """

    # 抖音域名
    DOUYIN_DOMAIN = "https://www.douyin.com"

    # 抖音直播域名
    DOUYIN_LIVE_DOMAIN = "https://live.douyin.com"

    # 发现页面
    DISCOVER_URL = "https://www.douyin.com/discover"

    # 推荐页面
    RECOMMEND_URL = "https://www.douyin.com/?recommend=1"

    # SSO域名 (SSO Domain)
    SSO_DOMAIN = "https://sso.douyin.com"

    # 登录检查 (Login Check)
    SSO_LOGIN_CHECK_QR = f"{SSO_DOMAIN}/check_qrconnect/"

    # 登入用户详细信息 (User Detail Info)
    USER_DETAIL = f"{DOUYIN_DOMAIN}/user/self"

    # SSO登录 (SSO Login)
    SSO_LOGIN_GET_QR = f"{SSO_DOMAIN}/get_qrcode/"

    # 验证码校验
    SMS_LOGIN_VALIDATE = f"{DOUYIN_DOMAIN}/passport/web/validate_code/"

    # 人机校验
    REBOT_CHECK = "https://rmc.bytedance.com/verifycenter/captcha"