---
title: MCP (Model Context Protocol) Best Practices
inclusion: always
---

# MCP (Model Context Protocol) Best Practices

## Server Configuration
- Use workspace-level config (`.kiro/settings/mcp.json`) for project-specific servers
- Use user-level config (`~/.kiro/settings/mcp.json`) for global/cross-workspace servers
- Workspace config takes precedence over user config for server name conflicts
- Always specify exact versions or use `@latest` for stability
- Always include the fetch server
- Only include AWS related servers when AWS services are involved in a project.

## Installation and Setup
- Use `uvx` command for Python-based MCP servers (requires `uv` package manager)
- Install `uv` via pip, homebrew, or follow: https://docs.astral.sh/uv/getting-started/installation/
- No separate installation needed for uvx servers - they download automatically
- Test servers immediately after configuration, don't wait for issues

## Security and Auto-Approval
- Use `autoApprove` sparingly and only for trusted, low-risk tools
- Review tool capabilities before adding to auto-approve list
- Regularly audit auto-approved tools for security implications
- Consider environment-specific auto-approve settings

## Error Handling and Debugging
- Set `FASTMCP_LOG_LEVEL: "ERROR"` to reduce noise in logs
- Use `disabled: false` to temporarily disable problematic servers
- Servers reconnect automatically on config changes
- Use MCP Server view in Kiro feature panel for manual reconnection

## Common MCP Server Examples
```json
{
  "mcpServers": {
    "fetch": {
      "command": "uvx",
      "args": [
        "mcp-server-fetch@latest"
      ],
      "env": {},
      "disabled": false,
      "autoApprove": []
    },
    "awslabs.aws-documentation-mcp-server": {
      "command": "C:\\Users\\heveri\\AppData\\Roaming\\uv\\tools\\awslabs-aws-documentation-mcp-server\\Scripts\\awslabs.aws-documentation-mcp-server.exe",
      "args": [],
      "env": {
        "FASTMCP_LOG_LEVEL": "ERROR"
      },
      "disabled": false,
      "autoApprove": [
        "search_documentation",
        "read_documentation"
      ]
    },
    "awslabs.aws-pricing-mcp-server": {
      "command": "C:\\Users\\heveri\\AppData\\Roaming\\uv\\tools\\awslabs-aws-pricing-mcp-server\\Scripts\\awslabs.aws-pricing-mcp-server.exe",
      "args": [],
      "env": {
        "FASTMCP_LOG_LEVEL": "ERROR",
        "AWS_REGION": "us-east-1"
      },
      "disabled": false,
      "autoApprove": [
        "get_pricing_service_codes"
      ]
    },
    "awslabs.aws-diagram-mcp-server": {
      "command": "C:\\Users\\heveri\\AppData\\Roaming\\uv\\tools\\awslabs-aws-diagram-mcp-server\\Scripts\\awslabs.aws-diagram-mcp-server.exe",
      "args": [],
      "env": {
        "FASTMCP_LOG_LEVEL": "ERROR"
      },
      "disabled": true,
      "autoApprove": []
    },
    "filesystem": {
      "command": "uvx",
      "args": ["mcp-server-filesystem@latest"],
      "env": {
        "FASTMCP_LOG_LEVEL": "ERROR"
      },
      "disabled": false,
      "autoApprove": ["read_file", "list_directory"]
    },
    "mcp-server-git": {
      "command": "wsl",
      "args": [
        "-d",
        "AmazonWSL",
        "-e",
        "bash",
        "-c",
        "source ~/.local/bin/env && uvx mcp-server-git"
      ],
      "env": {},
      "disabled": false,
      "autoApprove": [
        "git_log",
        "git_diff",
        "git_show",
        "git_status"
      ]
    },
    "mcp-server-sqlite": {
      "command": "wsl",
      "args": [
        "-d",
        "AmazonWSL",
        "-e",
        "bash",
        "-c",
        "source ~/.local/bin/env && uvx mcp-server-sqlite"
      ],
      "env": {},
      "disabled": true,
      "autoApprove": [
        "query",
        "list_tables",
        "describe_table"
      ]
    },
  }
}
```

## Testing MCP Tools
- Test MCP tools immediately after configuration
- Don't inspect configurations unless facing specific issues
- Use sample calls to verify tool behavior
- Test with various parameter combinations
- Document working examples for team reference

## Performance Optimization
- Disable unused servers to improve startup time
- Use specific tool names in auto-approve rather than wildcards
- Monitor server resource usage and adjust as needed
- Consider server-specific environment variables for optimization

## Development Workflow
- Add MCP servers incrementally, test each addition
- Use version pinning for production environments
- Document server purposes and usage in team documentation
- Create project-specific server collections for different use cases

## Troubleshooting
- Check server logs in Kiro's MCP Server view
- Verify `uv` and `uvx` installation if Python servers fail
- Test server connectivity outside of Kiro if needed
- Use command palette "MCP" commands for server management
- Restart servers via MCP Server view rather than restarting Kiro

## Best Practices for Tool Usage
- Understand tool capabilities before first use
- Use descriptive prompts when calling MCP tools
- Handle tool errors gracefully in workflows
- Combine multiple MCP tools for complex tasks
- Cache results when appropriate to avoid repeated calls

## Development Integration
- Use Context7 MCP server to verify dependency compatibility before adding libraries
- Leverage AWS-Knowledge MCP server for current AWS documentation and best practices
- Use aws-api-mcp-server for AWS API interactions and validation
- Reference official sources through MCP servers when available in documentation