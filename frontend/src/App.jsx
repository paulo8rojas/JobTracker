import { useEffect, useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from './assets/vite.svg'
import heroImg from './assets/hero.png'
import './App.css'

function App() {
  const [applications, setApplications] = useState([]);

  useEffect(() => {
    fetch("http://localhost:8000/applications")
      .then(response => response.json())
      .then(data => {
        setApplications(data);
        console.log(data);
      });
  }, []);

  return (
    <div>
      <h1>Job Application Tracker</h1>

      <ul>
        {applications.map((app) => (
          <li key= {app.id}>{app.company} - {app.role_title}</li>
        ))}
      </ul>
    </div>
  );
}

export default App
