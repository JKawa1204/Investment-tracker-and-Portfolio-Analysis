// src/components/PortfolioGraph.tsx
import React from 'react';

interface PortfolioGraphProps {
  data: Array<{ name: string; value: number }>;
}

const PortfolioGraph: React.FC<PortfolioGraphProps> = ({ data }) => {
  return (
    <div className="portfolio-graph">
      <h3>Portfolio Distribution</h3>
      <div>Graph Visualization Coming Soon</div>
    </div>
  );
};

export default PortfolioGraph;
