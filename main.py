import discord
import timeit
import os
import youtube_dl

from discord.ext import commands
from discord.utils import get

client = commands.Bot(command_prefix = '/mt ')
vote_chest = [] #투표함
vote_time = False
# 가사 데이터로 가공
Lyrcis_file = open("HASTA LA VISTA lyrics.txt", "r", encoding="UTF-8")
lyrcis = Lyrcis_file.readlines()
Lyrcis_file.close()


message = []
message_list = []

for i in range(0,len(lyrcis)):


    if lyrcis[i] == "\n":

        pass

    elif lyrcis[i][1] != "x":

        message_list.append(message)
        message = []
        message.append(lyrcis[i].replace("\n", ""))

    else:

        message.append(lyrcis[i][3:].replace("\n", ""))

@client.event
async def on_ready():
    print(client.user.id)
    print("ready")

@client.command()
async def command(ctx):
    await ctx.send("```        ##### 명령어 리스트 #####"
                   "\n\n /mt set [?] : 해당 [?]을 투표목록에 추가합니다."
                   "\n\n /mt clear : 등록된 게임을 초기화 합니다"
                   "\n\n /mt start : 투표가 시작되며 더이상 추가할수 없습니다"
                   "\n\n /mt vote [?] : 해당 [번호] 에  투표합니다."
                   "\n\n /mt check : 투표 결과를 확인합니다."
                   "\n\n /mt musiclist : 음악 리스트를 확인합니다. "
                   "\n\n /mt play [?] : 해당 [번호] 음악을 재생합니다. "
                   "\n\n /mt stop : 음악을 끕니다.```")

@client.command()
async def set(ctx,thing):

    global list

    if not vote_time:
        list.append(thing)
        await ctx.send(f"{thing} 등록 완료")
    else:
        await ctx.send("투표 진행중입니다. 등록할수 없습니다.")


@client.command()
async def start(ctx):

    global vote_time

    vote_time = True


    for i in range(0,len(list)):
        vote_chest.append(0)
        await ctx.send(f"{list[i]} 해당 번호 :  "+ str(i))




@client.command()
async def vote(ctx,vote):

    if 0 <= int(vote) < len(list):
        vote_chest[int(vote)] += 1
        
        print(vote_chest)
        await ctx.message.delete()
        await ctx.send(f"{ctx.message.author} 투표완료")

    else:
        await ctx.send("올바르지 않은 숫자 입니다.")


@client.command()
async def check(ctx):

    global vote_time,list,vote_chest

    for i in range(0,len(list)):

        await ctx.send(f"{list[0]} 의 득표수 : {vote_chest[0]} ")
        del list[0]
        del vote_chest[0]

    vote_time = False

@client.command()
async def clear(ctx):

    global vote_chest,list

    for i in range(0,len(list)):

        del list[0]
        if len(vote_chest) != 0:
            del vote_chest[0]
    else:
        print((ctx.author).status)


@client.command()
async def play(ctx,num):

    channel = ctx.author.voice.channel
    voice = await channel.connect()
    voice.play(discord.FFmpegPCMAudio(options= "-loglevel panic", source="HASTA LA VISTA (Prod. InsideWill).mp3"))
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 0.07
    voice.is_playing()
    print("Play")

    start_time = timeit.default_timer()
    i = 1
    time = 0
    Time = 0
    second_Time = 0

    while True :
        if time >= 80 :

            Time = int(timeit.default_timer() - start_time)
            time = 0
            if Time > 60 :
                second_Time = Time - int(Time / 60) * 60

            else:
                second_Time = Time

        else :

            time += 1

        if int(Time / 60) == int(message_list[i][0][1]) and second_Time == int(message_list[i][0][3:5]):

            await ctx.channel.purge(limit= len(message_list[i-1]))
            for j in message_list[i]:
                if j[0] == "[":
                    await ctx.send(j[6:])
                else:
                    await ctx.send(j)



            i += 1

        else:

            print("noLaging")









client.run("Nzg1NDM3MDUwODUzMzkyNDE0.X831QQ.J4Zy-UwiEXsHlO2QQNqv9kKW9bM")