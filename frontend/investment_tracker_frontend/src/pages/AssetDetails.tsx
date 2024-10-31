// src/pages/AssetDetails.tsx
import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import TransactionList from '../components/TransactionList';
import { fetchAssetDetails } from '../services/Api';

interface Asset {
  id: string;
  name: string;
  price: number;
  sector: string;
  transactions: { date: string; type: string; amount: number }[];
}

const AssetDetails: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [asset, setAsset] = useState<Asset | null>(null);

  useEffect(() => {
    async function loadData() {
      if (id) {
        const assetData = await fetchAssetDetails(id);
        setAsset(assetData);
      }
    }
    loadData();
  }, [id]);

  if (!asset) return <div>Loading...</div>;

  return (
    <div className="asset-details">
      <h2>{asset.name}</h2>
      <p>Price: ${asset.price}</p>
      <p>Sector: {asset.sector}</p>
      <TransactionList transactions={asset.transactions} />
    </div>
  );
};

export default AssetDetails;
