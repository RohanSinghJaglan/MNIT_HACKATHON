@echo off
echo Starting Multi-Agent AI Research Assistant...
echo.

echo Starting MCP Server...
start "MCP Server" cmd /k "python research_server.py"

timeout /t 5 /nobreak >nul

echo Starting Streamlit Application...
streamlit run research_client_ui.py

pause
