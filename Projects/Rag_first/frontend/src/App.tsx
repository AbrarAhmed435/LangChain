import { useState } from "react";
import reactLogo from "./assets/react.svg";
import viteLogo from "/vite.svg";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import Register from "./pages/Register";
import { toast, ToastContainer } from "react-toastify";
import Login from "./pages/Logis";
import ProtectedRoute from "./routes/ProtectedRoute";
import Home from "./pages/Home";
import Users from "./pages/Users";
import Dashboard from "./pages/Dashboard";
import "./index.css";
import Chat from "./pages/Chat";

function App() {
  return (
    <>
      <BrowserRouter>
        <Routes>
          <Route path="/register" element={<Register />} />
          <Route path="/login" element={<Login />} />
          <Route element={<ProtectedRoute />}>
            <Route path="/home" element={<Home />} />
            <Route path="/admin-panel" element={<Users />} />
            <Route path="/dashboard" element={<Dashboard/>} />
             <Route path="/document/:id" element={<Chat />} />
          </Route>
          <Route path="*" element={<Home />} />
        </Routes>
      </BrowserRouter>
    </>
  );
}

export default App;
