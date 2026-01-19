import { useState } from "react";
import api from "../api/axios";
import { toast, ToastContainer } from "react-toastify";
import './Dashboard.css'
import { MdDelete } from "react-icons/md";
import { Navigate, useNavigate } from "react-router-dom";

interface PdfDocument{
    id: string;
    name: string
}
interface PdfResponse {
    documents: PdfDocument[];
}
interface Youtube{
    id: string,
    name:string,
    url:string
}



export default function Dashboard(){

    const [pdfs,setPdfs]=useState<PdfDocument[]>([])
    const [urls,setUrls]=useState<Youtube[]>([])

    const navigate=useNavigate()

    const fetchPdfs= async ()=>{
        console.log("Button Pressed")
        try{
            const res=await api.get<PdfResponse>("/upload-pdf/");
            console.log(res)
            setPdfs(res.data.documents)
        }catch(error){
            toast.error("Somehing went wron")
        }
    }
    const fetchUrls=async ()=>{
    try{
        const res=await api.get('/upload/youtube/url/')
        if (res.status!=200){
            toast.error("Documents were not fetched")
            return 
        }
        setUrls(res.data)
    }catch(error){

    }
    }
    const deleteDocument=async(id:string)=>{
        try{
            const res=await api.delete(`/document/delete/${id}/`)
            if (res.status!=204){
                toast.error("Document not Deleted")
            }
          
            toast.success("Document 📟Deleted...",{
                onClose:()=>fetchPdfs()
            })
            // fetchPdfs()
        }catch(error){

        }
    }
    const deleteYoutubeUrl=async(id:string)=>{
        try{
            const res=await api.delete(`/delete/youtube/url/${id}/`)
            if (res.status!=204){
                toast.error("Url not Deleted")
            }
          
            toast.success("Url🔗  Deleted...",{
                onClose:()=>fetchUrls()
            })
            // fetchPdfs()
        }catch(error){

        }
    }

    return (
  <div className="dashboard">
    <ToastContainer
  position="top-right"
  autoClose={1000}        // ⏱ toast visible for 1.5s
  hideProgressBar={true} // optional
  closeOnClick
  pauseOnHover={false}
  draggable={false}
/>
    <div className="dashboard-card">
      <h1>Documents</h1>

      <button onClick={fetchPdfs} className="loadbutton">Load Documents</button>

      <div className="documents">
        {pdfs.length > 0 ? (
          pdfs.map((pdf) => (
            <div className="document-item" key={pdf.id} onClick={() => navigate(`/document/${pdf.id}`)}>
              {pdf.name}
              <button className="del" onClick={()=>deleteDocument(pdf.id)}><MdDelete /></button>
            </div>
          ))
        ) : (
          <p className="empty">No Documents Available</p>
        )}
      </div>
    </div>
    <div className="dashboard-card">
      <h1>Youtube Urls</h1>

      <button onClick={fetchUrls} className="loadbutton">Load Url's</button>

      <div className="documents">
        {urls.length > 0 ? (
          urls.map((url) => (
            <div className="document-item" key={url.id}>
              {url.name}
              <button className="del" onClick={()=>deleteYoutubeUrl(url.id)}><MdDelete /></button>
            </div>
          ))
        ) : (
          <p className="empty">No Documents Available</p>
        )}
      </div>
    </div>
  </div>
);
}