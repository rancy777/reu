import sys
import types
import unittest
from unittest.mock import patch
from re_skill.mcp_client import _LegacySessionFacade

class FakeSession:
    def __init__(self): self.params=[]
    async def list_tools(self, **kw):
        self.params.append(kw)
        return types.SimpleNamespace(tools=[],next_cursor=None)
    async def call_tool(self,name,args): return (name,args)

class LegacySSEFacadeTests(unittest.IsolatedAsyncioTestCase):
    async def test_client_session_cursor_is_adapted(self):
        fake = types.ModuleType('mcp.types')
        class Params:
            def __init__(self,cursor=None): self.cursor=cursor
        fake.PaginatedRequestParams=Params
        session=FakeSession()
        init=types.SimpleNamespace(server_info=types.SimpleNamespace(name='legacy',version='1'),protocol_version='2025-06-18')
        with patch.dict(sys.modules, {'mcp.types':fake}):
            client=_LegacySessionFacade(session,init)
            await client.list_tools()
            await client.list_tools(cursor='PAGE-2')
            self.assertEqual(session.params[0],{})
            self.assertEqual(session.params[1]['params'].cursor,'PAGE-2')
            self.assertEqual(await client.call_tool('list',{}),('list',{}))
