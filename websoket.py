
import threading,base64
from websocket import create_connection
import  json

#接收回传数据
def onmessage(aria):
    while aria._isrecv:
        result= aria.ws.recv()
        if result:
            jsonobj= json.loads(result)
            if "method" in jsonobj.keys():
                if aria.event:
                    aria.event(jsonobj)
            else:
                aria.message(jsonobj)

class aria2:
    """
    通过websocket通信的，aria2的下载器。通信格式 jsonrpc

    """
    event_DownloadStart="aria2.onDownloadStart"
    event_DownloadPause= 'aria2.onDownloadPause',
    event_DownloadStop= 'aria2.onDownloadStop',
    event_DownloadComplete= 'aria2.onDownloadComplete',
    event_DownloadError= 'aria2.onDownloadError',
    event_BtDownloadComplete= 'aria2.onBtDownloadComplete',


    def __init__(self,host,port=6800,token=None,recv_message=None,event_message=None):
        """
        aria2对象初始化
        :param host: ws服务器IP地址
        :param port: ws服务器端口 默认：6800
        :param token: secret token  通信密令
        :param recv_message: 接收信息回调
        :param event_message: 事件信息回调

        """

        self.addr = "ws://{}:{}/jsonrpc".format(host,port)
        self.ws = create_connection(self.addr)
        self._token = token
        if recv_message:
            self._isrecv = True
            self.message=recv_message
            thread = threading.Thread(target=onmessage,args=(self,))
            thread.start()
            if event_message:
                self.event=event_message

    def _send(self,method,params=[],id=None):
        """
        调用aria2的函数
        :param method:需要调用的方法名
        :param params:传入到方法的参数
        :param id: 通信会话id

        """
        jsonreq = {'jsonrpc': '2.0', 'id': id,
                   'method': method,
                   "params": params
                }
        data = json.dumps(jsonreq)
        self.ws.send(data)

    def addUri(self,urls,options=[] ,id='addUri'):
        """
        此方法添加了新的下载。
        :param urls: uri是指向同一资源的HTTP/FTP/SFTP/BitTorrent URI（字符串）的数组
        :param options: 下载设置配置项
        :param id:通信会话id
        :return: 新建任务gid '{"id":"qwer","jsonrpc":"2.0","result":"2089b05ecca3d829"}'
        """

        params=[]
        if self._token:
            params.append("token:"+self._token)
        params.append(urls)
        params.append(options)
        self._send("aria2.addUri",params,id)

    def addTorrent(self,torrent,urls=[],options=[],id='addTorrent'):
        """
        此方法通过上传“.torrent”文件来添加BitTorrent下载
        :param torrent: 种子文件的本地地址
        :param urls: uris是URI（字符串）的数组。uris用于网络播种。
        :param options: 下载设置配置项
        :param id:通信会话id
        :return:新建任务gid '{"id":"qwer","jsonrpc":"2.0","result":"2089b05ecca3d829"}'
        """

        if torrent.endswith(".torrent"):
            params = []
            if self._token:
                params.append("token:" + self._token)
            btorrent=""
            with open(torrent,'br') as file:
                btorrent=base64.b64encode(file.read())
                btorrent=btorrent.decode('utf-8')
            params.append(btorrent)
            params.append(urls)
            params.append(options)
            self._send("aria2.addTorrent", params, id)
        else:
            raise TypeError("种子格式错误")

    def addMetalink(self,metalink,options=[],id='addMetalink'):
        """
        此方法通过上传“ .metalink”文件来添加Metalink下载。
        :param torrent: .metalink文件的本地地址
        :param options: 下载设置配置项
        :param id:通信会话id
        :return:新建任务gid '{"id":"qwer","jsonrpc":"2.0","result":"2089b05ecca3d829"}'
        """

        if metalink.endswith(".metalink"):
            params = []
            if self._token:
                params.append("token:" + self._token)
            btorrent=""
            with open(metalink,'br') as file:
                btorrent=str(base64.b64encode(file.read()),encoding="utf-8")
            params.append(metalink)
            params.append(options)
            self._send("aria2.addMetalink", params, id)
        else:
            raise TypeError(".metalink文件格式错误")

    def remove(self,gid,id='remove'):
        """
        移除指定gid的下载，如果指定的下载正在进行中，则会首先停止。
        下载的状态变为removed。此方法返回已删除下载的GID。
        :param gid:下载任务gid
        :param id:用户会话id
        :return: 受影响的下载id '{"id":"qwer","jsonrpc":"2.0","result":"2089b05ecca3d829"}'
        """

        params=[]
        if self._token:
            params.append("token:"+self._token)
        params.append(gid)
        self._send("aria2.remove",params,id)

    def forceRemove(self,gid,id='forceRemove'):
        """
        强制移除指定gid的下载，如果指定的下载正在进行中，则会首先停止。
        下载的状态变为removed。此方法返回已删除下载的GID。
        :param gid:下载任务gid
        :param id:用户会话id
        :return: 受影响的下载id '{"id":"qwer","jsonrpc":"2.0","result":"2089b05ecca3d829"}'
        """

        params=[]
        if self._token:
            params.append("token:"+self._token)
        params.append(gid)
        self._send("aria2.forceRemove",params,id)

    def pause(self,gid,id='pause'):

        """
        暂停指定gid的下载，下载的状态变为paused。如果下载处于活动状态，则将下载放置在等待队列的前面。
        状态为时paused，无法开始下载。要将状态更改为waiting，请使用 aria2.unpause()方法。此方法返回已暂停下载的GID
        :param gid:下载任务gid
        :param id:用户会话id
        :return:受影响的下载id '{"id":"qwer","jsonrpc":"2.0","result":"2089b05ecca3d829"}'
        """

        params=[]
        if self._token:
            params.append("token:"+self._token)
        params.append(gid)
        self._send("aria2.pause",params,id)

    def pauseAll(self,id='pauseAll'):
        """
        暂停全部的下载，下载的状态变为paused。如果下载处于活动状态，则将下载放置在等待队列的前面。
        状态为时paused，无法开始下载。要将状态更改为waiting，请使用 aria2.unpause()方法。此方法返回已暂停下载的GID
        :param id:用户会话id
        :return:此方法返回OK。
        """

        params=[]
        if self._token:
            params.append("token:"+self._token)
        self._send("aria2.pauseAll",params,id)

    def forcePause(self, gid, id='forcePause'):
        """
        强制暂停指定gid的下载，下载的状态变为paused。如果下载处于活动状态，则将下载放置在等待队列的前面。
        状态为时paused，无法开始下载。要将状态更改为waiting，请使用 aria2.unpause()方法。此方法返回已暂停下载的GID
        :param gid:下载任务gid
        :param id:用户会话id
        :return:受影响的下载id '{"id":"qwer","jsonrpc":"2.0","result":"2089b05ecca3d829"}'
        """

        params = []
        if self._token:
            params.append("token:" + self._token)
        params.append(gid)
        self._send("aria2.forcePause", params, id)

    def forcePauseAll(self,id='forcePauseAll'):
        """
        强制暂停全部的下载，下载的状态变为paused。如果下载处于活动状态，则将下载放置在等待队列的前面。
        状态为时paused，无法开始下载。要将状态更改为waiting，请使用 aria2.unpause()方法。此方法返回已暂停下载的GID
        :param id:用户会话id
        :return:此方法返回OK。
        """


        params=[]
        if self._token:
            params.append("token:"+self._token)
        self._send("aria2.forcePauseAll",params,id)

    def unpause(self, gid, id='unpause'):
        """
        将gid（字符串）表示的下载状态从 paused更改为waiting，使下载符合重新启动的条件。此方法返回未暂停下载的GID。
        :param gid: 下载任务gid
        :param id: 用户会话id
        :return: 此方法返回未暂停下载的GID
        """

        params = []
        if self._token:
            params.append("token:" + self._token)
        params.append(gid)
        self._send("aria2.unpause", params, id)

    def unpauseAll(self,id='unpauseAll'):
        """
        将全部下载的状态从 paused更改为waiting，
        :param id:用户会话id
        :return:此方法返回OK。
        """
        params=[]
        if self._token:
            params.append("token:"+self._token)
        self._send("aria2.unpauseAll",params,id)

    def tellStatus(self,gid,keys=[],id='tellStatus'):
        """
        此方法返回gid（字符串）的下载进度。
        :param gid:下载任务gid
        :param keys: 字符串数组。如果指定，则响应仅在keys数组中包含键。如果键为空或省略，则响应包含所有键。
        :param id: 用户会话id
        :return:
            gid              :下载的GID。
            status           :active当前下载/播种下载。 waiting用于队列中的下载；下载未开始。 paused暂停下载。 error对于由于错误而停止的下载。 complete停止和完成下载。 removed用户删除的下载。
            totalLength      :下载的总长度（以字节为单位）。
            completedLength  :下载的完整长度（以字节为单位）。
            uploadLength     :上载的下载长度（以字节为单位）。
            bitfield         :下载进度的十六进制表示。最高位对应于索引为0的件。任何置位的位指示已加载的件，而未设置的位指示尚未加载和/或缺失的件。最后的任何溢出位都设置为零。当尚未开始下载时，该密钥将不包含在响应中。
            downloadSpeed    :此下载的下载速度以字节/秒为单位。
            uploadSpeed      :此下载的上传速度（以字节/秒为单位）。
            infoHash         :InfoHash。仅限BitTorrent。
            numSeeders       :aria2所连接的播种机数量。仅限BitTorrent。
            seeder           :true如果本地端点是播种者。否则false。仅限BitTorrent。
            pieceLength      :片段长度（以字节为单位）。
            numPieces        :件数。
            connections      :aria2已连接的对等/服务器数。
            errorCode        :此项最后错误的代码（如果有）。该值是一个字符串。错误代码在“ 退出状态”部分中定义。此值仅适用于停止/完成的下载。
            errorMessage     :与errorCode对应的错误消息 。
            followedBy       :下载结果生成的GID列表。例如，aria2下载Metalink文件时，它会生成Metalink中所述的下载内容（请参阅 --follow-metalink选项）。
                该值对于跟踪自动生成的下载很有用。如果没有此类下载，则此密钥将不包含在响应中。
            following        :的反向链接followedBy。其中包含的下载内容 followedBy具有此对象的GID following。
            belongsTo        :父级下载的GID。某些下载是另一下载的一部分。例如，如果Metalink中的文件具有BitTorrent资源，则“ .torrent”文件的下载是该父文件的一部分。如果此下载没有父项，则此密钥将不包含在响应中。
            dir              :保存文件的目录。
            files            :返回文件列表。该列表的元素与aria2.getFiles()方法中使用的结构相同。
            bittorrent       :包含从.torrent（文件）中检索到的信息的结构。仅限BitTorrent。它包含以下键。

                announceList :公告URI列表列表。如果torrent包含announce 和announce-list，announce则将转换为 announce-list格式。
                comment      :种子的评论。comment.utf-8如果可用，则使用。
                creationDate :种子的创建时间。该值是自纪元以来的整数，以秒为单位。
                mode         :torrent的文件模式。值为single或multi。
                info         :包含信息字典中数据的结构。它包含以下键。
                    name     :信息字典中的名称。name.utf-8如果可用，则使用。
            verifiedLength   :在对文件进行哈希检查时，已验证的字节数。仅当对该下载进行哈希检查时，该密钥才存在。
            verifyIntegrityPending :true如果此下载正在等待队列中的哈希检查。仅当此下载在队列中时，此密钥才存在。
        """

        params = []
        if self._token:
            params.append("token:" + self._token)
        params.append(gid)
        params.append(keys)
        self._send("aria2.tellStatus", params, id)

    def getUris(self,gid,id='getUris'):
        """
        返回由gid（字符串）表示的下载使用的URI 。响应是一个结构数组，它包含以下键。值是字符串
        uri：    URI
        status： 如果已使用URI，则为“已使用”。如果URI仍在队列中等待，则“等待”。
            {u'status': u'used',u'uri': u'http://example.org/file'}
        :param gid:
        :param id:
        :return:
        """
        params = []
        if self._token:
            params.append("token:" + self._token)
        params.append(gid)
        self._send("aria2.getUris", params, id)

    def getFiles(self,gid,id='getFiles'):
        """
        此方法返回以gid（字符串）表示下载的文件列表。响应是包含以下键的结构数组。值是字符串。
        index   ：文件的索引，从1开始，与文件在多文件torrent中的显示顺序相同。
        path    ：文件路径。
        length  ：文件大小（以字节为单位）。
        completedLength ：此文件的完整长度（以字节为单位）。请注意，的总和可能completedLength小于 方法completedLength返回的总和aria2.tellStatus()。这是因为，completedLength在 aria2.getFiles() 仅包括完成作品。在另一方面，completedLength 在aria2.tellStatus()还包括部分完成的块。
        selected ：true如果通过--select-file选项选择了此文件。如果 --select-file未指定，或者这是单文件洪流或根本不是洪流下载，则此值始终为true。否则 false。
        uris ：返回此文件的URI列表。元素类型与aria2.getUris()方法中使用的结构相同。
        :param gid:
        :param id:
        :return:
        """

        params = []
        if self._token:
            params.append("token:" + self._token)
        params.append(gid)
        self._send("aria2.getFiles", params, id)

    def getPeers(self,gid,id='getPeers'):
        """
        此方法返回由gid（字符串）表示的下载列表的同级对象。此方法仅适用于BitTorrent。响应是一个结构数组，包含以下键。值是字符串。
        peerId  ：百分比编码的对等ID。
        ip      ：对端的IP地址。
        port    ：对等体的端口号。
        bitfield：对等体下载进度的十六进制表示形式。最高位对应于索引为0的作品。置位表示作品可用，未置位表示作品缺失。最后的任何备用位都设置为零。
        amChoking：true如果aria2使同伴窒息。否则false。
        peerChoking：true如果同伴正在窒息aria2。否则false。
        downloadSpeed：该客户端从对等方获得的下载速度（字节/秒）。
        uploadSpeed：此客户端上载到对等方的上载速度（字节/秒）。
        seeder：true如果此对等方是播种机。否则false。
        :param gid:
        :param id:
        :return:
        """
        params = []
        if self._token:
            params.append("token:" + self._token)
        params.append(gid)
        self._send("aria2.getPeers", params, id)

    def getServers(self,gid,id='getServers'):
        """
        此方法返回以gid（字符串）表示的下载的当前连接的HTTP（S）/ FTP / SFTP服务器。响应是一个结构数组，包含以下键。值是字符串。
        index   ：从1开始的文件索引，与文件在多文件metalink中出现的顺序相同。
        servers     ：包含以下键的结构列表。
            uri     ：原始URI。
            currentUri      ：这是当前用于下载的URI。如果涉及重定向，则currentUri和uri可能会不同。
            downloadSpeed   ：下载速度（字节/秒）
        :param gid:
        :param id:
        :return:
        """

        params = []
        if self._token:
            params.append("token:" + self._token)
        params.append(gid)
        self._send("aria2.getServers", params, id)

    def tellActive(self,keys=[],id='tellActive'):
        """
        此方法返回活动下载列表。响应是与aria2.tellStatus()方法返回的结构相同的数组。
        对于keys参数，请参考该aria2.tellStatus()方法。
        :param keys: keys参数，请参考该aria2.tellStatus()方法
        :param id:
        :return:
        """

        params=[]
        if self._token:
            params.append("token:"+self._token)
        if keys :
            params.append(keys)
        self._send("aria2.tellActive",params,id)

    def tellWaiting(self,offset,num,keys=[],id="tellWaiting"):
        """
        此方法返回等待下载的列表，包括暂停的下载。 offset是一个整数，它指定从前面等待下载的偏移量。
        num是整数，并指定最大值。返回的下载数量。对于keys参数，请参考该aria2.tellStatus()方法。
        :param offset:offset是正整数，则此方法返回在[ offset，offset + num）范围内的下载
        ffset为负整数。offset == -1指向等待队列中的最后一次下载，offset == -2指向最后一次下载前的下载，依此类推。然后，响应中的下载​​将以相反的顺序进行。
        :param num:
        :param keys: keys参数，请参考该aria2.tellStatus()方法。
        :return: 响应是与aria2.tellStatus()方法返回的结构相同的数组 。
        """
        params = []
        if self._token:
            params.append("token:" + self._token)

        params.append(offset)
        params.append(num)
        params.append(keys)
        self._send("aria2.tellWaiting", params, id)

    def tellStopped(self,offset,num,keys=[],id="tellStopped"):
        """
        此方法返回已停止下载的列表。 offset是一个整数，指定距最近停止下载的位置的偏移量。
        num是整数，并指定最大值。返回的下载数量。对于keys参数，请参考该aria2.tellStatus()方法。
        :param offset:
        :param num:
        :param keys:
        :return:
        """
        params = []
        if self._token:
            params.append("token:" + self._token)

        params.append(offset)
        params.append(num)
        params.append(keys)
        self._send("aria2.tellStopped", params, id)

    def changePosition(self,gid,pos,how,id='changePosition' ):
        """
        此方法更改队列中gid表示的下载位置 。
        :param gid: 下载任务唯一id
        :param pos: POS_SET，它会将下载相对于队列的开始位置。
                    POS_CUR，它会将下载到相对于当前位置的位置。
                    POS_END，它会将下载相对于队列末尾的位置。
        :param how: 当前位置的偏移量  +1  -1
        :return:
        """

        params = []
        if self._token:
            params.append("token:" + self._token)

        params.append(gid)
        params.append(how)
        params.append(pos)

        self._send("aria2.changePosition", params, id)

    def changeUri(self,gid,fileIndex,delUris,addUris ,position=None,id='changeUri'):
        """
        此方法删除的URI的delUris从和追加的URI中 addUris下载由表示GID。
        :param gid:
        :param fileIndex:fileIndex用于选择要删除/附加给定URI的文件
        :param delUris:
        :param addUris:
        :param position:指定在现有的等待URI列表中插入URI的位置。省略position，则URI会附加到列表的后面
        :param id:
        :return:
        """
        params = []
        if self._token:
            params.append("token:" + self._token)

        params.append(gid)
        params.append(fileIndex)
        params.append(delUris)
        params.append(addUris)
        if position:
            params.append(position)

        self._send("aria2.changePosition", params, id)

    def getOption(self,gid,id='getOption'):
        """
        此方法返回以gid表示的下载选项。
        :param gid: 下载任务唯一ID
        :return:
        """
        params = []
        if self._token:
            params.append("token:" + self._token)
        params.append(gid)
        self._send("aria2.getOption", params, id)

    def changeOption(self,gid,options,id='changeOption'):
        """
        此方法动态更改由gid（字符串）表示的下载选项。
        :param gid:
        :param options: 配置项
        :return:
        """
        params = []
        if self._token:
            params.append("token:" + self._token)
        params.append(gid)
        params.append(options)
        self._send("aria2.changeOption", params, id)

    def getGlobalOption(self,id='getGlobalOption'):
        """
        此方法返回全局选项。
        :param id:
        :return:
        """
        params = []
        if self._token:
            params.append("token:" + self._token)
        self._send("aria2.getGlobalOption", params, id)

    def changeGlobalOption(self,options,id='changeGlobalOption'):
        """
        此方法动态更改全局选项。 options是一个结构。
        :param options:
        :param id:
        :return:
        """
        params = []
        if self._token:
            params.append("token:" + self._token)
        params.append(options)
        self._send("aria2.changeGlobalOption", params, id)

    def getGlobalStat(self,id='getGlobalStat'):
        """
        此方法返回全局统计信息，例如总体下载和上传速度。
        downloadSpeed   ：总体下载速度（字节/秒）。
        uploadSpeed     ：整体上传速度（字节/秒）。
        numActive       ：活动下载数。
        numWaiting      ：等待下载的次数。
        numStopped      ：当前会话中已停止的下载数。该值由--max-download-result选项限制。
        numStoppedTotal ：当前会话中已停止的下载次数，但不受 该--max-download-result选项的限制。
        :param id:
        :return:
        """
        params = []
        if self._token:
            params.append("token:" + self._token)
        self._send("aria2.getGlobalStat", params, id)

    def purgeDownloadResult(self,id='purgeDownloadResult'):
        """
        此方法将完成/错误/删除的下载清除到可用内存中。此方法返回OK。
        :param id:
        :return:
        """
        params = []
        if self._token:
            params.append("token:" + self._token)
        self._send("aria2.purgeDownloadResult", params, id)

    def removeDownloadResult(self,gid,id='removeDownloadResult'):
        """
        此方法 从内存中移除由gid表示的已完成/错误/已删除下载。此方法返回OK成功。
        :param id:
        :return:
        """
        params = []
        if self._token:
            params.append("token:" + self._token)
        params.append(gid)
        self._send("aria2.removeDownloadResult", params, id)

    def getVersion(self,id='getVersion'):
        """
        此方法返回aria2的版本和已启用功能的列表。响应是一个结构，包含以下键。
            version         ：aria2的版本号作为字符串。
            enabledFeatures ：启用的功能列表。每个功能都以字符串形式给出。
        :param id:
        :return:
        """
        params = []
        if self._token:
            params.append("token:" + self._token)
        return self._send('aria2.getVersion',params,id)

    def getSessionInfo(self,id='getSessionInfo'):
        """
        此方法返回会话信息。响应是一个结构，并包含以下键。
        sessionId每次调用aria2时生成的会话ID。
        :param id:
        :return:
        """
        params = []
        if self._token:
            params.append("token:" + self._token)
        self._send("aria2.getSessionInfo", params, id)

    def shutdown(self,id="shutdown"):
        """
        此方法将关闭aria2()。
        :param id:
        :return:
        """
        params = []
        if self._token:
            params.append("token:" + self._token)
        self._send("aria2.shutdown", params, id)

    def forceShutdown(self,id='forceShutdown'):
        """
        此方法将关闭aria2()。 强制
        :param id:
        :return:
        """
        params = []
        if self._token:
            params.append("token:" + self._token)
        self._send("aria2.forceShutdown", params, id)

    def saveSession(self,id='saveSession'):
        """
        此方法将当前会话保存到该--save-session选项指定的文件中 。OK如果成功，则此方法返回。
        :param id:
        :return:
        """
        params = []
        if self._token:
            params.append("token:" + self._token)
        self._send("aria2.saveSession", params, id)

    def S_multicall(self,methods,id="S_multicall"):
        """
        此方法将多个方法调用封装在单个请求中。 方法是一个结构数组。该结构包含两个键： methodName和params。
         methodName是要调用的方法名称，并且params是包含方法调用参数的数组。此方法返回响应数组。
         如果封装的方法调用失败，则元素将是包含方法调用的返回值的单项数组，或者是故障元素的结构。
        :param methods:方法是一个结构数组。
        :return:
        """
        params = []
        if self._token:
            params.append("token:" + self._token)

        params.append(methods)
        self._send("system.multicall", params, id)

    def S_listNotifications(self,id='S_listNotifications'):
        """
        system.listNotifications
        此方法以字符串数组形式返回所有可用的RPC方法。与其他方法不同，此方法不需要秘密令牌。这是安全的，因为此方法仅返回可用的方法名称。
        :param id:
        :return:
        """
        params = []
        if self._token:
            params.append("token:" + self._token)

        self._send("system.listNotifications", params, id)

    def S_listMethods(self,id='S_listMethods'):
        """
        system.listMethods
        此方法以字符串数组形式返回所有可用的RPC方法。与其他方法不同，此方法不需要秘密令牌。这是安全的，因为此方法仅返回可用的方法名称。
        :param id:
        :return:
        """
        return self._send('system.listMethods',id=id)

    def _shutdown(self):
        """
        关闭aria2服务器
        :return:
        """
        params = []
        if self._token:
            params.append("token:" + self._token)
        return self._send("aria2.shutdown", params)

    def close(self):
        """
        关闭aria2服务器 并结束接收线程
        :return:
        """
        self._isrecv=False
        self._shutdown()



