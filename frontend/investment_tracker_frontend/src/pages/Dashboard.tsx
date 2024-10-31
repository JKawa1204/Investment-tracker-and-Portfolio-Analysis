// src/pages/Dashboard.tsx
import React, { useEffect, useState } from 'react';
import AssetCard from '../components/AssetCard';
import PortfolioGraph from '../components/Portfoliograph'
import RiskAlerts from '../components/RiskAlerts';
import { fetchPortfolio, fetchRiskAlerts } from '../services/Api';

interface Asset {
  id: string;
  name: string;
  price: number;
  sector: string;
}

const Dashboard: React.FC = () => {
  const [portfolio, setPortfolio] = useState<Asset[]>([]);
  const [alerts, setAlerts] = useState<string[]>([]);

  useEffect(() => {
    async function loadData() {
      const portfolioData = await fetchPortfolio();
      const alertsData = await fetchRiskAlerts();
      setPortfolio(portfolioData);
      setAlerts(alertsData);
    }
    loadData();
  }, []);

  return (
    <div className="dashboard">
      <h2>Dashboard</h2>
      <PortfolioGraph data={portfolio.map((asset) => ({ name: asset.name, value: asset.price }))} />
      <RiskAlerts alerts={alerts} />
      <div className="assets">
        {portfolio.map((asset) => (
          <AssetCard key={asset.id} asset={asset} />
        ))}
      </div>
    </div>
  );
};

export default Dashboard;
