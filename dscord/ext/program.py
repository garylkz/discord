from discord.ext import commands

import os
from dscord.func import log_proc
from tempfile import NamedTemporaryFile


class Program(commands.Cog):
    class execute:
        def __init__(self, suffix):
            self.suffix = f'.{suffix}'

        def output(self, command, code):
            with NamedTemporaryFile('r+t', suffix=self.suffix) as tp:
                tp.write(code); tp.seek(0)
                return log_proc(command+[tp.name])


    def __init__(self, bot):
        self.bot = bot

    @commands.command('sh')
    async def prgmBash(self, ctx, *cmds):
        for x in log_proc(cmds): await ctx.send(x)

    @commands.command('py')
    async def prgmPython(self, ctx, *, code):
        python = execute('py')
        for log in python.output(code): await ctx.send(log)

    @commands.command('js')
    async def prgmJavascript(self, ctx, *, code):
        with ntf('r+t',suffix='.js') as tp:
            tp.write(code)
            tp.seek(0)
            for x in log_proc(['node', tp.name]): await ctx.send(x)

    @commands.command('java')
    async def prgmJava(self, ctx, *, code):
        with ntf('r+t',suffix='.java') as tp:
            tp.write(code)
            tp.seek(0)
            for x in log_proc(['java', tp.name]): await ctx.send(x)

    @commands.command('r')
    async def prgmR(self, ctx, *, code):
        with ntf('r+t',suffix='.r') as tp:
            tp.write(code)
            tp.seek(0)
            for x in log_proc(['Rscript', tp.name]): await ctx.send(x)


def setup(bot):
    bot.add_cog(Program(bot))