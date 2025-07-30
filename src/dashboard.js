// Minimal dashboard functionality (React Example)
import React, { useState, useEffect } from 'react';

function Dashboard() {
  const [status, setStatus] = useState('Loading...');

  useEffect(() => {
    fetch('/health')
      .then(response => response.json())
      .then(data => setStatus(data.status));
  }, []);

  return (
    <div>
      <h1>Integration Status</h1>
      <p>Status: {status}</p>
    </div>
  );
}

export default Dashboard;
