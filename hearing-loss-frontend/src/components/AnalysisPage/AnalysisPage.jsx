// src/components/AnalysisPage.jsx
import React, { useEffect, useRef } from 'react';
import Chart from 'chart.js/auto';
import './AnalysisPage.css';

const AnalysisPage = () => {
  // Use a ref to ensure charts are only initialized once
  const chartsInitialized = useRef(false);

  useEffect(() => {
    if (chartsInitialized.current) return;

    // --- Chart Color Palette ---
    const chartColors = {
        blue: 'rgba(54, 162, 235, 0.7)',
        red: 'rgba(255, 99, 132, 0.7)',
        yellow: 'rgba(255, 206, 86, 0.7)',
        green: 'rgba(75, 192, 192, 0.7)',
        purple: 'rgba(153, 102, 255, 0.7)',
        orange: 'rgba(255, 159, 64, 0.7)'
    };

    // --- Chart Initializations ---

    // 1. Hearing Loss Type Distribution (Pie Chart)
    new Chart(document.getElementById('typePieChart'), {
        type: 'pie',
        data: {
            labels: ['Sensorineural', 'Conductive', 'Normal', 'Mixed', 'Auditory Neuropathy'],
            datasets: [{
                label: 'Distribution of Loss Types',
                data: [200, 100, 100, 50, 50], // Based on our generation script
                backgroundColor: [chartColors.yellow, chartColors.blue, chartColors.green, chartColors.orange, chartColors.red],
                borderColor: '#fff',
                borderWidth: 2
            }]
        },
        options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { position: 'bottom' } } }
    });

    // 2. Hearing Loss Severity Distribution
    new Chart(document.getElementById('severityChart'), {
        type: 'bar',
        data: {
            labels: ['Normal', 'Mild', 'Moderate', 'Severe', 'Profound'],
            datasets: [{
                label: 'Number of Patients',
                data: [100, 138, 192, 82, 38], // Example distribution from dataset
                backgroundColor: [chartColors.green, chartColors.yellow, chartColors.orange, chartColors.red, chartColors.purple]
            }]
        },
        options: { scales: { y: { beginAtZero: true } }, responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } } }
    });

    // 3. Age vs. Hearing Loss
    new Chart(document.getElementById('ageChart'), {
        type: 'bar',
        data: {
            labels: ['<40', '40-65', '>65'],
            datasets: [{
                label: 'No Loss', data: [85, 40, 10], backgroundColor: chartColors.green
            }, {
                label: 'Hearing Loss', data: [15, 60, 90], backgroundColor: chartColors.red
            }]
        },
        options: { scales: { x: { stacked: true }, y: { stacked: true, beginAtZero: true } }, responsive: true, maintainAspectRatio: false }
    });

    // 4. Tinnitus vs. Hearing Loss
    new Chart(document.getElementById('tinnitusChart'), {
        type: 'bar',
        data: {
            labels: ['No Tinnitus', 'Tinnitus'],
            datasets: [{
                label: 'No Loss', data: [90, 10], backgroundColor: chartColors.green
            }, {
                label: 'Hearing Loss', data: [25, 75], backgroundColor: chartColors.red
            }]
        },
        options: { indexAxis: 'y', scales: { x: { stacked: true }, y: { stacked: true } }, responsive: true, maintainAspectRatio: false }
    });

    // 5. Noise Exposure vs. Hearing Loss
    new Chart(document.getElementById('noiseChart'), {
        type: 'bar',
        data: {
            labels: ['No Exposure', 'Noise Exposure'],
            datasets: [{
                label: 'No Loss', data: [70, 30], backgroundColor: chartColors.green
            }, {
                label: 'Hearing Loss', data: [35, 65], backgroundColor: chartColors.red
            }]
        },
        options: { scales: { x: { stacked: true }, y: { stacked: true } }, responsive: true, maintainAspectRatio: false }
    });

    // 6. Word Recognition by Loss Type
    new Chart(document.getElementById('wrsChart'), {
        type: 'bar',
        data: {
            labels: ['Normal', 'Conductive', 'SNHL', 'Mixed', 'ANSD'],
            datasets: [{
                label: 'Avg. Word Recognition Score (%)',
                data: [98, 95, 75, 65, 30],
                backgroundColor: [chartColors.green, chartColors.blue, chartColors.yellow, chartColors.orange, chartColors.red]
            }]
        },
        options: { scales: { y: { beginAtZero: true, max: 100 } }, responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } } }
    });

    chartsInitialized.current = true;
  }, []);

  return (
    <div className="analysis-page">
      {/* --- Hero Section --- */}
      <section className="analysis-hero">
        <div className="analysis-hero-content">
          <h1 className="analysis-hero-title">Dataset Analysis</h1>
          <p className="analysis-hero-subtitle">
            Visualizing the trends and patterns within our hearing health dataset.
          </p>
        </div>
      </section>

      {/* --- Main Analysis Area --- */}
      <section className="analysis-main">
        <div className="analysis-grid">
          
          <div className="chart-card">
            <h3 className="chart-title">Distribution of Loss Types</h3>
            <div className="chart-wrapper">
              <canvas id="typePieChart"></canvas>
            </div>
          </div>

          <div className="chart-card">
            <h3 className="chart-title">Distribution of Severity</h3>
            <div className="chart-wrapper">
              <canvas id="severityChart"></canvas>
            </div>
          </div>

          <div className="chart-card">
            <h3 className="chart-title">Age vs. Hearing Loss</h3>
            <div className="chart-wrapper">
              <canvas id="ageChart"></canvas>
            </div>
          </div>

          <div className="chart-card">
            <h3 className="chart-title">Tinnitus vs. Hearing Loss</h3>
            <div className="chart-wrapper">
              <canvas id="tinnitusChart"></canvas>
            </div>
          </div>

          <div className="chart-card">
            <h3 className="chart-title">Noise Exposure vs. Hearing Loss</h3>
            <div className="chart-wrapper">
              <canvas id="noiseChart"></canvas>
            </div>
          </div>

          <div className="chart-card">
            <h3 className="chart-title">Word Recognition by Loss Type</h3>
            <div className="chart-wrapper">
              <canvas id="wrsChart"></canvas>
            </div>
          </div>

        </div>
      </section>
    </div>
  );
};

export default AnalysisPage;
