import never_jscore
import execjs

js = """
    a = 'sfaf1s2a3fsf4as6fa'
    console.log(a.substring(2,5))
"""
# ctx2 = execjs.compile(js)
# print(ctx2.call("aaa"))
ctx = never_jscore.Context(enable_extensions=True)

ctx.eval(js)