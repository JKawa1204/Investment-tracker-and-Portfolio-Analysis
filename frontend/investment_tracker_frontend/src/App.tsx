// src/App.js
import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Dashboard from "./pages/Dashboard";
import AssetDetails from './pages/AssetDetails';

const App = () => (
  <Router>
    <Routes>
      <Route path="/" element={<Dashboard />} />
      <Route path="/asset/:id" element={<AssetDetails />} />
    </Routes>
  </Router>
);

export default App;
