import { useEffect, useState } from "react";
import api from "../api/axios";
import "./home.css";

const Home = () => {
  const [loading, setLoading] = useState(true);
  const [ready, setReady] = useState(false);

  useEffect(() => {
    const bootstrap = async () => {
      try {
        // any protected endpoint works
        await api.get("/get-users/");
        setReady(true);
      } finally {
        setLoading(false);
      }
    };

    bootstrap();
  }, []);

  if (loading) {
    return <p className="loading">Loading your workspace…</p>;
  }

  return (
    <div className="home">
      <header className="home-header">
        <h2>RAG Workspace</h2>
        <button className="logout-btn">Logout</button>
      </header>

      <section className="upload-section">
        <h3>Upload Sources</h3>
        <button disabled={!ready}>Upload PDF</button>
        <button disabled={!ready}>Add YouTube URL</button>
      </section>

      <section className="documents">
        <h3>Your Documents</h3>
        <p>No documents uploaded yet.</p>
      </section>

      <section className="chat">
        <h3>Ask a Question</h3>
        <input
          placeholder="Ask something about your documents..."
          disabled={!ready}
        />
        <button disabled={!ready}>Ask</button>
      </section>
    </div>
  );
};

export default Home;
