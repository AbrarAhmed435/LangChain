import { useState } from "react";
import { loginApi } from "../api/auth.api";
import "./Login.css";
import { useNavigate } from "react-router-dom";

import { toast, ToastContainer } from "react-toastify";

const Login=()=>{
    const [email,setEmail]=useState<string>("")
    const [password,setPassword]=useState<string>("")
    const [loading, setLoading] = useState<boolean>(false);

    const navigate=useNavigate()

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


    <div className="login-card">
      <h2>Login</h2>

      <form onSubmit={handleLogin}>
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />

        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />

        <button disabled={loading}>{loading? "Logging in ":"Login"}</button>
      </form>
    </div>
  </div>
);

}

export default Login