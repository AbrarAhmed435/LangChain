import { registerApi } from "../api/auth.api"
import { useState } from "react";
import { toast, ToastContainer } from "react-toastify";
import { useNavigate } from "react-router-dom";
import "./Register.css";


const Register=()=>{
    const [email,setEmail]=useState<string>("")
    const [password,setPassword]=useState<string>("")
    const [password2,setPassword2]=useState<string>("")
    const navigate=useNavigate()


const handleRegister=async(e:React.FormEvent<HTMLFormElement>)=>{
    e.preventDefault()
    try{
        const res=await registerApi({
            email,
            password,
            confirm_password:password2,
        });
        toast.success("Register successful! Redirecting to Login Page....", {
          onClose: () => navigate("/login"), // Navigate only after toast closes
        });
        


    }catch(error){
        console.error("Registration failed",error)

    }
}
    return (
  <div className="register-container">
    <ToastContainer />
    <div className="register-card">
      <h2>Register</h2>

      <form onSubmit={handleRegister}>
        <input
          type="email"
          placeholder="Email"
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

        <input
          type="password"
          placeholder="Confirm password"
          value={password2}
          onChange={(e) => setPassword2(e.target.value)}
          required
        />

        <button>Register</button>
      </form>
    </div>
  </div>
);

}

export default Register;