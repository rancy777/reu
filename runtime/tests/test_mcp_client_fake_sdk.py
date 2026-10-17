import asyncio
import sys
import types
import unittest


class FakeInfo:
    name = "fake"
    version = "0.0.1"


class FakePage:
    def __init__(self, tools, cursor=None):
        self.tools = tools
        self.next_cursor = cursor


class FakeClient:
    def __init__(self, server):
        self.server = server
        self.server_info = FakeInfo()
        self.protocol_version = "2026-07-28"

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        return False

    async def list_tools(self, cursor=None):
        if cursor is None:
            return FakePage([types.SimpleNamespace(name="one")], "next")
        return FakePage([types.SimpleNamespace(name="two")], None)


class FakeParams:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


class MCPClientTests(unittest.IsolatedAsyncioTestCase):
    async def test_list_all_tools_handles_pagination(self):
        fake = types.ModuleType("mcp")
        fake.Client = FakeClient
        fake.StdioServerParameters = FakeParams
        original = sys.modules.get("mcp")
        sys.modules["mcp"] = fake
        try:
            from re_skill.mcp_client import list_all_tools
            tools = await list_all_tools(FakeClient(None))
            self.assertEqual([t.name for t in tools], ["one", "two"])
        finally:
            if original is None:
                sys.modules.pop("mcp", None)
            else:
                sys.modules["mcp"] = original


if __name__ == "__main__":
    unittest.main()
