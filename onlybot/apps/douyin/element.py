# -*- coding: utf-8 -*-
"""
@Description: 
@Date       : 2024/4/9 23:19
@Author     : 
@Version    : 
@License    : 
@Github     : 
@Mail       : 
-------------------------------------------------
Change Log  :
2024/4/9 23:19 -  - 
"""


class DouyinEleSelector:
    # 用于判断是否登入的元素
    IS_LOGIN_SIGN = 'button:has-text("登录")'

    # 用于获取二维码的元素
    LOGIN_GET_QR = '#web-login-container > article > article > article > div:nth-child(2) > div > div.web-login-scan-code__content__qrcode-tip > img'

    # 用于判断是否扫描二维码的元素
    LOGIN_CHECK_QR = '#web-login-container > article > article > article > div:nth-child(2) > div > div.web-login-scan-code__content__qrcode-wrapper > div > div > p.web-login-scan-code__content__qrcode-wrapper__mask__toast__text.success'

    # 用于判断二维码是否有风险防控
    LOGIN_SECURITY_QR = '#uc-second-verify'

    # 登入频繁警告
    LOGIN_FREQUENT_QR = ''

    # 验证码登入标签
    SMS_LOGIN_TAG = '#web-login-container > article > article > article > div.web-login-common-wrapper__tab > ul.web-login-tab-list > li:nth-child(2)'

    # 验证码登入手机号码输入框
    SMS_LOGIN_PHONE_INPUT = '#web-login-container > article > article > article > form > div.web-login-mobile-code__mobile-input-wrapper > div > input'

    # 获取验证码按钮
    GET_SMS_CODE_BUTTON = '#web-login-container > article > article > article > form > div.web-login-mobile-code__code-input-wrapper > div > span'

    # 二次验证接收验证码标签
    RE_SMS_VERIFY_TAG = 'p:has-text("接收短信验证")'

    # 二次验证验证码输入框
    RE_SMS_CODE_INPUT = '#uc-second-verify > div > div > article > div > div > div > div> input[type=number]'

    # 二次验证验证码提交按钮
    RE_SMS_CODE_SUMMIT_BUTTON = 'div.uc-ui-verify_sms-verify_button:has-text("验证")'

    # 二次验证发送验证码按钮
    RE_SMS_CODE_SEND_BUTTON = 'p:has-text("获取验证码")'

    # 登入用户昵称标签
    LOGIN_USER_NICKNAME = '#douyin-right-container > div.tQ0DXWWO.DAet3nqK.userNewUi > div > div > div.o1w0tvbC.F3jJ1P9_.InbPGkRv > div.mZmVWLzR > div.ds1zWG9C > h1 > span > span > span > span > span > span'

    # 我的导航栏
    MY_NAV_TAG = '#island_e62be > div > div > div.juSoeZQJ.YK5O2mtI > div > div:nth-child(1) > div.FvezCAI7 > div > div.EoY455Q_.QQzJ6KOK.pGb3BrAQ.QyvqC4r5.zipjTPpf > a'

    # 评论输入框
    COMMENT_INPUT = '#merge-all-comment-container > div > div > div > div > div > div > div > div > div > div > div > div > span > span'

    # 打开评论标签
    OPEN_COMMENT_TAG = '#sliderVideo > div > div > div > div > div > div:nth-child(3) > div > div'

    # 点击评论输入框
    CLICK_COMMENT_INPUT = '#merge-all-comment-container > div > div.comment-input-container'

    # 视频点赞
    VIDEO_LIKE = '#sliderVideo > div > div.slider-video > div > div.immersive-player-switch-on-hide-interaction-area.positionBox > div > div:nth-child(2) > div > div'

    # 视频收藏
    VIDEO_COLLECT = '#sliderVideo > div.playerContainer > div.slider-video > div > div > div > div:nth-child(4) > div > div'

    # 发现下一条视频
    VIDEO_NEXT = '#sliderVideo > div > div > div > div > div> div > div > div.xgplayer-playswitch-next'

    # 推荐类型为直播标记
    RECOMMEND_VIDEO_IS_LIVE = '#slider-card > div > a'

    # 用户视频详情文案
    VIDEO_DESC = '#video-info-wrap>.video-info-detail'

    # 滑块验证码
    PASS_CAPTCHA = '#captcha_container'

    # 关闭滑块验证码
    CLOSE_CAPTCHA = '#vc_captcha_box > div > div > div.vc-captcha-close-btn.captcha_verify_bar--close'

    # 直播弹幕发送
    LIVE_BARRAGE_INPUT = '#chat-textarea'
