import { useState } from "react";
import { loginApi } from "../api/auth.api";
import "./Login.css";

import { toast, ToastContainer } from "react-toastify";

const Login=()=>{
    const [email,setEmail]=useState<string>("")
    const [password,setPassword]=useState<string>("")

const handleLogin=async (e:React.FormEvent<HTMLFormElement>)=>{
    e.preventDefault()

    try{
        const res=await loginApi({
            email,
            password,
        });

        localStorage.setItem("access",res.access);
        localStorage.setItem("refresh",res.refresh);
        toast.success("You are logged in")
        console.log("Logged in Successfully")

    }catch(error){
        console.log("Login Failed",error)
    }

};
return (
  <div className="login-container">
    <ToastContainer />

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

        <button>Login</button>
      </form>
    </div>
  </div>
);

}

export default Login