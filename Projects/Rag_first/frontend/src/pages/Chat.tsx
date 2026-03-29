import { useState } from "react";
import { useParams } from "react-router-dom";
import api from "../api/axios";
import { toast, ToastContainer } from "react-toastify";
import ReactMarkdown from "react-markdown";
import "./Chat.css";

export default function Chat() {
  const { id } = useParams<{ id: string }>();
  const [response, setResponse] = useState("");
  const [question, setQuestion] = useState("");
  const [loading, setLoading] = useState(false);
  const [summary, setSummary] = useState("")
const [loadingSummary, setLoadingSummary] = useState(false)

  const handleQuery = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    if (!id) return;

    try {
      setLoading(true);

      const res = await api.post(`/ask/${id}/`, {
        question: question,
      });

      if (res.status !== 200) {
        toast.error("Something went wrong");
        return;
      }

      setResponse(res.data.llm_answer);
      setQuestion("");
    } catch {
      toast.error("Something went wrong");
    } finally {
      setLoading(false);
    }
  };
  const handleSummary = async () => {
  if (!id) return

  try {
    setLoadingSummary(true)

    const res = await api.get(`/summarize/${id}/`)

    if (res.status !== 200) {
      toast.error("Failed to generate summary")
      return
    }

    setSummary(res.data.summary || res.data)

  } catch {
    toast.error("Something went wrong")
  } finally {
    setLoadingSummary(false)
  }
}

  return (
    <div className="chat-page">
      <ToastContainer autoClose={1200} hideProgressBar />
      <button className="summary-btn" onClick={handleSummary} disabled={loadingSummary}>
  {loadingSummary ? "Generating Summary..." : "Generate Summary"}
</button>

      <form onSubmit={handleQuery} className="chat-form">
        <input
          type="text"
          placeholder="Ask a question about your document..."
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          required
        />
        <button type="submit" disabled={loading}>
          {loading ? "Thinking..." : "Ask"}
        </button>
      </form>
      {summary && (
  <div className="chat-summary">
    <ReactMarkdown>{summary}</ReactMarkdown>
  </div>
)}

      {response && (
        <div className="chat-response">
          <ReactMarkdown>{response}</ReactMarkdown>
        </div>
      )}
    </div>
  );
}
