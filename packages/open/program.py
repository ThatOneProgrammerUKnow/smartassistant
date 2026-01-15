class Program:
    
    _instances = []

    def __init__(self, name, path, alias=[]):
        # Atttributes
        self.name = name
        self.path = path
        # Always include the program name as an alias
        self.alias = [self.name.upper()]
        
        if alias:
            self.alias.extend([str(a).upper() for a in alias])

        # Instances
        Program._instances.append(self)
    
 
    
    def __str__(self):
        return f"{self.name}"


##-->> Other methods
# Add new program here
def load():
    Program._instances.clear()
    

    return [
    #=====# Programs #=====#
    Program("Spotify", "C:/Users/kobus/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Spotify.lnk", ["spotify", "music"]),
    Program("Logitec G HUB", "C:/ProgramData/Microsoft/Windows/Start Menu/Programs/Logi/Logitech G HUB.lnk", ["g hub", "logitec", "mouse app", "mouse settings"]),
    Program("Discord", "C:/Users/kobus/OneDrive/Desktop/Discord.lnk"),
    Program("Google", "C:/Program Files/Google/Chrome/Application/chrome.exe", ["chrome"]),
    Program("Visual Studio Code", "C:/Users/kobus/OneDrive/Desktop/Visual Studio Code.lnk", ["vs code", "visual studio", "visual studio's"]),
    Program("Docker Desktop", "C:/Users/kobus/OneDrive/Desktop/Docker Desktop.lnk", ["docker"]),
    Program("Android Studios", "C:/Users/kobus/OneDrive/Desktop/Android Studio.lnk"),
    Program("Fusion 360", "C:/Users/kobus/OneDrive/Desktop/Autodesk Fusion.lnk", ["fusion"]),
    Program("Prusa Slicer", "C:/Users/Public/Desktop/PrusaSlicer 2.8.1.lnk"),
    Program("Arduinio IDE", "C:/Users/Public/Desktop/Arduino.lnk", ["arduino code", "arduino editor"]),
    Program("GitHUB Desktop", "C:/Users/kobus/OneDrive/Desktop/GitHub Desktop.lnk"),
    Program("Canva", "C:/Users/kobus/OneDrive/Desktop/Canva.lnk"),
    Program("Steam", "C:/Users/kobus/OneDrive/Desktop/Steam.lnk"),
    

    #=====# Files #=====#
    Program("Timesheet", "C:/Users/kobus/OneDrive/Desktop/Kobus/VSI/Timesheet.xlsx", ["timesheet", "time sheet"]),
    Program("Desktop", "C:/Users/kobus/OneDrive/Desktop", ["file explorer", "my files"]),

    #=====# Websites #=====#
    ## Google Programs
    Program("Google Calender", "https://calendar.google.com/calendar/u/0/r", ["Calender"]),

    Program("Youtube", "https://www.youtube.com/"),
    Program("Youtube History", "https://www.youtube.com/feed/history"),
    
    ## Shortcuts
    Program("Bible", "https://www.bible.com/bible", ["bible", "youversion"]),
    Program("Chess", "https://www.chess.com/"),
    Program("CTU Student Campus online", "https://ctu.campusmanager.co.za/portal/student-home.php", ["student website", "student dashboard", "student faculty"]),
    Program("Udemy", "https://www.udemy.com/?utm_source=adwords-brand&utm_medium=udemyads&utm_campaign=Brand-Udemy_la.EN_cc.ROW&campaigntype=Search&portfolio=BrandDirect&language=EN&product=Course&test=&audience=Keyword&topic=&priority=&utm_content=deal4584&utm_term=_._ag_80315195513_._ad_535757779892_._kw_udemy_._de_c_._dm__._pl__._ti_kwd-296956216253_._li_1028743_._pd__._&matchtype=b&gad_source=1&gclid=CjwKCAiAm-67BhBlEiwAEVftNvzvrWw2SQ5SlnvKbRSdB0OuKoyNnXHiRQsdNbQl0THnWXopLkHB3xoCJrMQAvD_BwE"),
    Program("Kindle", "https://read.amazon.com/kindle-library"),
    Program("Trello", "https://trello.com/?campaign=18422680946&adgroup=142052239375&targetid=kwd-3609071522&matchtype=e&network=g&device=c&device_model=&creative=672183050319&keyword=trello&placement=&target=&ds_eid=700000001557344&ds_e1=GOOGLE&gad_source=1&gad_campaignid=18422680946&gbraid=0AAAAADMO9Yh1cY34d2_Lr3GNrUSKscXSn&gclid=Cj0KCQjwotDBBhCQARIsAG5pinNmITRKD1VNC9_xQAoZAnqbjCG-sWHtIJwfYVsqwVfnbGfaenbFR7waAn_QEALw_wcB"),
    Program("Claude AI", "https://claude.ai/"),
    Program("GitHUB", "https://github.com/"),
    Program("W3Schools", "https://pathfinder.w3schools.com/", ["w three schools", "w schools", "three schools"]),
    Program("Ultimate guitar", "https://www.ultimate-guitar.com/"),

    ## Bookmarks
    Program("Amazon Prime Video", "https://www.primevideo.com", ["prime", "prime video", "amazon prime"]),
    Program("Satrix", "https://platform.satrixnow.co.za/AccountOverview"),
    Program("Elevenlabs", "https://elevenlabs.io/app/speech-synthesis/text-to-speech"),
    Program("Minecraft Server", "https://intenseservers.co.za/dashboard.php"),

    # Shoping
    Program("Takelot", "https://www.takealot.com/?gclsrc=aw.ds&gad_source=1&gad_campaignid=21875674689&gbraid=0AAAAADuiBEw3rI9L83FkIO-S3vmgW3NDP&gclid=Cj0KCQjw-ZHEBhCxARIsAGGN96L6swZyGVZ8Nr_Dy2cdRJVDkwMjdPbt5HWKXW3iZ-c7B"),
    Program("Makro", "https://www.makro.co.za"),
    Program("Amazon", "https://www.amazon.co.za/?tag=zatxtabkgode-21&ref=nav_signin&adgrpid=176086901168&hvpone=&hvptwo=&hvadid=721507624979&hvpos=&hvnetw=g&hvrand=17970700248363669328&hvqmt=e&hvdev=c&hvdvcmdl=&hvlocint=&hvlocphy=9195388&hvtargid=kwd-360364908397&hydadcr=9972_2328982&mcid=6799fe1a2d4d3f7d8d5f50780aa631c2&language=en_ZA&gad_source=1"),

    ## Other
]


#====================# Public functions #====================#
def is_valid(query):
    for program in Program._instances:
        if any(a in query.upper() for a in program.alias):
            return True
    return False

def find(query):
    for program in Program._instances:
        if any(a in query.upper() for a in program.alias):
            return program
    return "Something went wrong"  
    
def all():
    return [str(program) for program in Program._instances]




    
