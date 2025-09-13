import React, {useState} from 'react';
import axios from 'axios';

export function Signup({onAuth}) {
  const [username,setUsername]=useState('demo_user_' + Math.random().toString(36).slice(2,8));
  const [email,setEmail]=useState('');
  const [password,setPassword]=useState('Password123!');
  const [referral,setReferral]=useState('');

  async function register(){
    try{
      const res = await axios.post('/api/register/', {username, email, password, referral_code: referral});
      localStorage.setItem('access', res.data.access);
      localStorage.setItem('refresh', res.data.refresh);
      onAuth && onAuth();
    }catch(e){
      alert('Register failed: ' + (e.response?.data || e.message));
    }
  }

  return (
    <div style={{border:'1px solid #ddd', padding:12, marginBottom:12}}>
      <h3>Sign up</h3>
      <input value={username} onChange={e=>setUsername(e.target.value)} placeholder="username"/><br/>
      <input value={email} onChange={e=>setEmail(e.target.value)} placeholder="email"/><br/>
      <input value={password} onChange={e=>setPassword(e.target.value)} placeholder="password"/><br/>
      <input value={referral} onChange={e=>setReferral(e.target.value)} placeholder="referral code (optional)"/><br/>
      <button onClick={register}>Create account</button>
    </div>
  );
}

export function Login({onAuth}) {
  const [username,setUsername]=useState('');
  const [password,setPassword]=useState('');

  async function login(){
    try{
      const res = await axios.post('/api/token/', {username, password});
      localStorage.setItem('access', res.data.access);
      localStorage.setItem('refresh', res.data.refresh);
      onAuth && onAuth();
    }catch(e){
      alert('Login failed: ' + (e.response?.data || e.message));
    }
  }

  return (
    <div style={{border:'1px solid #ddd', padding:12, marginBottom:12}}>
      <h3>Login</h3>
      <input value={username} onChange={e=>setUsername(e.target.value)} placeholder="username"/><br/>
      <input value={password} onChange={e=>setPassword(e.target.value)} placeholder="password"/><br/>
      <button onClick={login}>Login</button>
    </div>
  );
}
