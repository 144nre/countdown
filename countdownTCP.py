import sys
import socket
import selectors
import types
import traceback
import json
import requests
import re
import time
import math

def capitalize(str):
    return re.sub("(?:[0-9A-Za-z])\S*", lambda e: e[0][0].upper() + e[0][1:], str)

session = requests.Session()
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
           'X-Requested-With': 'OnlineShopping.WebApp'}

lists = {}

sel = selectors.DefaultSelector()
host, port = '0.0.0.0', 8889
lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lsock.bind((host, port))
lsock.listen()
print(f"Listening on {(host, port)}")
lsock.setblocking(False)
sel.register(lsock, selectors.EVENT_READ, data=None)

def accept_wrapper(sock):
    conn, addr = sock.accept()
    # print(f"Accepted connection from {addr}")
    conn.setblocking(False)
    data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(conn, events, data=data)

def service_connection(key, mask):
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)
        if recv_data:
            data.outb += recv_data
        else:
            print(f"Closing connection to {data.addr}")
            sel.unregister(sock)
            sock.close()
    if mask & selectors.EVENT_WRITE:
        if data.outb:
            message = data.outb.decode()
            if message.startswith('16e0050be90d8f4eb098a24679d71ab5$'):
                msg = message[33:]
                print(msg)
                try:
                    listIds = json.loads(msg)
                    for listId in listIds:
                        if listId not in lists or listIds[listId] == "clear":
                            lists[listId] = {}
                        if listIds[listId] == "view":
                            print("view")
                            sock.send(json.dumps(lists[listId]).encode())
                            sel.unregister(sock)
                            sock.close()
                            return
                        for action in listIds[listId]:
                            print(action)
                            if action == "view":
                                if listIds[listId][action] in lists[listId]:
                                    pass
                                    sock.send(json.dumps(lists[listId][listIds[listId][action]]).encode())
                                    sel.unregister(sock)
                                    sock.close()
                                    return
                            if action == "delete":
                                lists[listId].pop(listIds[listId][action], None)
                            for productId in listIds[listId][action]:
                                if action == "set":
                                    if productId in lists[listId]:
                                        for key in listIds[listId][action][productId]:
                                            lists[listId][productId][key] = listIds[listId][action][productId][key]
                                    elif listIds[listId][action][productId]["type"] == "product":
                                        r = session.get("http://shop.countdown.co.nz/api/v1/products/%s" % (productId), headers=headers)
                                        if r.status_code == 200:
                                            item = json.loads(r.text)
                                            lists[listId][productId] = {"name": capitalize(item["name"]), "type": "product", "quantity": listIds[listId][action][productId]["quantity"], "id": item["sku"], "price": item["price"]["originalPrice"], "salePrice": item["price"]["salePrice"], "aisle": {"name": item["breadcrumb"]["aisle"]["name"], "value": item["breadcrumb"]["aisle"]["value"]}, "images": item["images"]}
                                        else:
                                            pass
                                            sock.send(b"failed")
                                            sel.unregister(sock)
                                            sock.close()
                                            return
                                    elif listIds[listId][action][productId]["type"] == "custom":
                                        lists[listId][productId] = {"name": capitalize(productId), "id": productId, "notes": "", "type": "custom"}
                                        for key in listIds[listId][action][productId]:
                                            lists[listId][productId][key] = listIds[listId][action][productId][key]
                                if action == "add":
                                    if productId in lists[listId]:
                                        lists[listId][productId]["quantity"] += listIds[listId][action][productId]["quantity"]
                                    elif listIds[listId][action][productId]["type"] == "product":
                                        r = session.get("http://shop.countdown.co.nz/api/v1/products/%s" % (productId), headers=headers)
                                        if r.status_code == 200:
                                            item = json.loads(r.text)
                                            lists[listId][productId] = {"name": capitalize(item["name"]), "type": "product", "quantity": listIds[listId][action][productId]["quantity"], "id": item["sku"], "price": item["price"]["originalPrice"], "salePrice": item["price"]["salePrice"], "aisle": {"name": item["breadcrumb"]["aisle"]["name"], "value": item["breadcrumb"]["aisle"]["value"]}, "images": item["images"]}
                                        else:
                                            pass
                                            sock.send(b"failed")
                                            sel.unregister(sock)
                                            sock.close()
                                            return
                                    elif listIds[listId][action][productId]["type"] == "custom":
                                        lists[listId][productId] = {"name": capitalize(productId), "id": productId, "notes": "", "type": "custom"}
                                        for key in listIds[listId][action][productId]:
                                            lists[listId][productId][key] = listIds[listId][action][productId][key]
                                if action == "subtract":
                                    if productId in lists[listId]:
                                        lists[listId][productId]["quantity"] -= listIds[listId][action][productId]["quantity"]
                    sock.send(b"success")
                    sel.unregister(sock)
                    sock.close()
                    return
                except Exception as e:
                    traceback.print_exc()
            sock.send(b"failed")
            sel.unregister(sock)
            sock.close()

try:
    while True:
        try:
            events = sel.select(timeout=None)
            for key, mask in events:
                if key.data is None:
                    accept_wrapper(key.fileobj)
                else:
                    service_connection(key, mask)
        except:
            traceback.print_exc()
except KeyboardInterrupt:
    print("Caught keyboard interrupt, exiting")
finally:
    sel.close()