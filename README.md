### LLAMA INDEX MICROSERVICE
this is an example a multi services RAG agent that communicates with other processes throught APIs, you can find the list of these apis

myapp
├── app
│   ├── __init__.py          # Create Flask app + register blueprints
│   ├── routes.py            # Flask routes (controllers / API endpoints)
│   ├── services/
│   │   ├── __init__.py
│   │   └── llama_service.py # Encapsulates LlamaIndex logic
│   ├── templates/           # Jinja2 templates for HTML
│   │   └── index.html
│   ├── static/              # CSS, JS, images
│   └── config.py            # App config (keys, model settings, etc.)
├── agents
│   ├──__init__.py
│   ├── agent_starter.py
│   └── base.py
│
├── workflows
│
├── config
│   ├── __init__.py
│   ├── config.py
│   └── settings.py
│
├── loaders
│   ├── __init__.py
│   ├── base.py
│   ├── local.py
│   └── sharepoint.py
│
├── notebooks
│   ├── agents_as_tools.ipynb
│   ├── agent_workflow_multi.ipynb
│   ├── custom_multi_agent.ipynb
│   ├── Evaluate_RAG_with_LlamaIndex_lesson.ipynb
│   ├── Finetuning_RAG_Deep_Memory.ipynb
│   ├── Module_01_LangChain_Basic_Concepts_Recap.ipynb
│   ├── Module_01_LlamaIndex_Introduction.ipynb
│   ├── Module_02_Mastering_Advanced_RAG.ipynb
│   └── structured_outputs.ipynb
│
├── chains
│   └── __init__.py
│
├── prompts
│   └── __init__.py
│
├── training
│   └── __init__.py
│   ├── agentworkflow.jpg
│
├── piplines
│   ├── __init__.py
│   ├── indexing.py
│   ├── ingestion.py
│   ├── query.py
│   └── transformers.py
│
├── storage_manager
│
├── utils
│   ├── chain_utils.py
│   ├── query_helpers.py
│   └── set_env_vars.py
├── vector_stores
│   └── chroma_db
│       └── chroma.sqlite3
│
├── main.py
├── README.md
├── requirements.txt
├── notes.txt
├── run.py
├── starter.py
└── workflow_starter.py
