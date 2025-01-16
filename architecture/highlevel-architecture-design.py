from diagrams import Diagram, Cluster, Edge
from diagrams.generic.compute import Rack
from diagrams.onprem.database import MongoDB as Storage
from diagrams.generic.network import Switch
from diagrams.generic.place import Datacenter
from diagrams.onprem.client import Users
from diagrams.onprem.network import Internet
from diagrams.programming.framework import React
from diagrams.saas.chat import Telegram

# Diagram configuration
graph_attr = {
    "fontsize": "45",
    "bgcolor": "transparent",
    "splines": "ortho",
    "pad": "0.5"
}

cluster_attr = {
    "fontsize": "12",
    "bgcolor": "lightgray",
    "padding": "15"
}

# Create the diagram
with Diagram(
    "Token Analysis AI Agent Architecture Highlevelcd arch",
    show=False,
    direction="TB",
    graph_attr=graph_attr
):
    # Data Sources
    with Cluster("External Data Layer", graph_attr=cluster_attr):
        blockchain = Internet("Blockchain\nNodes")
        market = Internet("Market\nData")
        social = Internet("Social\nMedia")
        
        data_sources = [blockchain, market, social]

    # Core Processing
    with Cluster("Core Processing Layer", graph_attr=cluster_attr):
        # Data Processing
        with Cluster("Data Pipeline"):
            ingestion = Switch("Data\nIngestion")
            storage = Storage("Data\nStorage")
            
            ingestion >> storage

        # AI Processing
        with Cluster("AI Engine"):
            ai_models = Rack("AI Models")
            eliza = Rack("ElizaOS")
            analyzer = Rack("Analysis\nEngine")
            
            storage >> ai_models
            ai_models >> analyzer
            eliza >> analyzer

    # Service Layer
    with Cluster("Service Layer", graph_attr=cluster_attr):
        gateway = Switch("API Gateway")
        auth = Rack("Auth Service")
        cache = Storage("Cache")
        
        analyzer >> cache
        cache >> gateway
        auth >> gateway

    # Client Applications
    with Cluster("Application Layer", graph_attr=cluster_attr):
        web = React("Web App")
        mobile = Users("Mobile App")
        trading = Telegram("Trading Bot")
        
        clients = [web, mobile, trading]

    # System Management
    with Cluster("Management Layer", graph_attr=cluster_attr):
        monitor = Datacenter("Monitoring")
        alerts = Datacenter("Alerts")
        
        monitor - alerts

    # Connect layers
    for source in data_sources:
        source >> ingestion

    for client in clients:
        gateway >> client

    # Monitoring connections
    monitor >> Edge(style="dotted", color="gray") >> ingestion
    monitor >> Edge(style="dotted", color="gray") >> ai_models
    monitor >> Edge(style="dotted", color="gray") >> gateway

    # Add edge labels
    Edge(color="blue", label="Data Flow")
    Edge(style="dotted", color="gray", label="Monitoring")