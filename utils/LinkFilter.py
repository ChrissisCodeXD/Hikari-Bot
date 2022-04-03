from imports import *
from Bot.DataBase.LinkSystem import DBLink

class LinkFilter:

    def __init__(self, app, msg: hikari.Message):
        self.app = app
        self.msg = msg
        self.guild_id = msg.guild_id
        self.settings = DBLink(app.db).get_settings(self.guild_id)

    async def case(self, case: str):
        await self.msg.delete()
        # TODO: Add audit log when message was deleted!

    async def is_social_media(self):
        regex = "http(?:s?):\/\/(?:www\.)?youtu(?:be\.com\/watch\?v=|\.be\/)([\w\-\_]*)(&(amp;)?‌​[\w\?‌​=]*)?"
        case = False
        if re.search(regex, self.msg.content):
            case = True
        regex = "/(?:(?:http|https):\/\/)?(?:www.)?(?:instagram.com|instagr.am|instagr.com)\/(\w+)/igm"
        if re.search(regex, self.msg.content):
            case = True
        regex = "https?:\/\/(?:www\.)?twitter\.com\/(?:#!\/)?(\w+)\/?(?:\S+)?$"
        if re.search(regex, self.msg.content):
            case = True
        regex = "https?:\/\/(?:www\.)?(?:youtube\.com|youtu.be)\/(?:watch\?v=)?(.+)"
        if re.search(regex, self.msg.content):
            case = True
        regex = "^http(?:s)?://(?:www\.)?(?:[\w-]+?\.)?reddit.com(/r/|/user/)?(?(1)([\w:]{2,21}))(/comments/)?(?(3)(\w{5,6})(?:/[\w%\\\\-]+)?)?(?(4)/(\w{7}))?/?(\?)?(?(6)(\S+))?(\#)?(?(8)(\S+))?$"
        if re.search(regex, self.msg.content):
            case = True
        regex = "/(?:http:\/\/)?(?:www\.)?facebook\.com\/(?:(?:\w)*#!\/)?(?:pages\/)?(?:[\w\-]*\/)*([\w\-]*)/"
        if re.search(regex, self.msg.content):
            case = True
        regex = "^https?:\/\/www\.facebook\.com.*\/(video(s)?|watch|story)(\.php?|\/).+$"
        if re.search(regex, self.msg.content):
            case = True
        regex = "^https?:\/\/www\.facebook\.com\/(?:(?:\w)*#!\/)?(?:pages\/)?(?:[\w\-]*\/)*([\w\-]*)/videos/(\w+)"
        if re.search(regex, self.msg.content):
            case = True
        regex = "^https?:\/\/www\.facebook\.com\/(?:(?:\w)*#!\/)?(?:pages\/)?(?:[\w\-]*\/)*([\w\-]*)/photos/(\w+)"
        if re.search(regex, self.msg.content):
            case = True
        regex = "^https?:\/\/www\.facebook\.com\/(?:(?:\w)*#!\/)?(?:pages\/)?(?:[\w\-]*\/)*([\w\-]*)/posts/(\w+)"
        if re.search(regex, self.msg.content):
            case = True
        regex = "|^http(s)?://pinterest.com/(.*)?$|i"
        if re.search(regex, self.msg.content):
            case = True
        regex = "|^http(s)?://(www\.)?pinterest\.com/(?!pin/)(.*)?$|i"
        if re.search(regex, self.msg.content):
            case = True
        regex = "|^http(s)?://(www\.)?pinterest\.com/pin/(.*)?$|i"
        if re.search(regex, self.msg.content):
            case = True
        regex = "|^http(s)?://(www\.)?pinterest\.com/([a-zA-Z0-9_\-]*)/?$|i"
        if re.search(regex, self.msg.content):
            case = True
        regex = "|^http(s)?://(www\.)?pinterest\.com/([a-zA-Z0-9_\-]*)/([a-zA-Z0-9_\-]*)/?$|i"
        if re.search(regex, self.msg.content):
            case = True
        regex = "|^http(s)?://(www\.)?pinterest\.com/([a-zA-Z0-9_\-]*)/([a-zA-Z0-9_\-]*)/([a-zA-Z0-9_\-]*)/?$|i"
        if re.search(regex, self.msg.content):
            case = True
        regex = "(?x)https?://(?:(?:www|m)\.(?:tiktok.com)\/(?:v|embed|trending)(?:\/)?(?:\?shareId=)?)(?P<id>[\da-z]+)"
        if re.search(regex, self.msg.content):
            case = True
        regex = "|^http(s)?://(www\.)?tiktok\.com/@([a-zA-Z0-9_\-]*)/?$|i"
        if re.search(regex, self.msg.content):
            case = True

        if case:
            await self.case("social_media")

    async def is_google(self):
        regex = "^https?:\/\/(www\.)?google\.com\/(search|url|webhp)?\?(.*)?q=(.*)?$"
        if re.search(regex, self.msg.content):
            await self.case("google")
        regex = "/http(s?):\/\/(www?).google.(com|ad|ae|com.af|com.ag|com.ai|al|am|co.ao|com.ar|as|at|com.au|az|ba|com.bd|be|bf|bg|com.bh|bi|bj|com.bn|com.bo|com.br|bs|bt|co.bw|by|com.bz|ca|cd|cf|cg|ch|ci|co.ck|cl|cm|cn|com.co|co.cr|com.cu|cv|com.cy|cz|de|dj|dk|dm|com.do|dz|com.ec|ee|com.eg|es|com.et|fi|com.fj|fm|fr|ga|ge|gg|com.gh|com.gi|gl|gm|gp|gr|com.gt|gy|com.hk|hn|hr|ht|hu|co.id|ie|co.il|im|co.in|iq|is|it|je|com.jm|jo|co.jp|co.ke|com.kh|ki|kg|co.kr|com.kw|kz|la|com.lb|li|lk|co.ls|lt|lu|lv|com.ly|co.ma|md|me|mg|mk|ml|com.mm|mn|ms|com.mt|mu|mv|mw|com.mx|com.my|co.mz|com.na|com.nf|com.ng|com.ni|ne|nl|no|com.np|nr|nu|co.nz|com.om|com.pa|com.pe|com.pg|com.ph|com.pk|pl|pn|com.pr|ps|pt|com.py|com.qa|ro|ru|rw|com.sa|com.sb|sc|se|com.sg|sh|si|sk|com.sl|sn|so|sm|sr|st|com.sv|td|tg|co.th|com.tj|tk|tl|tm|tn|to|com.tr|tt|com.tw|co.tz|com.ua|co.ug|co.uk|com.uy|co.uz|com.vc|co.ve|vg|co.vi|com.vn|vu|ws|rs|co.za|co.zm|co.zw|cat)\/*/"
        if re.search(regex, self.msg.content):
            await self.case("google")

    async def is_bitly(self):
        regex = "http://(linkd\.in|t\.co|bitly\.co|tcrn\.ch).*?(\s|$)"
        if re.search(regex, self.msg.content):
            await self.case("bitly")

    async def is_discord(self):
        regex = "(https?:\/\/)?(www\.)?(discord\.(gg|io|me|li)|discordapp\.com\/invite)\/.+[a-z]"
        if re.search(regex,self.msg.content):
            await self.case("discord")

    async def is_gif(self):
        regex = "(?:([^:/?#]+):)?(?://([^/?#]*))?([^?#]*\.(?:gif))(?:\?([^#]*))?(?:#(.*))?"
        if re.search(regex,self.msg.content):
            await self.case("gif")

    async def is_link(self):
        regex = "(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})"
        if re.search(regex,self.msg.content):
            await self.case("link")
