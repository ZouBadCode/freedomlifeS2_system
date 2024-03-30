import discord
from discord.ext import commands, tasks
import json
import datetime
from discord import app_commands
import time
import random
import math
import aiohttp
import requests
from discord.ui import Button, View

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix="/", intents=intents)

messages_to_delete = {}




class ApprovalButton(Button):
    def __init__(self, label, style, tag):
        super().__init__(label=label, style=style, custom_id=tag)

    async def callback(self, interaction):
        # 定義按鈕點擊後的行為
        tag = self.custom_id
        if tag.endswith("_approve"):
            url = 'http://localhost:25566/accept-user'
            original_tag = tag[:-8]  # 移除 "_approve"
        elif tag.endswith("_deny"):
            url = 'http://localhost:25566/deny-user'
            original_tag = tag[:-5]   # 移除 "_deny"
        else:
            original_tag = tag  # 如果不符合以上情況，直接使用 tag
        # 從 JSON 檔案讀取數據
        with open('record_data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        if original_tag in data:
            await interaction.response.send_message("正在處理您的請求...", ephemeral=True)
            record_data = data[original_tag]
            # 找到相關的 DiscordUsername
            discord_username = record_data['DiscordUsername']
            
            guild = bot.get_guild(1055876558620995675)
            member = discord.utils.get(guild.members, name=discord_username)

            
            # 遍歷並刪除所有具有相同 DiscordUsername 的條目
            data = {k: v for k, v in data.items() if v['DiscordUsername'] != discord_username}

            # 寫回更新後的數據到 JSON 檔案
            with open('record_data.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            await interaction.channel.purge(limit=10, bulk=True)
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=record_data) as response:
                    if response.status == 200:
                        await interaction.followup.send("請求已成功處理。", ephemeral=True)
                        if member:
                            await send_discord_user_id_to_backend(discord_username, member.id)
                        else:
                            print("can't find")
                    else:
                        await interaction.followup.send("處理請求時出錯。", ephemeral=True)
            
        else:
            await interaction.response.send_message("找不到相關的資料。", ephemeral=True)
# 為了使用按鈕，需要一個包含按鈕的 view
class ApprovalView(View):
    def __init__(self, tag):
        super().__init__(timeout=None)
        self.add_item(ApprovalButton("同意", discord.ButtonStyle.success, f"{tag}_approve"))
        self.add_item(ApprovalButton("否決", discord.ButtonStyle.danger, f"{tag}_deny"))


async def send_discord_user_id_to_backend(discord_username, user_id):
    time.sleep(3)
    url = 'http://localhost:25566/update_discord_user_id'  # 替換成你的後端接收數據的URL
    data = {
        'discordusername': discord_username,
        'discorduserid': user_id
    }
    print(data)
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data) as response:
            if response.status == 200:
                print("User ID updated successfully.")
            else:
                print("Failed to update user ID.")




@bot.tree.command(name="delmes_in_time",description="時間格式:年-月-日 時-分  (不可以用秒，(時)為24進位制")
async def delmes_in_time(interaction: discord.Interaction, message_content: str, timestamp: str):
    # 捕獲用戶資訊和頻道ID
    author_avatar = interaction.user.avatar.url if interaction.user.avatar else None
    author_name = interaction.user.display_name
    channel_id = interaction.channel_id
    current_timestamp_past = datetime.datetime.strptime(timestamp, "%Y-%m-%d %H:%M").timestamp()
    current_timestamp = int(current_timestamp_past)
    message_content_format = message_content.replace("\\n", "\n")
    full_mes = (f"{message_content_format}\n將於<t:{current_timestamp}:f>銷毀")
    # 計算刪除時間
    delete_time = datetime.datetime.strptime(timestamp, "%Y-%m-%d %H:%M")

    # 使用 webhook 發送訊息並獲取訊息ID
    webhook = await interaction.channel.create_webhook(name=author_name)
    sent_message = await webhook.send(content=full_mes, username=author_name, avatar_url=author_avatar, wait=True)
    await webhook.delete()

    # 設置訊息刪除計劃
    messages_to_delete[sent_message.id] = {"delete_time": delete_time, "channel_id": channel_id}

    # 儲存到 JSON 檔案
    with open("messages.json", "w") as file:
        json.dump(messages_to_delete, file, indent=4, default=str)

    # 給予用戶即時回應
    await interaction.response.send_message("訊息將在指定時間被刪除。", ephemeral=True) 

@tasks.loop(seconds=60)
async def check_for_deletion():
    current_time = datetime.datetime.now()
    for message_id, info in list(messages_to_delete.items()):
        if current_time >= info["delete_time"]:
            channel = bot.get_channel(info["channel_id"])
            if channel:
                try:
                    message = await channel.fetch_message(message_id)
                    await message.delete()
                    del messages_to_delete[message_id]

                    # 更新 JSON 檔案
                    with open("messages.json", "w") as file:
                        json.dump(messages_to_delete, file, indent=4, default=str)
                except discord.NotFound:
                    # 如果消息已被刪除或找不到
                    del messages_to_delete[message_id]
                    # 更新 JSON 檔案
                    with open("messages.json", "w") as file:
                        json.dump(messages_to_delete, file, indent=4, default=str)
                except discord.Forbidden:
                    # 如果機器人沒有足夠的權限刪除消息
                    print(f"No permission to delete message in channel {channel.id}")
                except Exception as e:
                    # 處理其他可能的錯誤
                    print(f"An error occurred: {e}")



@bot.tree.command(name="bar",description="為您調制一款伏特加酒品")
async def bartender(interaction: discord.Interaction):
    # 加載 JSON 檔案
    with open('C:/Users/User/Desktop/management_system/backend/discord_bot/wine.json', 'r', encoding='utf-8') as file:
        items = json.load(file)
    
    # 從列表中隨機選擇一個項目
    item = random.choice(items)
    
    # 創建嵌入式訊息
    embed = discord.Embed(title=item["name"], color=0x00ff00)
    image_path = item["path"]
    file = discord.File(image_path, filename="image.png")
    embed.add_field(name="成分", value=item["ing"], inline=False)
    embed.set_image(url="attachment://image.png")
    await interaction.response.send_message(file=file, embed=embed)




@bot.tree.command(name='spreadteam', description='將指定身分組的成員平均分配到指定數量的隊伍中')
async def spreadteam(interaction: discord.Interaction, role_name: str, team_count: int):
    guild = interaction.guild

    if guild is None:
        await interaction.response.send_message("此命令無法在私訊中使用。")
        return

    role = discord.utils.get(guild.roles, name=role_name)
    if role is None:
        await interaction.response.send_message(f"找不到身分組: {role_name}")
        return

    members = [member for member in role.members]
    member_count = len(members)

    if member_count == 0:
        await interaction.response.send_message(f"身分組 {role_name} 沒有成員。")
        return

    team_size = math.ceil(member_count / team_count)
    teams = [members[i * team_size:(i + 1) * team_size] for i in range(team_count)]

    response = "分隊結果：\n"
    for i, team in enumerate(teams, start=1):
        team_members = ', '.join([member.mention for member in team])
        response += f"隊伍 {i}: {team_members}\n"

    await interaction.response.send_message(response)



async def delete_messages(channel):
    async for message in channel.history(limit=100):
        try:
            await message.delete()
            print(f"Deleted message from {message.author.name}")
        except discord.errors.Forbidden:
            print("I do not have permissions to delete messages in this channel.")
        except discord.errors.HTTPException as e:
            print(f"Failed to delete message: {e}")

@tasks.loop(hours=1)
async def fetch_form_count():
    channel = bot.get_channel(1217271085372936252)  # 替換 YOUR_CHANNEL_ID 為實際的聊天室 ID
    if channel:
        await delete_messages(channel)
        async with aiohttp.ClientSession() as session:
            async with session.get('http://localhost:25566/form-count-discord-bot') as response:
                if response.status == 200:
                    data = await response.json()
                    total_count = data.get('total_count', 0)
                    await channel.send(f'目前待審核表單數：{total_count}，每小時更新\n 表單審核連結:')
                else:
                    await channel.send('無法獲取待審核表單數量。')

@tasks.loop(hours=12)
async def fetch_member_info():
    channel = bot.get_channel(1216768355533590568)
    if channel:
        # 使用異步列表推導來獲取頻道訊息列表
        messages = [message async for message in channel.history(limit=None)]
        # 計算訊息數量
        messages_count = len(messages)
        await channel.purge(limit= messages_count, bulk=True)
        async with aiohttp.ClientSession() as session:
            async with session.get('http://localhost:25566/show-member-discord') as response:
                if response.status == 200:
                    datas = await response.json()
                    print(datas)
                    for data in datas:
                        embed = discord.Embed(title="成員", color=0x00ff00)
                        for key,value in data.items():
                            embed.add_field(name=key, value=value, inline=False)
                        await channel.send(embed=embed)
                else:
                    await channel.send("有內鬼，伺服器炸了，而且是王炸，請聯繫工程師")


@bot.event
async def on_member_join(member):
    channel = bot.get_channel(1216768357626544279)
    if channel:
        async with aiohttp.ClientSession() as session:
            async with session.get(f'http://localhost:25566//check-join-user-state?discordusername={member}') as response:
                if response.status == 200:
                    data = await response.json()
    try:
        if data == "2":
            await member.send('您尚未填寫表單')
        elif data == "1":
            await member.send("您已通過審核，本次為您安排的遊玩時間為")
            await send_discord_user_id_to_backend(member.name, member.id)
        elif data == "4":
            await member.send("很抱歉，您並未通過審核，您可以再次填寫表單，申請加入")
        elif data == "3":
            await member.send("您的表單尚未審核，系統已向管理員發出審核提醒")
            admin_user_id = 1042927270601429033  # 替換為特定用戶的ID
            admin_channel = bot.get_channel(1216768357626544279)  # 替換為需要發送訊息的頻道ID
            if admin_channel:
                await admin_channel.send(f'<@{admin_user_id}>\n{member.mention}尚未完成審核。')
                await query_discord_embed_card(member.name, admin_channel)
    except Exception as e:
        print("無法發送訊息")               
    print(f'{member} 加入了伺服器。')



async def query_discord_embed_card(discord_username, admin_channel):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'http://localhost:25566/query_discord_embed_card?discord_username={discord_username}') as response:
            if response.status == 200:
                records = await response.json()
                data_to_save = {}
                for record in records:
                    tag = record.get('Tag')
                    if tag:
                        data_to_save[tag] = {
                            'Tag': tag,
                            'DiscordUsername': record.get('DiscordUsername'),
                            'dataType': record.get('dataType')
                        }
                with open('record_data.json', 'w', encoding='utf-8') as f:
                    json.dump(data_to_save, f, ensure_ascii=False, indent=4)

                for record in records:
                    embed = discord.Embed(title=f"資料類型：{record['Type']}", color=0x00ff00)
                    for key, value in record.items():
                        embed.add_field(name=key, value=value, inline=False)
                    tag = record.get('Tag')
                    if tag:
                        view = ApprovalView(tag)
                        await admin_channel.send(embed=embed, view=view)
            else:
                await admin_channel.send("查無此人的資料。")











@bot.command()
async def query(ctx, discord_username: str):
    response = requests.get(f'http://localhost:25566/query_discord_embed_card?discord_username={discord_username}')
    if response.status_code == 200:
        records = response.json()
        data_to_save = {}
        for record in records:
            tag = record.get('Tag')
            if tag:
                # 存储有限的字段到 data_to_save
                data_to_save[tag] = {
                    'Tag': tag,
                    'DiscordUsername': record.get('DiscordUsername'),
                    'dataType': record.get('dataType')
                }
        with open('record_data.json', 'w', encoding='utf-8') as f:
            json.dump(data_to_save, f, ensure_ascii=False, indent=4)

        for record in records:
            embed = discord.Embed(title=f"資料類型：{record['Type']}", color=0x00ff00)
            for key, value in record.items():
                embed.add_field(name=key, value=value, inline=False)
            tag = record.get('Tag')
            if tag:
                view = ApprovalView(tag)
                await ctx.send(embed=embed, view=view)
    else:
        await ctx.send("查無此人的資料。")





@bot.tree.command(name="clear", description="刪訊息(請不要嘗試衝擊上限，每次刪100條)")
async def clearmsg(interaction: discord.Interaction, number_of_messages: int):
    # 首先確認交互操作並使其處於等待狀態
    await interaction.response.defer(ephemeral=True)

    # 執行刪除訊息的操作
    await interaction.channel.purge(limit=number_of_messages, bulk=True)

    # 在刪除完成後發送最終回應
    await interaction.followup.send("已完成刪除", ephemeral=True)

    
# 當機器人完成啟動並準備好時，會調用這個事件
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    if not check_for_deletion.is_running():
        check_for_deletion.start()  # 只有當任務沒有在運行時才啟動
    #fetch_form_count.start()   
    fetch_member_info.start()
    slash = await bot.tree.sync()
    print(f"目前登入身份 --> {bot.user}")
    print(f"載入 {len(slash)} 個斜線指令")
# 在這裡插入您的Token
bot.run('MTIwMTU2NTAwMDg1NTIwODA1Ng.GzEVXQ.ZpOpGbOJoWUzxRlGRDGvH7gm4nUcxry-fMFr4I')