import React, {useEffect, useState} from 'react';
import axios from 'axios';
import { useParams } from 'react-router-dom';

export default function ReportView(){
  const { id } = useParams();
  const [report, setReport] = useState(null);
  const token = localStorage.getItem('access');
  useEffect(()=>{
    if(!token) return;
    axios.get(`/api/report/${id}/`, {headers:{Authorization:`Bearer ${token}`}})
      .then(r=> setReport(r.data))
      .catch(e=> console.error(e));
  }, [id, token]);

  if(!report) return <div>Loading...</div>;
  return (
    <div style={{padding:20}}>
      <h1>Report for {report.url}</h1>
      <p>Status: {report.status} | Score: {report.score}</p>
      <h2>AI Analysis</h2>
      <pre style={{whiteSpace:'pre-wrap'}}>{JSON.stringify(report.ai_analysis || report.ai_analysis?.raw || report.ai_analysis?.raw || report.ai_analysis, null, 2)}</pre>
    </div>
  );
}
