// src/components/AssetCard.tsx
import React from 'react';
import { Link } from 'react-router-dom';

interface Asset {
  id: string;
  name: string;
  price: number;
  sector: string;
}

interface AssetCardProps {
  asset: Asset;
}

const AssetCard: React.FC<AssetCardProps> = ({ asset }) => (
  <div className="asset-card">
    <h3>{asset.name}</h3>
    <p>Current Price: ${asset.price}</p>
    <p>Sector: {asset.sector}</p>
    <Link to={`/asset/${asset.id}`}>View Details</Link>
  </div>
);

export default AssetCard;
