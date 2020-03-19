
import  asyncio
from aria2.websoket import aria2
from aria2.utils import format_bytes,format_rate

def recv(message):
    """
    接收信息回调
    :param message:  返回信息
    :return:
    """
    print(message)
    id=message.get('id')


    if id =="addUri" or id  =="addTorrent" :
        gid=message.get("result")
        print("任务创建成功 gid %s" %gid)
    elif id == "tellActive":
        for item in  message.get("result"):
            status = item.get("status")
            Speed = item.get("downloadSpeed")
            completed=item.get("completedLength")
            total=item.get("totalLength")
            print("gid:%s  活动状态：%s  速度: %s/s   进度: %s  已下载：%s  总大小：%s"
                  % (item.get("gid"),
                     status,
                     format_bytes(Speed) ,
                     format_rate(completed,total),
                     format_bytes(completed),
                     format_bytes(total)
                     ))




def event(message):
    """
    aria2事件响应回调
    :param message: 返回信息
    :return:
    """
    print(message)
    if message.get("method") == aria2.event_DownloadStart :
        pass
    elif message.get("method") == aria2.event_DownloadPause :
        pass
    elif message.get("method") == aria2.event_DownloadStop:
        pass
    elif message.get("method") == aria2.event_DownloadComplete :
        pass
    elif message.get("method") == aria2.event_DownloadError  :
        pass
    elif message.get("method") == aria2.event_BtDownloadComplete  :
        pass
    else:
        pass


async def tell_loop(aria):
    while True:
        aria.tellActive(["gid", "status", "totalLength", "completedLength", "downloadSpeed"])
        await asyncio.sleep(1)


if __name__ == '__main__':

    aria=aria2("127.0.0.1",token="usertoken",recv_message=recv,event_message=event)

    options={
        'dir': '/root',
        'out':'猎心者第13集.mp4'
    }
    aria.addUri(["http://okzy.xzokzyzy.com/20200316/7550_90c48879/猎心者第13集.mp4"],options )
    asyncio.run(tell_loop(aria))
