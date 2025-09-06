// src/components/PredictionPage/PredictionPage.jsx
import React, { useState, useRef, useEffect } from 'react';
import Chart from 'chart.js/auto';
import apiService from '../../Service/apiService';
import './PredictionPage.css';

const PredictionPage = () => {
  const [predictionMode, setPredictionMode] = useState('basic');
  const [results, setResults] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const chartRef = useRef(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');
    setResults(null);

    const formData = new FormData(e.target);
    const data = Object.fromEntries(formData.entries());

    // --- GATHER AND FORMAT DATA FOR API ---
    const requestData = {
        age: parseInt(data.age, 10) || 0,
        sex: parseInt(data.sex, 10) || 0,
        genetic_history: parseInt(data.genetic_history, 10) || 0,
        noise_exposure_history: parseInt(data.noise_exposure_history, 10) || 0,
        tinnitus: parseInt(data.tinnitus, 10) || 0,
        vertigo_dizziness: parseInt(data.vertigo_dizziness, 10) || 0,
        hearing_difficulty_in_noise: parseInt(data.hearing_difficulty_in_noise, 10) || 0,
        
        // Left Ear
        ac_l_250: parseFloat(data.ac_l_250) || 0,
        ac_l_500: parseFloat(data.ac_l_500) || 0,
        ac_l_1000: parseFloat(data.ac_l_1000) || 0,
        ac_l_2000: parseFloat(data.ac_l_2000) || 0,
        ac_l_4000: parseFloat(data.ac_l_4000) || 0,
        ac_l_8000: parseFloat(data.ac_l_8000) || 0,
        bc_l_500: parseFloat(data.bc_l_500) || 0,
        bc_l_1000: parseFloat(data.bc_l_1000) || 0,
        bc_l_2000: parseFloat(data.bc_l_2000) || 0,
        bc_l_4000: parseFloat(data.bc_l_4000) || 0,
        srt_l: parseFloat(data.srt_l) || 0,
        wrs_l: parseFloat(data.wrs_l) || 0,
        tymp_type_l: data.tymp_type_l,

        // Right Ear
        ac_r_250: parseFloat(data.ac_r_250) || 0,
        ac_r_500: parseFloat(data.ac_r_500) || 0,
        ac_r_1000: parseFloat(data.ac_r_1000) || 0,
        ac_r_2000: parseFloat(data.ac_r_2000) || 0,
        ac_r_4000: parseFloat(data.ac_r_4000) || 0,
        ac_r_8000: parseFloat(data.ac_r_8000) || 0,
        bc_r_500: parseFloat(data.bc_r_500) || 0,
        bc_r_1000: parseFloat(data.bc_r_1000) || 0,
        bc_r_2000: parseFloat(data.bc_r_2000) || 0,
        bc_r_4000: parseFloat(data.bc_r_4000) || 0,
        srt_r: parseFloat(data.srt_r) || 0,
        wrs_r: parseFloat(data.wrs_r) || 0,
        tymp_type_r: data.tymp_type_r,
        
        // Optional Advanced Fields
        oae_500_present: parseInt(data.oae_500_present, 10) || 0,
        oae_1000_present: parseInt(data.oae_1000_present, 10) || 0,
        oae_4000_present: parseInt(data.oae_4000_present, 10) || 0,
        abr_wave_i_latency: parseFloat(data.abr_wave_i_latency) || 0,
        abr_wave_iii_latency: parseFloat(data.abr_wave_iii_latency) || 0,
        abr_wave_v_latency: parseFloat(data.abr_wave_v_latency) || 0,
        abr_wave_v_absent: parseInt(data.abr_wave_v_absent, 10) || 0,
    };

    try {
      const response = await apiService.getPrediction(requestData);
      // Transform the new backend response to match frontend expectations
      setResults({
        hearingLoss: response.data.hearing_loss,
        lossType: response.data.hearing_loss_type,
        lossSeverity: response.data.hearing_loss_severity,
        confidenceScores: response.data.confidence_scores,
        clinicalSummary: response.data.clinical_summary,
        audiogramData: {
            ac_r: [data.ac_r_250, data.ac_r_500, data.ac_r_1000, data.ac_r_2000, data.ac_r_4000, data.ac_r_8000],
            bc_r: [null, data.bc_r_500, data.bc_r_1000, data.bc_r_2000, data.bc_r_4000, null],
            ac_l: [data.ac_l_250, data.ac_l_500, data.ac_l_1000, data.ac_l_2000, data.ac_l_4000, data.ac_l_8000],
            bc_l: [null, data.bc_l_500, data.bc_l_1000, data.bc_l_2000, data.bc_l_4000, null],
        }
      });
    } catch (err) {
      setError('Prediction failed. The backend service may be unavailable.');
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    if (results && results.audiogramData) {
      if (chartRef.current) {
        chartRef.current.destroy();
      }
      const ctx = document.getElementById('audiogramChart').getContext('2d');
      const audiogramData = results.audiogramData;
      
      chartRef.current = new Chart(ctx, {
        type: 'line',
        data: {
          labels: ['250', '500', '1000', '2000', '4000', '8000'],
          datasets: [
            { label: 'Right Ear AC', data: audiogramData.ac_r, borderColor: 'red', backgroundColor: 'red', pointStyle: 'circle', pointRadius: 6, showLine: true },
            { label: 'Left Ear AC', data: audiogramData.ac_l, borderColor: 'blue', backgroundColor: 'blue', pointStyle: 'crossRot', pointRadius: 6, showLine: true },
            { label: 'Right Ear BC', data: audiogramData.bc_r, borderColor: 'red', backgroundColor: 'red', pointStyle: 'triangle', pointRotation: 90, pointRadius: 6, showLine: false },
            { label: 'Left Ear BC', data: audiogramData.bc_l, borderColor: 'blue', backgroundColor: 'blue', pointStyle: 'triangle', pointRotation: -90, pointRadius: 6, showLine: false }
          ]
        },
        options: {
          responsive: true, maintainAspectRatio: false,
          scales: {
            y: { reverse: true, min: -10, max: 120, ticks: { stepSize: 10 }, title: { display: true, text: 'Hearing Level (dB HL)' } },
            x: { title: { display: true, text: 'Frequency (Hz)' }, position: 'top' }
          },
          plugins: {
            title: { display: true, text: 'Patient Audiogram', font: { size: 18 } },
            legend: { position: 'bottom' }
          }
        }
      });
    }
  }, [results]);


  return (
    <div className="prediction-page">
      <section className="prediction-hero">
        <div className="prediction-hero-content">
          <h1 className="prediction-hero-title">AI-Powered Prediction</h1>
          <p className="prediction-hero-subtitle">
            Choose your prediction method and input patient data to receive an instant analysis.
          </p>
        </div>
      </section>

      <section className="prediction-main">
        <div className="switcher-container">
          <div className={`switcher-background ${predictionMode === 'advanced' ? 'advanced-active' : ''}`}></div>
          <button onClick={() => setPredictionMode('basic')} className={predictionMode === 'basic' ? 'active' : ''}>
            Basic Prediction
          </button>
          <button onClick={() => setPredictionMode('advanced')} className={predictionMode === 'advanced' ? 'active' : ''}>
            Advanced Prediction
          </button>
        </div>

        {predictionMode === 'basic' && (
          <div className="form-container">
            <form onSubmit={handleSubmit}>
              <fieldset className="form-section">
                <legend className="section-title">Patient Demographics</legend>
                <div className="grid-inputs">
                  <div className="input-wrapper"><label>Age</label><input name="age" type="number" placeholder="e.g., 55" required /></div>
                  <div className="input-wrapper"><label>Sex</label><select name="sex"><option value="1">Male</option><option value="0">Female</option></select></div>
                  <div className="input-wrapper"><label>Genetic History</label><select name="genetic_history"><option value="0">No</option><option value="1">Yes</option></select></div>
                  <div className="input-wrapper"><label>Noise Exposure</label><select name="noise_exposure_history"><option value="0">No</option><option value="1">Yes</option></select></div>
                  <div className="input-wrapper"><label>Tinnitus</label><select name="tinnitus"><option value="0">No</option><option value="1">Yes</option></select></div>
                  <div className="input-wrapper"><label>Vertigo/Dizziness</label><select name="vertigo_dizziness"><option value="0">No</option><option value="1">Yes</option></select></div>
                  <div className="input-wrapper"><label>Difficulty in Noise</label><select name="hearing_difficulty_in_noise"><option value="0">No</option><option value="1">Yes</option></select></div>
                </div>
              </fieldset>
              
              <fieldset className="form-section">
                <legend className="section-title">Audiological Metrics</legend>
                <div className="dual-column">
                  <div className="column">
                    <h4 className="column-title">Left Ear</h4>
                    <label>AC 250Hz</label><input name="ac_l_250" type="number" placeholder="dB" required /><label>AC 500Hz</label><input name="ac_l_500" type="number" placeholder="dB" required /><label>AC 1000Hz</label><input name="ac_l_1000" type="number" placeholder="dB" required /><label>AC 2000Hz</label><input name="ac_l_2000" type="number" placeholder="dB" required /><label>AC 4000Hz</label><input name="ac_l_4000" type="number" placeholder="dB" required /><label>AC 8000Hz</label><input name="ac_l_8000" type="number" placeholder="dB" required /><label>BC 500Hz</label><input name="bc_l_500" type="number" placeholder="dB" required /><label>BC 1000Hz</label><input name="bc_l_1000" type="number" placeholder="dB" required /><label>BC 2000Hz</label><input name="bc_l_2000" type="number" placeholder="dB" required /><label>BC 4000Hz</label><input name="bc_l_4000" type="number" placeholder="dB" required /><label>SRT (dB)</label><input name="srt_l" type="number" placeholder="dB" required /><label>WRS (%)</label><input name="wrs_l" type="number" placeholder="%" required /><label>Tymp Type</label><select name="tymp_type_l"><option>A</option><option>B</option><option>C</option><option>As</option><option>Ad</option></select>
                  </div>
                  <div className="column">
                    <h4 className="column-title">Right Ear</h4>
                    <label>AC 250Hz</label><input name="ac_r_250" type="number" placeholder="dB" required /><label>AC 500Hz</label><input name="ac_r_500" type="number" placeholder="dB" required /><label>AC 1000Hz</label><input name="ac_r_1000" type="number" placeholder="dB" required /><label>AC 2000Hz</label><input name="ac_r_2000" type="number" placeholder="dB" required /><label>AC 4000Hz</label><input name="ac_r_4000" type="number" placeholder="dB" required /><label>AC 8000Hz</label><input name="ac_r_8000" type="number" placeholder="dB" required /><label>BC 500Hz</label><input name="bc_r_500" type="number" placeholder="dB" required /><label>BC 1000Hz</label><input name="bc_r_1000" type="number" placeholder="dB" required /><label>BC 2000Hz</label><input name="bc_r_2000" type="number" placeholder="dB" required /><label>BC 4000Hz</label><input name="bc_r_4000" type="number" placeholder="dB" required /><label>SRT (dB)</label><input name="srt_r" type="number" placeholder="dB" required /><label>WRS (%)</label><input name="wrs_r" type="number" placeholder="%" required /><label>Tymp Type</label><select name="tymp_type_r"><option>A</option><option>B</option><option>C</option><option>As</option><option>Ad</option></select>
                  </div>
                </div>
              </fieldset>

              <fieldset className="form-section">
                <legend className="section-title">Advanced Tests (Optional)</legend>
                <div className="grid-inputs">
                    <div className="input-wrapper"><label>OAE 500Hz</label><select name="oae_500_present"><option value="">N/A</option><option value="1">Present</option><option value="0">Absent</option></select></div>
                    <div className="input-wrapper"><label>OAE 1000Hz</label><select name="oae_1000_present"><option value="">N/A</option><option value="1">Present</option><option value="0">Absent</option></select></div>
                    <div className="input-wrapper"><label>OAE 4000Hz</label><select name="oae_4000_present"><option value="">N/A</option><option value="1">Present</option><option value="0">Absent</option></select></div>
                    <div className="input-wrapper"><label>ABR Wave I Latency (ms)</label><input name="abr_wave_i_latency" type="number" step="0.01" placeholder="e.g., 1.55" /></div>
                    <div className="input-wrapper"><label>ABR Wave III Latency (ms)</label><input name="abr_wave_iii_latency" type="number" step="0.01" placeholder="e.g., 3.75" /></div>
                    <div className="input-wrapper"><label>ABR Wave V Latency (ms)</label><input name="abr_wave_v_latency" type="number" step="0.01" placeholder="e.g., 5.65" /></div>
                    <div className="input-wrapper"><label>ABR Wave V</label><select name="abr_wave_v_absent"><option value="">N/A</option><option value="0">Present</option><option value="1">Absent</option></select></div>
                </div>
              </fieldset>

              <div className="submit-container">
                <button type="submit" className="submit-button" disabled={isLoading}>
                  {isLoading ? 'Analyzing...' : 'Generate Prediction'}
                </button>
              </div>
            </form>
          </div>
        )}

        {predictionMode === 'advanced' && (
          <div className="advanced-placeholder">
            <h2>Advanced Prediction</h2>
            <p>This feature for uploading audiogram images is coming soon.</p>
          </div>
        )}
      </section>

      {error && <div className="error-banner">{error}</div>}
      {results && (
        <section className="results-section">
            <h2 className="section-title">Prediction Report</h2>
            <div className="results-grid">
                <div className="results-summary">
                    <div className="result-card">
                        <h3>Hearing Loss</h3>
                        <p className={results.hearingLoss === 'Yes' ? 'loss-yes' : 'loss-no'}>
                            {results.hearingLoss}
                        </p>
                        {results.confidenceScores && (
                            <span className="confidence-score">
                                Confidence: {(results.confidenceScores.hearing_loss * 100).toFixed(1)}%
                            </span>
                        )}
                    </div>
                    <div className="result-card">
                        <h3>Predicted Type</h3>
                        <p>{results.lossType}</p>
                        {results.confidenceScores && (
                            <span className="confidence-score">
                                Confidence: {(results.confidenceScores.hearing_loss_type * 100).toFixed(1)}%
                            </span>
                        )}
                    </div>
                    <div className="result-card">
                        <h3>Predicted Severity</h3>
                        <p>{results.lossSeverity}</p>
                        {results.confidenceScores && (
                            <span className="confidence-score">
                                Confidence: {(results.confidenceScores.hearing_loss_severity * 100).toFixed(1)}%
                            </span>
                        )}
                    </div>
                </div>
                <div className="audiogram-container">
                    <canvas id="audiogramChart"></canvas>
                </div>
            </div>
            
            {/* Clinical Summary Section */}
            {results.clinicalSummary && (
                <div className="clinical-summary">
                    <h3 className="section-title">Clinical Summary</h3>
                    <div className="clinical-metrics">
                        <div className="metric-group">
                            <div className="metric">
                                <span className="metric-label">Left Ear PTA:</span>
                                <span className="metric-value">{results.clinicalSummary.pta_left} dB HL</span>
                            </div>
                            <div className="metric">
                                <span className="metric-label">Right Ear PTA:</span>
                                <span className="metric-value">{results.clinicalSummary.pta_right} dB HL</span>
                            </div>
                            <div className="metric">
                                <span className="metric-label">Asymmetry:</span>
                                <span className="metric-value">{results.clinicalSummary.asymmetry} dB</span>
                            </div>
                        </div>
                        <div className="metric-group">
                            <div className="metric">
                                <span className="metric-label">Left Air-Bone Gap:</span>
                                <span className="metric-value">{results.clinicalSummary.air_bone_gap_left} dB</span>
                            </div>
                            <div className="metric">
                                <span className="metric-label">Right Air-Bone Gap:</span>
                                <span className="metric-value">{results.clinicalSummary.air_bone_gap_right} dB</span>
                            </div>
                        </div>
                    </div>
                    
                    {results.clinicalSummary.clinical_notes && results.clinicalSummary.clinical_notes.length > 0 && (
                        <div className="clinical-notes">
                            <h4>Clinical Notes:</h4>
                            <ul>
                                {results.clinicalSummary.clinical_notes.map((note, index) => (
                                    <li key={index}>{note}</li>
                                ))}
                            </ul>
                        </div>
                    )}
                </div>
            )}
        </section>
      )}
    </div>
  );
};

export default PredictionPage;