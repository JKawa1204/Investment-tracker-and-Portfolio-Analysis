// src/services/api.ts
const API_URL = 'http://localhost:5000';

export async function fetchPortfolio(): Promise<{ id: string; name: string; price: number; sector: string }[]> {
  const response = await fetch(`${API_URL}/portfolio`);
  return response.json();
}

export async function fetchRiskAlerts(): Promise<string[]> {
  const response = await fetch(`${API_URL}/alerts`);
  return response.json();
}

export async function fetchAssetDetails(id: string): Promise<{ id: string; name: string; price: number; sector: string; transactions: { date: string; type: string; amount: number }[] }> {
  const response = await fetch(`${API_URL}/asset/${id}`);
  return response.json();
}
