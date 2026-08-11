import { useEffect, useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from './assets/vite.svg'
import heroImg from './assets/hero.png'
import './App.css'

function App() {
  const [applications, setApplications] = useState([]);
  const [company, setCompany] = useState("");
  const [roleTitle, setRoleTitle] = useState("");
  const [status, setStatus] = useState("applied");

  useEffect(() => {
    fetch("http://localhost:8000/applications")
      .then(response => response.json())
      .then(data => {
        setApplications(data);
        console.log(data);
      });
  }, []);

  function handleSubmit(e) {
    e.preventDefault();

    fetch("http://localhost:8000/applications", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({"company" : company, "role_title" : roleTitle, "status": status})
    })
      .then(response => response.json())
      .then(data => {
        setApplications([...applications,data]);
        setCompany("");
        setRoleTitle("");
        setStatus("applied");
      })
  }

  async function handleStatusChange(targetId, newStatus) {

    const response = await fetch(`http://localhost:8000/applications/${targetId}`, {
      method: "PATCH",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({"status": newStatus})
    });
    const data = await response.json();

    const updatedApplications = applications.map((app) => {
      if (app.id === targetId) {
        return data
      }

      return app
    });

    setApplications(updatedApplications);
  }

  async function handleDelete(targetId) {
    const response = await fetch (`http://localhost:8000/applications/${targetId}`, {
      method: "DELETE"
    });

    const updatedApplications = applications.filter((app) => app.id != targetId);

    setApplications(updatedApplications);
  }

  return (
    <div>
      <h1>Job Application Tracker</h1>

      <ul>
        {applications.map((app) => (
          <li key= {app.id}>{app.company} - {app.role_title} - 

          <select 
            value={app.status} 
            onChange={(e) => handleStatusChange(app.id,e.target.value)}
          >
            <option value="applied">Applied</option>
            <option value="interviewing">Interviewing</option>
            <option value="offer">Offer</option>
            <option value="rejected">Rejected</option>
          </select>

          <button onClick={() => handleDelete(app.id)}>🗑</button>
          </li>
        ))}
      </ul>

      <form onSubmit={handleSubmit}>
        <input 
          value={company}
          onChange={(e) => setCompany(e.target.value)}
          placeholder='Company'
        />

        <input 
          value={roleTitle}
          onChange={(e) => setRoleTitle(e.target.value)}
          placeholder='Role Title'
        />

        <select value={status} onChange={(e) => setStatus(e.target.value)}>
          <option value="applied">Applied</option>
          <option value="interviewing">Interviewing</option>
          <option value="offer">Offer</option>
          <option value="rejected">Rejected</option>
        </select>

        <button type="submit">Add Application</button>
      </form>
    </div>
  );
}

export default App
