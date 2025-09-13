import Reports from './pages/Reports';
import ReportView from './pages/ReportView';
import Referral from './pages/Referral';
import React, {useState} from 'react';
import axios from 'axios';
import { Signup, Login } from './Auth';
export default function App(){
  const [url, setUrl] = useState('');
  const [report, setReport] = useState(null);
  const [token, setToken] = useState(localStorage.getItem('access') || '');
  const [profile, setProfile] = React.useState(null);
  async function loginDemo(){
    // demo login to get token - you should implement real auth
    alert('For demo: create a user via Django admin or implement signup. This scaffold expects JWT auth endpoints.');
  }

async function fetchProfile(){
  const t = localStorage.getItem('access');
  if(!t) return;
  try{
    const r = await axios.get('/api/profile/', {headers:{Authorization:`Bearer ${t}`}});
    setProfile(r.data);
  }catch(e){
    console.error('profile fetch error', e);
  }
}

React.useEffect(()=>{ fetchProfile(); }, [token]);

function onAuth(){
  setToken(localStorage.getItem('access'));
  fetchProfile();
}


async function buyCredits(){
  const t = localStorage.getItem('access');
  if(!t){ alert('Please login to purchase credits.'); return; }
  try{
    // Request backend to create a checkout session
    const res = await axios.post('/api/create-checkout-session/', {credits: 10, unit_price_cents: 50}, {headers:{Authorization:`Bearer ${t}`}});
    if(res.data.session_url){
      window.location.href = res.data.session_url;
    } else {
      alert('Failed to create checkout session');
    }
  }catch(e){
    alert('Checkout error: ' + (e.response?.data?.error || e.message));
  }
}

  async function submit(){
    if(!token){ alert('Please login or set token in local storage (access)'); return;}
    try{
      const res = await axios.post('/api/submit/', {url}, {headers:{Authorization:`Bearer ${token}`}});
      const id = res.data.id || res.data.report_id;
      // poll for report
      const iv = setInterval(async ()=>{
        try{
          const r = await axios.get(`/api/report/${id}/`, {headers:{Authorization:`Bearer ${token}`}});
          if(r.data.status === 'done' || r.data.status === 'failed'){
            setReport(r.data);
            clearInterval(iv);
          }
        }catch(e){
          console.error(e);
        }
      },2000);
    }catch(e){
      console.error(e);
      alert('Submit failed: ' + e.message);
    }
  }
  return (
    <div style={{maxWidth:800, margin:'40px auto', fontFamily:'Arial, sans-serif'}}>
      <h1>Funnel Audit (React + Django)</h1>
      <p>Note: This scaffold requires a Django backend running at the same origin (/api/...).</p>
      <div style={{marginBottom:12}}>
        <input value={url} onChange={e=>setUrl(e.target.value)} placeholder="https://example.com/landing" style={{width:'100%', padding:8}}/>
      </div>
      <div style={{display:'flex', gap:8}}>
        <button onClick={submit} style={{padding:'8px 12px'}}>Analyze</button>
        <button onClick={loginDemo} style={{padding:'8px 12px'}}>How to login</button>
      </div>
      {profile && (
            <div style={{marginBottom:12}}>Credits: {profile.credits} &nbsp; Referral code: <b>{profile.referral_code}</b></div>
          )}
          {report && (
        <div style={{marginTop:20}}>
          <h2>Report</h2>
          <pre style={{whiteSpace:'pre-wrap'}}>{JSON.stringify(report, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}
