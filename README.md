## Project Description

**This repository provides a complete and scalable toolkit for building, deploying, and interacting with AI agents using the powerful LangGraph framework, combined with FastAPI and Streamlit.** It offers an **end-to-end solution** covering everything from agent creation to a user-friendly chat interface, designed to accelerate your AI development workflow.

The toolkit includes:

* A **LangGraph Agent** that leverages graph-based language modeling for intelligent, context-aware interactions.
* A **FastAPI Service** that hosts and serves the LangGraph agent with high performance and scalability.
* A lightweight **Python Client** for seamless communication with the API service, enabling easy programmatic access.
* An intuitive **Streamlit Chat App** providing a clean, interactive, real-time user interface without frontend development overhead.
* All data structures and configurations are built with **Pydantic**, ensuring robust data validation, clear typing, and easy customization.

This project is ideal for developers, data scientists, and researchers who want a **full-stack AI agent solution** with modular, extensible architecture, leveraging FastAPI’s asynchronous speed and Streamlit’s simplicity. It serves as a **ready-to-use template** for building conversational agents, personal assistants, customer support bots, or experimental AI tools.

By combining these technologies, the toolkit simplifies the process of creating, running, and interacting with LangGraph-powered AI agents—making it easier than ever to prototype, deploy, and demo intelligent language-based applications.

## Architecture Diagram

![Architecture Diagram](https://github.com/imtiyazahmed1650/LangAgentToolkit/blob/b00370708cca7842fd7e25439b04f0c8768bd177/agent_architecture%20(1).png)

## Key Features

- **LangGraph Agent with Latest Features**: A highly customizable agent built on the LangGraph framework (v0.3), incorporating advanced capabilities such as **human-in-the-loop control with `interrupt()`**, **flow management via `Command`**, **long-term memory through `Store`**, and monitoring with **`langgraph-supervisor`**.
- **FastAPI Service**: Efficiently serves the agent with both **streaming and non-streaming API endpoints**, enabling flexible interaction modes.
- **Advanced Streaming Support**: Innovative handling of both **token-based and message-based streaming** for real-time response delivery.
- **Streamlit Chat Interface**: A **user-friendly, web-based chat UI** built with Streamlit to easily interact with the AI agent without additional frontend setup.
- **Multiple Agent Support**: Run and manage **multiple agents simultaneously** within the service, accessible via distinct URL paths. Agent and model details are available at `/info`.
- **Asynchronous Architecture**: Leveraging Python’s **`async/await`** for high-performance concurrent request handling.
- **Content Moderation**: Integrates **LlamaGuard** for safe content filtering (**requires Groq API key**).
- **Feedback System**: **Star-based feedback mechanism** seamlessly integrated with **LangSmith** to collect user evaluations.

- **Robust Testing**: Comprehensive **unit and integration tests** covering the entire codebase to ensure reliability and maintainability.

 **Note:** This project uses **free-tier or open-source language models** rather than paid OpenAI APIs, making it accessible without incurring usage costs.
