import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import { BrowserRouter,Route,Routes } from 'react-router-dom'
import Register from './pages/Register'
import { toast,ToastContainer } from 'react-toastify'
import Login from './pages/Logis'
import ProtectedRoute from './routes/ProtectedRoute'
import Home from './pages/Home'


function App() {
  const [count, setCount] = useState(0)

  return (
    <>
    <BrowserRouter>
    
    <Routes>
      <Route path='/register' element={<Register/>}/>
      <Route path='/login' element={<Login/>}/>
      <Route element={<ProtectedRoute/>}>
      <Route path="/home" element={<Home/>}/>
      </Route>
    </Routes>

    </BrowserRouter>
    </>
  )
}

export default App
