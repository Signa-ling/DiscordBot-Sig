# TOKEN等を消しているので使う場合は適宜置き換えること
# coding: UTF-8
import traceback
from discord.ext import commands


INITIAL_EXTENSIONS = [
    'cog'
]

# tokenは自分の使うbotに合わせて適宜変更する
TOKEN = ''
prefix = '$'


class MyBot(commands.Bot):
    # MyBotのコンストラクタ。

    def __init__(self, command_prefix, help_command):
        # スーパークラスのコンストラクタに値を渡して実行。
        super().__init__(command_prefix, help_command)

        # INITIAL_COGSに格納されている名前から、コグを読み込む。
        # エラーが発生した場合は、エラー内容を表示。
        for cog in INITIAL_EXTENSIONS:
            try:
                self.load_extension(cog)
            except Exception:
                traceback.print_exc()

    # Botの準備完了時に呼び出されるイベント
    async def on_ready(self):
        print('-----')
        print(self.user.name)
        print(self.user.id)
        print('-----')

        # 起動時のコメントを表示するチャンネルID
        # idを入れる場合は''を消してidに置き換える
        channel_id = ''
        if channel_id != '':
            channnel = bot.get_channel(channel_id)
            await channnel.send("やっほー しぐだよ！")


class JapaneseHelpCommand(commands.DefaultHelpCommand):

    def __init__(self):
        super().__init__()
        self.commands_heading = "コマンド:"
        self.no_category = "ヘルプコマンドについて"
        self.command_attrs["help"] = "ぼくができることを教えるよ！"

    def get_ending_note(self):
        return (f"各コマンドの詳細な説明は {prefix}help <コマンド名> で確認できるよ！")


if __name__ == '__main__':
    bot = MyBot(command_prefix=prefix, help_command=JapaneseHelpCommand())
    bot.run(TOKEN)
