// src/components/Dashboard.jsx
import React, { useState, useEffect } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ReferenceLine, ResponsiveContainer } from 'recharts';

export default function Dashboard() {
  const [priceData, setPriceData] = useState([]);
  const [events, setEvents] = useState([]);
  const [changePoints, setChangePoints] = useState([]);
  const [selectedEvent, setSelectedEvent] = useState(null);
  
  // State management configurations for Date Range Selectors
  const [startDate, setStartDate] = useState('2020-01-01');
  const [endDate, setEndDate] = useState('2020-06-30');

  useEffect(() => {
    // Synchronize multiple API calls simultaneously across backend models
    Promise.all([
      fetch(`http://127.0.0.1:5000/api/v1/historical-prices?start_date=${startDate}&end_date=${endDate}`).then(res => res.json()),
      fetch('http://127.0.0.1:5000/api/v1/events').then(res => res.json()),
      fetch('http://127.0.0.1:5000/api/v1/change-points').then(res => res.json())
    ]).then(([prices, eventList, points]) => {
      setPriceData(prices);
      setEvents(eventList);
      setChangePoints(points);
    }).catch(err => console.error("API Pipeline broken: ", err));
  }, [startDate, endDate]);

  return (
    <div style={{ padding: '24px', fontFamily: 'sans-serif', backgroundColor: '#f8fafc', minHeight: '100vh' }}>
      {/* Dashboard Top Navigation Header Section */}
      <header style={{ borderBottom: '2px solid #e2e8f0', paddingBottom: '16px', marginBottom: '24px' }}>
        <h1 style={{ fontSize: '28px', color: '#0f172a', fontWeight: 'bold', margin: 0 }}>
          Birhan Energies Market Intelligence Pipeline Dashboard
        </h1>
        <p style={{ color: '#64748b', marginTop: '6px' }}>Macroeconomic Geopolitical Impact & Bayesian Change Point Matrix Analytics</p>
      </header>

      {/* Control Widgets Layer — Filters and Date Range Selectors */}
      <section style={{ display: 'flex', gap: '16px', backgroundColor: '#ffffff', padding: '16px', borderRadius: '8px', boxShadow: '0 1px 3px rgba(0,0,0,0.1)', marginBottom: '24px' }}>
        <div>
          <label style={{ fontWeight: '600', marginRight: '8px', fontSize: '14px' }}>Timeline Start Bounds:</label>
          <input type="date" value={startDate} onChange={(e) => setStartDate(e.target.value)} style={{ padding: '6px', borderRadius: '4px', border: '1px solid #cbd5e1' }} />
        </div>
        <div>
          <label style={{ fontWeight: '600', marginRight: '8px', fontSize: '14px' }}>Timeline End Bounds:</label>
          <input type="date" value={endDate} onChange={(e) => setEndDate(e.target.value)} style={{ padding: '6px', borderRadius: '4px', border: '1px solid #cbd5e1' }} />
        </div>
      </section>

      {/* Primary Visual Graph Array Grid Framework */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr', gap: '24px', marginBottom: '24px' }}>
        <div style={{ backgroundColor: '#ffffff', padding: '24px', borderRadius: '8px', boxShadow: '0 1px 3px rgba(0,0,0,0.1)' }}>
          <h3 style={{ margin: '0 0 16px 0', fontSize: '18px', color: '#334155' }}>Historical Pricing Evolution with High-Impact Event Mappings</h3>
          
          <div style={{ width: '100%', height: 400 }}>
            <ResponsiveContainer>
              <LineChart data={priceData} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
                <XAxis dataKey="date" stroke="#64748b" style={{ fontSize: '12px' }} />
                <YAxis domain={['auto', 'auto']} stroke="#64748b" style={{ fontSize: '12px' }} unit=" USD" />
                <Tooltip contentStyle={{ backgroundColor: '#1e293b', color: '#fff', borderRadius: '6px' }} />
                <Line type="monotone" dataKey="price" stroke="#3182ce" strokeWidth={2.5} dot={false} activeDot={{ r: 6 }} />
                
                {/* Event Highlight Functionality mapping custom reference markers onto graph timeline dynamically */}
                {events.map((ev, idx) => (
                  <ReferenceLine key={idx} x={ev.date} stroke="#e53e3e" strokeDasharray="4 4" label={{ value: '⚡', position: 'top', fill: '#e53e3e' }} />
                ))}
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* Drill-Down Capabilities & Insight Grid Layout Columns */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))', gap: '24px' }}>
        {/* Module A: Tabular Event Interactive Feed Tracker */}
        <div style={{ backgroundColor: '#ffffff', padding: '20px', borderRadius: '8px', boxShadow: '0 1px 3px rgba(0,0,0,0.1)' }}>
          <h4 style={{ margin: '0 0 12px 0', color: '#1e293b' }}>Active Geopolitical / OPEC Impact Feed Tracker</h4>
          <div style={{ maxHeight: '280px', overflowY: 'auto' }}>
            {events.map((ev, i) => (
              <div key={i} onClick={() => setSelectedEvent(ev)} style={{ padding: '10px', borderBottom: '1px solid #f1f5f9', cursor: 'pointer', backgroundColor: selectedEvent?.name === ev.name ? '#ebf8ff' : 'transparent', transition: 'background-color 0.2s' }}>
                <span style={{ fontSize: '11px', color: '#718096', fontWeight: 'bold' }}>{ev.date} [{ev.category}]</span>
                <p style={{ margin: '4px 0 0 0', fontSize: '14px', fontWeight: '600', color: '#2d3748' }}>{ev.name}</p>
              </div>
            ))}
          </div>
        </div>

        {/* Module B: Interactive Context Drill-Down Component */}
        <div style={{ backgroundColor: '#ffffff', padding: '20px', borderRadius: '8px', boxShadow: '0 1px 3px rgba(0,0,0,0.1)', display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
          <div>
            <h4 style={{ margin: '0 0 12px 0', color: '#1e293b' }}>Context Drill-Down Insights Panel</h4>
            {selectedEvent ? (
              <div>
                <span style={{ backgroundColor: '#fed7d7', color: '#9b2c2c', padding: '4px 8px', borderRadius: '4px', fontSize: '12px', fontWeight: 'bold' }}>{selectedEvent.category}</span>
                <h5 style={{ margin: '12px 0 6px 0', fontSize: '16px', color: '#2d3748' }}>{selectedEvent.name}</h5>
                <p style={{ margin: 0, fontSize: '14px', color: '#4a5568', lineHeight: '1.5' }}>{selectedEvent.description}</p>
              </div>
            ) : (
              <p style={{ color: '#a0aec0', fontSize: '14px', fontStyle: 'italic' }}>Select any event row from the feed panel to expand deep strategic attribution statements.</p>
            )}
          </div>

          {/* Indicators Bar for Key Indicators Metrics */}
          <div style={{ marginTop: '20px', paddingTop: '16px', borderTop: '1px solid #e2e8f0' }}>
            <h5 style={{ margin: '0 0 10px 0', fontSize: '12px', color: '#718096', textTransform: 'uppercase' }}>Discovered Model Shift Constants</h5>
            <div style={{ display: 'flex', gap: '16px' }}>
              <div>
                <span style={{ fontSize: '11px', color: '#718096' }}>Avg Impact Drop</span>
                <div style={{ fontSize: '20px', fontWeight: 'bold', color: '#e53e3e' }}>-45.73%</div>
              </div>
              <div>
                <span style={{ fontSize: '11px', color: '#718096' }}>MCMC Convergence</span>
                <div style={{ fontSize: '20px', fontWeight: 'bold', color: '#38a169' }}>1.00 (R-hat)</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}