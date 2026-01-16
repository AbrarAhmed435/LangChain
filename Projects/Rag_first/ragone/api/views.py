from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from rest_framework import generics
from api.chroma import vector_store
from langchain_openai import ChatOpenAI
from langchain_community.document_loaders import YoutubeLoader
from langchain_community.document_loaders.youtube import TranscriptFormat
from dotenv import load_dotenv
from urllib.parse import urlparse, parse_qs
from django.shortcuts import get_object_or_404
from api.serializers import *

load_dotenv()

model=ChatOpenAI(model='gpt-4o-mini')

 
class RegisterView(generics.CreateAPIView):
    serializer_class=RegisterSerializer


class GetUsersView(generics.ListAPIView):
    permission_classes=[permissions.IsAdminUser]
    queryset=CustomUser.objects.all()
    serializer_class=UserSerializer


class LoginView(APIView):
    permission_classes=[permissions.AllowAny]

    def post(self,request):
        serializer=LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user=serializer.validated_data['user']
        refresh=RefreshToken.for_user(user)
        return Response({ 
            "access":str(refresh.access_token),
            "refresh":str(refresh)
        },status=status.HTTP_200_OK)
    
    """
Input data (request.data)
        ↓
serializer.is_valid()
        ↓
    - Check individual fields
    - Call validate()
        ↓
serializer.validated_data
        ↓
View can use validated_data['user'], etc.
    """


class DocumentUploadView(APIView):
    permission_classes=[permissions.IsAuthenticated]

    def post(self,request):
        serializer=DocumentUploadSerializer(
            data=request.data,
            context={"request":request}
        )
        serializer.is_valid(raise_exception=True)
        document=serializer.save()

        loader=PyMuPDFLoader(document.file.path)
        docs=loader.load()
        # print(len(docs))

        splitter=RecursiveCharacterTextSplitter(
            chunk_size=300,
            chunk_overlap=20,
            separators=["\n\n", "\n", " ", ""]
        )

        chunks=splitter.split_documents(docs)
        # print(len(chunks))
        # print(chunks[-1].page_content)

        for idx,chunk in enumerate(chunks):
            chunk.metadata.update({
                "user_id":request.user.id,
                "document_id":str(document.id),
                "chunk_index":idx,
                "source":"pdf"
            })

        vector_store.add_documents(chunks)
        info = vector_store.get()
        print("Number of embeddings:", len(info["ids"]))

        return Response({
            "id":document.id,
            "name":document.name,
            "message":"pdf uploaded successfully"
        },status=status.HTTP_201_CREATED)


class DestroyDocumentView(generics.DestroyAPIView):
    permission_classes=[permissions.IsAuthenticated]
    serializer_class=[DocumentUploadSerializer]

    def get_queryset(self):
        return Document.objects.filter(user=self.request.user)
    
    def perform_destroy(self, instance):
        vector_store.delete(
            where={
                # "user_id":self.request.user.id,
                "document_id":str(instance.id),
            }
        )
        instance.delete() # default perform_destroy() has only this line 

class YoutubeUploadView(generics.ListCreateAPIView):
    permission_classes=[permissions.IsAuthenticated]
    serializer_class=YoutubeUploadSerializer

    def get_queryset(self):
        return YoutubeVideo.objects.filter(user=self.request.user)
    
    def extract_video_id(self,url: str) -> str | None:
        parsed = urlparse(url)

        # youtu.be/<id>
        if parsed.netloc in ("youtu.be", "www.youtu.be"):
            return parsed.path.lstrip("/")

        # youtube.com/watch?v=<id>
        if parsed.path == "/watch":
            return parse_qs(parsed.query).get("v", [None])[0]

        # youtube.com/shorts/<id>
        if parsed.path.startswith("/shorts/"):
            return parsed.path.split("/")[2]

        return None

    def perform_create(self,serializer):
        youtube_url=serializer.validated_data['url']
        video_name=serializer.validated_data['name'
                                             ]
        video_id=self.extract_video_id(youtube_url)
        if not video_id:
            raise serializers.ValidationError("Invalid Youtube URL")
        #Check is video exists in db for user
        user_video=YoutubeVideo.objects.filter(user=self.request.user,video_id=video_id)
        if user_video.exists():
            raise serializers.ValidationError({
                "error":"Video already present in database"
            })

        
        
        video=serializer.save(
            user=self.request.user,
            video_id=video_id
        )

        loader=YoutubeLoader.from_youtube_url(
            youtube_url,
            add_video_info=False,
            language=['en','hi'],
            transcript_format=TranscriptFormat.CHUNKS,
            chunk_size_seconds=40
        )
        try:
            docs=loader.load()
        except Exception as e:
            video.delete()
            raise serializers.ValidationError("Could not fetch Youtube transcript")
        for idx,doc in enumerate(docs):
            doc.metadata.update({
                "video_name":video_name,
                "user_id":self.request.user.id,
                "source":"youtube",
                "document_id":str(video.id),
                "video_id":video_id,
                "chunk_index":idx,
            })
        vector_store.add_documents(docs)
class YoutubeDelete(generics.DestroyAPIView):
    permission_classes=[permissions.IsAuthenticated]
    serializer_class=YoutubeUploadSerializer

    def get_queryset(self):
        return YoutubeVideo.objects.filter(user=self.request.user)
    
    def perform_destroy(self, instance):
        #deleting in chroma
        vector_store.delete(
            where={
                # "user_id":self.request.user.id,
                "document_id":str(instance.id),
            }
        )

        # for deleting in django db
        instance.delete() # for deleting in django db


    

class AskQuestionView(APIView):
    permission_classes=[permissions.IsAuthenticated]

    def post(self,request,pk):
        serializer=QuestionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        question=serializer.validated_data["question"]

        # retriever=vector_store.as_retriever(
        #     search_type="mmr",
        #     search_kwargs={"k":3,"lambda_mult":0.3},
        #     filter={
        #         "user_id":request.user.id
        #     }
        # )
        # results=retriever.invoke(question)
        results=vector_store.similarity_search_with_score(
            query=question,
            k=4,
            # where={
            #     "$and":[
            #         {"user_id":request.user.id},
            #         {"document_id":str(pk)}
            #     ]
            # }
            filter={
                "$and":[
                    {"user_id": request.user.id,},
                    {"document_id": str(pk)}
                ]
            }

        )

        response_data=[]
        for doc,score in results:
            response_data.append({
                "content":doc.page_content,
                "score":score,
                "document_id":doc.metadata.get("document_id")
            })
        # if len(response_data):
        #     print(response_data[-1])
        if len(response_data):
            llm_answer=model.invoke(f"Give answer based on mathing sentences, Question= {question} Anwers= \n {response_data}").content
        else:
            llm_answer="No Document Found"
        return Response({
            "Question":question,
            "results":response_data,
            "llm_answer":llm_answer
        },status=status.HTTP_200_OK)

class GenerateSummary(APIView):
    permission_classes=[permissions.IsAuthenticated]

    MODEL_MAP={
        "pdf":Document,
        "youtube":YoutubeVideo
    }

    def generate_summary(self,docs):
        temp=docs
        temp_sum=""
        for i in range(len(temp)-1):
            temp_sum=model.invoke(f"Summarize foollowing content in  150-200(if text is larger if text is smaller you can generate shorter as well) words Start summarize directly without saying \"this is summarization\" of text or any other heading \n Content:{temp_sum+temp[i]+temp[i+1]}").content
            print(temp_sum)
        if len(temp)==1:
            temp_sum=model.invoke(f"Summarize foollowing content in 100 -150(if text is smaller you can generate shorter as well) words Start summarize directly without saying \"this is summarization\" of text or any other heading \n Content:{temp_sum+temp[0]}").content
        
        return temp_sum

        


    def get(self,request,pk):
        # print(pk)
        mydocs = vector_store.get(
            where={
                "$and": [
                    {"document_id": str(pk)},
                    {"user_id": request.user.id}
                ]
            },
            include=["documents", "metadatas"]
        )
        docs = mydocs["documents"]
        metas = mydocs["metadatas"]
        if not metas:
            return Response({
                "detail":"No Content found",
            },status=status.HTTP_404_NOT_FOUND)
        
        ordered_docs = [
            doc for doc, meta in sorted(
                zip(docs, metas),
                key=lambda pair: pair[1]["chunk_index"]
            )
        ]
        if not ordered_docs:
            return Response({
                "detail":"No content available",
            },status=status.HTTP_404_NOT_FOUND)
        # print(ordered_docs)

        source=metas[0].get("source")
        Model=self.MODEL_MAP.get(source)
        if not Model:
            return Response({
                "detail":"Invalid Content Type",
            },status=status.HTTP_400_BAD_REQUEST)


        #db instance
        # from django.shortcuts import get_object_or_404
        instance=get_object_or_404(Model,id=pk,user=request.user)
        if instance.summary:
            summary=instance.summary
        else:    
            summary=self.generate_summary(ordered_docs)
            instance.summary=summary
            instance.save(update_fields=['summary'])

        # print(f"Summary :\n{summary}")

        

        return Response({
            "summary":summary,

        },status=status.HTTP_200_OK)
