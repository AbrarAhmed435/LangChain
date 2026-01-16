import { useState ,useEffect} from "react";
import api from "../api/axios";
import './users.css'

interface User {
  id: number;
  email: string;
}


export default function Users(){
    const [loading,setLoading]=useState(true)
    const [users,setUsers]=useState<User[]>([])

useEffect(()=>{
    const booststrap=async ()=>{
        try{
            const res=await api.get("/get-users/");
            setUsers(res.data)
        }finally{
            setLoading(false)
        }
    }
    booststrap();
},[])

if (loading){
    return <p className="loading">Loading users...</p>
}


    return (
        <div className="user-list">
            <h2>Users</h2>
            
            {users.length>0 ? (
                users.map((user)=>(
                    <p key={user.id} className="user_Element">{user.email}</p>
                ))
            ):(
                <p>You are not authorized to see this</p>
            )
        }
        </div>
    )
}