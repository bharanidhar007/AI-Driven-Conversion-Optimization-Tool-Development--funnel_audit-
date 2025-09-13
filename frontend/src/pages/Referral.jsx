import React, {useEffect, useState} from 'react';
import axios from 'axios';

export default function Referral(){
  const [ref, setRef] = useState(null);
  const token = localStorage.getItem('access');
  useEffect(()=>{
    if(!token) return;
    axios.get('/api/me/referral/', {headers:{Authorization:`Bearer ${token}`}})
      .then(r=> setRef(r.data))
      .catch(e=> console.error(e));
  }, [token]);

  const redeem = async () => {
    const code = prompt('Enter referral code to redeem:');
    if(!code) return;
    try{
      const res = await axios.post('/api/me/redeem/', {code}, {headers:{Authorization:`Bearer ${token}`}});
      alert(JSON.stringify(res.data));
    }catch(e){
      alert('Redeem failed: ' + (e.response?.data || e.message));
    }
  }

  if(!ref) return <div>Loading...</div>;
  return (
    <div style={{padding:20}}>
      <h1>Referral</h1>
      <p>Your referral code: <b>{ref.referral_code}</b></p>
      <p>Your credits: <b>{ref.credits}</b></p>
      <button onClick={redeem}>Redeem a code</button>
      <p>Share this link: <code>{window.location.origin}/signup?ref={ref.referral_code}</code></p>
    </div>
  );
}
