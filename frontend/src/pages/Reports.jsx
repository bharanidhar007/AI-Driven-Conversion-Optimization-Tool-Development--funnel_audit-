import React, {useEffect, useState} from 'react';
import axios from 'axios';

export default function Reports(){
  const [reports, setReports] = useState([]);
  const token = localStorage.getItem('access');
  useEffect(()=>{
    if(!token) return;
    axios.get('/api/reports/', {headers:{Authorization:`Bearer ${token}`}})
      .then(r=> setReports(r.data))
      .catch(e=> console.error(e));
  }, [token]);

  return (
    <div style={{padding:20}}>
      <h1>Your Reports</h1>
      <ul>
        {reports.map(r=> (
          <li key={r.id}>
            <b>{r.url}</b> — {r.status} — {r.score || 'n/a'} — <a href={`/report/${r.id}`}>View</a>
          </li>
        ))}
      </ul>
    </div>
  );
}
