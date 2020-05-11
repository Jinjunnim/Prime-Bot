import discord
import openpyxl
import os

clinet = discord.Client()


@clinet.event
async def on_ready():
    print(clinet.user.id)
    print("ready")
    game = discord.Game("메이플")
    await clinet.change_presence(status=discord.Status.online, activity=game)


@clinet.event
async def on_message(message):
    if message.content.startswith("안녕"):
        await message.channel.send("반가워")


    if message.content.startswith("/사진"):
        pic = message.content.split(" ")[1]
        await message.channel.send(file=discord.File(pic))


    if message.content.startswith("/메가폰"):
        channel = message.content[5:23]
        msg = message.content[24:]
        await clinet.get_channel(int(channel)).send(msg)

    if message.content.startswith("/확"):
        channel = message.content[3:21]
        msg = message.content[22:]
        await clinet.get_channel(int(channel)).send(msg)

    if message.content.startswith("/귓속말"):
        author = message.guild.get_member(int(message.content[5:23]))
        msg = message.content[24:]
        await author.send(msg)

    if message.content.startswith("/귓"):
        author = message.guild.get_member(int(message.content[3:21]))
        msg = message.content[22:]
        await author.send(msg)


    if message.content.startswith("/뮤트"):
        author = message.guild.get_member(int(message.content[4:22]))
        role = discord.utils.get(message.guild.roles, name="블랙")
        await author.add_roles(role)

    if message.content.startswith("/언뮤트"):
        author = message.guild.get_member(int(message.content[5:23]))
        role = discord.utils.get(message.guild.roles, name="블랙")
        await author.remove_roles(role)


    if message.content.startswith("/경고"):
        author = message.guild.get_member(int(message.content[4:22]))
        file = openpyxl.load_workbook("경고.xlsx")
        sheet = file.active
        i = 1
        while True:
            if sheet["A" + str(i)].value == str(author.id):
                sheet["B" + str(i)].value = int(sheet["B" + str(i)].value) + 1
                file.save("경고.xlsx")
                if sheet["B" + str(i)].value == 3:
                    await message.guild.ban(author)
                    await message.channel.send("경고 3회 누적입니다. 서버에서 추방됩니다.")
                else:
                    await message.channel.send("경고를 1회 받았습니다.")
                break
            if sheet["A" + str(i)].value == None:
                sheet["A" + str(i)].value = str(author.id)
                sheet["B" + str(i)].value = 1
                file.save("경고.xlsx")
                await message.channel.send("경고를 1회 받았습니다.")
                break
            i += 1


access_token = os.environ["BOT_TOKEN"]            
clinet.run(access_token)

