import instaloader, discord, os, random, datetime, asyncio
from discord.ext.commands import Bot

#CONFIGURE BEFORE USE
mImageDir = ""#enter the directory that will store the folder the pictures will be in(dont include the file name)
mChannelID = #enter the channel you wish to use for the bot(dont leave blank and dont enclose in quotes)
insAccount = "tommyinnitt"#enter the instagram account to use pictures from(default tommyinnitt)
nSDelay = #enter the amount of seconds to wait till next picture is sent

#initialising discord bot CONFIGURE BEFORE USE
BOT_PREFIX = ("t!")#
TOKEN = ""#enter your bot oauth token
client = Bot(command_prefix=BOT_PREFIX)

#initialising instaloader
loader = instaloader.Instaloader()
loader.post_metadata_txt_pattern = ""
loader.download_geotags = False
loader.save_metadata = False
loader.save_metadata_json = False
loader.download_comments = False
profile = instaloader.Profile.from_username(loader.context, insAccount)
posts = profile.get_posts()

async def randPics():
    imageDir = mImageDir
    await client.wait_until_ready()
    channel = client.get_channel(mChannelID)
    dateTimeObj = datetime.datetime.now()
    startTime = 10#10am
    endTime = 22#10pm   
    tfHour = int(dateTimeObj.strftime("%H"))
    print(tfHour)
    if (tfHour >= startTime and endTime >= tfHour):
        while not client.is_closed():
            randPic = random.choice(os.listdir(imageDir))
            dateTimeStr =  dateTimeObj.strftime("%c")
            print("sending at "+dateTimeStr)
            await channel.send(file=discord.File(imageDir + randPic))
            await asyncio.sleep(nSDelay) #in seconds (1hour=3600)
    else:
        print("not sending at "+dateTimeObj.strftime("%I")+dateTimeObj.strftime("%p"))
        await asyncio.sleep(nSDelay) #in seconds (1hour=3600)
   
def checkNewPosts():
    picExists = False
    for post in posts:
        postIDs = open("captions.txt", "r")
        for postID in postIDs:
            if post == postID:
                picExists = True
        if picExists == False:
            try:
                loader.download_post(post, insAccount)
                with open("captions.txt", "a") as file:
                    file.write(post.shortcode+"\n")
            except:
                print("something went wrong while downloading...")
    client.loop.create_task(randPics())

def main():
    checkNewPosts()

async def list_servers():
    await client.wait_until_ready()
    while not client.is_closed:
        print("Current servers:")
        for server in client.servers:
            print(server.name)
        print("Date and Time: ")
        currentDT = datetime.datetime.now()
        print(currentDT)
        await asyncio.sleep(600)


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

main()
client.loop.create_task(list_servers())
client.run(TOKEN)
