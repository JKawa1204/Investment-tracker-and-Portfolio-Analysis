// src/components/TransactionList.tsx
import React from 'react';

interface Transaction {
  date: string;
  type: string;
  amount: number;
}

interface TransactionListProps {
  transactions: Transaction[];
}

const TransactionList: React.FC<TransactionListProps> = ({ transactions }) => (
  <div className="transaction-list">
    <h3>Transaction History</h3>
    <ul>
      {transactions.map((transaction, index) => (
        <li key={index}>
          {transaction.date} - {transaction.type} - ${transaction.amount}
        </li>
      ))}
    </ul>
  </div>
);

export default TransactionList;
