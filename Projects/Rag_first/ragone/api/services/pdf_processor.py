
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from ..chroma import vector_store
from ..models import Document


def process_pdf(document_id):

    document = Document.objects.get(id=document_id)

    try:
        print("Initializing Processing....")
        document.processing_status = "processing"
        document.save(update_fields=["processing_status"])

        loader = PyPDFLoader(document.file.path)
        docs = loader.load()

        print("Document Loaded...")

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=300,
            chunk_overlap=20,
            separators=["\n\n", "\n", " ", ""]
        )

        chunks = splitter.split_documents(docs)

        for idx, chunk in enumerate(chunks):
            chunk.metadata.update({
                "user_id": document.user.id,
                "document_id": str(document.id),
                "chunk_index": idx,
                "source": "pdf"
            })

        vector_store.add_documents(chunks)

        document.processing_status = "completed"
        document.save(update_fields=["processing_status"])
        print("Processing Finished...")

    except Exception as e:

        document.processing_status = "failed"
        document.error_message = str(e)

        document.save(
            update_fields=[
                "processing_status",
                "error_message"
            ]
        )