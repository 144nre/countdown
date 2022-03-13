from http.server import BaseHTTPRequestHandler, HTTPServer
import http.cookies
from math import prod
import time
import datetime
from tkinter import W
from urllib.parse import urlparse, parse_qs
import json
import traceback
import socket
import requests
import re
import urllib
import math
import uuid

def capitalize(str):
    return re.sub("(?:[0-9A-Za-z])\S*", lambda e: e[0][0].upper() + e[0][1:], str)

session = requests.Session()
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
           'X-Requested-With': 'OnlineShopping.WebApp'}

hostName = "0.0.0.0"
serverPort = 18081

host = "127.0.0.1"
port = 8889

def recvAll(s):
    data = ""
    newData = s.recv(1024)
    while newData:
        data += newData.decode()
        newData = s.recv(1024)
    return data
    

def send(msg):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(("16e0050be90d8f4eb098a24679d71ab5$%s" % (msg)).encode())
        data = recvAll(s)
        return data

def do_ERROR(self):
    self.send_response(404)
    self.send_header("Content-type", "text/html")
    self.end_headers()
    self.write(b"<html>")
    self.write(b"<head>")
    self.write(b"<title>Shopping List</title>")
    self.write(b"</head>")
    self.write(b"<body>")
    self.write(b"<center>")
    self.write(b"<h1>Error: Something went Wrong.</h1>")
    self.write(b"</center>")
    self.write(b"</body>")
    self.write(b"</html>")

class MyServer(BaseHTTPRequestHandler):
    def write(self, msg):
        self.wfile.write(msg + b"\n")
    def do_GET(self):
        cookie = self.headers.get('Cookie')
        cookies = http.cookies.SimpleCookie(cookie)
        path = urlparse(self.path).path
        query = parse_qs(urlparse(self.path).query)
        if path in ["/", "/index", "/index.html"]:
            if "listId" not in cookies:
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.write(b"<html>")
                self.write(b"<head>")
                self.write(b'<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=0">')
                self.write(b"<title>Shopping List Id</title>")
                self.write(b'<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">')
                self.write(b"<style>")
                self.write(b"""
                                    body {
                                        margin-left: 100px;
                                        margin-right: 100px;
                                        margin-top: 50px;
                                        margin-bottom: 50px;
                                    }
                                    
                                    .title {
                                        margin-bottom: 35px;
                                    }

                                    br {
                                        display: block;
                                        content: "";
                                        margin: 10px 0;
                                    }

                                    .listId {
                                        text-align: center;
                                        width: 130px;
                                        box-sizing: border-box;
                                        border: 2px solid #ccc;
                                        border-radius: 4px;
                                        font-size: 16px;
                                        padding: 12px 20px 12px 20px;
                                        transition: width 0.4s ease-in-out;
                                    }

                                    .listId:focus {
                                        width: 100%;    
                                    }

                                    .changeId {
                                        width: 130px;
                                        background-color: white;
                                        color: black;
                                        border: 2px solid #555555;
                                        border-radius: 6px;
                                        padding: 16px 32px;
                                        text-align: center;
                                        text-decoration: none;
                                        display: inline-block;
                                        font-size: 16px;
                                        margin: 4px 2px;
                                        transition-duration: 0.4s;
                                    }
                                    
                                    .changeId:hover {
                                        cursor: pointer;
                                        background-color: #555555;
                                        color: white;
                                    }""")
                self.write(b"</style>")
                self.write(b"</head>")
                self.write(b"<body>")
                self.write(b"<center>")
                self.write(b'<h1 class="title">Enter Shopping List Id</h1>')
                self.write(b"</br>")
                self.write(b'<form action="%s" method="post">' % (path.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&#39;').encode()))
                self.write(b'<input type="text" class="listId" name="listId" placeholder="List Id..."><br/>')
                self.write(b'<br/>')
                self.write(b'<input type="submit" value="Submit" class="changeId">')
                self.write(b"</form>")
                self.write(b"</center>")
                self.write(b"</body>")
                self.write(b"</html>")
            else:
                self.send_response(301)
                self.send_header('Location', '/list')
                self.end_headers()
        elif path in ["/list", "/list.html"]:
            if "listId" not in cookies:
                self.send_response(301)
                self.send_header('Location', '/')
                self.end_headers()
                return
            listId = cookies["listId"].value
            products = json.loads(send('{"%s":"view"}' % listId))
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.write(b"<html>")
            self.write(b"<head>")
            self.write(b'<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=0">')
            self.write(b"<title>Shopping List</title>")
            self.write(b'<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">')
            self.write(b"<style>")
            self.write(b"""
                                body {
                                    margin-left: 100px;
                                    margin-right: 100px;
                                    margin-top: 50px;
                                    margin-bottom: 50px;
                                }

                                h1 {
                                    font-size: 3em;
                                }

                                h2 {
                                    font-size: 2.2em;
                                }

                                .productImage {
                                    width: 200px;
                                    height: 200px;
                                }

                                .searchBtn {
                                    padding: 0px;
                                    width: 80px;
                                    height: 38px;
                                    background-color: white;
                                    color: #4CAF50;
                                    border: 2px solid #4CAF50;
                                    border-radius: 6px;
                                    text-align: center;
                                    text-decoration: none;
                                    display: inline-block;
                                    font-size: 16px;
                                    margin: 4px 2px;
                                    transition-duration: 0.4s;
                                    cursor: pointer;
                                }

                                .searchBtn:hover {
                                    background-color: #4CAF50;
                                    color: white;
                                }

                                .customBtn {
                                    padding: 0px;
                                    width: 90px;
                                    height: 38px;
                                    background-color: white;
                                    color: #4CAF50;
                                    border: 2px solid #4CAF50;
                                    border-radius: 6px;
                                    text-align: center;
                                    text-decoration: none;
                                    display: inline-block;
                                    font-size: 16px;
                                    margin: 4px 2px;
                                    transition-duration: 0.4s;
                                    cursor: pointer;
                                }

                                .customBtn:hover {
                                    background-color: #4CAF50;
                                    color: white;
                                }
                                
                                .quantityBtn {
                                    padding: 0px;
                                    width: 38px;
                                    height: 38px;
                                    background-color: white;
                                    color: #4CAF50;
                                    border: 2px solid #4CAF50;
                                    border-radius: 6px;
                                    text-align: center;
                                    text-decoration: none;
                                    display: inline-block;
                                    font-size: 16px;
                                    margin: 4px 2px;
                                    transition-duration: 0.4s;
                                    cursor: pointer;
                                }
                                
                                .quantityBtn:hover {
                                    background-color: #4CAF50;
                                    color: white;
                                }

                                .deleteBtn {
                                    padding: 0px;
                                    width: 38px;
                                    height: 38px;
                                    background-color: white;
                                    color: #f44336;
                                    border: 2px solid #f44336;
                                    border-radius: 6px;
                                    text-align: center;
                                    text-decoration: none;
                                    display: inline-block;
                                    font-size: 16px;
                                    margin: 4px 2px;
                                    transition-duration: 0.4s;
                                    cursor: pointer;
                                }
                                
                                .deleteBtn:hover {
                                    background-color: #f44336;
                                    color: white;
                                }
                                
                                .product {
                                    overflow: hidden;
                                    margin: 10px;
                                    padding: 20px;
                                    border-radius: 10px;
                                    border: 1px solid #555555;
                                    min-width: 350px;
                                    max-width: 650px;
                                }
                                
                                .products {
                                    padding: 100px;
                                }
                                
                                .handle-counter {
                                    overflow:hidden;
                                    display: flex;
                                    align-items: center;
                                    justify-content: center;
                                }

                                .deleteForm {
                                    display: flex;
                                    margin: 0;
                                }

                                .quantityForm {
                                    margin: 0;
                                }
                                
                                .counterBtn, #counter {
                                    text-align: center;
                                }

                                .counterBtn {
                                    width: 38px;
                                    height: 38px;
                                    float: left;
                                    background-color: #4CAF50;
                                    padding: 6px 12px;
                                    border: 1px solid transparent;
                                    color: white;
                                    transition-duration: 0.4s;
                                }

                                .counterBtn:disabled, .counterBtn:disabled:hover {
                                    background-color: darkgrey;
                                    cursor: not-allowed;
                                }

                                .counterBtn:hover {
                                    background-color: #419544;
                                }
                                
                                .titleInput {
                                    min-width: 100px;
                                    border: 1px solid #989898;
                                    border-radius: 3px;
                                    background-image: url('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADAAAAAwCAQAAAD9CzEMAAAAp0lEQVRYw+3SQQrCMBRF0QtZSLuWgrspdO4qdBHZh+BCsociDv0Ok9pmIv+Bwn+Zn0tCIBb7hQ3ceHAlafiRgmEYWZGovCSx5QWJ+YMXJM4HiYvP40zdxOrBF56cOom7B29YJ1EYfPjjRGH04/cJd36bmD35zMJrl3DkE7A0t5j8+URufo7r4wQffPDB/zWPmkfN14CIrwERXwPtceRR86h51Hws9t3exfxsR4kLnvYAAAAASUVORK5CYII=');
                                    background-size: 21px 21px;
                                    background-position: 10px 10px; 
                                    background-repeat: no-repeat;
                                    padding-top: 6px;
                                    padding-bottom: 6px;
                                    padding-left: 40px;
                                }

                                .titleInputText {
                                    font-size: 18pt;
                                }

                                .customTitleInput {
                                    min-width: 100px;
                                    border: 1px solid #989898;
                                    border-radius: 3px;
                                    background-image: url('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADAAAAAwCAQAAAD9CzEMAAAAp0lEQVRYw+3SQQrCMBRF0QtZSLuWgrspdO4qdBHZh+BCsociDv0Ok9pmIv+Bwn+Zn0tCIBb7hQ3ceHAlafiRgmEYWZGovCSx5QWJ+YMXJM4HiYvP40zdxOrBF56cOom7B29YJ1EYfPjjRGH04/cJd36bmD35zMJrl3DkE7A0t5j8+URufo7r4wQffPDB/zWPmkfN14CIrwERXwPtceRR86h51Hws9t3exfxsR4kLnvYAAAAASUVORK5CYII=');
                                    background-size: 21px 21px;
                                    background-position: 10px 10px; 
                                    background-repeat: no-repeat;
                                    padding-top: 6px;
                                    padding-bottom: 6px;
                                    padding-left: 40px;
                                }

                                .customTitleInputText {
                                    font-size: 18pt;
                                }

                                .customCounter {
                                    float: left;
                                    width: 75px;
                                    text-align: center;
                                    border-width: 1px;
                                    border-left: none;
                                    border-right: none;
                                    padding: 6px 12px;
                                    color: #555;
                                    background-color: white;
                                    border: 1px solid #ccc;
                                }
                                
                                .customCounter:focus {
                                    outline: none;
                                }
                                
                                .customCounter::-webkit-outer-spin-button, .customCounter::-webkit-inner-spin-button {
                                    -webkit-appearance: none;
                                    margin: 0;
                                }
                                
                                .customCounter {
                                    -moz-appearance: textfield;
                                }
                                
                                .quantityCounter {
                                    float: left;
                                    width: 75px;
                                    text-align: center;
                                    border-width: 1px;
                                    border-left: none;
                                    border-right: none;
                                    padding: 6px 12px;
                                    color: #555;
                                    background-color: white;
                                    border: 1px solid #ccc;
                                }
                                
                                .quantityCounter:focus {
                                    outline: none;
                                }
                                
                                .quantityCounter::-webkit-outer-spin-button, .quantityCounter::-webkit-inner-spin-button {
                                    -webkit-appearance: none;
                                    margin: 0;
                                }
                                
                                .quantityCounter {
                                    -moz-appearance: textfield;
                                }

                                .searchBtn {
                                    padding: 0px;
                                    width: 100px;
                                    height: 38px;
                                    top: 10px;
                                    left: 10px;
                                    position: absolute;
                                    background-color: white;
                                    color: #4CAF50;
                                    border: 2px solid #4CAF50;
                                    border-radius: 6px;
                                    text-align: center;
                                    text-decoration: none;
                                    display: inline-block;
                                    font-size: 16px;
                                    margin: 4px 2px;
                                    transition-duration: 0.4s;
                                    cursor: pointer;
                                }
                                
                                .searchBtn:hover {
                                    background-color: #4CAF50;
                                    color: white;
                                }

                                #clearListForm {
                                    display: inline;
                                }

                                .clearListBtn {
                                    padding: 0px;
                                    width: 100px;
                                    height: 38px;
                                    background-color: white;
                                    color: #f44336;
                                    border: 2px solid #f44336;
                                    border-radius: 6px;
                                    text-align: center;
                                    text-decoration: none;
                                    display: inline-block;
                                    font-size: 16px;
                                    margin: 4px 2px;
                                    transition-duration: 0.4s;
                                    cursor: pointer;
                                }
                                
                                .clearListBtn:hover {
                                    background-color: #f44336;
                                    color: white;
                                }

                                .clearIdBtn {
                                    padding: 0px;
                                    width: 100px;
                                    height: 38px;
                                    top: 10px;
                                    right: 10px;
                                    position: absolute;
                                    background-color: white;
                                    color: #f44336;
                                    border: 2px solid #f44336;
                                    border-radius: 6px;
                                    text-align: center;
                                    text-decoration: none;
                                    display: inline-block;
                                    font-size: 16px;
                                    margin: 4px 2px;
                                    transition-duration: 0.4s;
                                    cursor: pointer;
                                }
                                
                                .clearIdBtn:hover {
                                    background-color: #f44336;
                                    color: white;
                                }
                                
                                .modal {
                                    display: none;
                                    position: fixed;
                                    z-index: 1;
                                    padding-top: 10%;
                                    left: 0;
                                    top: 0;
                                    width: 100%;
                                    height: 100%
                                    overflow: auto;
                                    background-color: rgb(0, 0, 0);
                                    background-color: rgba(0, 0, 0, 0.4);
                                }
                                
                                .modal-content {
                                    position: relative;
                                    background-color: #fefefe;
                                    margin: auto;
                                    padding: 0;
                                    border: 1px solid #888;
                                    border-radius: 10px;
                                    width: 50%;
                                    height: 20%;
                                    box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
                                    -webkit-animation-name: animatetop;
                                    -webkit-animation-duration: 0.4s;
                                    animation-name: animatetop;
                                    animation-duration: 0.4s;
                                }

                                .custom-modal-content {
                                    position: relative;
                                    background-color: #fefefe;
                                    margin: auto;
                                    padding: 0;
                                    border: 1px solid #888;
                                    border-radius: 10px;
                                    width: 500px;
                                    height: 550px;
                                    box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
                                    -webkit-animation-name: animatetop;
                                    -webkit-animation-duration: 0.4s;
                                    animation-name: animatetop;
                                    animation-duration: 0.4s;
                                }
                                
                                @-webkit-keyframes animatetop {
                                    from {top:-300px; opacity:0} 
                                    to {top:0; opacity:1}
                                }

                                @keyframes animatetop {
                                    from {top:-300px; opacity:0}
                                    to {top:0; opacity:1}
                                }
                                
                                .errorClose {
                                    color: #f44336;
                                    z-index: 1;
                                    font-size: 28px;
                                    font-weight: bold;
                                    position: absolute;
                                    top: 10px;
                                    right: 20px;
                                    transition-duration: 0.2s;

                                    -webkit-touch-callout: none;
                                    -webkit-user-select: none;
                                    -khtml-user-select: none;
                                    -moz-user-select: none;
                                    -ms-user-select: none;
                                    user-select: none;
                                }

                                .customClose:hover, .customClose:focus {
                                    color: #ab2f26;
                                    text-decoration: none;
                                    cursor: pointer;
                                    transition-duration: 0.2;
                                }

                                .customClose {
                                    color: #f44336;
                                    z-index: 1;
                                    font-size: 28px;
                                    font-weight: bold;
                                    position: absolute;
                                    top: 10px;
                                    right: 20px;
                                    transition-duration: 0.2s;

                                    -webkit-touch-callout: none;
                                    -webkit-user-select: none;
                                    -khtml-user-select: none;
                                    -moz-user-select: none;
                                    -ms-user-select: none;
                                    user-select: none;
                                }

                                .customClose:hover, .customClose:focus {
                                    color: #ab2f26;
                                    text-decoration: none;
                                    cursor: pointer;
                                    transition-duration: 0.2;
                                }
                                
                                .modal-body {
                                    width: 100%;
                                    height: 100%;
                                    display: flex;
                                    align-items: center;
                                    justify-content: center;
                                }
                                
                                @-webkit-keyframes customFadein {
                                    from {bottom: 0; opacity: 0;}
                                    to {bottom: 30px; opacity: 1;}
                                }

                                @keyframes customFadein {
                                    from {bottom: 0; opacity: 0;}
                                    to {bottom: 30px; opacity: 1;}
                                }

                                @-webkit-keyframes customFadeout {
                                    from {bottom: 30px; opacity: 1;}
                                    to {bottom: 0; opacity: 0;}
                                }

                                @keyframes customFadeout {
                                    from {bottom: 30px; opacity: 1;}
                                    to {bottom: 0; opacity: 0;}
                                }
                                
                                #customError {
                                    visibility: hidden;
                                }

                                #customError.show {
                                    visibility: visible;
                                    -webkit-animation: customFadein 0.5s, customFadeout 0.5s 2.5s;
                                    animation: customFadein 0.5s, customFadeout 0.5s 2.5s;
                                }""")
            self.write(b"</style>")
            self.write(b"</head>")
            self.write(b"<body>")
            self.write(b'<a href="/search"><input class="searchBtn" value="Search" type="button"></a>')
            self.write(b'<form id="clearIdForm" action="%s" method="post">' % (path.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&#39;').encode()))
            self.write(b'<input name="clearId" value="1" type="hidden">')
            self.write(b'<input class="clearIdBtn" value="Clear Id" type="submit">')
            self.write(b"</form>")
            self.write(b"<center>")
            self.write(b'<h1>Shopping List</h1>')
            self.write(b"<br/>")
            self.write(b'<a href="/search"><input type="button" class="searchBtn" value="Search"></a>')
            self.write(b'<form id="clearListForm" action="%s" method="post">' % (path.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&#39;').encode()))
            self.write(b'<input name="clearList" value="1" type="hidden">')
            self.write(b'<input name="listId" value="%s" type="hidden">' % (listId.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&#39;').encode()))
            self.write(b'<input class="clearListBtn" value="Clear List" type="submit">')
            self.write(b"</form>")
            # self.write(b"<span>&nbsp;&nbsp;</span>")
            self.write(b'<input type="button" class="customBtn" onclick="document.getElementById(\'customModal\').style.display = \'block\'" value="+Custom">')
            self.write(b"<br/>")
            self.write(b'<div id="customModal" class="modal">')
            self.write(b'<div class="custom-modal-content">')
            self.write(b'<span class="customClose" onclick="document.getElementById(\'customModal\').style.display = \'none\'">&times;</span>')
            self.write(b'<div class="modal-body">')
            self.write(b'<center>')
            self.write(b'<form id="deleteForm" action="%s" method="post">' % (path.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&#39;').encode()))
            self.write(b'<input type="text" name="name" class="customTitleInput customTitleInputText h3" onload="adjustWidthOfInput(this)" oninput="adjustWidthOfInput(this)" value="" >')
            self.write(b"<br/>")
            self.write(b"<h6>Notes:</h6>")
            self.write(b'<textarea name="notes" class="productImage"></textarea>')
            self.write(b"<br/>")
            self.write(b"<br/>")
            self.write(b'<div class="handle-counter">')
            self.write(b'<button type="button" onclick="counter = document.getElementsByClassName(\'customCounter\')[0]; if (counter.value) { counter.value = (parseInt(counter.value) - 1).toString(); } else { counter.value = \'-1\' }" class="counterBtn">-</button>')
            self.write(b'<input type="number" name="customCounter" class="customCounter" min="1" max="20" value="1" required>')
            self.write(b'<input type="hidden" name="listId" value="%s" required>' % (listId.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&#39;').encode()))
            self.write(b'<input type="hidden" name="customItem" value="1" required>')
            self.write(b'<button type="button" onclick="counter = document.getElementsByClassName(\'customCounter\')[0]; if (counter.value) { counter.value = (parseInt(counter.value) + 1).toString(); } else { counter.value = \'1\' }" class="counterBtn">+</button>')
            self.write(b"</div>")
            self.write(b"<br/>")
            self.write(b'<input type="button" value="Add" onclick="changeCustomValidity()" class="customBtn">')
            self.write(b'</form>')
            self.write(b"<br/>")
            self.write(b'<h4 id="customError"></h4>')
            self.write(b'</center>')
            self.write(b'</div>')
            self.write(b'</div>')
            self.write(b'</div>')
            self.write(b'<script>')
            self.write(b'customModal = document.getElementById("customModal");')
            self.write(b'window.onclick = function(event) {')
            self.write(b'     if (event.target == customModal) {')
            self.write(b'         errorModal.style.display = "none";')
            self.write(b'     }')
            self.write(b'}')
            self.write(b'function changeCustomValidity() {')
            self.write(b'     counter = document.getElementsByClassName("customCounter")[0];')
            self.write(b'     title = document.getElementsByClassName("customTitleInput")[0];')
            self.write(b'     errorMsg = document.getElementById("customError");')
            self.write(b'     if (!counter.checkValidity()) {')
            self.write(b'          errorMsg.innerHTML = counter.validationMessage;')
            self.write(b'          errorMsg.className = "show";')
            self.write(b'          setTimeout(function() { errorMsg.className = errorMsg.className.replace("show", ""); }, 3000);')
            self.write(b'     } else if (title.value === "") {')
            self.write(b'          errorMsg.innerHTML = "Value required for name.";')
            self.write(b'          errorMsg.className = "show";')
            self.write(b'          setTimeout(function() { errorMsg.className = errorMsg.className.replace("show", ""); }, 3000);')
            self.write(b'     } else {')
            self.write(b'         form = document.getElementById("deleteForm");')
            self.write(b'         form.submit()')
            self.write(b'     }')
            self.write(b'}')
            self.write(b"function getWidthOfInput(input) {")
            self.write(b'    var tmp = document.createElement("span");')
            self.write(b'    tmp.className = "titleInputText h3";')
            self.write(b"    tmp.innerHTML = input.value.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/ /g, '&nbsp;');")
            self.write(b"    document.body.appendChild(tmp);")
            self.write(b"    var width = tmp.getBoundingClientRect().width;")
            self.write(b"    document.body.removeChild(tmp);")
            self.write(b"    return width;")
            self.write(b"}")
            self.write(b"function adjustWidthOfInput(input) {")
            self.write(b'    input.style.width = "100%";')
            self.write(b'    var maxWidth = input.getBoundingClientRect().width;')
            self.write(b"    var newWidth = getWidthOfInput(input) + 48;")
            self.write(b"    if (newWidth > maxWidth) {")
            self.write(b"        newWidth = maxWidth;")
            self.write(b"    }")
            self.write(b'    input.style.width = newWidth + "px";')
            self.write(b"}")
            self.write(b"adjustWidthOfInput(document.getElementsByClassName('customTitleInput')[0])")
            self.write(b"</script>")
            self.write(b'<h2>Items: %d</h2>' % (len(products)))
            if not products:
                self.write(b"<h2 class='title'>No Items in List. Add using search function.</h1>")
            else:
                self.write(b'<div class="row justify-content-center">')
                for i, product in enumerate(products):
                    if products[product]["type"] == "product":
                        self.write(b'<div class="col-sm product" name="%s">' % (products[product]["id"].replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&#39;').encode()))
                        self.write(b"<h3>%s</h3>" % (products[product]["name"].replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&#39;').encode()))
                        self.write(b"<br/>")
                        self.write(b'<center><img class="productImage" src="%s" /></center>' % (products[product]["images"][0]["big"].replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&#39;').encode()))
                        self.write(b"<br/>")
                        self.write(b"<h5>Sale Price: $%.2f</h5>" % (products[product]["salePrice"]))
                        self.write(b'<br/>')
                        self.write(b'<form id="deleteForm%d" class="deleteForm" action="%s" method="post">' % (i, path.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&#39;').encode()))
                        self.write(b'<input type="hidden" name="listId" value="%s" required>' % (listId.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&#39;').encode()))
                        self.write(b'<input type="hidden" name="id" value="%s" required>' % (products[product]["id"].replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&#39;').encode()))
                        self.write(b'<input type="hidden" name="delete" value="1" required>')
                        self.write(b"</form>")
                        self.write(b'<form class="quantityForm" action="%s" method="post">' % (path.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&#39;').encode()))
                        self.write(b'<div class="handle-counter">')
                        self.write(b'<input type="submit" value="&#128711;" class="deleteBtn" form="deleteForm%d">' % (i))
                        self.write(b'<span>&nbsp;&nbsp;</span>')
                        self.write(b'<button type="button" onclick="counter = document.getElementsByClassName(\'quantityCounter\')[%d]; if (counter.value) { counter.value = (parseInt(counter.value) - 1).toString(); } else { counter.value = \'-1\' }" class="counterBtn">-</button>' % (i))
                        self.write(b'<input type="number" name="quantityCounter" class="quantityCounter" min="0" max="20" value="%d" required>' % (products[product]["quantity"]))
                        self.write(b'<input type="hidden" name="originalQuantity" value="%d" required>' % (products[product]["quantity"]))
                        self.write(b'<input type="hidden" name="listId" value="%s" required>' % (listId.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&#39;').encode()))
                        self.write(b'<input type="hidden" name="id" value="%s" required>' % (products[product]["id"].replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&#39;').encode()))
                        self.write(b'<input type="hidden" name="name" class="titleInputText" value="%s" required>' % (products[product]["name"].replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&#39;').encode()))
                        self.write(b'<input type="hidden" name="productType" value="%s" required>' % (products[product]["type"].replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&#39;').encode()))
                        self.write(b'<button type="button" onclick="counter = document.getElementsByClassName(\'quantityCounter\')[%d]; if (counter.value) { counter.value = (parseInt(counter.value) + 1).toString(); } else { counter.value = \'1\' }" class="counterBtn">+</button>' % (i))
                        self.write(b'<span>&nbsp;&nbsp;</span>')
                        self.write(b'<input type="button" value="&check;" onclick="changeValidity(%d)" class="quantityBtn">' % (i))
                        self.write(b"</div>")
                        self.write(b'</form>')
                        self.write(b'<br/>')
                        self.write(b"<h5>Aisle Name: %s</h5>" % (products[product]["aisle"]["name"].replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&#39;').encode()))
                        self.write(b"</div>")
                        self.write(b"<br/>")
                    elif products[product]["type"] == "custom":
                        self.write(b'<div class="col-sm product" name="%s">' % (products[product]["id"].replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&#39;').encode()))
                        self.write(b'<form id="deleteForm%d" class="deleteForm" action="%s" method="post">' % (i, path.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&#39;').encode()))
                        self.write(b'<input type="hidden" name="listId" value="%s" required>' % (listId.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&#39;').encode()))
                        self.write(b'<input type="hidden" name="id" value="%s" required>' % (products[product]["id"].replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&#39;').encode()))
                        self.write(b'<input type="hidden" name="delete" value="1" required>')
                        self.write(b"</form>")
                        self.write(b'<form class="quantityForm" action="%s" method="post">' % (path.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&#39;').encode()))
                        self.write(b'<input type="text" name="name" class="titleInput titleInputText h3" onload="adjustWidthOfInput(this)" oninput="adjustWidthOfInput(this)" value="%s" >' % (products[product]["name"].replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&#39;').encode()))
                        self.write(b"<br/>")
                        self.write(b"<h6>Notes:</h6>")
                        self.write(b'<textarea name="notes" class="productImage">%s</textarea>' % (products[product]["notes"].replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&#39;').encode()))
                        self.write(b"<br/>")
                        self.write(b"<br/>")
                        self.write(b'<div class="handle-counter">')
                        self.write(b'<input type="submit" value="&#128711;" class="deleteBtn" form="deleteForm%d">' % (i))
                        self.write(b'<span>&nbsp;&nbsp;</span>')
                        self.write(b'<button type="button" onclick="counter = document.getElementsByClassName(\'quantityCounter\')[%d]; if (counter.value) { counter.value = (parseInt(counter.value) - 1).toString(); } else { counter.value = \'-1\' }" class="counterBtn">-</button>' % (i))
                        self.write(b'<input type="number" name="quantityCounter" class="quantityCounter" min="0" max="20" value="%d" required>' % (products[product]["quantity"]))
                        self.write(b'<input type="hidden" name="originalQuantity" value="%d" required>' % (products[product]["quantity"]))
                        self.write(b'<input type="hidden" name="listId" value="%s" required>' % (listId.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&#39;').encode()))
                        self.write(b'<input type="hidden" name="id" value="%s" required>' % (products[product]["id"].replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&#39;').encode()))
                        self.write(b'<input type="hidden" name="productType" value="%s" required>' % (products[product]["type"].replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&#39;').encode()))
                        self.write(b'<button type="button" onclick="counter = document.getElementsByClassName(\'quantityCounter\')[%d]; if (counter.value) { counter.value = (parseInt(counter.value) + 1).toString(); } else { counter.value = \'1\' }" class="counterBtn">+</button>' % (i))
                        self.write(b'<span>&nbsp;&nbsp;</span>')
                        self.write(b'<input type="button" value="&check;" onclick="changeValidity(%d)" class="quantityBtn">' % (i))
                        self.write(b"</div>")
                        self.write(b'</form>')
                        self.write(b"</div>")
                        self.write(b"<br/>")
                        self.write(b"<script>")
                        self.write(b"function getWidthOfInput(input) {")
                        self.write(b'    var tmp = document.createElement("span");')
                        self.write(b'    tmp.className = "titleInputText h3";')
                        self.write(b"    tmp.innerHTML = input.value.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/ /g, '&nbsp;');")
                        self.write(b"    document.body.appendChild(tmp);")
                        self.write(b"    var width = tmp.getBoundingClientRect().width;")
                        self.write(b"    document.body.removeChild(tmp);")
                        self.write(b"    return width;")
                        self.write(b"}")
                        self.write(b"function adjustWidthOfInput(input) {")
                        self.write(b'    input.style.width = "100%";')
                        self.write(b'    var maxWidth = input.getBoundingClientRect().width;')
                        self.write(b"    var newWidth = getWidthOfInput(input) + 48;")
                        self.write(b"    if (newWidth > maxWidth) {")
                        self.write(b"        newWidth = maxWidth;")
                        self.write(b"    }")
                        self.write(b'    input.style.width = newWidth + "px";')
                        self.write(b"}")
                        self.write(b"for (let i = 0; i < document.getElementsByClassName('titleInput').length; i++) {")
                        self.write(b"    adjustWidthOfInput(document.getElementsByClassName('titleInput')[i])")
                        self.write(b"}")
                        self.write(b"</script>")
                self.write(b'</div>')
            self.write(b"</center>")
            self.write(b'<div id="errorModal" class="modal">')
            self.write(b'<div class="modal-content">')
            self.write(b'<span class="errorClose">&times;</span>')
            self.write(b'<div class="modal-body">')
            self.write(b'<center>')
            self.write(b'<h4 id="errorModalContent">&nbsp;</h4>')
            self.write(b'</center>')
            self.write(b'</div>')
            self.write(b'</div>')
            self.write(b'</div>')
            self.write(b"</body>")
            self.write(b'<script>')
            self.write(b'errorModal = document.getElementById("errorModal");')
            self.write(b'errorClose = document.getElementsByClassName("errorClose")[0];')
            self.write(b'errorClose.onclick = function() {')
            self.write(b'     errorModal.style.display = "none";')
            self.write(b'}')
            self.write(b'window.onclick = function(event) {')
            self.write(b'     if (event.target == errorModal) {')
            self.write(b'         errorModal.style.display = "none";')
            self.write(b'     }')
            self.write(b'}')
            self.write(b'function changeValidity(index) {')
            self.write(b'     counter = document.getElementsByClassName("quantityCounter")[index];')
            self.write(b'     title = document.getElementsByClassName("titleInputText")[index];')
            self.write(b'     if (!counter.checkValidity()) {')
            self.write(b'          document.getElementById("errorModalContent").innerHTML = counter.validationMessage;')
            self.write(b'          errorModal.style.display = "block";')
            self.write(b'     } else if (title.value === "") {')
            self.write(b'          document.getElementById("errorModalContent").innerHTML = "Value required for name.";')
            self.write(b'          errorModal.style.display = "block";')
            self.write(b'     } else {')
            self.write(b'         form = document.getElementsByClassName("quantityForm")[index];')
            self.write(b'         form.submit()')
            self.write(b'     }')
            self.write(b'}')
            self.write(b'</script>')
            self.write(b"</html>")
        elif path in ["/search", "/search.html"]:
            if "listId" not in cookies:
                self.send_response(301)
                self.send_header('Location', '/')
                self.end_headers()
                return
            listId = cookies["listId"].value
            search = ""
            if "search" in query:
                search = query["search"][0].replace("*", "")
            r = session.get("http://shop.countdown.co.nz/api/v1/products?target=search&search=%s&size=1" % (urllib.parse.quote_plus(search)), headers=headers)
            try:
                totalItems = json.loads(r.text)["products"]["totalItems"]
            except:
                totalItems = 0

            products = []

            for i in range(1, math.ceil(totalItems / 120) + 1):
                r = session.get("http://shop.countdown.co.nz/api/v1/products?target=search&search=%s&page=%d&size=120" % (urllib.parse.quote_plus(search), i), headers=headers)
                productsDict = json.loads(r.text)["products"]["items"]
                for j, item in enumerate(productsDict):
                    products.append({"name": capitalize(item["name"]), "type": "product", "quantity": 0, "id": item["sku"], "price": item["price"]["originalPrice"], "salePrice": item["price"]["salePrice"], "images": item["images"]})
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.write(b"<html>")
            self.write(b"<head>")
            self.write(b'<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=0">')
            self.write(b"<title>Shopping List Search</title>")
            self.write(b'<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">')
            self.write(b"<style>")
            self.write(b"""
                                body {
                                    margin-left: 100px;
                                    margin-right: 100px;
                                    margin-top: 50px;
                                    margin-bottom: 50px;
                                }

                                h1 {
                                    font-size: 3em;
                                }

                                h2 {
                                    font-size: 2.2em;
                                }

                                .productImage {
                                    width: 200px;
                                    height: 200px;
                                }

                                .listBtn {
                                    padding: 0px;
                                    width: 100px;
                                    height: 38px;
                                    top: 10px;
                                    left: 10px;
                                    position: absolute;
                                    background-color: white;
                                    color: #4CAF50;
                                    border: 2px solid #4CAF50;
                                    border-radius: 6px;
                                    text-align: center;
                                    text-decoration: none;
                                    display: inline-block;
                                    font-size: 16px;
                                    margin: 4px 2px;
                                    transition-duration: 0.4s;
                                    cursor: pointer;
                                }
                                
                                .listBtn:hover {
                                    background-color: #4CAF50;
                                    color: white;
                                }

                                .clearIdBtn {
                                    padding: 0px;
                                    width: 100px;
                                    height: 38px;
                                    top: 10px;
                                    right: 10px;
                                    position: absolute;
                                    background-color: white;
                                    color: #f44336;
                                    border: 2px solid #f44336;
                                    border-radius: 6px;
                                    text-align: center;
                                    text-decoration: none;
                                    display: inline-block;
                                    font-size: 16px;
                                    margin: 4px 2px;
                                    transition-duration: 0.4s;
                                    cursor: pointer;
                                }
                                
                                .clearIdBtn:hover {
                                    background-color: #f44336;
                                    color: white;
                                }

                                .addToListBtn {
                                    padding: 0px;
                                    width: 100px;
                                    height: 38px;
                                    background-color: white;
                                    color: #4CAF50;
                                    border: 2px solid #4CAF50;
                                    border-radius: 6px;
                                    text-align: center;
                                    text-decoration: none;
                                    display: inline-block;
                                    font-size: 16px;
                                    margin: 4px 2px;
                                    transition-duration: 0.4s;
                                    cursor: pointer;
                                }
                                
                                .addToListBtn:hover {
                                    background-color: #4CAF50;
                                    color: white;
                                }
                                
                                .product {
                                    overflow: hidden;
                                    margin: 10px;
                                    padding: 20px;
                                    border-radius: 10px;
                                    border: 1px solid #555555;
                                    min-width: 350px;
                                    max-width: 650px;
                                }
                                
                                .products {
                                    padding: 100px;
                                }
                                
                                .handle-counter {
                                    overflow:hidden;
                                    display: flex;
                                    align-items: center;
                                    justify-content: center;
                                }

                                .counterBtn, #counter {
                                    text-align: center;
                                }

                                .counterBtn {
                                    width: 38px;
                                    height: 38px;
                                    float: left;
                                    background-color: #4CAF50;
                                    padding: 6px 12px;
                                    border: 1px solid transparent;
                                    color: white;
                                    transition-duration: 0.4s;
                                }

                                .counterBtn:disabled, .counterBtn:disabled:hover {
                                    background-color: darkgrey;
                                    cursor: not-allowed;
                                }

                                .counterBtn:hover {
                                    background-color: #419544;
                                }
                                
                                .titleInput {
                                    min-width: 100px;
                                    border: 1px solid #999999;
                                    border-radius: 3px;
                                    background-image: url('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADAAAAAwCAQAAAD9CzEMAAAAp0lEQVRYw+3SQQrCMBRF0QtZSLuWgrspdO4qdBHZh+BCsociDv0Ok9pmIv+Bwn+Zn0tCIBb7hQ3ceHAlafiRgmEYWZGovCSx5QWJ+YMXJM4HiYvP40zdxOrBF56cOom7B29YJ1EYfPjjRGH04/cJd36bmD35zMJrl3DkE7A0t5j8+URufo7r4wQffPDB/zWPmkfN14CIrwERXwPtceRR86h51Hws9t3exfxsR4kLnvYAAAAASUVORK5CYII=');
                                    background-size: 21px 21px;
                                    background-position: 10px 10px; 
                                    background-repeat: no-repeat;
                                    padding-top: 6px;
                                    padding-bottom: 6px;
                                    padding-left: 40px;
                                }

                                .titleInputText {
                                    font-size: 18pt;
                                }

                                .quantityCounter {
                                    float: left;
                                    width: 75px;
                                    text-align: center;
                                    border-width: 1px;
                                    border-left: none;
                                    border-right: none;
                                    padding: 6px 12px;
                                    color: #555;
                                    background-color: white;
                                    border: 1px solid #ccc;
                                }
                                
                                .quantityCounter:focus {
                                    outline: none;
                                }
                                
                                .quantityCounter::-webkit-outer-spin-button, .quantityCounter::-webkit-inner-spin-button {
                                    -webkit-appearance: none;
                                    margin: 0;
                                }
                                
                                .quantityCounter {
                                    -moz-appearance: textfield;
                                }
                                
                                .modal {
                                    display: none;
                                    position: fixed;
                                    z-index: 1;
                                    padding-top: 10%;
                                    left: 0;
                                    top: 0;
                                    width: 100%;
                                    height: 100%
                                    overflow: auto;
                                    background-color: rgb(0, 0, 0);
                                    background-color: rgba(0, 0, 0, 0.4);
                                }
                                
                                .modal-content {
                                    position: relative;
                                    background-color: #fefefe;
                                    margin: auto;
                                    padding: 0;
                                    border: 1px solid #888;
                                    border-radius: 10px;
                                    width: 50%;
                                    height: 20%;
                                    box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
                                    -webkit-animation-name: animatetop;
                                    -webkit-animation-duration: 0.4s;
                                    animation-name: animatetop;
                                    animation-duration: 0.4s;
                                }
                                
                                @-webkit-keyframes animatetop {
                                    from {top:-300px; opacity:0} 
                                    to {top:0; opacity:1}
                                }

                                @keyframes animatetop {
                                    from {top:-300px; opacity:0}
                                    to {top:0; opacity:1}
                                }
                                
                                .errorClose {
                                    color: #f44336;
                                    z-index: 1;
                                    font-size: 28px;
                                    font-weight: bold;
                                    position: absolute;
                                    top: 10px;
                                    right: 20px;
                                    transition-duration: 0.2s;

                                    -webkit-touch-callout: none;
                                    -webkit-user-select: none;
                                    -khtml-user-select: none;
                                    -moz-user-select: none;
                                    -ms-user-select: none;
                                    user-select: none;
                                }

                                .errorClose:hover, .errorClose:focus {
                                    color: #ab2f26;
                                    text-decoration: none;
                                    cursor: pointer;
                                    transition-duration: 0.2;
                                }
                                
                                .modal-body {
                                    width: 100%;
                                    height: 100%;
                                    display: flex;
                                    align-items: center;
                                    justify-content: center;
                                }
                                
                                .searchInput {
                                    width: 130px;
                                    height: 45px;
                                    text-align: center;
                                    box-sizing: border-box;
                                    border: 2px solid #ccc;
                                    border-radius: 4px;
                                    font-size: 16px;
                                    background-color: white;
                                    background-image: url('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABUAAAAVCAYAAACpF6WWAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAAEnQAABJ0Ad5mH3gAAAACYktHRAD/h4/MvwAAAAl2cEFnAAABKgAAASkAUBZlMQAAACV0RVh0ZGF0ZTpjcmVhdGUAMjAxMy0wNC0xMFQwNjo1OTowNy0wNzowMI5BiVEAAAAldEVYdGRhdGU6bW9kaWZ5ADIwMTMtMDQtMTBUMDY6NTk6MDctMDc6MDD/HDHtAAAAGXRFWHRTb2Z0d2FyZQB3d3cuaW5rc2NhcGUub3Jnm+48GgAAABF0RVh0VGl0bGUAc2VhcmNoLWljb27Cg+x9AAACKklEQVQ4T6WUSavqQBCFK+2sII7gShFXLpUsBBHFf+1KcAQFwaWiolsnnBDn++4p0iHRqPDuByFJd/Wp6qrqVn5+IQP3+52m0ymtVis6Ho885na7KRgMUiKR4O9vmEQHgwGNx2NyOp0khCBFUXgcJo/Hg67XK8ViMcpkMjz+Dl200+nQZrMhh8PBE4gYQgDidrudvzEOm2KxyP9WsCginM1mHKEUS6VSFA6HOWI4G41GPAfx2+1GgUCAVFXVZMwovwY/lUqFPB4PiyFn+XxemzbT6/VovV6z8Ol0olwux+LPCBQFEQKIvhME2WyWbWGHFCD/VghUGVvE1rDlb6TTabbFmuVyqY2aEWgbFALeI5GINvyeUCjEtlgju+IZoRWfkS30CURoxFJUNjMEt9stf38CNjJKIFvNiMBJgTebzcZt843hcMhCELWqPBDxeJwulwtvC/3X7/e1qVfgFD0rC5tMJrUZM8Lr9VI0GmVBRDCfz6nZbHI/Sna7HXW7XZpMJtxSiBIP1lmhH9NqtaqfGKQDTmQREBnSgwfmMqfYYblc1o+2xHShtNttLgSiee4EmMEp3hDBPJzikimVSuRyuTTLJ1GwWCz4pCB3UhiL/X4/Hw50C5zjLSM+n898weCogxdRIzAGxigAdtNqtV6EC4UC+Xy+z6Kf2O/31Gg0TMK4ZBDxf4uCw+FA9XpdF0aaUOg/iQLcHbVaTb/p0Cl/FgXIJ/oYnaCqKv0DC6dltH6Ks84AAAAASUVORK5CYII=');
                                    background-position: 10px 10px; 
                                    background-repeat: no-repeat;
                                    padding: 12px 20px 12px 40px;
                                    -webkit-transition: width 0.4s ease-in-out;
                                    transition: width 0.4s ease-in-out;
                                }
                                
                                .searchInput:focus {
                                    width: 100%;
                                }""")
            self.write(b"</style>")
            self.write(b"</head>")
            self.write(b"<body>")
            self.write(b'<a href="/list"><input class="listBtn" value="List" type="button"></a>')
            self.write(b'<form id="clearIdForm" action="%s" method="post">' % (path.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&#39;').encode()))
            self.write(b'<input name="clearId" value="1" type="hidden">')
            self.write(b'<input class="clearIdBtn" value="Clear Id" type="submit">')
            self.write(b"</form>")
            self.write(b"<center>")
            self.write(b'<h1>Shopping List Search</h1>')
            self.write(b"<br/>")
            self.write(b'<form class="searchForm" action="%s" method="get">' % (path.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&#39;').encode()))
            self.write(b'<input name="search" type="text" class="searchInput" placeholder="Search..." >')
            self.write(b"</form>")
            if search:
                if not products:
                    self.write(b"<h1 class='title'>No Items Found.</h1>")
                else:
                    self.write(b'<h2>Items: %d</h2>' % (len(products)))
                    self.write(b"<br/>")
                    self.write(b'<div class="row justify-content-center">')
                    for i, product in enumerate(products):
                        self.write(b'<div class="col-sm product" name="%s">' % (product["id"].replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&#39;').encode()))
                        self.write(b"<h3>%s</h3>" % (product["name"].replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&#39;').encode()))
                        self.write(b"<br/>")
                        self.write(b'<center><img class="productImage" src="%s" /></center>' % (product["images"]["big"].replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&#39;').encode()))
                        self.write(b"<br/>")
                        self.write(b"<p>$%.2f</p>" % (product["salePrice"]))
                        self.write(b'<form class="quantityForm" action="%s" method="post">' % (path.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&#39;').encode()))
                        self.write(b'<div class="handle-counter">')
                        self.write(b'<button type="button" onclick="counter = document.getElementsByClassName(\'quantityCounter\')[%d]; if (counter.value) { counter.value = (parseInt(counter.value) - 1).toString(); } else { counter.value = \'-1\' }" class="counterBtn">-</button>' % (i))
                        self.write(b'<input type="number" name="quantityCounter" class="quantityCounter" min="1" max="20" value="1" required>')
                        self.write(b'<input type="hidden" name="listId" value="%s" required>' % (listId.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&#39;').encode()))
                        self.write(b'<input type="hidden" name="query" value="%s" required>' % (search.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&#39;').encode()))
                        self.write(b'<input type="hidden" name="id" value="%s" required>' % (product["id"].replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&#39;').encode()))
                        self.write(b'<input type="hidden" name="productType" value="%s" required>' % (product["type"].replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&#39;').encode()))
                        self.write(b'<button type="button" onclick="counter = document.getElementsByClassName(\'quantityCounter\')[%d]; if (counter.value) { counter.value = (parseInt(counter.value) + 1).toString(); } else { counter.value = \'1\' }" class="counterBtn">+</button>' % (i))
                        self.write(b"</div>")
                        self.write(b'<br />')
                        self.write(b'<input type="button" value="Add to List!" onclick="changeValidity(%d)" class="addToListBtn">' % (i))
                        self.write(b'</form>')
                        self.write(b"</div>")
                        self.write(b"<br/>")
                    self.write(b'</div>')
            self.write(b"</center>")
            self.write(b'<div id="errorModal" class="modal">')
            self.write(b'<div class="modal-content">')
            self.write(b'<span class="errorClose">&times;</span>')
            self.write(b'<div class="modal-body">')
            self.write(b'<center>')
            self.write(b'<h4 id="errorModalContent"></h4>')
            self.write(b'</center>')
            self.write(b'</div>')
            self.write(b'</div>')
            self.write(b'</div>')
            self.write(b"</body>")
            self.write(b'<script>')
            self.write(b'errorModal = document.getElementById("errorModal");')
            self.write(b'errorClose = document.getElementsByClassName("errorClose")[0];')
            self.write(b'errorClose.onclick = function() {')
            self.write(b'     errorModal.style.display = "none";')
            self.write(b'}')
            self.write(b'window.onclick = function(event) {')
            self.write(b'     if (event.target == errorModal) {')
            self.write(b'         errorModal.style.display = "none";')
            self.write(b'     }')
            self.write(b'}')
            self.write(b'function changeValidity(index) {')
            self.write(b'     counter = document.getElementsByClassName("quantityCounter")[index];')
            self.write(b'     if (!counter.checkValidity()) {')
            self.write(b'          document.getElementById("errorModalContent").innerHTML = counter.validationMessage;')
            self.write(b'          errorModal.style.display = "block";')
            self.write(b'     } else {')
            self.write(b'         form = document.getElementsByClassName("quantityForm")[index];')
            self.write(b'         form.submit()')
            self.write(b'     }')
            self.write(b'}')
            self.write(b'</script>')
            self.write(b"</html>")
        else:
            do_ERROR(self)

    def do_POST(self):
        path = urlparse(self.path).path
        length = int(self.headers['Content-Length'])
        content = self.rfile.read(length).decode('utf-8')
        post_data = parse_qs(content)
        if path in ["/", "/index", "/index.html"]:
            if "listId" not in post_data:
                self.send_response(301)
                self.send_header('Location', path)
                self.end_headers()
                return
            else:
                self.send_response(301)
                cookie = http.cookies.SimpleCookie()
                cookie["listId"] = post_data["listId"][0]
                expires = datetime.datetime.utcnow() + datetime.timedelta(days=7)
                cookie["listId"]["expires"] = expires.strftime("%a, %d %b %Y %H:%M:%S GMT")
                for value in cookie.values():
                    self.send_header("Set-Cookie", value.OutputString())
                self.send_header('Location', path)
                self.end_headers()
        elif path in ["/list", "/list.html"]:
            if "clearList" in post_data and post_data["clearList"][0] == "1" and "listId" in post_data:
                listId = post_data["listId"][0]
                send('{"%s": "clear"}' % (listId))
                self.send_response(301)
                self.send_header('Location', path)
                self.end_headers()
            elif "clearId" in post_data and post_data["clearId"][0] == "1":
                self.send_response(301)
                cookie = http.cookies.SimpleCookie()
                cookie["listId"] = ""
                cookie["listId"]["expires"] = datetime.datetime.fromtimestamp(0).strftime("%a, %d %b %Y %H:%M:%S GMT")

                for value in cookie.values():
                    print(value)
                    self.send_header("Set-Cookie", value.OutputString())
                self.send_header('Location', path)
                self.end_headers()
            elif "customItem" in post_data and post_data["customItem"][0] == "1" and "listId" in post_data and "name" in post_data and "customCounter" in post_data:
                try:
                    listId = post_data["listId"][0]
                    id = str(uuid.uuid4())
                    productType = "custom"
                    quantityCounter = int(post_data["customCounter"][0])
                    if "notes" not in post_data:
                        notes = ""
                    else:
                        notes = post_data["notes"][0]
                    name = post_data["name"][0]
                    send('{"%s": {"add": {"%s": {"type": "%s", "name": "%s", "notes": "%s", "quantity": %d}}}}' % (listId, id, productType, name, notes, quantityCounter))
                    send('{"%s": {"set": {"%s": {"type": "%s", "name": "%s", "notes": "%s"}}}}' % (listId, id, productType, name, notes))
                    self.send_response(301)
                    self.send_header('Location', path)
                    self.end_headers()
                except:
                    traceback.print_exc()
            elif "delete" in post_data and post_data["delete"][0] == "1" and "listId" in post_data and "id" in post_data:
                listId = post_data["listId"][0]
                id = post_data["id"][0]
                try:
                    send('{"%s": {"delete": "%s"}}' % (listId, id))
                except Exception as e:
                    traceback.print_exc()
                self.send_response(301)
                self.send_header('Location', path)
                self.end_headers()
            elif "quantityCounter" not in post_data or "originalQuantity" not in post_data or "id" not in post_data or "listId" not in post_data or "productType" not in post_data or (post_data["productType"][0] == "custom" and "name" not in post_data):
                self.send_response(301)
                self.send_header('Location', path)
                self.end_headers()
            elif post_data["productType"][0] == "product":
                try:
                    quantityCounter = int(post_data["quantityCounter"][0])
                    originalQuantity = int(post_data["originalQuantity"][0])
                    listId = post_data["listId"][0]
                    id = post_data["id"][0]
                    productType = post_data["productType"][0]
                    deltaQuantity = quantityCounter - originalQuantity
                    if deltaQuantity > 0:
                        send('{"%s": {"add": {"%s": {"type": "%s", "quantity": %d}}}}' % (listId, id, productType, deltaQuantity))
                    elif deltaQuantity < 0:
                        send('{"%s": {"subtract": {"%s": {"type": "%s", "quantity": %d}}}}' % (listId, id, productType, deltaQuantity * -1))
                    if quantityCounter == 0:
                        send('{"%s": {"delete": "%s"}}' % (listId, id))
                except Exception as e:
                    traceback.print_exc()
                self.send_response(301)
                self.send_header('Location', path)
                self.end_headers()
            elif post_data["productType"][0] == "custom":
                try:
                    quantityCounter = int(post_data["quantityCounter"][0])
                    originalQuantity = int(post_data["originalQuantity"][0])
                    listId = post_data["listId"][0]
                    id = post_data["id"][0]
                    productType = post_data["productType"][0]
                    if "notes" not in post_data:
                        notes = ""
                    else:
                        notes = post_data["notes"][0]
                    name = post_data["name"][0]
                    deltaQuantity = quantityCounter - originalQuantity
                    if deltaQuantity > 0:
                        send('{"%s": {"add": {"%s": {"type": "%s", "name": "%s", "notes": "%s", "quantity": %d}}}}' % (listId, id, productType, name, notes, deltaQuantity))
                        send('{"%s": {"set": {"%s": {"type": "%s", "name": "%s", "notes": "%s"}}}}' % (listId, id, productType, name, notes))
                    elif deltaQuantity < 0:
                        send('{"%s": {"subtract": {"%s": {"type": "%s", "name": "%s", "notes": "%s", "quantity": %d}}}}' % (listId, id, productType, name, notes, deltaQuantity * -1))
                        send('{"%s": {"set": {"%s": {"type": "%s", "name": "%s", "notes": "%s"}}}}' % (listId, id, productType, name, notes))
                    else:
                        send('{"%s": {"set": {"%s": {"type": "%s", "name": "%s", "notes": "%s"}}}}' % (listId, id, productType, name, notes))
                    if quantityCounter == 0:
                        send('{"%s": {"delete": "%s"}}' % (listId, id))
                except Exception as e:
                    traceback.print_exc()
                self.send_response(301)
                self.send_header('Location', path)
                self.end_headers()
        elif path in ["/search", "/search.html"]:
            if "clearId" in post_data and post_data["clearId"][0] == "1":
                self.send_response(301)
                cookie = http.cookies.SimpleCookie()
                cookie["listId"] = ""
                cookie["listId"]["expires"] = datetime.datetime.fromtimestamp(0).strftime("%a, %d %b %Y %H:%M:%S GMT")
                for value in cookie.values():
                    self.send_header("Set-Cookie", value.OutputString())
                self.send_header('Location', "/")
                self.end_headers()
            elif "quantityCounter" not in post_data or "id" not in post_data or "listId" not in post_data or "query" not in post_data:
                self.send_response(301)
                try:
                    query = "?search=" + urllib.parse.quote_plus(post_data["query"][0])
                except:
                    query = ""
                self.send_header('Location', path + query)
                self.end_headers()
            else:
                try:
                    quantityCounter = int(post_data["quantityCounter"][0])
                    listId = post_data["listId"][0]
                    id = post_data["id"][0]
                    query = "?search=" + urllib.parse.quote_plus(post_data["query"][0])
                    send('{"%s": {"add": {"%s": {"type": "product", "quantity": %d}}}}' % (listId, id, quantityCounter))
                except Exception as e:
                    traceback.print_exc()
                self.send_response(301)
                self.send_header('Location', path + query)
                self.end_headers()
        else:
            self.send_response(301)
            self.send_header('Location', path)
            self.end_headers()

if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")