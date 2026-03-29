import { useState ,useEffect} from "react";
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
    
    const [pdfFile, setPdfFile] = useState<File | null>(null)
const [pdfName, setPdfName] = useState("")
const [youtubeName, setYoutubeName] = useState("")
const [youtubeUrl, setYoutubeUrl] = useState("")

useEffect(()=>{
  fetchPdfs()
  fetchUrls()
},[])

    

    const navigate=useNavigate()
    const uploadPdf = async () => {
  if (!pdfFile || !pdfName) {
    toast.error("Enter name and select file")
    return
  }

  const formData = new FormData()
  formData.append("file", pdfFile)
  formData.append("name", pdfName)

  try {
    const res = await api.post("/upload-pdf/", formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    })

    if (res.status === 201) {
      toast.success("PDF Uploaded 📄")
      setPdfFile(null)
      setPdfName("")
      fetchPdfs()
    }
  } catch (error) {
    toast.error("Upload failed")
  }
}
const uploadYoutube = async () => {
  if (!youtubeName || !youtubeUrl) {
    toast.error("Enter name and url")
    return
  }

  try {
    const res = await api.post("/upload/youtube/url/", {
      name: youtubeName,
      url: youtubeUrl,
    })

    if (res.status === 201) {
      toast.success("Youtube URL Added 🔗")
      setYoutubeName("")
      setYoutubeUrl("")
      fetchUrls()
    }
  } catch (error) {
    toast.error("Upload failed")
  }
}

    const fetchPdfs= async ()=>{
        console.log("Button Pressed")
        try{
            const res=await api.get<PdfResponse>("/upload-pdf/");
            console.log(res)
            setPdfs(res.data.documents)
        }catch(error){
            toast.error("Somehing went wrong")
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
      <div className="upload-section">

  <input
    type="text"
    placeholder="Document Name"
    value={pdfName}
    onChange={(e) => setPdfName(e.target.value)}
  />

  <input
    type="file"
    accept="application/pdf"
    onChange={(e) => setPdfFile(e.target.files?.[0] || null)}
  />

  <button onClick={uploadPdf}>
    Upload PDF
  </button>

</div>

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
      <div className="upload-section">

  <input
    type="text"
    placeholder="Video Name"
    value={youtubeName}
    onChange={(e) => setYoutubeName(e.target.value)}
  />

  <input
    type="text"
    placeholder="Youtube URL"
    value={youtubeUrl}
    onChange={(e) => setYoutubeUrl(e.target.value)}
  />

  <button onClick={uploadYoutube}>
    Upload URL
  </button>

</div>

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