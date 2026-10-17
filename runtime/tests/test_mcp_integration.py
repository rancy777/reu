import importlib.util
import unittest
import sys
from pathlib import Path

MCP_AVAILABLE = importlib.util.find_spec("mcp") is not None


@unittest.skipUnless(MCP_AVAILABLE, "official MCP Python SDK is not installed in this build environment")
class MCPIntegrationSmokeTest(unittest.IsolatedAsyncioTestCase):
    async def test_sdk_client_surface(self):
        from mcp import Client, StdioServerParameters

        self.assertTrue(callable(Client))
        params = StdioServerParameters(command="python", args=["-V"])
        self.assertEqual(params.command, "python")

    async def test_official_sdk_connects_to_local_fixture(self):
        from re_skill.mcp_client import connect, list_all_tools, call_tool
        from re_skill.models import ProviderSpec
        fixture = Path(__file__).with_name('fixtures')/'mock_mcp_stdio.py'
        spec = ProviderSpec('sdk-fixture', 'stdio', command=sys.executable, args=[str(fixture)])
        async with connect(spec) as session:
            tools = await list_all_tools(session)
            self.assertEqual([t.name for t in tools], ['get_functions','decompile_function','write_memory'])
            response = await call_tool(session, 'get_functions', {})
            self.assertEqual(response.structured_content['functions'], ['main'])
