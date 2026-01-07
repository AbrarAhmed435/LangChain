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
from dotenv import load_dotenv

load_dotenv()

model=ChatOpenAI(model='gpt-4o-mini')


from api.serializers import *

# class RegisterView(APIView):
#     permission_classes=[permissions.AllowAny]
#     def post(self,request):
#         serializer=RegisterSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user=serializer.save()
#         return Response({
#             "message":"User Registered Successfully",
#             "user_id":user.id,
#             "user_name":user.username
#         },status=status.HTTP_201_CREATED)
    
class RegisterView(generics.CreateAPIView):
    serializer_class=RegisterSerializer


class GetUsersView(generics.ListAPIView):
    permission_classes=[permissions.AllowAny]
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

        for chunk in chunks:
            chunk.metadata={
                "user_id":request.user.id,
                "document_id":str(document.id)
            }

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


class AskQuestionView(APIView):
    permission_classes=[permissions.IsAuthenticated]

    def post(self,request):
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
            filter={
                "user_id":request.user.id
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








