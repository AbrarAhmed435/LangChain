import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import "./home.css";
import { Link } from "react-router-dom";
import { toast, ToastContainer } from "react-toastify";

const messages = [
  "😎Search less, Understand More",
  "📄 Chat with your documents in natural language.",
  "🔍 Retrieve the most relevant context instantly.",
  "🧠 Generate grounded answers, not hallucinations.",
  "⚡ Ask complex questions and get precise results.",
  "📚 Turn unstructured data into useful knowledge.",
  "🤖 Powered by Retrieval-Augmented Generation.",
];



const Home = () => {
  const [text, setText] = useState("");
  const [index, setIndex] = useState(0);
  const [charIndex, setCharIndex] = useState(0);
  const navigate = useNavigate();

  // Typewriter effect
  useEffect(() => {
    const current = messages[index];

    if (charIndex < current.length) {
      const timeout = setTimeout(() => {
        setText((prev) => prev + current[charIndex]);
        setCharIndex(charIndex + 1);
      }, 80);
      return () => clearTimeout(timeout);
    } else {
      const timeout = setTimeout(() => {
        setText("");
        setCharIndex(0);
        setIndex((index + 1) % messages.length);
      }, 1500);
      return () => clearTimeout(timeout);
    }
  }, [charIndex, index]);

  return (
    <div className="home">
      <h1>Welcome 👋</h1>

      <h2 className="typewriter">
        {text}
        <span className="cursor">|</span>
      </h2>

      <p className="home-intro">
        A simple platform to explore features, understand the flow,
        and get started quickly.
      </p>

      <button
        className="primary-btn"
        onClick={() => navigate("/dashboard")}
      >
        Get Started →
      </button>
    </div>
  );
};

export default Home;
