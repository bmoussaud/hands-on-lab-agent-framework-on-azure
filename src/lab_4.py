import asyncio
import os
from agent_framework.azure import AzureAIAgentClient
from agent_framework import ChatAgent, HostedMCPTool
from azure.identity.aio import AzureCliCredential
from dotenv import load_dotenv
from models.issue_analyzer import IssueAnalyzer

load_dotenv()


async def create_issue_analyzer_agent(chat_client: AzureAIAgentClient) -> ChatAgent:
    return ChatAgent(
        chat_client=chat_client,
        instructions="You are analyzing issues.",
        name="IssueAnalyzerAgent",
        response_format=IssueAnalyzer,
    )


async def create_ms_learn_agent(chat_client: AzureAIAgentClient) -> ChatAgent:
    return ChatAgent(
        chat_client=chat_client,
        name="DocsAgent",
        instructions="You are a helpful assistant that can help with microsoft documentation questions.",
        tools=HostedMCPTool(
            name="Microsoft Learn MCP",
            url="https://learn.microsoft.com/api/mcp",
            description="A Microsoft Learn MCP server for documentation questions",
            approval_mode="never_require",
        ),
    )


async def create_github_agent(chat_client: AzureAIAgentClient) -> ChatAgent:
    return ChatAgent(
        chat_client=chat_client,
        name="GitHubAgent",
        instructions="""
                You are a helpful assistant that can create an issue on the user's GitHub repository.
                To summmarize an issue, use the GitHub MCP tool. 
            """,
        tools=HostedMCPTool(
            name="GitHub MCP",
            url="https://api.githubcopilot.com/mcp",
            description="A GitHub MCP server for GitHub interactions",
            approval_mode="never_require",
            # PAT token, restricting which repos the MCP Server
            headers={
                "Authorization": f"Bearer {os.environ['GITHUB_MCP_PAT']}",
            },
        ),
    )


async def main():
    settings = {
        "project_endpoint": os.environ["AZURE_AI_PROJECT_ENDPOINT"],
        "model_deployment_name": os.environ["AZURE_AI_MODEL_DEPLOYMENT_NAME"],
        "async_credential": AzureCliCredential(),
    }

    async with (
        AzureAIAgentClient(**settings).create_agent(
            name="GitHubAgent",
            instructions="""
                    You are a helpful assistant that can create an issue on the user's GitHub repository.
                    To summmarize an issue, use the GitHub MCP tool. 
                """,
            tools=HostedMCPTool(
                name="GitHub MCP",
                url="https://api.githubcopilot.com/mcp",
                description="A GitHub MCP server for GitHub interactions",
                approval_mode="never_require",
                # PAT token, restricting which repos the MCP Server
                headers={
                    "Authorization": f"Bearer {os.environ['GITHUB_MCP_PAT']}",
                },
            ),
        ) as github_agent,
        AzureAIAgentClient(**settings).create_agent(
            instructions="You are analyzing issues.",
            name="IssueAnalyzerAgent",
            response_format=IssueAnalyzer,
        ) as issue_analyzer_agent,
        AzureAIAgentClient(**settings).create_agent(
            name="DocsAgent",
            instructions="You are a helpful assistant that can help with microsoft documentation questions.",
            tools=HostedMCPTool(
                name="Microsoft Learn MCP",
                url="https://learn.microsoft.com/api/mcp",
                description="A Microsoft Learn MCP server for documentation questions",
                approval_mode="never_require",
            ),
        ) as ms_learn_agent,
    ):
        github_result = await github_agent.run(
            "Create an issue on hands-on-lab-agent-framework-on-azure repo about adding a new feature to support Azure Functions."
        )
        print(github_result.text)

        result = await issue_analyzer_agent.run("""
                    Traceback (most recent call last):
                        File "<string>", line 38, in <module>
                            main_application()                    ← Entry point
                        File "<string>", line 30, in main_application
                            results = process_data_batch(test_data)  ← Calls processor
                        File "<string>", line 13, in process_data_batch
                            avg = calculate_average(batch)        ← Calls calculator
                        File "<string>", line 5, in calculate_average
                            return total / count                  ← ERROR HERE
                                ~~~~~~^~~~~~~
                        ZeroDivisionError: division by zero
                                    """)
        print(result.text)

        agent_result = await ms_learn_agent.run(
            "How do I create a virtual machine in Azure?"
        )
        print(agent_result.text)


if __name__ == "__main__":
    asyncio.run(main())
