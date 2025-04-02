from flask import request, redirect


def checkCookie() -> str:
  cookie:str = request.cookies.get("name")
  if not cookie:
    return False
  return cookie
