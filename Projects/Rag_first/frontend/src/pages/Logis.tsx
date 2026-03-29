import { useState,useEffect } from "react";
import { loginApi } from "../api/auth.api";
import "./Login.css";
import { useNavigate } from "react-router-dom";


import { toast, ToastContainer } from "react-toastify";

const Login=()=>{
    const [email,setEmail]=useState<string>("")
    const [password,setPassword]=useState<string>("")
    const [loading, setLoading] = useState<boolean>(false);

    const navigate=useNavigate()

    useEffect(() => {
  const canvas = document.getElementById('snow-canvas') as HTMLCanvasElement | null;
  if (!canvas) return;

  const card = canvas.parentElement!;
  const ctx = canvas.getContext('2d');
  if (!ctx) return;

  const FLAKES = 90;

  const resize = () => {
    canvas.width = card.offsetWidth;
    canvas.height = card.offsetHeight;
  };

  resize();
  window.addEventListener("resize", resize);

  const flakes = Array.from({ length: FLAKES }, () => ({
    x: Math.random() * canvas.width,
    y: Math.random() * canvas.height,
    r: 1.2 + Math.random() * 2.2,
    speed: 0.4 + Math.random() * 0.9,
    drift: -0.25 + Math.random() * 0.5,
    alpha: 0.35 + Math.random() * 0.5,
    wobble: Math.random() * Math.PI * 2,
    wobbleSpeed: 0.01 + Math.random() * 0.02,
  }));

  let raf: number;

  const draw = () => {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    for (const f of flakes) {
      f.wobble += f.wobbleSpeed;
      f.x += f.drift + Math.sin(f.wobble) * 0.3;
      f.y += f.speed;

      if (f.y > canvas.height + 4) {
        f.y = -4;
        f.x = Math.random() * canvas.width;
      }

      ctx.beginPath();
      ctx.arc(f.x, f.y, f.r, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(200,220,255,${f.alpha})`;
      ctx.fill();
    }

    raf = requestAnimationFrame(draw);
  };

  draw();

  return () => {
    cancelAnimationFrame(raf);
    window.removeEventListener("resize", resize);
  };
}, []);

const handleLogin=async (e:React.FormEvent<HTMLFormElement>)=>{
    e.preventDefault()
    setLoading(true)

    try{
        const res=await loginApi({
            email,
            password,
        });

        localStorage.setItem("access",res.access);
        localStorage.setItem("refresh",res.refresh);
        toast.success("You'r Loged in Redirecting to Home page...", {
          onClose: () => navigate("/home"), // Navigate only after toast closes
        });
    }catch(error){
      toast.error("Invalid credentials")
        console.log("Login Failed",error)
    }finally{
      setLoading(false)
    }

};
return (
  <div className="login-container">
  <ToastContainer
  position="top-right"
  autoClose={1000}        // ⏱ toast visible for 1.5s
  hideProgressBar={true} // optional
  closeOnClick
  pauseOnHover={false}
  draggable={false}
/>

  <h1 className="site-title">RagFirst</h1>
    <div className="login-card">
      <canvas id="snow-canvas"></canvas>
      <h2>Login</h2>

      <form onSubmit={handleLogin}>
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />

        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />

        <button disabled={loading}>{loading? "Logging in ":"Login"}</button>
      </form>
    </div>
  </div>
);

}

export default Login