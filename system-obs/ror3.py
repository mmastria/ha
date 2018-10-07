#!/usr/bin/python3

from aiohttp import web

async def index(request):
  return web.Response(text='REST Services - Roll-Off Roof Controller')

async def unpark(request):
  return web.Response(text='0')

async def park(request):
  return web.Response(text='0')

app = web.Application()
#app.router.add_post('/unpark', unpark)
app.router.add_get('/', index)
app.router.add_get('/unpark', unpark)
app.router.add_get('/park', park)

web.run_app(app, port=80)

