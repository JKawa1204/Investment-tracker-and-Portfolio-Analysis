// src/components/RiskAlerts.tsx
import React from 'react';

interface RiskAlertsProps {
  alerts: string[];
}

const RiskAlerts: React.FC<RiskAlertsProps> = ({ alerts }) => (
  <div className="risk-alerts">
    <h3>Risk Alerts</h3>
    {alerts.length ? (
      alerts.map((alert, index) => <p key={index}>{alert}</p>)
    ) : (
      <p>No recent alerts</p>
    )}
  </div>
);

export default RiskAlerts;
