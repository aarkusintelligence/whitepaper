from diagrams import Diagram, Cluster, Edge
from diagrams.aws.analytics import KinesisDataAnalytics, KinesisDataFirehose, KinesisDataStreams
from diagrams.aws.compute import Lambda
from diagrams.aws.database import RDS, ElastiCache
from diagrams.aws.storage import S3
from diagrams.aws.network import APIGateway, ELB
from diagrams.aws.security import IAM
from diagrams.aws.integration import SQS
from diagrams.aws.ml import Sagemaker
from diagrams.onprem.analytics import Spark
from diagrams.onprem.compute import Server
from diagrams.onprem.database import MongoDB
from diagrams.onprem.monitoring import Grafana, Prometheus
from diagrams.onprem.network import Internet
from diagrams.programming.framework import Flutter, React
from diagrams.saas.chat import Telegram

# Initialize the diagram
with Diagram("Token Analysis AI Agent Architecture", show=False, direction="TB"):
    
    # External Data Sources
    with Cluster("External Data Sources"):
        blockchain = Internet("Blockchain Nodes")
        moralis = Internet("Moralis API")
        social = Internet("Social Media APIs")
        data_sources = [blockchain, moralis, social]
    
    # Data Ingestion Layer
    with Cluster("Data Ingestion Layer"):
        kinesis = KinesisDataStreams("Real-time Streams")
        firehose = KinesisDataFirehose("Data Firehose")
        spark = Spark("Data Processing")
        
        for source in data_sources:
            source >> kinesis
        kinesis >> firehose
        firehose >> spark
    
    # Storage Layer
    with Cluster("Storage Layer"):
        timescale = RDS("TimescaleDB")
        redis = ElastiCache("Redis Cache")
        s3 = S3("Historical Data")
        
        spark >> timescale
        spark >> s3
    
    # AI Core
    with Cluster("AI Core"):
        sagemaker = Sagemaker("AI Models")
        eliza = Server("ElizaOS")
        mongodb = MongoDB("Model Storage")
        
        timescale >> sagemaker
        s3 >> sagemaker
        sagemaker >> mongodb
        eliza >> Edge(color="red", style="dashed") >> sagemaker
    
    # API Layer
    with Cluster("API Layer"):
        api = APIGateway("API Gateway")
        lb = ELB("Load Balancer")
        auth = IAM("Auth Service")
        
        api >> lb
        api >> auth
    
    # Application Services
    with Cluster("Application Services"):
        lambda_prompt = Lambda("Prompt Service")
        lambda_analysis = Lambda("Analysis Service")
        lambda_notify = Lambda("Notification Service")
        queue = SQS("Message Queue")
        
        lb >> lambda_prompt
        lb >> lambda_analysis
        lambda_analysis >> queue
        queue >> lambda_notify
        
        # Connect to AI Core
        lambda_prompt >> sagemaker
        lambda_analysis >> sagemaker
        
        # Connect to Storage
        lambda_prompt >> redis
        lambda_analysis >> timescale
    
    # Client Applications
    with Cluster("Client Applications"):
        web = React("Web App")
        mobile = Flutter("Mobile App")
        telegram = Telegram("Trading Bot")
        
        api >> web
        api >> mobile
        api >> telegram
    
    # Monitoring
    with Cluster("Monitoring"):
        prometheus = Prometheus("Metrics")
        grafana = Grafana("Dashboards")
        
        prometheus >> grafana
        
        # Monitor all services
        lambda_prompt >> Edge(color="gray", style="dotted") >> prometheus
        lambda_analysis >> Edge(color="gray", style="dotted") >> prometheus
        sagemaker >> Edge(color="gray", style="dotted") >> prometheus