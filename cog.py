import datetime
import discord
import random
import time
from discord.ext import commands


# ゲームには使えないけど便利そうなコマンドはこっち
# ここに含まれてる機能
# 現在日時, 天気, コマンドエイリアスヘルプ
class Etc_utils(commands.Cog, name="その他便利機能"):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    @commands.command(aliases=['t'])
    async def time(self, ctx):
        """
        今の日時を教えるよ！

        それ以上でもそれ以下でもないから言うほど他のコマンドよりは多用しない気はするよねー
        """
        now_dt = datetime.datetime.today()
        now_dt = now_dt.strftime('%Y/%m/%d %H:%M:%S')
        await ctx.send(f'今は{now_dt}だよ！')

    @commands.command(aliases=['a'])
    async def aliases(self, ctx):
        """
        コマンドのエイリアス一覧を表示するよ！

        覚えたら短い文字でコマンドを打てるよ！
        $help <コマンド>でも確認は出来るんだけど、それよりも見やすくしたんだよ！
        """

        msg = """
{0}
エイリアス一覧
$dice => $d
    ・ダイスを振れるよ！
$poll => $p
    ・多数決を取れるよ！
$roulette => $r
    ・ルーレットを回せるよ！
$time => $t
    ・今の日時を教えてあげるよ！
$aliases => $a
    ・今見てるこれを表示してるよ！
{0}
        """.format('```')

        await ctx.send(msg)


# 主にゲームに使えそうなコマンドはこっち
# ここに含まれてる機能
# ダイス, 投票, ルーレット
class Game_utils(commands.Cog, name="主にゲームに使える便利機能"):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    # TRPG形式なダイスを振る
    # コマンドはndm: n=振りたいサイコロの個数, m=サイコロの面の数
    # ex. 1d100 => 100面ダイス1個, 3d6 => 6面ダイス3個
    @commands.command(aliases=['d'])
    async def dice(self, ctx, dice_arg):
        """
        ダイスを振るよー！

        ダイスはTRPGみたく、△d◇の形で振ってもらうよー
        △にはダイスの個数、◇には振るダイスの面を数字で入力してね！
        個数と面を区切るときは"d"を入れ忘れないように気をつけてね？
        """

        upper_dice = dice_arg.upper()

        try:
            d_idx = upper_dice.index("D")
        except ValueError:
            await ctx.send("△d◇の形で入力してくれるかな？△と◇には数字しか入れれないからそこにも気をつけてね！")

        try:
            d_cnt = int(upper_dice[:d_idx])
        except ValueError:
            await ctx.send("ダイスの個数が数字じゃない、もしくはdの前に余計な文字を含んでるみたい…？")

        try:
            await ctx.send(f'{ctx.message.author.name}はダイスを振った！')
            d_face = int(upper_dice[d_idx+1::])
            dice_result = [random.randint(1, d_face) for _ in range(d_cnt)]
            result_items = ', '.join(str(e) for e in dice_result)
            msg = discord.Embed(title="結果",
                                description=sum(dice_result),
                                colour=0x1e90ff)
            msg.add_field(name="内訳", value=result_items)
            await ctx.send(embed=msg)
        except ValueError:
            await ctx.send("ダイスの面が数字じゃない、もしくは余計な文字を含んでるみたい…？")

    # 多数決コマンド
    # 空白で選択肢を区切る
    # 最初に入れたキーワードはお題となり、以下最大10個までお題に関する選択肢を設定できる
    @commands.command(aliases=['p'])
    async def poll(self, ctx, poll_title, *poll_args):
        """
        多数決がとれるよ！

        最初のキーワードはお題になるよ！
        続くキーワード(最大10個)はお題に関する選択肢として設定できるよ！
        """
        poll_num = len(poll_args)

        if poll_num > 10:
            return await ctx.send('ごめんね、作れる選択肢は10個までなんだ… 選択肢の数を減らしてくれると使えるよ！')

        text = ""
        emojis = ["\N{DIGIT ONE}\N{COMBINING ENCLOSING KEYCAP}",
                  "\N{DIGIT TWO}\N{COMBINING ENCLOSING KEYCAP}",
                  "\N{DIGIT THREE}\N{COMBINING ENCLOSING KEYCAP}",
                  "\N{DIGIT FOUR}\N{COMBINING ENCLOSING KEYCAP}",
                  "\N{DIGIT FIVE}\N{COMBINING ENCLOSING KEYCAP}",
                  "\N{DIGIT SIX}\N{COMBINING ENCLOSING KEYCAP}",
                  "\N{DIGIT SEVEN}\N{COMBINING ENCLOSING KEYCAP}",
                  "\N{DIGIT EIGHT}\N{COMBINING ENCLOSING KEYCAP}",
                  "\N{DIGIT NINE}\N{COMBINING ENCLOSING KEYCAP}",
                  "\N{KEYCAP TEN}"]
        for i in range(poll_num):
            text += "{}: {}{}".format(emojis[i], poll_args[i], '\n')
        msg = discord.Embed(title=f"お題: {poll_title}",
                            description=text, colour=0x1e90ff)
        text_msg = await ctx.send(embed=msg)

        for j in range(poll_num):
            await text_msg.add_reaction(emojis[j])

    # ルーレットコマンド
    # 空白で選択肢を区切る
    # 最初に入れた数字は抽選個数
    # 2番めに入れるキーワードはお題
    # 3番目以降のキーワードが抽選対象となる
    @commands.command(aliases=['r'])
    async def roulette(self, ctx, roulette_num, roulette_title,
                       *roulette_args):
        """
        ルーレットを回すよん！

        最初に抽選対象から何個を選びたいか数字を入れてね！
        これが数字じゃないとエラーを返すから気をつけてね！

        数字の次はルーレットのお題のキーワードが入るよ！
        お題以降のキーワードは抽選対象になるよ！
        抽選対象の数が最初に記入した数字より少ないとエラーになるから注意！
        """
        try:
            roulette_num = int(roulette_num)
        except ValueError:
            error_msg = "抽選で選びたい個数がよく分からないことになってるみたい…？数字を見直してみてくれるかな？"
            await ctx.send(error_msg)

        num_args = len(roulette_args)

        if num_args < roulette_num:
            error_msg = "ありゃりゃー…？抽選で選ぶ個数が多くないかな…？"
            return await ctx.send(error_msg)

        roulette_items = ', '.join(str(e) for e in roulette_args)
        result = []
        nums = []
        while len(result) != roulette_num:
            t = random.randint(0, num_args-1)
            print(t)
            if nums.count(t) == 0:
                nums.append(t)
                result.append(roulette_args[t])

        results = ', '.join(str(e) for e in result)
        msg = discord.Embed(title="お題",
                            description=roulette_title,
                            colour=0x1e90ff)
        msg.add_field(name="抽選対象",
                      value='{}{}この中から、{}個選ぶよ！'.format(roulette_items, '\n', roulette_num))
        await ctx.send(embed=msg)

        result_msg = discord.Embed(title='抽選結果',
                                   description=results,
                                   colour=0x1e90ff)
        await ctx.send("抽選中…")
        time.sleep(3)
        await ctx.send(embed=result_msg)


def setup(bot):
    bot.add_cog(Etc_utils(bot))
    bot.add_cog(Game_utils(bot))
