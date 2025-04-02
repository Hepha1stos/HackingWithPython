from flask import request, redirect


def checkCookie(redirectPath:str) -> str:
  cookie:str = request.cookies.get("name")
  if not cookie:
    return redirect(redirectPath)
  return cookie