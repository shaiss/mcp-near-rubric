@echo off
echo Testing NEAR Rubric MCP Server
echo ==============================
echo.
echo Sending request to server.py...
type test_request.json | python near-rubric-mcp\server.py
echo.
echo Done 