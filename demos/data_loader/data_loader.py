import json
import chromadb
from llama_index.core import StorageContext, VectorStoreIndex, Settings
from llama_index.core.node_parser import CodeSplitter
from llama_index.core.schema import Document
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.vector_stores.chroma import ChromaVectorStore
import os
import click
import psycopg2
import requests as req
from dotenv import load_dotenv
from psycopg2.extras import NamedTupleCursor
import utils

load_dotenv(dotenv_path=".env")

# logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
# logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

# Default Chroma DB collection name
CT_RAG_COLLECTION = "CT_RAG"


def get_latest_nct_ids(count):
    db_username = os.getenv("AACT_USERNAME")
    db_password = os.getenv("AACT_PASSWORD")

    if not db_username or not db_password:
        print("Please make sure AACT_USERNAME and AACT_PASSWORD env variables are set in .env")
        return

    conn = psycopg2.connect(
        host="aact-db.ctti-clinicaltrials.org",
        database="aact",
        user=db_username,
        password=db_password,
        port="5432",
        cursor_factory=NamedTupleCursor
    )

    query = f"select nct_id from studies order by updated_at desc limit {count}"

    with conn:
        with conn.cursor() as curs:
            curs.execute(query)
            nct_ids = [rec.nct_id for rec in curs.fetchall()]

    return nct_ids


def get_trial(nct_id):
    trial = req.get(f"https://clinicaltrials.gov/api/v2/studies/{nct_id}")
    trial_json = trial.json()
    return trial_json


def create_document(target_json, nct_id):
    document = Document(
        text=json.dumps(target_json, indent=2),
        id_=f"doc_{nct_id}"
    )
    return document


def create_nodes(docs):
    code_splitter = CodeSplitter(
        language="json",
        chunk_lines=40,
        chunk_lines_overlap=15,
        max_chars=1500
    )
    nodes = code_splitter.get_nodes_from_documents(docs)
    return nodes


@click.command()
@click.option("--nct_id", default=None)
@click.option("--nct_count", type=click.INT)
def load_data(nct_id, nct_count):
    if nct_id is None and nct_count is None:
        raise click.UsageError("Either nct_id or nct_count must be specified")
    if nct_id and nct_count:
        raise click.UsageError("Only one of nct_id or nct_count can be specified")

    nct_ids = []
    docs = []

    if nct_id:
        nct_ids.append(nct_id)
    if nct_count:
        click.echo(f"Getting {nct_count} latest trials...")
        nct_id_list = get_latest_nct_ids(count=nct_count)
        nct_ids.extend(nct_id_list)

    for nct_id in nct_ids:
        click.echo(f"Getting the trial with id {nct_id}...")
        trial_json = get_trial(nct_id)
        target_json = utils.build_target_json(trial_json)
        document = create_document(target_json, nct_id)
        docs.append(document)

    print("Splitting documents into chunks (nodes)")
    nodes = create_nodes(docs)
    embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
    print("Reading persistent Chroma DB from file system")
    db = chromadb.PersistentClient(path="chroma_db")
    print(f"Looking for the {CT_RAG_COLLECTION} collection in the database..." )
    if CT_RAG_COLLECTION not in [col.name for col in db.list_collections()]:
        print(f"{CT_RAG_COLLECTION} collection was not found in Chroma DB, creating...")
        chroma_collection = db.create_collection(CT_RAG_COLLECTION)
        print("Creating vector store...")
        vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
        storage_context = StorageContext.from_defaults(vector_store=vector_store)

        Settings.embed_model = embed_model
        Settings.llm = None

        print("Creating vector store index")
        VectorStoreIndex(
            nodes=nodes,
            storage_context=storage_context,
            store_nodes_override=True
        )
    else:
        print(f"{CT_RAG_COLLECTION} collection was found in Chroma DB")
        ct_rag_collection = db.get_collection(CT_RAG_COLLECTION)
        vector_store = ChromaVectorStore(chroma_collection=ct_rag_collection)
        print("Restoring vector store index from the collection...")
        index = VectorStoreIndex.from_vector_store(
            vector_store=vector_store,
            embed_model=embed_model,
            store_nodes_override=True
        )
        print("Inserting nodes in the vector store index...")
        index.insert_nodes(nodes)

    print("Done")

if __name__ == "__main__":
    load_data()
